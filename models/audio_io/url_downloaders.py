from pytube import YouTube, request
import re

import re
from pytube import YouTube
from pytube import request


class YouTubeDownloader:
    def __init__(self):
        self.is_paused = False
        self.is_cancelled = False
        self.filesize = 0
        self.downloaded = 0

    def download_audio(self, url, filelocation):
        try:
            print('Connecting ...')
            yt = YouTube(url)
            stream = yt.streams.filter(only_audio=True).first()
            self.filesize = stream.filesize
            filename = ''.join([i for i in re.findall('[\w +/.]', yt.title) if i.isalpha()])
            filepath = f'{filelocation}/{filename}.mp3'
            with open(filepath, 'wb') as f:
                self.is_paused = self.is_cancelled = False
                stream = request.stream(stream.url)
                self.downloaded = 0
                while True:
                    if self.is_cancelled:
                        print('Download cancelled')
                        break
                    if self.is_paused:
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
        except Exception as e:
            print(e)

downloader = YouTubeDownloader()
downloader.download_audio('https://www.youtube.com/watch?v=SDFdzLJBH7g', './')
