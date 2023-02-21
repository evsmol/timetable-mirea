from data import db_session
from data.models.update_time import UpdateTime


def get_time():
    db_sess = db_session.create_session()

    time = db_sess.query(UpdateTime).first()

    try:
        return time
    finally:
        db_sess.close()


def set_time(time):
    time = UpdateTime()
    time.date = time

    db_sess = db_session.create_session()

    db_sess.query(UpdateTime).first().delete()
    db_sess.add(time)

    db_sess.commit()

    try:
        return time
    finally:
        db_sess.close()
