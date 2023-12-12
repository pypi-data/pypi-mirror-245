from pyscreech.audio import AudioWaveform
from pyscreech.stipa import StipaCalculator
from tests.conftest import reference_stipa_waveform


input = AudioWaveform.load_audio("/Users/blackstoma/DEC/repos/septools/python/resources/MITLL_device_STIPA_T3-2.wav")
ref = AudioWaveform.load_audio("/Users/blackstoma/DEC/repos/septools/python/resources/StipaV5_CEA.wav")

duration = 25
offset = 5

duration = 25
offset = 5

stipa_calculator = StipaCalculator()

stipa_score = stipa_calculator.calculate_average_score(input_waveform=input,
                                                       reference_waveform=ref,
                                                       duration_sec=duration,
                                                       offset_sec=offset,
                                                       randomize=False)

print(stipa_score)

