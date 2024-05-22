import numpy as np
from pydub import AudioSegment
from pydub.utils import get_array_type
from enum import Enum


class BaseBand:
    def __init__(self, segment: AudioSegment):
        self.segment = segment
        self.fs = segment.frame_rate
        self.samples = np.array(segment.get_array_of_samples(), dtype=np.float32)
        self.channels = segment.channels
        self.sample_width = segment.sample_width

    def apply_gain(self, data, gain_db):
        factor = 10 ** (gain_db / 20)
        return data * factor

    def get_filtered_segment(self, filtered_samples):
        new_data = np.array(filtered_samples, dtype=get_array_type(self.sample_width * 8))
        new_segment = self.segment._spawn(new_data.tobytes())
        return new_segment

    def change_band_gain(self, freq_range: tuple, gain: float) -> AudioSegment:
        samples = self.samples
        sample_rate = self.fs

        freqs = np.fft.rfftfreq(len(samples), d=1 / sample_rate)
        fft_samples = np.fft.rfft(samples)

        band_mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
        fft_samples[band_mask] *= 10 ** (gain / 20.0)

        new_samples = np.fft.irfft(fft_samples)
        new_samples = np.int16(new_samples / np.max(np.abs(new_samples)) * 32767)

        new_segment = self.segment._spawn(new_samples.tobytes())
        return new_segment


class Band62Hz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((31, 62), gain_db)


class Band125Hz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((62, 125), gain_db)


class Band250Hz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((125, 250), gain_db)


class Band500Hz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((250, 500), gain_db)


class Band1kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((500, 1000), gain_db)


class Band2kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((1000, 2000), gain_db)


class Band4kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((2000, 4000), gain_db)


class Band8kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((4000, 8000), gain_db)


class Band16kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        return self.change_band_gain((8000, 16000), gain_db)


class Equalizer(Enum):
    BAND_62_HZ = lambda segment: Band62Hz(segment)
    BAND_125_HZ = lambda segment: Band125Hz(segment)
    BAND_250_HZ = lambda segment: Band250Hz(segment)
    BAND_500_HZ = lambda segment: Band500Hz(segment)
    BAND_1_KHZ = lambda segment: Band1kHz(segment)
    BAND_2_KHZ = lambda segment: Band2kHz(segment)
    BAND_4_KHZ = lambda segment: Band4kHz(segment)
    BAND_8_KHZ = lambda segment: Band8kHz(segment)
    BAND_16_KHZ = lambda segment: Band16kHz(segment)


def apply_equalizer(segment: AudioSegment, adjustments: dict) -> AudioSegment:
    temp = segment
    for band, gain in adjustments.items():
        temp = band(temp).apply(gain)
    return temp


# Example usage
if __name__ == "__main__":
    segment = AudioSegment.from_file("10.mp3")

    adjustments = {
        Equalizer.BAND_62_HZ: 24.0,
        Equalizer.BAND_125_HZ: 24.0,
        Equalizer.BAND_250_HZ: 24.0,
        Equalizer.BAND_500_HZ: 24.0,
        Equalizer.BAND_1_KHZ: 24.0,
        Equalizer.BAND_2_KHZ: 24.0,
        Equalizer.BAND_4_KHZ: 24.0,
        Equalizer.BAND_8_KHZ: 24.0,
        Equalizer.BAND_16_KHZ: 24.0,
    }

    equalized_segment = apply_equalizer(segment, adjustments)

    reversed_adjustments = {k: -v for k, v in adjustments.items()}
    reversed_segment = apply_equalizer(equalized_segment, reversed_adjustments)

    # Export the modified audio
    reversed_segment.export("1231212313re.mp3", format="mp3")

