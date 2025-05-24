import sys

from PySide6.QtWidgets import QApplication

from downloader import VideoDownload
from filehandler import FileHandler
from PySide6.QtCore import QTimer

from osplayer import OSPlayer
from playlist import Playlist

app = QApplication(sys.argv)
FileHandler.check_folder()
playlist = Playlist.load("0a4543711e9448f59c43e70940d9dde8")

player = OSPlayer()
player.play(playlist)

# a = VideoDownload("undertale ost 071", search=True)
# a.download()
# print(a.uid)

gui_timer = QTimer()
gui_timer.timeout.connect(player.update)
gui_timer.start(500)

app.exec()