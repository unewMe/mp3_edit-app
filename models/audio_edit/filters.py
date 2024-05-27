from enum import Enum, StrEnum

import numpy as np
from scipy.signal import butter, lfilter
import abc


class FilterType(Enum):
    LOW_PASS = "Low Pass"
    HIGH_PASS = "High Pass"
    ECHO = "Echo"
    REVERB = "Reverb"
    FLANGER = "Flanger"

    def create_filter(self, audio):
        match self:
            case FilterType.LOW_PASS:
                return LowPassFilter(audio, 5000, 5).apply()
            case FilterType.HIGH_PASS:
                return HighPassFilter(audio, 200, 5).apply()
            case FilterType.ECHO:
                return EchoFilter(audio, delay_ms=500, decay_factor=0.5).apply()
            case FilterType.REVERB:
                return ReverbFilter(audio).apply()
            case FilterType.FLANGER:
                return FlangerFilter(audio, delay_ms=5, speed=0.5).apply()


class BaseFilter(metaclass=abc.ABCMeta):
    """
    Abstract base class for audio filters.
    Audio is instance of AudioFile
    """

    samples: np.ndarray  # Array of audio samples
    fs: int  # Frame rate of the audio

    def __init__(self, audio):
        self.audio = audio
        self.samples = np.array(audio.get_array_of_samples())
        self.fs = audio.frame_rate

    @abc.abstractmethod
    def apply(self):
        """
        Applies the filter to the audio.
        """
        pass

    def cast_to_scaled_int16(self, samples: np.ndarray) -> np.ndarray:
        """
        Casts the samples to 16-bit integers and scales them to the range of -32768 to 32767.
        """
        max_val = np.max(np.abs(samples))
        return np.int16(samples / max_val * 32767)


class LowPassFilter(BaseFilter):
    cutoff: int  # Cutoff frequency for the filter
    order: int  # Order of the filter

    def __init__(self, audio, cutoff: int = 5000, order: int = 5):
        super().__init__(audio)
        self.cutoff = cutoff
        self.order = order

    def apply(self):
        """
        Apply the low pass filter to the audio.
        """
        from models.audio_edit.AudioFile import AudioFile
        nyq = 0.5 * self.fs
        normal_cutoff = self.cutoff / nyq
        b, a = butter(self.order, normal_cutoff, btype='low', analog=False)
        filtered_samples = lfilter(b, a, self.samples)

        filtered_samples_bytes = self.cast_to_scaled_int16(filtered_samples).tobytes()

        return AudioFile.combine_with_audio_segment(self.audio, self.audio._spawn(filtered_samples_bytes))


class HighPassFilter(BaseFilter):
    cutoff: int  # Cutoff frequency for the filter
    order: int  # Order of the filter
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

        filtered_samples_bytes = self.cast_to_scaled_int16(filtered_samples).tobytes()

        return AudioFile.combine_with_audio_segment(self.audio, self.audio._spawn(filtered_samples_bytes))


class EchoFilter(BaseFilter):
    delay_ms: int  # Delay in milliseconds
    decay_factor: float  # Decay factor for the echo

    def __init__(self, audio, delay_ms: int = 500, decay_factor: float = 0.5):
        super().__init__(audio)
        self.delay_ms = delay_ms
        self.decay_factor = decay_factor

    def apply(self):
        """
        Apply the echo filter to the audio.
        """
        from models.audio_edit.AudioFile import AudioFile

        delay_samples = int(self.fs * self.delay_ms / 1000)
        echo = np.zeros_like(self.samples)
        echo[delay_samples:] = self.samples[:-delay_samples] * self.decay_factor
        echo_samples = self.samples + echo

        filtered_samples_bytes = self.cast_to_scaled_int16(echo_samples).tobytes()

        return AudioFile.combine_with_audio_segment(self.audio, self.audio._spawn(filtered_samples_bytes))


class ReverbFilter(BaseFilter):
    reverb_time: float  # Reverb time in seconds
    decay: float  # Decay factor for the reverb

    def __init__(self, audio, reverb_time=0.02, decay=0.3):
        super().__init__(audio)
        self.reverb_time = reverb_time
        self.decay = decay

    def apply(self):
        """
        Apply the reverb filter to the audio.
        """
        from models.audio_edit.AudioFile import AudioFile

        num_samples = int(self.fs * self.reverb_time)
        impulse_response = np.exp(-np.arange(num_samples) / (self.fs * self.decay))
        reverb_samples = np.convolve(self.samples, impulse_response, mode='full')[:len(self.samples)]

        filtered_samples_bytes = self.cast_to_scaled_int16(reverb_samples).tobytes()

        return AudioFile.combine_with_audio_segment(self.audio, self.audio._spawn(filtered_samples_bytes))


class FlangerFilter(BaseFilter):
    delay_ms: int  # Delay in milliseconds
    speed: float  # Speed of the flanger effect

    def __init__(self, audio, delay_ms=5, speed=0.5):
        super().__init__(audio)
        self.delay_ms = delay_ms
        self.speed = speed

    def apply(self):
        """
        Apply the flanger filter to the audio.
        """
        from models.audio_edit.AudioFile import AudioFile

        flanger_samples = np.copy(self.samples)
        max_delay_samples = int(self.fs * self.delay_ms / 1000)
        for i in range(max_delay_samples, len(flanger_samples)):
            delay = int(max_delay_samples * (1 + np.sin(2 * np.pi * i * self.speed / self.fs)) / 2)
            flanger_samples[i] += flanger_samples[i - delay] * 0.5

        filtered_samples_bytes = self.cast_to_scaled_int16(flanger_samples).tobytes()

        return AudioFile.combine_with_audio_segment(self.audio, self.audio._spawn(filtered_samples_bytes))
