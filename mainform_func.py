from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QColor

from datetime import datetime


def fill_dates(day_list, dates):
    for day in day_list:
        day.clear()
    for i, lst_widget in enumerate(day_list):
        if dates[i].split(',')[0] == datetime.today().strftime('%d.%m.%Y'):
            item = QListWidgetItem(dates[i])
            item.setBackground(QColor('#926bff'))
            lst_widget.addItem(item)
        else:
            lst_widget.addItem(QListWidgetItem(dates[i]))
