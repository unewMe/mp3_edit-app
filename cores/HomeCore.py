from PIL.ImageQt import QPixmap

from models.audio_edit.AudioFile import AudioFile
from models.mp3_players.AudioQueuePlayer import AudioQueuePlayer
from models.audio_io.io import read_audio_file
from models.mp3_players.MultiPlayer import MultiPlayer
from models.audio_edit.filters import FilterType
from models.visualizers.basevis import AudioVisualizer
from models.visualizers.rythmic import RhythmicAnalysis
from models.visualizers.segmentation import SegmentationAnalysis
from models.audio_edit.equalizer import Bands


class HomeCore:
    files: dict[str, AudioFile]
    players: dict[str, AudioQueuePlayer]
    plots: dict[str, QPixmap]
    _player_id: int
    multiplayer: MultiPlayer

    def __init__(self):
        self.files = {}
        self.players = {}
        self.plots = {}
        self._player_id = 1
        self.multiplayer = MultiPlayer()

    def add_file(self, file_path: str) -> None:
        """Adds an audio file to the file list. If the file already exists, a copy is created."""

        file_name = file_path.split("/")[-1].split(".")[0]
        audio_file = read_audio_file(file_path)
        if file_name not in self.files:
            self.files[file_name] = audio_file
        else:
            copy = file_name + "_copy"
            self.files[copy] = audio_file

    def remove_file(self, file_name: str) -> None:
        """Removes the selected file from the file list."""
        if file_name in self.files:
            self.files.pop(file_name)

    def create_player(self) -> None:
        """Creates a new player and adds it to the player list."""

        player = AudioQueuePlayer()
        self.players[f"Player{self._player_id}"] = player
        self.multiplayer.add_player(f"Player{self._player_id}", player)
        self._player_id += 1

    def remove_player(self, player_name: str) -> None:
        """Removes the selected player from the player list."""
        if player_name in self.players:
            self.players.pop(player_name)
            self.multiplayer.players.pop(player_name)

    def add_file_to_player(self, file_name: str, player_name: str) -> bool:
        """Adds the selected file to the selected player."""
        if player_name in self.players and file_name in self.files:
            self.players[player_name].load(file_name, AudioFile.from_segment(self.files[file_name]))
            return True
        return False

    def combine_audio_files(self) -> None:
        """Combines all audio files from the selected player."""
        for player in self.players.values():
            player.combine_audio_files()

    def play_multiplayer(self, volume: float) -> None:
        """Plays all the audio files from all the players."""

        self.multiplayer.play_all(volume)

    def pause_multiplayer(self) -> None:
        """Pauses the playback of all players."""

        self.multiplayer.pause_all()

    def resume_multiplayer(self) -> None:
        """Resumes the playback of all players."""

        self.multiplayer.resume_all()

    def stop_multiplayer(self) -> None:
        """Stops the playback of all players."""

        self.multiplayer.stop_all()

    def get_max_length_in_seconds(self) -> int:
        """Returns the maximum length of all audio files."""

        return round(self.multiplayer.get_max_length() / 1000)

    def get_current_time(self) -> tuple[int, int, int]:
        """Returns the current playback time."""

        return self.multiplayer.get_time()

    def check_if_any_audio_is_loaded_into_player(self) -> bool:
        """Checks if any audio is loaded into the player."""

        return any(player.sound_files for player in self.players.values())

    def update_player_order(self, player_name: str, order: list[str]) -> None:
        """Updates the play order of the selected player."""
        if player_name in self.players:
            self.players[player_name].set_play_order(order)

    def remove_from_player(self, file_name: str, player_name: str) -> None:
        """Removes the selected file from the selected player."""
        if player_name in self.players:
            self.players[player_name].remove(file_name)

    def get_volume_on_sound_in_player(self, player_name: str, selected_audio: str) -> float:
        """Returns the volume of the selected audio in the selected player."""
        if player_name in self.players:
            return self.players[player_name].get_audio_volume(selected_audio)
        return 0.0

    def get_audio_delay_in_player(self, player_name: str, selected_audio: str) -> int:
        """Returns the delay of the selected audio in the selected player."""
        if player_name in self.players:
            return self.players[player_name].get_audio_delay(selected_audio)
        return 0

    def set_volume_on_sound(self, player_name: str, selected_audio: str, volume: float) -> None:
        """Sets the volume of the selected audio in the selected player."""
        if player_name in self.players:
            self.players[player_name].set_volume_on_sound(selected_audio, volume)

    def set_audio_delay(self, player_name: str, selected_audio: str, delay: int) -> None:
        """ Sets the delay of the selected audio in the selected player."""
        if player_name in self.players:
            self.players[player_name].set_delay_on_sound(selected_audio, delay)

    def get_filters_from_sound(self, player_name: str, selected_audio: str) -> list[str]:
        """Returns the filters applied to the selected audio in the selected player."""
        if player_name in self.players:
            return [filter.value for filter in self.players[player_name].get_filters_from_sound(selected_audio)]
        return []

    def get_rest_of_filters(self, filters: list[str]) -> list[str]:
        """Returns the filters that are not applied to the selected audio."""

        return [filter.value for filter in FilterType if filter.value not in filters]

    def add_filter_on_audio(self, player_name: str, selected_audio: str, filter: str) -> None:
        """Adds a filter to the selected audio in the selected player."""
        if player_name in self.players:
            self.players[player_name].apply_filter(selected_audio, FilterType(filter))

    def remove_all_filters_on_audio(self, player_name: str, selected_audio: str) -> None:
        """Removes all filters from the selected audio in the selected player."""

        if player_name in self.players:
            new_audio = AudioFile.combine_with_audio_segment(self.players[player_name].sound_files[selected_audio],
                                                             self.files[selected_audio])
            new_audio.filters = []
            self.players[player_name].load(selected_audio, new_audio)

    def add_to_pixel_maps(self, name: str, file_path: str, analyzer: object, function_name: callable) -> None:
        """Adds a plot to the plot list. If the plot already exists, a copy is created."""

        path = f"{file_path}/{name}"
        function = getattr(analyzer, function_name.__name__)
        function(path)
        if name in self.plots:
            while name in self.plots:
                name = name.split(".")[0] + "_copy.png"
        self.plots[name] = QPixmap(path)

    def generate_plot(self, player_name: str, selected_audio: str, file_path: str, type: str, plots: list[str]) -> None:
        """Generates a plot of the selected audio in the selected player."""

        if player_name in self.players and selected_audio in self.players[player_name].sound_files:
            audio = self.players[player_name].sound_files[selected_audio]
            match type:
                case "Rythmic":
                    analyzer = RhythmicAnalysis(audio)
                    if "Tempogram" in plots:
                        self.add_to_pixel_maps(f"{selected_audio}_tempogram.png", file_path, analyzer,
                                               analyzer.analyze_tempogram)

                    if "Beats" in plots:
                        self.add_to_pixel_maps(f"{selected_audio}_beats.png", file_path, analyzer, analyzer.analyze_beats)

                case "Segmentation":
                    analyzer = SegmentationAnalysis(audio)
                    if "Silent segments" in plots:
                        self.add_to_pixel_maps(f"{selected_audio}_silent_segments.png", file_path, analyzer,
                                               analyzer.plot_silence_segments)
                    if "Beat segments" in plots:
                        self.add_to_pixel_maps(f"{selected_audio}_beat_segments.png", file_path, analyzer,
                                               analyzer.plot_silence_segments)
                case "Base visualize":
                    analyzer = AudioVisualizer(audio)
                    if "Waveform" in plots:
                        self.add_to_pixel_maps(f"{selected_audio}_waveform.png", file_path, analyzer,
                                               analyzer.plot_waveform)
                    if "Spectrogram" in plots:
                        self.add_to_pixel_maps(f"{selected_audio}_spectrogram.png", file_path, analyzer,
                                               analyzer.plot_spectrogram)

    def get_bands(self) -> list[Bands]:
        """Returns all bands."""

        return [band for band in Bands]

    def all_bands_value_from_audio(self, player_id: str, audio_id: str) -> dict[Bands, float]:
        """Returns the value of all bands from the selected audio in the selected player."""
        if player_id in self.players:
            return self.players[player_id].get_all_bands_from_audio(audio_id)

    def set_band_on_audio(self, player: str, audio: str, band: Bands, value: float) -> None:
        """Sets the value of the selected band on the selected audio in the selected player."""
        if player in self.players:
            self.players[player].set_band_on_audio(audio, band, value)

    def export(self, to_export: MultiPlayer | AudioQueuePlayer | AudioFile, path: str, format) -> None:
        """Exports the audio files from the selected player or the multiplayer to the selected path."""
        to_export.export(path, format=format)

    def set_main_volume(self, volume: float) -> None:
        """Sets the main volume of the player."""
        self.multiplayer.set_volume(volume)

    def __getstate__(self):
        state = self.__dict__.copy()
        file_info = {}

        if 'plots' in state:
            i = 0
            for key, plot in state['plots'].items():
                filename = f"{key}_plot_secret_{i}.png"
                plot.save(filename)
                file_info[key] = filename
                i += 1
            del state['plots']

        state['file_info'] = file_info

        return state

    def __setstate__(self, state):
        if 'file_info' in state:
            file_info = state.pop('file_info')
            state['plots'] = {}
            for key, filename in file_info.items():
                pixmap = QPixmap(filename)
                if not pixmap.isNull():
                    state['plots'][key] = pixmap
                else:
                    print(f"Error loading {key} from {filename}")

        self.__dict__.update(state)

    def remove_plot(self, plot_name) -> None:
        """Removes the selected plot from the plot list."""
        if plot_name in self.plots:
            self.plots.pop(plot_name)

    def init_all_players(self) -> None:
        """Initializes all players."""
        for player in self.players.values():
            player.init_player()
