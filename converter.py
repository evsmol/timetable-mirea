from openpyxl import load_workbook
from pandas import date_range

from datetime import datetime
import csv

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
end_date = datetime(2022, 12, 22)

dates = date_range(
    min(start_date, end_date),
    max(start_date, end_date)
).strftime('%d.%m.%Y %W %w').tolist()

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

        if '\n' not in discipline:
            timelist.append((week, week_day,
                             cell.strip(), pair_number,
                             discipline.strip(), activity_type.strip(),
                             teacher.strip(), auditorium.strip()))
        else:
            timelist.append((week, week_day,
                             cell.strip(), pair_number,
                             discipline.split('\n')[0].strip(),
                             activity_type.split('\n')[0].strip(),
                             ' '.join(teacher.split()[:2]).strip(),
                             auditorium.split('\n')[0].strip()))
            timelist.append((week, week_day,
                             cell.strip(), pair_number,
                             discipline.split('\n')[1].strip(),
                             activity_type.split('\n')[1].strip(),
                             ' '.join(teacher.split()[2:]).strip(),
                             auditorium.split('\n')[1].strip()))

# таблица с расписанием
timetable = [['date', 'week', 'week_day',
              'group', 'pair_number',
              'discipline', 'activity_type',
              'teacher', 'auditorium']]

# начальная неделя семестра
first_week = int(dates[0].split()[1])

# заполнение таблицы
for row in timelist:
    week, week_day, group, pair_number, discipline, activity_type, teacher, \
        auditorium = row

    # проход по датам
    for date in dates:
        date = (date.split()[0], int(date.split()[1]), int(date.split()[2]))
        # проверка на день
        if (date[1] - first_week + 1) % 2 == week and date[2] == week_day:
            discipline = row[4]
            # проверка на исключения
            if 'н. ' in discipline or 'н ' in discipline:
                if 'кр.' in discipline or 'кр ' in discipline:
                    exception_weeks = tuple(
                        map(int,
                            discipline.split('н')[0].strip('кр. ').split(','))
                    )
                    if (date[1] - first_week + 1) in exception_weeks:
                        continue

                elif '-' in discipline.split('н')[0]:
                    span = tuple(
                        map(int,
                            discipline.split('н')[0].strip().split('-'))
                    )
                    necessary_weeks = list(range(span[0], span[1] + 1))

                    if (date[1] - first_week + 1) not in necessary_weeks:
                        continue

                else:
                    necessary_weeks = tuple(
                        map(int,
                            discipline.split('н')[0].strip().split(','))
                    )
                    if (date[1] - first_week + 1) not in necessary_weeks:
                        continue

                discipline = 'н'.join(
                    discipline.split('н')[1:]
                ).lstrip('. ')

            timetable.append([date[0], date[1] - first_week + 1, date[2],
                              group, pair_number, discipline,
                              activity_type, teacher, auditorium])


with open('test.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(timetable)