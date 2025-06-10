from PySide6.QtCore import QSize
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout

from gui.songWidget import SongWidget
from playlist import Playlist


class FullPlaylistWidget(QWidget):
    def __init__(self, osplayer, uid):
        super().__init__()
        self.osPlayer = osplayer
        self.playlist = Playlist.load(uid)
        self.myLayout = QVBoxLayout()

        hLayout = QHBoxLayout()
        image = QLabel()
        image.setPixmap(QPixmap(self.playlist._image_url))
        image.setMaximumSize(QSize(256, 256))
        image.setScaledContents(True)
        hLayout.addWidget(image)

        vLayout = QVBoxLayout()
        title = QLabel()
        title.setText(self.playlist._name)
        shuffle = QLabel()
        shuffle.setText(f"Shuffle: {'ON' if self.playlist._shuffle else 'OFF'}")
        vLayout.addWidget(title)
        vLayout.addWidget(shuffle)
        hLayout.addLayout(vLayout)

        self.myLayout.addLayout(hLayout)
        self.uidToIndex = {}
        for index, song in enumerate(self.playlist._songs):
            widget = SongWidget(song)
            widget.clicked.connect(self.play_song_in_playlist)
            self.myLayout.addWidget(widget)
            self.uidToIndex[song] = index

        self.setLayout(self.myLayout)
        self.myLayout.update()


    def play_song_in_playlist(self, uid):
        self.playlist.set_guaranteed_next(self.uidToIndex[uid])
        self.osPlayer.play(self.playlist)

