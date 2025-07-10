import os

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QDesktopServices, QAction
from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QListWidget, QListWidgetItem, QSplitter, QHBoxLayout, \
    QCheckBox, QScrollArea, QWidget, QPushButton, QFileDialog, QMessageBox, QMenu
from gui.blocks.pluginBlock import PluginBlock
from osop.filehandler import FileHandler
from plugins.pluginInfo import PluginInfo


class PluginEditor(QDialog):
    def __init__(self, parent):
        super().__init__(parent)
        self.setWindowTitle("Manage Plugins/Styles")
        self.setModal(True)
        self.uidWidget = {}
        self.uidPluginWidget = {}
        self.list_widget = QListWidget()

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
        self.reload = QPushButton("Reload styles")
        self.reload.clicked.connect(lambda: PluginInfo.reload_style())
        self.buttonsLayout.addWidget(self.reload)
        self.myLayout.addLayout(self.buttonsLayout)

        self.reloadAndDragInfo = QLabel("To reload plugins/see the effects of your changes in plugins, you must close and reopen OpenMusic.\nTo activate a plugin, press its checkmark on the left. \nUse the right reordering side to reorder the order in which styles are applied (code plugins are not affected by this)")
        self.myLayout.addWidget(self.reloadAndDragInfo)
        self.splitter = QSplitter()

        self.pluginLayout = QVBoxLayout()
        self.checkboxes = {}
        self.pluginsWidget = QWidget()
        self.pluginsWidget.setLayout(self.pluginLayout)
        self.reload_plugin_list()

        self.pluginScrollArea = QScrollArea()
        self.pluginScrollArea.setWidget(self.pluginsWidget)
        self.splitter.addWidget(self.pluginScrollArea)

        # Enable drag and drop for reordering
        self.list_widget.setDragDropMode(QListWidget.InternalMove)
        self.list_widget.setDefaultDropAction(Qt.MoveAction)
        self.list_widget.setSelectionMode(QListWidget.SingleSelection)
        for i in PluginInfo.order:
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
        x = self.size().toTuple()[0]
        self.splitter.setSizes([x/2, x/2])

        self.setLayout(self.myLayout)

    def open_plugin_context(self, pos, uid):
        menu = QMenu(self)

        # Add actions to the menu
        edit_action = QAction("Open Folder", self)
        edit_action.triggered.connect(lambda: QDesktopServices.openUrl(QUrl.fromLocalFile(os.path.join(FileHandler.PLUGINS, uid))))
        menu.addAction(edit_action)

        delete_action = QAction("Delete", self)
        delete_action.triggered.connect(lambda: self.delete_plugin(uid))
        menu.addAction(delete_action)

        sender_widget = self.sender()
        if isinstance(sender_widget, PluginBlock):
            # Map the position from the sender widget to global coordinates
            global_pos = sender_widget.mapToGlobal(pos)
            menu.exec(global_pos)
        else:
            # Fallback to current behavior if sender isn't available
            menu.exec(self.mapToGlobal(pos))

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
            PluginInfo.enabled[i] = self.checkboxes[i].isChecked()

        PluginInfo.order = []
        for i in range(self.list_widget.count()):
            item = self.list_widget.item(i)
            PluginInfo.order.append(self.list_widget.itemWidget(item).uid)
        PluginInfo.save()

    def request_folder(self):
        folderName = QFileDialog.getExistingDirectory(self, "Open File", str(os.path.expanduser("~")))
        if folderName != "":
            PluginInfo.import_plugin(folderName)
            self.reload_plugin_list()

    def request_zip(self):
        fileName = QFileDialog.getOpenFileName(self, "Open File", str(os.path.expanduser("~")),"Zipped File (*.zip)")
        fileName = fileName[0]
        if fileName != "":
            PluginInfo.import_plugin(fileName)
            self.reload_plugin_list()

    def clear_layout(self, layout):
        while layout.count():
            child = layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                self.clear_layout(child.layout())
                child.layout().deleteLater()

    def reload_plugin_list(self):
        self.checkboxes = {}
        while self.pluginLayout.count():
            child = self.pluginLayout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()
            elif child.layout():
                # Recursively delete nested layouts
                self.clear_layout(child.layout())
                child.layout().deleteLater()

        for i in PluginInfo.plugins:
            hori = QHBoxLayout()
            hori.setAlignment(Qt.AlignmentFlag.AlignLeft)
            widget = PluginBlock(i)
            widget.right_click.connect(self.open_plugin_context)
            checkbox = QCheckBox()
            if PluginInfo.get_enabled(i):
                checkbox.toggle()

            checkbox.stateChanged.connect(lambda state, song=i: self.handle_checkbox(state, song))
            self.checkboxes[i] = checkbox
            hori.addWidget(checkbox)
            hori.addWidget(widget)
            self.pluginLayout.addLayout(hori)

        self.pluginsWidget.updateGeometry()
        self.pluginsWidget.update()
        self.pluginLayout.update()

    def delete_plugin(self, uid):
        message = QMessageBox.critical(self, "Really delete?", f"Really delete plugin {PluginInfo.info[uid]["name"]}? This action is irreversible", QMessageBox.Ok | QMessageBox.Cancel)
        if message == QMessageBox.Ok:
            PluginInfo.delete_plugin(uid)
            if uid in self.uidWidget.keys():
                self.list_widget.removeItemWidget(self.uidWidget[uid])
                for i in range(self.list_widget.count()):
                    item = self.list_widget.item(i)
                    if self.uidWidget[uid] == item:
                        self.list_widget.takeItem(i)
                        break
                self.uidPluginWidget[uid].deleteLater()
                del self.uidWidget[uid]
                del self.uidPluginWidget[uid]
            self.reload_plugin_list()
