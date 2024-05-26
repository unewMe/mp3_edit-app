from PySide6.QtWidgets import (QDialog, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QApplication,
                               QComboBox, QLabel, QMessageBox)
import sys

from views.popups.PopUpMsg import PopUpMsg
from views.tools.utils import is_valid_filename, _FILE_EXTENSIONS


class PathSelectorPopUp(QDialog):
    directory: str | None

    def __init__(self):
        super().__init__()
        self.initUI()
        self.directory = None

    def initUI(self):
        self.setGeometry(100, 100, 400, 100)
        self.setWindowTitle('Path Selector')

        self.line_edit = QLineEdit(self)
        self.line_edit.setReadOnly(True)

        self.select_button = QPushButton('Select Path', self)
        self.select_button.clicked.connect(self.select_path)

        self.continue_button = QPushButton('Continue', self)
        self.continue_button.clicked.connect(self.accept)
        self.continue_button.setEnabled(False)

        top_layout = QHBoxLayout()
        top_layout.addWidget(self.line_edit)
        top_layout.addWidget(self.select_button)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.continue_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(top_layout)
        main_layout.addLayout(bottom_layout)

        self.setLayout(main_layout)

    def select_path(self):
        """Select a directory and set the path to the line edit."""
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)

        if directory:
            self.line_edit.setText(directory)
            self.directory = directory
            self.continue_button.setEnabled(True)


class PathSelectorWithTypeAndFileName(QDialog):
    file_type: str | None
    file_name: str | None
    path: str | None
    is_rejected : bool = False

    def __init__(self):
        super().__init__()
        self.file_name = None
        self.file_type = None
        self.path_selector = PathSelectorPopUp()
        self.path_selector.exec()
        self.path = self.path_selector.directory
        if self.path:
            self.initUI()
        else:
            self.is_rejected = True

    def initUI(self):
        self.setGeometry(100, 100, 400, 100)

        self.file_name_label = QLabel('File Name', self)
        self.file_name_edit = QLineEdit(self)
        self.file_name_edit.textChanged.connect(self.file_name_given)

        self.file_type_label = QLabel('File Type', self)
        self.file_type_combobox = QComboBox(self)
        self.file_type_combobox.setEditable(False)
        self.file_type_combobox.addItems(_FILE_EXTENSIONS)

        self.continue_button = QPushButton('Continue', self)
        self.continue_button.clicked.connect(self.continue_apk)
        self.continue_button.setEnabled(False)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(self.continue_button)

        layout = QVBoxLayout()
        layout.addWidget(self.file_name_label)
        layout.addWidget(self.file_name_edit)
        layout.addWidget(self.file_type_label)
        layout.addWidget(self.file_type_combobox)
        layout.addLayout(bottom_layout)

        self.setLayout(layout)

    def file_name_given(self):
        """Check if the file name is given and enable the continue button."""
        if self.file_name_edit.text():
            self.continue_button.setEnabled(True)
        else:
            self.continue_button.setEnabled(False)
    def continue_apk(self):
        """Get the file name and type and close the dialog."""
        self.file_name = self.file_name_edit.text()
        self.file_type = self.file_type_combobox.currentText()

        if is_valid_filename(self.file_name):
            self.close()
        else:
            PopUpMsg('Error', 'Invalid filename!', buttons=QMessageBox.Ok, if_exec=True)


