from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLayout

from filehandler import FileHandler


class PlaylistWidget(QWidget):
    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        image_url, title = self.load_data()

        self.layout = QHBoxLayout()
        self.albumCover = QLabel()
        self.albumCover.setPixmap(QPixmap(image_url))
        self.albumCover.setMaximumSize(QSize(64, 64))
        self.albumCover.setScaledContents(True)

        self.title = QLabel()
        self.title.setText(title)
        self.layout.addWidget(self.albumCover)

        textLayout = QVBoxLayout()
        textLayout.addWidget(self.title)
        self.layout.addLayout(textLayout)
        self.setLayout(self.layout)

    def load_data(self):
        image_url = f"{FileHandler.PLAYLIST_DATA}/{self.uid}.png"
        with open(f"{FileHandler.PLAYLIST_DATA}/{self.uid}.txt") as f:
            title = f.readline()

        return image_url, title