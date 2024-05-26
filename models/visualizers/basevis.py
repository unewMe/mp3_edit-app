import numpy as np
import matplotlib.pyplot as plt
from models.audio_edit.AudioFile import AudioFile
from scipy.signal import spectrogram


class AudioVisualizer:
    """
    Class to visualize audio files.
    """

    _audio_file: AudioFile # Audio file to visualize
    _samples: np.ndarray # Samples of the audio file
    _frame_rate: int # Frame rate of the audio file

    def __init__(self, audio_file: AudioFile):
        """
        AudioFile constructor.
        """
        self._audio_file = audio_file
        self._samples = np.array(self._audio_file.get_array_of_samples())
        self._frame_rate = self._audio_file.frame_rate

    def plot_waveform(self, file_path: str) -> None:
        """
        Visualizes the waveform of the sound file.
        """
        plt.figure(figsize=(10, 4))
        plt.plot(self._samples)
        plt.title('Waveform')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.savefig(file_path)

    def plot_spectrogram(self, file_path: str) -> None:
        """
        Visualizes the intensity of the sound at different frequencies over time.
        """
        f, t, Sxx = spectrogram(self._samples, self._frame_rate)
        plt.figure(figsize=(10, 4))
        plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title('Spectrogram')
        plt.colorbar(label='Intensity [dB]')
        plt.tight_layout()
        plt.savefig(file_path)


