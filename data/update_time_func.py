from datetime import datetime

from data import db_session
from data.models.update_time import UpdateTime

from logging_func import logging


def get_time():
    db_sess = db_session.create_session()

    # получение времени
    time = db_sess.query(UpdateTime).first()

    try:
        return time.update_date, time.start_date, time.finish_date
    except AttributeError:
        return
    finally:
        db_sess.close()


def set_time(update_time, start_time, finish_time):
    db_sess = db_session.create_session()

    logging(datetime.now(), 'INFO_DB',
            f'Обновление БД учёта времени: '
            f'время загрузки расписания «{update_time}», '
            f'дата начала семестра «{start_time}», '
            f'дата окончания семестра «{finish_time}»')

    # очистка таблицы
    if db_sess.query(UpdateTime).first():
        db_sess.query(UpdateTime).delete()

    # добавление новых значений
    time = UpdateTime()
    time.update_date = update_time
    time.start_date = start_time
    time.finish_date = finish_time

    db_sess.add(time)

    db_sess.commit()

    try:
        pass
    finally:
        db_sess.close()
