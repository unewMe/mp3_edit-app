from pydub import AudioSegment
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt
from .utils import convert_to_librosa_format


class RhythmicAnalysis:
    _audio_segment: AudioSegment  # AudioSegment object
    _y: np.ndarray  # Audio signal as numpy array
    _sr: int  # Sample rate of the audio signal

    def __init__(self, audio_segment: AudioSegment):
        self._audio_segment = audio_segment
        self._y, self._sr = convert_to_librosa_format(audio_segment.get_array_of_samples(), audio_segment.channels,
                                                      audio_segment.frame_rate)

    def analyze_tempogram(self, file_path: str) -> None:
        """Computes and plots the tempogram of the audio signal"""

        onset_env = librosa.onset.onset_strength(y=self._y, sr=self._sr)
        tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=self._sr)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(tempogram, sr=self._sr, hop_length=512, x_axis='time', y_axis='tempo')
        plt.title('Tempogram')
        plt.colorbar()
        plt.tight_layout()
        plt.savefig(file_path)

    def analyze_beats(self, file_path: str) -> None:
        """Detects beats in the audio signal and plots them on the onset strength curve"""

        onset_env = librosa.onset.onset_strength(y=self._y, sr=self._sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=self._sr)

        plt.figure(figsize=(10, 4))
        times = librosa.frames_to_time(beats, sr=self._sr)
        plt.plot(times, onset_env[beats], 'ro')
        plt.title('Beat Detection')
        plt.xlabel('Time (s)')
        plt.ylabel('Onset Strength')
        plt.tight_layout()
        plt.savefig(file_path)
