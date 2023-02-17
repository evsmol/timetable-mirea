from PyQt6.QtWidgets import QMainWindow

from config import VERSION


class MainForm(QMainWindow):
    """Класс основного окна программы."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 378, 40)
        self.setWindowTitle(VERSION)