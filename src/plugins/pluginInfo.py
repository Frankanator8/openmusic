import os
import shutil
from pathlib import Path
from zipfile import ZipFile

from osop.filehandler import FileHandler
from util.songs import Songs

# Stores all info about plugins but has no info on them

class PluginInfo:
    plugins = []
    info = {}
    # to_process is accessed by PluginManager
    to_process = []
    to_delete = []
    order = []
    enabled = {}
    reload_styles = False

    # Sees if a uid has a valid plugin in files
    @classmethod
    def is_valid_plugin(cls, plugin):
        return os.path.exists(os.path.join(FileHandler.PLUGINS, plugin, "declarations.txt"))

    # Gets info about a plugin from declarations.txt
    @classmethod
    def get_info(cls, plugin):
        if cls.is_valid_plugin(plugin):
            info = {}
            with open(str(os.path.join(FileHandler.PLUGINS, plugin, "declarations.txt"))) as f:
                version = f.readline().strip()
                info["api_version"] = version
                if version == "0.1":
                    info["name"] = f.readline().strip()
                    info["author"] = f.readline().strip()
                    info["version"] = f.readline().strip()
                    info["image_url"] = f.readline().strip()
                    info["has_plugin"] = True if f.readline().strip()[0] == "y" else False
                    info["has_style"] = True if f.readline().strip()[0] == "y" else False
                    info["dependencies"] = f.readline().strip().split()

            cls.info[plugin] = info

    @classmethod
    def get_plugins_info(cls):
        for plugin in cls.plugins:
            cls.get_info(plugin)

    # Loads the saved state of plugins (e.g. application order and which are enabled)
    @classmethod
    def load_save(cls):
        tempOrder = {}
        if os.path.exists(os.path.join(FileHandler.PLUGINS, "prefs.txt")):
            with open(os.path.join(FileHandler.PLUGINS, "prefs.txt")) as f:
                lines = f.readlines()

            version = int(lines[0])
            if version == 0:
                count = 0
                for line in lines[1:]:
                    if line[0] == "e":
                        uid = line.split()[1]
                        cls.enabled[uid] = True

                    elif line[0] == "d":
                        uid = line.split()[1]
                        cls.enabled[uid] = False

                    elif line[0] == "o":
                        uid = line.split()[1]
                        order = int(line.split()[2])
                        tempOrder[order] = uid
                        count += 1

                up = 0
                registered = 0
                while registered < count:
                    if up in tempOrder:
                        cls.order.append(tempOrder[up])
                        registered += 1
                    up += 1

        else:
            with open(os.path.join(FileHandler.PLUGINS, "prefs.txt"), "w") as f:
                f.write("0")

    # Saves the enabled/application order file
    @classmethod
    def save(cls):
        data = "0"
        for key, value in cls.enabled.items():
            data = f"{data}\n{"e" if value else "d"} {key}"

        for index, item in enumerate(cls.order):
            data=f"{data}\no {item} {index}"

        with open(os.path.join(FileHandler.PLUGINS, "prefs.txt"), "w") as f:
            f.write(data)

    # Gets whether a plugin is enabled. If it isn't registered, return False
    @classmethod
    def get_enabled(cls, uid):
        if uid in cls.enabled.keys():
            return cls.enabled[uid]

        else:
            cls.enabled[uid] = False
            cls.save()
            return False

    # Move plugins from their source into applicable folder in OpenMusic
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

            if cls.is_valid_plugin(uid):
                cls.to_process.append(uid)
                cls.plugins.append(uid)
                cls.enabled[uid] = False
                cls.get_info(uid)
                cls.save()

    # Deletes a plugin (from memory and storage)
    @classmethod
    def delete_plugin(cls, uid):
        cls.plugins.remove(uid)
        del cls.info[uid]
        if uid in cls.to_process:
            cls.to_process.remove(uid)
        if uid in cls.order:
            cls.order.remove(uid)
        del cls.enabled[uid]
        cls.save()
        cls.to_delete.append(uid)

    # Reload all styles by signalling to PluginManager
    @classmethod
    def reload_style(cls):
        cls.reload_styles = True
