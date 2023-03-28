import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QPalette, QColor

from forms.MainForm import MainForm
from data import db_session


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == '__main__':
    db_session.global_init('db/timetable.db')

    app = QApplication(sys.argv)
    # app.setStyle('Fusion')

    form = MainForm()
    form.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
