from dataclasses import dataclass

from pytube import YouTube, request
from pytube import exceptions as exp
import re


@dataclass
class YouTubeDownloader:
    """
    Class to download audio from YouTube
    """
    _is_paused: bool = False # flag to check if download is paused
    _is_cancelled: bool = False # flag to check if download is cancelled
    downloaded: int = 0 # downloaded bytes
    filesize: int = 0 # total file size

    def download_audio(self, url: str, filelocation: str, filename: str) -> None:
        """
        Download audio from YouTube to mp3
        """

        try:
            print('Connecting ...')
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            self.filesize = stream.filesize
            filepath = f'{filelocation}/{filename}.mp3'
            with open(filepath, 'wb') as f:
                self._is_paused = self._is_cancelled = False
                stream = request.stream(stream.url)
                self.downloaded = 0
                while True:
                    if self._is_cancelled:
                        print('Download cancelled')
                        break
                    if self._is_paused:
                        continue
                    chunk = next(stream, None)
                    if chunk:
                        f.write(chunk)
                        self.downloaded += len(chunk)
                        print(f'Downloaded {self.downloaded} / {self.filesize}')
                    else:
                        # no more data
                        print('Audio Download completed!')
                        break
            print('done')
        except exp.VideoUnavailable:
            raise exp.VideoUnavailable("Video is unavailable.")
        except ConnectionError:
            raise ConnectionError("Network connection error.")
        except TimeoutError:
            raise TimeoutError("Request timed out.")
        except IOError:
            raise IOError("Incorrect path.")
        except exp.RegexMatchError:
            raise ValueError("Invalid URL.")
        except Exception as e:
            raise Exception(f"An unexpected error occurred: {str(e)}")
