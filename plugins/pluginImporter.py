import os
import shutil
from pathlib import Path
from zipfile import ZipFile

from osop.filehandler import FileHandler
from plugins.pluginInfo import PluginInfo
from util.songs import Songs


class PluginImporter:
    @classmethod
    def import_plugin(cls, url):
        path = Path(url)
        if path.exists():
            uid = Songs.make_uid()
            if path.is_dir():
                shutil.copytree(url, str(os.path.join(FileHandler.PLUGINS, uid)))

            elif path.suffix[0] == ".zip":
                with ZipFile(url) as zipped:
                    zipped.extractall(str(os.path.join(FileHandler.PLUGINS, uid)))

            if PluginInfo.is_valid_plugin(uid):
                PluginInfo.to_process.append(uid)
                PluginInfo.get_info(uid)
