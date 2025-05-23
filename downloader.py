import os

from yt_dlp import YoutubeDL
import uuid
from filehandler import FileHandler
from moviepy import *
from PIL import Image


class VideoDownload:
    def __init__(self, url, search=True):
        self.url = url
        self.search = search
        self.finished = False
        self._downloading = False
        self.uid = ""

    def _generate_uuid(self):
        return str(uuid.uuid4()).replace("-", "")

    def download(self):
        if not self.finished and not self._downloading:
            self._downloading = True
            self._download()

    def _download(self):
        uid = self._generate_uuid()
        self.uid = uid
        params = {
            "quiet":True,
            "paths":{"home":f"{FileHandler.TEMP_VID_STORAGE}/{uid}/", "temp":f"{FileHandler.TEMP_VID_STORAGE}/{uid}/"}
        }
        url = self.url
        if self.search:
            params["playlist_items"] = "1:1"
            url = f"https://www.youtube.com/results?search_query={self.url.replace(" ", "+")}+%22topic%22"

        album = "Song Album"
        title = "Song Title"
        artist = "Unknown Artist"
        with YoutubeDL(params) as ydl:
            info = ydl.extract_info(url, download=False)
            ydl.download([url])
            desc = ydl.sanitize_info(info)["entries"][0]["description"]
            titleLine = desc.split("\n")[2].split("·")
            album = desc.split("\n")[4]
            title = titleLine[0].strip()
            artist = titleLine[1].strip()

        videoFile = ""
        for file in os.listdir(f"{FileHandler.TEMP_VID_STORAGE}/{uid}/"):
            if file != ".DS_Store":
                videoFile = file
        clip = VideoFileClip(f"{FileHandler.TEMP_VID_STORAGE}/{uid}/{videoFile}")
        clip.audio.write_audiofile(f"{FileHandler.AUDIOS}/{uid}.mp3")
        img = Image.fromarray(clip.get_frame(0))
        img.save(f"{FileHandler.SONG_DATA}/{uid}.png")

        with open(f"{FileHandler.SONG_DATA}/{uid}.txt", "w") as f:
            f.write(f"{title}\n{artist}\n{album}\n{clip.duration}")

        self.finished = True
        self._downloading = False


