from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenu, QMessageBox
from gui.dialogs.playlistEditor import PlaylistEditor
from gui.blocks.playlistBlock import PlaylistBlock
from gui.globalUpdater import GlobalUpdater
from util.playlist import Playlist


class PlaylistMenu(QWidget):
    def __init__(self, globalUpdater, osplayer):
        super().__init__()
        self.myLayout = QVBoxLayout()
        self.globalUpdater = globalUpdater
        self.osPlayer = osplayer
        self.reload()
        self.setLayout(self.myLayout)
        self.adjustSize()

    def set_playlist_widget(self, uid):
        self.globalUpdater.playlist_uid = uid
        self.globalUpdater.update(GlobalUpdater.CENTER_MENU)

    def reload(self):
        while self.myLayout.count():
            child = self.myLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i in Playlist.retrieve_playlists():
            widget = PlaylistBlock(i)
            widget.clicked.connect(self.set_playlist_widget)
            widget.right_click.connect(self.open_context_plwidget)
            self.myLayout.addWidget(widget)

        self.updateGeometry()

    def edit_playlist(self, playlist):
        dialog = PlaylistEditor(self, self.globalUpdater, self.osPlayer, playlist)
        dialog.exec()

    def open_context_plwidget(self, pos, uid):
        playlist = Playlist.load(uid)
        def toggle_shuffle():
            playlist.shuffle = not playlist.shuffle
            playlist.save()
            self.globalUpdater.update(GlobalUpdater.CENTER_MENU)
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
            self.globalUpdater.playlist_uid = ""
            self.globalUpdater.update(GlobalUpdater.CENTER_MENU | GlobalUpdater.PLAYLIST_MENU)
            self.osPlayer.stop()

    def check_update(self):
        if self.globalUpdater.check_and_unset(GlobalUpdater.PLAYLIST_MENU):
            self.reload()