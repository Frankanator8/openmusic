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

        self.leftMenu = LeftMenu(osPlayer, self.globalUpdater)
        self.center = CenterScrollArea(osPlayer, self.globalUpdater)
        self.rightMenu = RightMenu(osPlayer)

        splitter = QSplitter()
        self.layout.addWidget(splitter)

        splitter.addWidget(self.leftMenu)
        splitter.addWidget(self.center)
        splitter.addWidget(self.rightMenu)

        x = self.size().toTuple()[0]
        splitter.setSizes([x/4, 11*x/20, x/5])

        self.setLayout(self.layout)

    def update_subs(self):
        self.leftMenu.playlistMenu.check_update()
        self.leftMenu.songMenu.check_update()
        self.center.check_update()
        self.rightMenu.update_gui()