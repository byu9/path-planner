import io

import folium
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow

from .query_provider import get_node_geometry


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        self.setMinimumSize(800, 600)
        self.setWindowTitle('Map Viewer')

        self._map = folium.Map(control_scale=True)

    def plot_path(self, nodes: list):
        geometries = [
            get_node_geometry(node)
            for node in nodes
        ]

        folium.PolyLine(geometries).add_to(self._map)

    def show(self):
        self._map.fit_bounds(self._map.get_bounds())
        html_data = io.BytesIO()
        self._map.save(html_data, close_file=False)
        self.web_view.setHtml(html_data.getvalue().decode())
        super().show()


_app = QApplication()

# Holds references to created windows to prevent them from being garbage
# collected by Python
_windows = list()


def figure():
    window = MainWindow()
    _windows.append(window)
    return window


def show():
    for window in _windows:
        window.show()

    _app.exec()
