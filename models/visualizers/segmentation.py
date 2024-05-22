from pydub import AudioSegment, silence
import librosa
import numpy as np
import matplotlib.pyplot as plt

class AudioSegmentation:
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

    def detect_silence_segments(self, min_silence_len=1000, silence_thresh=-40):
        silence_segments = silence.detect_silence(self.audio_segment,
                                                  min_silence_len=min_silence_len,
                                                  silence_thresh=silence_thresh)
        silence_segments = [(start / 1000, stop / 1000) for start, stop in silence_segments]  # Convert to seconds
        return silence_segments

    def segment_by_beats(self):
        tempo, beats = librosa.beat.beat_track(y=self.y, sr=self.sr)
        beat_times = librosa.frames_to_time(beats, sr=self.sr)
        return beat_times

    def plot_silence_segments(self, silence_segments):
        plt.figure(figsize=(10, 4))
        plt.plot(self.y, label='Audio Signal')
        for i, (start, stop) in enumerate(silence_segments):
            if i == 0:
                plt.axvspan(start * self.sr, stop * self.sr, color='red', alpha=0.5, label='Silence')
            else:
                plt.axvspan(start * self.sr, stop * self.sr, color='red', alpha=0.5)
        plt.xlabel('Samples')
        plt.ylabel('Amplitude')
        plt.title('Silence Segments')
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()

    def plot_beat_segments(self, beat_times):
        plt.figure(figsize=(10, 4))
        times = np.arange(len(self.y)) / self.sr
        plt.plot(times, self.y, label='Audio Signal')
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
        plt.show()


audio_segment = AudioSegment.from_file('Beethoven.mp3')
segmentation = AudioSegmentation(audio_segment)


silence_segments = segmentation.detect_silence_segments()
segmentation.plot_silence_segments(silence_segments)


beat_times = segmentation.segment_by_beats()
segmentation.plot_beat_segments(beat_times)
