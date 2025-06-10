from PySide6.QtWidgets import QWidget, QVBoxLayout

from gui.fullPlaylistWidget import FullPlaylistWidget
from gui.playlistWidget import PlaylistWidget
from playlistLibrary import PlaylistLibrary


class PlaylistMenu(QWidget):
    def __init__(self, osplayer, centralScrollArea):
        super().__init__()
        self.vlayout = QVBoxLayout()
        self.centralScrollArea = centralScrollArea
        self.osPlayer = osplayer
        amt = 0
        for i in PlaylistLibrary.retrieve_playlists():
            widget = PlaylistWidget(i)
            widget.clicked.connect(self.set_playlist_widget)
            self.vlayout.addWidget(widget)
            amt += 1

        self.setLayout(self.vlayout)

    def set_playlist_widget(self, uid):
        self.centralScrollArea.setWidget(FullPlaylistWidget(self.osPlayer, uid))