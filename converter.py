from openpyxl import load_workbook
from pandas import date_range

from datetime import datetime

# загрузка книги
workbook = load_workbook('test.xlsx', read_only=True)
worksheet = workbook.active

# создание списка строк страницы
worksheet_list = list()
for row in worksheet.rows:
    worksheet_list.append(row)

# список с расписанием
# (неделя, день, группа, пара, дисциплина, вид, преподаватель, аудитория)
timelist = list()

# список с датами
start_date = datetime(2022, 9, 1)
end_date = datetime(2023, 12, 22)

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

    # получение расписания
    pair_number = None
    week_day = None
    for row in range(3, 87):
        if worksheet_list[row][1].value:
            pair_number = int(worksheet_list[row][1].value)

        if worksheet_list[row][0].value:
            match worksheet_list[row][0].value:
                case 'ПОНЕДЕЛЬНИК':
                    week_day = 1
                case 'ВТОРНИК':
                    week_day = 2
                case 'СРЕДА':
                    week_day = 3
                case 'ЧЕТВЕРГ':
                    week_day = 4
                case 'ПЯТНИЦА':
                    week_day = 5
                case 'СУББОТА':
                    week_day = 6

        if not worksheet_list[row][col].value:
            continue

        week = 1 if worksheet_list[row][col - 1].value == 'I' else 0
        discipline = worksheet_list[row][col].value
        activity_type = worksheet_list[row][col + 1].value
        teacher = worksheet_list[row][col + 2].value
        auditorium = worksheet_list[row][col + 3].value

        timelist.append((week, week_day,
                         cell, pair_number,
                         discipline, activity_type,
                         teacher, auditorium))

# таблица с расписанием
timetable = [['date', 'week', 'week_day',
              'group', 'pair_number',
              'discipline', 'activity_type',
              'teacher', 'auditorium']]

first_week = int(dates[0].split()[1])

normal_disciplines = list(
    filter(lambda x: 'н. ' not in x[4] and 'н ' not in x[4], timelist)
)
exceptional_disciplines = list(
    filter(lambda x: 'н. ' in x[4] or 'н ' in x[4], timelist)
)
print(timelist)
