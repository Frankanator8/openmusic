from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from filehandler import FileHandler


class SongWidget(QWidget):
    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        image_url, title, artist, album = self.load_data()

        self.layout = QHBoxLayout()
        self.albumCover = QLabel()
        self.albumCover.setPixmap(QPixmap(image_url))

        self.title = QLabel()
        self.title.setText(title)
        self.artistAndAlbum = QLabel()
        self.artistAndAlbum.setText(f"{artist} ({album})")
        self.layout.addWidget(self.albumCover)

        textLayout = QVBoxLayout()
        textLayout.addWidget(self.title)
        textLayout.addWidget(self.artistAndAlbum)
        # self.layout.addLayout(textLayout)

    def load_data(self):
        image_url = f"{FileHandler.SONG_DATA}/{self.uid}.png"
        with open(f"{FileHandler.SONG_DATA}/{self.uid}.txt") as f:
            title = f.readline().strip()
            artist = f.readline().strip()
            album = f.readline().strip()

        return image_url, title, artist, album