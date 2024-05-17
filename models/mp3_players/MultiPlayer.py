from models.mp3_players.Player import Player

class MultiPlayer:
    """
    Class to manage multiple audio players.
    """

    players: list[Player] # List of Player objects

    def __init__(self, players_num=3):
        self.players = [Player() for _ in range(players_num)]

    def load_in_player(self, player_index, sound_id, file_path):
        if 0 <= player_index < len(self.players):
            self.players[player_index].load(sound_id, file_path)

    def add_to_player_schedule(self, player_index, sound_id, delay):
        if 0 <= player_index < len(self.players):
            self.players[player_index].add_to_schedule(sound_id, delay)

    def play_all(self):
        for player in self.players:
            player.play()

    def pause_all(self):
        for player in self.players:
            player.pause()

    def resume_all(self):
        for player in self.players:
            player.resume()

    def stop_all(self):
        for player in self.players:
            player.stop()
