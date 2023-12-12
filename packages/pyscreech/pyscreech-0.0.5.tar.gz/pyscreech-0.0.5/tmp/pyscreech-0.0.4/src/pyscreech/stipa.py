"""Methods used for calculating STIPA score"""

import numpy as np
from typing import List

from loguru import logger

from .audio import AudioWaveform

from .filter import (
    apply_butter_sos_bandpass_filter,
    DEFAULT_BUTTER_ORDER,
    apply_lowpass_filter,
    FilterException,
    FirwinFilterParameters,
    get_octave_band_edges,
    BandwidthType
)
from .score import ScoreCalculator


class StipaCalculationException(Exception):
    pass


OCTAVE_BAND_CENTERS = np.array([125, 250, 500, 1000, 2000, 4000, 8000])
OCTAVE_MODULATION_FREQUENCIES = np.array(
    [[1.6, 8], [1, 5], [0.63, 3.15], [2, 10], [1.25, 6.25], [0.8, 4], [2.5, 12.5]])

MALE_WEIGHTS_ALPHA = np.array([0.085, 0.127, 0.230, 0.233, 0.309, 0.224, 0.173])
MALE_WEIGHTS_BETA = np.array([0.085, 0.078, 0.065, 0.011, 0.047, 0.095])


class StipaCalculator(ScoreCalculator):

    @staticmethod
    def calculate_modulation_depth(intensity_envelope: AudioWaveform, modulation_frequency: float) -> float:
        """
        Calculates the modulation depth given an intensity envelope and a modulation frequency

        Args:
            intensity_envelope (AudioWaveform): intensity envelope of the waveform
            modulation_frequency (float): modulation frequency

        Returns:
            Calculated modulation depth for this modulation frequency
        """

        times = intensity_envelope.get_times()
        intensity = intensity_envelope.timeseries

        # use an integer number of periods in to calculate depth, so calculate the corresponding max time
        max_time_whole_number_periods = int(times[-1] * modulation_frequency) / modulation_frequency

        intensity = intensity[times <= max_time_whole_number_periods]
        times = times[times <= max_time_whole_number_periods]

        I = np.sin(2 * np.pi * modulation_frequency * times)
        Q = np.cos(2 * np.pi * modulation_frequency * times)

        # calculate modulation depth, ignoring divide by zero b/c we'll handle it later
        with np.errstate(divide='ignore'):
            return 2 * np.sqrt(np.sum(intensity * I) ** 2 + np.sum(intensity * Q) ** 2) / np.sum(intensity)

    @staticmethod
    def calculate_octave_depths(waveform: AudioWaveform,
                                modulation_frequencies: List[float],
                                central_frequency: float = None,
                                butter_order: int = DEFAULT_BUTTER_ORDER,
                                firwin_filter_params: FirwinFilterParameters = None) -> np.ndarray:
        """
        Calculate the octave modulation depths for this frequency band given a list of modulation frequencies

        Args:
            waveform (AudioWaveform): Waveform to assess
            central_frequency (float): central frequency of the band
            modulation_frequencies (List): list of modulation frequencies for which to calculate depths
            butter_order (int): order of the butter filter. Defaults to DEFAULT_BUTTER_ORDER
            firwin_filter_params (FirwinFilterParameters): low pass filter parameters

        Returns:
            Numpy array of modulations depths for each modulation frequency used in calculation
        """

        # Apply bandpass filter to the waveform
        frequency_range = get_octave_band_edges(central_frequency, bandwidth=BandwidthType.FULL_OCTAVE)
        try:
            filtered_output = apply_butter_sos_bandpass_filter(waveform=waveform,
                                                               frequency_range=frequency_range,
                                                               butter_order=butter_order)

        except FilterException:
            return None

        # Get the intensity envelope by squaring the filtered waveform
        filtered_output.timeseries = filtered_output.timeseries ** 2

        # Apply a low pass filter (FIR)
        if firwin_filter_params is not None:
            filtered_output = apply_lowpass_filter(filtered_output, filter_params=firwin_filter_params)

        # Calculate the depths for each modulation frequency
        depths = np.array(
            [StipaCalculator.calculate_modulation_depth(filtered_output, mi) for mi in modulation_frequencies])

        return depths

    @staticmethod
    def construct_stipa_depth_matrix(waveform: AudioWaveform,
                                     butter_order: int = DEFAULT_BUTTER_ORDER,
                                     firwin_filter_params: FirwinFilterParameters = None) -> np.ndarray:
        """
        Construct the depth matrix for each octave band

        Args:
            waveform (AudioWaveform): Waveform to process
            butter_order (int): Butterworth filter order used in octave band filter
            firwin_filter_params (FirwinFilterParameters): low pass filter parameters

        Returns:
            Matrix of modulation depths for each octave and with modulation frequency requested
        """

        m = []

        for c, mf in zip(OCTAVE_BAND_CENTERS, OCTAVE_MODULATION_FREQUENCIES):
            depths = StipaCalculator.calculate_octave_depths(waveform=waveform,
                                                             modulation_frequencies=mf,
                                                             central_frequency=c,
                                                             butter_order=butter_order,
                                                             firwin_filter_params=firwin_filter_params)

            if depths is not None:
                m.append(depths)

        m = np.asarray(m)

        # for depths > 1.0, set back to 1.0 (per IEC document)
        m[m > 1.0] = 1.0
        return m

    @staticmethod
    def calculate_modulation_transfer_index(mtf: np.ndarray) -> np.ndarray:
        """
        Calculate the modulation transfer index for each octave band given the modulation transfer matrix

        Args:
            mtf (np.ndarray): 2D modulation transfer matrix, giving modulation depth ratios between the two
                waveforms for each modulation frequency (axis=1) for each octave band (axis=0)

        Returns:
            Numpy array of modulation transfer index for each octave band
        """
        # mtf is matrix of ratios...
        m = np.asarray(mtf)

        # figure out which octaves have valid values
        m_valid = ~np.isnan(np.sum(m, axis=1))

        # calculate snr, ignoring divide by zero b/c we'll handle it below
        with np.errstate(divide='ignore'):
            snr = 10 * np.log10(m / (1 - m))

        # if m = 1 then SNR will be NaN...but should be max so setting to 15
        snr = np.nan_to_num(snr, nan=15, posinf=15, neginf=-15)

        snr[snr > 15] = 15
        snr[snr < -15] = -15

        ti = (snr + 15) / 30
        mti = np.sum(ti, axis=1) / 2.0

        # only include the values if they are valid
        mti *= m_valid

        return mti

    @staticmethod
    def calculate_weighted_stipa(mti: np.ndarray) -> float:
        """
        Calculate the male-weighted STIPA score for each octave band given the modulation transfer matrix.
        Per IEC document, female speech is generally considered more intelligible than male speech, so
        male speech is typically used to assess speech transmission

        Args:
            mti (np.ndarray): modulation transfer indices for each octave band

        Returns:
            Male-weighted STIPA score
        """

        # if we've cut off higher frequency bands b/c our waveform has low sampling rate,
        # then we need to set the transfer indices for those bands to zero
        mti_p = mti
        length_diff = len(MALE_WEIGHTS_ALPHA) - len(mti)
        if length_diff > 0:
            mti_p = np.append(mti_p, [0.0] * length_diff)

        value = np.sum(MALE_WEIGHTS_ALPHA * mti_p) - np.sum(MALE_WEIGHTS_BETA * np.sqrt(mti_p[:-1] * mti_p[1:]))
        return value

    def calculate_score_from_waveforms(self,
                                       input_waveform: AudioWaveform,
                                       reference_waveform: AudioWaveform,
                                       butter_order: int = DEFAULT_BUTTER_ORDER,
                                       firwin_filter_params: FirwinFilterParameters = None,
                                       **kwargs) -> float:
        """
        Calculate the STIPA score between two waveforms following Instructions provided in
        the IEC60268-16-2011 Standard

        Args:
            input_waveform (AudioWaveform): input waveform to assess
            reference_waveform (AudioWaveform): reference waveform used to compare
            butter_order (int): Butterworth filter order used in octave band filter
            firwin_filter_params (FirwinFilterParameters): low pass filter parameters

        Returns:
            A single calculated STIPA score
        """

        if len(kwargs) > 0:
            logger.info(f"Ignoring extra kwargs passed in: {kwargs}")

        # Calculate the depth matrix for each waveform
        input_depth_matrix = self.construct_stipa_depth_matrix(input_waveform,
                                                               butter_order=butter_order,
                                                               firwin_filter_params=firwin_filter_params)
        reference_depth_matrix = self.construct_stipa_depth_matrix(reference_waveform,
                                                                   butter_order=butter_order,
                                                                   firwin_filter_params=firwin_filter_params)

        # if our input waveform has low enough sampling rate,
        # the higher frequency octaves do not exist, so just ignore them
        if len(input_depth_matrix) != len(reference_depth_matrix):
            reference_depth_matrix = reference_depth_matrix[:len(input_depth_matrix)]

        # Calculate the modulation transfer matrix, which is the ratio of the input and reference depth matrices
        modulation_transfer_matrix = input_depth_matrix / reference_depth_matrix
        modulation_transfer_matrix[modulation_transfer_matrix > 1.0] = 1.0

        # Calculate the modulation transfer index at each octave
        modulation_transfer_index = self.calculate_modulation_transfer_index(modulation_transfer_matrix)

        # Calculate the male-weighted STIPA score
        return self.calculate_weighted_stipa(modulation_transfer_index)

