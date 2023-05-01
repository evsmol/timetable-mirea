from datetime import datetime

from data import db_session
from data.models.schedule import Schedule

from logging_func import logging


def clear_table():
    db_sess = db_session.create_session()

    # очистка всеобщего расписания
    db_sess.query(Schedule).delete()

    db_sess.commit()

    try:
        pass
    finally:
        db_sess.close()


def add_pairs(timetable):
    db_sess = db_session.create_session()

    # добавление пар во всеобщее расписание
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
        pass
    finally:
        db_sess.close()


def get_group_pairs(group):
    db_sess = db_session.create_session()

    # получение пар нужной группы
    group_pairs = db_sess.query(Schedule).filter(
        Schedule.group == group
    ).order_by(Schedule.pair_number).all()

    try:
        return group_pairs
    finally:
        db_sess.close()


def get_teacher_pairs(teacher):
    db_sess = db_session.create_session()

    # получение пар нужного преподавателя
    teacher_pairs = db_sess.query(Schedule).filter(
        Schedule.teacher == teacher
    ).order_by(Schedule.pair_number).all()

    try:
        return teacher_pairs
    finally:
        db_sess.close()


def get_auditorium_pairs(auditorium):
    db_sess = db_session.create_session()

    # получение пар в нужной аудитории
    auditorium_pairs = db_sess.query(Schedule).filter(
        Schedule.auditorium == auditorium
    ).order_by(Schedule.pair_number).all()

    try:
        return auditorium_pairs
    finally:
        db_sess.close()
