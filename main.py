import sys

from PySide6.QtWidgets import QApplication

from osop.filehandler import FileHandler
from PySide6.QtCore import QTimer

from gui.mainGui import MainGui
from osop.osplayer import OSPlayer
from plugins.pluginInfo import PluginInfo
from plugins.pluginManager import PluginManager
from plugins.pluginOrder import PluginOrder

PluginManager.discover_plugins()
PluginInfo.get_plugins_info()
PluginOrder.load_save()

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

PluginManager.create_payload(app, player, widget)
PluginManager.load_plugins()
PluginManager.load_styles()
PluginManager.on_launch()

plugin_timer = QTimer()
plugin_timer.timeout.connect(PluginManager.timer_update)
plugin_timer.start(50)

widget.show()

app.exec()