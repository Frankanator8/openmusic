import os

from filehandler import FileHandler


class SongLibrary:
    @classmethod
    def retrieve_songs(cls):
        song_lib = {}
        for file in os.listdir(FileHandler.SONG_DATA):
            if file != ".DS_Store":
                uid = file.split(".")[0]
                if uid not in song_lib.keys():
                    song_lib[uid] = [False, False, False]

                if file.endswith(".txt"):
                    song_lib[uid][0] = True

                if file.endswith(".png"):
                    song_lib[uid][1] = True

        for file in os.listdir(FileHandler.AUDIOS):
            if file != ".DS_Store":
                uid = file.split(".")[0]
                song_lib[uid][2] = True

        songs = []
        for key, value in song_lib.items():
            if all(value):
                songs.append(key)

        return songs