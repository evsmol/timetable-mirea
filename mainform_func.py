from PyQt6.QtWidgets import QListWidgetItem
from PyQt6.QtGui import QColor, QIcon, QFont

from datetime import datetime

from data.schedule_func import get_group_pairs, get_teacher_pairs


def fill_dates(day_list, dates):
    for day in day_list:
        day.clear()
    for i, lst_widget in enumerate(day_list):
        item = QListWidgetItem(dates[i])
        if dates[i].split(',')[0] == datetime.today().strftime('%d.%m.%Y'):
            item.setBackground(QColor('#926bff'))
        else:
            item.setBackground(QColor('#4f4f4f'))
        lst_widget.addItem(item)


def get_pairs(groups_list, teachers_list):
    groups = []
    for group in groups_list:
        groups.append(get_group_pairs(group))

    teachers = []
    for teacher in teachers_list:
        teachers.append(get_teacher_pairs(teacher))

    return groups, teachers


def fill_pairs(groups_list, teachers_list, dates):
    dates_str = []
    for date in dates:
        dates_str.append(date.item(0).text().split(',')[0])

    for group in groups_list:
        for pair in group:
            for date in dates_str:
                if date == pair.date:
                    item = QListWidgetItem(f'{pair.group}\n'
                                           f'{pair.discipline}\n'
                                           f'{pair.teacher}')
                    item.setIcon(QIcon(f'image/group{pair.pair_number}.png'))
                    item.setFont(QFont('Arial', 10))
                    dates[dates_str.index(pair.date)].addItem(item)

    for teacher in teachers_list:
        for pair in teacher:
            for date in dates_str:
                if date == pair.date:
                    item = QListWidgetItem(f'{pair.teacher}\n'
                                           f'{pair.discipline}\n'
                                           f'{pair.group}')
                    item.setIcon(QIcon(f'image/teacher{pair.pair_number}.png'))
                    item.setFont(QFont('Arial', 10))
                    dates[dates_str.index(pair.date)].addItem(item)
