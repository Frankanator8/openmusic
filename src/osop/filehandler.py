import pathlib
import os
import sys


class FileHandler:
    # Path to Application Support folder
    _app_support_path = os.path.join(pathlib.Path.home(), "Library", "Application Support", "OpenMusic") if sys.platform == "darwin" else os.path.join(pathlib.Path.home(), "AppData", "Roaming", "OpenMusic")

    # Subdirectories
    AUDIOS = os.path.join(_app_support_path, "audio")
    SONG_DATA = os.path.join(_app_support_path, "songdata")
    PLAYLIST_DATA = os.path.join(_app_support_path, "playlistdata")
    PLUGINS = os.path.join(_app_support_path, "plugins")

    # Makes sure all above folders existx
    @classmethod
    def check_folder(cls):
        check = ["audio", "songdata", "playlistdata", "plugins"]
        if not os.path.isdir(FileHandler._app_support_path):
            os.mkdir(FileHandler._app_support_path)

        for i in os.listdir(FileHandler._app_support_path):
            if os.path.isdir(os.path.join(FileHandler._app_support_path, i)):
                if i in check:
                    check.remove(i)

        for folder in check:
            os.mkdir(os.path.join(FileHandler._app_support_path, folder))



