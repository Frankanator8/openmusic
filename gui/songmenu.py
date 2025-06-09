from PySide6.QtWidgets import QWidget, QVBoxLayout

from gui.songWidget import SongWidget
from songLibrary import SongLibrary


class SongMenu(QWidget):
    def __init__(self, osPlayer):
        super().__init__()
        self.osPlayer = osPlayer
        self.vlayout = QVBoxLayout()
        amt = 0
        for i in SongLibrary.retrieve_songs():
            widget = SongWidget(i)
            self.vlayout.addWidget(widget)
            widget.clicked.connect(self.play_song)
            amt += 1

        self.setLayout(self.vlayout)

    def play_song(self, uid):
        self.osPlayer.play(uid)
