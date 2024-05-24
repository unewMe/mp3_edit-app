import pygame
from pydub import AudioSegment

import pygame
from models.audio_edit.AudioFile import AudioFile
from models.audio_edit.filters import FilterType


class AudioQueuePlayer:
    """
    Class to play a queue of audio files in sequence.
    """

    sound_files: dict[str, AudioFile]  # Dictionary mapping sound_id to AudioFile
    play_order: list[str]  # List of sound_ids in the order they should be played
    final_audio: AudioFile | None  # Combined audio file to be played
    channel: pygame.mixer.Channel | None  # Channel used to play the sound file
    sound: pygame.mixer.Sound
    is_playing: bool  # Flag to check if the sound file is playing
    paused: bool  # Flag to check if playback is paused

    def __init__(self):
        pygame.mixer.init()
        self.sound_files = {}
        self.play_order = []
        self.final_audio = None
        self.channel = None
        self.paused = False

    def load(self, sound_id: str, audio_file: AudioFile, delay: int = 0):
        """
        Load a sound file with an optional delay.
        """
        audio_file.delay = delay
        self.sound_files[sound_id] = audio_file
        if sound_id not in self.play_order:
            self.play_order.append(sound_id)

    def combine_audio_files(self):
        """
        Combine all audio files in the play_order into one, adding silence for delays.
        """
        combined_audio = AudioSegment.silent(duration=0)
        for sound_id in self.play_order:
            audio_file = self.sound_files[sound_id]
            # Add silence before appending the next audio file
            if audio_file.delay > 0:
                silence = AudioSegment.silent(duration=audio_file.delay * 1000)  # Delay in milliseconds
                combined_audio += silence
            combined_audio += audio_file

        self.final_audio = AudioFile.from_segment(combined_audio)
        self.sound = pygame.mixer.Sound(self.final_audio.to_buffer())

    def play(self):
        """
        Play the combined audio file that includes all sounds and silences.
        """
        if not self.is_playing and self.final_audio:
            self.channel = self.sound.play()

    def pause(self):
        """
        Pause the current playback, if playing.
        """
        if self.channel and self.is_playing and not self.paused:
            self.channel.pause()
            self.paused = True

    def resume(self):
        """
        Resume the paused playback, if paused.
        """
        if self.channel and self.is_playing and self.paused:
            self.channel.unpause()
            self.paused = False

    def stop(self):
        """
        Stop all playback, clear the play queue, and reset the playback state.
        """
        if self.channel:
            self.channel.stop()
        self.paused = False

    def set_play_order(self, play_order: list[str]):
        """
        Set the order in which the sounds should be played.
        """
        self.play_order = play_order

    def apply_filter(self, sound_id: str, filter_type: FilterType):
        """
        Apply a filter to the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            self.sound_files[sound_id].apply_filter(filter_type)

    def set_volume_on_sound(self, sound_id: str, volume: float):
        """
        Set the volume of the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            self.sound_files[sound_id].set_volume(volume)

    def set_volume(self, volume: float):
        """
        Set the volume of the playback.
        """
        if self.channel:
            self.channel.set_volume(volume)

    def set_time(self, time: float):
        """
        Set the playback time in milliseconds.
        """
        if self.final_audio and self.channel:
            self.channel.stop()  # Stop current playback
            self.sound = pygame.mixer.Sound(buffer=self.final_audio[time*1000:].raw_data)
            self.channel = self.sound.play()
            self.channel.pause() if self.channel else None

    @property
    def is_playing(self) -> bool:
        return self.channel.get_busy() if self.channel else False

    def remove(self, sound_id: str):
        """
        Remove the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            self.sound_files.pop(sound_id)
            if sound_id in self.play_order:
                self.play_order.remove(sound_id)