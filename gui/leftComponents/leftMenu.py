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
        splitter = QSplitter(Qt.Vertical)

        self.osPlayer = osPlayer
        self.playlistMenu = PlaylistMenu(self.globalUpdater, osPlayer)

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
        self.songMenu = SongMenu(self.globalUpdater, osPlayer)
        scrollArea.setWidget(self.songMenu)
        topMenu.addLayout(hLayout)
        topMenu.addWidget(scrollArea)
        self.topWidget.setLayout(topMenu)
        splitter.addWidget(self.topWidget)

        self.bottomWidget = QWidget()
        bottomMenu = QVBoxLayout()


        hLayout = QHBoxLayout()
        top = QLabel()
        top.setText("Playlists")
        hLayout.addWidget(top)
        button = QPushButton()
        button.setText("New playlist")
        button.clicked.connect(self.new_playlist)
        hLayout.addWidget(button)

        self.playlistScrollArea = QScrollArea()
        self.playlistScrollArea.setWidget(self.playlistMenu)
        self.playlistScrollArea.setWidgetResizable(True)
        bottomMenu.addLayout(hLayout)
        bottomMenu.addWidget(self.playlistScrollArea)
        self.bottomWidget.setLayout(bottomMenu)
        splitter.addWidget(self.bottomWidget)

        self.myLayout.addWidget(splitter)
        self.setLayout(self.myLayout)
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
        self.modalLayout.addWidget(QLabel("Enter the naming pattern for your audio files. \nThe naming pattern must include all 3 of the following parameters:\n%s - song name; %a - artist name; %l - album name; \n%% - percent symbol; * - wild card section\nExample: /Users/EX/%s - %a (%l)**.mp3"))

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
        self.submitButton.clicked.connect(self.make_songs)
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
            Songs.make_song(self.songNameEdit.text().strip(), self.artistEdit.text().strip(), self.albumEdit.text().strip(),
                            self.image_file_label.text(), self.audio_file_label.text())
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
        self.audio_files_label.setText("\n".join(self.audio_files))
        self.multi_button_update()

    def request_images(self):
        fileNames = QFileDialog.getOpenFileNames(self, "Open Files", str(os.path.expanduser("~")),"Image (*.png)")
        self.image_files = fileNames[0]
        self.image_files_label.setText("\n".join(self.image_files))
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
        new = Playlist.create_playlist("New playlist", "/Users/hanyangliu/Regular.png", [], True)
        self.playlistMenu.edit_playlist(new)

