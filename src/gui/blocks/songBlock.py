from PySide6.QtCore import QSize, Qt, Signal
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout

from util.songs import Songs

# Represents a song
class SongBlock(QWidget):
    # slots for when it is clicked/right clicked
    clicked = Signal(str)
    right_click = Signal(tuple, str)

    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        image_url, _, title, artist, album = Songs.load_song_data(self.uid)

        self.myLayout = QHBoxLayout()
        # album cover image
        self.albumCover = QLabel()
        self.albumCover.setPixmap(QPixmap(image_url))
        self.albumCover.setMaximumSize(QSize(64, 64))
        self.albumCover.setScaledContents(True)
        self.myLayout.addWidget(self.albumCover)

        # song title, artist, album
        self.title = QLabel()
        self.title.setText(title)
        self.artistAndAlbum = QLabel()
        self.artistAndAlbum.setText(f"{artist} ({album})")
        self.textLayout = QVBoxLayout()
        self.textLayout.addWidget(self.title)
        self.textLayout.addWidget(self.artistAndAlbum)

        self.myLayout.addLayout(self.textLayout)
        self.setLayout(self.myLayout)

        # make it clickable
        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        for child in self.findChildren(QLabel):
            child.setCursor(Qt.PointingHandCursor)

        # make it right clickable
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(lambda pos: self.right_click.emit(pos, self.uid))

    # slots for when it is clicked/right clicked
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.uid)
        elif event.button() == Qt.RightButton:
            return event.accept()
        super().mousePressEvent(event)