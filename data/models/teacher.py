import sqlalchemy

from data.db_session import SqlAlchemyBase


class Teacher(SqlAlchemyBase):
    """Таблица избранных преподавателей"""

    __tablename__ = 'teacher'

    id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        primary_key=True,
        autoincrement=True
    )

    teacher = sqlalchemy.Column(
        sqlalchemy.TEXT
    )

    selected = sqlalchemy.Column(
        sqlalchemy.BOOLEAN
    )
