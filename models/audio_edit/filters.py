from enum import Enum
from pydub import AudioSegment
import numpy as np
from scipy.signal import butter, lfilter
import abc


class FilterType(Enum):
    LOW_PASS = lambda audio: LowPassFilter(audio, 5000, 5)
    HIGH_PASS = lambda audio: HighPassFilter(audio, 200, 5)

class BaseFilter(metaclass=abc.ABCMeta):
    def __init__(self, audio: AudioSegment):
        self.audio = audio
        self.samples = np.array(audio.get_array_of_samples())
        self.fs = audio.frame_rate

    @abc.abstractmethod
    def apply(self):
        pass

class LowPassFilter(BaseFilter):
    def __init__(self, audio, cutoff=5000, order=5):
        super().__init__(audio)
        self.cutoff = cutoff
        self.order = order

    def apply(self):
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        filtered_samples = lfilter(b, a, self.samples)
        return self.audio._spawn(filtered_samples)

class HighPassFilter(BaseFilter):
    def __init__(self, audio, cutoff=200, order=5):
        super().__init__(audio)
        self.cutoff = cutoff
        self.order = order

    def apply(self):
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.order, normal_cutoff, btype='high', analog=False)
        filtered_samples = lfilter(b, a, self.samples)
        return self.audio._spawn(filtered_samples)

