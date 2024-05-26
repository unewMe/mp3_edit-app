import sys
from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox
from models.audio_io.url_downloaders import YouTubeDownloader
from views.popups.PopUpMsg import PopUpMsg
from models.audio_io.ai_generators import LeapMusicGenerator
from .utils import is_valid_filename

class AiPopUp(QWidget):
    def __init__(self):
        super().__init__()
        self.api_key = None
        self.leap = LeapMusicGenerator()

        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 500)
        self.setWindowTitle('AI Generator powered by Leap Music')

        layout = QVBoxLayout()

        self.api_key_label = QLabel('Your API KEY:', self)
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setPlaceholderText('Enter your API KEY') if not self.api_key else self.api_key_input.setText(self.api_key)

        self.path_label = QLabel('Path:', self)
        self.path_input = QLineEdit(self)
        self.path_input.setReadOnly(True)

        self.setpath_button = QPushButton('Set Path', self)
        self.setpath_button.clicked.connect(self.set_path)

        self.prompt_label = QLabel('Propmpt:', self)
        self.prompt_input = QLineEdit(self)

        self.melody_label = QLabel('Melody:', self)
        self.melody_input = QLineEdit(self)

        self.duration_label = QLabel('Duration:', self)
        self.duration_input = QLineEdit(self)

        self.filename_label = QLabel('Filename:', self)
        self.filename_input = QLineEdit(self)

        self.generate_button = QPushButton('Generate', self)
        self.generate_button.clicked.connect(self.generate)

        layout.addWidget(self.api_key_label)
        layout.addWidget(self.api_key_input)
        layout.addWidget(self.path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.setpath_button)
        layout.addWidget(self.prompt_label)
        layout.addWidget(self.prompt_input)
        layout.addWidget(self.melody_label)
        layout.addWidget(self.melody_input)
        layout.addWidget(self.duration_label)
        layout.addWidget(self.duration_input)
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename_input)
        layout.addWidget(self.generate_button)

        self.setLayout(layout)

    def set_path(self):
        """Set the path for the generated file."""
        path = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if path:
            self.path_input.setText(path)


    def generate(self):
        """Generate the audio file."""
        path = self.path_input.text()
        prompt = self.prompt_input.text()
        melody = self.melody_input.text()
        duration = self.duration_input.text()
        filename = self.filename_input.text()
        self.leap.set_api_key(self.api_key)

        if path and prompt and melody and duration and filename:
            try:
                self.leap.generate(prompt, melody, int(duration), path,filename)
            except ValueError as e:
                PopUpMsg('Error', str(e), buttons=QMessageBox.Ok, if_exec=True)
            else:
                PopUpMsg('Success', 'Download completed!', buttons=QMessageBox.Ok, if_exec=True)
                self.close()
        elif not path or not prompt or not melody or not duration or not filename:
            PopUpMsg('Error', 'Please fill in all fields!', buttons=QMessageBox.Ok, if_exec=True)
        elif not is_valid_filename(filename):
            PopUpMsg('Error', 'Invalid filename!', buttons=QMessageBox.Ok, if_exec=True)
        else:
            PopUpMsg('Error', 'Error', buttons=QMessageBox.Ok, if_exec=True)

