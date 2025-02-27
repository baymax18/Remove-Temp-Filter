from qgis.core import QgsProject, QgsVectorLayer
from qgis.PyQt.QtWidgets import QAction, QMessageBox

class RemoveTempFilterPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.action = None

    def initGui(self):
        """Initialize the plugin (create button and add to toolbar)"""
        icon_path = 'path/to/icon.png'  # Add the path to your plugin icon
        self.action = QAction("Remove Temporary Filters", self.iface.mainWindow())
        self.action.triggered.connect(self.remove_temp_filters)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Remove Temp Filter", self.action)

    def unload(self):
        """Remove the plugin's actions when unloading"""
        self.iface.removePluginMenu("&Remove Temp Filter", self.action)
        self.iface.removeToolBarIcon(self.action)

    def remove_temp_filters(self):
        """Remove temporary filters from all vector layers"""
        layers = QgsProject.instance().mapLayers().values()
        
        layers_with_removed_filters = []  # To keep track of layers whose filters were removed
        
        for layer in layers:
            if isinstance(layer, QgsVectorLayer):
                if layer.subsetString():
                    layer.setSubsetString("")  # Removes the filter
                    layers_with_removed_filters.append(layer.name())

        if layers_with_removed_filters:
            QMessageBox.information(self.iface.mainWindow(), 
                                    "Temporary Filters Removed", 
                                    f"Filters removed from layers: {', '.join(layers_with_removed_filters)}")
        else:
            QMessageBox.information(self.iface.mainWindow(),
                                    "No Filters Found", 
                                    "No temporary filters were found to remove.")

