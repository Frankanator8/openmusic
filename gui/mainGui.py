from PySide6.QtWidgets import *

from gui.fullPlaylistWidget import FullPlaylistWidget
from gui.leftMenu import LeftMenu
from gui.rightMenu import RightMenu


class MainGui(QWidget):
    def __init__(self, osPlayer):
        super().__init__()
        self.setWindowTitle("OpenMusic")
        self.showFullScreen()
        self.layout = QVBoxLayout()
        self.rightMenu = RightMenu(osPlayer)
        splitter = QSplitter()
        centralScrollArea = QScrollArea()

        self.layout.addWidget(splitter)
        splitter.addWidget(LeftMenu(osPlayer, centralScrollArea))
        centralScrollArea.setWidget(FullPlaylistWidget(osPlayer, "0a4543711e9448f59c43e70940d9dde8"))

        splitter.addWidget(centralScrollArea)
        splitter.addWidget(self.rightMenu)

        x = self.size().toTuple()[0]
        splitter.setSizes([x/4, 11*x/20, x/5])

        self.setLayout(self.layout)