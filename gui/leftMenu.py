from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QScrollArea, QLabel

from gui.songWidget import SongWidget
from gui.songmenu import SongMenu


class LeftMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)

        self.topWidget = QWidget()
        topMenu = QVBoxLayout()
        top = QLabel()
        top.setText("Song Library")
        scrollArea = QScrollArea()
        scrollArea.setWidget(SongMenu())
        topMenu.addWidget(top)
        topMenu.addWidget(scrollArea)
        self.topWidget.setLayout(topMenu)
        splitter.addWidget(self.topWidget)
        splitter.addWidget(QScrollArea())
        self.layout.addWidget(splitter)
        self.setLayout(self.layout)