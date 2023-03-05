from pandas import date_range

from datetime import datetime, timedelta

from data.update_time_func import get_time


def get_list_dates(dates):
    dates = list(filter(lambda x: x[-1] != '0', dates))

    time = get_time()
    if time is None:
        dates = [x.split()[0] for x in dates]
        return dates

    first_week = int(datetime.strptime(time[1], '%d.%m.%Y').strftime('%W'))
    print(dates)
    print(first_week)
    dates = [x.split()[0] + f', {(int(x.split()[1]) - first_week + 1) % 52} н.'
             for x in dates]
    return dates


def set_now_month():
    first_date = datetime.today().replace(day=1)

    start_date = first_date - timedelta(days=first_date.weekday())
    end_date = start_date + timedelta(days=41)

    dates = date_range(
            min(start_date, end_date),
            max(start_date, end_date)
        ).strftime('%d.%m.%Y %W %w').tolist()

    return get_list_dates(dates)


def set_previous_month(date):
    now_day = datetime.strptime(date.split(',')[0], '%d.%m.%Y')
    last_day = now_day - timedelta(days=20)

    first_date = last_day.replace(day=1)

    start_date = first_date - timedelta(days=first_date.weekday())
    end_date = start_date + timedelta(days=41)

    dates = date_range(
        min(start_date, end_date),
        max(start_date, end_date)
    ).strftime('%d.%m.%Y %W %w').tolist()

    return get_list_dates(dates)


def set_next_month(date):
    now_day = datetime.strptime(date.split(',')[0], '%d.%m.%Y')
    next_day = now_day + timedelta(days=35)

    first_date = next_day.replace(day=1)

    start_date = first_date - timedelta(days=first_date.weekday())
    end_date = start_date + timedelta(days=41)

    dates = date_range(
        min(start_date, end_date),
        max(start_date, end_date)
    ).strftime('%d.%m.%Y %W %w').tolist()

    return get_list_dates(dates)
