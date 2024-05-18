import io

from PySide6.QtWebEngineWidgets import (
    QWebEngineView,
)
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
)


class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.web_view = QWebEngineView()
        self.setCentralWidget(self.web_view)
        self.setMinimumSize(640, 480)
        self.show()

    def plot(self, folium_map, title='Map Viewer'):
        html_data = io.BytesIO()
        folium_map.save(html_data, close_file=False)
        self.web_view.setHtml(html_data.getvalue().decode())
        self.setWindowTitle(title)


_app = QApplication()

# Holds references to created windows to prevent them from being garbage
# collected by Python
_windows = list()


def show():
    _app.exec()


def plot(*args, **kwargs):
    window = MainWindow()
    _windows.append(window)

    window.plot(*args, **kwargs)
