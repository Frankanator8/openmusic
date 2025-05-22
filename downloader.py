import json
import threading
from yt_dlp import YoutubeDL

class VideoDownload:
    def __init__(self, url, search=True):
        self.url = url
        self.search = search
        self.finished = False
        self._downloading = False

    def download(self):
        if not self.finished and not self._downloading:
            self._downloading = True
            self._download()

    def _download(self):
        params = {

        }
        url = self.url
        if self.search:
            params["playlist_items"] = "1:1"
            url = f"https://www.youtube.com/results?search_query={self.url.replace(" ", "+")}+%22topic%22"

        with YoutubeDL(params) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
            print(json.dumps(ydl.sanitize_info(info)))


