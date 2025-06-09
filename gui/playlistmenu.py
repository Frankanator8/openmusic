from PySide6.QtWidgets import QWidget, QVBoxLayout

from gui.playlistWidget import PlaylistWidget
from playlistLibrary import PlaylistLibrary


class PlaylistMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.vlayout = QVBoxLayout()
        amt = 0
        for i in PlaylistLibrary.retrieve_playlists():
            self.vlayout.addWidget(PlaylistWidget(i))
            amt += 1

        self.setLayout(self.vlayout)