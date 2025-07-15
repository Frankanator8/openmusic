from PySide6.QtWidgets import QScrollArea

from gui.centerComponents.fullPlaylistDisplay import FullPlaylistDisplay
from gui.globalUpdater import GlobalUpdater

# Describes the central area. Is by default scrollable
class CenterScrollArea(QScrollArea):
    def __init__(self, globalUpdater, osPlayer):
        super().__init__()
        self.globalUpdater = globalUpdater
        self.osPlayer = osPlayer
        self.fullDisplayWidget = FullPlaylistDisplay(self.osPlayer, self.globalUpdater.playlist_uid, "")
        self.setWidget(self.fullDisplayWidget)

    # check if we need to update the center menu by replacing center widget. Note this isn't a reload
    def check_update(self):
        if self.globalUpdater.check_and_unset(GlobalUpdater.CENTER_MENU):
            self.widget().deleteLater()
            self.takeWidget()
            self.fullDisplayWidget = FullPlaylistDisplay(self.globalUpdater, self.osPlayer, self.globalUpdater.playlist_uid)
            self.setWidget(self.fullDisplayWidget)