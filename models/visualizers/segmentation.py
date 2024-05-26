from pydub import AudioSegment, silence
import librosa
import numpy as np
import matplotlib.pyplot as plt
from .utils import convert_to_librosa_format


class SegmentationAnalysis:
    _audio_segment: AudioSegment  # AudioSegment object
    _y: np.ndarray  # Audio signal
    _sr: int  # Sample rate

    def __init__(self, audio_segment: AudioSegment):
        self._audio_segment = audio_segment
        self._y, self._sr = convert_to_librosa_format(audio_segment.get_array_of_samples(), audio_segment.channels,
                                                      audio_segment.frame_rate)

    def _detect_silence_segments(self, min_silence_len: int = 1000, silence_thresh: int = -40) -> list[
        tuple[float, float]]:
        """Detects silence segments in the audio signal"""

        silence_segments = silence.detect_silence(self._audio_segment,
                                                  min_silence_len=min_silence_len,
                                                  silence_thresh=silence_thresh)
        silence_segments = [(start / 1000, stop / 1000) for start, stop in silence_segments]  # Convert to seconds
        return silence_segments

    def _segment_by_beats(self):
        """Segments the audio signal by beats"""

        tempo, beats = librosa.beat.beat_track(y=self._y, sr=self._sr)
        beat_times = librosa.frames_to_time(beats, sr=self._sr)
        return beat_times

    def plot_silence_segments(self, file_path: str) -> None:
        """Plots the silence segments in the audio signal"""

        silence_segments = self._detect_silence_segments()
        plt.figure(figsize=(10, 4))
        plt.plot(self._y, label='Audio Signal')
        for i, (start, stop) in enumerate(silence_segments):
            if i == 0:
                plt.axvspan(start * self._sr, stop * self._sr, color='red', alpha=0.5, label='Silence')
            else:
                plt.axvspan(start * self._sr, stop * self._sr, color='red', alpha=0.5)
        plt.xlabel('Samples')
        plt.ylabel('Amplitude')
        plt.title('Silence Segments')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(file_path)

    def plot_beat_segments(self, file_path: str) -> None:
        """Plots the audio signal segmented by beats"""

        beat_times = self._segment_by_beats()
        plt.figure(figsize=(10, 4))
        times = np.arange(len(self._y)) / self._sr
        plt.plot(times, self._y, label='Audio Signal')
        for i, beat in enumerate(beat_times):
            if i == 0:
                plt.axvline(beat, color='green', linestyle='--', label='Beat')
            else:
                plt.axvline(beat, color='green', linestyle='--')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.title('Beat Segments')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.savefig(file_path)
