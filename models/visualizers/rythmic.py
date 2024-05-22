from pydub import AudioSegment
import librosa
import librosa.display
import numpy as np
import matplotlib.pyplot as plt

class RhythmicAnalysis:

    audio_segment: AudioSegment
    y: np.ndarray
    sr: int

    def __init__(self, audio_segment: AudioSegment):
        self.audio_segment = audio_segment
        self.y, self.sr = self._convert_to_librosa_format()

    def _convert_to_librosa_format(self):
        # Convert AudioSegment to numpy array
        samples = np.array(self.audio_segment.get_array_of_samples())
        if self.audio_segment.channels == 2:
            samples = samples.reshape((-1, 2)).mean(axis=1)  # Convert stereo to mono
        y = samples.astype(np.float32)

        # Normalize to [-1, 1] range if needed
        if np.issubdtype(samples.dtype, np.integer):
            y /= np.iinfo(samples.dtype).max

        sr = self.audio_segment.frame_rate
        return y, sr

    def analyze_tempogram(self):
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        tempogram = librosa.feature.tempogram(onset_envelope=onset_env, sr=self.sr)

        plt.figure(figsize=(10, 4))
        librosa.display.specshow(tempogram, sr=self.sr, hop_length=512, x_axis='time', y_axis='tempo')
        plt.title('Tempogram')
        plt.colorbar()
        plt.tight_layout()
        plt.show()

    def analyze_beats(self):
        onset_env = librosa.onset.onset_strength(y=self.y, sr=self.sr)
        tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=self.sr)

        plt.figure(figsize=(10, 4))
        times = librosa.frames_to_time(beats, sr=self.sr)
        plt.plot(times, onset_env[beats], 'ro')
        plt.title('Beat Detection')
        plt.xlabel('Time (s)')
        plt.ylabel('Onset Strength')
        plt.tight_layout()
        plt.show()

        print(f'Tempo: {tempo} BPM')
        print(f'Beats: {times}')


audio_segment = AudioSegment.from_file('Beethoven.mp3')
analysis = RhythmicAnalysis(audio_segment)
analysis.analyze_tempogram()
analysis.analyze_beats()
