import numpy as np
from scipy.signal import butter, lfilter
from pydub import AudioSegment
from pydub.utils import get_array_type
from enum import Enum

def butter_bandpass(lowcut, highcut, fs, order=5):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band')
    return b, a

def bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y

class BaseBand:
    def __init__(self, segment: AudioSegment):
        self.segment = segment
        self.last_gained = 0.0
        self.fs = segment.frame_rate
        self.samples = np.array(segment.get_array_of_samples(), dtype=np.float32)
        self.channels = segment.channels

    def apply_gain(self, data, gain_db):
        factor = 10 ** (gain_db / 20)
        return data * factor

    def get_filtered_segment(self, filtered_samples):
        new_data = np.array(filtered_samples, dtype=get_array_type(self.segment.sample_width * 8))
        new_segment = self.segment._spawn(new_data.tobytes())
        return new_segment

    def update_segment(self, new_segment):
        self.segment = new_segment
        self.samples = np.array(self.segment.get_array_of_samples(), dtype=np.float32)

class Band62Hz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 31, 62, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Band125Hz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 62, 125, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Band250Hz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 125, 250, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Band500Hz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 250, 500, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Band1kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 500, 1000, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Band2kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 1000, 2000, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Band4kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 2000, 4000, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Band8kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 4000, 8000, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Band16kHz(BaseBand):
    def apply(self, gain_db: float) -> AudioSegment:
        total_gain = gain_db - self.last_gained
        if total_gain:
            self.last_gained = gain_db
            filtered = bandpass_filter(self.samples, 8000, 16000, self.fs)
            gained = self.apply_gain(filtered, total_gain)
            new_segment = self.get_filtered_segment(gained)
            self.update_segment(new_segment)
        return self.segment

class Equalizer(Enum):
    BAND_62_HZ = Band62Hz
    BAND_125_HZ = Band125Hz
    BAND_250_HZ = Band250Hz
    BAND_500_HZ = Band500Hz
    BAND_1_KHZ = Band1kHz
    BAND_2_KHZ = Band2kHz
    BAND_4_KHZ = Band4kHz
    BAND_8_KHZ = Band8kHz
    BAND_16_KHZ = Band16kHz

def apply_equalizer(segment: AudioSegment, adjustments: dict) -> AudioSegment:
    results = []
    for band_enum, gain_db in adjustments.items():
        band_class = band_enum.value(segment)
        result_segment = band_class.apply(gain_db)
        results.append(result_segment.get_array_of_samples())

    combined = np.sum(results, axis=0)
    combined_segment = segment._spawn(np.array(combined, dtype=get_array_type(segment.sample_width * 8)).tobytes())
    return combined_segment

# Example usage
if __name__ == "__main__":

    segment = AudioSegment.from_file("Beethoven.mp3")


    adjustments = {
        Equalizer.BAND_62_HZ: 6.0,
        Equalizer.BAND_125_HZ: -3.0,
        Equalizer.BAND_250_HZ: 0.0,
        Equalizer.BAND_500_HZ: 3.0,
        Equalizer.BAND_1_KHZ: -6.0,
        Equalizer.BAND_2_KHZ: 6.0,
        Equalizer.BAND_4_KHZ: -12.0,
        Equalizer.BAND_8_KHZ: 0.0,
        Equalizer.BAND_16_KHZ: 3.0,
    }

    adjustments2 = {
        Equalizer.BAND_62_HZ: -6.0,
        Equalizer.BAND_125_HZ: 3.0,
        Equalizer.BAND_250_HZ: 0.0,
        Equalizer.BAND_500_HZ: -3.0,
        Equalizer.BAND_1_KHZ: 6.0,
        Equalizer.BAND_2_KHZ: -6.0,
        Equalizer.BAND_4_KHZ: 12.0,
        Equalizer.BAND_8_KHZ: 0.0,
        Equalizer.BAND_16_KHZ: -3.0,
    }


    equalized_segment = apply_equalizer(segment, adjustments)
    equalized_segment = apply_equalizer(equalized_segment, adjustments2)

    # Export the modified audio
    equalized_segment.export("equalized_example.mp3", format="mp3")
