import numpy as np
import matplotlib.pyplot as plt
from models.audio_edit.AudioFile import AudioFile
from scipy.signal import spectrogram


class AudioVisualizer:
    def __init__(self, audio_file):
        """
        Konstruktor klasy AudioVisualizer.

        :param audio_file: Instancja klasy AudioFile.
        """
        self.audio_file = audio_file
        self.samples = np.array(self.audio_file.get_array_of_samples())
        self.frame_rate = self.audio_file.frame_rate

    def plot_waveform(self):
        """
        Wizualizuje amplitudę dźwięku w czasie.
        """
        plt.figure(figsize=(10, 4))
        plt.plot(self.samples)
        plt.title('Waveform')
        plt.xlabel('Sample Number')
        plt.ylabel('Amplitude')
        plt.grid(True)
        plt.show()

    def plot_spectrogram(self):
        """
        Wizualizuje spektrogram dźwięku.
        """
        f, t, Sxx = spectrogram(self.samples, self.frame_rate)
        plt.figure(figsize=(10, 4))
        plt.pcolormesh(t, f, 10 * np.log10(Sxx), shading='gouraud')
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.title('Spectrogram')
        plt.colorbar(label='Intensity [dB]')
        plt.show()


# Przykład użycia:
audio_path = 'Beethoven.mp3'
audio_file = AudioFile.from_file(audio_path)
visualizer = AudioVisualizer(audio_file)
visualizer.plot_waveform()
visualizer.plot_spectrogram()
