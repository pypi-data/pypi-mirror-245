"""Integration tests of score calculations"""

__author__ = "Seth Henshaw and Matthew Blackston"
__copyright__ = "Copyright 2023 Leidos"

import copy

import numpy as np
import pytest

from pyscreech.score import ScoreCalculationException


def test_STIPA(reference_stipa_waveform, stipa_calculator):
    # For StipaV5_CEA, first do sequential segments and calculate an average score,
    # then do the same with randomized segments
    input = reference_stipa_waveform

    score0 = 1.0
    score1 = 0.99

    duration = 25
    offset = 5

    stipa_score = stipa_calculator.calculate_average_score(input_waveform=input,
                                                           reference_waveform=reference_stipa_waveform,
                                                           duration_sec=duration,
                                                           offset_sec=offset,
                                                           randomize=False)

    assert round(stipa_score, 2) == score0

    stipa_score = stipa_calculator.calculate_average_score(input_waveform=input,
                                                           reference_waveform=reference_stipa_waveform,
                                                           duration_sec=duration,
                                                           offset_sec=offset,
                                                           randomize=True,
                                                           random_seed=43)

    assert round(stipa_score, 2) == score1


def test_full_waveform_calc(reference_stipa_waveform, stipa_calculator):
    # Get the STIPA score for the entire StipaV5_CEA waveform with itself, confirm score of 1.0

    input = reference_stipa_waveform

    score = 1.0

    stipa_score = stipa_calculator.calculate_score_from_waveforms(input, reference_stipa_waveform)
    assert round(stipa_score, 2) == score


def test_multiple_scores(reference_stipa_waveform, stipa_calculator):
    # Test the ability to generate multiple scores using different segments of the waveforms

    input = reference_stipa_waveform

    # Test with randomly selected segments
    stipa_results = stipa_calculator.calculate_multiple_random(input_waveform=input,
                                                               reference_waveform=reference_stipa_waveform,
                                                               duration_sec=25,
                                                               offset_sec=5,
                                                               num_segments=10,
                                                               random_seed=42)

    stipa_results = np.round(stipa_results, 2)

    assert np.all(stipa_results >= 0.97)

    # Fail when asking for more segments than is available
    with pytest.raises(ScoreCalculationException):
        stipa_calculator.calculate_multiple_sequential(input_waveform=input,
                                                       reference_waveform=reference_stipa_waveform,
                                                       duration_sec=25,
                                                       offset_sec=5,
                                                       num_segments=20)

    # Test with sequential segments
    stipa_results = stipa_calculator.calculate_multiple_sequential(input_waveform=input,
                                                                   reference_waveform=reference_stipa_waveform,
                                                                   duration_sec=25,
                                                                   offset_sec=5,
                                                                   num_segments=3)

    stipa_results = np.round(stipa_results, 2)

    assert np.all(stipa_results >= 0.97)


def test_zeroes(reference_stipa_waveform, stipa_calculator):
    # a waveform of all zeros should have STIPA score of zero

    input = copy.deepcopy(reference_stipa_waveform)
    input.timeseries = np.zeros_like(input.timeseries)

    stipa_score = stipa_calculator.calculate_score_from_waveforms(input, reference_stipa_waveform)
    assert stipa_score == 0.0

