from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QVBoxLayout
from util.playlist import Playlist


class PlaylistBlock(QWidget):
    clicked = Signal(str)
    right_click = Signal(tuple, str)
    def __init__(self, uid):
        super().__init__()
        self.uid = uid
        image_url, title = self.load_data()

        self.myLayout = QHBoxLayout()

        self.albumCover = QLabel()
        self.albumCover.setPixmap(QPixmap(image_url))
        self.albumCover.setMaximumSize(QSize(64, 64))
        self.albumCover.setScaledContents(True)
        self.myLayout.addWidget(self.albumCover)

        textLayout = QVBoxLayout()
        self.title = QLabel()
        self.title.setText(title)
        textLayout.addWidget(self.title)
        self.myLayout.addLayout(textLayout)

        self.setLayout(self.myLayout)

        self.setCursor(Qt.PointingHandCursor)
        self.setAttribute(Qt.WA_Hover)
        self.setMouseTracking(True)
        for child in self.findChildren(QLabel):
            child.setCursor(Qt.PointingHandCursor)

        self.setContextMenuPolicy(Qt.CustomContextMenu)  # Enable context menu
        self.customContextMenuRequested.connect(lambda pos: self.right_click.emit(pos, self.uid))


    def load_data(self):
        return Playlist.retrieve_quick_data(self.uid)

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
