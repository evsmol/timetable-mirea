from openpyxl import load_workbook
from pandas import date_range

from datetime import datetime

from timedict_pattern import get_timedict_pattern

# загрузка книги
workbook = load_workbook('test.xlsx', read_only=True)
worksheet = workbook.active

# создание списка строк страницы
worksheet_list = list()
for row in worksheet.rows:
    worksheet_list.append(row)

# словарь с расписанием
timedict = dict()

# список с датами
start_date = datetime(2023, 2, 9)
end_date = datetime(2023, 4, 23)

dates = date_range(
    min(start_date, end_date),
    max(start_date, end_date)
).strftime('%d/%m/%Y %W %w').tolist()

# заполнение словаря
for col in range(0, len(worksheet_list[1])):
    # получение значения ячейки
    cell = worksheet_list[1][col].value

    # проверка ячейки на соответствие номеру группы
    if cell is None or len(str(cell)) != 10 or len(cell.split('-')) != 3:
        continue

    # шаблон словаря расписания
    timedict[cell] = get_timedict_pattern()

    # получение расписания
    pair_number = None
    week_day = None
    for row in range(3, 87):
        if worksheet_list[row][1].value:
            pair_number = int(worksheet_list[row][1].value)

        if worksheet_list[row][0].value:
            week_day = worksheet_list[row][0].value.capitalize()

        if not worksheet_list[row][col].value:
            continue

        week = 'Нечётная' if worksheet_list[row][col - 1].value == 'I' else \
            'Чётная'
        discipline = worksheet_list[row][col].value
        activity_type = worksheet_list[row][col + 1].value
        teacher = worksheet_list[row][col + 2].value
        auditorium = worksheet_list[row][col + 3].value

        timedict[cell][week][week_day][pair_number] = {
            'Дисциплина': discipline,
            'Вид занятий': activity_type,
            'Преподаватель': teacher,
            'Аудитория': auditorium
        }

with open('test.json', 'w') as file:
    file.write(str(timedict))