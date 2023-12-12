"""
CLI for the pyscreech module. At present, it calculates STIPA or STOI scores using audio files passed
in from the command line, but will be extended as the project develops
"""
import os

import numpy as np

from pyscreech.audio import AudioWaveform
from pyscreech.score import DEFAULT_NUM_SEGMENTS, DEFAULT_STARTING_OFFSET
from pyscreech.stipa import StipaCalculator
from pyscreech.stoi import StoiCalculator

from pyscreech.filter import DEFAULT_BUTTER_ORDER, DEFAULT_HAMMING_TIME_MS, FirwinFilterParameters
from loguru import logger

scores = {
    'STIPA': StipaCalculator,
    'STOI': StoiCalculator,
}


def main(score_type, recording, reference, starting_offset, duration, num_segments, sync_waveforms, randomize,
         print_all_scores, butter_order, corner_frequency, hamming_time):
    logger.info(f"** Calculating {score_type} for \'{recording}\' **")
    logger.info(f"** Using \'{reference}\' as reference **")
    logger.info(f"** Measurement duration = {duration} seconds **")
    logger.info(f"** Number of segments to analyze = {num_segments} seconds **")
    logger.info(f"** Start of file offset to ignore = {starting_offset} seconds **")

    if score_type == 'STOI' and not sync_waveforms:
        sync_waveforms = True
        logger.info(f"** Forcing sync_waveforms to {sync_waveforms} for {score_type} calculation **")

    if not sync_waveforms:
        logger.info("** No attempt will be made to sync the waveforms **")
    else:
        logger.info("** Attempt will be made to sync the waveforms **")

    if randomize:
        logger.info("** Segments analyzed will be randomized **")
    else:
        logger.info("** Segments analyzed will be sequential time segments **")
    if print_all_scores:
        logger.info("** Scores for all segments will be reported. No score agreement enforced. **")
    else:
        logger.info("** Only successfully averaged scores will be reported **")
    logger.info(f"** Butter order = {butter_order} **")
    logger.info(f"** Low-pass corner frequency = {corner_frequency} **")
    logger.info(f"** Low-pass hamming time = {hamming_time} **")

    if hamming_time is not None and corner_frequency is not None:
        firwin_filter_params = FirwinFilterParameters(firwin_hamming_time=hamming_time,
                                                      firwin_corner_freq=corner_frequency)
    else:
        logger.info("Not using a firwin low pass filter on octave band signals")
        firwin_filter_params = None

    input = AudioWaveform.load_audio(recording)
    ref = AudioWaveform.load_audio(reference)

    score_calculator = scores[score_type]()

    if print_all_scores:
        if randomize:
            score_results = score_calculator.calculate_multiple_random(input_waveform=input,
                                                                       reference_waveform=ref,
                                                                       duration_sec=duration,
                                                                       offset_sec=starting_offset,
                                                                       num_segments=num_segments,
                                                                       sync_waveforms=sync_waveforms,
                                                                       butter_order=butter_order,
                                                                       firwin_filter_params=firwin_filter_params)
        else:
            score_results = score_calculator.calculate_multiple_sequential(input_waveform=input,
                                                                           reference_waveform=ref,
                                                                           duration_sec=duration,
                                                                           offset_sec=starting_offset,
                                                                           num_segments=num_segments,
                                                                           sync_waveforms=sync_waveforms,
                                                                           butter_order=butter_order,
                                                                           firwin_filter_params=firwin_filter_params)

        score_results = np.array([round(v, 2) for v in score_results])
        logger.info(f"Individual {score_type} scores = {score_results}")
        logger.info(f"{score_type} average score     = {np.mean(score_results)} +/- {np.std(score_results):.3f}")
        return score_results
    else:
        score_results = score_calculator.calculate_average_score(input_waveform=input,
                                                                 reference_waveform=ref,
                                                                 num_segments_in_avg=num_segments,
                                                                 duration_sec=duration,
                                                                 offset_sec=starting_offset,
                                                                 sync_waveforms=sync_waveforms,
                                                                 randomize=randomize,
                                                                 butter_order=butter_order,
                                                                 firwin_filter_params=firwin_filter_params)
        logger.info(f"{score_type} score = {round(score_results, 2)}")
        return score_results


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "score_type", type=str, choices=scores.keys(), help="Score to calculate."
    )
    parser.add_argument("recording", type=str, help=".wav File containing the Audio Recording of reference signal")
    parser.add_argument("-d", "--duration", type=float, default=25,
                        help="Measurement time in seconds. Pass 0 to process the entire waveforms")
    repo_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    parser.add_argument("-r", "--reference", type=str, default=f"{repo_dir}/resources/StipaV5_CEA.wav",
                        help=".wav file containing `reference` recording")
    parser.add_argument("-o", "--starting-offset", type=float, default=DEFAULT_STARTING_OFFSET,
                        help="Length of time in seconds at the start of each file to skip. Default is"
                             f" {DEFAULT_STARTING_OFFSET}.")
    parser.add_argument("-n", "--num-segments", type=int, default=DEFAULT_NUM_SEGMENTS,
                        help=f"Number of segments to use in calculation. Defaults to {DEFAULT_NUM_SEGMENTS}.")
    parser.add_argument("--sync-waveforms", default=False, action="store_true",
                        help="Whether to synchronize waveforms (--sync-waveforms) before performing calculations "
                             "Default is False. If STOI is selected, this argument is forced to be True.")
    parser.add_argument("--randomize", default=False, action="store_true",
                        help="Whether to use random segments of the files in calculations (--randomize) or "
                             "to use sequential segments of the file (default).")
    parser.add_argument("--print-all-scores", default=False, action="store_true",
                        help="Whether to print scores from all calculations to the screen (--print-all-scores) or "
                             "only the average (default)")
    parser.add_argument("-b", "--butter-order", type=int, default=DEFAULT_BUTTER_ORDER,
                        help="Butterworth filter order used in octave band filter")
    parser.add_argument("-c", "--corner-frequency", type=float, default=None,
                        help="Corner frequency used low pass filter applied to each octave band")
    parser.add_argument("-m", "--hamming-time", type=float, default=DEFAULT_HAMMING_TIME_MS,
                        help="Hamming time in ms used in the low pass filter applied to each octave band")

    args = parser.parse_args()
    main(**vars(args))
