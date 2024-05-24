from models.audio_edit.AudioFile import AudioFile
from models.mp3_players.AudioQueuePlayer import AudioQueuePlayer
from models.audio_io.io import read_audio_file
from models.mp3_players.MultiPlayer import MultiPlayer


class HomeCore:
    files: dict[str, AudioFile]
    players: dict[str, AudioQueuePlayer]
    player_id: int
    multiplayer: MultiPlayer

    def __init__(self):
        self.files = {}
        self.players = {}
        self.player_id = 1
        self.multiplayer = MultiPlayer()

    def add_file(self, file_path) -> None:
        """Adds an audio file to the file list. If the file already exists, a copy is created."""
        file_name = file_path.split("/")[-1]
        audio_file = read_audio_file(file_path)
        if file_name not in self.files:
            self.files[file_name] = audio_file
        else:
            copy = file_name.split(".")[0] + "_copy" + "." + file_name.split(".")[1]
            self.files[copy] = audio_file

    def remove_file(self, file_name) -> None:
        """Removes the selected file from the file list."""
        self.files.pop(file_name)

    def create_player(self) -> None:
        """Creates a new player and adds it to the player list."""
        player = AudioQueuePlayer()
        self.players[f"Player{self.player_id}"] = player
        self.multiplayer.add_player(f"Player{self.player_id}", player)
        self.player_id += 1

    def remove_player(self, player_name) -> None:
        """Removes the selected player from the player list."""
        self.players.pop(player_name)
        self.multiplayer.players.pop(player_name)

    def add_file_to_player(self, file_name, player_name) -> bool:
        """Adds the selected file to the selected player."""
        if file_name in self.players[player_name].sound_files:
            return False
        self.players[player_name].load(file_name, AudioFile.from_audiofile(self.files[file_name]))

        return True

    def combine_audio_files(self) -> None:
        """Combines all audio files from the selected player."""
        for player in self.players.values():
            player.combine_audio_files()

    def play_multiplayer(self) -> None:
        """Plays all the audio files from all the players."""
        self.multiplayer.play_all()

    def pause_multiplayer(self) -> None:
        """Pauses the playback of all players."""
        self.multiplayer.pause_all()

    def resume_multiplayer(self) -> None:
        """Resumes the playback of all players."""
        self.multiplayer.resume_all()

    def stop_multiplayer(self) -> None:
        """Stops the playback of all players."""
        self.multiplayer.stop_all()

    def get_max_length_in_seconds(self) -> int:
        """Returns the maximum length of all audio files."""
        return round(self.multiplayer.get_max_length() / 1000)

    def get_current_time(self) -> tuple[int, int, int]:
        """Returns the current playback time."""
        return self.multiplayer.get_time()

    def check_if_any_audio_is_loaded_into_player(self) -> bool:
        """Checks if any audio is loaded into the player."""
        return any(player.sound_files for player in self.players.values())

    def update_player_order(self, player_name, order) -> None:
        """Updates the play order of the selected player."""
        self.players[player_name].set_play_order(order)

    def remove_from_player(self, file_name, player_name):
        """Removes the selected file from the selected player."""
        self.players[player_name].remove(file_name)
