from PySide6.QtWidgets import QMainWindow, QWidget, QTabWidget, QVBoxLayout, QHBoxLayout, QPushButton, QListWidget
from PySide6.QtCore import Qt

class HomeView(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowState(Qt.WindowMaximized)
        self.setWindowTitle('Music editor')

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout(self.central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        top_layout = QHBoxLayout()
        top_layout.setContentsMargins(0, 0, 0, 0)

        self.tabs = QTabWidget()
        self.files_tab = QWidget()
        self.players_tab = QWidget()

        self.tabs.addTab(self.files_tab, "Files")
        self.tabs.addTab(self.players_tab, "Players")

        top_layout.addWidget(self.tabs)
        top_layout.addStretch()

        main_layout.addLayout(top_layout)
        main_layout.addStretch(1)

        self.tabs.setFixedSize(800, 600)

        files_layout = QVBoxLayout(self.files_tab)
        files_buttons_layout = QHBoxLayout()

        add_button = QPushButton("Add")
        delete_button = QPushButton("Remove")
        add_button.setFixedSize(80, 25)
        delete_button.setFixedSize(80, 25)
        files_buttons_layout.addWidget(add_button)
        files_buttons_layout.addWidget(delete_button)
        files_buttons_layout.addStretch(1)


        files_layout.addLayout(files_buttons_layout)

        self.files_list = QListWidget()
        self.files_list.setFixedSize(780, 540)
        files_layout.addWidget(self.files_list)
