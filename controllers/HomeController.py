import sys
import os

from PySide6 import QtCore
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QFileDialog, QMessageBox

from views.HomeView import HomeView
from cores.HomeCore import HomeCore
from views.popups.PopUpMsg import PopUpMsg
from views.tools.url import UrlPopUp
from views.tools.ai import AiPopUp
from views.popups.selectors import PathSelectorPopUp

plots_type_with_values = {"Rythmic": ["Tempogram", "Beats"], "Segmentation": ["Silent segments", "Beat segments"],
                          "Base visualize": ["Waveform", "Spectrogram"]}


class HomeController():
    def __init__(self):
        super().__init__()
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

        self.view.audios_in_player_list.itemSelectionChanged.connect(self.update_audio_info)
        self.view.audio_volume_slider.valueChanged.connect(self.set_audio_volume)
        self.view.audio_delay_edit.editingFinished.connect(self.set_audio_delay)
        self.view.add_filter_butoon.clicked.connect(self.add_filter_on_audio)
        self.view.remove_all_filters_button.clicked.connect(self.remove_all_filters_on_audio)

        self.view.plots_type_combobox.currentIndexChanged.connect(self.update_plots)
        self.view.generate_plot_button.clicked.connect(self.generate_plot)

        self.view.generated_plots_list.itemSelectionChanged.connect(self.show_plot)

        bands = self.core.get_bands()
        self.view.hz62_slider.setProperty('band', bands[0])
        self.view.hz62_slider.valueChanged.connect(lambda ind: self.set_band('0', ind))
        self.view.hz125_slider.setProperty('band', bands[1])
        self.view.hz125_slider.valueChanged.connect(lambda ind: self.set_band('1', ind))
        self.view.hz250_slider.setProperty('band', bands[2])
        self.view.hz250_slider.valueChanged.connect(lambda ind: self.set_band('2', ind))
        self.view.hz500_slider.setProperty('band', bands[3])
        self.view.hz500_slider.valueChanged.connect(lambda ind: self.set_band('3', ind))
        self.view.khz1_slider.setProperty('band', bands[4])
        self.view.khz1_slider.valueChanged.connect(lambda ind: self.set_band('4', ind))
        self.view.khz2_slider.setProperty('band', bands[5])
        self.view.khz2_slider.valueChanged.connect(lambda ind: self.set_band('5', ind))
        self.view.khz4_slider.setProperty('band', bands[6])
        self.view.khz4_slider.valueChanged.connect(lambda ind: self.set_band('6', ind))
        self.view.khz8_slider.setProperty('band', bands[7])
        self.view.khz8_slider.valueChanged.connect(lambda ind: self.set_band('7', ind))
        self.view.khz16_slider.setProperty('band', bands[8])
        self.view.khz16_slider.valueChanged.connect(lambda ind: self.set_band('8', ind))

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
        file_path, _ = QFileDialog.getOpenFileName(self.view, "Open Audio File", "",
                                                   "Audio Files (*.mp3);;All Files (*)")
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

    def update_audio_info(self):
        selected_audio = self.view.audios_in_player_list.currentItem().text()
        player_name = self.view.created_players_list.currentItem().text()
        delay, volume = self.core.get_audio_delay_in_player(player_name,
                                                            selected_audio), self.core.get_volume_on_sound_in_player(
            player_name, selected_audio)
        filters_in = self.core.get_filters_from_sound(player_name, selected_audio)
        filters_out = self.core.get_rest_of_filters(filters_in)
        self.view.update_audio_info(delay=delay, volume=volume, filters_in=filters_in, filters_out=filters_out,
                                    plots=plots_type_with_values, bands=self.core.all_bands_value_from_audio(player_name, selected_audio))

    def set_audio_volume(self):
        selected_audio = self.view.audios_in_player_list.currentItem().text()
        player_name = self.view.created_players_list.currentItem().text()
        volume = self.view.audio_volume_slider.value()
        self.core.set_volume_on_sound(player_name, selected_audio, volume)

    def set_audio_delay(self):
        selected_audio = self.view.audios_in_player_list.currentItem().text()
        player_name = self.view.created_players_list.currentItem().text()
        delay = self.view.audio_delay_edit.text()
        try:
            if int(delay) < 0:
                PopUpMsg("Error", "Delay must be a positive int number.", buttons=QMessageBox.Ok, if_exec=True)
                self.view.audio_delay_edit.setText(
                    f"{self.core.get_audio_delay_in_player(player_name, selected_audio)}")
        except ValueError:
            PopUpMsg("Error", "Delay must be a positive int number.", buttons=QMessageBox.Ok, if_exec=True)
            self.view.audio_delay_edit.setText(f"{self.core.get_audio_delay_in_player(player_name, selected_audio)}")
        else:
            self.core.set_audio_delay(player_name, selected_audio, int(delay))

    def add_filter_on_audio(self):
        selected_audio = self.view.audios_in_player_list.currentItem().text()
        player_name = self.view.created_players_list.currentItem().text()
        self.core.add_filter_on_audio(player_name, selected_audio, self.view.filter_type_combobox.currentText())
        self.update_audio_info()

    def remove_all_filters_on_audio(self):
        selected_audio = self.view.audios_in_player_list.currentItem().text()
        player_name = self.view.created_players_list.currentItem().text()
        self.core.remove_all_filters_on_audio(player_name, selected_audio)
        self.update_audio_info()

    def update_plots(self):
        if any(item.isSelected() for item in self.view.audios_in_player_list.selectedItems()):
            self.view.update_plot_type(plots_type_with_values)

    def generate_plot(self):
        player_name = self.view.created_players_list.currentItem().text()
        selected_audio = self.view.audios_in_player_list.currentItem().text()
        type = self.view.plots_type_combobox.currentText()
        plots = [plot.text() for plot in self.view.plots_type_list.selectedItems()]
        path_selector = PathSelectorPopUp()
        path_selector.exec_()
        path = path_selector.directory
        if os.path.isdir(path):
            self.core.generate_plot(player_name, selected_audio, type, plots, path)
            self.view.update_plots(self.core.plots)

    def show_plot(self):
        plot_name = self.view.generated_plots_list.currentItem().text()
        self.view.show_plot(self.core.plots[plot_name])


    def set_band(self, cd, ind):
        if cd == '0':
            self.core.set_band_on_audio(self.view.created_players_list.currentItem().text(),
                                        self.view.audios_in_player_list.currentItem().text(), self.view.hz62_slider.property('band'), ind)
