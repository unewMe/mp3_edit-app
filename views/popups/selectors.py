from PySide6.QtWidgets import (QDialog, QLineEdit, QPushButton, QFileDialog, QHBoxLayout, QVBoxLayout, QApplication)
import sys


class PathSelectorPopUp(QDialog):

    directory : str | None

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
        options = QFileDialog.Options()
        directory = QFileDialog.getExistingDirectory(self, "Select Directory", options=options)

        if directory:
            self.line_edit.setText(directory)
            self.directory = directory


