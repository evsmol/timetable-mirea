from pandas import date_range

from datetime import datetime, timedelta


def set_now_month():
    first_date = datetime.today().replace(day=1)

    start_date = first_date - timedelta(days=first_date.weekday())
    end_date = start_date + timedelta(days=41)

    dates = date_range(
            min(start_date, end_date),
            max(start_date, end_date)
        ).strftime('%d.%m.%Y, %W н. %w').tolist()

    dates = list(filter(lambda x: x[-1] != '0', dates))
    dates = [x[:-2] for x in dates]

    return dates


def set_previous_month(date):
    now_day = datetime.strptime(date.split(',')[0], '%d.%m.%Y')
    last_day = now_day - timedelta(days=15)

    first_date = last_day.replace(day=1)

    start_date = first_date - timedelta(days=first_date.weekday())
    end_date = start_date + timedelta(days=41)

    dates = date_range(
        min(start_date, end_date),
        max(start_date, end_date)
    ).strftime('%d.%m.%Y, %W н. %w').tolist()

    dates = list(filter(lambda x: x[-1] != '0', dates))
    dates = [x[:-2] for x in dates]

    return dates


def set_next_month(date):
    now_day = datetime.strptime(date.split(',')[0], '%d.%m.%Y')
    next_day = now_day + timedelta(days=15)

    first_date = next_day.replace(day=1)

    start_date = first_date - timedelta(days=first_date.weekday())
    end_date = start_date + timedelta(days=41)

    dates = date_range(
        min(start_date, end_date),
        max(start_date, end_date)
    ).strftime('%d.%m.%Y, %W н. %w').tolist()

    dates = list(filter(lambda x: x[-1] != '0', dates))
    dates = [x[:-2] for x in dates]

    return dates