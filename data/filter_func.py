from data import db_session
from data.models.group import Group
from data.models.teacher import Teacher
from data.models.schedule import Schedule


def load_group():
    db_sess = db_session.create_session()

    groups = db_sess.query(Group).all()

    try:
        return groups
    finally:
        db_sess.close()


def load_teacher():
    db_sess = db_session.create_session()

    teachers = db_sess.query(Teacher).all()

    try:
        return teachers
    finally:
        db_sess.close()


def update_group():
    db_sess = db_session.create_session()

    if db_sess.query(Group).first():
        db_sess.query(Group).delete()

    groups = db_sess.query(Schedule).all()

    groups_list = list(set([x.group for x in groups]))

    objects = [Group(group=x, selected=True) for x in groups_list]
    db_sess.bulk_save_objects(objects)

    db_sess.commit()

    try:
        return objects
    finally:
        db_sess.close()


def update_teacher():
    db_sess = db_session.create_session()

    if db_sess.query(Teacher).first():
        db_sess.query(Teacher).delete()

    teachers = db_sess.query(Schedule).all()

    teachers_list = list(set([x.teacher for x in teachers]))

    objects = [Teacher(teacher=x, selected=True) for x in teachers_list]
    db_sess.bulk_save_objects(objects)

    db_sess.commit()

    try:
        return objects
    finally:
        db_sess.close()
