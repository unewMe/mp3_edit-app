import sys
from PySide6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLabel, QFileDialog
from PySide6.QtCore import QTimer
from models.mp3_players.AudioQueuePlayer import AudioQueuePlayer
from models.audio_io.io import read_audio_file


"""TESTING THE GUI"""

class MusicPlayerGUI(QWidget):
    def __init__(self):
        super().__init__()

        self.player = AudioQueuePlayer()
        self.init_ui()
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer)

    def init_ui(self):
        self.setWindowTitle("Music Player")
        self.layout = QVBoxLayout(self)

        self.time_label = QLabel("00:00:00", self)
        self.layout.addWidget(self.time_label)

        self.load_button = QPushButton("Load Music", self)
        self.load_button.clicked.connect(self.load_music)
        self.layout.addWidget(self.load_button)

        self.start_button = QPushButton("Start", self)
        self.start_button.clicked.connect(self.start_playback)
        self.layout.addWidget(self.start_button)

        self.pause_button = QPushButton("Pause", self)
        self.pause_button.clicked.connect(self.pause_playback)
        self.layout.addWidget(self.pause_button)

        self.resume_button = QPushButton("Resume", self)
        self.resume_button.clicked.connect(self.resume_playback)
        self.layout.addWidget(self.resume_button)

        self.stop_button = QPushButton("Stop", self)
        self.stop_button.clicked.connect(self.stop_playback)
        self.layout.addWidget(self.stop_button)

    def load_music(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Music File", "", "MP3 Files (*.mp3)")
        if file_path:
            self.player.load(read_audio_file(file_path))

    def start_playback(self):
        self.player.play()
        self.timer.start(1000)

    def pause_playback(self):
        self.player.pause()
        self.timer.stop()

    def resume_playback(self):
        self.player.resume()
        self.timer.start()

    def stop_playback(self):
        self.player.stop()
        self.timer.stop()
        self.time_label.setText("00:00:00")

    def update_timer(self):
        current_time = self.player.get_current_time()
        hours, minutes, seconds = current_time
        self.time_label.setText(f"{round(hours):02}:{round(minutes):02}:{round(seconds):02}")


def main():
    app = QApplication(sys.argv)
    gui = MusicPlayerGUI()
    gui.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
