import time
from models.timers.Timer import Timer
import pygame
from models.audio_edit.AudioFile import AudioFile
import abc


class Player(metaclass=abc.ABCMeta):
    play_obj: pygame.mixer.Sound | None  # Play object which represents the sound file
    channel: pygame.mixer.Channel | None  # Channel , which is used to play the sound file
    is_playing: bool  # Flag to check if the sound file is playing
    audio_file: AudioFile | None  # Pydub audio segment for in-memory editing

    def __init__(self):
        pygame.mixer.init()
        self.play_obj = None
        self.channel = None
        self.is_playing = False
        self.audio_file = None

    @abc.abstractmethod
    def is_loaded(self):
        """
        Check if a sound file is loaded.
        """
        pass

    @abc.abstractmethod
    def load(self, audio_file: AudioFile):
        """
        Load a sound file from the given file path.
        """
        pass

    @abc.abstractmethod
    def play(self):
        """
        Play the loaded sound file.
        """
        pass

    @abc.abstractmethod
    def pause(self):
        """
        Pause the sound file.
        """
        pass

    @abc.abstractmethod
    def resume(self):
        """
        Resume the sound file.
        """
        pass

    @abc.abstractmethod
    def stop(self):
        """
        Stop the sound file.
        """
        pass

    @abc.abstractmethod
    def set_volume(self, volume: float):
        """
        Set the volume of the sound file.
        """
        pass

    def wait_for_finish(self):
        """
        Wait for the sound file to finish playing.
        """
        if self.is_loaded() and self.is_playing:
            while self.channel.get_busy():
                pygame.time.delay(100)

    def get_total_time(self):

        if self.audio_file:
            total_seconds = self.audio_file.duration_seconds
            hours = total_seconds // 3600
            total_seconds %= 3600
            minutes = total_seconds // 60
            total_seconds %= 60
            seconds = total_seconds % 60
            return hours, minutes, seconds
        else:
            return (0, 0, 0)
