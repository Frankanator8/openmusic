from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout, QLayout

from filehandler import FileHandler


class PlaylistWidget(QWidget):
    clicked = Signal(str)
    right_click = Signal(tuple, str)
    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        image_url, title = self.load_data()

        self.layout = QHBoxLayout()
        self.albumCover = QLabel()
        self.albumCover.setPixmap(QPixmap(image_url))
        self.albumCover.setMaximumSize(QSize(64, 64))
        self.albumCover.setScaledContents(True)

        self.title = QLabel()
        self.title.setText(title)
        self.layout.addWidget(self.albumCover)

        textLayout = QVBoxLayout()
        textLayout.addWidget(self.title)
        self.layout.addLayout(textLayout)
        self.setLayout(self.layout)

        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        for child in self.findChildren(QLabel):
            child.setCursor(Qt.PointingHandCursor)

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Enable context menu
        self.customContextMenuRequested.connect(lambda pos: self.right_click.emit(pos, self.uid))


    def load_data(self):
        if self.uid != "":
            image_url = f"{FileHandler.PLAYLIST_DATA}/{self.uid}.png"
            with open(f"{FileHandler.PLAYLIST_DATA}/{self.uid}.txt") as f:
                title = f.readline()

        else:
            image_url = "img/x.png"
            title = "(no playlist)"

        return image_url, title

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit(self.uid)
        elif event.button() == Qt.RightButton:
            return event.accept()
        super().mousePressEvent(event)  # Call parent class implementation

    def updateUID(self, uid):
        self.uid = uid
        image_url, title = self.load_data()
        self.albumCover.setPixmap(QPixmap(image_url))
        self.title.setText(title)
