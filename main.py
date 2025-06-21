import sys

from PySide6.QtWidgets import QApplication

from osop.filehandler import FileHandler
from PySide6.QtCore import QTimer

from gui.mainGui import MainGui
from osop.osplayer import OSPlayer
from util.playlist import Playlist
from library.songLibrary import SongLibrary

app = QApplication(sys.argv)
FileHandler.check_folder()
playlist = Playlist.load("0a4543711e9448f59c43e70940d9dde8")

player = OSPlayer()

songs = SongLibrary.retrieve_songs()
# a = VideoDownload("undertale ost 071", search=True)
# a.download()
# print(a.uid)

gui_timer = QTimer()
gui_timer.timeout.connect(player.update)
gui_timer.start(50)

widget = MainGui(player)
gui_update_timer = QTimer()
gui_update_timer.timeout.connect(widget.update_subs)
gui_update_timer.start(50)

widget.show()

app.exec()