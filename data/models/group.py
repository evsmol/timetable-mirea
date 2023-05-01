import sqlalchemy

from data.db_session import SqlAlchemyBase


class Group(SqlAlchemyBase):
    """Таблица избранных групп"""

    __tablename__ = 'group'

    id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        primary_key=True,
        autoincrement=True
    )

    group = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=10)
    )

    selected = sqlalchemy.Column(
        sqlalchemy.BOOLEAN
    )
