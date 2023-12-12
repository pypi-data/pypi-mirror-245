"""Tests of audio.py"""

__author__ = "Seth Henshaw and Matthew Blackston"
__copyright__ = "Copyright 2023 Leidos"

import copy

import numpy as np
import pytest

from pyscreech.audio import AudioWaveform, WaveformOperationException


def test_audio_load(reference_stipa_waveform):
    # Test loading a wav file with different sampling rates

    # read in with file-defined sampling
    expected_sample_rate = 48000
    assert reference_stipa_waveform.sample_rate == expected_sample_rate
    expected_length = 4800000
    assert len(reference_stipa_waveform.timeseries) == expected_length

    # try downsampling
    target_sample_rate = 8000
    waveform = AudioWaveform.load_audio(reference_stipa_waveform.name, target_sample_rate=target_sample_rate)
    assert waveform.sample_rate == target_sample_rate
    assert len(waveform.timeseries) == expected_length * target_sample_rate / expected_sample_rate

    # try upsampling
    target_sample_rate = 80000
    waveform = AudioWaveform.load_audio(reference_stipa_waveform.name, target_sample_rate=target_sample_rate)
    assert waveform.sample_rate == target_sample_rate
    assert len(waveform.timeseries) == expected_length * target_sample_rate / expected_sample_rate


def test_resample(reference_stipa_waveform):
    assert reference_stipa_waveform.sample_rate == 48000

    waveform_p = reference_stipa_waveform.resample(new_sample_rate=8000)
    assert waveform_p.sample_rate == 8000

    assert len(waveform_p.timeseries) < len(reference_stipa_waveform.timeseries)
    assert np.isclose(reference_stipa_waveform.get_times()[-1], waveform_p.get_times()[-1])

    with pytest.raises(ValueError):
        reference_stipa_waveform.resample(new_sample_rate=8000, resample_quality='junk')


def test_get_random_segment(reference_stipa_waveform):
    rand_seg = reference_stipa_waveform.get_random_segment(duration_sec=10,
                                                           offset_sec=5)

    assert len(rand_seg.timeseries) / rand_seg.sample_rate == 10

    with pytest.raises(WaveformOperationException):
        # Can't get a 10 sec sample if we say offset is 5 and max time is 12
        reference_stipa_waveform.get_random_segment(duration_sec=10,
                                                    offset_sec=5,
                                                    max_time_sec=12)


def test_sync_correlation():
    sample_shift = 5
    waveform = AudioWaveform(np.arange(-100, 100.5, 1), sample_rate=1)

    # make a copy and roll it by sample_shift
    rolled_waveform = copy.deepcopy(waveform)
    rolled_waveform.timeseries = np.roll(waveform.timeseries, sample_shift)

    # ensure we get sample_shift back as the offset in samples
    optimum_offset = AudioWaveform.get_sync_sample_offset(rolled_waveform, waveform)
    assert optimum_offset == sample_shift

    # sync the waveforms
    waveformA, waveformB = AudioWaveform.get_synced_waveforms(rolled_waveform, waveform)

    # check that they are identical now
    max_len = max(len(waveformA.timeseries), len(waveformA.timeseries))
    assert np.allclose(waveformA.timeseries[:max_len], waveformB.timeseries[:max_len])


@pytest.mark.parametrize('match_higher_rate', [True, False])
def test_match_sample_rates(match_higher_rate):
    sample_rate = 2
    waveformA = AudioWaveform(np.arange(-100, 100.5, 1), sample_rate=sample_rate)
    waveformB = AudioWaveform(np.arange(-100, 100.5, 2), sample_rate=sample_rate / 2.0)

    # waveforms are not equal to start
    assert waveformB.sample_rate != waveformA.sample_rate

    waveformA, waveformB = AudioWaveform.match_sample_rates(waveformA, waveformB, match_higher_rate=match_higher_rate)
    # waveforms are equal after match_sample_rates
    assert waveformB.sample_rate == waveformA.sample_rate

    # test that identical sample rates don't get changed
    waveformC = AudioWaveform(np.arange(-100, 100.5, 1), sample_rate=sample_rate)
    waveformD = AudioWaveform(np.arange(-100, 100.5, 1), sample_rate=sample_rate)
    assert waveformC.sample_rate == waveformD.sample_rate

    waveformC, waveformD = AudioWaveform.match_sample_rates(waveformC, waveformD, match_higher_rate=match_higher_rate)
    assert waveformC.sample_rate == waveformD.sample_rate
    assert waveformC.sample_rate == sample_rate


def test_convert_bit_depth():
    # Test converting the bit depths of a waveform

    max_val = np.iinfo(np.uint16).max
    np.random.seed(42)

    # start with 16-bit
    test_vals0 = np.random.randint(low=0, high=max_val, size=10, dtype=np.uint16)

    def _convert_to_float(x, bd_max_val):
        return 2.0 * (x.astype(float) / bd_max_val) - 1.0

    test_vals = _convert_to_float(test_vals0, max_val)
    test_waveform = AudioWaveform(test_vals, sample_rate=1)
    test_waveform0 = copy.deepcopy(test_waveform)

    for target_bit_depth in np.arange(16, 1, -1):
        # convert the bit depth
        modified_waveform = AudioWaveform.convert_bit_depth(test_waveform, target_bit_depth=target_bit_depth)
        # check that a deepcopy isn't needed inside convert_bit_depth
        assert np.array_equal(test_waveform0.timeseries, test_waveform.timeseries)

        # determine the equivalent float spacing on a -1, 1 range for this bit depth
        float_rep_0_1 = _convert_to_float(np.array([0, 1]), 2 ** target_bit_depth)
        float_diff_for_bit_depth = float_rep_0_1[1] - float_rep_0_1[0]

        # ensure that the differences between values are only those allowed by this bit depth,
        # e.g. whole numbers of factors of float_diff_for_bit_depth between values
        val_diff = np.diff(modified_waveform.timeseries) / float_diff_for_bit_depth
        assert np.allclose(val_diff, val_diff.astype(int))
