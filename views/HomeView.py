from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtGui import QFont, QAction
from PySide6.QtWidgets import (QComboBox, QFrame, QLabel, QLineEdit, QListView, QPushButton, QSlider, QTabWidget,
                               QWidget, QMainWindow, QListWidget, QMenuBar, QVBoxLayout, QAbstractItemView)


class HomeView(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI()
        self.showMaximized()

    def resizeEvent(self, event):
        screen_width = self.width()
        screen_height = self.height()
        self.update_geometry(screen_width, screen_height)
        super().resizeEvent(event)

    def update_geometry(self, screen_width, screen_height):
        def scale_rect(x, y, width, height):
            return QRect(int(x * screen_width / 1920), int(y * screen_height / 1080), int(width * screen_width / 1920),
                         int(height * screen_height / 1080))

        self.tab_view.setGeometry(scale_rect(10, 40, 701, 481))
        self.read_files_list.setGeometry(scale_rect(20, 60, 641, 391))
        self.add_file_button.setGeometry(scale_rect(505, 30, 75, 24))
        self.remove_files_button.setGeometry(scale_rect(586, 30, 75, 24))
        self.read_files_label.setGeometry(scale_rect(21, 32, 71, 16))

        self.create_player_button.setGeometry(scale_rect(505, 30, 75, 24))
        self.created_players_label.setGeometry(scale_rect(21, 32, 121, 21))
        self.remove_player_button.setGeometry(scale_rect(586, 30, 75, 24))
        self.created_players_list.setGeometry(scale_rect(20, 60, 641, 391))

        self.generated_plots_label.setGeometry(scale_rect(21, 32, 121, 21))
        self.remove_generated_plot_button.setGeometry(scale_rect(586, 30, 75, 24))
        self.generated_plots_list.setGeometry(scale_rect(20, 60, 641, 391))

        self.main_player_frame.setGeometry(scale_rect(720, 43, 1191, 478))
        self.play_button.setGeometry(scale_rect(620, 440, 51, 24))
        self.stop_button.setGeometry(scale_rect(560, 440, 51, 24))
        self.multiplayer_slider.setGeometry(scale_rect(20, 410, 1161, 22))
        self.main_volume_slider.setGeometry(scale_rect(1010, 440, 160, 22))
        self.main_volume_label.setGeometry(scale_rect(950, 442, 49, 16))
        self.plot_display_frame.setGeometry(scale_rect(70, 30, 1071, 361))
        self.plot_display_label.setGeometry(scale_rect(70, 30, 1071, 361))
        self.playing_time_label.setGeometry(scale_rect(20, 450, 49, 16))
        self.max_time_label.setGeometry(scale_rect(70, 450, 61, 16))

        self.player_editing_frame.setGeometry(scale_rect(10, 540, 1901, 531))
        self.editing_player_label.setGeometry(scale_rect(10, 10, 141, 21))
        self.audios_in_player_list.setGeometry(scale_rect(10, 110, 461, 391))
        self.audios_in_player_label.setGeometry(scale_rect(12, 80, 61, 21))

        self.audio_editing_frame.setGeometry(scale_rect(570, 60, 1311, 441))
        self.audio_filters_list.setGeometry(scale_rect(182, 90, 261, 261))
        self.hz62_slider.setGeometry(scale_rect(840, 140, 22, 160))
        self.hz125_slider.setGeometry(scale_rect(890, 140, 22, 160))
        self.hz250_slider.setGeometry(scale_rect(940, 140, 22, 160))
        self.hz500_slider.setGeometry(scale_rect(990, 140, 22, 160))
        self.khz1_slider.setGeometry(scale_rect(1040, 140, 22, 160))
        self.khz2_slider.setGeometry(scale_rect(1090, 140, 22, 160))
        self.khz4_slider.setGeometry(scale_rect(1140, 140, 22, 160))
        self.khz8_slider.setGeometry(scale_rect(1190, 140, 22, 160))
        self.khz16_slider.setGeometry(scale_rect(1240, 140, 22, 160))

        self.line.setGeometry(scale_rect(830, 180, 441, 16))
        self.line_2.setGeometry(scale_rect(830, 211, 441, 16))
        self.line_3.setGeometry(scale_rect(830, 242, 441, 16))
        self.line_4.setGeometry(scale_rect(830, 272, 441, 16))
        self.line_5.setGeometry(scale_rect(830, 150, 441, 16))

        self.dB12_label.setGeometry(scale_rect(775, 150, 49, 16))
        self.db6_label.setGeometry(scale_rect(775, 180, 49, 16))
        self.dB0_label.setGeometry(scale_rect(775, 210, 49, 16))
        self.dBn6_label.setGeometry(scale_rect(775, 240, 49, 16))
        self.dbn12_label.setGeometry(scale_rect(775, 270, 49, 16))

        self.audio_volume_label.setGeometry(scale_rect(60, 130, 49, 16))
        self.audio_delay_label.setGeometry(scale_rect(60, 230, 41, 16))

        self.equalizer_label.setGeometry(scale_rect(840, 90, 101, 21))
        self.audio_volume_slider.setGeometry(scale_rect(30, 160, 111, 22))
        self.audio_delay_edit.setGeometry(scale_rect(60, 250, 41, 22))
        self.audio_filters_label.setGeometry(scale_rect(182, 60, 61, 21))
        self.add_filter_butoon.setGeometry(scale_rect(370, 60, 75, 24))
        self.remove_all_filters_button.setGeometry(scale_rect(370, 30, 75, 24))

        self.audio_plots_label.setGeometry(scale_rect(502, 60, 61, 21))
        self.plots_type_list.setGeometry(scale_rect(502, 90, 261, 261))
        self.generate_plot_button.setGeometry(scale_rect(690, 60, 75, 24))
        self.plots_type_combobox.setGeometry(scale_rect(598, 60, 91, 24))

        self.cancel_audio_button.setGeometry(scale_rect(1228, 10, 75, 24))
        self.save_audio_button.setGeometry(scale_rect(1150, 10, 75, 24))

        self.add_to_player_button.setGeometry(scale_rect(318, 80, 75, 24))
        self.remove_from_player_button.setGeometry(scale_rect(397, 80, 75, 24))
        self.queue_up_button.setGeometry(scale_rect(490, 230, 51, 41))
        self.queue_down_button.setGeometry(scale_rect(490, 280, 51, 41))
        self.queue_label.setGeometry(scale_rect(498, 200, 49, 16))
        self.choose_audio_label.setGeometry(scale_rect(-10, -10, 1321, 451))
        self.choose_player_label.setGeometry(scale_rect(-160, -10, 2411, 651))

        self.filter_type_combobox.setGeometry(scale_rect(292, 60, 75, 24))

    def initUI(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("Audio editor")

        self.file_action_mb = self.menuBar().addMenu("File")
        self.file_action_url = QAction("Url Download", self)
        self.file_action_mb.addAction(self.file_action_url)

        self.file_action_ai = QAction("AI Generator", self)
        self.file_action_mb.addAction(self.file_action_ai)

        self.tab_view = QTabWidget(self)

        self.files = QWidget()
        self.files.setObjectName("files")

        self.read_files_list = QListWidget(self.files)
        self.add_file_button = QPushButton(self.files)
        self.add_file_button.setText("Add")

        self.remove_files_button = QPushButton(self.files)
        self.remove_files_button.setText("Remove")
        self.remove_files_button.setEnabled(False)

        self.read_files_label = QLabel(self.files)
        font = QFont()
        font.setPointSize(12)
        self.read_files_label.setFont(font)
        self.read_files_label.setText("Read files")

        self.tab_view.addTab(self.files, "Files")

        self.players = QWidget()

        self.create_player_button = QPushButton(self.players)
        self.create_player_button.setText("Create")

        self.created_players_label = QLabel(self.players)
        self.created_players_label.setFont(font)
        self.created_players_label.setText("Created players")

        self.remove_player_button = QPushButton(self.players)
        self.remove_player_button.setText("Remove")
        self.remove_player_button.setEnabled(False)

        self.created_players_list = QListWidget(self.players)

        self.tab_view.addTab(self.players, "Players")

        self.plots = QWidget()

        self.generated_plots_label = QLabel(self.plots)
        self.generated_plots_label.setFont(font)
        self.generated_plots_label.setText("Generated plots")

        self.remove_generated_plot_button = QPushButton(self.plots)
        self.remove_generated_plot_button.setText("Remove")
        self.remove_generated_plot_button.setEnabled(False)

        self.generated_plots_list = QListWidget(self.plots)

        self.tab_view.addTab(self.plots, "Plots")

        self.main_player_frame = QFrame(self)
        self.main_player_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_player_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.play_button = QPushButton(self.main_player_frame)
        self.play_button.setText("Play")
        self.play_button.setEnabled(False)

        self.stop_button = QPushButton(self.main_player_frame)
        self.stop_button.setText("Stop")
        self.stop_button.setEnabled(False)

        self.multiplayer_slider = QSlider(self.main_player_frame)
        self.multiplayer_slider.setOrientation(Qt.Orientation.Horizontal)

        self.main_volume_slider = QSlider(self.main_player_frame)
        self.main_volume_slider.setMaximum(100)
        self.main_volume_slider.setValue(100)
        self.main_volume_slider.setOrientation(Qt.Orientation.Horizontal)

        self.main_volume_label = QLabel(self.main_player_frame)
        self.main_volume_label.setText("Volume")

        self.plot_display_frame = QFrame(self.main_player_frame)
        self.plot_display_frame.setFrameShape(QFrame.Shape.Box)
        self.plot_display_frame.setFrameShadow(QFrame.Shadow.Sunken)

        self.plot_display_label = QLabel(self.plot_display_frame)

        self.playing_time_label = QLabel(self.main_player_frame)
        self.playing_time_label.setText("00:00:00")

        self.max_time_label = QLabel(self.main_player_frame)
        self.max_time_label.setText("00:00:00")

        self.player_editing_frame = QFrame(self)
        self.player_editing_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.player_editing_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.editing_player_label = QLabel(self.player_editing_frame)
        self.editing_player_label.setFont(font)
        self.editing_player_label.setText("Player: Not Selected")

        self.audios_in_player_list = QListWidget(self.player_editing_frame)
        self.audios_in_player_label = QLabel(self.player_editing_frame)
        self.audios_in_player_label.setFont(font)
        self.audios_in_player_label.setText("Audios")

        self.audio_editing_frame = QFrame(self.player_editing_frame)
        self.audio_editing_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.audio_editing_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.audio_filters_list = QListWidget(self.audio_editing_frame)

        self.hz62_slider = QSlider(self.audio_editing_frame)
        self.hz62_slider.setMinimum(-15)
        self.hz62_slider.setMaximum(15)
        self.hz62_slider.setValue(0)
        self.hz62_slider.setSliderPosition(0)
        self.hz62_slider.setOrientation(Qt.Orientation.Vertical)

        self.hz125_slider = QSlider(self.audio_editing_frame)
        self.hz125_slider.setMinimum(-15)
        self.hz125_slider.setMaximum(15)
        self.hz125_slider.setValue(0)
        self.hz125_slider.setOrientation(Qt.Orientation.Vertical)

        self.hz250_slider = QSlider(self.audio_editing_frame)
        self.hz250_slider.setMinimum(-15)
        self.hz250_slider.setMaximum(15)
        self.hz250_slider.setValue(0)
        self.hz250_slider.setOrientation(Qt.Orientation.Vertical)

        self.hz500_slider = QSlider(self.audio_editing_frame)
        self.hz500_slider.setMinimum(-15)
        self.hz500_slider.setMaximum(15)
        self.hz500_slider.setValue(0)
        self.hz500_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz1_slider = QSlider(self.audio_editing_frame)
        self.khz1_slider.setMinimum(-15)
        self.khz1_slider.setMaximum(15)
        self.khz1_slider.setValue(0)
        self.khz1_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz2_slider = QSlider(self.audio_editing_frame)
        self.khz2_slider.setMinimum(-15)
        self.khz2_slider.setMaximum(15)
        self.khz2_slider.setValue(0)
        self.khz2_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz4_slider = QSlider(self.audio_editing_frame)
        self.khz4_slider.setMinimum(-15)
        self.khz4_slider.setMaximum(15)
        self.khz4_slider.setValue(0)
        self.khz4_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz8_slider = QSlider(self.audio_editing_frame)
        self.khz8_slider.setMinimum(-15)
        self.khz8_slider.setMaximum(15)
        self.khz8_slider.setValue(0)
        self.khz8_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz16_slider = QSlider(self.audio_editing_frame)
        self.khz16_slider.setMinimum(-15)
        self.khz16_slider.setMaximum(15)
        self.khz16_slider.setValue(0)
        self.khz16_slider.setOrientation(Qt.Orientation.Vertical)

        self.equalizer_label = QLabel(self.audio_editing_frame)
        self.equalizer_label.setText("Equalizer")
        font = QFont()
        font.setPointSize(15)
        self.equalizer_label.setFont(font)

        self.audio_volume_label = QLabel(self.audio_editing_frame)
        self.audio_volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_volume_label.setText("Volume")

        self.audio_delay_label = QLabel(self.audio_editing_frame)
        self.audio_delay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_delay_label.setText("Delay")

        self.audio_delay_edit = QLineEdit(self.audio_editing_frame)

        self.audio_filters_label = QLabel(self.audio_editing_frame)
        self.audio_filters_label.setFont(font)
        self.audio_filters_label.setText("Filters")

        self.filter_type_combobox = QComboBox(self.audio_editing_frame)
        self.filter_type_combobox.setEditable(False)

        self.add_filter_butoon = QPushButton(self.audio_editing_frame)
        self.add_filter_butoon.setText("Add")

        self.remove_all_filters_button = QPushButton(self.audio_editing_frame)
        self.remove_all_filters_button.setText("Remove all")

        self.line = QFrame(self.audio_editing_frame)
        self.line.setEnabled(False)
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_2 = QFrame(self.audio_editing_frame)
        self.line_2.setEnabled(False)
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_3 = QFrame(self.audio_editing_frame)
        self.line_3.setEnabled(False)
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_4 = QFrame(self.audio_editing_frame)
        self.line_4.setEnabled(False)
        self.line_4.setFrameShape(QFrame.Shape.HLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.line_5 = QFrame(self.audio_editing_frame)
        self.line_5.setEnabled(False)
        self.line_5.setFrameShape(QFrame.Shape.HLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.hz62_slider.raise_()
        self.hz125_slider.raise_()
        self.hz250_slider.raise_()
        self.hz500_slider.raise_()
        self.khz1_slider.raise_()
        self.khz2_slider.raise_()
        self.khz4_slider.raise_()
        self.khz8_slider.raise_()
        self.khz16_slider.raise_()

        self.dB12_label = QLabel(self.audio_editing_frame)
        self.dB12_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.dB12_label.setText("+12 dB")

        self.db6_label = QLabel(self.audio_editing_frame)
        self.db6_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.db6_label.setText("+6 dB")

        self.dB0_label = QLabel(self.audio_editing_frame)
        self.dB0_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.dB0_label.setText("0 dB")

        self.dBn6_label = QLabel(self.audio_editing_frame)
        self.dBn6_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.dBn6_label.setText("-6 dB")

        self.dbn12_label = QLabel(self.audio_editing_frame)
        self.dbn12_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
        self.dbn12_label.setText("-12 dB")

        self.audio_plots_label = QLabel(self.audio_editing_frame)
        self.audio_plots_label.setFont(font)
        self.audio_plots_label.setText("Plots")

        self.plots_type_list = QListWidget(self.audio_editing_frame)
        self.plots_type_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self.generate_plot_button = QPushButton(self.audio_editing_frame)
        self.generate_plot_button.setText("Generate")

        self.plots_type_combobox = QComboBox(self.audio_editing_frame)
        self.plots_type_combobox.setEditable(False)
        self.plots_type_combobox.setCurrentText("Type")

        self.editing_audio_label = QLabel(self.audio_editing_frame)
        self.editing_audio_label.setFont(font)
        self.editing_audio_label.setText("Editing: Not Selected")

        self.audio_volume_slider = QSlider(self.audio_editing_frame)
        self.audio_volume_slider.setMaximum(80)
        self.audio_volume_slider.setMinimum(5)
        self.audio_volume_slider.setValue(80)
        self.audio_volume_slider.setOrientation(Qt.Orientation.Horizontal)

        self.cancel_audio_button = QPushButton(self.audio_editing_frame)
        self.cancel_audio_button.setText("Cancel")

        self.save_audio_button = QPushButton(self.audio_editing_frame)
        self.save_audio_button.setText("Save")

        self.choose_audio_label = QLabel(self.audio_editing_frame)
        self.choose_audio_label.setFont(font)
        self.choose_audio_label.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
        self.choose_audio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_audio_label.setText("Choose Audio")

        self.add_to_player_button = QPushButton(self.player_editing_frame)
        self.add_to_player_button.setText("Add")

        self.remove_from_player_button = QPushButton(self.player_editing_frame)
        self.remove_from_player_button.setText("Remove")
        self.remove_from_player_button.setEnabled(False)

        self.queue_up_button = QPushButton(self.player_editing_frame)
        self.queue_up_button.setText("Up")
        self.queue_up_button.setEnabled(False)

        self.queue_down_button = QPushButton(self.player_editing_frame)
        self.queue_down_button.setText("Down")
        self.queue_down_button.setEnabled(False)

        self.queue_label = QLabel(self.player_editing_frame)
        self.queue_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.queue_label.setText("Queue")

        self.choose_player_label = QLabel(self.player_editing_frame)
        self.choose_player_label.setEnabled(True)
        self.choose_player_label.setFont(font)
        self.choose_player_label.setStyleSheet(u"background-color: rgba(0, 0, 0, 120);")
        self.choose_player_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_player_label.setText("Choose Player")

        self.choose_audio_label.raise_()
        self.choose_player_label.raise_()

    def update_file_list(self, files):
        """Updates read files list"""
        self.read_files_list.clear()
        self.read_files_list.addItems(files)
        if self.read_files_list.count() == 0:
            self.remove_files_button.setEnabled(False)
        else:
            self.remove_files_button.setEnabled(True)

    def update_player_list(self, players):
        """Updates created players list"""
        self.created_players_list.clear()
        self.created_players_list.addItems(players)
        if self.created_players_list.count() == 0:
            self.remove_player_button.setEnabled(False)
            self.play_button.setEnabled(False)
            self.stop_button.setEnabled(False)
        else:
            self.remove_player_button.setEnabled(True)

    def update_player_info(self):
        """Updates player info"""
        if self.created_players_list.selectedItems():
            player_name = self.created_players_list.currentItem().text()
            self.editing_player_label.setText(f"Player: {player_name}")
            self.choose_player_label.hide()
            self.update_player_audio_list(self.controller.core.players[player_name].sound_files.keys())
        else:
            self.editing_player_label.setText("Player: Not Selected")
            self.choose_player_label.show()
            self.audios_in_player_list.clear()

    def update_player_audio_list(self, audios):
        """Updates player audio list"""
        self.audios_in_player_list.clear()
        self.audios_in_player_list.addItems(audios)
        if self.audios_in_player_list.count() == 0:
            self.remove_from_player_button.setEnabled(False)
            self.play_button.setEnabled(self.controller.check_if_audio())
            self.stop_button.setEnabled(self.controller.check_if_audio())
        else:
            self.remove_from_player_button.setEnabled(True)
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)

    def update_audio_info(self, volume, delay, filters_in, filters_out, plots, bands):
        """Updates audio info"""
        if self.audios_in_player_list.selectedItems():
            audio_name = self.audios_in_player_list.currentItem().text()
            self.editing_audio_label.setText(f"Editing: {audio_name}")

            self.audio_delay_edit.setText(str(delay))
            self.audio_volume_slider.setValue(volume)

            self.filter_type_combobox.clear()
            self.filter_type_combobox.addItems(filters_out)
            self.audio_filters_list.clear()
            self.audio_filters_list.addItems(filters_in)

            self.plots_type_combobox.clear()
            self.plots_type_combobox.addItems(plots.keys())
            self.update_plot_type(plots)

            self.hz62_slider.setValue(bands[self.hz62_slider.property('band')])
            self.hz125_slider.setValue(bands[self.hz125_slider.property('band')])
            self.hz250_slider.setValue(bands[self.hz250_slider.property('band')])
            self.hz500_slider.setValue(bands[self.hz500_slider.property('band')])
            self.khz1_slider.setValue(bands[self.khz1_slider.property('band')])
            self.khz2_slider.setValue(bands[self.khz2_slider.property('band')])
            self.khz4_slider.setValue(bands[self.khz4_slider.property('band')])
            self.khz8_slider.setValue(bands[self.khz8_slider.property('band')])
            self.khz16_slider.setValue(bands[self.khz16_slider.property('band')])


            row = self.audios_in_player_list.row(self.audios_in_player_list.currentItem())

            if row > 0:
                self.queue_up_button.setEnabled(True)
            else:
                self.queue_up_button.setEnabled(False)

            if row < self.audios_in_player_list.count() - 1:
                self.queue_down_button.setEnabled(True)
            else:
                self.queue_down_button.setEnabled(False)

            self.choose_audio_label.hide()
        else:
            self.editing_audio_label.setText("Editing: Not Selected")
            self.choose_audio_label.show()
            self.queue_up_button.setEnabled(False)
            self.queue_down_button.setEnabled(False)
            self.audio_delay_edit.setText("")
            self.audio_volume_slider.setValue(80)
            self.filter_type_combobox.clear()
            self.audio_filters_list.clear()
            self.plots_type_combobox.clear()
            self.plots_type_list.clear()

    def update_max_timer_and_slider(self, seconds: int):
        """Updates max timer and slider"""
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        self.max_time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.multiplayer_slider.setMaximum(hours * 3600 + minutes * 60 + seconds)

    def update_timer_and_slider(self, hour_minut_second: tuple[int, int, int]):
        """Updates timer and slider"""
        self.playing_time_label.setText(
            f"{hour_minut_second[0]:02}:{hour_minut_second[1]:02}:{hour_minut_second[2]:02}")
        self.multiplayer_slider.setValue(hour_minut_second[0] * 3600 + hour_minut_second[1] * 60 + hour_minut_second[2])

    def update_plot_type(self, plots):
        """Updates plot type"""
        self.plots_type_list.clear()
        if self.plots_type_combobox.currentText():
            self.plots_type_list.addItems(plots[self.plots_type_combobox.currentText()])

    def update_plots(self, plot):
        """Updates plot"""
        self.generated_plots_list.clear()
        self.generated_plots_list.addItems(plot.keys())

    def show_plot(self, plot):
        self.plot_display_label.setPixmap(
            plot.scaled(self.plot_display_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
