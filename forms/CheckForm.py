from datetime import datetime

from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QTabWidget, QTableWidget
from PySide6.QtGui import QIcon

from logging_func import logging


class CheckForm(QMainWindow):
    """Класс окна проверки корректности расписания."""

    def __init__(self, MainForm):
        super().__init__()
        self.main_form = MainForm
        self.initUI()

    def initUI(self):
        logging(datetime.now(), 'WARNING',
                'Открытие формы проверки корректности расписания')

        self.setWindowTitle('Проверка загруженного расписания')
        self.setWindowIcon(QIcon('image/check.png'))

        # создание виджетов
        self.tab = QTabWidget()

        # добавление страниц отображения
        self.widget_schedule = QMainWindow()
        self.widget_timetable = QMainWindow()

        # добавление табов
        self.tab.addTab(self.widget_schedule, 'Расписание по неделям')
        self.tab.addTab(self.widget_timetable, 'Расписание по датам')

        self.widget_schedule.setCentralWidget(QTableWidget())

        self.setCentralWidget(self.tab)

    def closeEvent(self, event):
        logging(datetime.now(), 'WARNING',
                'Закрытие формы проверки корректности расписания')
