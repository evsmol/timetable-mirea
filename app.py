import os
import sys
from datetime import datetime
import sqlite3

from PySide6.QtWidgets import QApplication
import qdarktheme

from forms.MainForm import MainForm
from data import db_session
from logging_func import logging


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)
    logging(datetime.now(), 'ERROR',
            f'Traceback: File "{traceback.tb_frame.f_code.co_filename}", '
            f'line {traceback.tb_lineno}, '
            f'in {traceback.tb_frame.f_code.co_name}; '
            f'{cls.__name__}: {exception}')


if __name__ == '__main__':
    logging(datetime.now(), 'INFO', 'Запуск программы!')

    # создание вспомогательных директорий
    if not os.path.isdir('files'):
        os.mkdir('files')
        logging(datetime.now(), 'INFO', 'Создание директории «files»')
    if not os.path.isdir('db'):
        os.mkdir('db')
        sqlite3.connect('db/timetable.db')
        logging(datetime.now(), 'INFO', 'Создание «db/timetable.db»')

    # подключение к базе данных
    db_session.global_init('db/timetable.db')

    # инициализация приложения
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    # открытие формы основного окна программы
    form = MainForm()
    form.show()
    sys.excepthook = except_hook
    try:
        sys.exit(app.exec())
    finally:
        logging(datetime.now(), 'WARNING', 'Завершение программы!')
