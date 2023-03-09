import sqlalchemy

from data.db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase):
    __tablename__ = 'teacher'

    id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        primary_key=True,
        autoincrement=True
    )

    teacher = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=10)
    )

    selected = sqlalchemy.Column(
        sqlalchemy.BOOLEAN
    )
