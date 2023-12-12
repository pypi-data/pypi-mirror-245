"""Methods used for calculating STOI score"""

import numpy as np
from loguru import logger

from .audio import AudioWaveform
from pystoi import stoi
from .score import ScoreCalculator


class StoiCalculationException(Exception):
    pass


class StoiCalculator(ScoreCalculator):

    def calculate_score_from_waveforms(self,
                                       input_waveform: AudioWaveform,
                                       reference_waveform: AudioWaveform,
                                       extended: bool = False,
                                       **kwargs) -> float:
        """
        Calculate STOI score for two waveforms using pystoi

        Args:
            input_waveform (AudioWaveform): input waveform to assess
            reference_waveform (AudioWaveform): reference waveform used to compare
            extended (bool): argument passed to the stoi function. See pystoi documentation

        Returns:
            A single calculated STOI score
        """

        if len(kwargs) > 0:
            logger.info(f"Ignoring extra kwargs passed in: {kwargs}")

        if input_waveform.sample_rate != reference_waveform.sample_rate:
            raise StoiCalculationException("Sample rates of waveforms must match")

        if len(input_waveform.timeseries) != len(reference_waveform.timeseries):
            raise StoiCalculationException("Lengths of waveforms must match")

        score = stoi(reference_waveform.timeseries,
                     input_waveform.timeseries,
                     input_waveform.sample_rate,
                     extended=extended)

        return score



