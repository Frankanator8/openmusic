from PySide6.QtWidgets import QWidget, QVBoxLayout

from gui.songWidget import SongWidget
from songLibrary import SongLibrary


class SongMenu(QWidget):
    def __init__(self, osPlayer):
        super().__init__()
        self.osPlayer = osPlayer
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

        self.reload()

    def play_song(self, uid):
        self.osPlayer.play(uid)

    def reload(self):
        while self.vlayout.count():
            child = self.vlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i in SongLibrary.retrieve_songs():
            widget = SongWidget(i)
            self.vlayout.addWidget(widget)
            widget.clicked.connect(self.play_song)

