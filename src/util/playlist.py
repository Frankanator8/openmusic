import os
import random
import shutil

from util.songs import Songs
from osop.filehandler import FileHandler

class Playlist:
    # Holds previously created Playlist objects to prevent dupes
    cache = {}
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
        Playlist.cache[uid] = self

    # Next few functions are pretty self explanatory
    def add_song(self, song_id):
        self._songs.append(song_id)
        self._changed = True

    def remove_song(self, song_id):
        self._songs.remove(song_id)
        self._changed = True

    @property
    def songs(self):
        return self._songs

    @songs.setter
    def songs(self, value):
        self._songs = value
        self._changed = True

    @property
    def shuffle(self):
        return self._shuffle

    @shuffle.setter
    def shuffle(self, value):
        self._shuffle = value
        self._changed = True

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name
        self._changed = True

    @property
    def image_url(self):
        return self._image_url

    @image_url.setter
    def image_url(self, url):
        self._image_url = url
        self._changed = True

    def set_index(self, index):
        self._index = index
        self._changed = True

    def set_guaranteed_next(self, index):
        self._guaranteedNext = index

    # Save playlist as a file
    def save(self):
        with open(os.path.join(FileHandler.PLAYLIST_DATA, f"{self.uid}.txt"), "w") as f:
            f.write("\n".join([self._name, str(1 if self._shuffle else 0), str(self._index), ""] + self._songs))

        if self._image_url != "" and not self._image_url.split("/")[-1].startswith(self.uid):
            shutil.copyfile(self._image_url, str(os.path.join(FileHandler.PLAYLIST_DATA, f"{self.uid}.png")))
            self._image_url = str(os.path.join(FileHandler.PLAYLIST_DATA, f"{self.uid}.png"))

        self._changed = False

    # Unused, but saves the playlist as a .m3u file
    def save_as_m3u(self, path):
        data = "#EXTM3U\n\n"
        for song in self._songs:
            with open(os.path.join(FileHandler.SONG_DATA, f"{song}.txt")) as f:
                title = f.read()
                artist = f.read()
                album = f.read()
                duration = int(round(float(f.read())))
            data = f"#EXTINF:{duration},logo={str(os.path.join(FileHandler.SONG_DATA, f'{song}.png'))},{title} - {artist} from {album}\n{str(os.path.join(FileHandler.AUDIOS, f'{song}.mp3'))}\n\n"

        data.strip()
        with open(path, "w") as f:
            f.write(data)

    # Loads a playlist file
    @classmethod
    def load(cls, uid):
        if uid in cls.cache:
            return cls.cache[uid]

        else:
            instance = cls(uid)
            with open(os.path.join(FileHandler.PLAYLIST_DATA, f"{uid}.txt")) as f:
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

            instance._image_url = str(os.path.join(FileHandler.PLAYLIST_DATA, f"{uid}.png"))
            instance._changed = False

            return instance

    # Called by OSPlayer to get the next track (random if shuffled, next index if not)
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

    # Get previously played track
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

    # Creates a playlist given following parameters
    @classmethod
    def create_playlist(cls, name, image_url, songs, shuffle):
        instance = cls(Songs.make_uid())
        instance.name = name
        instance.image_url = image_url
        instance.shuffle = shuffle

        for song in songs:
            instance.add_song(song)

        return instance

    # Deletes this playlist
    def delete(self):
        os.remove(os.path.join(FileHandler.PLAYLIST_DATA, f"{self.uid}.txt"))
        os.remove(os.path.join(FileHandler.PLAYLIST_DATA, f"{self.uid}.png"))
        del Playlist.cache[self.uid]

    # Retrieves all available playlists. Force no cache makes sure that it reloads from disk and not from program memory
    @classmethod
    def retrieve_playlists(cls, force_no_cache=False):
        if cls.cache == {} or force_no_cache:
            playlist_lib = {}
            for file in os.listdir(FileHandler.PLAYLIST_DATA):
                if file != ".DS_Store":
                    uid = file.split(".")[0]
                    if uid not in playlist_lib.keys():
                        playlist_lib[uid] = [False, False]

                    if file.endswith(".txt"):
                        playlist_lib[uid][0] = True

                    if file.endswith(".png"):
                        playlist_lib[uid][1] = True


            playlists = []
            for key, value in playlist_lib.items():
                if all(value):
                    playlists.append(key)
                    Playlist.load(key)

            return playlists

        else:
            playlists = []
            for key in cls.cache.keys():
                playlists.append(key)
            return playlists

    # Used for playlist blocks, finds a Playlist's image and title and nothing else
    @classmethod
    def retrieve_quick_data(cls, uid):
        if uid != "":
            if uid not in cls.cache.keys():
                Playlist.load(uid)


            image_url = cls.cache[uid].image_url
            title = cls.cache[uid].name

        else:
            image_url = os.path.join("img", "x.png")
            title = "(no playlist)"

        return image_url, title