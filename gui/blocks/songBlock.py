from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from osop.filehandler import FileHandler


class SongBlock(QWidget):
    clicked = Signal(str)
    right_click = Signal(tuple, str)

    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        image_url, title, artist, album = self.load_data()

        self.layout = QHBoxLayout()
        self.albumCover = QLabel()
        self.albumCover.setPixmap(QPixmap(image_url))
        self.albumCover.setMaximumSize(QSize(64, 64))
        self.albumCover.setScaledContents(True)

        self.title = QLabel()
        self.title.setText(title)
        self.artistAndAlbum = QLabel()
        self.artistAndAlbum.setText(f"{artist} ({album})")
        self.layout.addWidget(self.albumCover)

        textLayout = QVBoxLayout()
        textLayout.addWidget(self.title)
        textLayout.addWidget(self.artistAndAlbum)
        self.layout.addLayout(textLayout)
        self.setLayout(self.layout)

        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        for child in self.findChildren(QLabel):
            child.setCursor(Qt.PointingHandCursor)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pos: self.right_click.emit(pos, self.uid))


    def load_data(self):
        image_url = f"{FileHandler.SONG_DATA}/{self.uid}.png"
        with open(f"{FileHandler.SONG_DATA}/{self.uid}.txt") as f:
            title = f.readline().strip()
            artist = f.readline().strip()
            album = f.readline().strip()

        return image_url, title, artist, album

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.uid)
        elif event.button() == Qt.RightButton:
            return event.accept()
        super().mousePressEvent(event)