import pygame
from pydub import AudioSegment

import pygame
from models.audio_edit.AudioFile import AudioFile
from models.audio_edit.equalizer import Bands
from models.audio_edit.filters import FilterType
from models.mp3_players.Player import Player


class AudioQueuePlayer(Player):
    """
    Class to play a queue of audio files in sequence.
    """

    sound_files: dict[str, AudioFile]  # Dictionary mapping sound_id to AudioFile
    play_order: list[str]  # List of sound_ids in the order they should be played
    _channel: pygame.mixer.Channel | None  # Channel used to play the sound file
    _sound: pygame.mixer.Sound | None  # Sound object to play the sound file
    _is_playing: bool  # Flag to check if the sound file is playing
    _paused: bool  # Flag to check if playback is paused

    def __init__(self):
        super().__init__()
        pygame.mixer.init()
        self.sound_files = {}
        self.play_order = []
        self._channel = None
        self._paused = False
        self._sound = None

    def load(self, sound_id: str, audio_file: AudioFile, delay: int = 0) -> None:
        """
        Load a sound file with an optional delay.
        """
        while sound_id in self.sound_files:
            sound_id += "_copy"
        audio_file.delay = delay
        self.sound_files[sound_id] = audio_file
        self.play_order.append(sound_id)


    def combine_audio_files(self) -> None:
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
        self._sound = pygame.mixer.Sound(self.final_audio.to_buffer())

    def play(self) -> None:
        """
        Play the combined audio file that includes all sounds and silences.
        """
        if not self.is_playing and self.final_audio:
            self._channel = self._sound.play()

    def pause(self) -> None:
        """
        Pause the current playback, if playing.
        """
        if self._channel and self.is_playing and not self._paused:
            self._channel.pause()
            self._paused = True

    def resume(self) -> None:
        """
        Resume the paused playback, if paused.
        """
        if self._channel and self.is_playing and self._paused:
            self._channel.unpause()
            self._paused = False

    def stop(self) -> None:
        """
        Stop all playback, clear the play queue, and reset the playback state.
        """
        if self._channel:
            self._channel.stop()
        self._paused = False

    def set_play_order(self, play_order: list[str]) -> None:
        """
        Set the order in which the sounds should be played.
        """
        self.play_order = play_order

    def apply_filter(self, sound_id: str, filter_type: FilterType) -> None:
        """
        Apply a filter to the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            self.sound_files[sound_id] = self.sound_files[sound_id].apply_filter(filter_type)

    def set_volume_on_sound(self, sound_id: str, volume: float) -> None:
        """
        Set the volume of the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            self.sound_files[sound_id] = self.sound_files[sound_id].set_volume(volume)

    def set_delay_on_sound(self, sound_id: str, delay: int) -> None:
        """
        Set the delay of the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            self.sound_files[sound_id].delay = delay

    def set_volume(self, volume: float) -> None:
        """
        Set the volume of the playback.
        """
        if self._channel:
            self._channel.set_volume(volume)

    def set_time(self, time: float) -> None:
        """
        Set the playback time in milliseconds.
        """
        if self.final_audio and self._channel:
            self._channel.stop()  # Stop current playback
            self._sound = pygame.mixer.Sound(buffer=self.final_audio[time * 1000:].raw_data)
            self._channel = self._sound.play()
            self._channel.pause() if self._channel else None

    @property
    def is_playing(self) -> bool:
        return self._channel.get_busy() if self._channel else False

    def remove(self, sound_id: str) -> None:
        """
        Remove the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            self.sound_files.pop(sound_id)
            if sound_id in self.play_order:
                self.play_order.remove(sound_id)

    def get_audio_delay(self, sound_id: str) -> int:
        """
        Get the delay of the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            return self.sound_files[sound_id].delay
        return 0

    def get_audio_volume(self, sound_id: str) -> float:
        """
        Get the volume of the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            return self.sound_files[sound_id].volume
        return 0.0

    def get_filters_from_sound(self, sound_id: str) -> list[FilterType]:
        """
        Get the filters applied to the audio file corresponding to the given sound_id.
        """
        if sound_id in self.sound_files:
            return self.sound_files[sound_id].filters
        return []

    def set_band_on_audio(self, sound_id: str, band: Bands, value: float) -> None:
        """
        Set the band of the equalizer.
        """
        if sound_id in self.sound_files:
            self.sound_files[sound_id] = self.sound_files[sound_id].set_value_on_band(band, value)

    def get_all_bands_from_audio(self, sound_id: str) -> dict[Bands, float]:
        """
        Get all the bands from the equalizer.
        """
        if sound_id in self.sound_files:
            return self.sound_files[sound_id].get_all_bands()
        return {}

    def export(self, file_path: str, format: str = "mp3") -> None:
        """
        Export the combined audio file to a file.
        """
        final_audio = self.final_audio
        if not final_audio:
            self.combine_audio_files()
        self.final_audio.export(file_path, format=format)
        self.final_audio = final_audio

    def init_player(self) -> None:
        """
        Initialize the player for playback.
        """
        pygame.mixer.init()

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['_channel']
        del state['_sound']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)
        self._channel = None
        self._sound = None
        self._paused = False
        self.init_player()