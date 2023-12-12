"""Tests of stipa.py"""

__author__ = "Seth Henshaw and Matthew Blackston"
__copyright__ = "Copyright 2023 Leidos"

import copy

import numpy as np
import pytest

from pyscreech.audio import AudioWaveform
from pyscreech.stipa import StipaCalculator


@pytest.mark.parametrize('sample_rate', [48000, 24000, 8000, 4000])
@pytest.mark.parametrize('orig_wave_frequency_hz', [125, 250, 500])
@pytest.mark.parametrize('modulation_frequency', [0.5, 3.0, 12.5])
@pytest.mark.parametrize('modulation_depth', [0.2, 0.5, 0.75, 0.9])
def test_modulation_depth(sample_rate, orig_wave_frequency_hz, modulation_frequency, modulation_depth):
    # Test the depth modulation calculation for a wide variety of parameters

    time_step = 1.0 / sample_rate

    num_periods = 5
    end_time = num_periods * (1 / modulation_frequency)

    unmodulated_wave_times = np.arange(0, end_time, time_step)
    unmodulated_wave = np.sin(2.0 * np.pi * unmodulated_wave_times * orig_wave_frequency_hz)

    modulation_signal = np.sqrt(
        0.5 * (1 + modulation_depth * np.cos(2.0 * np.pi * unmodulated_wave_times * modulation_frequency)))
    modulated_wave = unmodulated_wave * modulation_signal

    intensity_envelope = modulated_wave ** 2

    intensity_waveform = AudioWaveform(intensity_envelope, sample_rate=sample_rate)

    calc_modulation_depth = StipaCalculator.calculate_modulation_depth(intensity_waveform, modulation_frequency)
    perc_diff = np.abs(modulation_depth - calc_modulation_depth) / modulation_depth
    assert perc_diff < 0.005


def test_zeroes(stipa_calculator, reference_stipa_waveform):

    input = copy.deepcopy(reference_stipa_waveform)
    input.timeseries = np.zeros_like(input.timeseries)

    stipa_score = stipa_calculator.calculate_score_from_waveforms(input, reference_stipa_waveform)
    assert stipa_score == 0.0




