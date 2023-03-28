from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QTabWidget, QTableWidget
from PyQt6.QtGui import QIcon


class CheckForm(QMainWindow):
    """Класс окна проверки корректности расписания."""

    def __init__(self, MainForm):
        super().__init__()
        self.main_form = MainForm
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Проверка загруженного расписания')
        self.setWindowIcon(QIcon('image/check.png'))

        # создание виджетов
        self.tab = QTabWidget()

        self.widget_schedule = QMainWindow()
        self.widget_timetable = QMainWindow()

        self.tab.addTab(self.widget_schedule, 'Расписание по неделям')
        self.tab.addTab(self.widget_timetable, 'Расписание по датам')

        self.widget_schedule.setCentralWidget(QTableWidget())

        self.setCentralWidget(self.tab)
