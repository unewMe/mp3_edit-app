from pydub import AudioSegment
import math
import io
from models.audio_edit.filters import FilterType


class AudioFile(AudioSegment):
    delay: int

    def __init__(self, data=None, *args, **kwargs):
        super().__init__(data, *args, **kwargs)
        self.delay = 0

    @classmethod
    def from_segment(cls, segment: AudioSegment):
        return cls(segment._data, frame_rate=segment.frame_rate, sample_width=segment.sample_width,
                   channels=segment.channels)

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
        return self.apply_gain(math.log10(volume) * 10)

    def apply_filter(self, filter_type: FilterType):
        """
        Applies the given filter to the audio file.
        """
        filter_instance = filter_type.value(self)
        return filter_instance.apply()
