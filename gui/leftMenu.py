import shutil
import uuid

import moviepy
from PySide6.QtCore import Qt, QTimer
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QScrollArea, QLabel, QHBoxLayout, QPushButton, QDialog, \
    QFormLayout, QLineEdit, QFileDialog, QCheckBox, QSizePolicy
import os

from filehandler import FileHandler
from gui.playlistmenu import PlaylistMenu
from gui.songmenu import SongMenu
from songmaker import SongMaker


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

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Song Pattern Match"))
        self.songEdit = QLineEdit()
        self.songEdit.textChanged.connect(self.multi_button_update)
        hLayout.addWidget(self.songEdit)
        self.modalLayout.addLayout(hLayout)
        self.modalLayout.addWidget(QLabel("Enter the naming pattern for your audio files. \nThe naming pattern must include all 3 of the following parameters:\n%s - song name; %a - artist name; %l - album name; \n%% - percent symbol\nExample %s - %a (%l)"))

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Cover Pattern Match"))
        self.coverEdit = QLineEdit()
        self.coverEdit.textChanged.connect(self.multi_button_update)
        hLayout.addWidget(self.coverEdit)
        self.modalLayout.addLayout(hLayout)
        self.modalLayout.addWidget(QLabel("Enter the naming pattern for your album cover files. \nThe naming pattern must include all equality parameters"))

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Check Song Name Equality"))
        self.songNameEquality = QCheckBox()
        self.songNameEquality.setChecked(True)
        self.songNameEquality.clicked.connect(self.multi_button_update)
        hLayout.addWidget(self.songNameEquality)
        self.modalLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Check Artist Name Equality"))
        self.artistNameEquality = QCheckBox()
        self.artistNameEquality.setChecked(True)
        self.artistNameEquality.clicked.connect(self.multi_button_update)
        hLayout.addWidget(self.artistNameEquality)
        self.modalLayout.addLayout(hLayout)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Check Album Name Equality"))
        self.albumNameEquality = QCheckBox()
        self.albumNameEquality.setChecked(True)
        self.albumNameEquality.clicked.connect(self.multi_button_update)
        hLayout.addWidget(self.albumNameEquality)
        self.modalLayout.addLayout(hLayout)

        self.modalLayout.addWidget(QLabel("Mark which parameters must be equal to match an album cover to an audio file"))

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Ignore errors?"))
        self.ignoreErrors = QCheckBox()
        self.ignoreErrors.setChecked(True)
        self.ignoreErrors.clicked.connect(self.multi_button_update)
        hLayout.addWidget(self.ignoreErrors)
        self.modalLayout.addLayout(hLayout)

        self.modalLayout.addWidget(QLabel("In the event of an error (parameter match failure, no matching cover/song), a dialog will open and pause parsing.\nChecking this will not show dialogs and not pause parsing."))

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Audio Files"))
        button = QPushButton()
        button.setText("Choose Audio Files")
        button.clicked.connect(self.request_audios)
        hLayout.addWidget(button)
        self.modalLayout.addLayout(hLayout)
        self.audio_files_label = QLabel()
        self.audio_files_label.setWordWrap(True)  # If displaying text
        self.audio_files_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.audio_files = []
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.audio_files_label)
        scrollArea.setWidgetResizable(True)
        self.modalLayout.addWidget(scrollArea)

        hLayout = QHBoxLayout()
        hLayout.addWidget(QLabel("Album Cover Files"))
        button = QPushButton()
        button.setText("Choose Album Cover Files")
        button.clicked.connect(self.request_images)
        hLayout.addWidget(button)
        self.modalLayout.addLayout(hLayout)
        self.image_files_label = QLabel()
        self.image_files_label.setWordWrap(True)  # If displaying text
        self.image_files_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_files = []
        scrollArea = QScrollArea()
        scrollArea.setWidget(self.image_files_label)
        scrollArea.setWidgetResizable(True)
        self.modalLayout.addWidget(scrollArea)

        self.submitButton = QPushButton()
        self.submitButton.setText("Create")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.make_song)
        self.modalLayout.addWidget(self.submitButton)

        self.resultLabel = QLabel()
        self.resultLabel.setText("Fill out all fields")
        self.modalLayout.addWidget(self.resultLabel)
        self.createdSongs = 0

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
            SongMaker.make_song(self.songNameEdit.text().strip(), self.artistEdit.text().strip(), self.albumEdit.text().strip(),
                                self.image_file_label.text(), self.audio_file_label.text())
            self.createdSongs += 1
            self.resultLabel.setText(f"Success! Created {self.createdSongs} since start of session")
            self.songMenu.reload()

    def multi_button_update(self):
        enabled = False
        allFilled = len(self.image_files) > 0 and len(self.audio_files) > 0 and self.songEdit.text().strip() != "" \
        and self.coverEdit.text().strip() != ""
        if allFilled:
            pattern = self.songEdit.text().strip()
            allParametersIn = "%s" in pattern and "%a" in pattern and "%l" in pattern
            if allParametersIn:
                oneChecked = self.songNameEquality.isChecked() or self.albumNameEquality.isChecked() or self.artistNameEquality.isChecked()
                if oneChecked:
                    coverPattern = self.coverEdit.text().strip()
                    good = (not self.songNameEquality.isChecked() or "%s" in coverPattern) \
                    and (not self.albumNameEquality.isChecked() or "%l" in coverPattern) \
                    and (not self.artistNameEquality.isChecked() or "%a" in coverPattern)
                    # check | includes | result
                    #   T        T         T
                    #   T        F         F
                    #   F        T         T
                    #   F        F         T
                    if good:
                        enabled = True
                        self.resultLabel.setText("Ready to create")

                    else:
                        self.resultLabel.setText("One or more equality parameters missing in album cover pattern")

                else:
                    self.resultLabel.setText("You must check for at least one parameter")

            else:
                self.resultLabel.setText("Song pattern is missing parameter(s)")

        else:
            self.resultLabel.setText("Fill out pattern fields and choose the files")

        self.submitButton.setEnabled(enabled)



    def request_audios(self):
        fileNames = QFileDialog.getOpenFileNames(self, "Open Files", str(os.path.expanduser("~")),"Audio (*.mp3)")
        self.audio_files = fileNames[0]
        self.audio_files_label.setText("\n".join(self.audio_files))
        self.multi_button_update()

    def request_images(self):
        fileNames = QFileDialog.getOpenFileNames(self, "Open Files", str(os.path.expanduser("~")),"Image (*.png)")
        self.image_files = fileNames[0]
        self.image_files_label.setText("\n".join(self.image_files))
        self.multi_button_update()
