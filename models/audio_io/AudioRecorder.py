import pyaudio
from pydub import AudioSegment


class AudioRecorder:
    """
    Class to record audio from the microphone.
    """

    _format: int  # Format of the audio
    _channels: int  # Number of audio channels
    _rate: int  # Sampling rate
    _chunk: int  # Chunk size
    _frames: list[bytes]  # List of recorded audio frames
    _stream: pyaudio.Stream | None  # Audio stream
    _audio: pyaudio.PyAudio  # PyAudio instance

    def __init__(self, format: int = pyaudio.paInt16, channels: int = 1, rate: int = 44100, chunk: int = 1024):
        self._format = format
        self._channels = channels
        self._rate = rate
        self._chunk = chunk
        self._frames = []
        self._stream = None
        self._audio = pyaudio.PyAudio()

    def start(self) -> None:
        """
        Start recording audio with callback.
        """
        self._stream = self._audio.open(format=self._format, channels=self._channels,
                                        rate=self._rate, input=True, frames_per_buffer=self._chunk,
                                        stream_callback=self.record_callback)
        self._frames = []
        self._stream.start_stream()
        print("Recording started.")

    def stop(self) -> None:
        """
        Stop the recording and close the stream.
        """
        self._stream.stop_stream()
        self._stream.close()
        print("Recording stopped.")

    def convert_to_audiosegment(self) -> AudioSegment:
        """
        Convert the recorded frames to a pydub AudioSegment directly from raw data.
        """
        # Combine frames into a byte buffer
        raw_data = b''.join(self._frames)

        audio_segment = AudioSegment(
            data=raw_data,
            sample_width=self._audio.get_sample_size(self._format),
            frame_rate=self._rate,
            channels=self._channels
        )
        return audio_segment

    def record_callback(self, in_data: bytes, frame_count: int, time_info: dict, status: int) -> tuple[bytes, int]:
        """
        Callback function to collect frames from the audio stream.
        """
        self._frames.append(in_data)
        return (in_data, pyaudio.paContinue)

    def export(self, filepath: str) -> None:
        """
        Export the recorded audio to a file.
        """
        audio_segment = self.convert_to_audiosegment()
        format = filepath.split(".")[-1]
        audio_segment.export(filepath, format=format)

    def reset(self) -> None:
        """
        Reset the recorder.
        """
        self._frames = []
        self._stream = None
        self._audio.terminate()
        self._audio = pyaudio.PyAudio()
