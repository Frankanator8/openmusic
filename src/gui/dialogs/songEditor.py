import os

from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog

from gui.globalUpdater import GlobalUpdater
from util.songs import Songs

class SongEditor(QDialog):
    def __init__(self, parent, globalUpdater, osPlayer, uid):
        super().__init__(parent)
        self.osPlayer = osPlayer
        self.globalUpdater = globalUpdater
        self.uid = uid

        # This data is largely the same as the dialog in leftMenu for create_single_menu. Refer to that
        image_url, audio_url, title, artist, album = Songs.load_song_data(self.uid)
        self.myLayout = QVBoxLayout()
        self.nameLayout = QHBoxLayout()
        self.nameLabel = QLabel("Name")
        self.nameLayout.addWidget(self.nameLabel)
        self.songNameEdit = QLineEdit()
        self.songNameEdit.setText(title)
        self.nameLayout.addWidget(self.songNameEdit)
        self.songNameEdit.textChanged.connect(self.check_save)
        self.myLayout.addLayout(self.nameLayout)

        self.artistLayout = QHBoxLayout()
        self.artistLabel = QLabel("Artist")
        self.artistLayout.addWidget(self.artistLabel)
        self.artistEdit = QLineEdit()
        self.artistEdit.setText(artist)
        self.artistEdit.textChanged.connect(self.check_save)
        self.artistLayout.addWidget(self.artistEdit)
        self.myLayout.addLayout(self.artistLayout)

        self.albumLayout = QHBoxLayout()
        self.albumLabel = QLabel("Album")
        self.albumLayout.addWidget(self.albumLabel)
        self.albumEdit = QLineEdit()
        self.albumEdit.setText(album)
        self.albumEdit.textChanged.connect(self.check_save)
        self.albumLayout.addWidget(self.albumEdit)
        self.myLayout.addLayout(self.albumLayout)

        self.audioLayout = QHBoxLayout()
        self.audioLabel = QLabel("Audio")
        self.audioLayout.addWidget(self.audioLabel)
        self.audioButton = QPushButton()
        self.audioButton.setText("Choose Audio File")
        self.audioButton.clicked.connect(self.request_audio)
        self.audioLayout.addWidget(self.audioButton)
        self.myLayout.addLayout(self.audioLayout)
        self.audioFileLabel = QLabel()
        self.audioFileLabel.setWordWrap(True)
        self.audioFileLabel.setText(audio_url)
        self.myLayout.addWidget(self.audioFileLabel)

        self.albumLayout = QHBoxLayout()
        self.albumChooseLabel = QLabel("Album Cover")
        self.albumLayout.addWidget(self.albumChooseLabel)
        self.albumButton = QPushButton()
        self.albumButton.setText("Choose Image File")
        self.albumButton.clicked.connect(self.request_image)
        self.albumLayout.addWidget(self.albumButton)
        self.myLayout.addLayout(self.albumLayout)
        self.imageFileLabel = QLabel()
        self.imageFileLabel.setWordWrap(True)
        self.imageFileLabel.setText(image_url)
        self.myLayout.addWidget(self.imageFileLabel)

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

    # Check saving is possible/safe
    def check_save(self):
        if self.songNameEdit.text().strip() != "" and self.albumEdit.text().strip() != "" and \
                self.artistEdit.text().strip() != "" and self.audioFileLabel.text() != "" and \
                self.imageFileLabel.text() != "":
            self.submitButton.setEnabled(True)
            self.resultLabel.setText("Ready to create")

        else:
            self.submitButton.setEnabled(False)
            self.resultLabel.setText("Fill out all fields")

    # Save song data
    def save(self):
        Songs.edit_song(self.uid, self.songNameEdit.text().strip(), self.artistEdit.text().strip(), self.albumEdit.text().strip(),
                        self.imageFileLabel.text(), self.audioFileLabel.text())
        self.globalUpdater.update(GlobalUpdater.SONG_MENU | GlobalUpdater.CENTER_MENU)
        if self.osPlayer.uid == self.uid:
            self.osPlayer.stop()

        self.resultLabel.setText("Saved!")

    # Make system requests for files
    def request_audio(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Audio (*.mp3)")
        self.audioFileLabel.setText(fileName[0])
        self.check_save()

    def request_image(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Image (*.png)")
        self.imageFileLabel.setText(fileName[0])
        self.check_save()
