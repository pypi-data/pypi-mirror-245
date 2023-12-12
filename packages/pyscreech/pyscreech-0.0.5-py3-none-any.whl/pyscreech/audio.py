"""Class with methods for reading in, accessing, and manipulating audio waveforms"""

from __future__ import annotations

from typing import Tuple

import numpy as np
import librosa
import scipy
import soundfile as sf
import matplotlib.pyplot as plt
import soxr

from loguru import logger


class WaveformOperationException(Exception):
    pass


class AudioWaveform(object):
    """
    Object holding an audio waveform and tools to manipulate it
    """

    def __init__(self, timeseries: np.ndarray, sample_rate: float, name: str = None, start_time_sec: float = 0.0):
        """
        Initialize the AudioWaveform object

        Args:
            timeseries (np.ndarray): the waveform timeseries data
            sample_rate (float): sampling frequency of the data points in Hz
            name (str): name of the waveform (Optional)
            start_time_sec (float): start time of the waveform, which is useful for syncing up
                subsegments of two distinct waveforms. Defaults to 0.0
        """
        self.name = name
        self.timeseries = np.asarray(timeseries)
        self.sample_rate = sample_rate
        self.start_time_sec = start_time_sec  # 1000 * offset / short_ref.sample_rate

    def resample(self, new_sample_rate: float, resample_quality='VHQ') -> AudioWaveform:
        """
        Resample the with a new sampling rate

        Args:
            new_sample_rate (float): new sample rate requested
            resample_quality (str): the resampling quality. See soxr documentation for details. Default is very high
                quality (VHQ)
        Returns:
             Resampled AudioWaveform
        """

        timeseries = soxr.resample(self.timeseries,
                                   in_rate=self.sample_rate,
                                   out_rate=new_sample_rate,
                                   quality=resample_quality)
        return AudioWaveform(timeseries=timeseries, sample_rate=new_sample_rate,
                             name=self.name, start_time_sec=self.start_time_sec)

    def get_times(self) -> np.ndarray:
        """
        Use the sample rate to get the array of relative times associated with the waveform

        Returns:
            Numpy array with relative timestamps in seconds for the waveform
        """
        time_step = 1.0 / self.sample_rate
        times = np.arange(0, (len(self.timeseries)) * time_step, time_step) + self.start_time_sec

        # deal with floating point imprecision
        if len(times) > len(self.timeseries):
            times = times[:len(self.timeseries)]

        return times

    def get_segment(self, duration_sec: float, segment_start_sec: float, segment_name: str = None) -> AudioWaveform:
        """
        Get a segment of a waveform given a start time and requested duration

        Args:
            duration_sec (float): Requested duration in seconds
            segment_start_sec (float): Requested start time in seconds, relative to t=0 being the first point in the
                waveform
            segment_name (str): Optional string to name the segment

        Returns:
            Segment of the original waveform as an AudioWaveform object
        """

        num_points_in_segment = int(duration_sec * self.sample_rate)
        index_lo = int(segment_start_sec * self.sample_rate)
        index_hi = int(index_lo + num_points_in_segment)

        if segment_start_sec < 0.0:
            raise WaveformOperationException("Negative segment start time is not allowed")

        if index_hi > len(self.timeseries):
            raise WaveformOperationException("Requested segment extends past end of waveform")

        return AudioWaveform(timeseries=self.timeseries[index_lo:index_hi],
                             sample_rate=self.sample_rate,
                             name=segment_name,
                             start_time_sec=segment_start_sec)

    def get_random_segment(self, duration_sec: float, offset_sec: float = 0, random_seed: int = None,
                           segment_index: int = None, max_time_sec: float = None) -> AudioWaveform:
        """
        Get a random segment of this waveform of duration duration_sec in seconds

        Args:
            duration_sec (float): duration of the segment in seconds
            offset_sec (float): offset in seconds from the beginning of the file and between each segment
            random_seed (int): random seed
            segment_index (int): optional index to use in the AudioWaveform name
            max_time_sec (float): maximum allowed time when selecting a segment. No portion of the
                segment can go beyond this timestamp

        Returns:
            AudioWaveform object with the requested segment of the original waveform
        """

        if random_seed is not None:
            logger.info(f"Seeding random number generator with seed={random_seed}")
            np.random.seed(random_seed)

        if max_time_sec is None:
            max_time_sec = len(self.timeseries) / self.sample_rate

        if max_time_sec - offset_sec < duration_sec:
            raise WaveformOperationException(f"This combination of duration ({duration_sec}), maximum time "
                                             f"({max_time_sec}), and offset ({offset_sec}) does not allow a random "
                                             "segment to be selected.")

        segment_start_sec = np.random.uniform(low=offset_sec, high=max_time_sec - duration_sec)

        if segment_index is None:
            segment_index = f"{segment_start_sec:.2f}"

        if self.name is not None:
            name = f"{self.name}_{segment_index}"
        else:
            name = f"segment_{segment_index}"

        return self.get_segment(duration_sec=duration_sec, segment_start_sec=segment_start_sec, segment_name=name)

    def get_num_segments(self, duration_sec: float, offset_sec: float = 0) -> int:
        """
        Calculate the number of sequential segments that the waveform can be divided into, given a
        duration of duration_sec per segment and with gaps of offset_sec between segments. First gap
        happens at the beginning of the file

        Args:
            duration_sec (float): duration of the segment in seconds
            offset_sec (float): offset in seconds from the beginning of the file and between each segment

        Returns:
            The integer number of full sequential segments given the request parameters
        """
        num_points_offset = offset_sec * self.sample_rate
        num_points_duration = duration_sec * self.sample_rate
        num_points_available = len(self.timeseries) - num_points_offset
        num_segments = int(num_points_available / num_points_duration)

        if num_segments <= 0:
            raise WaveformOperationException(
                f"duration_sec={duration_sec} and offset_sec={offset_sec} results in no segments")

        return num_segments

    @staticmethod
    def get_synced_waveforms(waveformA: AudioWaveform,
                             waveformB: AudioWaveform,
                             match_final_length: bool = False) -> Tuple[AudioWaveform, AudioWaveform]:
        """
        Synchronize two waveforms and return the two synchronized waveforms with the first sample
        representing the first time sample of overlap

        Args:
            waveformA (AudioWaveform): first waveform
            waveformB (AudioWaveform): second waveform
            match_final_length (bool): whether to truncate the waveform with more samples after the synchronization
                to force the length of the two waveforms to be identical

        Returns:
            Two synchronized waveforms
        """

        # match sample rates if they aren't already
        waveformA, waveformB = AudioWaveform.match_sample_rates(waveformA, waveformB)

        # Find offset that best synchronizes the waveforms
        offset_samples = AudioWaveform.get_sync_sample_offset(waveformA, waveformB)
        logger.info(
            f"Sample offset found to be {offset_samples} samples ({offset_samples / waveformA.sample_rate} seconds)")

        # Truncate away the waveform samples for waveform that's early
        if offset_samples > 0:
            waveformA.timeseries = waveformA.timeseries[offset_samples:]
        else:
            waveformB.timeseries = waveformB.timeseries[abs(offset_samples):]

        if match_final_length:
            waveformA, waveformB = AudioWaveform.match_lengths(waveformA=waveformA, waveformB=waveformB)

        return waveformA, waveformB

    @staticmethod
    def get_sync_sample_offset(waveformA: AudioWaveform,
                               waveformB: AudioWaveform) -> int:
        """
        Determine the sample offset required to synchronize two waveforms

        Args:
            waveformA (AudioWaveform): first waveform
            waveformB (AudioWaveform): second waveform

        Returns:
            Number of samples to offset such that maximal synchronization is achieved
        """

        # expected to be the same sampling rates
        if waveformA.sample_rate != waveformB.sample_rate:
            raise WaveformOperationException("Waveform sample rates must match before calling this method.")

        # get the correlation between the two waveforms
        correlation = scipy.signal.correlate(waveformA.timeseries, waveformB.timeseries)

        # get the number of samples required to achieve maximum correlation
        index_max = np.argmax(np.abs(correlation))
        lags = scipy.signal.correlation_lags(len(waveformA.timeseries), len(waveformB.timeseries))
        return lags[index_max]
    

    @staticmethod
    def match_lengths(waveformA: AudioWaveform, waveformB: AudioWaveform) -> tuple[AudioWaveform, AudioWaveform]:
        """
        Matches the lengths of two AudioWaveform timeseries.  Makes both the length of the shorter series.

        :param AudioWaveform waveformA: first AudioWaveform
        :param AudioWaveform waveformB: second AudioWaveform
        :return tuple[AudioWaveform, AudioWaveform]: Tuple of (first, second) AudioWaveforms with matched timeseries lengths.
        """
        if waveformA.sample_rate != waveformB.sample_rate:
            logger.warning("You are matching the lengths of two waveforms with different sample rates.  The matched number of samples in the waveform does not represent a match in the total time of the waveforms.")

        min_length = min(len(waveformA.timeseries), len(waveformB.timeseries))
        waveformA.timeseries = waveformA.timeseries[:min_length]
        waveformB.timeseries = waveformB.timeseries[:min_length]
        return waveformA, waveformB


    @staticmethod
    def match_sample_rates(waveformA: AudioWaveform,
                           waveformB: AudioWaveform,
                           match_higher_rate=True,
                           resample_quality='VHQ',
                           match_final_length: bool = False) -> Tuple[AudioWaveform, AudioWaveform]:
        """
        Match sampling rates of two AudioWaveforms

        Args:
            waveformA (AudioWaveform): first waveform
            waveformB (AudioWaveform): second waveform
            match_higher_rate (bool): whether to match using the waveform with higher sampling rate (True, default) or
                the one with lower sampling rate (False)
            resample_quality (str): the resampling quality. See soxr documentation for details. Default is very high
                quality (VHQ)

        Returns:
            Two waveforms with matched sampling rates
        """

        if (
                ((waveformA.sample_rate > waveformB.sample_rate) and match_higher_rate) or
                ((waveformA.sample_rate < waveformB.sample_rate) and not match_higher_rate)
        ):
            logger.debug(f"Sample rate of {waveformB.name} waveform is being upsampled")
            waveformB = waveformB.resample(new_sample_rate=waveformA.sample_rate,
                                           resample_quality=resample_quality)

        elif (
                ((waveformA.sample_rate < waveformB.sample_rate) and match_higher_rate) or
                ((waveformA.sample_rate > waveformB.sample_rate) and not match_higher_rate)
        ):
            logger.debug(f"Sample rate of {waveformA.name} waveform is being upsampled")
            waveformA = waveformA.resample(new_sample_rate=waveformB.sample_rate,
                                           resample_quality=resample_quality)

        # This should never happen after the operations above
        if waveformA.sample_rate != waveformB.sample_rate:
            raise WaveformOperationException("Waveform sample rates do not match")
        
        if match_final_length:
            waveformA, waveformB = AudioWaveform.match_lengths(waveformA=waveformA, waveformB=waveformB)


        return waveformA, waveformB

    @staticmethod
    def check_waveform_ranges(waveform: AudioWaveform):
        """
        Method to check that the AudioWaveform is in the expected form. Raises an exception if it is not
        """
        if np.max(np.abs(waveform.timeseries)) > 1.0:
            wave_min = np.min(waveform.timeseries)
            wave_max = np.max(waveform.timeseries)

            raise WaveformOperationException(
                f"Expecting waveform with values between -1 and 1, but range of {wave_min} - {wave_max} observed"
            )

    @staticmethod
    def convert_bit_depth(original_waveform: AudioWaveform, target_bit_depth: int) -> AudioWaveform:
        """
        Convert value to desired bit depth. Values of waveforms will still be floats, but the
        conversion will remove the information contained in less significant bits as requested

        Args:
            original_waveform (AudioWaveform): original waveform to be manipulated
            target_bit_depth (int): number of bits in final waveform

        Returns:
            AudioWaveform object with converted bit depth
        """

        AudioWaveform.check_waveform_ranges(original_waveform)

        max_val_for_bit_depth = 2 ** target_bit_depth

        # convert to values between 0 and 1
        timeseries = (original_waveform.timeseries + 1.0) / 2.0

        # convert to integers with max given by bit depth
        timeseries = (timeseries * max_val_for_bit_depth).astype(int)

        # convert back to floats between -1 and 1
        timeseries = (timeseries * 2.0 - max_val_for_bit_depth) / max_val_for_bit_depth

        converted_waveform = AudioWaveform(timeseries,
                                           original_waveform.sample_rate,
                                           f'{target_bit_depth}-bit {original_waveform.name}')

        return converted_waveform

    def plot_timeseries(self, ax=None):
        """
        Plot the timeseries

        Args:
            ax: the matplotlib axis to use
        """
        if ax is None:
            f, ax = plt.subplots()

        ax.set_title(f"self.name (Sample Rate: {self.sample_rate} Hz")
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("Amplitude")
        ax.plot(self.get_times(), self.timeseries)

    def plot_mel_spectrogram(self, n_fft: int = 2048, hop_length: int = 512, n_mels: int = 128, ax: plt.axes = None):
        """
        Plot the waveform frequencies on the Mel scale

        Args:
            n_fft:
            hop_length:
            n_mels:
            ax: the matplotlib axis to use
        """
        if ax is None:
            f, ax = plt.subplots()

        S = librosa.feature.melspectrogram(y=self.timeseries, sr=self.sample_rate, n_fft=n_fft, hop_length=hop_length,
                                           n_mels=n_mels)
        S_DB = librosa.power_to_db(S, ref=np.max)
        librosa.display.specshow(S_DB, sr=self.sample_rate, hop_length=hop_length, x_axis='time', y_axis='mel', ax=ax)

    @staticmethod
    def load_audio(filename: str, target_sample_rate: float = None, scale_factor: float = None) -> AudioWaveform:
        """Load Audio File into a Waveform object

        Args:
            filename (str): Only .wav file type has been tested
            target_sample_rate (float): sample rate requested the waveform. Default of None uses
                the sample rate from the file itself with no conversion
            scale_factor (float): scale factor to apply to waveform amplitudes after reading in file. Defaults to None,
                which results in no scale factor being applied

        Returns:
            AudioWaveform: Waveform Object containing timeseries data
        """

        with sf.SoundFile(filename) as of:
            logger.info(
                f"File: `{filename}` Sample Rate: {of.samplerate} Hz, nChannels: {of.channels}, "
                f"File Format: {of.format} [{sf.available_formats()[of.format]}], "
                f"Encoding: {of.subtype} [{sf.available_subtypes()[of.subtype]}]"
            )

        if target_sample_rate is not None and of.samplerate != target_sample_rate:
            logger.info(
                f"File sample rate is {of.samplerate} Hz, but converting to {target_sample_rate} Hz on loading.")

        wave, rate = librosa.load(filename, sr=target_sample_rate)
        if scale_factor is not None:
            wave *= scale_factor
        return AudioWaveform(timeseries=wave, sample_rate=rate, name=filename)



