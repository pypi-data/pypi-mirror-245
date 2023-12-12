"""Tests of score.py"""

import numpy as np

from pyscreech.audio import AudioWaveform
from pyscreech.score import ScoreCalculator


def test_core_score():
    class A(ScoreCalculator):

        def calculate_score_from_waveforms(self,
                                           input_waveform: AudioWaveform,
                                           reference_waveform: AudioWaveform,
                                           **kwargs):
            # simple score that takes the sum of the two waveforms and then
            # calculates the average sample value
            sum = input_waveform.timeseries + reference_waveform.timeseries

            return np.mean(sum)


    score_calculator = A()

    input_waveform = AudioWaveform(np.arange(-100, 100.5, 1), sample_rate=1)
    reference_waveform = AudioWaveform(np.arange(100, -100.5, -1), sample_rate=1)

    scores = score_calculator.calculate_multiple_random(input_waveform=input_waveform,
                                                        reference_waveform=reference_waveform,
                                                        duration_sec=5,
                                                        sync_waveforms=True)

    assert np.all(scores == 0)

    scores = score_calculator.calculate_multiple_sequential(input_waveform=input_waveform,
                                                            reference_waveform=reference_waveform,
                                                            duration_sec=5,
                                                            sync_waveforms=True)

    assert np.all(scores == 0)

