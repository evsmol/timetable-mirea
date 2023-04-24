from PyQt6.QtCore import Qt

from data import db_session
from data.models.group import Group
from data.models.teacher import Teacher
from data.models.auditorium import Auditorium
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


def load_auditorium():
    db_sess = db_session.create_session()

    auditoriums = db_sess.query(Auditorium).all()

    try:
        return auditoriums
    finally:
        db_sess.close()


def update_group():
    db_sess = db_session.create_session()

    if db_sess.query(Group).first():
        db_sess.query(Group).delete()

    groups = db_sess.query(Schedule).all()

    groups_list = sorted(
        list(set([x.group for x in groups])),
        key=lambda x: (x.split('-')[0], x.split('-')[2], x.split('-')[1])
    )

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

    teachers_list = sorted(list(set([x.teacher for x in teachers])))

    objects = [Teacher(teacher=x, selected=True) for x in teachers_list]
    db_sess.bulk_save_objects(objects)

    db_sess.commit()

    try:
        return objects
    finally:
        db_sess.close()


def update_auditorium():
    db_sess = db_session.create_session()

    if db_sess.query(Auditorium).first():
        db_sess.query(Auditorium).delete()

    auditoriums = db_sess.query(Schedule).all()

    auditoriums_list = sorted(list(set([x.auditorium for x in auditoriums])))

    objects = [Auditorium(auditorium=x, selected=True)
               for x in auditoriums_list]
    db_sess.bulk_save_objects(objects)

    db_sess.commit()

    try:
        return objects
    finally:
        db_sess.close()


def change_group(items):
    db_sess = db_session.create_session()

    for item in items:
        group = db_sess.query(Group).filter(
            Group.group == item.text()
        ).first()
        if item.checkState() == Qt.CheckState.Checked:
            group.selected = True
        else:
            group.selected = False

        db_sess.add(group)
        db_sess.flush()
        db_sess.refresh(group)

    db_sess.commit()

    try:
        return
    finally:
        db_sess.close()


def change_teacher(items):
    db_sess = db_session.create_session()

    for item in items:
        teacher = db_sess.query(Teacher).filter(
            Teacher.teacher == item.text()
        ).first()
        if item.checkState() == Qt.CheckState.Checked:
            teacher.selected = True
        else:
            teacher.selected = False

        db_sess.add(teacher)

    db_sess.commit()

    try:
        return
    finally:
        db_sess.close()


def change_auditorium(items):
    db_sess = db_session.create_session()

    for item in items:
        auditorium = db_sess.query(Auditorium).filter(
            Auditorium.auditorium == item.text()
        ).first()
        if item.checkState() == Qt.CheckState.Checked:
            auditorium.selected = True
        else:
            auditorium.selected = False

        db_sess.add(auditorium)

    db_sess.commit()

    try:
        return
    finally:
        db_sess.close()
