from PySide6.QtCore import (QCoreApplication,
                            QMetaObject, QRect, Qt)
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QComboBox, QFrame,
                               QLabel, QLineEdit, QListView, QPushButton,
                               QSlider, QTabWidget, QWidget, QMainWindow, QListWidget, QMenuBar)


class HomeView(QMainWindow):

    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.initUI(self)

    def initUI(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"Dialog")

        dialog.setFixedSize(1920, 1080)
        dialog.setWindowTitle("Audio editor")

        self.menuBar().addMenu("File")
        self.menuBar().setGeometry(QRect(0, 0, 1920, 10))

        self.tab_view = QTabWidget(dialog)
        self.tab_view.setGeometry(QRect(10, 40, 701, 481))

        self.files = QWidget()
        self.files.setObjectName(u"files")

        self.read_files_list = QListWidget(self.files)
        self.read_files_list.setGeometry(QRect(20, 60, 641, 391))

        self.add_file_button = QPushButton(self.files)
        self.add_file_button.setGeometry(QRect(505, 30, 75, 24))
        self.add_file_button.setText("Add")

        self.remove_files_button = QPushButton(self.files)
        self.remove_files_button.setGeometry(QRect(586, 30, 75, 24))
        self.remove_files_button.setText("Remove")

        self.read_files_label = QLabel(self.files)
        self.read_files_label.setGeometry(QRect(21, 32, 71, 16))

        font = QFont()
        font.setPointSize(12)

        self.read_files_label.setFont(font)
        self.read_files_label.setText("Read files")

        self.tab_view.addTab(self.files, "")
        self.tab_view.setTabText(self.tab_view.indexOf(self.files),"Files")

        self.players = QWidget()

        self.create_player_button = QPushButton(self.players)
        self.create_player_button.setGeometry(QRect(505, 30, 75, 24))
        self.create_player_button.setText("Create")

        self.created_players_label = QLabel(self.players)
        self.created_players_label.setGeometry(QRect(21, 32, 121, 21))
        self.created_players_label.setFont(font)
        self.created_players_label.setText("Created players")

        self.remove_player_button = QPushButton(self.players)
        self.remove_player_button.setGeometry(QRect(586, 30, 75, 24))
        self.remove_player_button.setText("Remove")

        self.created_players_list = QListWidget(self.players)
        self.created_players_list.setGeometry(QRect(20, 60, 641, 391))

        self.tab_view.addTab(self.players, "")
        self.tab_view.setTabText(self.tab_view.indexOf(self.players), "Players")

        self.plots = QWidget()

        self.generated_plots_label = QLabel(self.plots)
        self.generated_plots_label.setGeometry(QRect(21, 32, 121, 21))
        self.generated_plots_label.setFont(font)
        self.generated_plots_label.setText("Generated plots")

        self.remove_generated_plot_button = QPushButton(self.plots)
        self.remove_generated_plot_button.setGeometry(QRect(586, 30, 75, 24))
        self.remove_generated_plot_button.setText("Remove")

        self.generated_plots_list = QListView(self.plots)
        self.generated_plots_list.setGeometry(QRect(20, 60, 641, 391))

        self.tab_view.addTab(self.plots, "")
        self.tab_view.setTabText(self.tab_view.indexOf(self.plots), "Plots")

        self.main_player_frame = QFrame(dialog)
        self.main_player_frame.setGeometry(QRect(720, 43, 1191, 478))
        self.main_player_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.main_player_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.play_button = QPushButton(self.main_player_frame)
        self.play_button.setGeometry(QRect(620, 440, 51, 24))
        self.play_button.setText("Play")

        self.stop_button = QPushButton(self.main_player_frame)
        self.stop_button.setGeometry(QRect(560, 440, 51, 24))
        self.stop_button.setText("Stop")

        self.multiplayer_slider = QSlider(self.main_player_frame)
        self.multiplayer_slider.setGeometry(QRect(20, 410, 1161, 22))
        self.multiplayer_slider.setOrientation(Qt.Orientation.Horizontal)

        self.main_volume_slider = QSlider(self.main_player_frame)
        self.main_volume_slider.setGeometry(QRect(1010, 440, 160, 22))
        self.main_volume_slider.setMaximum(100)
        self.main_volume_slider.setValue(100)
        self.main_volume_slider.setOrientation(Qt.Orientation.Horizontal)

        self.main_volume_label = QLabel(self.main_player_frame)
        self.main_volume_label.setGeometry(QRect(950, 442, 49, 16))
        self.main_volume_label.setText("Volume")

        self.plot_display_frame = QFrame(self.main_player_frame)
        self.plot_display_frame.setGeometry(QRect(70, 30, 1071, 361))
        self.plot_display_frame.setFrameShape(QFrame.Shape.Box)
        self.plot_display_frame.setFrameShadow(QFrame.Shadow.Sunken)

        self.playing_time_label = QLabel(self.main_player_frame)
        self.playing_time_label.setGeometry(QRect(20, 450, 49, 16))
        self.playing_time_label.setText("00:00:00")

        self.max_time_label = QLabel(self.main_player_frame)
        self.max_time_label.setGeometry(QRect(70, 450, 61, 16))
        self.max_time_label.setText("/  00:00:00")

        self.player_editing_frame = QFrame(dialog)
        self.player_editing_frame.setGeometry(QRect(10, 540, 1901, 531))
        self.player_editing_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.player_editing_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.editing_player_label = QLabel(self.player_editing_frame)
        self.editing_player_label.setGeometry(QRect(10, 10, 141, 21))
        self.editing_player_label.setFont(font)
        self.editing_player_label.setText("Player:")

        self.audios_in_player_list = QListView(self.player_editing_frame)
        self.audios_in_player_list.setGeometry(QRect(10, 110, 461, 391))

        self.audios_in_player_label = QLabel(self.player_editing_frame)
        self.audios_in_player_label.setGeometry(QRect(12, 80, 61, 21))
        self.audios_in_player_label.setFont(font)
        self.audios_in_player_label.setText("Audios")

        self.audio_editing_frame = QFrame(self.player_editing_frame)
        self.audio_editing_frame.setGeometry(QRect(570, 60, 1311, 441))
        self.audio_editing_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.audio_editing_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.audio_filters_list = QListView(self.audio_editing_frame)
        self.audio_filters_list.setGeometry(QRect(182, 90, 261, 261))

        self.hz62_slider = QSlider(self.audio_editing_frame)
        self.hz62_slider.setGeometry(QRect(840, 140, 22, 160))
        self.hz62_slider.setMinimum(-15)
        self.hz62_slider.setMaximum(15)
        self.hz62_slider.setValue(0)
        self.hz62_slider.setSliderPosition(0)
        self.hz62_slider.setOrientation(Qt.Orientation.Vertical)

        self.hz125_slider = QSlider(self.audio_editing_frame)
        self.hz125_slider.setGeometry(QRect(890, 140, 22, 160))
        self.hz125_slider.setMinimum(-15)
        self.hz125_slider.setMaximum(15)
        self.hz125_slider.setValue(0)
        self.hz125_slider.setOrientation(Qt.Orientation.Vertical)

        self.hz250_slider = QSlider(self.audio_editing_frame)
        self.hz250_slider.setGeometry(QRect(940, 140, 22, 160))
        self.hz250_slider.setMinimum(-15)
        self.hz250_slider.setMaximum(15)
        self.hz250_slider.setValue(0)
        self.hz250_slider.setOrientation(Qt.Orientation.Vertical)

        self.hz500_slider = QSlider(self.audio_editing_frame)
        self.hz500_slider.setGeometry(QRect(990, 140, 22, 160))
        self.hz500_slider.setMinimum(-15)
        self.hz500_slider.setMaximum(15)
        self.hz500_slider.setValue(0)
        self.hz500_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz1_slider = QSlider(self.audio_editing_frame)
        self.khz1_slider.setGeometry(QRect(1040, 140, 22, 160))
        self.khz1_slider.setMinimum(-15)
        self.khz1_slider.setMaximum(15)
        self.khz1_slider.setValue(0)
        self.khz1_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz2_slider = QSlider(self.audio_editing_frame)
        self.khz2_slider.setGeometry(QRect(1090, 140, 22, 160))
        self.khz2_slider.setMinimum(-15)
        self.khz2_slider.setMaximum(15)
        self.khz2_slider.setValue(0)
        self.khz2_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz4_slider = QSlider(self.audio_editing_frame)
        self.khz4_slider.setGeometry(QRect(1140, 140, 22, 160))
        self.khz4_slider.setMinimum(-15)
        self.khz4_slider.setMaximum(15)
        self.khz4_slider.setValue(0)
        self.khz4_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz8_slider = QSlider(self.audio_editing_frame)
        self.khz8_slider.setGeometry(QRect(1190, 140, 22, 160))
        self.khz8_slider.setMinimum(-15)
        self.khz8_slider.setMaximum(15)
        self.khz8_slider.setValue(0)
        self.khz8_slider.setOrientation(Qt.Orientation.Vertical)

        self.khz16_slider = QSlider(self.audio_editing_frame)
        self.khz16_slider.setGeometry(QRect(1240, 140, 22, 160))
        self.khz16_slider.setMinimum(-15)
        self.khz16_slider.setMaximum(15)
        self.khz16_slider.setValue(0)
        self.khz16_slider.setOrientation(Qt.Orientation.Vertical)

        self.equalizer_label = QLabel(self.audio_editing_frame)
        self.equalizer_label.setGeometry(QRect(840, 90, 101, 21))
        self.equalizer_label.setText("Equalizer")

        font = QFont()
        font.setPointSize(15)
        self.equalizer_label.setFont(font)

        audio_volume_label = QLabel(self.audio_editing_frame)
        audio_volume_label.setGeometry(QRect(60, 130, 49, 16))

        audio_delay_label = QLabel(self.audio_editing_frame)
        audio_delay_label.setGeometry(QRect(60, 230, 41, 16))
        audio_delay_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        audio_volume_label.setText("Volume")
        audio_delay_label.setText("Delay")

        self.audio_delay_edit = QLineEdit(self.audio_editing_frame)
        self.audio_delay_edit.setGeometry(QRect(60, 250, 41, 22))

        self.audio_filters_label = QLabel(self.audio_editing_frame)
        self.audio_filters_label.setGeometry(QRect(182, 60, 61, 21))
        self.audio_filters_label.setFont(font)
        self.audio_filters_label.setText("Filters")

        self.add_filter_butoon = QPushButton(self.audio_editing_frame)
        self.add_filter_butoon.setGeometry(QRect(292, 60, 75, 24))
        self.add_filter_butoon.setText("Add")

        self.remove_all_filters_button = QPushButton(self.audio_editing_frame)
        self.remove_all_filters_button.setGeometry(QRect(370, 60, 75, 24))
        self.remove_all_filters_button.setText("Remove all")

        line = QFrame(self.audio_editing_frame)
        line.setEnabled(False)
        line.setGeometry(QRect(830, 180, 441, 16))
        line.setFrameShape(QFrame.Shape.HLine)
        line.setFrameShadow(QFrame.Shadow.Sunken)

        line_2 = QFrame(self.audio_editing_frame)
        line_2.setEnabled(False)
        line_2.setGeometry(QRect(830, 211, 441, 16))
        line_2.setFrameShape(QFrame.Shape.HLine)
        line_2.setFrameShadow(QFrame.Shadow.Sunken)

        line_3 = QFrame(self.audio_editing_frame)
        line_3.setEnabled(False)
        line_3.setGeometry(QRect(830, 242, 441, 16))
        line_3.setFrameShape(QFrame.Shape.HLine)
        line_3.setFrameShadow(QFrame.Shadow.Sunken)

        line_4 = QFrame(self.audio_editing_frame)
        line_4.setEnabled(False)
        line_4.setGeometry(QRect(830, 272, 441, 16))
        line_4.setFrameShape(QFrame.Shape.HLine)
        line_4.setFrameShadow(QFrame.Shadow.Sunken)

        line_5 = QFrame(self.audio_editing_frame)
        line_5.setEnabled(False)
        line_5.setGeometry(QRect(830, 150, 441, 16))
        line_5.setFrameShape(QFrame.Shape.HLine)
        line_5.setFrameShadow(QFrame.Shadow.Sunken)

        dB12_label = QLabel(self.audio_editing_frame)
        dB12_label.setGeometry(QRect(775, 150, 49, 16))
        dB12_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        db6_label = QLabel(self.audio_editing_frame)
        db6_label.setGeometry(QRect(775, 180, 49, 16))
        db6_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        dB0_label = QLabel(self.audio_editing_frame)
        dB0_label.setGeometry(QRect(775, 210, 49, 16))
        dB0_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        dBn6_label = QLabel(self.audio_editing_frame)
        dBn6_label.setGeometry(QRect(775, 240, 49, 16))
        dBn6_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        dbn12_label = QLabel(self.audio_editing_frame)
        dbn12_label.setGeometry(QRect(775, 270, 49, 16))
        dbn12_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignTrailing | Qt.AlignmentFlag.AlignVCenter)

        dB12_label.setText("+12 dB")
        db6_label.setText("+6 dB")
        dB0_label.setText("0 dB")
        dbn12_label.setText("-12 dB")
        dBn6_label.setText("-6 dB")


        self.audio_plots_label = QLabel(self.audio_editing_frame)
        self.audio_plots_label.setGeometry(QRect(502, 60, 61, 21))
        self.audio_plots_label.setFont(font)
        self.audio_plots_label.setText("Plots")

        self.plots_type_list = QListView(self.audio_editing_frame)
        self.plots_type_list.setGeometry(QRect(502, 90, 261, 261))

        self.generate_plot_button = QPushButton(self.audio_editing_frame)
        self.generate_plot_button.setGeometry(QRect(690, 60, 75, 24))
        self.generate_plot_button.setText("Generate")

        self.plots_type_combobox = QComboBox(self.audio_editing_frame)
        self.plots_type_combobox.setGeometry(QRect(598, 60, 91, 24))
        self.plots_type_combobox.setEditable(True)
        self.plots_type_combobox.setCurrentText("Type")


        self.editing_audio_label = QLabel(self.audio_editing_frame)
        self.editing_audio_label.setGeometry(QRect(10, 10, 141, 21))
        self.editing_audio_label.setFont(font)
        self.editing_audio_label.setText("Editing")

        self.audio_volume_slider = QSlider(self.audio_editing_frame)
        self.audio_volume_slider.setGeometry(QRect(30, 160, 111, 22))
        self.audio_volume_slider.setMaximum(100)
        self.audio_volume_slider.setValue(100)
        self.audio_volume_slider.setOrientation(Qt.Orientation.Horizontal)

        self.cancel_audio_button = QPushButton(self.audio_editing_frame)
        self.cancel_audio_button.setGeometry(QRect(1228, 10, 75, 24))
        self.cancel_audio_button.setText("Cancel")

        self.save_audio_button = QPushButton(self.audio_editing_frame)
        self.save_audio_button.setGeometry(QRect(1150, 10, 75, 24))
        self.save_audio_button.setText("Save")

        self.choose_audio_label = QLabel(self.audio_editing_frame)
        self.choose_audio_label.setGeometry(QRect(-10, -10, 1321, 451))
        self.choose_audio_label.setFont(font)
        self.choose_audio_label.setStyleSheet(u"background-color: rgba(0, 0, 0, 120);")
        self.choose_audio_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.choose_audio_label.setText("Choose Audio")

        self.hz62_slider.raise_()
        self.hz125_slider.raise_()
        self.hz250_slider.raise_()
        self.hz500_slider.raise_()
        self.khz1_slider.raise_()
        self.khz2_slider.raise_()
        self.khz4_slider.raise_()
        self.khz8_slider.raise_()
        self.khz16_slider.raise_()



        self.add_to_player_button = QPushButton(self.player_editing_frame)
        self.add_to_player_button.setGeometry(QRect(318, 80, 75, 24))
        self.add_to_player_button.setText("Add")

        self.remove_from_player_button = QPushButton(self.player_editing_frame)
        self.remove_from_player_button.setGeometry(QRect(397, 80, 75, 24))
        self.remove_from_player_button.setText("Remove")

        self.queue_up_button = QPushButton(self.player_editing_frame)
        self.queue_up_button.setGeometry(QRect(490, 230, 51, 41))
        self.queue_up_button.setText("Up")

        self.queue_down_button = QPushButton(self.player_editing_frame)
        self.queue_down_button.setGeometry(QRect(490, 280, 51, 41))
        self.queue_down_button.setText("Down")

        self.queue_label = QLabel(self.player_editing_frame)
        self.queue_label.setGeometry(QRect(498, 200, 49, 16))
        self.queue_label.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.queue_label.setText("Queue")

        self.choose_player_label = QLabel(self.player_editing_frame)
        self.choose_player_label.setEnabled(True)
        self.choose_player_label.setGeometry(QRect(-160, -10, 2411, 651))
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

    def update_player_list(self, players):
        """Updates created players list"""
        self.created_players_list.clear()
        self.created_players_list.addItems(players)

    def update_player_info(self):
        """Updates player info"""
        if self.created_players_list.selectedItems():
            player_name = self.created_players_list.currentItem().text()
            self.editing_player_label.setText(f"Player: {player_name}")
            self.choose_player_label.hide()
        else:
            self.editing_player_label.setText("Player:")
            self.choose_player_label.show()





