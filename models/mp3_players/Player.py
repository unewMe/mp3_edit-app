import time
from models.timers.Timer import Timer
import pygame
from dataclasses import dataclass


class Player:
    timer: Timer  # Timer object to keep track of the time of the sound file
    play_obj: pygame.mixer.Sound | None   # Play object which represents the sound file
    channel: pygame.mixer.Channel | None   # Channel , which is used to play the sound file
    is_playing: bool   # Flag to check if the sound file is playing

    def __init__(self):
        pygame.mixer.init()
        self.play_obj = None
        self.channel = None
        self.is_playing = False
        self.timer = Timer()

    def is_loaded(self):
        """Check if a sound file is loaded."""
        return self.play_obj is not None

    def load(self, file_path):
        """Load a sound file."""
        self.stop()
        self.play_obj = pygame.mixer.Sound(file_path)

    def play(self):
        """Play the loaded sound file."""
        if self.is_loaded():
            self.channel = self.play_obj.play()
            self.is_playing = True
            self.timer.start()

    def pause(self):
        """Pause the sound file."""
        if self.is_loaded() and self.is_playing:
            self.channel.pause()
            self.is_playing = False
            self.timer.pause()

    def resume(self):
        """Resume the sound file."""
        if self.is_loaded() and not self.is_playing:
            self.channel.unpause()
            self.is_playing = True
            self.timer.resume()

    def stop(self):
        """Stop the sound file."""
        if self.is_loaded():
            self.channel.stop()
            self.is_playing = False
            self.timer.restart()

    def get_current_time(self):
        """Get the current time of the sound file."""
        return self.timer.get_time()

    def wait_for_finish(self):
        """Wait for the sound file to finish playing."""
        if self.is_loaded() and self.is_playing:
            while self.channel.get_busy():
                pygame.time.delay(100)
