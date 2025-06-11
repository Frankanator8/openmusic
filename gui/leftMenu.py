import shutil
import uuid

import moviepy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QScrollArea, QLabel, QHBoxLayout, QPushButton, QDialog, \
    QFormLayout, QLineEdit, QFileDialog
import os

from filehandler import FileHandler
from gui.playlistmenu import PlaylistMenu
from gui.songmenu import SongMenu


class LeftMenu(QWidget):
    def __init__(self, osPlayer, centralScrollArea):
        super().__init__()
        self.layout = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)


        self.topWidget = QWidget()
        topMenu = QVBoxLayout()

        hLayout = QHBoxLayout()
        top = QLabel()
        top.setText("Song Library")
        hLayout.addWidget(top)

        newSong = QPushButton()
        newSong.setText("Add song")
        newSong.clicked.connect(self.new_song)
        hLayout.addWidget(newSong)

        scrollArea = QScrollArea()
        self.songMenu = SongMenu(osPlayer)
        scrollArea.setWidget(self.songMenu)
        topMenu.addLayout(hLayout)
        topMenu.addWidget(scrollArea)
        self.topWidget.setLayout(topMenu)
        splitter.addWidget(self.topWidget)

        self.bottomWidget = QWidget()
        bottomMenu = QVBoxLayout()
        top = QLabel()
        top.setText("Playlists")
        scrollArea = QScrollArea()
        scrollArea.setWidget(PlaylistMenu(osPlayer, centralScrollArea))
        bottomMenu.addWidget(top)
        bottomMenu.addWidget(scrollArea)
        self.bottomWidget.setLayout(bottomMenu)
        splitter.addWidget(self.bottomWidget)

        self.layout.addWidget(splitter)
        self.setLayout(self.layout)
        self.createdSongs = 0

    def new_song(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Add New Song")
        self.dialog.setModal(True)

        layout = QVBoxLayout()
        self.modalLayout = layout
        hLayout = QHBoxLayout()
        self.leftButton = QPushButton()
        self.leftButton.setText("Add songs individually")
        self.leftButton.clicked.connect(self.create_single_song)
        hLayout.addWidget(self.leftButton)
        self.rightButton = QPushButton()
        self.rightButton.setText("Add songs in bulk")
        self.rightButton.clicked.connect(self.create_bulk_song)
        hLayout.addWidget(self.rightButton)
        layout.addLayout(hLayout)

        self.dialog.setLayout(layout)
        self.dialog.exec()

    def create_single_song(self):
        self.leftButton.setEnabled(False)
        self.rightButton.setEnabled(False)
        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Name"))
        self.songNameEdit = QLineEdit()
        hLayout.addWidget(self.songNameEdit)
        self.songNameEdit.textChanged.connect(self.single_button_update)
        self.modalLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Artist"))
        self.artistEdit = QLineEdit()
        self.artistEdit.textChanged.connect(self.single_button_update)
        hLayout.addWidget(self.artistEdit)
        self.modalLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Album"))
        self.albumEdit = QLineEdit()
        self.albumEdit.textChanged.connect(self.single_button_update)
        hLayout.addWidget(self.albumEdit)
        self.modalLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Audio"))
        button = QPushButton()
        button.setText("Choose Audio File")
        button.clicked.connect(self.request_audio)
        hLayout.addWidget(button)
        self.modalLayout.addLayout(hLayout)
        self.audio_file_label = QLabel()
        self.audio_file_label.setWordWrap(True)
        self.modalLayout.addWidget(self.audio_file_label)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Album Cover"))
        button = QPushButton()
        button.setText("Choose Image File")
        button.clicked.connect(self.request_image)
        hLayout.addWidget(button)
        self.modalLayout.addLayout(hLayout)
        self.image_file_label = QLabel()
        self.image_file_label.setWordWrap(True)
        self.modalLayout.addWidget(self.image_file_label)

        self.submitButton = QPushButton()
        self.submitButton.setText("Create")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.make_song)
        self.modalLayout.addWidget(self.submitButton)

        self.resultLabel = QLabel()
        self.resultLabel.setText("Fill out all fields")
        self.modalLayout.addWidget(self.resultLabel)
        self.createdSongs = 0


    def create_bulk_song(self):
        self.leftButton.setEnabled(False)
        self.rightButton.setEnabled(False)

    def request_audio(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Audio (*.mp3)")
        self.audio_file_label.setText(fileName[0])
        self.single_button_update()

    def request_image(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Image (*.png)")
        self.image_file_label.setText(fileName[0])
        self.single_button_update()

    def single_button_update(self):
        if self.songNameEdit.text().strip() != "" and self.albumEdit.text().strip() != "" and \
                self.artistEdit.text().strip() != "" and self.audio_file_label.text() != "" and \
                self.image_file_label.text() != "":
            self.submitButton.setEnabled(True)
            self.resultLabel.setText("Ready to create")

        else:
            self.submitButton.setEnabled(False)
            self.resultLabel.setText("Fill out all fields")

    def make_song(self):
        if self.songNameEdit.text().strip() != "" and self.albumEdit.text().strip() != "" and \
                self.artistEdit.text().strip() != "" and self.audio_file_label.text() != "" and \
                self.image_file_label.text() != "":
            uid = str(uuid.uuid4()).replace("-", "")
            clip = moviepy.AudioFileClip(self.audio_file_label.text())
            with open(f"{FileHandler.SONG_DATA}/{uid}.txt", "w") as f:
                f.write(f"{self.songNameEdit.text().strip()}\n{self.artistEdit.text().strip()}\n{self.albumEdit.text().strip()}\n{clip.duration}")

            clip.write_audiofile(f"{FileHandler.AUDIOS}/{uid}.mp3")
            shutil.copyfile(self.image_file_label.text(), f"{FileHandler.SONG_DATA}/{uid}.png")
            self.createdSongs += 1
            self.resultLabel.setText(f"Success! Created {self.createdSongs} since start of session")
            self.songMenu.reload()
