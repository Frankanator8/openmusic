import sys

from PySide6.QtWidgets import QApplication

from osop.filehandler import FileHandler
from PySide6.QtCore import QTimer

from gui.mainGui import MainGui
from osop.osplayer import OSPlayer
from util.playlist import Playlist
from util.songs import Songs

app = QApplication(sys.argv)
FileHandler.check_folder()
player = OSPlayer()

songs = Songs.retrieve_songs()
gui_timer = QTimer()
gui_timer.timeout.connect(player.update)
gui_timer.start(50)

widget = MainGui(player)
gui_update_timer = QTimer()
gui_update_timer.timeout.connect(widget.update_subs)
gui_update_timer.start(50)

widget.show()

app.exec()