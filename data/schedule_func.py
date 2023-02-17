from data import db_session
from data.models.schedule import Schedule


def add_pairs(timetable):
    db_sess = db_session.create_session()

    objects = [
        Schedule(
            date=row['date'],
            week=row['week'],
            week_day=row['week_day'],
            group=row['group'],
            pair_number=row['pair_number'],
            discipline=row['discipline'],
            activity_type=row['activity_type'],
            teacher=row['teacher'],
            auditorium=row['auditorium']
        ) for row in timetable
    ]
    db_sess.bulk_save_objects(objects)

    db_sess.commit()

    try:
        return
    finally:
        db_sess.close()
