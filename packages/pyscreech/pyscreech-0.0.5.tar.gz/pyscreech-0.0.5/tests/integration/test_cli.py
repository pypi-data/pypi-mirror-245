import numpy as np
import pytest

from pyscreech.cli import main, scores
from tests.conftest import recording_filename

from loguru import logger


@pytest.mark.parametrize('score_type', scores)
@pytest.mark.parametrize('print_all_scores', [True, False])
@pytest.mark.parametrize('randomize', [True, False])
@pytest.mark.parametrize('sync_waveforms', [True, False])
def test_cli(reference_stipa_waveform, score_type, print_all_scores, randomize, sync_waveforms):

    recording = recording_filename("StipaV5_CEA.wav")
    starting_offset = 0
    duration = 5
    num_segments = 3
    # print_all_scores = False
    butter_order = 2
    corner_frequency = None
    hamming_time = None

    logger.info("\n")
    logger.info(f"score_type={score_type}, randomize={randomize}, sync_waveforms={sync_waveforms}")

    score_result = main(score_type=score_type,
                        recording=recording,
                        reference=recording,
                        starting_offset=starting_offset,
                        duration=duration,
                        num_segments=num_segments,
                        sync_waveforms=sync_waveforms,
                        randomize=randomize,
                        print_all_scores=print_all_scores,
                        butter_order=butter_order,
                        corner_frequency=corner_frequency,
                        hamming_time=hamming_time)

    if score_type == 'STIPA' and randomize and not sync_waveforms:
        # 0.9 should be pretty safe here for a random 5-second segment
        assert np.all(score_result > 0.88)
    else:
        assert np.allclose(score_result, 1.0)
