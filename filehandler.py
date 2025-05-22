import pathlib
import os

class FileHandler:
    # Path to the user's home directory
    _app_support_path = os.path.join(pathlib.Path.home(), "Library", "Application Support", "OpenMusic")
    TEMP_VID_STORAGE = os.path.join(_app_support_path, "tmp_videos")
    AUDIOS = os.path.join(_app_support_path, "audio")
    SONG_DATA = os.path.join(_app_support_path, "songdata")
    PLAYLIST_DATA = os.path.join(_app_support_path, "playlistdata")
