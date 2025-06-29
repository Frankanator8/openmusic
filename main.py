import sys

from PySide6.QtWidgets import QApplication

from osop.filehandler import FileHandler
from PySide6.QtCore import QTimer

from gui.mainGui import MainGui
from osop.osplayer import OSPlayer
from plugins.pluginManager import PluginManager

plugin_manager = PluginManager()
plugin_manager.discover_plugins()

app = QApplication(sys.argv)
FileHandler.check_folder()
player = OSPlayer()

gui_timer = QTimer()
gui_timer.timeout.connect(player.update)
gui_timer.start(50)

widget = MainGui(player)
gui_update_timer = QTimer()
gui_update_timer.timeout.connect(widget.update_subs)
gui_update_timer.start(50)

plugin_manager.create_payload(app, player, widget)
plugin_manager.load_plugins()

plugin_timer = QTimer()
plugin_timer.timeout.connect(plugin_manager.timer_update)
plugin_timer.start(50)

widget.show()

app.exec()