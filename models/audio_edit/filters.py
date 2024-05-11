from enum import Enum
from pydub import AudioSegment
import numpy as np
from scipy.signal import butter, lfilter
import abc


class FilterType(Enum):
    """
    Enum class for the different types of filters.
    """
    LOW_PASS = lambda audio: LowPassFilter(audio, 5000, 5)
    HIGH_PASS = lambda audio: HighPassFilter(audio, 200, 5)


class BaseFilter(metaclass=abc.ABCMeta):
    """
    Abstract base class for audio filters.
    """
    def __init__(self, audio: AudioSegment):
        self.audio = audio
        self.samples = np.array(audio.get_array_of_samples())
        self.fs = audio.frame_rate

    @abc.abstractmethod
    def apply(self):
        """
        Applies the filter to the audio.
        """
        pass


class LowPassFilter(BaseFilter):
    def __init__(self, audio: AudioSegment, cutoff: int = 5000, order: int = 5):
        super().__init__(audio)
        self.cutoff = cutoff
        self.order = order

    def apply(self):
        """
        Apply the low pass filter to the audio.
        """
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        filtered_samples = lfilter(b, a, self.samples)
        return self.audio._spawn(filtered_samples)


class HighPassFilter(BaseFilter):
    def __init__(self, audio: AudioSegment, cutoff: int = 200, order: int = 5):
        super().__init__(audio)
        self.cutoff = cutoff
        self.order = order

    def apply(self):
        """
        Apply the high pass filter to the audio.
        """

        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.order, normal_cutoff, btype='high', analog=False)
        filtered_samples = lfilter(b, a, self.samples)
        return self.audio._spawn(filtered_samples)
