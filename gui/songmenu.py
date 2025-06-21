import os

from PySide6.QtGui import QAction
from PySide6.QtWidgets import QWidget, QVBoxLayout, QMenu, QMessageBox

from filehandler import FileHandler
from gui.fullPlaylistWidget import FullPlaylistWidget
from gui.songEditor import SongEditor
from gui.songWidget import SongWidget
from playlist import Playlist
from playlistLibrary import PlaylistLibrary
from songLibrary import SongLibrary


class SongMenu(QWidget):
    def __init__(self, osPlayer, centralScrollArea, playlistMenu):
        super().__init__()
        self.osPlayer = osPlayer
        self.centralScrollArea = centralScrollArea
        self.playlistMenu = playlistMenu
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)

        self.reload()

    def play_song(self, uid):
        self.osPlayer.play(uid)

    def reload(self):
        while self.vlayout.count():
            child = self.vlayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        for i in SongLibrary.retrieve_songs():
            widget = SongWidget(i)
            self.vlayout.addWidget(widget)
            widget.clicked.connect(self.play_song)
            widget.right_click.connect(self.open_context_sowidget)


    def open_context_sowidget(self, pos, uid):
        menu = QMenu(self)

        # Add actions to the menu
        edit_action = QAction("Edit", self)
        edit_action.triggered.connect(lambda: self.edit(uid))
        menu.addAction(edit_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.delete_song(uid))
        menu.addAction(delete_action)

        # Add separator if needed
        menu.addSeparator()

        # Add more actions as needed
        add_more = QMenu("Add to playlist", self)
        for playlist in PlaylistLibrary.retrieve_playlists():
            playlistAction = QAction(Playlist.load(playlist).name, self)
            playlistAction.triggered.connect(lambda : self.add_song_to_playlist(uid, playlist))
            add_more.addAction(playlistAction)
        menu.addMenu(add_more)

        sender_widget = self.sender()
        if isinstance(sender_widget, SongWidget):
            # Map the position from the sender widget to global coordinates
            global_pos = sender_widget.mapToGlobal(pos)
            menu.exec(global_pos)
        else:
            # Fallback to current behavior if sender isn't available
            menu.exec(self.mapToGlobal(pos))

    def delete_song(self, uid):
        message = QMessageBox.critical(self, "Really delete?", f"Really delete this song and from all playlists? This action is irreversible", QMessageBox.Ok | QMessageBox.Cancel)
        if message == QMessageBox.Ok:
            os.remove(f"{FileHandler.SONG_DATA}/{uid}.txt")
            os.remove(f"{FileHandler.AUDIOS}/{uid}.mp3")
            os.remove(f"{FileHandler.SONG_DATA}/{uid}.png")
            changed = []
            for playlist_id in PlaylistLibrary.retrieve_playlists():
                playlist = Playlist.load(playlist_id)
                if uid in playlist.songs:
                    playlist.remove_song(uid)
                    playlist.save()
                    changed.append(playlist_id)

            if self.osPlayer.uid == uid:
                self.osPlayer.toggle_play_pause()
                self.osPlayer.player = None

            if self.centralScrollArea.widget().playlist.uid in changed:
                self.centralScrollArea.setWidget(FullPlaylistWidget(self.osPlayer,  self.centralScrollArea.widget().playlist.uid, self.playlistMenu))

            self.reload()

    def add_song_to_playlist(self, song_uid, playlist_uid):
        playlist = Playlist.load(playlist_uid)
        playlist.add_song(song_uid)
        playlist.save()
        if self.centralScrollArea.widget().playlist.uid == playlist_uid:
            self.centralScrollArea.setWidget(FullPlaylistWidget(self.osPlayer, playlist_uid, self.playlistMenu))

    def edit(self, uid):
        dialog = SongEditor(self, uid)
        dialog.exec()

