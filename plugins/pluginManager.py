# declarations.txt - api version number, title, author, plugin version, dependencies, APICommunicator file
# api communicator - mainGui, osPlayer, update_timer (all under initialize), class loader
import importlib
import inspect
import os
import sys
from pathlib import Path

from gui.blocks.playlistBlock import PlaylistBlock
from gui.blocks.songBlock import SongBlock
from gui.centerComponents.centerScroll import CenterScrollArea
from gui.centerComponents.fullPlaylistDisplay import FullPlaylistDisplay
from gui.dialogs.playlistEditor import PlaylistEditor
from gui.dialogs.songEditor import SongEditor
from gui.globalUpdater import GlobalUpdater
from gui.leftComponents.leftMenu import LeftMenu
from gui.leftComponents.playlistmenu import PlaylistMenu
from gui.leftComponents.songmenu import SongMenu
from gui.mainGui import MainGui
from gui.rightComponents.rightMenu import RightMenu
from osop.filehandler import FileHandler
from osop.osplayer import OSPlayer
from plugins.opapi import OpenMusicClient
from util.playlist import Playlist
from util.songs import Songs


class PluginManager:
    def __init__(self):
        self.plugins = []
        self.clients = {}
        self.payload = {}

    def discover_plugins(self):
        self.plugins = []
        for folder in os.listdir(FileHandler.PLUGINS):
            if os.path.isdir(folder):
                if os.path.exists(os.path.join(folder, "declarations.txt")) and os.path.exists(os.path.join(folder, "opapi.py")):
                    self.plugins.append(Path(folder).stem)

    def create_payload(self, app, osPlayer, mainGui):
        self.payload = {
            "app": app,
            "os_player": osPlayer,
            "main_gui": mainGui,
            "classes": {
                "Playlist": Playlist,
                "OSPlayer": OSPlayer,
                "MainGui": MainGui,
                "GlobalUpdater": GlobalUpdater,
                "RightMenu": RightMenu,
                "LeftMenu": LeftMenu,
                "PlaylistMenu": PlaylistMenu,
                "SongMenu": SongMenu,
                "PlaylistEditor": PlaylistEditor,
                "SongEditor": SongEditor,
                "CenterScrollArea": CenterScrollArea,
                "FullPlaylistDisplay": FullPlaylistDisplay,
                "PlaylistBlock": PlaylistBlock,
                "SongBlock": SongBlock
            },
            "statics": {
                "FileHandler": FileHandler,
                "Songs": Songs,
            }
        }


    def load_plugins(self):
        if self.payload is not {}:
            for plugin in self.plugins:
                plugin_dir = os.path.join(FileHandler.PLUGINS, plugin)
                sys.path.insert(0, str(plugin_dir))

                try:
                    opapi = importlib.import_module("opapi")
                    payload = {}
                    for name, obj in inspect.getmembers(opapi):
                        if inspect.isclass(obj) and issubclass(obj, OpenMusicClient):
                            plugin_client = obj(**payload)
                            self.clients[plugin] = plugin_client

                except Exception as e:
                    print(str(e))

                if str(plugin_dir) in sys.path:
                    sys.path.remove(str(plugin_dir))


    def pre_gui_creation(self):
        for plugin in self.clients.values():
            plugin.pre_gui_creation()

    def post_gui_creation(self):
        for plugin in self.clients.values():
            plugin.post_gui_creation()

    def timer_update(self):
        for plugin in self.clients.values():
            plugin.timer_update()

