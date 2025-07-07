import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QSplitter, QHBoxLayout, \
    QCheckBox, QScrollArea, QWidget, QPushButton, QFileDialog
from gui.blocks.pluginBlock import PluginBlock
from osop.filehandler import FileHandler
from plugins.pluginImporter import PluginImporter
from plugins.pluginInfo import PluginInfo
from plugins.pluginOrder import PluginOrder


class PluginEditor(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Manage Plugins/Styles")
        self.setModal(True)

        self.myLayout = QVBoxLayout()
        self.infoLabel = QLabel("Manage, view, or add plugins here.\n\n"
                                "Plugins - plugins directly modify the behavior of OpenMusic, adding new functionalities and/or modifying existing ones. WARNING: since plugins directly modify the code, they have the SAME PERMISSIONS AND CAPABILITIES as OpenMusic and can cause significant damage to OpenMusic or your system. As a result, make sure you verify the plugins you use.\n\n"
                                "Styles - styles are a special type of plugin that do not change the behavior of OpenMusic but merely change how it looks. Styles are applied in order from the top of the list to the bottom of the list."
                                ""
                                ""
                    )
        self.infoLabel.setWordWrap(True)
        self.myLayout.addWidget(self.infoLabel)

        self.buttonsLayout = QHBoxLayout()
        self.importFolder = QPushButton("Import Plugin from Folder")
        self.importFolder.clicked.connect(self.request_folder)
        self.buttonsLayout.addWidget(self.importFolder)
        self.importZip = QPushButton("Import Plugin from .zip file")
        self.importZip.clicked.connect(self.request_zip)
        self.buttonsLayout.addWidget(self.importZip)
        self.openFolder = QPushButton("Open Plugin Folder")
        self.openFolder.clicked.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(FileHandler.PLUGINS)))
        self.buttonsLayout.addWidget(self.openFolder)
        self.myLayout.addLayout(self.buttonsLayout)

        self.splitter = QSplitter()
        self.pluginLayout = QVBoxLayout()
        self.checkboxes = {}
        for i in PluginInfo.plugins:
            hori = QHBoxLayout()
            hori.setAlignment(Qt.AlignmentFlag.AlignLeft)
            widget = PluginBlock(i)
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(lambda state, song=i: self.handle_checkbox(state, song))
            hori.addWidget(checkbox)
            hori.addWidget(widget)
            if PluginOrder.get_enabled(i):
                checkbox.toggle()

            self.checkboxes[i] = checkbox
            self.pluginLayout.addLayout(hori)

        self.pluginsWidget = QWidget()
        self.pluginsWidget.setLayout(self.pluginLayout)
        self.pluginScrollArea = QScrollArea()
        self.pluginScrollArea.setWidget(self.pluginsWidget)
        self.splitter.addWidget(self.pluginScrollArea)

        self.uidWidget = {}
        self.uidPluginWidget = {}
        self.list_widget = QListWidget()

        # Enable drag and drop for reordering
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setDefaultDropAction(Qt.MoveAction)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        for i in PluginOrder.order:
            item = QListWidgetItem()
            plugin_widget = PluginBlock(i)
            item.setSizeHint(plugin_widget.sizeHint())
            self.uidWidget[i] = item
            self.uidPluginWidget[i] = plugin_widget
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, plugin_widget)

        self.list_widget.model().rowsMoved.connect(self.save)

        self.splitter.addWidget(self.list_widget)
        self.myLayout.addWidget(self.splitter)

        self.setLayout(self.myLayout)

    def handle_checkbox(self, state, plugin_uid):
        if not state:
            self.list_widget.removeItemWidget(self.uidWidget[plugin_uid])
            for i in range(self.list_widget.count()):
                item = self.list_widget.item(i)
                if self.uidWidget[plugin_uid] == item:
                    self.list_widget.takeItem(i)
                    break
            self.uidPluginWidget[plugin_uid].deleteLater()
            del self.uidWidget[plugin_uid]
            del self.uidPluginWidget[plugin_uid]

        else:
            item = QListWidgetItem()
            plugin_widget = PluginBlock(plugin_uid)
            item.setSizeHint(plugin_widget.sizeHint())
            self.uidWidget[plugin_uid] = item
            self.uidPluginWidget[plugin_uid] = plugin_widget
            self.list_widget.addItem(item)
            self.list_widget.setItemWidget(item, plugin_widget)

        self.save()

    def save(self):
        for i in PluginInfo.plugins:
            PluginOrder.enabled[i] = self.checkboxes[i].isChecked()

        PluginOrder.order = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            PluginOrder.order.append(self.list_widget.itemWidget(item).uid)
        PluginOrder.save()

    def request_folder(self):
        folderName = QFileDialog.getExistingDirectory(self, "Open File", str(os.path.expanduser("~")))
        if folderName != "":
            PluginImporter.import_plugin(folderName)

    def request_zip(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Zipped File (*.zip)")
        fileName = fileName[0]
        if fileName != "":
            PluginImporter.import_plugin(fileName)

    def reload_plugin_list(self):
        self.pluginLayout = QVBoxLayout()
        for i in PluginInfo.plugins:
            hori = QHBoxLayout()
            hori.setAlignment(Qt.AlignmentFlag.AlignLeft)
            widget = PluginBlock(i)
            checkbox = QCheckBox()
            checkbox.stateChanged.connect(lambda state, song=i: self.handle_checkbox(state, song))
            if PluginOrder.get_enabled(i):
                checkbox.toggle()

            self.checkboxes[i] = checkbox
            hori.addWidget(checkbox)
            hori.addWidget(widget)
            self.pluginLayout.addLayout(hori)

        self.pluginsWidget.setLayout(self.pluginLayout)