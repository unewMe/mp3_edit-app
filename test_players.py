from models.mp3_players.AudioQueuePlayer import AudioQueuePlayer
from models.mp3_players.MultiPlayer import MultiPlayer
from models.audio_io.io import read_audio_file
import time

"""TESTING """

def player_test():
    player = AudioQueuePlayer()
    player2 = AudioQueuePlayer()
    player2.load("sound2", read_audio_file("Cypis.mp3"))
    player.load("sound1", read_audio_file("Beethoven.mp3"))
    player.combine_audio_files()
    player2.combine_audio_files()
    player.play()
    player2.play()
    time.sleep(15)
    player.pause()
    player2.pause()
    time.sleep(5)
    player.resume()
    player2.resume()
    time.sleep(50)
    player.stop()
    player2.stop()


def multi_player_test():
    player = AudioQueuePlayer()
    player2 = AudioQueuePlayer()
    player3 = AudioQueuePlayer()
    player2.load("sound2", read_audio_file("Cypis.mp3"))
    player.load("sound1", read_audio_file("Beethoven.mp3"))
    player3.load("sound3", read_audio_file("10.mp3"))
    player.combine_audio_files()
    player2.combine_audio_files()
    player3.combine_audio_files()
    multi_player = MultiPlayer({"player1": player, "player2": player2, "player3": player3})
    # multi_player.play_all()
    # time.sleep(15)
    # multi_player.pause_all()
    # time.sleep(5)
    # multi_player.resume_all()
    # time.sleep(5)
    # multi_player.stop_all()

    multi_player.export("output2.mp3")

def single_player_test():
    player = AudioQueuePlayer()
    x = read_audio_file("10.mp3")
    from models.audio_edit.filters import LowPassFilter,HighPassFilter
    filter_ = HighPassFilter(x)
    x = filter_.apply()
    player.load("sound1", x)
    player.combine_audio_files()
    player.play()
    time.sleep(50)

if __name__ == "__main__":
    multi_player_test()