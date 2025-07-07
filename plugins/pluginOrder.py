import os.path

from osop.filehandler import FileHandler


class PluginOrder:
    order = []
    enabled = {}

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
            with open(os.path.join(FileHandler.PLUGINS, "prefs.txt")) as f:
                f.write("0")

    @classmethod
    def save(cls):
        data = "0"
        for key, value in cls.enabled.items():
            data = f"{data}\n{"e" if value else "d"} {key}"

        for index, item in enumerate(cls.order):
            data=f"{data}\no {item} {index}"

        with open(os.path.join(FileHandler.PLUGINS, "prefs.txt")) as f:
            f.write(data)

    @classmethod
    def get_enabled(cls, uid):
        if uid in cls.enabled.keys():
            return cls.enabled[uid]

        else:
            cls.enabled[uid] = False
            cls.save()
            return False
