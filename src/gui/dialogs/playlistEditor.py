import os

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QCheckBox, QPushButton, QFileDialog, \
    QSplitter, QScrollArea, QWidget, QListWidget, QListWidgetItem
from gui.blocks.songBlock import SongBlock
from gui.globalUpdater import GlobalUpdater
from util.songs import Songs

# PlaylistEditor dialog
class PlaylistEditor(QDialog):
    def __init__(self, parent, globalUpdater, osPlayer, playlist):
        super().__init__(parent)
        self.globalUpdater = globalUpdater
        self.playlist = playlist
        self.setWindowTitle("Playlist Editor")
        self.setModal(True)

        self.osPlayer = osPlayer

        self.uidWidget = {}
        self.uidSongWidget = {}

        self.myLayout = QVBoxLayout()
        # Playlist name input
        self.nameEditLayout = QHBoxLayout()
        self.nameLabel = QLabel("Playlist Name")
        self.nameEditLayout.addWidget(self.nameLabel)
        self.nameLineEdit = QLineEdit()
        self.nameLineEdit.setText(playlist.name)
        self.nameLineEdit.textChanged.connect(self.check_save)
        self.nameEditLayout.addWidget(self.nameLineEdit)
        self.myLayout.addLayout(self.nameEditLayout)

        # Toggle playlist shuffle
        self.shuffleLayout = QHBoxLayout()
        self.shuffleLabel = QLabel("Playlist Shuffle")
        self.shuffleLayout.addWidget(self.shuffleLabel)
        self.shuffle = QCheckBox()
        if playlist.shuffle:
            self.shuffle.toggle()

        self.shuffle.stateChanged.connect(self.check_save)
        self.shuffleLayout.addWidget(self.shuffle)
        self.myLayout.addLayout(self.shuffleLayout)

        # Playlist image file choose
        self.imageLayout = QHBoxLayout()
        self.imageLabel = QLabel("Playlist Image")
        self.imageLayout.addWidget(self.imageLabel)
        self.chooseImageButton = QPushButton("Choose File")
        self.chooseImageButton.clicked.connect(self.request_image)
        self.imageLayout.addWidget(self.chooseImageButton)
        self.myLayout.addLayout(self.imageLayout)

        self.fileLabel = QLabel(playlist.image_url)
        self.myLayout.addWidget(self.fileLabel)

        # Load all available songs in SongLibrary with checkmarks to add
        self.splitter = QSplitter()
        self.songLayout = QVBoxLayout()
        for i in Songs.retrieve_songs():
            hori = QHBoxLayout()
            hori.setAlignment(Qt.AlignmentFlag.AlignLeft)
            widget = SongBlock(i)
            checkbox = QCheckBox()
            if i in playlist.songs:
                checkbox.toggle()
            checkbox.stateChanged.connect(lambda state, song=i: self.handle_checkbox(state, song))
            hori.addWidget(checkbox)
            hori.addWidget(widget)
            self.songLayout.addLayout(hori)

        self.songsWidget = QWidget()
        self.songsWidget.setLayout(self.songLayout)
        self.songScrollArea = QScrollArea()
        self.songScrollArea.setWidget(self.songsWidget)
        self.splitter.addWidget(self.songScrollArea)

        self.list_widget = QListWidget()

        # Enable drag and drop for reordering
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setDefaultDropAction(Qt.MoveAction)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)

        # Put all songs in the PLAYLIST in a reorderable list
        for i in playlist.songs:
            item = QListWidgetItem()
            song_widget = SongBlock(i)
            item.setSizeHint(song_widget.sizeHint())
            self.uidWidget[i] = item
            self.uidSongWidget[i] = song_widget
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, song_widget)

        self.splitter.addWidget(self.list_widget)
        self.songAddInfo = QLabel("Check songs you want in the playlist on the Song Library (left), and reorder on the right.")
        self.myLayout.addWidget(self.songAddInfo)
        self.myLayout.addWidget(self.splitter)

        # Save data
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

    # System request image file
    def request_image(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Image (*.png)")
        self.fileLabel.setText(fileName[0])
        self.check_save()

    # Handle adding a song to the list (update lists accordingly)
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
            song_widget = SongBlock(song_uid)
            item.setSizeHint(song_widget.sizeHint())
            self.uidWidget[song_uid] = item
            self.uidSongWidget[song_uid] = song_widget
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, song_widget)

    # Check that saving is possible/safe
    def check_save(self):
        if self.nameLineEdit.text().strip() != "" and self.fileLabel.text().strip() != "":
            self.submitButton.setEnabled(True)
            self.resultLabel.setText("Ready to save")

        else:
            self.submitButton.setEnabled(False)
            self.resultLabel.setText("Fill out playlist name and/or image file")

    # Save playlist data and update
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
            self.globalUpdater.playlist_uid = self.playlist.uid
            self.globalUpdater.update(GlobalUpdater.PLAYLIST_MENU | GlobalUpdater.CENTER_MENU)

