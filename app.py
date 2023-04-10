import os
import sys
from PyQt6.QtWidgets import QApplication
import qdarktheme

import sqlite3

from forms.MainForm import MainForm
from data import db_session


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    if not os.path.isdir('files'):
        os.mkdir('files')
    if not os.path.isdir('db'):
        os.mkdir('db')
        sqlite3.connect('db/timetable.db')
    db_session.global_init('db/timetable.db')

    app = QApplication(sys.argv)
    qdarktheme.setup_theme()

    form = MainForm()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
