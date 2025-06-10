from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QScrollArea, QLabel

from gui.playlistmenu import PlaylistMenu
from gui.songWidget import SongWidget
from gui.songmenu import SongMenu


class LeftMenu(QWidget):
    def __init__(self, osPlayer, centralScrollArea):
        super().__init__()
        self.layout = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)


        self.topWidget = QWidget()
        topMenu = QVBoxLayout()
        top = QLabel()
        top.setText("Song Library")
        scrollArea = QScrollArea()
        scrollArea.setWidget(SongMenu(osPlayer))
        topMenu.addWidget(top)
        topMenu.addWidget(scrollArea)
        self.topWidget.setLayout(topMenu)
        splitter.addWidget(self.topWidget)

        self.bottomWidget = QWidget()
        bottomMenu = QVBoxLayout()
        top = QLabel()
        top.setText("Playlists")
        scrollArea = QScrollArea()
        scrollArea.setWidget(PlaylistMenu(osPlayer, centralScrollArea))
        bottomMenu.addWidget(top)
        bottomMenu.addWidget(scrollArea)
        self.bottomWidget.setLayout(bottomMenu)
        splitter.addWidget(self.bottomWidget)

        self.layout.addWidget(splitter)
        self.setLayout(self.layout)