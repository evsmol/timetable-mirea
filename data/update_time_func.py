from data import db_session
from data.models.update_time import UpdateTime


def get_time():
    db_sess = db_session.create_session()

    time = db_sess.query(UpdateTime).first()

    try:
        return time.update_date, time.start_date, time.finish_date
    except AttributeError:
        return
    finally:
        db_sess.close()


def set_time(update_time, start_time, finish_time):
    time = UpdateTime()
    time.update_date = update_time
    time.start_date = start_time
    time.finish_date = finish_time

    db_sess = db_session.create_session()

    if db_sess.query(UpdateTime).first():
        db_sess.query(UpdateTime).delete()
    db_sess.add(time)

    db_sess.commit()

    try:
        return time
    finally:
        db_sess.close()
