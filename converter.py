from openpyxl import load_workbook
from pandas import date_range

from datetime import datetime


def get_timetable(file, day_start, date_end):
    # загрузка книги
    workbook = load_workbook(file)
    worksheet = workbook.active

    # создание списка строк страницы
    worksheet_list = list()
    for row in worksheet.rows:
        worksheet_list.append(row)

    # список с расписанием
    # (неделя, день, группа, пара, дисциплина, вид, преподаватель, аудитория)
    timelist = list()

    # список с датами
    start_date = datetime.strptime(day_start, "%d.%m.%Y")
    end_date = datetime.strptime(date_end, "%d.%m.%Y")
    dates = date_range(
        min(start_date, end_date),
        max(start_date, end_date)
    ).strftime('%d.%m.%Y %W %w').tolist()

    # заполнение списка
    for col in range(0, len(worksheet_list[1])):
        # получение значения ячейки
        cell = worksheet_list[1][col].value

        # проверка ячейки на соответствие номеру группы
        if cell is None or len(str(cell)) != 10 or len(cell.split('-')) != 3:
            continue

        # исключение аспирантуры
        if cell.split('-')[0][2] == 'А':
            return []

        # получение расписания
        pair_number = None
        week_day = None
        for row in range(3, 87):
            # номер пары
            if worksheet_list[row][1].value:
                pair_number = int(worksheet_list[row][1].value)

            # день недели
            if worksheet_list[row][0].value:
                if worksheet_list[row][0].value == 'ПОНЕДЕЛЬНИК':
                    week_day = 1
                elif worksheet_list[row][0].value == 'ВТОРНИК':
                    week_day = 2
                elif worksheet_list[row][0].value == 'СРЕДА':
                    week_day = 3
                elif worksheet_list[row][0].value == 'ЧЕТВЕРГ':
                    week_day = 4
                elif worksheet_list[row][0].value == 'ПЯТНИЦА':
                    week_day = 5
                elif worksheet_list[row][0].value == 'СУББОТА':
                    week_day = 6

            if not worksheet_list[row][col].value:
                continue

            # номер недели
            week = 1 if worksheet_list[row][col - 1].value == 'I' \
                        or worksheet_list[row][col - 6].value == 'I' else 0
            # название дисциплины
            discipline = worksheet_list[row][col].value
            # тип занятия
            activity_type = worksheet_list[row][col + 1].value
            # преподаватель
            teacher = worksheet_list[row][col + 2].value
            if teacher is None:
                teacher = ''
            # аудитория
            auditorium = worksheet_list[row][col + 3].value

            # разделение пар-двоек
            if '\n' not in discipline:
                timelist.append((week, week_day,
                                 cell.strip(), pair_number,
                                 discipline.strip(), activity_type.strip(),
                                 teacher.strip(), auditorium.strip()))
            elif '\n' not in auditorium:
                timelist.append((week, week_day,
                                 cell.strip(), pair_number,
                                 discipline.split('\n')[0].strip(),
                                 activity_type.split('\n')[0].strip(),
                                 ' '.join(teacher.split()[:2]).strip(),
                                 auditorium.strip()))
                timelist.append((week, week_day,
                                 cell.strip(), pair_number,
                                 discipline.split('\n')[1].strip(),
                                 activity_type.split('\n')[1].strip(),
                                 ' '.join(teacher.split()[2:]).strip(),
                                 auditorium.strip()))
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
    timetable = []

    # начальная неделя семестра
    first_week = int(dates[0].split()[1])

    # заполнение таблицы
    for row in timelist:
        week, week_day, group, pair_number, discipline, activity_type, \
            teacher, auditorium = row

        # проход по датам
        for date in dates:
            date = (date.split()[0],
                    int(date.split()[1]),
                    int(date.split()[2]))
            # проверка на день
            if (date[1] - first_week + 1) % 2 == week and date[2] == week_day:
                discipline = row[4]
                # проверка на исключения
                if 'н. ' in discipline or 'н ' in discipline:
                    if 'кр.' in discipline or 'кр ' in discipline:
                        exception_weeks = tuple(map(
                            int,
                            discipline.split('н')[0].strip('кр. ').split(',')
                        ))
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

                timetable.append(dict([('date', date[0]),
                                       ('week', date[1] - first_week + 1),
                                       ('week_day', date[2]),
                                       ('group', group),
                                       ('pair_number', pair_number),
                                       ('discipline', discipline),
                                       ('activity_type', activity_type),
                                       ('teacher', teacher),
                                       ('auditorium', auditorium)]))

    workbook.save(file)
    workbook.close()
    return timetable
