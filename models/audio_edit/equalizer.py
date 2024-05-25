import numpy as np
from pydub import AudioSegment
from pydub.utils import get_array_type
from enum import Enum


class Bands(Enum):
    HZ_62 = (31, 62)
    HZ_125 = (62, 125)
    HZ_250 = (125, 250)
    HZ_500 = (250, 500)
    HZ_1K = (500, 1000)
    HZ_2K = (1000, 2000)
    HZ_4K = (2000, 4000)
    HZ_8K = (4000, 8000)
    HZ_16K = (8000, 16000)


class Equalizer:
    def __init__(self, segment):
        self.segment = segment
        self.fs = segment.frame_rate
        self.samples = np.array(segment.get_array_of_samples(), dtype=np.float32)
        self.channels = segment.channels
        self.sample_width = segment.sample_width
        self.gains = {band: 0.0 for band in Bands}

    def change_band_gain(self, band: Bands, gain: float):
        from models.audio_edit.AudioFile import AudioFile
        freq_range = band.value
        previous_gain = self.gains[band]
        gain_change = gain - previous_gain

        samples = self.samples
        sample_rate = self.fs

        freqs = np.fft.rfftfreq(len(samples), d=1 / sample_rate)
        fft_samples = np.fft.rfft(samples)

        band_mask = (freqs >= freq_range[0]) & (freqs <= freq_range[1])
        fft_samples[band_mask] *= 10 ** (gain_change / 20.0)

        new_samples = np.fft.irfft(fft_samples)
        new_samples = np.int16(new_samples / np.max(np.abs(new_samples)) * 32767)

        new_segment = self.segment._spawn(new_samples.tobytes())

        # Update the gain for the band
        self.gains[band] = gain
        self.segment = AudioFile.combine_with_audio_segment(self.segment, new_segment)

        return self.segment

    def get_all_bands(self):
        return self.gains

