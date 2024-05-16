from models.mp3_players.AudioQueuePlayer import AudioQueuePlayer
from models.audio_io.io import read_audio_file
import time

"""TESTING """

def player_test():
    player = AudioQueuePlayer()
    player2 = AudioQueuePlayer()
    player2.load("sound2", read_audio_file("Cypis.mp3"))
    player.load("sound1", read_audio_file("Beethoven.mp3"))
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
    single_player_test()