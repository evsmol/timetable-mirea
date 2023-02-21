from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QWidget
from PyQt6.QtWidgets import QGridLayout, QStatusBar, QToolBar, \
    QLabel, QPushButton, QListWidget, QListWidgetItem

from config import VERSION

from data.update_time_func import get_time


class MainForm(QMainWindow):
    """Класс основного окна программы."""

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(f'Учебное расписание РТУ МИРЭА (v{VERSION})')

        self.layout = QGridLayout()

        self.list = QListWidget()
        self.layout.addWidget(self.list, 0, 0, 3, 3)
        self.layout.addWidget(QListWidget(), 3, 0, 3, 3)

        self.layout.addWidget(QPushButton('Применить'), 6, 0, 1, 3)

        time = get_time()
        if time is None:
            time = '<i>расписание не загружалось</i>'
        self.labelUpdate = QLabel(f'Последнее обновление расписания: {time}')
        self.labelUpdate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.labelUpdate, 6, 3, 1, 6)

        day_list = [QListWidget() for _ in range(36)]
        counter = 0
        for i in range(6):
            for j in range(3, 9):
                self.layout.addWidget(day_list[counter], i, j)
                counter += 1

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)