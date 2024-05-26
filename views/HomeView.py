from PySide6.QtCore import QRect, Qt
from PySide6.QtGui import QFont, QAction, QPixmap, QResizeEvent
from PySide6.QtWidgets import (QComboBox, QFrame, QLabel, QLineEdit, QPushButton, QSlider, QTabWidget,
                               QWidget, QMainWindow, QListWidget, QAbstractItemView)

from models.audio_edit.equalizer import Bands

_NUMBER_OF_LINES = 5
_DB_LABELS = ["+12 dB", "+6 dB", "0 dB", "-6 dB", "-12 dB"]


class HomeView(QMainWindow):

    tab_view: QTabWidget
    files: QWidget
    read_files_label: QLabel
    read_files_list: QListWidget
    add_file_button: QPushButton
    remove_files_button: QPushButton
    players: QWidget
    create_player_button: QPushButton
    created_players_label: QLabel
    remove_player_button: QPushButton
    created_players_list: QListWidget
    plots: QWidget
    generated_plots_label: QLabel
    remove_generated_plot_button: QPushButton
    generated_plots_list: QListWidget
    main_player_frame: QFrame
    play_button: QPushButton
    stop_button: QPushButton
    multiplayer_slider: QSlider
    main_volume_slider: QSlider
    main_volume_label: QLabel
    plot_display_frame: QFrame
    plot_display_label: QLabel
    playing_time_label: QLabel
    max_time_label: QLabel
    player_editing_frame: QFrame
    editing_player_label: QLabel
    audios_in_player_list: QListWidget
    audios_in_player_label: QLabel
    add_to_player_button: QPushButton
    remove_from_player_button: QPushButton
    queue_up_button: QPushButton
    queue_down_button: QPushButton
    queue_label: QLabel
    choose_audio_label: QLabel
    choose_player_label: QLabel
    audio_editing_frame: QFrame
    choose_audio_label: QLabel
    editing_audio_label: QLabel
    audio_volume_label: QLabel
    audio_delay_label: QLabel
    audio_volume_slider: QSlider
    audio_delay_edit: QLineEdit
    audio_filters_list: QListWidget
    audio_filters_label: QLabel
    filter_type_combobox: QComboBox
    add_filter_butoon: QPushButton
    remove_all_filters_button: QPushButton
    audio_plots_label: QLabel
    plots_type_list: QListWidget
    generate_plot_button: QPushButton
    plots_type_combobox: QComboBox
    equalizer_label: QLabel
    equalizer_sliders: dict[Bands, QSlider]
    equalizer_lines: list[QFrame]
    equalizer_db_labels: list[QLabel]
    equalizer_hz_labels: list[QLabel]

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.equalizer_sliders = {}
        self.equalizer_lines = []
        self.equalizer_db_labels = []
        self.equalizer_hz_labels = []
        self.initUI()
        self.showMaximized()

    def resizeEvent(self, event: QResizeEvent) -> None:
        """Resizes widgets when window is resized"""
        screen_width = self.width()
        screen_height = self.height()
        self.update_geometry(screen_width, screen_height)
        super().resizeEvent(event)

    def update_geometry(self, screen_width: int, screen_height: int):
        """Updates geometry of widgets"""
        def scale_rect(x, y, width, height):
            return QRect(int(x * screen_width / 1920), int(y * screen_height / 1080), int(width * screen_width / 1920),
                         int(height * screen_height / 1080))

        # Gemoetry for tab view - files, players, plots

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

        # Geometry for main player frame

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

        # Geometry for player editing frame

        self.player_editing_frame.setGeometry(scale_rect(10, 540, 1901, 531))
        self.editing_player_label.setGeometry(scale_rect(10, 10, 141, 21))
        self.audios_in_player_list.setGeometry(scale_rect(10, 110, 461, 391))
        self.audios_in_player_label.setGeometry(scale_rect(12, 80, 61, 21))

        # Geometry for player editing frame - queue and chosen audio, player
        self.add_to_player_button.setGeometry(scale_rect(318, 80, 75, 24))
        self.remove_from_player_button.setGeometry(scale_rect(397, 80, 75, 24))
        self.queue_up_button.setGeometry(scale_rect(490, 230, 51, 41))
        self.queue_down_button.setGeometry(scale_rect(490, 280, 51, 41))
        self.queue_label.setGeometry(scale_rect(498, 200, 49, 16))
        self.choose_audio_label.setGeometry(scale_rect(-10, -10, 1321, 451))
        self.choose_player_label.setGeometry(scale_rect(-160, -10, 2411, 651))

        # Geometry for audio editing frame

        self.audio_editing_frame.setGeometry(scale_rect(570, 60, 1311, 441))
        self.editing_audio_label.setGeometry(scale_rect(20, 10, 250, 30))
        self.audio_filters_list.setGeometry(scale_rect(182, 90, 261, 261))

        # Geometry for audio editing frame - equalizer

        self.equalizer_label.setGeometry(scale_rect(840, 90, 101, 25))

        temp = 0
        for slider in self.equalizer_sliders.values():
            slider.setGeometry(scale_rect(840 + temp, 138, 22, 160))
            temp += 50

        for i, line in enumerate(self.equalizer_lines):
            line.setGeometry(scale_rect(830, 149 + i * 30, 441, 16))

        for i, label in enumerate(self.equalizer_db_labels):
            label.setGeometry(scale_rect(775, 150 + i * 30, 49, 16))

        for i, label in enumerate(self.equalizer_hz_labels):
            label.setGeometry(scale_rect(825 + i * 50, 300, 50, 16))

        # Geometry for audio editing frame - volume, delay
        self.audio_volume_label.setGeometry(scale_rect(60, 130, 49, 16))
        self.audio_volume_min_label.setGeometry(scale_rect(-5, 162, 41, 16))
        self.audio_volume_max_label.setGeometry(scale_rect(140, 162, 41, 16))
        self.audio_delay_label.setGeometry(scale_rect(60, 230, 41, 16))
        self.audio_volume_slider.setGeometry(scale_rect(30, 160, 111, 22))
        self.audio_delay_edit.setGeometry(scale_rect(60, 250, 41, 22))

        # Geometry for audio editing frame - filters
        self.filter_type_combobox.setGeometry(scale_rect(292, 60, 75, 24))
        self.audio_filters_label.setGeometry(scale_rect(182, 60, 61, 21))
        self.add_filter_butoon.setGeometry(scale_rect(370, 60, 75, 24))
        self.remove_all_filters_button.setGeometry(scale_rect(370, 30, 75, 24))

        # Geometry for audio editing frame - plots
        self.audio_plots_label.setGeometry(scale_rect(502, 60, 61, 21))
        self.plots_type_list.setGeometry(scale_rect(502, 90, 261, 261))
        self.generate_plot_button.setGeometry(scale_rect(690, 60, 75, 24))
        self.plots_type_combobox.setGeometry(scale_rect(598, 60, 91, 24))

    def initUI(self):
        self.setObjectName("MainWindow")
        self.setWindowTitle("Audio editor")

        # Menu bar

        # Menu bar - File

        self.file_action_mb = self.menuBar().addMenu("File")

        self.file_action_save = QAction("Save", self)
        self.file_action_mb.addAction(self.file_action_save)

        self.file_action_open_recent = QAction("Open Recent", self)
        self.file_action_mb.addAction(self.file_action_open_recent)

        self.file_action_export = QAction("Export", self)
        self.file_action_mb.addAction(self.file_action_export)

        # Menu bar - Tools

        self.tools_action_mb = self.menuBar().addMenu("Tools")
        self.tools_action_url = QAction("Url Download", self)
        self.tools_action_mb.addAction(self.tools_action_url)

        self.tools_action_ai = QAction("AI Generator", self)
        self.tools_action_mb.addAction(self.tools_action_ai)

        self.tools_action_recorder = QAction("Recorder", self)
        self.tools_action_mb.addAction(self.tools_action_recorder)

        # Tab view

        self.tab_view = QTabWidget(self)

        # Tab view - files

        self.files = QWidget()
        self.files.setObjectName("files")

        self.read_files_label = QLabel(self.files)
        font = QFont()
        font.setPointSize(12)
        self.read_files_label.setFont(font)
        self.read_files_label.setText("Read files")

        self.read_files_list = QListWidget(self.files)
        self.add_file_button = QPushButton(self.files)
        self.add_file_button.setText("Add")

        self.remove_files_button = QPushButton(self.files)
        self.remove_files_button.setText("Remove")
        self.remove_files_button.setEnabled(False)

        self.tab_view.addTab(self.files, "Files")

        # Tab view - players

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

        # Tab view - plots

        self.plots = QWidget()

        self.generated_plots_label = QLabel(self.plots)
        self.generated_plots_label.setFont(font)
        self.generated_plots_label.setText("Generated plots")

        self.remove_generated_plot_button = QPushButton(self.plots)
        self.remove_generated_plot_button.setText("Remove")
        self.remove_generated_plot_button.setEnabled(False)

        self.generated_plots_list = QListWidget(self.plots)

        self.tab_view.addTab(self.plots, "Plots")

        # Main player frame

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

        # Player editing frame

        self.player_editing_frame = QFrame(self)
        self.player_editing_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.player_editing_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.choose_player_label = QLabel(self.player_editing_frame)
        self.choose_player_label.setEnabled(True)
        self.choose_player_label.setFont(font)
        self.choose_player_label.setStyleSheet(u"background-color: rgba(0, 0, 0, 120);")
        self.choose_player_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_player_label.setText("Choose Player")

        self.editing_player_label = QLabel(self.player_editing_frame)
        self.editing_player_label.setFont(font)
        self.editing_player_label.setText("Player: Not Selected")

        self.audios_in_player_list = QListWidget(self.player_editing_frame)
        self.audios_in_player_label = QLabel(self.player_editing_frame)
        self.audios_in_player_label.setFont(font)
        self.audios_in_player_label.setText("Audios")

        # Player editing frame - add to player, remove from player

        self.add_to_player_button = QPushButton(self.player_editing_frame)
        self.add_to_player_button.setText("Add")
        self.add_to_player_button.setEnabled(False)

        self.remove_from_player_button = QPushButton(self.player_editing_frame)
        self.remove_from_player_button.setText("Remove")
        self.remove_from_player_button.setEnabled(False)

        # Player editing frame - queue

        self.queue_up_button = QPushButton(self.player_editing_frame)
        self.queue_up_button.setText("Up")
        self.queue_up_button.setEnabled(False)

        self.queue_down_button = QPushButton(self.player_editing_frame)
        self.queue_down_button.setText("Down")
        self.queue_down_button.setEnabled(False)

        self.queue_label = QLabel(self.player_editing_frame)
        self.queue_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.queue_label.setText("Queue")

        # Audio editing frame

        self.audio_editing_frame = QFrame(self.player_editing_frame)
        self.audio_editing_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.audio_editing_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.choose_audio_label = QLabel(self.audio_editing_frame)
        self.choose_audio_label.setFont(font)
        self.choose_audio_label.setStyleSheet("background-color: rgba(0, 0, 0, 120);")
        self.choose_audio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_audio_label.setText("Choose Audio")

        self.editing_audio_label = QLabel(self.audio_editing_frame)
        self.editing_audio_label.setFont(font)
        self.editing_audio_label.setText("Editing: Not Selected")

        # Audio editing frame - volume, delay

        self.audio_volume_label = QLabel(self.audio_editing_frame)
        self.audio_volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_volume_label.setText("Volume")

        self.audio_volume_min_label = QLabel(self.audio_editing_frame)
        self.audio_volume_min_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_volume_min_label.setText("5%")

        self.audio_volume_max_label = QLabel(self.audio_editing_frame)
        self.audio_volume_max_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_volume_max_label.setText("100%")

        self.audio_volume_slider = QSlider(self.audio_editing_frame)
        self.audio_volume_slider.setMaximum(60)
        self.audio_volume_slider.setMinimum(5)
        self.audio_volume_slider.setValue(60)
        self.audio_volume_slider.setOrientation(Qt.Orientation.Horizontal)

        self.audio_delay_label = QLabel(self.audio_editing_frame)
        self.audio_delay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.audio_delay_label.setText("Delay")

        self.audio_delay_edit = QLineEdit(self.audio_editing_frame)

        # Audio editing frame - filters

        self.audio_filters_list = QListWidget(self.audio_editing_frame)

        self.audio_filters_label = QLabel(self.audio_editing_frame)
        self.audio_filters_label.setFont(font)
        self.audio_filters_label.setText("Filters")

        self.filter_type_combobox = QComboBox(self.audio_editing_frame)
        self.filter_type_combobox.setEditable(False)

        self.add_filter_butoon = QPushButton(self.audio_editing_frame)
        self.add_filter_butoon.setText("Add")

        self.remove_all_filters_button = QPushButton(self.audio_editing_frame)
        self.remove_all_filters_button.setText("Remove all")
        self.remove_all_filters_button.setEnabled(False)

        # Audio editing frame - plots

        self.audio_plots_label = QLabel(self.audio_editing_frame)
        self.audio_plots_label.setFont(font)
        self.audio_plots_label.setText("Plots")

        self.plots_type_list = QListWidget(self.audio_editing_frame)
        self.plots_type_list.setSelectionMode(QAbstractItemView.MultiSelection)

        self.generate_plot_button = QPushButton(self.audio_editing_frame)
        self.generate_plot_button.setText("Generate")
        self.generate_plot_button.setEnabled(False)

        self.plots_type_combobox = QComboBox(self.audio_editing_frame)
        self.plots_type_combobox.setEditable(False)
        self.plots_type_combobox.setCurrentText("Type")

        # Audio editing frame - equalizer

        self.equalizer_label = QLabel(self.audio_editing_frame)
        self.equalizer_label.setText("Equalizer")
        font = QFont()
        font.setPointSize(15)
        self.equalizer_label.setFont(font)

        for band in Bands:
            slider = QSlider(self.audio_editing_frame)
            slider.setMaximum(15)
            slider.setMinimum(-15)
            slider.setValue(0)
            slider.setOrientation(Qt.Orientation.Vertical)
            self.equalizer_sliders[band] = slider

        for i in range(_NUMBER_OF_LINES):
            line = QFrame(self.audio_editing_frame)
            line.setEnabled(False)
            line.setFrameShape(QFrame.Shape.HLine)
            line.setFrameShadow(QFrame.Shadow.Sunken)
            self.equalizer_lines.append(line)

        for slider in self.equalizer_sliders.values():
            slider.raise_()

        for i in _DB_LABELS:
            label = QLabel(self.audio_editing_frame)
            label.setAlignment(
                Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)
            label.setText(i)
            self.equalizer_db_labels.append(label)

        for i in self.equalizer_sliders:
            label = QLabel(self.audio_editing_frame)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setText(f"{i.name}")
            self.equalizer_hz_labels.append(label)

        # Raise blocking widgets

        self.choose_audio_label.raise_()
        self.choose_audio_label.hide()
        self.choose_player_label.raise_()

    def update_file_list(self, files) -> None:
        """Updates read files list"""
        self.read_files_list.clear()
        self.read_files_list.addItems(files)

    def update_player_list(self, players) -> None:
        """Updates created players list"""
        self.created_players_list.clear()
        self.created_players_list.addItems(players)
        if self.created_players_list.count() == 0:
            self.remove_player_button.setEnabled(False)
            self.play_button.setEnabled(False)
            self.stop_button.setEnabled(False)

    def update_player_info(self) -> None:
        """Updates player info"""
        if self.created_players_list.selectedItems():
            player_name = self.created_players_list.currentItem().text()
            self.editing_player_label.setText(f"Player: {player_name}")
            self.choose_player_label.hide()
            self.choose_audio_label.show()
            self.update_player_audio_list(self.controller.core.players[player_name].sound_files.keys())
            self.remove_player_button.setEnabled(True)
        else:
            self.editing_player_label.setText("Player: Not Selected")
            self.choose_audio_label.hide()
            self.choose_player_label.show()
            self.audios_in_player_list.clear()
            self.remove_player_button.setEnabled(False)

    def update_player_audio_list(self, audios: list[str]) -> None:
        """Updates player audio list"""
        self.audios_in_player_list.clear()
        self.audios_in_player_list.addItems(audios)
        if self.audios_in_player_list.count() == 0:
            self.remove_from_player_button.setEnabled(False)
            self.play_button.setEnabled(self.controller.check_if_audio() or self.play_button.text() != "Play")
            self.stop_button.setEnabled(self.controller.check_if_audio() or self.play_button.text() != "Play")
        else:
            self.remove_from_player_button.setEnabled(True)
            self.play_button.setEnabled(True)
            self.stop_button.setEnabled(True)



    def update_audio_info(self, volume: int, delay: int, filters_in: list[str], filters_out: list[str],
                          plots: dict[str, list[str]], bands: dict[Bands, int]) -> None:
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
            self.remove_all_filters_button.setEnabled(bool(filters_in))
            self.add_filter_butoon.setEnabled(bool(filters_out))

            self.plots_type_combobox.clear()
            self.plots_type_combobox.addItems(list(plots.keys()))
            self.update_plot_type(plots)

            for band, value in bands.items():
                self.equalizer_sliders[band].setValue(value)

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
            self.audio_volume_slider.setValue(60)
            self.filter_type_combobox.clear()
            self.audio_filters_list.clear()
            self.plots_type_combobox.clear()
            self.plots_type_list.clear()
            for slider in self.equalizer_sliders.values():
                slider.setValue(0)

    def update_max_timer_and_slider(self, seconds: int) -> None:
        """Updates max timer and slider"""
        hours = seconds // 3600
        seconds %= 3600
        minutes = seconds // 60
        seconds %= 60
        self.max_time_label.setText(f"{hours:02}:{minutes:02}:{seconds:02}")
        self.multiplayer_slider.setMaximum(hours * 3600 + minutes * 60 + seconds)

    def update_timer_and_slider(self, hour_minut_second: tuple[int, int, int]) -> None:
        """Updates timer and slider"""
        self.playing_time_label.setText(
            f"{hour_minut_second[0]:02}:{hour_minut_second[1]:02}:{hour_minut_second[2]:02}")
        self.multiplayer_slider.setValue(hour_minut_second[0] * 3600 + hour_minut_second[1] * 60 + hour_minut_second[2])

    def update_plot_type(self, plots: dict[str, list[str]]) -> None:
        """Updates plot type"""
        self.plots_type_list.clear()
        if self.plots_type_combobox.currentText():
            self.plots_type_list.addItems(plots[self.plots_type_combobox.currentText()])

    def update_plots(self, plot: dict[str, QPixmap]) -> None:
        """Updates plot"""
        self.generated_plots_list.clear()
        self.generated_plots_list.addItems(list(plot.keys()))

    def show_plot(self, plot: QPixmap | None) -> None:
        """Shows plot"""
        if plot:
            self.plot_display_label.setPixmap(
                plot.scaled(self.plot_display_label.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
            self.remove_generated_plot_button.setEnabled(True)
        else:
            self.plot_display_label.clear()
            self.remove_generated_plot_button.setEnabled(False)

    def update_file_selected(self):
        """Updates file selected"""
        if self.read_files_list.selectedItems():
            self.remove_files_button.setEnabled(True)
            self.add_to_player_button.setEnabled(True)
        else:
            self.remove_files_button.setEnabled(False)
            self.add_to_player_button.setEnabled(False)
