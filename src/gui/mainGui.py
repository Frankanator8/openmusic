import sys

from PySide6.QtCore import QTimer
from PySide6.QtWidgets import *

from gui.centerComponents.centerScroll import CenterScrollArea
from gui.centerComponents.fullPlaylistDisplay import FullPlaylistDisplay
from gui.globalUpdater import GlobalUpdater
from gui.leftComponents.leftMenu import LeftMenu
from gui.rightComponents.rightMenu import RightMenu


class MainGui(QWidget):
    def __init__(self, osPlayer):
        super().__init__()
        # Set window properties
        self.setWindowTitle("OpenMusic")
        if sys.platform == "darwin":
            self.showFullScreen()

        else:
            QTimer.singleShot(0, self.showMaximized)

        # Create layout
        self.myLayout = QVBoxLayout()

        # Create updater
        self.globalUpdater = GlobalUpdater()

        # Create sub menus
        self.leftMenu = LeftMenu(self.globalUpdater, osPlayer)
        self.center = CenterScrollArea(self.globalUpdater, osPlayer)
        self.rightMenu = RightMenu(osPlayer)

        # Create organization for submenus
        self.splitter = QSplitter()
        self.myLayout.addWidget(self.splitter)

        self.splitter.addWidget(self.leftMenu)
        self.splitter.addWidget(self.center)
        self.splitter.addWidget(self.rightMenu)

        # Appropriately size splitter
        x = self.size().toTuple()[0]
        self.splitter.setSizes([x/4, 11*x/20, x/5])

        self.setLayout(self.myLayout)

    # Called every few seconds so all submenus update
    def update_subs(self):
        self.leftMenu.playlistMenu.check_update()
        self.leftMenu.songMenu.check_update()
        self.center.check_update()
        self.rightMenu.update_gui()