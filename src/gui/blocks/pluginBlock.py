import os

from PySide6.QtCore import QSize, Signal
from PySide6.QtGui import QPixmap, Qt
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel

from osop.filehandler import FileHandler
from plugins.pluginInfo import PluginInfo

# Reps a plugin
class PluginBlock(QWidget):
    clicked = Signal(str)
    right_click = Signal(tuple, str)

    def __init__(self, uid):
        super().__init__()
        self.myLayout = QHBoxLayout()
        self.uid = uid
        info = PluginInfo.info[uid]

        if info["api_version"] == "0.1":
            image_url = info["image_url"]
            if image_url == "":
                image_url = os.path.join("img", "x.png") # no image, use default

            else:
                image_url = os.path.join(FileHandler.PLUGINS, self.uid, *image_url.split("/")) # use path relative to the plugin
            title = info["name"]
            author = info["author"]
            version = info["version"]
            type = f"Type: {", ".join(["Plugin" if info["has_plugin"] else "", "Style" if info["has_style"] else ""])}" # type of plugin (style or code)
            self.image = QLabel() # plugin image
            self.image.setPixmap(QPixmap(image_url))
            self.image.setMaximumSize(QSize(64, 64))
            self.image.setScaledContents(True)

            self.info = QLabel() # plugin data
            self.info.setText(f"{title} - {author}\n{type}\nAPI Version: 0.1/Plugin Version: {version}")
            self.myLayout.addWidget(self.image)
            self.myLayout.addWidget(self.info)

        # make it clickable
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        self.setLayout(self.myLayout)
        for child in self.findChildren(QLabel):
            child.setCursor(Qt.PointingHandCursor)

        # make it right clickable
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pos: self.right_click.emit(pos, self.uid))

    # fire clicked slot when needed and make sure right clicks dont count as clicks
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.uid)
        elif event.button() == Qt.RightButton:
            return event.accept()
        super().mousePressEvent(event)

