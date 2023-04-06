from PyQt6.QtCore import Qt
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
        item.__hash__ = 0
        lst_widget.addItem(item)


def get_pairs(groups_list, teachers_list):
    groups = []
    for group in groups_list:
        groups.append(get_group_pairs(group))

    teachers = []
    for teacher in teachers_list:
        teachers.append(get_teacher_pairs(teacher))

    return groups, teachers


def fill_pairs(groups_list, teachers_list, dates, parameters):
    parameters_items = [parameters.item(x) for x in range(parameters.count())]
    # ___, преподаватель, группа, аудитория, тип занятия, дисциплина, поток
    parameters_flag = [True
                       if x.checkState() == Qt.CheckState.Checked
                       else False
                       for x in parameters_items]

    dates_str = []
    for date in dates:
        dates_str.append(date.item(0).text().split(',')[0])

    for group in groups_list:
        for pair in group:
            text = []
            if parameters_flag[2]:
                text.append(pair.group)
            if parameters_flag[5]:
                text.append(pair.discipline)
            if parameters_flag[3] and parameters_flag[4]:
                text.append(f'{pair.auditorium}  ●  {pair.activity_type}')
            elif parameters_flag[3]:
                text.append(pair.auditorium)
            elif parameters_flag[4]:
                text.append(pair.activity_type)
            if parameters_flag[1]:
                text.append(pair.teacher)

            for date in dates_str:
                if date == pair.date:
                    item = QListWidgetItem('\n'.join(text))
                    item.__hash__ = pair.pair_number
                    icon = QIcon(f'image/group{pair.pair_number}.png')
                    item.setIcon(icon)
                    item.setFont(QFont('Arial', 10))
                    item.icon()
                    dates[dates_str.index(pair.date)].addItem(item)

    for teacher in teachers_list:
        for pair in teacher:
            text = []
            if parameters_flag[1]:
                text.append(pair.teacher)
            if parameters_flag[5]:
                text.append(pair.discipline)
            if parameters_flag[3] and parameters_flag[4]:
                text.append(f'{pair.auditorium}  ●  {pair.activity_type}')
            elif parameters_flag[3]:
                text.append(pair.auditorium)
            elif parameters_flag[4]:
                text.append(pair.activity_type)
            if parameters_flag[2]:
                text.append(pair.group)

            for date in dates_str:
                if date == pair.date:
                    item = QListWidgetItem('\n'.join(text))
                    item.__hash__ = pair.pair_number
                    icon = QIcon(f'image/teacher{pair.pair_number}.png')
                    item.setIcon(icon)
                    item.setFont(QFont('Arial', 10))
                    dates[dates_str.index(pair.date)].addItem(item)

    for date in dates_str:
        lst = dates[dates_str.index(date)]
        items = [lst.item(x) for x in range(lst.count())]
        for _ in range(lst.count()):
            lst.takeItem(0)
        items.sort(key=lambda x: x.__hash__)

        if parameters_flag[6]:
            new_items = []
            for i, item in enumerate(items):
                if i == 0:
                    new_items.append(item)
                    continue
                if len(new_items) > 1 and \
                        item.text().split('\n')[:-1] == \
                        new_items[-1].text().split('\n')[:-1] and \
                        item.__hash__ == new_items[-1].__hash__ and \
                        item.text().split('\n')[-1] != \
                        new_items[-1].text().split('\n')[-1]:
                    slash_n = '\n'
                    new_items[-1].setText(f'{new_items[-1].text()}, '
                                          f'{item.text().split(slash_n)[-1]}')
                else:
                    new_items.append(item)
            for item in new_items:
                lst.addItem(item)

        else:
            for item in items:
                lst.addItem(item)
