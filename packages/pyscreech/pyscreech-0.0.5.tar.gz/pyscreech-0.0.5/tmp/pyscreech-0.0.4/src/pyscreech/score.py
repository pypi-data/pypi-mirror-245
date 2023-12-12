"""Abstract base class definition for calculating a score"""

import numpy as np

from .audio import AudioWaveform, WaveformOperationException
from loguru import logger
import abc

DEFAULT_NUM_SEGMENTS = 3
DEFAULT_STARTING_OFFSET = 0
DEFAULT_SCORE_SPREAD_REQUIREMENT = 0.03

class ScoreCalculationException(Exception):
    pass


class ScoreCalculator(abc.ABC):

    @abc.abstractmethod
    def calculate_score_from_waveforms(self,
                                       input_waveform: AudioWaveform,
                                       reference_waveform: AudioWaveform,
                                       **kwargs):
        raise NotImplementedError("Can't call abstract method")

    def calculate_multiple_random(self,
                                  input_waveform: AudioWaveform,
                                  reference_waveform: AudioWaveform,
                                  duration_sec: float,
                                  offset_sec: float = DEFAULT_STARTING_OFFSET,
                                  num_segments: int = DEFAULT_NUM_SEGMENTS,
                                  sync_waveforms: bool = False,
                                  random_seed: int = None,
                                  print_status: bool = False,
                                  **kwargs) -> np.ndarray:
        """
        Calculate scores for multiple randomly selected segments of a waveform

        Args:
            input_waveform (AudioWaveform): input waveform to assess
            reference_waveform (AudioWaveform): reference waveform used to compare
            duration_sec (float): duration in seconds of each randomly selected segment
            offset_sec (float): offset in seconds at the beginning of the waveform that is ignored
            num_segments (int): number of segments to randomly select and evaluate
            sync_waveforms (bool): whether to attempt to sync the start times of the segments
                for the two files.  Note that if the sampling rates differ, the lower sampling rate
                waveform will be upsampled.
            random_seed (int): random number seed
            print_status (bool): whether to print a status message to the screen for monitoring progress

        Returns:
            Numpy array of scores for the randomized segments
        """

        if len(kwargs) > 0:
            logger.info(f"Ignoring extra kwargs passed in: {kwargs}")

        if sync_waveforms:
            input_waveform, reference_waveform = AudioWaveform.get_synced_waveforms(input_waveform,
                                                                                    reference_waveform)
            max_time_sec = min(len(input_waveform.timeseries) / input_waveform.sample_rate,
                               len(reference_waveform.timeseries) / reference_waveform.sample_rate)
        else:
            max_time_sec = None

        score_results = []

        logger.info(f"Using {duration_sec} second samples to calculate scores.")

        for i_score in range(num_segments):
            seed = random_seed
            if i_score > 0:
                seed = None

            if print_status and (i_score + 1) % 10 == 0:
                logger.info(f"Score {i_score + 1} of {num_segments}")

            input_segment = input_waveform.get_random_segment(duration_sec=duration_sec,
                                                              offset_sec=offset_sec,
                                                              random_seed=seed,
                                                              segment_index=i_score,
                                                              max_time_sec=max_time_sec)
            if not sync_waveforms:
                ref_segment = reference_waveform.get_random_segment(duration_sec=duration_sec,
                                                                    offset_sec=offset_sec,
                                                                    random_seed=None,
                                                                    segment_index=i_score,
                                                                    max_time_sec=max_time_sec)
            else:
                try:
                    ref_segment = reference_waveform.get_segment(
                        duration_sec=duration_sec,
                        segment_start_sec=input_segment.start_time_sec,
                        segment_name=f"{reference_waveform.name}_{i_score}"
                    )
                except WaveformOperationException as e:
                    logger.warning(e)
                    logger.warning("Segment request failure: fewer scores will be returned than were requested.")
                    continue
            try:
                individual_score = self.calculate_score_from_waveforms(input_segment,
                                                                       ref_segment,
                                                                       **kwargs)

                score_results.append(individual_score)
            except Exception as e:
                logger.error(e)
                logger.error("Score calculation failed. Skipping this score")

        return np.array(score_results)

    def calculate_multiple_sequential(self,
                                      input_waveform: AudioWaveform,
                                      reference_waveform: AudioWaveform,
                                      duration_sec: float,
                                      offset_sec: float = DEFAULT_STARTING_OFFSET,
                                      num_segments: int = DEFAULT_NUM_SEGMENTS,
                                      sync_waveforms: bool = False,
                                      print_status: bool = False,
                                      **kwargs) -> np.ndarray:
        """
        Calculate scores for multiple sequential segments of a waveform

        Args:
            input_waveform (AudioWaveform): input waveform to assess
            reference_waveform (AudioWaveform): reference waveform used to compare
            duration_sec (float): duration in seconds of each randomly selected segment
            offset_sec (float): offset in seconds at the beginning of the waveform that is ignored
            num_segments (int): number of segments to randomly select and evaluate
            sync_waveforms (bool): whether to attempt to sync the start times of the segments
                for the two files.  Note that if the sampling rates differ, the lower sampling rate
                waveform will be upsampled.
            print_status (bool): whether to print a status message to the screen for monitoring progress

        Returns:
            Numpy array of scores for the sequential segments
        """

        if len(kwargs) > 0:
            logger.info(f"Ignoring extra kwargs passed in: {kwargs}")

        if sync_waveforms:
            input_waveform, reference_waveform = AudioWaveform.get_synced_waveforms(input_waveform,
                                                                                    reference_waveform)

        num_input_segments = input_waveform.get_num_segments(duration_sec=duration_sec, offset_sec=offset_sec)
        num_ref_segments = reference_waveform.get_num_segments(duration_sec=duration_sec, offset_sec=offset_sec)

        if num_input_segments < num_segments or num_ref_segments < num_segments:
            raise ScoreCalculationException(f"Number of input segments ({num_input_segments}) or number of reference "
                                            f"segments ({num_ref_segments}) is less than requested "
                                            f"number ({num_segments})")

        score_results = []

        logger.info(f"Using {duration_sec} second samples to calculate scores.")

        for i_score in range(num_segments):
            if print_status and (i_score + 1) % 10 == 0:
                logger.info(f"Score {i_score + 1} of {num_segments}")

            input_segment = input_waveform.get_segment(duration_sec=duration_sec,
                                                       segment_start_sec=offset_sec + duration_sec * i_score,
                                                       segment_name=f"{input_waveform.name}_{i_score}"
                                                       )
            if not sync_waveforms:
                ref_segment = reference_waveform.get_segment(duration_sec=duration_sec,
                                                             segment_start_sec=offset_sec + duration_sec * i_score,
                                                             segment_name=f"{reference_waveform.name}_{i_score}"
                                                             )
            else:
                try:
                    ref_segment = reference_waveform.get_segment(
                        duration_sec=duration_sec,
                        segment_start_sec=input_segment.start_time_sec,
                        segment_name=f"{reference_waveform.name}_{i_score}"
                    )
                except WaveformOperationException:
                    logger.warning("Segment request failure: fewer scores will be returned than were requested.")
                    continue

            try:
                individual_score = self.calculate_score_from_waveforms(input_segment,
                                                                       ref_segment,
                                                                       **kwargs)

                score_results.append(individual_score)
            except Exception as e:
                logger.error(e)
                logger.error("Score calculation failed. Skipping this score")

        return np.array(score_results)

    def calculate_average_score(
            self,
            input_waveform: AudioWaveform,
            reference_waveform: AudioWaveform,
            duration_sec: float,
            offset_sec: float = DEFAULT_STARTING_OFFSET,
            num_segments_in_avg: int = DEFAULT_NUM_SEGMENTS,
            score_spread_requirement: float = DEFAULT_SCORE_SPREAD_REQUIREMENT,
            sync_waveforms: bool = False,
            max_attempts: int = 10,
            randomize: bool = False,
            random_seed: int = None,
            **kwargs
    ) -> float:
        """
        Segment the input_waveform and reference_waveform waveforms to be of duration specified by `duration`.
        Specify the number of segments to include in the average and the required spread in score values required
        before calculating the average. If randomize is set to True, random segments of the waveforms will be
        compared, otherwise the segments will be sequential chunks of the waveforms

        Args:
            input_waveform (AudioWaveform): input waveform to assess
            reference_waveform (AudioWaveform): reference waveform used to compare
            duration_sec (float): duration in seconds of the waveform segments
            offset_sec (float): offset to ignore from start of waveform in seconds
            num_segments_in_avg (int): number of segments to use in the average. Defaults to DEFAULT_NUM_SEGMENTS
            sync_waveforms (bool): whether to attempt to sync the start times of the segments
                for the two files.  Note that if the sampling rates differ, the lower sampling rate
                waveform will be upsampled.
            score_spread_requirement (float): the spread in scores required before an average is calculated.
                Defaults to DEFAULT_SCORE_SPREAD_REQUIREMENT
            max_attempts (int): Maximum number of attempted segments to calculate to achieve the
                score_spread_requirement before giving up
            randomize (bool): If True (default), then randomly select segments from the waveforms. If False, then
                sequential segments will be selected
            random_seed (int): optional starting random seed. Defaults to None

        Returns:
            The average calculated score
        """

        if len(kwargs) > 0:
            logger.info(f"Ignoring extra kwargs passed in: {kwargs}")

        for i_attempt in range(max_attempts):

            if randomize:
                seed = random_seed
                if i_attempt > 0:
                    # only set the seed once
                    seed = None

                score_results = self.calculate_multiple_random(input_waveform=input_waveform,
                                                               reference_waveform=reference_waveform,
                                                               duration_sec=duration_sec,
                                                               offset_sec=offset_sec,
                                                               num_segments=num_segments_in_avg,
                                                               sync_waveforms=sync_waveforms,
                                                               random_seed=seed,
                                                               **kwargs)
            else:
                cycle_offset = offset_sec + i_attempt * (duration_sec * 0.2)
                score_results = self.calculate_multiple_sequential(input_waveform=input_waveform,
                                                                   reference_waveform=reference_waveform,
                                                                   duration_sec=duration_sec,
                                                                   offset_sec=cycle_offset,
                                                                   num_segments=num_segments_in_avg,
                                                                   sync_waveforms=sync_waveforms,
                                                                   **kwargs)

            if np.max(score_results) - np.min(score_results) > score_spread_requirement:
                logger.warning(f"Warning for attempt {i_attempt + 1}: score results have too much spread.")
            elif len(score_results) < num_segments_in_avg:
                logger.warning(f"Warning for attempt {i_attempt + 1}: too few score results {len(score_results)}for "
                               f"average.")
            else:
                average_score = np.mean(score_results)
                return float(average_score)

        # if we fail to converge, return None
        return np.nan

