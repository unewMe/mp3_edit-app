from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from models.audio_io.url_downloaders import YouTubeDownloader
from views.popups.PopUpMsg import PopUpMsg

from .utils import is_valid_filename

class UrlPopUp(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle('Youtube URL Downloader')

        layout = QVBoxLayout()

        self.path_label = QLabel('Path:', self)
        self.path_input = QLineEdit(self)
        self.path_input.setReadOnly(True)

        self.setpath_button = QPushButton('Set Path', self)
        self.setpath_button.clicked.connect(self.set_path)

        self.url_label = QLabel('Youtube URL:', self)
        self.url_input = QLineEdit(self)

        self.filename_label = QLabel('Filename:', self)
        self.filename_input = QLineEdit(self)

        self.download_button = QPushButton('Download', self)
        self.download_button.clicked.connect(self.download)

        layout.addWidget(self.path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.setpath_button)
        layout.addWidget(self.url_label)
        layout.addWidget(self.url_input)
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename_input)
        layout.addWidget(self.download_button)

        self.setLayout(layout)

    def set_path(self):
        """Set the path for the downloaded file."""
        path = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if path:
            self.path_input.setText(path)

    def download(self):
        """Download the audio from the provided URL."""
        path = self.path_input.text()
        url = self.url_input.text()
        filename = self.filename_input.text()
        downloader = YouTubeDownloader()

        if path and url and filename:
            try:
                downloader.download_audio(url, path, filename)
            except Exception as e:
                PopUpMsg('Error', str(e), buttons=QMessageBox.Ok, if_exec=True)
            else:
                PopUpMsg('Success', 'Download completed!', buttons=QMessageBox.Ok, if_exec=True)
                self.close()
        elif not path or not url or not filename:
            PopUpMsg('Error', 'Please fill in all fields!', buttons=QMessageBox.Ok, if_exec=True)
        elif not is_valid_filename(filename):
            PopUpMsg('Error', 'Invalid filename!', buttons=QMessageBox.Ok, if_exec=True)
        else:
            PopUpMsg('Error', 'Error', buttons=QMessageBox.Ok, if_exec=True)
