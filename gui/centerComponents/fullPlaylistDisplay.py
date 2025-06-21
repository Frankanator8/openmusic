from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy
from gui.blocks.songBlock import SongBlock
from gui.dialogs.playlistEditor import PlaylistEditor
from util.playlist import Playlist


class FullPlaylistDisplay(QWidget):
    def __init__(self, globalUpdater, osplayer, uid):
        super().__init__()
        self.osPlayer = osplayer
        self.globalUpdater = globalUpdater
        self.myLayout = QVBoxLayout()
        self.uid = uid

        if uid != "":
            self.playlist = Playlist.load(uid)
            hLayout = QHBoxLayout()
            image = QLabel()
            image.setPixmap(QPixmap(self.playlist.image_url))
            image.setMaximumSize(QSize(256, 256))
            image.setScaledContents(True)
            hLayout.addWidget(image)

            vLayout = QVBoxLayout()
            vLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            title = QLabel()
            title.setText(self.playlist.name)
            shuffle = QLabel()
            shuffle.setText(f"Shuffle: {'ON' if self.playlist.shuffle else 'OFF'}")
            button = QPushButton()
            button.setText("Edit Playlist")
            button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            button.clicked.connect(self.edit_curr_playlist)

            vLayout.addWidget(title)
            vLayout.addWidget(shuffle)
            hLayout.addLayout(vLayout)
            vLayout.addWidget(button)

            self.myLayout.addLayout(hLayout)
            self.uidToIndex = {}
            for index, song in enumerate(self.playlist.songs):
                widget = SongBlock(song)
                widget.clicked.connect(self.play_song_in_playlist)

                self.myLayout.addWidget(widget)
                self.uidToIndex[song] = index

        else:
            label = QLabel("Choose a playlist in your Playlist Library to play (scroll and click on the row), or choose a song to play from your Song Library (scroll and click on the row).")
            label.setWordWrap(True)
            self.myLayout.addWidget(label)

        self.setLayout(self.myLayout)
        self.myLayout.update()


    def play_song_in_playlist(self, uid):
        self.playlist.set_guaranteed_next(self.uidToIndex[uid])
        self.osPlayer.play(self.playlist)

    def edit_curr_playlist(self):
        dialog = PlaylistEditor(self, self.globalUpdater, self.playlist, self.osPlayer)
        dialog.exec()


