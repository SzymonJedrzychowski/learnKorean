from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal


class QLabelClickable(QLabel):
    """Clickable label class"""

    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()
