from models.audio_edit.AudioFile import AudioFile
import abc


class Player(metaclass=abc.ABCMeta):
    final_audio: AudioFile | None  # Final audio file to be played

    def __init__(self):
        self.final_audio = None

    @abc.abstractmethod
    def load(self, sound_id: str, audio_file: AudioFile, delay: int = 0) -> None:
        """
        Load a sound file from the given file path.
        """
        pass

    @abc.abstractmethod
    def play(self) -> None:
        """
        Play the loaded sound file.
        """
        pass

    @abc.abstractmethod
    def pause(self) -> None:
        """
        Pause the sound file.
        """
        pass

    @abc.abstractmethod
    def resume(self) -> None:
        """
        Resume the sound file.
        """
        pass

    @abc.abstractmethod
    def stop(self) -> None:
        """
        Stop the sound file.
        """
        pass

    @abc.abstractmethod
    def set_volume(self, volume: float) -> None:
        """
        Set the volume of the sound file.
        """
        pass

    @abc.abstractmethod
    def set_time(self, time: float) -> None:
        """
        Return the current time of the sound file.
        """
        pass

    @abc.abstractmethod
    def is_playing(self) -> bool:
        """
        Return True if the sound file is playing, False otherwise.
        """
        pass
