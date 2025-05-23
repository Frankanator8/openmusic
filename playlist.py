import shutil
from operator import truediv

from filehandler import FileHandler


class Playlist:
    def __init__(self, uid):
        self.uid = uid
        self._songs = []
        self._shuffle = False
        self._name = ""
        self._image_url = ""
        self._changed = False

    def add_song(self, song_id):
        self._songs.append(song_id)
        self._changed = True

    def toggle_shuffle(self):
        self._shuffle = not self._shuffle
        self._changed = True

    def set_name(self, name):
        self._name = name
        self._changed = True

    def set_image_url(self, url):
        self._image_url = url
        self._changed = True


    def save(self):
        with open(f"{FileHandler.PLAYLIST_DATA}/{self.uid}.txt", "w") as f:
            f.writelines([self._name, 1 if self._shuffle else 0, ""] + self._songs)

        if self._image_url != "" and not self._image_url.startswith(self.uid):
            shutil.copyfile(self._image_url, f"{FileHandler.PLAYLIST_DATA}/{self.uid}.png")
            self._image_url = f"{FileHandler.PLAYLIST_DATA}/{self.uid}.png"

        self._changed = False

    def save_as_m3u(self, path):
        data = "#EXTM3U\n\n"
        for song in self._songs:
            with open(f"{FileHandler.SONG_DATA}/{song}.txt") as f:
                title = f.read()
                artist = f.read()
                album = f.read()
                duration = int(round(float(f.read())))
            data = f"#EXTINF:{duration},logo={FileHandler.SONG_DATA}/{song}.png,{title} - {artist} from {album}\n{FileHandler.AUDIOS}/{song}.mp3\n\n"

        data.strip()
        with open(path, "w") as f:
            f.write(data)

    @classmethod
    def load(cls, uid):
        instance = cls(uid)
        with open(f"{FileHandler.PLAYLIST_DATA}/{uid}.txt") as f:
            lines = f.readlines()

        for index, line in enumerate(lines):
            line = line.strip()
            if index == 0:
                instance._name = line

            elif index == 1:
                instance._shuffle = True if line == "1" else False

            elif index == 2:
                pass

            else:
                instance._songs.append(line)

        instance._image_url = f"{FileHandler.PLAYLIST_DATA}/{uid}.png"
        instance._changed = False

        return instance
