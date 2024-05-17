from models.audio_io.AudioRecorder import AudioRecorder
import time
from models.mp3_players.AudioQueuePlayer import AudioQueuePlayer
from models.audio_edit.AudioFile import AudioFile
def test_audio_recorder():
    recorder = AudioRecorder()
    recorder.start()
    time.sleep(5)
    recorder.stop()
    audio_segment = recorder.convert_to_audiosegment()

    audio_segment.export("test.mp3", format="mp3")

    player = AudioQueuePlayer()
    player.load("sound1", AudioFile.from_segment(audio_segment))
    player.combine_audio_files()
    player.play()
    time.sleep(15)

if __name__ == "__main__":
    test_audio_recorder()