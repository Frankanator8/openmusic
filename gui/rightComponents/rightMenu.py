import math

from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QPushButton

from gui.blocks.playlistBlock import PlaylistBlock


class RightMenu(QWidget):
    def __init__(self, osPlayer):
        super().__init__()
        self.block_slider = False
        self.osPlayer = osPlayer
        self.myLayout = QVBoxLayout()

        self.image = QLabel()
        self.image.setPixmap(QPixmap("img/x.png"))
        self.image.setMinimumSize(QSize(256, 256))

        self.image.setMaximumSize(QSize(256, 256))
        self.image.setScaledContents(True)
        self.myLayout.addWidget(self.image)

        self.title = QLabel()
        self.title.setText("Select a song to play")
        self.myLayout.addWidget(self.title)
        self.artist = QLabel()
        self.artist.setText("Choose a song from either a\nplaylist or the song library")
        self.myLayout.addWidget(self.artist)
        self.album = QLabel()
        self.album.setText("Click the song's tile to play it")
        self.myLayout.addWidget(self.album)

        hLayout = QHBoxLayout()
        self.timeElapsed = QLabel()
        self.timeElapsed.setText("0:00")
        self.timeTotal = QLabel()
        self.timeTotal.setText("0:00")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.seek_time)

        self.playlistLabel = QLabel()
        self.playlistLabel.setText("Part of playlist:")
        self.playlistWidget = PlaylistBlock("")
        self.myLayout.addWidget(self.playlistLabel)
        self.myLayout.addWidget(self.playlistWidget)

        hLayout.addWidget(self.timeElapsed)
        hLayout.addWidget(self.slider)
        hLayout.addWidget(self.timeTotal)

        self.myLayout.addLayout(hLayout)

        hLayout2 = QHBoxLayout()
        self.playButton = QPushButton()
        self.playButton.setText("Play")
        self.playButton.clicked.connect(self.toggle_play)
        self.skipBackward = QPushButton()
        self.skipBackward.setText("<<")
        self.skipBackward.clicked.connect(self.previous_track)
        self.skipForward = QPushButton()
        self.skipForward.setText(">>")
        self.skipForward.clicked.connect(self.next_track)
        self.backward15 = QPushButton()
        self.backward15.setText("<15")
        self.backward15.clicked.connect(self.skip_backward)
        self.forward15 = QPushButton()
        self.forward15.setText("15>")
        self.forward15.clicked.connect(self.skip_forward)
        hLayout2.addWidget(self.playButton)
        hLayout2.addWidget(self.skipBackward)
        hLayout2.addWidget(self.skipForward)
        hLayout2.addWidget(self.backward15)
        hLayout2.addWidget(self.forward15)
        self.myLayout.addLayout(hLayout2)

        self.setLayout(self.myLayout)

    def update_gui(self):
        if self.osPlayer.player:
            self.block_slider = True
            self.title.setText(self.osPlayer.title)
            self.artist.setText(self.osPlayer.artist)
            self.album.setText(self.osPlayer.album)
            self.image.setPixmap(QPixmap(self.osPlayer.artwork_path))
            duration = self.osPlayer.duration
            self.timeTotal.setText(f"{math.floor(duration//60)}:{'0' if math.floor(duration%60) < 10 else ''}{math.floor(duration%60)}")
            time = self.osPlayer.player.currentTime()
            self.timeElapsed.setText(f"{math.floor(time//60)}:{'0' if math.floor(time%60) < 10 else ''}{math.floor(time%60)}")

            self.slider.setValue(time / duration * 1000)
            if not self.osPlayer.playing_song:
                if self.playlistWidget.uid != self.osPlayer.playlist.uid:
                    self.playlistWidget.updateUID(self.osPlayer.playlist.uid)
                self.playlistLabel.setText("Part of playlist:")

            else:
                self.playlistLabel.setText("Not a part of a playlist")
                self.playlistWidget.updateUID("")

            if self.osPlayer.paused:
                self.playButton.setText("Play")

            else:
                self.playButton.setText("Pause")

            if self.osPlayer.playing_song:
                self.skipBackward.setEnabled(False)
                self.skipForward.setEnabled(False)

            else:
                self.skipBackward.setEnabled(True)
                self.skipForward.setEnabled(True)

            self.block_slider = False
            self.playButton.setEnabled(True)
            self.forward15.setEnabled(True)
            self.backward15.setEnabled(True)

        else:
            self.playButton.setEnabled(False)
            self.forward15.setEnabled(False)
            self.backward15.setEnabled(False)
            self.skipForward.setEnabled(False)
            self.skipBackward.setEnabled(False)
            self.title.setText("Select a song to play")
            self.artist.setText("Choose a song from either a\nplaylist or the song library")
            self.album.setText("Click the song's tile to play it")
            self.playlistWidget.updateUID("")
            self.playlistLabel.setText("Not a part of a playlist")
            self.image.setPixmap(QPixmap("img/x.png"))

    def seek_time(self, value):
        if self.osPlayer.player and not self.block_slider:
            self.osPlayer.seek(value/1000 * self.osPlayer.duration)

    def toggle_play(self):
        if self.osPlayer.player:
            self.osPlayer.toggle_play_pause()

    def skip_backward(self):
        if self.osPlayer.player:
            self.osPlayer.skip_backward(15.0)

    def skip_forward(self):
        if self.osPlayer.player:
            self.osPlayer.skip_forward(15.0)

    def next_track(self):
        if self.osPlayer.player:
            self.osPlayer.next_track()

    def previous_track(self):
        if self.osPlayer.player:
            self.osPlayer.previous_track()