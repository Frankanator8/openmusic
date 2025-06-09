from PySide6.QtWidgets import QWidget, QVBoxLayout

from gui.songWidget import SongWidget
from songLibrary import SongLibrary


class SongMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.vlayout = QVBoxLayout()
        amt = 0
        for i in SongLibrary.retrieve_songs():
            self.vlayout.addWidget(SongWidget(i))
            amt += 1

        self.setLayout(self.vlayout)
