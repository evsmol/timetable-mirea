import sqlalchemy

from data.db_session import SqlAlchemyBase


class Schedule(SqlAlchemyBase):
    __tablename__ = 'schedule'

    id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        primary_key=True,
        autoincrement=True
    )

    date = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=10)
    )

    week = sqlalchemy.Column(
        sqlalchemy.INTEGER
    )

    week_day = sqlalchemy.Column(
        sqlalchemy.INTEGER
    )

    group = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=10)
    )

    pair_number = sqlalchemy.Column(
        sqlalchemy.INTEGER
    )

    discipline = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=100)
    )

    activity_type = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=5)
    )

    teacher = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=50)
    )

    auditorium = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=30)
    )
