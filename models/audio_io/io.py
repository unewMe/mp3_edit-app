from models.audio_edit.AudioFile import AudioFile


def read_audio_file(file_path: str) -> AudioFile:
    """
    Read an audio file from the given file path.
    """
    return AudioFile.from_file(file_path)


def write_audio_file(audio_file: AudioFile, file_path: str, file_format: str = "mp3") -> None:
    """
    Write an audio file to the given file path.
    """
    audio_file.export(file_path, format=file_format)
