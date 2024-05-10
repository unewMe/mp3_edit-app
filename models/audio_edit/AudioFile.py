from pydub import AudioSegment
import math
import io


class AudioFile(AudioSegment):

    def to_buffer(self, format: str = "wav"):
        """Exports the audio file to a buffer."""
        buffer = io.BytesIO()
        self.export(buffer, format=format)
        buffer.seek(0)
        return buffer

    def set_volume(self, percent: float):
        """Sets the volume of the audio file to the given percentage"""
        if percent == 0:
            # For 0% volume, we set the volume to negative infinity in dB
            new_volume = -math.inf
        else:
            # Logarithmic scale for volume
            new_volume = 20 * math.log10(percent / 100)

        # Calculates the volume change in dB
        volume_change = new_volume - self.dBFS

        # Returns a new AudioFile with the volume changed
        return self._spawn(self.get_array_of_samples(), overrides={
            "frame_rate": self.frame_rate,
            "sample_width": self.sample_width,
            "channels": self.channels
        }).apply_gain(volume_change)

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
