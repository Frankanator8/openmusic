import os

from osop.filehandler import FileHandler


class PluginInfo:
    plugins = []
    info = {}

    @classmethod
    def get_info(cls, plugin):
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
