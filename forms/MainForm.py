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

        self.statusBar = QStatusBar()
        self.setStatusBar(self.statusBar)
        time = get_time()
        if time is None:
            time = '<i>расписание не загружалось</i>'
        self.labelUpdate = QLabel(f'Последнее обновление расписания: {time}')
        self.labelUpdate.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.statusBar.addWidget(self.labelUpdate, 1)
        # self.group_list = QPushButton()
        #
        # self.layout = QGridLayout()
        # self.layout.addLayout(self.group_list, 0, 0)
        #
        # widget = QWidget()
        # widget.setLayout(self.layout)
        # self.setCentralWidget(widget)

        self.layout = QGridLayout()

        self.list = QListWidget()
        self.layout.addWidget(self.list, 0, 0, 3, 3)
        self.layout.addWidget(QListWidget(), 3, 0, 3, 3)
        # self.list.setModel(QtCore.QAbstractTableModel(['Нурлигареев Д.Х.', 'Коломийцева Е.А.']))

        self.layout.addWidget(QPushButton('Применить'), 6, 0, 1, 3)
        self.layout.addWidget(QPushButton('Пред. месяц'), 6, 3)
        self.layout.addWidget(QPushButton('След. месяц'), 6, 4)

        self.layout.addWidget(QListWidget(), 0, 3)
        self.layout.addWidget(QListWidget(), 0, 4)
        self.layout.addWidget(QListWidget(), 0, 5)
        self.layout.addWidget(QListWidget(), 0, 6)
        self.layout.addWidget(QListWidget(), 0, 7)
        self.layout.addWidget(QListWidget(), 0, 8)

        self.layout.addWidget(QListWidget(), 1, 3)
        self.layout.addWidget(QListWidget(), 1, 4)
        self.layout.addWidget(QListWidget(), 1, 5)
        self.layout.addWidget(QListWidget(), 1, 6)
        self.layout.addWidget(QListWidget(), 1, 7)
        self.layout.addWidget(QListWidget(), 1, 8)

        self.layout.addWidget(QListWidget(), 2, 3)
        self.layout.addWidget(QListWidget(), 2, 4)
        self.layout.addWidget(QListWidget(), 2, 5)
        self.layout.addWidget(QListWidget(), 2, 6)
        self.layout.addWidget(QListWidget(), 2, 7)
        self.layout.addWidget(QListWidget(), 2, 8)

        self.layout.addWidget(QListWidget(), 3, 3)
        self.layout.addWidget(QListWidget(), 3, 4)
        self.layout.addWidget(QListWidget(), 3, 5)
        self.layout.addWidget(QListWidget(), 3, 6)
        self.layout.addWidget(QListWidget(), 3, 7)
        self.layout.addWidget(QListWidget(), 3, 8)

        self.layout.addWidget(QListWidget(), 4, 3)
        self.layout.addWidget(QListWidget(), 4, 4)
        self.layout.addWidget(QListWidget(), 4, 5)
        self.layout.addWidget(QListWidget(), 4, 6)
        self.layout.addWidget(QListWidget(), 4, 7)
        self.layout.addWidget(QListWidget(), 4, 8)

        self.layout.addWidget(QListWidget(), 5, 3)
        self.layout.addWidget(QListWidget(), 5, 4)
        self.layout.addWidget(QListWidget(), 5, 5)
        self.layout.addWidget(QListWidget(), 5, 6)
        self.layout.addWidget(QListWidget(), 5, 7)
        self.layout.addWidget(QListWidget(), 5, 8)

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)