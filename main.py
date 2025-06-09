import sys

from PySide6.QtWidgets import QApplication

from filehandler import FileHandler
from PySide6.QtCore import QTimer

from gui.mainGui import MainGui
from osplayer import OSPlayer
from playlist import Playlist
from songLibrary import SongLibrary

app = QApplication(sys.argv)
FileHandler.check_folder()
playlist = Playlist.load("0a4543711e9448f59c43e70940d9dde8")

player = OSPlayer()

songs = SongLibrary.retrieve_songs()
playlist = Playlist.create_playlist("all", "/Users/hanyangfliu/Regular.png", songs, True)
player.play(playlist)
# a = VideoDownload("undertale ost 071", search=True)
# a.download()
# print(a.uid)

gui_timer = QTimer()
gui_timer.timeout.connect(player.update)
gui_timer.start(50)

widget = MainGui()
widget.show()

app.exec()