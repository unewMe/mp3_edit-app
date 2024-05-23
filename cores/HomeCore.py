from models.audio_edit.AudioFile import AudioFile
from models.mp3_players.AudioQueuePlayer import AudioQueuePlayer
from models.audio_io.io import read_audio_file
class HomeCore:

    files: dict[str, AudioFile]
    players: dict[str, AudioQueuePlayer]
    player_id: int

    def __init__(self):
        self.files = {}
        self.players = {}
        self.player_id = 1

    def add_file(self, file_path) -> None:
        file_name = file_path.split("/")[-1]
        audio_file = read_audio_file(file_path)
        if file_name not in self.files:
            self.files[file_name] = audio_file
        else:
            copy = file_name.split(".")[0] + "_copy" + "." + file_name.split(".")[1]
            self.files[copy] = audio_file

    def create_player(self) -> None:
        player = AudioQueuePlayer()
        self.players[f"Player{self.player_id}"] = player
        self.player_id += 1

    def remove_file(self, file_name):
        self.files.pop(file_name)


