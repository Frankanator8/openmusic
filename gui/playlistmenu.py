from PySide6.QtWidgets import QWidget, QVBoxLayout, QScrollArea

from gui.fullPlaylistWidget import FullPlaylistWidget
from gui.playlistEditor import PlaylistEditor
from gui.playlistWidget import PlaylistWidget
from playlistLibrary import PlaylistLibrary


class PlaylistMenu(QWidget):
    def __init__(self, osplayer, centralScrollArea):
        super().__init__()
        self.vlayout = QVBoxLayout()
        self.centralScrollArea = centralScrollArea
        self.osPlayer = osplayer
        amt = 0
        self.reload()

        self.setLayout(self.vlayout)

    def set_playlist_widget(self, uid):
        self.centralScrollArea.widget().deleteLater()
        self.centralScrollArea.setWidget(FullPlaylistWidget(self.osPlayer, uid, self))

    def reload(self):
        while self.vlayout.count():
            child = self.vlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i in PlaylistLibrary.retrieve_playlists():
            widget = PlaylistWidget(i)
            widget.clicked.connect(self.set_playlist_widget)
            self.vlayout.addWidget(widget)

        self.updateGeometry()

    def edit_playlist(self, playlist):
        dialog = PlaylistEditor(playlist, self, self.osPlayer, self.centralScrollArea)
        dialog.exec()