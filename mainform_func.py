from PyQt6.QtWidgets import QListWidgetItem


def fill_dates(day_list, dates):
    for day in day_list:
        day.clear()
    for i, lst_widget in enumerate(day_list):
        lst_widget.addItem(QListWidgetItem(dates[i]))
