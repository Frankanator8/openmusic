import random
import shutil
import uuid
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
        self._index = 0
        self.last_tracks = []
        self._guaranteedNext = -1

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

    def set_index(self, index):
        self._index = index
        self._changed = True

    def set_guaranteed_next(self, index):
        self._guaranteedNext = index

    def save(self):
        with open(f"{FileHandler.PLAYLIST_DATA}/{self.uid}.txt", "w") as f:
            f.write("\n".join([self._name, str(1 if self._shuffle else 0), str(self._index), ""] + self._songs))

        if self._image_url != "" and not self._image_url.split("/")[-1].startswith(self.uid):
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
                instance._index = int(line)

            elif index == 3:
                pass

            else:
                instance._songs.append(line)

        instance._image_url = f"{FileHandler.PLAYLIST_DATA}/{uid}.png"
        instance._changed = False

        return instance

    def request_next_track(self):
        self.last_tracks.append(self._index)
        seen = []
        for i in range(len(self._songs)):
            seen.append(False)

        for i in self.last_tracks:
            seen[i] = True

        if all(seen):
            self.last_tracks = self.last_tracks[-1:]

        if self._guaranteedNext != -1:
            self.set_index(self._guaranteedNext)
            self._guaranteedNext = -1

        else:
            if self._shuffle:
                attempts = 15
                while attempts > 0:
                    self.set_index(random.randint(0, len(self._songs)-1))
                    if self._index not in self.last_tracks:
                        break
                    attempts -= 1

            else:
                i = self._index
                i+=1
                i%= len(self._songs)
                self.set_index(i)

        return self._songs[self._index]

    def request_last_track(self, duration):
        if duration > 5:
            return self._songs[self._index]

        else:
            if len(self.last_tracks) == 0:
                self.set_index(0)
                return self._songs[0]

            else:
                self.set_index(self.last_tracks.pop(len(self.last_tracks)-1))
                return self._songs[self._index]

    @classmethod
    def create_playlist(cls, name, image_url, songs, shuffle):
        instance = cls(str(uuid.uuid4()).replace("-", ""))
        instance.set_name(name)
        instance.set_image_url(image_url)
        if shuffle:
            instance.toggle_shuffle()

        for song in songs:
            instance.add_song(song)

        return instance
