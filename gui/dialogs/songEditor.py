import os

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

from gui.globalUpdater import GlobalUpdater
from library.songLibrary import SongLibrary
from osop.filehandler import FileHandler

class SongEditor(QDialog):
    def __init__(self, parent, osPlayer, globalUpdater, uid):
        super().__init__(parent)
        self.osPlayer = osPlayer
        self.globalUpdater = globalUpdater
        self.uid = uid
        image_url, audio_url, title, artist, album = self.load_data()
        self.myLayout = QVBoxLayout()
        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Name"))
        self.songNameEdit = QLineEdit()
        self.songNameEdit.setText(title)
        hLayout.addWidget(self.songNameEdit)
        self.songNameEdit.textChanged.connect(self.check_save)
        self.myLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Artist"))
        self.artistEdit = QLineEdit()
        self.artistEdit.setText(artist)
        self.artistEdit.textChanged.connect(self.check_save)
        hLayout.addWidget(self.artistEdit)
        self.myLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Album"))
        self.albumEdit = QLineEdit()
        self.albumEdit.setText(album)
        self.albumEdit.textChanged.connect(self.check_save)
        hLayout.addWidget(self.albumEdit)
        self.myLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Audio"))
        button = QPushButton()
        button.setText("Choose Audio File")
        button.clicked.connect(self.request_audio)
        hLayout.addWidget(button)
        self.myLayout.addLayout(hLayout)
        self.audio_file_label = QLabel()
        self.audio_file_label.setWordWrap(True)
        self.audio_file_label.setText(audio_url)
        self.myLayout.addWidget(self.audio_file_label)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Album Cover"))
        button = QPushButton()
        button.setText("Choose Image File")
        button.clicked.connect(self.request_image)
        hLayout.addWidget(button)
        self.myLayout.addLayout(hLayout)
        self.image_file_label = QLabel()
        self.image_file_label.setWordWrap(True)
        self.image_file_label.setText(image_url)
        self.myLayout.addWidget(self.image_file_label)

        self.submitButton = QPushButton()
        self.submitButton.setText("Save")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.save)
        self.myLayout.addWidget(self.submitButton)

        self.resultLabel = QLabel()
        self.resultLabel.setText("Fill out all fields")
        self.myLayout.addWidget(self.resultLabel)

        self.check_save()

        self.setLayout(self.myLayout)

    def check_save(self):
        if self.songNameEdit.text().strip() != "" and self.albumEdit.text().strip() != "" and \
                self.artistEdit.text().strip() != "" and self.audio_file_label.text() != "" and \
                self.image_file_label.text() != "":
            self.submitButton.setEnabled(True)
            self.resultLabel.setText("Ready to create")

        else:
            self.submitButton.setEnabled(False)
            self.resultLabel.setText("Fill out all fields")


    def save(self):
        SongLibrary.edit_song(self.uid, self.songNameEdit.text().strip(), self.artistEdit.text().strip(), self.albumEdit.text().strip(),
                            self.image_file_label.text(), self.audio_file_label.text())
        self.globalUpdater.update(GlobalUpdater.SONG_MENU | GlobalUpdater.CENTER_MENU)
        if self.osPlayer.uid == self.uid:
            self.osPlayer.stop()

        self.resultLabel.setText("Saved!")


    def load_data(self):
        image_url = f"{FileHandler.SONG_DATA}/{self.uid}.png"
        audio_url = f"{FileHandler.AUDIOS}/{self.uid}.mp3"
        with open(f"{FileHandler.SONG_DATA}/{self.uid}.txt") as f:
            title = f.readline().strip()
            artist = f.readline().strip()
            album = f.readline().strip()

        return image_url, audio_url, title, artist, album

    def request_audio(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Audio (*.mp3)")
        self.audio_file_label.setText(fileName[0])
        self.check_save()

    def request_image(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Image (*.png)")
        self.image_file_label.setText(fileName[0])
        self.check_save()
