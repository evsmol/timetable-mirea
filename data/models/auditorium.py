import sqlalchemy

from data.db_session import SqlAlchemyBase


class Auditorium(SqlAlchemyBase):
    """Таблица избранных аудиторий"""

    __tablename__ = 'auditorium'

    id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        primary_key=True,
        autoincrement=True
    )

    auditorium = sqlalchemy.Column(
        sqlalchemy.TEXT
    )

    selected = sqlalchemy.Column(
        sqlalchemy.BOOLEAN
    )
