import os

from osop.filehandler import FileHandler


class PlaylistLibrary:
    @classmethod
    def retrieve_playlists(cls):
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

        return playlists