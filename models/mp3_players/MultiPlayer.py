from pydub import AudioSegment

from models.audio_edit.AudioFile import AudioFile
from models.mp3_players.Player import Player
from models.timers.Timer import Timer


class MultiPlayer:
    """
    Class to manage multiple audio players.
    """

    players: dict[str, Player]  # Dict of Player objects
    timer: Timer | None  # Timer object to manage the playback time

    def __init__(self):
        self.players = {}
        self.timer = None

    def add_player(self, player_name: str, player: Player) -> None:
        """Adds a player to the player list."""
        self.players[player_name] = player

    def play_all(self) -> None:
        self.timer = Timer()
        for _, player in self.players.items():
            player.play()
        self.timer.start()

    def pause_all(self) -> None:
        for _, player in self.players.items():
            player.pause()
        self.timer.pause()

    def resume_all(self) -> None:
        for _, player in self.players.items():
            player.resume()
        self.timer.resume()

    def stop_all(self) -> None:
        for _, player in self.players.items():
            player.stop()
        self.timer.stop()

    def export(self, file_path: str, format="mp3") -> None:
        """Combines all audio files from all players into one and exports them to a single file."""

        combined_audio = AudioSegment.silent(duration=self.get_max_length())

        for _, player in self.players.items():
            if isinstance(player.final_audio, AudioSegment):
                combined_audio = combined_audio.overlay(player.final_audio)
            else:
                raise ValueError("player.final_audio is not an instance of AudioSegment")

        combined_audio.export(file_path, format=format)

    def get_time(self) -> tuple[int, int, int]:
        hours, minutes, seconds = self.timer.get_time()
        return round(hours), round(minutes), round(seconds)

    def get_max_length(self) -> float:
        max_length = 0
        for _, player in self.players.items():
            max_length = max(max_length, len(player.final_audio))
        return max_length

    @property
    def is_playing(self) -> bool:
        for _, player in self.players.items():
            if not player.is_playing:
                return False
        return True

    def set_time(self, time: float) -> None:
        for _, player in self.players.items():
            player.set_time(time)
        self.timer.set_time(time)
