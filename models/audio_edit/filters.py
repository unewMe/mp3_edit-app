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

    samples: np.ndarray  # Array of audio samples
    fs: int  # Frame rate of the audio
    cutoff: int  # Cutoff frequency for the filter
    order: int  # Order of the filter

    def __init__(self, audio, cutoff: int, order: int):
        self.audio = audio
        self.samples = np.array(audio.get_array_of_samples())
        self.fs = audio.frame_rate
        self.cutoff = cutoff
        self.order = order

    @abc.abstractmethod
    def apply(self):
        """
        Applies the filter to the audio.
        """
        pass


class LowPassFilter(BaseFilter):
    def __init__(self, audio, cutoff: int = 5000, order: int = 5):
        super().__init__(audio, cutoff, order)

    def apply(self):
        """
        Apply the low pass filter to the audio.
        """
        from models.audio_edit.AudioFile import AudioFile
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        filtered_samples = lfilter(b, a, self.samples)
        max_val = np.max(np.abs(filtered_samples))
        scaled_samples = np.int16(filtered_samples / max_val * 32767)

        filtered_samples_bytes = scaled_samples.tobytes()

        return AudioFile.from_segment(self.audio._spawn(filtered_samples_bytes))


class HighPassFilter(BaseFilter):
    def __init__(self, audio, cutoff: int = 200, order: int = 5):
        super().__init__(audio)
        self.cutoff = cutoff
        self.order = order

    def apply(self):
        """
        Apply the high pass filter to the audio.
        """
        from models.audio_edit.AudioFile import AudioFile

        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.order, normal_cutoff, btype='high', analog=False)
        filtered_samples = lfilter(b, a, self.samples)
        max_val = np.max(np.abs(filtered_samples))
        scaled_samples = np.int16(filtered_samples / max_val * 32767)

        filtered_samples_bytes = scaled_samples.tobytes()
        return AudioFile.from_segment(self.audio._spawn(filtered_samples_bytes))
