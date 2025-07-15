import sys
import platform
from PySide6.QtWidgets import QApplication

from osop.filehandler import FileHandler
from PySide6.QtCore import QTimer

from gui.mainGui import MainGui
from plugins.pluginInfo import PluginInfo
from plugins.pluginManager import PluginManager

# Discover all plugins and their information, but don't load them yet
PluginManager.discover_plugins()
PluginInfo.get_plugins_info()
PluginInfo.load_save()

app = QApplication(sys.argv)

# Makes sure all folders exist in App Support
FileHandler.check_folder()

# Load appropriate OS Player
if platform.system() == "Darwin":
    from osop.osPlayers.macos import MacOSPlayer
    player = MacOSPlayer()

elif platform.system() == "Windows":
    from osop.osPlayers.windows import WindowsPlayer
    player = WindowsPlayer()

else:
    print("OpenMusic currently only supports MacOS and Windows. Check back later for further support!")
    sys.exit()

# Set up "loops" for all constant update functions
player_timer = QTimer()
player_timer.timeout.connect(player.update)
player_timer.start(50)

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

# Start app
widget.show()
app.exec()