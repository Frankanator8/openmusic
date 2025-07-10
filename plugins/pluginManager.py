# declarations.txt - api version number, title, author, plugin version, dependencies, APICommunicator file
# api communicator - mainGui, osPlayer, update_timer (all under initialize), class loader
import importlib
import inspect
import os
import shutil
import sys
from pathlib import Path

from PySide6 import QtWidgets

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
from plugins.pluginInfo import PluginInfo
from util.playlist import Playlist
from util.songs import Songs


class PluginManager:
    clients = {}
    payload = {}

    @classmethod
    def discover_plugins(cls):
        PluginInfo.plugins = []
        for folder in os.listdir(FileHandler.PLUGINS):
            if os.path.isdir(os.path.join(FileHandler.PLUGINS, folder)):
                if os.path.exists(os.path.join(FileHandler.PLUGINS, folder, "declarations.txt")):
                    PluginInfo.plugins.append(folder)

    @classmethod
    def create_payload(cls, app, osPlayer, mainGui):
        cls.payload = {
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
                "Songs": Songs
            }
        }

    @classmethod
    def load_styles(cls):
        for plugin in PluginInfo.order:
            if PluginInfo.get_enabled(plugin):
                if os.path.exists(os.path.join(FileHandler.PLUGINS, plugin, "style.qss")):
                    with open(os.path.join(FileHandler.PLUGINS, plugin, "style.qss")) as f:
                        data = f.read()
                        cls.payload["app"].setStyleSheet(data)

                if os.path.exists(os.path.join(FileHandler.PLUGINS, plugin, "style.oss")):
                    with open(os.path.join(FileHandler.PLUGINS, plugin, "style.oss")) as f:
                        data = f.read()

                    error = False
                    scanType = 0
                    data = ""
                    appliedWidget = ""

                    for char in data:
                        if char == "{":
                            if scanType == 0:
                                appliedWidget = data.strip()
                                data = ""
                                scanType = 1

                            else:
                                error = True
                                break

                        elif char == "}":
                            if scanType == 1:
                                error = True
                                break

                            else:
                                hierarchy = appliedWidget.split(".")
                                currWidget = cls.payload["main_gui"]
                                for i in hierarchy:
                                    if hasattr(currWidget, i):
                                        currWidget = getattr(currWidget, i)

                                    else:
                                        error = True

                                currWidget.setStyleSheet(data.strip())
                                data = ""

                        else:
                            data = f"{data}{char}"

    @classmethod
    def load_plugins(cls):
        if cls.payload is not {}:
            for plugin in PluginInfo.plugins:
                cls.load_plugin(plugin)

    @classmethod
    def load_plugin(cls, plugin):
        plugin_dir = os.path.join(FileHandler.PLUGINS, plugin)
        sys.path.insert(0, str(plugin_dir))

        try:
            if PluginInfo.get_enabled(plugin):
                if os.path.exists(os.path.join(FileHandler.PLUGINS, plugin, "opapi.py")):
                    opapi = importlib.import_module("opapi")
                    payload = cls.payload
                    for name, obj in inspect.getmembers(opapi):
                        if inspect.isclass(obj) and obj.__name__ == "OpenMusicClient": #issubclass(obj, OpenMusicClient):
                            plugin_client = obj(**payload)
                            cls.clients[plugin] = plugin_client

        except Exception as e:
            print(str(e))

        if str(plugin_dir) in sys.path:
            sys.path.remove(str(plugin_dir))
    
    @classmethod
    def on_launch(cls):
        for uid, plugin in cls.clients.items():
            if PluginInfo.get_enabled(uid):
                plugin.on_launch()
    
    @classmethod
    def timer_update(cls):
        if len(PluginInfo.to_process) > 0:
            uid = PluginInfo.to_process.pop(0)
            cls.load_plugin(uid)

        if len(PluginInfo.to_delete) > 0:
            uid = PluginInfo.to_delete.pop(0)
            shutil.rmtree(os.path.join(FileHandler.PLUGINS, uid))
            try:
                del cls.clients[uid]

            except KeyError:
                pass

        if PluginInfo.reload_styles:
            PluginInfo.reload_styles = False
            cls.reload_all()

        for uid, plugin in cls.clients.items():
            if PluginInfo.get_enabled(uid):
                plugin.timer_update()

    @classmethod
    def reload_all(cls):
        queue = []
        queue.append(cls.payload["app"])
        while len(queue) > 0:
            next = queue.pop(0)
            next.setStyleSheet(None)
            for child in next.findChildren(QtWidgets.QWidget):
                queue.append(child)

        cls.load_styles()


