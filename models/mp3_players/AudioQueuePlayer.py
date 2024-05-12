import pygame
from pydub import AudioSegment

import pygame
from models.audio_edit.AudioFile import AudioFile

class AudioQueuePlayer:
    sound_files: dict[str, AudioFile]  # Dictionary mapping sound_id to AudioFile
    play_order: list[str]  # List of sound_ids in the order they should be played
    final_audio: AudioFile | None  # Combined audio file to be played
    channel: pygame.mixer.Channel | None  # Channel used to play the sound file
    is_playing: bool  # Flag to check if the sound file is playing
    current_index: int  # Current index in the play_order
    paused: bool  # Flag to check if playback is paused

    def __init__(self):
        pygame.mixer.init()
        self.sound_files = {}
        self.play_order = []
        self.final_audio = None
        self.channel = None
        self.is_playing = False
        self.current_index = 0
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

    def play(self):
        """
        Play the combined audio file that includes all sounds and silences.
        """
        if not self.is_playing and self.final_audio:
            self.channel = pygame.mixer.Sound(self.final_audio.to_buffer()).play()
            self.is_playing = True

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
        if self.channel and not self.is_playing and self.paused:
            self.channel.unpause()
            self.paused = False
            self.is_playing = True

    def stop(self):
        """
        Stop all playback, clear the play queue, and reset the playback state.
        """
        if self.channel:
            self.channel.stop()
        self.final_audio = None
        self.is_playing = False
        self.paused = False
        self.current_index = 0
        self.play_order.clear()