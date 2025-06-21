from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from util.songs import Songs
from osop.filehandler import FileHandler


class SongBlock(QWidget):
    clicked = Signal(str)
    right_click = Signal(tuple, str)

    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        image_url, _, title, artist, album = Songs.load_song_data(self.uid)

        self.myLayout = QHBoxLayout()

        self.albumCover = QLabel()
        self.albumCover.setPixmap(QPixmap(image_url))
        self.albumCover.setMaximumSize(QSize(64, 64))
        self.albumCover.setScaledContents(True)
        self.myLayout.addWidget(self.albumCover)

        self.title = QLabel()
        self.title.setText(title)
        self.artistAndAlbum = QLabel()
        self.artistAndAlbum.setText(f"{artist} ({album})")
        textLayout = QVBoxLayout()
        textLayout.addWidget(self.title)
        textLayout.addWidget(self.artistAndAlbum)

        self.myLayout.addLayout(textLayout)
        self.setLayout(self.myLayout)

        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        for child in self.findChildren(QLabel):
            child.setCursor(Qt.PointingHandCursor)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pos: self.right_click.emit(pos, self.uid))


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.uid)
        elif event.button() == Qt.RightButton:
            return event.accept()
        super().mousePressEvent(event)