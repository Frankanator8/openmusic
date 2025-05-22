from yt_dlp import YoutubeDL
import uuid
from filehandler import FileHandler


class VideoDownload:
    def __init__(self, url, search=True):
        self.url = url
        self.search = search
        self.finished = False
        self._downloading = False

    def _generate_uuid(self):
        return str(uuid.uuid4()).replace("-", "")

    def download(self):
        if not self.finished and not self._downloading:
            self._downloading = True
            self._download()

    def _download(self):
        uid = self._generate_uuid()
        params = {
            "quiet":True,
            "paths":{"home":f"{FileHandler.TEMP_VID_STORAGE}/{uid}/", "temp":f"{FileHandler.TEMP_VID_STORAGE}/{uid}/"}
        }
        url = self.url
        if self.search:
            params["playlist_items"] = "1:1"
            url = f"https://www.youtube.com/results?search_query={self.url.replace(" ", "+")}+%22topic%22"

        with YoutubeDL(params) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
            desc = ydl.sanitize_info(info)["entries"][0]["description"]
            titleLine = desc.split("\n")[2].split("·")
            album = desc.split("\n")[4]
            title = titleLine[0].strip()
            artist = titleLine[1].strip()
            print(title, artist, album)


