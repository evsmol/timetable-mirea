from datetime import datetime, timedelta

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import QWidget, QMainWindow
from PyQt6.QtWidgets import QGridLayout, QLabel, QPushButton, QDateEdit, QMessageBox
from PyQt6.QtGui import QIcon

from data.update_time_func import get_time, set_time
from data.filter_func import update_teacher, update_group, update_auditorium, \
    load_group, load_teacher, load_auditorium

from files_func import update_db

from logging_func import logging


class DateForm(QMainWindow):
    """Класс окна выбора диапазона дат."""

    def __init__(self, MainForm):
        super().__init__()
        self.main_form = MainForm
        self.initUI()

    def initUI(self):
        logging(datetime.now(), 'WARNING',
                'Открытие формы загрузки расписания')

        self.setWindowTitle('Загрузка расписания')
        self.setWindowIcon(QIcon('image/download.png'))
        self.setFixedSize(414, 132)

        # создание виджетов
        self.layout = QGridLayout()

        # добавление информационного текста
        self.label_info = QLabel('Для корректного слияния учебного '
                                 'расписания и календаря\nнеобходимо указать '
                                 'дату начала семестра.')
        self.layout.addWidget(self.label_info, 0, 0, 1, 2)

        # добавление текста к виджету ввода даты
        self.label_start = QLabel('Введите дату начала семестра:')
        self.layout.addWidget(self.label_start, 2, 0, 1, 1)

        # получение ранее введённой даты начала семестра
        time_start = datetime.now()
        time = get_time()
        if time:
            time_start = datetime.strptime(time[1], '%d.%m.%Y')

        # добавление виджета ввода даты
        self.date_start = QDateEdit(QDate(time_start.year,
                                          time_start.month,
                                          time_start.day))
        self.layout.addWidget(self.date_start, 2, 1, 1, 1)

        # добавление подтверждающей кнопки
        self.accept_btn = QPushButton('Применить')
        self.accept_btn.clicked.connect(self.button_click_accept)
        self.layout.addWidget(self.accept_btn, 3, 0, 1, 2)

        self.widget = QWidget()
        self.widget.setLayout(self.layout)
        self.setCentralWidget(self.widget)

    def button_click_accept(self):
        logging(datetime.now(), 'INFO',
                'Нажата кнопка для загрузки расписания')

        # добавление уведомления о времени загрузки расписания
        message_box = QMessageBox()

        message_box.setText('Для загрузки расписания может потребоваться '
                            'некоторое время')
        message_box.addButton('Загрузить', QMessageBox.ButtonRole.ApplyRole)
        message_box.addButton('Отменить', QMessageBox.ButtonRole.RejectRole)

        ret = message_box.exec()

        # если нажата кнопка подтверждения
        if ret == 8:
            # обновление базы данных
            update_db(
                self.date_start.text(),
                (datetime.strptime(self.date_start.text(), '%d.%m.%Y')
                 + timedelta(112)).strftime('%d.%m.%Y')
            )

            # обновление списков групп и преподавателей
            update_group()
            update_teacher()
            update_auditorium()

            # загрузка списков групп и преподавателей
            load_group()
            load_teacher()
            load_auditorium()

            # обновление даты начала семестра
            set_time(
                datetime.now().strftime('%d.%m.%Y %H:%M:%S'),
                self.date_start.text(),
                (datetime.strptime(self.date_start.text(), '%d.%m.%Y')
                 + timedelta(112)).strftime('%d.%m.%Y')
            )

            # обновление загруженного расписания в основном окне программы
            self.main_form.update_dates()
            self.main_form.update_time_download()

            # обновление списков в основном окне программы
            self.main_form.update_lists()

            self.close()

    def closeEvent(self, event):
        logging(datetime.now(), 'WARNING',
                'Закрытие формы загрузки расписания')
