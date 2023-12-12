"""Methods for filtering waveforms"""
from enum import Enum

import numpy as np
from scipy.signal import sosfiltfilt, butter, firwin, lfilter
from .audio import AudioWaveform


class FilterException(Exception):
    pass


DEFAULT_BUTTER_ORDER = 2
DEFAULT_HAMMING_TIME_MS = 16.6
DEFAULT_CORNER_FREQUENCY_HZ = 100.0


class BandwidthType(Enum):
    FULL_OCTAVE = 0
    THIRD_OCTAVE = 1


DEFAULT_BANDWIDTH = BandwidthType.FULL_OCTAVE


class FirwinFilterParameters():
    """
    Object to hold firwin filter parameters
    """

    def __init__(self, firwin_hamming_time: float = DEFAULT_HAMMING_TIME_MS,
                 firwin_corner_freq: float = DEFAULT_CORNER_FREQUENCY_HZ):
        """

        Args:
            firwin_hamming_time (float): Hamming time in units of ms used in the low pass filter applied to
                each octave band
            firwin_corner_freq (float): Corner frequency in hz used low pass filter applied to each octave band
        """

        self.firwin_hamming_time = firwin_hamming_time
        self.firwin_corner_freq = firwin_corner_freq


def apply_lowpass_filter(waveform: AudioWaveform, filter_params: FirwinFilterParameters) -> AudioWaveform:
    """Apply Low Pass Filter to Audio Waveform

    Args:
        waveform (AudioWaveform): Timeseries waveform containing audio data
        hamming_time (float, optional): Hamming Time (ms) used for filter. Defaults to DEFAULT_HAMMING_TIME_MS
        corner_frequency (float, optional): Frequency (Hz) for filter corner. Defaults to DEFAULT_CORNER_FREQUENCY_HZ.
    Returns:
        Filtered AudioWaveform object
    """
    nyquist = waveform.sample_rate * 0.5
    hamming_length = int((filter_params.firwin_hamming_time / 1000.0) * waveform.sample_rate)

    # ensure hamming length is odd b/c it includes nyquist frequency
    if hamming_length % 2 == 0:
        hamming_length += 1

    # construct the filter
    coeff = firwin(hamming_length, filter_params.firwin_corner_freq, nyq=nyquist)

    # apply the filter
    filteredData = lfilter(coeff, 1, waveform.timeseries)
    return AudioWaveform(filteredData, waveform.sample_rate)


def apply_butter_sos_bandpass_filter(waveform: AudioWaveform,
                                     frequency_range: tuple,
                                     butter_order: int = DEFAULT_BUTTER_ORDER) -> AudioWaveform:
    """
    Apply a bandpass filter using a butterworth filter in the form of second order sections (SOS).
    SOS representation of the filter reduces the amount of numerical problems compared to other representations

    Args:
        waveform (AudioWaveform): waveform to filter
        frequency_range (tuple): tuple with low and high frequency of the bandpass filter in Hz
        butter_order (int): order of the butter filter. Defaults to DEFAULT_BUTTER_ORDER

    Returns:
        Bandpass filtered waveform as AudioWaveform object
        FilterException if frequency range requested is out of range for butterworth filter
    """

    # Calculate the frequency limits
    nyquist = waveform.sample_rate * 0.5
    if len(frequency_range) != 2:
        raise FilterException(f"frequency_range ({frequency_range}) must be of length 2")

    # Calculate the critical frequencies
    critical_frequencies = np.array(frequency_range) / nyquist

    # Handle frequency limits
    if np.any(critical_frequencies > 1.0):
        if not np.all(critical_frequencies > 1.0):
            # If a band has one limit that stretches beyond 1.0, then just truncate back to end just below 1.0
            critical_frequencies[critical_frequencies >= 1.0] = 0.9999999
        else:
            # If the entire band is beyond critical frequency of 1.0, skip the calculation altogether
            raise FilterException("Entire band out of range for butter filter")

    # Create the filter
    sos = butter(N=butter_order, Wn=critical_frequencies, btype='bandpass', analog=False, output='sos')

    # Filter the signal
    filtered_data = sosfiltfilt(sos, waveform.timeseries)

    return AudioWaveform(filtered_data, waveform.sample_rate)


def get_octave_band_edges(center_frequency: float, bandwidth: BandwidthType = DEFAULT_BANDWIDTH) -> (float, float):
    """
    Calculate the frequency limits given a center frequency and a fractional octave bandwidth

    Args:
        center_frequency (float): Center frequency of the band requested
        bandwidth (BandwidthType): fractional bandwidth of an octave. Defaults to BandwidthType.FULL_OCTAVE

    Returns:
        Tuple of floats with the lower and upper frequency limits for this band
    """
    if bandwidth == BandwidthType.FULL_OCTAVE:
        return center_frequency / np.sqrt(2), center_frequency * np.sqrt(2)
    elif bandwidth == BandwidthType.THIRD_OCTAVE:
        return center_frequency / np.power(2, 1 / 6), center_frequency * np.power(2, 1 / 6)
    else:
        raise ValueError(f"Unrecognized bandwidth: {bandwidth}")
