from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter, QScrollArea

from gui.songWidget import SongWidget


class LeftMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        splitter = QSplitter(Qt.Vertical)
        splitter.addWidget(SongWidget("7154757342874e538d44ee98c537a192"))
        splitter.addWidget(QScrollArea())
        self.layout.addWidget(splitter)
        self.setLayout(self.layout)