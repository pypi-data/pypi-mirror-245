"""Tests of stoi.py"""

import copy

import numpy as np

from pyscreech.audio import AudioWaveform


def test_calculate_stoi_from_waveforms(reference_stipa_waveform, stoi_calculator):

    for extended in [True, False]:
        stoi_score = stoi_calculator.calculate_score_from_waveforms(input_waveform=reference_stipa_waveform,
                                                                    reference_waveform=reference_stipa_waveform,
                                                                    extended=extended)

        assert stoi_score > 0.9999

    target_length = 100000
    target_offset = 20
    short_ref = reference_stipa_waveform.get_segment(duration_sec=target_length / reference_stipa_waveform.sample_rate,
                                                     segment_start_sec=target_offset,
                                                     segment_name='short_ref')
    assert len(short_ref.timeseries) == target_length

    # test that we can handle relative shifts in the waveforms
    for offset in np.arange(0, 0.01, 0.001):

        # First do simple offset
        input_segment = reference_stipa_waveform.get_segment(
            duration_sec=target_length / reference_stipa_waveform.sample_rate,
            segment_start_sec=short_ref.start_time_sec - offset
        )

        stoi_score = stoi_calculator.calculate_score_from_waveforms(input_waveform=input_segment,
                                                                    reference_waveform=short_ref)

        # Get a score of 1 if no offset, otherwise it drops
        if offset == 0.0:
            assert np.allclose(1.0, stoi_score)
        else:
            assert not np.allclose(1.0, stoi_score)

    # Next do cross correlation to correct offset
    input_shift = copy.deepcopy(reference_stipa_waveform)
    input_shift.timeseries = np.roll(reference_stipa_waveform.timeseries, 10)
    input_shift, input = AudioWaveform.get_synced_waveforms(input_shift,
                                                            reference_stipa_waveform,
                                                            match_final_length=True)

    stoi_score = stoi_calculator.calculate_score_from_waveforms(input_waveform=input,
                                                                reference_waveform=input_shift,
                                                                extended=extended)

    # Get a score of 1 since we're correcting for offset
    assert np.allclose(1.0, stoi_score)
