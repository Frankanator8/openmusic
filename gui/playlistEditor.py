import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QFileDialog, \
    QSplitter, QScrollArea, QWidget, QListView, QScrollBar, QListWidget, QListWidgetItem

from gui.fullPlaylistWidget import FullPlaylistWidget
from gui.songWidget import SongWidget
from songLibrary import SongLibrary


class PlaylistEditor(QDialog):
    def __init__(self, playlist, playlistMenu, osPlayer, centralScrollArea):
        super().__init__(playlistMenu)
        self.playlistMenu = playlistMenu
        self.playlist = playlist
        self.setWindowTitle("Playlist Editor")
        self.setModal(True)

        self.osPlayer = osPlayer
        self.centralScrollArea = centralScrollArea

        self.uidWidget = {}
        self.uidSongWidget = {}

        self.myLayout = QVBoxLayout()

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Playlist Name"))
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setText(playlist.name)
        self.nameLineEdit.textChanged.connect(self.check_save)
        hLayout.addWidget(self.nameLineEdit)
        self.myLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Playlist Shuffle"))
        self.shuffle = QCheckBox()
        if playlist.shuffle:
            self.shuffle.toggle()

        self.shuffle.stateChanged.connect(self.check_save)
        hLayout.addWidget(self.shuffle)
        self.myLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Playlist Image"))
        button = QPushButton("Choose File")
        button.clicked.connect(self.request_image)
        hLayout.addWidget(button)
        self.myLayout.addLayout(hLayout)

        self.fileLabel = QLabel(playlist.image_url)
        self.myLayout.addWidget(self.fileLabel)

        splitter = QSplitter()
        songLayout = QVBoxLayout()
        for i in SongLibrary.retrieve_songs():
            hori = QHBoxLayout()
            hori.setAlignment(Qt.AlignmentFlag.AlignLeft)
            widget = SongWidget(i)
            checkbox = QCheckBox()
            if i in playlist.songs:
                checkbox.toggle()
            checkbox.stateChanged.connect(lambda state, song=i: self.handle_checkbox(state, song))
            hori.addWidget(checkbox)
            hori.addWidget(widget)
            songLayout.addLayout(hori)

        widg = QWidget()
        widg.setLayout(songLayout)
        scrollArea = QScrollArea()
        scrollArea.setWidget(widg)
        splitter.addWidget(scrollArea)

        self.list_widget = QListWidget()

        # Enable drag and drop for reordering
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setDefaultDropAction(Qt.MoveAction)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)

        for i in playlist.songs:
            item = QListWidgetItem()
            song_widget = SongWidget(i)
            item.setSizeHint(song_widget.sizeHint())
            self.uidWidget[i] = item
            self.uidSongWidget[i] = song_widget
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, song_widget)

        splitter.addWidget(self.list_widget)

        self.myLayout.addWidget(QLabel("Check songs you want in the playlist on the Song Library (left), and reorder on the right."))
        self.myLayout.addWidget(splitter)

        self.submitButton = QPushButton()
        self.submitButton.setText("Save")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.save_playlist)
        self.myLayout.addWidget(self.submitButton)

        self.resultLabel = QLabel()
        self.resultLabel.setText("Fill out all fields")
        self.myLayout.addWidget(self.resultLabel)

        self.setLayout(self.myLayout)
        self.check_save()

    def request_image(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Image (*.png)")
        self.fileLabel.setText(fileName[0])
        self.check_save()

    def handle_checkbox(self, state, song_uid):
        if not state:
            self.list_widget.removeItemWidget(self.uidWidget[song_uid])
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                if self.uidWidget[song_uid] == item:  # Or some other check
                    self.list_widget.takeItem(i)
                    break
            self.uidSongWidget[song_uid].deleteLater()
            del self.uidWidget[song_uid]
            del self.uidSongWidget[song_uid]

        else:
            item = QListWidgetItem()
            song_widget = SongWidget(song_uid)
            item.setSizeHint(song_widget.sizeHint())
            self.uidWidget[song_uid] = item
            self.uidSongWidget[song_uid] = song_widget
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, song_widget)

    def check_save(self):
        if self.nameLineEdit.text().strip() != "" and self.fileLabel.text().strip() != "":
            self.submitButton.setEnabled(True)
            self.resultLabel.setText("Ready to save")

        else:
            self.submitButton.setEnabled(False)
            self.resultLabel.setText("Fill out playlist name and/or image file")

    def save_playlist(self):
        if self.nameLineEdit.text().strip() != "" and self.fileLabel.text().strip() != "":
            self.playlist.name = self.nameLineEdit.text().strip()
            self.playlist.shuffle = self.shuffle.isChecked()
            self.playlist.image_url = self.fileLabel.text().strip()
            songs = []
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                songs.append(self.list_widget.itemWidget(item).uid)


            self.playlist.songs = songs
            self.playlist.save()
            self.playlistMenu.reload()
            self.centralScrollArea.widget().deleteLater()
            self.centralScrollArea.setWidget(FullPlaylistWidget(self.osPlayer, self.playlist.uid, self.playlistMenu))

