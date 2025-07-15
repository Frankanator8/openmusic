import pathlib
import os

class FileHandler:
    # Path to Application Support folder
    _app_support_path = os.path.join(pathlib.Path.home(), "Library", "Application Support", "OpenMusic")

    # Subdirectories
    AUDIOS = os.path.join(_app_support_path, "audio")
    SONG_DATA = os.path.join(_app_support_path, "songdata")
    PLAYLIST_DATA = os.path.join(_app_support_path, "playlistdata")
    PLUGINS = os.path.join(_app_support_path, "plugins")

    # Makes sure all above folders exist
    @classmethod
    def check_folder(cls):
        check = ["audio", "songdata", "playlistdata", "plugins"]
        for i in os.listdir(FileHandler._app_support_path):
            if os.path.isdir(os.path.join(FileHandler._app_support_path, i)):
                if i in check:
                    check.remove(i)

        for folder in check:
            os.mkdir(os.path.join(FileHandler._app_support_path, folder))



