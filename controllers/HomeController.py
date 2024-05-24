import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFileDialog, QMessageBox

from views.HomeView import HomeView
from cores.HomeCore import HomeCore
from views.popups.PopUpMsg import PopUpMsg
from views.tools.url import UrlPopUp
from views.tools.ai import AiPopUp


class HomeController:
    def __init__(self):
        self.view = HomeView(self)
        self.core = HomeCore()
        self.pop_url = UrlPopUp()
        self.pop_ai = AiPopUp()

        self.view.add_file_button.clicked.connect(self.add_file)
        self.view.remove_files_button.clicked.connect(self.remove_file)

        self.view.create_player_button.clicked.connect(self.create_player)
        self.view.remove_player_button.clicked.connect(self.remove_player)

        self.view.created_players_list.itemSelectionChanged.connect(self.view.update_player_info)

        self.view.add_to_player_button.clicked.connect(self.add_file_to_player)
        self.view.remove_from_player_button.clicked.connect(self.remove_file_from_player)

        self.view.audios_in_player_list.itemSelectionChanged.connect(self.view.update_audio_info)

        self.view.play_button.clicked.connect(self.play_multiplayer)

        self.playback_timer = QTimer()
        self.playback_timer.setInterval(1000)
        self.playback_timer.timeout.connect(self.update_playing)

        self.view.stop_button.clicked.connect(self.stop_multiplayer)

        self.view.multiplayer_slider.sliderPressed.connect(self.music_slider_clicked)
        self.view.multiplayer_slider.sliderReleased.connect(self.music_slider_changed)

        self.view.file_action_url.triggered.connect(self.url_download)
        self.view.file_action_ai.triggered.connect(self.ai_download)

        self.view.queue_up_button.clicked.connect(self.queue_up)
        self.view.queue_down_button.clicked.connect(self.queue_down)

    def show(self) -> None:
        """Shows the home view."""
        self.view.show()

    def add_file(self) -> None:
        """Opens a file dialog to select an audio file and adds it to the file list."""
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open Audio File", "", "Audio Files (*.mp3);;All Files (*)")
        if file_path:
            # pop_up = PopUpMsg("Pending", "Rendering audio file, please wait...")
            # pop_up.show()
            self.core.add_file(file_path)
            self.view.update_file_list(self.core.files)
            # pop_up.close()


    def remove_file(self) -> None:
        """Removes the selected file from the file list."""
        file_name = self.view.read_files_list.currentItem().text()
        self.core.remove_file(file_name)
        self.view.update_file_list(self.core.files)


    def create_player(self) -> None:
        """Creates a new player and updates the player list in the view."""
        self.core.create_player()
        self.view.update_player_list(self.core.players)


    def remove_player(self) -> None:
        """Removes the selected player from the player list."""
        player_name = self.view.created_players_list.currentItem().text()
        self.core.remove_player(player_name)
        self.view.update_player_list(self.core.players)

    def add_file_to_player(self) -> None:
        """Adds the selected file to the selected player."""
        file_name = self.view.read_files_list.currentItem().text()
        player_name = self.view.created_players_list.currentItem().text()
        if self.core.add_file_to_player(file_name, player_name):
            self.view.update_player_audio_list(self.core.players[player_name].play_order)
        else:
            PopUpMsg("Error", "File already added to player.", buttons=QMessageBox.Ok, if_exec=True)

    def remove_file_from_player(self) -> None:
        """Removes the selected file from the selected player."""
        file_name = self.view.audios_in_player_list.currentItem().text()
        player_name = self.view.created_players_list.currentItem().text()
        self.core.remove_from_player(file_name, player_name)
        self.view.update_player_audio_list(self.core.players[player_name].play_order)


    def play_multiplayer(self) -> None:
        """Plays all the audio files from all the players."""
        if self.view.play_button.text() == "Pause":
            self.core.multiplayer.pause_all()
            self.view.play_button.setText("Resume")
        elif self.view.play_button.text() == "Resume":
            self.core.multiplayer.resume_all()
            self.view.play_button.setText("Pause")
        else:
            self.core.combine_audio_files()
            self.view.update_max_timer_and_slider(self.core.get_max_length_in_seconds())
            self.playback_timer.start()
            self.core.play_multiplayer()
            self.view.play_button.setText("Pause")

    def update_playing(self) -> None:
        """Updates the playback time and stops the timer if the playback is finished."""
        if self.core.multiplayer.is_playing:
            self.view.update_timer_and_slider(self.core.get_current_time())
        else:
            self.playback_timer.stop()
            self.view.play_button.setText("Play")
            self.view.update_timer_and_slider((0, 0, 0))

    def stop_multiplayer(self) -> None:
        """Stops the playback of all players."""
        self.core.stop_multiplayer()
        self.view.play_button.setText("Play")
        self.playback_timer.stop()
        self.view.update_timer_and_slider((0, 0, 0))

    def music_slider_clicked(self):
        self.playback_timer.stop()
        self.core.pause_multiplayer()

    def music_slider_changed(self):
        self.core.multiplayer.timer.set_time(self.view.multiplayer_slider.value())
        self.core.multiplayer.set_time(self.view.multiplayer_slider.value())
        self.core.multiplayer.resume_all()
        self.core.multiplayer.timer.start()
        self.playback_timer.start()
        self.view.update_timer_and_slider(self.core.get_current_time())

    def url_download(self):
        self.pop_url.show()

    def ai_download(self):
        self.pop_ai.show()

    def check_if_audio(self):
        return self.core.check_if_any_audio_is_loaded_into_player()

    def queue_changed(self):
        self.view.created_players_list.currentItem().text()
        self.core.update_player_order(self.view.created_players_list.currentItem().text(),
                                      [self.view.audios_in_player_list.item(i).text() for i in
                                       range(self.view.audios_in_player_list.count())])

    def queue_up(self):
        item1 = self.view.audios_in_player_list.currentItem().text()
        item2 = self.view.audios_in_player_list.item(self.view.audios_in_player_list.currentRow() - 1).text()
        self.view.audios_in_player_list.item(self.view.audios_in_player_list.currentRow() - 1).setText(item1)
        self.view.audios_in_player_list.currentItem().setText(item2)

        self.view.audios_in_player_list.setCurrentRow(self.view.audios_in_player_list.currentRow() - 1)

        self.queue_changed()


    def queue_down(self):
        item1 = self.view.audios_in_player_list.currentItem().text()
        item2 = self.view.audios_in_player_list.item(self.view.audios_in_player_list.currentRow() + 1).text()
        self.view.audios_in_player_list.item(self.view.audios_in_player_list.currentRow() + 1).setText(item1)
        self.view.audios_in_player_list.currentItem().setText(item2)

        self.view.audios_in_player_list.setCurrentRow(self.view.audios_in_player_list.currentRow() + 1)

        self.queue_changed()




