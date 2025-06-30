from PIL.ImageStat import Global
from PySide6.QtWidgets import *

from gui.centerComponents.centerScroll import CenterScrollArea
from gui.centerComponents.fullPlaylistDisplay import FullPlaylistDisplay
from gui.globalUpdater import GlobalUpdater
from gui.leftComponents.leftMenu import LeftMenu
from gui.rightComponents.rightMenu import RightMenu


class MainGui(QWidget):
    def __init__(self, osPlayer):
        super().__init__()
        self.setWindowTitle("OpenMusic")
        self.showFullScreen()
        self.layout = QVBoxLayout()
        self.globalUpdater = GlobalUpdater()

        self.leftMenu = LeftMenu(self.globalUpdater, osPlayer)
        self.center = CenterScrollArea(self.globalUpdater, osPlayer)
        self.rightMenu = RightMenu(osPlayer)

        self.splitter = QSplitter()
        self.layout.addWidget(self.splitter)

        self.splitter.addWidget(self.leftMenu)
        self.splitter.addWidget(self.center)
        self.splitter.addWidget(self.rightMenu)

        x = self.size().toTuple()[0]
        self.splitter.setSizes([x/4, 11*x/20, x/5])

        self.setLayout(self.layout)

    def update_subs(self):
        self.leftMenu.playlistMenu.check_update()
        self.leftMenu.songMenu.check_update()
        self.center.check_update()
        self.rightMenu.update_gui()