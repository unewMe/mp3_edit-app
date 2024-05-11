from models.audio_edit.AudioFile import AudioFile


def read_audio_file(file_path: str) -> AudioFile:
    """
    Read an audio file from the given file path.
    """
    return AudioFile.from_file(file_path)