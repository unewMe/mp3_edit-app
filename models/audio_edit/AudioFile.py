from pydub import AudioSegment
import math
import io
from models.audio_edit.filters import FilterType
from models.audio_edit.equalizer import Equalizer


class AudioFile(AudioSegment):
    """
    Class to represent an audio file.
    """

    delay: int  # Delay in seconds before playing the audio file
    volume: float  # Volume of the audio file
    filters: list[FilterType]  # List of filters to apply to the audio file
    equalizer: Equalizer  # Equalizer object to adjust the audio file

    def __init__(self, data=None, delay=0, filters=None, volume: float = 100, equalizer=None, *args,
                 **kwargs):
        super().__init__(data, *args, **kwargs)
        filters = filters or []
        self.delay = delay
        self.volume = volume
        self.filters = filters
        self.equalizer = Equalizer(self) if not equalizer else equalizer

    @classmethod
    def from_segment(cls, segment: AudioSegment):
        return cls(segment._data, frame_rate=segment.frame_rate, sample_width=segment.sample_width,
                   channels=segment.channels)

    @classmethod
    def from_audiofile(cls, audiofile):
        return cls(audiofile._data, frame_rate=audiofile.frame_rate, sample_width=audiofile.sample_width,
                   channels=audiofile.channels, filters=audiofile.filters, delay=audiofile.delay,
                   volume=audiofile.volume, equalizer=audiofile.equalizer)

    @classmethod
    def from_file(cls, file_path: str):
        return cls.from_segment(AudioSegment.from_file(file_path))

    @classmethod
    def combine_with_audio_segment(cls, audiofile, audio_segment: AudioSegment):
        return cls(audio_segment._data, frame_rate=audio_segment.frame_rate, sample_width=audio_segment.sample_width,
                   channels=audio_segment.channels, delay=audiofile.delay,
                   volume=audiofile.volume, filters=audiofile.filters, equalizer=audiofile.equalizer)

    def _spawn(self, data: bytes, overrides={}):
        """
        Spawns a new AudioFile object with the given data and overrides.
        """
        return self.__class__(data, frame_rate=self.frame_rate, sample_width=self.sample_width,
                              channels=self.channels, delay=self.delay, volume=self.volume, filters=self.filters, equalizer=self.equalizer)

    def to_buffer(self, format: str = "mp3"):
        """
        Exports the audio file to a buffer.
        """
        buffer = io.BytesIO()
        self.export(buffer, format=format)
        buffer.seek(0)
        return buffer

    def replace_with_audio(self, new_audio: bytes | AudioSegment):
        """
        Replaces the current audio fragment with a new one, which can be either
        the AudioSegment object as well as the raw audio data.
        """
        if isinstance(new_audio, bytes):
            new_segment = AudioSegment.from_file(io.BytesIO(new_audio))
        elif isinstance(new_audio, AudioSegment):
            new_segment = new_audio
        else:
            raise TypeError("New audio must be either an AudioSegment instance or raw audio data as bytes.")

        # Returns a new AudioFile with the audio replaced
        return self._spawn(new_segment.get_array_of_samples(), overrides={
            "frame_rate": new_segment.frame_rate,
            "sample_width": new_segment.sample_width,
            "channels": new_segment.channels
        })

    def set_volume(self, volume: float):
        """
        Sets the volume of the audio file.
        """
        current_gain = -40.0 * math.log10(100 / self.volume) if self.volume > 0 else -80

        target_gain = -40.0 * math.log10(100 / volume) if volume > 0 else -80

        gain_adjustment = target_gain - current_gain

        adjusted_audio_segment = self.apply_gain(gain_adjustment)

        self.volume = volume

        return self.combine_with_audio_segment(self, adjusted_audio_segment)

    def apply_filter(self, filter_type: FilterType):
        """
        Applies the given filter to the audio file.
        :return: AudioFile
        """
        self.filters.append(filter_type)
        return filter_type.create_filter(self)

    def set_value_on_band(self, band, value: float):
        """
        Sets the value on the given band of the equalizer.
        :return: AudioFile
        """
        return self.equalizer.change_band_gain(band, value)

    def get_all_bands(self):
        """
        Returns all bands of the equalizer.
        """
        return self.equalizer.get_all_bands()
