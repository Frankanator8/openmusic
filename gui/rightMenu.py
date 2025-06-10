from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QSlider, QHBoxLayout, QPushButton

from gui.playlistWidget import PlaylistWidget


class RightMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.myLayout = QVBoxLayout()

        image = QLabel()
        image.setPixmap(QPixmap("/Users/hanyangliu/Regular.png"))
        image.setMaximumSize(QSize(256, 256))
        image.setScaledContents(True)
        self.myLayout.addWidget(image)

        self.title = QLabel()
        self.title.setText("Title goes here")
        self.myLayout.addWidget(self.title)
        self.artist = QLabel()
        self.artist.setText("Artist goes here")
        self.myLayout.addWidget(self.artist)
        self.album = QLabel()
        self.album.setText("Album goes here")
        self.myLayout.addWidget(self.album)

        hLayout = QHBoxLayout()
        self.timeElapsed = QLabel()
        self.timeElapsed.setText("0:00")
        self.timeTotal = QLabel()
        self.timeTotal.setText("0:00")
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0, 1000)
        self.slider.setValue(0)

        label = QLabel()
        label.setText("Part of playlist:")
        self.myLayout.addWidget(label)
        self.myLayout.addWidget(PlaylistWidget("0a4543711e9448f59c43e70940d9dde8"))

        hLayout.addWidget(self.timeElapsed)
        hLayout.addWidget(self.slider)
        hLayout.addWidget(self.timeTotal)

        self.myLayout.addLayout(hLayout)

        hLayout2 = QHBoxLayout()
        self.playButton = QPushButton()
        self.playButton.setText("Play")
        self.skipBackward = QPushButton()
        self.skipBackward.setText("<<")
        self.skipForward = QPushButton()
        self.skipForward.setText(">>")
        self.backward15 = QPushButton()
        self.backward15.setText("<15")
        self.forward15 = QPushButton()
        self.forward15.setText("15>")
        hLayout2.addWidget(self.playButton)
        hLayout2.addWidget(self.skipBackward)
        hLayout2.addWidget(self.skipForward)
        hLayout2.addWidget(self.backward15)
        hLayout2.addWidget(self.forward15)
        self.myLayout.addLayout(hLayout2)

        self.setLayout(self.myLayout)