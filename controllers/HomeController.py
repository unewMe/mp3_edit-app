from PySide6.QtWidgets import QFileDialog

from views.HomeView import HomeView
from cores.HomeCore import HomeCore
from views.popups.PopUpMsg import PopUpMsg

class HomeController:
    def __init__(self):
        self.view = HomeView(self)
        self.core = HomeCore()

        self.view.add_file_button.clicked.connect(self.add_file)
        self.view.remove_files_button.clicked.connect(self.remove_file)

        self.view.create_player_button.clicked.connect(self.create_player)


    def add_file(self):
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open Audio File", "", "Audio Files (*.mp3);;All Files (*)")
        if file_path:
            pop_up = PopUpMsg("Pending", "Rendering audio file, please wait...")
            pop_up.show()
            self.core.add_file(file_path)
            self.view.update_file_list(self.core.files)
            pop_up.close()


    def remove_file(self):
        file_name = self.view.read_files_list.currentItem().text()
        self.core.remove_file(file_name)
        self.view.update_file_list(self.core.files)


    def create_player(self):
        self.core.create_player()
        self.view.update_player_list(self.core.players)

    def show(self):
        self.view.show()

