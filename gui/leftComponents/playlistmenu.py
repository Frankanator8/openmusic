from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenu, QMessageBox

from gui.centerComponents.fullPlaylistDisplay import FullPlaylistDisplay
from gui.dialogs.playlistEditor import PlaylistEditor
from gui.blocks.playlistBlock import PlaylistBlock
from util.playlist import Playlist
from library.playlistLibrary import PlaylistLibrary


class PlaylistMenu(QWidget):
    def __init__(self, osplayer, centralScrollArea):
        super().__init__()
        self.vlayout = QVBoxLayout()
        self.centralScrollArea = centralScrollArea
        self.osPlayer = osplayer
        self.reload()
        self.setLayout(self.vlayout)
        self.adjustSize()

    def set_playlist_widget(self, uid):
        self.centralScrollArea.widget().deleteLater()
        self.centralScrollArea.setWidget(FullPlaylistDisplay(self.osPlayer, uid, self))

    def reload(self):
        while self.vlayout.count():
            child = self.vlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i in PlaylistLibrary.retrieve_playlists():
            widget = PlaylistBlock(i)
            widget.clicked.connect(self.set_playlist_widget)
            widget.right_click.connect(self.open_context_plwidget)
            self.vlayout.addWidget(widget)

        self.updateGeometry()

    def edit_playlist(self, playlist):
        dialog = PlaylistEditor(playlist, self, self.osPlayer, self.centralScrollArea)
        dialog.exec()

    def open_context_plwidget(self, pos, uid):
        playlist = Playlist.load(uid)
        def toggle_shuffle():
            playlist.shuffle = not playlist.shuffle
            playlist.save()
            self.centralScrollArea.widget().deleteLater()
            self.centralScrollArea.setWidget(FullPlaylistDisplay(self.osPlayer, playlist.uid, self))
        menu = QMenu(self)

        # Add actions to the menu
        rename_action = QAction("Edit", self)
        rename_action.triggered.connect(lambda: self.edit_playlist(playlist))
        menu.addAction(rename_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.deletePlaylist(playlist))
        menu.addAction(delete_action)

        # Add separator if needed
        menu.addSeparator()

        # Add more actions as needed
        info_action = QAction("Toggle Shuffle", self)
        info_action.triggered.connect(toggle_shuffle)
        menu.addAction(info_action)

        sender_widget = self.sender()
        if isinstance(sender_widget, PlaylistBlock):
            # Map the position from the sender widget to global coordinates
            global_pos = sender_widget.mapToGlobal(pos)
            menu.exec(global_pos)
        else:
            # Fallback to current behavior if sender isn't available
            menu.exec(self.mapToGlobal(pos))

    def deletePlaylist(self, playlist):
        message = QMessageBox.critical(self, "Really delete?", f"Really delete {playlist.name}? This action is irreversible", QMessageBox.Ok | QMessageBox.Cancel)
        if message == QMessageBox.Ok:
            playlist.delete()
            self.reload()
            if self.centralScrollArea.widget().playlist.uid == playlist.uid:
                self.centralScrollArea.setWidget(FullPlaylistDisplay(self.osPlayer, "", self))

            self.osPlayer.toggle_play_pause()
            self.osPlayer.player = None