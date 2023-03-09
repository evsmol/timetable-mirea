from datetime import datetime

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QDateEdit
from PyQt6.QtGui import QIcon

from data.update_time_func import get_time, set_time
from data.filter_func import update_teacher, update_group


class DateForm(QMainWindow):
    """Класс окна выбора диапазона дат."""

    def __init__(self, MainForm):
        super().__init__()
        self.main_form = MainForm
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Загрузка расписания')
        self.setWindowIcon(QIcon('image/download.png'))
        self.setFixedSize(405, 174)

        # создание виджетов
        self.layout = QGridLayout()

        self.label_info = QLabel('Для корректного слияния учебного '
                                 'расписания и календаря\nнеобходимо указать '
                                 'даты начала и конца семестра.')
        self.layout.addWidget(self.label_info, 0, 0, 1, 2)

        self.label_space = QLabel(' ')
        self.layout.addWidget(self.label_space, 1, 0, 1, 2)

        self.label_start = QLabel('Введите дату начала семестра:')
        self.layout.addWidget(self.label_start, 2, 0, 1, 1)

        self.label_finsh = QLabel('Введите дату конца семестра:')
        self.layout.addWidget(self.label_finsh, 3, 0, 1, 1)

        time_start = datetime.now()
        time_finish = datetime.now()
        time = get_time()
        if time:
            time_start = datetime.strptime(time[1], '%d.%m.%Y')
            time_finish = datetime.strptime(time[2], '%d.%m.%Y')

        self.date_start = QDateEdit(QDate(time_start.year,
                                          time_start.month,
                                          time_start.day))
        self.layout.addWidget(self.date_start, 2, 1, 1, 1)

        self.date_finish = QDateEdit(QDate(time_finish.year,
                                           time_finish.month,
                                           time_finish.day))
        self.layout.addWidget(self.date_finish, 3, 1, 1, 1)

        self.accept_btn = QPushButton('Применить')
        self.accept_btn.clicked.connect(self.button_click_accept)
        self.layout.addWidget(self.accept_btn, 4, 0, 1, 2)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def button_click_accept(self):
        # обновление списков групп и преподавателей
        update_group()
        update_teacher()

        set_time(
            datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
            self.date_start.text(),
            self.date_finish.text()
        )

        self.main_form.update_dates()
        self.main_form.update_time_download()

        self.close()
