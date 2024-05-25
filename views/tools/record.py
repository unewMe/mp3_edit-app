import sys

from PySide6.QtWidgets import QWidget, QLabel, QLineEdit, QPushButton, QVBoxLayout, QFileDialog, QMessageBox, QComboBox

from models.audio_io.AudioRecorder import AudioRecorder
from views.popups.PopUpMsg import PopUpMsg
from .validate import is_valid_filename



class RecordPopUp(QWidget):
    def __init__(self):
        super().__init__()
        self.recorder = AudioRecorder()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 300, 400)
        self.setWindowTitle('Audio Recorder')

        layout = QVBoxLayout()

        self.path_label = QLabel('Path:', self)
        self.path_input = QLineEdit(self)
        self.path_input.setReadOnly(True)
        self.setpath_button = QPushButton('Set Path', self)
        self.setpath_button.clicked.connect(self.set_path)

        self.filename_label = QLabel('Filename:', self)
        self.filename_input = QLineEdit(self)

        self.file_type_label = QLabel('File Type:', self)
        self.file_type_combobox = QComboBox(self)
        self.file_type_combobox.addItem('mp3')

        self.start_button = QPushButton('Start Recording', self)
        self.start_button.clicked.connect(self.start)

        self.stop_button = QPushButton('Stop and Save', self)
        self.stop_button.clicked.connect(self.stop)
        self.stop_button.setEnabled(False)

        layout.addWidget(self.path_label)
        layout.addWidget(self.path_input)
        layout.addWidget(self.setpath_button)
        layout.addWidget(self.filename_label)
        layout.addWidget(self.filename_input)
        layout.addWidget(self.file_type_label)
        layout.addWidget(self.file_type_combobox)
        layout.addWidget(self.start_button)
        layout.addWidget(self.stop_button)

        self.setLayout(layout)

    def set_path(self):
        path = QFileDialog.getExistingDirectory(self, 'Choose Directory')
        if path:
            self.path_input.setText(path)

    def show(self):
        super().show()
        self.recorder.reset()
        self.start_button.setEnabled(True)
        self.stop_button.setEnabled(False)
        self.file_type_combobox.setEnabled(True)
        self.filename_input.setReadOnly(False)

    def start(self):
        if is_valid_filename(self.filename_input.text()) and self.path_input.text():
            self.filename_input.setReadOnly(True)
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            self.file_type_combobox.setEnabled(False)
            self.recorder.start()
        elif not self.path_input.text():
            PopUpMsg('Error', 'Please set a path first!', buttons=QMessageBox.Ok, if_exec=True)
        else:
            PopUpMsg('Error', 'Invalid filename!', buttons=QMessageBox.Ok, if_exec=True)


    def stop(self):
        path = self.path_input.text()
        filename = self.filename_input.text()
        type = self.file_type_combobox.currentText()
        self.recorder.stop()
        self.recorder.export(path + '/' + filename + '.' + type)
        PopUpMsg('Success', 'Audio recorded and saved successfully!', buttons=QMessageBox.Ok, if_exec=True)

        self.close()
