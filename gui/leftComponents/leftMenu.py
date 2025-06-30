from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QScrollArea, QLabel, QHBoxLayout, QPushButton, QDialog, \
    QLineEdit, QFileDialog, QCheckBox, QSizePolicy, QMessageBox
import os

from gui.globalUpdater import GlobalUpdater
from gui.leftComponents.playlistmenu import PlaylistMenu
from gui.leftComponents.songmenu import SongMenu
from util.songs import Songs
from util.playlist import Playlist


class LeftMenu(QWidget):
    def __init__(self, globalUpdater, osPlayer):
        super().__init__()
        self.myLayout = QVBoxLayout()
        self.globalUpdater = globalUpdater
        self.splitter = QSplitter(Qt.Vertical)

        self.osPlayer = osPlayer
        self.playlistMenu = PlaylistMenu(self.globalUpdater, osPlayer)

        self.topWidget = QWidget()
        topMenu = QVBoxLayout()

        self.songHeaderLayout = QHBoxLayout()
        self.songLibraryLabel = QLabel()
        self.songLibraryLabel.setText("Song Library")
        self.songHeaderLayout.addWidget(self.songLibraryLabel)

        self.newSongButton = QPushButton()
        self.newSongButton.setText("Add song")
        self.newSongButton.clicked.connect(self.new_song)
        self.songHeaderLayout.addWidget(self.newSongButton)

        self.songScrollArea = QScrollArea()
        self.songMenu = SongMenu(self.globalUpdater, osPlayer)
        self.songScrollArea.setWidget(self.songMenu)
        topMenu.addLayout(self.songHeaderLayout)
        topMenu.addWidget(self.songScrollArea)
        self.topWidget.setLayout(topMenu)
        self.splitter.addWidget(self.topWidget)

        self.bottomWidget = QWidget()
        bottomMenu = QVBoxLayout()


        self.playlistHeaderLayout = QHBoxLayout()
        self.playlistsLabel = QLabel()
        self.playlistsLabel.setText("Playlists")
        self.playlistHeaderLayout.addWidget(self.playlistsLabel)
        self.newPlaylistButton = QPushButton()
        self.newPlaylistButton.setText("New playlist")
        self.newPlaylistButton.clicked.connect(self.new_playlist)
        self.playlistHeaderLayout.addWidget(self.newPlaylistButton)

        self.playlistScrollArea = QScrollArea()
        self.playlistScrollArea.setWidget(self.playlistMenu)
        self.playlistScrollArea.setWidgetResizable(True)
        bottomMenu.addLayout(self.playlistHeaderLayout)
        bottomMenu.addWidget(self.playlistScrollArea)
        self.bottomWidget.setLayout(bottomMenu)
        self.splitter.addWidget(self.bottomWidget)

        self.myLayout.addWidget(self.splitter)
        self.setLayout(self.myLayout)
        self.createdSongs = 0

    def new_song(self):
        self.dialog = QDialog(self)
        self.dialog.setWindowTitle("Add New Song")
        self.dialog.setModal(True)

        layout = QVBoxLayout()
        self.modalLayout = layout
        self.buttonSelectLayout = QHBoxLayout()
        self.leftButton = QPushButton()
        self.leftButton.setText("Add songs individually")
        self.leftButton.clicked.connect(self.create_single_song)
        self.buttonSelectLayout.addWidget(self.leftButton)
        self.rightButton = QPushButton()
        self.rightButton.setText("Add songs in bulk")
        self.rightButton.clicked.connect(self.create_bulk_song)
        self.buttonSelectLayout.addWidget(self.rightButton)
        layout.addLayout(self.buttonSelectLayout)

        self.dialog.setLayout(layout)
        self.dialog.exec()

    def create_single_song(self):
        self.leftButton.setEnabled(False)
        self.rightButton.setEnabled(False)
        self.nameLayout = QHBoxLayout()
        self.nameLabel = QLabel("Name")
        self.nameLayout.addWidget(self.nameLabel)
        self.songNameEdit = QLineEdit()
        self.nameLayout.addWidget(self.songNameEdit)
        self.songNameEdit.textChanged.connect(self.single_button_update)
        self.modalLayout.addLayout(self.nameLayout)

        self.artistLayout = QHBoxLayout()
        self.artistLabel = QLabel("Artist")
        self.artistLayout.addWidget(self.artistLabel)
        self.artistEdit = QLineEdit()
        self.artistEdit.textChanged.connect(self.single_button_update)
        self.artistLayout.addWidget(self.artistEdit)
        self.modalLayout.addLayout(self.artistLayout)

        self.albumLayout = QHBoxLayout()
        self.albumLabel = QLabel("Album")
        self.albumLayout.addWidget(self.albumLabel)
        self.albumEdit = QLineEdit()
        self.albumEdit.textChanged.connect(self.single_button_update)
        self.albumLayout.addWidget(self.albumEdit)
        self.modalLayout.addLayout(self.albumLayout)

        self.audioLayout = QHBoxLayout()
        self.audioLabel = QLabel("Audio")
        self.audioLayout.addWidget(self.audioLabel)
        self.audioButton = QPushButton()
        self.audioButton.setText("Choose Audio File")
        self.audioButton.clicked.connect(self.request_audio)
        self.audioLayout.addWidget(self.audioButton)
        self.modalLayout.addLayout(self.audioLayout)
        self.audioFileLabel = QLabel()
        self.audioFileLabel.setWordWrap(True)
        self.modalLayout.addWidget(self.audioFileLabel)

        self.albumLayout = QHBoxLayout()
        self.albumChooseLabel = QLabel("Album Cover")
        self.albumLayout.addWidget(self.albumChooseLabel)
        self.albumButton = QPushButton()
        self.albumButton.setText("Choose Image File")
        self.albumButton.clicked.connect(self.request_image)
        self.albumLayout.addWidget(self.albumButton)
        self.modalLayout.addLayout(self.albumLayout)
        self.imageFileLabel = QLabel()
        self.imageFileLabel.setWordWrap(True)
        self.modalLayout.addWidget(self.imageFileLabel)

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

        self.songPatternLayout = QHBoxLayout()
        self.songPatternLabel = QLabel("Song Pattern Match")
        self.songPatternLayout.addWidget(self.songPatternLabel)
        self.songEdit = QLineEdit()
        self.songEdit.textChanged.connect(self.multi_button_update)
        self.songPatternLayout.addWidget(self.songEdit)
        self.modalLayout.addLayout(self.songPatternLayout)
        self.songPatternAddlInfo = QLabel("Enter the naming pattern for your audio files. \nThe naming pattern must include all 3 of the following parameters:\n%s - song name; %a - artist name; %l - album name; \n%% - percent symbol; * - wild card section\nExample: /Users/EX/%s - %a (%l)**.mp3")
        self.modalLayout.addWidget(self.songPatternAddlInfo)

        self.coverPatternLayout = QHBoxLayout()
        self.coverPatternLabel = QLabel("Cover Pattern Match")
        self.coverPatternLayout.addWidget(self.coverPatternLabel)
        self.coverEdit = QLineEdit()
        self.coverEdit.textChanged.connect(self.multi_button_update)
        self.coverPatternLayout.addWidget(self.coverEdit)
        self.modalLayout.addLayout(self.coverPatternLayout)
        self.coverPatternAddlInfo = QLabel("Enter the naming pattern for your album cover files. \nThe naming pattern must include all equality parameters")
        self.modalLayout.addWidget(self.coverPatternAddlInfo)

        self.songNameEqualityLayout = QHBoxLayout()
        self.songNameEqualityLabel = QLabel("Check Song Name Equality")
        self.songNameEqualityLayout.addWidget(self.songNameEqualityLabel)
        self.songNameEquality = QCheckBox()
        self.songNameEquality.setChecked(True)
        self.songNameEquality.clicked.connect(self.multi_button_update)
        self.songNameEqualityLayout.addWidget(self.songNameEquality)
        self.modalLayout.addLayout(self.songNameEqualityLayout)

        self.artistNameEqualityLayout = QHBoxLayout()
        self.artistNameEqualityLabel = QLabel("Check Artist Name Equality")
        self.artistNameEqualityLayout.addWidget(self.artistNameEqualityLabel)
        self.artistNameEquality = QCheckBox()
        self.artistNameEquality.setChecked(True)
        self.artistNameEquality.clicked.connect(self.multi_button_update)
        self.artistNameEqualityLayout.addWidget(self.artistNameEquality)
        self.modalLayout.addLayout(self.artistNameEqualityLayout)

        self.albumNameEqualityLayout = QHBoxLayout()
        self.albumNameEqualityLabel = QLabel("Check Album Name Equality")
        self.albumNameEqualityLayout.addWidget(self.albumNameEqualityLabel)
        self.albumNameEquality = QCheckBox()
        self.albumNameEquality.setChecked(True)
        self.albumNameEquality.clicked.connect(self.multi_button_update)
        self.albumNameEqualityLayout .addWidget(self.albumNameEquality)
        self.modalLayout.addLayout(self.albumNameEqualityLayout )

        self.markLabel = QLabel("Mark which parameters must be equal to match an album cover to an audio file")
        self.modalLayout.addWidget(self.markLabel)

        self.ignoreErrorsLayout = QHBoxLayout()
        self.ignoreErrorsLabel = QLabel("Ignore errors?")
        self.ignoreErrorsLayout.addWidget(self.ignoreErrorsLabel)
        self.ignoreErrors = QCheckBox()
        self.ignoreErrors.setChecked(True)
        self.ignoreErrors.clicked.connect(self.multi_button_update)
        self.ignoreErrorsLayout.addWidget(self.ignoreErrors)
        self.modalLayout.addLayout(self.ignoreErrorsLayout)
        self.ignoreErrorsAddlInfo = QLabel("In the event of an error (parameter match failure, no matching cover/song), a dialog will open and pause parsing.\nChecking this will not show dialogs and not pause parsing.")
        self.modalLayout.addWidget(self.ignoreErrorsAddlInfo)

        self.audioFilesLayout = QHBoxLayout()
        self.audioFilesLabel = QLabel("Audio Files")
        self.audioFilesLayout.addWidget(self.audioFilesLabel)
        self.audioFilesButton = QPushButton()
        self.audioFilesButton.setText("Choose Audio Files")
        self.audioFilesButton.clicked.connect(self.request_audios)
        self.audioFilesLayout.addWidget(self.audioFilesButton)
        self.modalLayout.addLayout(self.audioFilesLayout)
        self.audioFilesSelectedLabel = QLabel()
        self.audioFilesSelectedLabel.setWordWrap(True)  # If displaying text
        self.audioFilesSelectedLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.audio_files = []
        self.audioScrollArea = QScrollArea()
        self.audioScrollArea.setWidget(self.audioFilesSelectedLabel)
        self.audioScrollArea.setWidgetResizable(True)
        self.modalLayout.addWidget(self.audioScrollArea)

        self.albumCoverFilesLayout = QHBoxLayout()
        self.albumCoverFilesLabel = QLabel("Album Cover Files")
        self.albumCoverFilesLayout.addWidget(self.albumCoverFilesLabel)
        self.albumCoverButton = QPushButton()
        self.albumCoverButton.setText("Choose Album Cover Files")
        self.albumCoverButton.clicked.connect(self.request_images)
        self.albumCoverFilesLayout.addWidget(self.albumCoverButton)
        self.modalLayout.addLayout(self.albumCoverFilesLayout)
        self.imageFilesLabel = QLabel()
        self.imageFilesLabel.setWordWrap(True)  # If displaying text
        self.imageFilesLabel.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_files = []
        self.imageScrollArea = QScrollArea()
        self.imageScrollArea.setWidget(self.imageFilesLabel)
        self.imageScrollArea.setWidgetResizable(True)
        self.modalLayout.addWidget(self.imageScrollArea)

        self.submitButton = QPushButton()
        self.submitButton.setText("Create")
        self.submitButton.setEnabled(False)
        self.submitButton.clicked.connect(self.make_songs)
        self.modalLayout.addWidget(self.submitButton)

        self.resultLabel = QLabel()
        self.resultLabel.setText("Fill out all fields")
        self.modalLayout.addWidget(self.resultLabel)
        self.createdSongs = 0

    def request_audio(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Audio (*.mp3)")
        self.audioFileLabel.setText(fileName[0])
        self.single_button_update()

    def request_image(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Image (*.png)")
        self.imageFileLabel.setText(fileName[0])
        self.single_button_update()

    def single_button_update(self):
        if self.songNameEdit.text().strip() != "" and self.albumEdit.text().strip() != "" and \
                self.artistEdit.text().strip() != "" and self.audioFileLabel.text() != "" and \
                self.imageFileLabel.text() != "":
            self.submitButton.setEnabled(True)
            self.resultLabel.setText("Ready to create")

        else:
            self.submitButton.setEnabled(False)
            self.resultLabel.setText("Fill out all fields")

    def make_song(self):
        if self.songNameEdit.text().strip() != "" and self.albumEdit.text().strip() != "" and \
                self.artistEdit.text().strip() != "" and self.audioFileLabel.text() != "" and \
                self.imageFileLabel.text() != "":
            Songs.make_song(self.songNameEdit.text().strip(), self.artistEdit.text().strip(), self.albumEdit.text().strip(),
                            self.imageFileLabel.text(), self.audioFileLabel.text())
            self.createdSongs += 1
            self.resultLabel.setText(f"Success! Created {self.createdSongs} since start of session")
            self.globalUpdater.update(GlobalUpdater.SONG_MENU)

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
        self.audioFilesSelectedLabel.setText("\n".join(self.audio_files))
        self.multi_button_update()

    def request_images(self):
        fileNames = QFileDialog.getOpenFileNames(self, "Open Files", str(os.path.expanduser("~")),"Image (*.png)")
        self.image_files = fileNames[0]
        self.imageFilesLabel.setText("\n".join(self.image_files))
        self.multi_button_update()

    def make_songs(self):
        audio_pattern = self.songEdit.text().strip()
        cover_pattern = self.coverEdit.text().strip()
        ignore = self.ignoreErrors.isChecked()

        matchList = []
        songsMade = 0
        if self.songNameEquality.isChecked():
            matchList.append(0)

        if self.artistNameEquality.isChecked():
            matchList.append(1)

        if self.albumNameEquality.isChecked():
            matchList.append(2)

        song_dict = {}
        match_dict = {}

        for i in self.audio_files:
            patternIndex = 0
            fileIndex = 0
            failed = False
            songdata = ["", "", ""]
            dataIndex = -1
            while patternIndex < len(audio_pattern) and fileIndex < len(i):
                if audio_pattern[patternIndex] == "%":
                    if patternIndex == len(audio_pattern) - 1:
                        failed = True
                        break

                    match audio_pattern[patternIndex+1]:
                        case "s":
                            dataIndex = 0

                        case "a":
                            dataIndex = 1

                        case "l":
                            dataIndex = 2

                        case "%":
                            if i[fileIndex] == "%":
                                dataIndex = -1
                                fileIndex += 1

                            else:
                                failed = True
                                break

                    patternIndex += 2

                elif audio_pattern[patternIndex] == "*":
                    patternIndex+=1
                    if patternIndex >= len(audio_pattern):
                        break

                    while i[fileIndex] != audio_pattern[patternIndex]:
                        fileIndex += 1

                    fileIndex += 1
                    patternIndex += 1

                else:
                    if i[fileIndex] == audio_pattern[patternIndex]:
                        dataIndex = -1
                        patternIndex += 1
                        fileIndex += 1

                    else:
                        if dataIndex != -1:
                            songdata[dataIndex] = f"{songdata[dataIndex]}{i[fileIndex]}"
                            fileIndex += 1

                        else:
                            failed = True
                            break


            if failed:
                if not ignore:
                    QMessageBox.critical(self, "Parse Error",
                    f"There was an error parsing\n{i}\nPress OK to continue",
                    QMessageBox.Ok)

            else:
                if songdata[0] == "" or songdata[1] == "" or songdata[2] == "":
                    if not ignore:
                        QMessageBox.critical(self, "Song Error",
                                             f"There were parameters missing in\n{i}\nPress OK to continue",
                                             QMessageBox.Ok)

                else:
                    song_dict[tuple(songdata)] = i

                    matchdata = [songdata[i] for i in matchList]

                    match_dict[tuple(matchdata)] = tuple(songdata)


        for i in self.image_files:
            patternIndex = 0
            fileIndex = 0
            failed = False
            songdata = ["", "", ""]
            dataIndex = -1
            while patternIndex < len(cover_pattern) and fileIndex < len(i):
                if cover_pattern[patternIndex] == "%":
                    if patternIndex == len(cover_pattern) - 1:
                        failed = True
                        break

                    match cover_pattern[patternIndex+1]:
                        case "s":
                            dataIndex = 0

                        case "a":
                            dataIndex = 1

                        case "l":
                            dataIndex = 2

                        case "%":
                            if i[fileIndex] == "%":
                                dataIndex = -1
                                fileIndex += 1

                            else:
                                failed = True
                                break

                    patternIndex += 2

                elif cover_pattern[patternIndex] == "*":
                    patternIndex+=1
                    if patternIndex >= len(cover_pattern):
                        break

                    while i[fileIndex] != cover_pattern[patternIndex]:
                        fileIndex += 1

                    fileIndex += 1
                    patternIndex += 1

                else:
                    if i[fileIndex] == cover_pattern[patternIndex]:
                        dataIndex = -1
                        patternIndex += 1
                        fileIndex += 1

                    else:
                        if dataIndex != -1:
                            songdata[dataIndex] = f"{songdata[dataIndex]}{i[fileIndex]}"
                            fileIndex += 1

                        else:
                            failed = True
                            break


            if failed:
                if not ignore:
                    QMessageBox.critical(self, "Parse Error",
                                         f"There was an error parsing\n{i}\nPress OK to continue",
                                         QMessageBox.Ok)

            else:
                matchdata = [songdata[i] for i in matchList]
                if matchdata in match_dict.keys():
                    name, artist, album = match_dict[matchdata]
                    audio_url = song_dict[match_dict[matchdata]]
                    image_url = i
                    Songs.make_song(name, artist, album, image_url, audio_url)
                    songsMade += 1

                else:
                    if not ignore:
                        QMessageBox.critical(self, "Match Error",
                                             f"There was no match for \n{i}\nPress OK to continue",
                                             QMessageBox.Ok)

        self.resultLabel.setText(f"Success! Created {songsMade}")
        self.globalUpdater.update(GlobalUpdater.SONG_MENU)

    def new_playlist(self):
        new = Playlist.create_playlist("New playlist", "", [], True)
        self.playlistMenu.edit_playlist(new)

