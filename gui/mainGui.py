from PySide6.QtWidgets import *

from gui.leftMenu import LeftMenu


class MainGui(QWidget):
    def __init__(self, osPlayer):
        super().__init__()
        self.setWindowTitle("OpenMusic")
        self.showFullScreen()
        self.layout = QVBoxLayout()
        splitter = QSplitter()

        self.layout.addWidget(splitter)
        splitter.addWidget(LeftMenu(osPlayer))
        splitter.addWidget(QScrollArea())
        splitter.addWidget(QScrollArea())

        x = self.size().toTuple()[0]
        splitter.setSizes([x/4, 11*x/20, x/5])

        self.setLayout(self.layout)