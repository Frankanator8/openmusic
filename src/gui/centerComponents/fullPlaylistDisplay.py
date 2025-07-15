from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QPushButton, QSizePolicy
from gui.blocks.songBlock import SongBlock
from gui.dialogs.playlistEditor import PlaylistEditor
from util.playlist import Playlist

# Displays all songs and data of a playlist
class FullPlaylistDisplay(QWidget):
    def __init__(self, globalUpdater, osPlayer, uid):
        super().__init__()
        self.osPlayer = osPlayer
        self.globalUpdater = globalUpdater
        self.myLayout = QVBoxLayout()
        self.uid = uid

        # There is an active playlist
        if uid != "":
            # show playlist cover image
            self.playlist = Playlist.load(uid)
            self.headerLayout = QHBoxLayout()
            self.playlistImage = QLabel()
            self.playlistImage.setPixmap(QPixmap(self.playlist.image_url))
            self.playlistImage.setMaximumSize(QSize(256, 256))
            self.playlistImage.setScaledContents(True)
            self.headerLayout.addWidget(self.playlistImage)

            # show all info about playlist and provide entry to edit said playlist
            self.infoLayout = QVBoxLayout()
            self.infoLayout.setAlignment(Qt.AlignmentFlag.AlignLeft)
            self.title = QLabel()
            self.title.setText(self.playlist.name)
            self.shuffle = QLabel()
            self.shuffle.setText(f"Shuffle: {'ON' if self.playlist.shuffle else 'OFF'}")
            self.editButton = QPushButton()
            self.editButton.setText("Edit Playlist")
            self.editButton.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
            self.editButton.clicked.connect(self.edit_curr_playlist)

            self.infoLayout.addWidget(self.title)
            self.infoLayout.addWidget(self.shuffle)
            self.infoLayout.addWidget(self.editButton)
            self.headerLayout.addLayout(self.infoLayout)

            # add all songs in playlist
            self.myLayout.addLayout(self.headerLayout)
            self.uidToIndex = {}
            for index, song in enumerate(self.playlist.songs):
                widget = SongBlock(song)
                widget.clicked.connect(self.play_song_in_playlist)

                self.myLayout.addWidget(widget)
                self.uidToIndex[song] = index

        # there is no active playlist
        else:
            self.noneLabel = QLabel("Choose a playlist in your Playlist Library to play (scroll and click on the row), or choose a song to play from your Song Library (scroll and click on the row).")
            self.noneLabel.setWordWrap(True)
            self.myLayout.addWidget(self.noneLabel)

        self.setLayout(self.myLayout)
        self.myLayout.update()

    # play a certain song in the playlist
    def play_song_in_playlist(self, uid):
        self.playlist.set_guaranteed_next(self.uidToIndex[uid])
        self.osPlayer.play(self.playlist)

    # open playlist editor dialog
    def edit_curr_playlist(self):
        dialog = PlaylistEditor(self, self.globalUpdater, self.osPlayer, self.playlist)
        dialog.exec()


