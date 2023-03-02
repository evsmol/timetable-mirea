import sqlalchemy

from data.db_session import SqlAlchemyBase


class UpdateTime(SqlAlchemyBase):
    __tablename__ = 'update_time'

    id = sqlalchemy.Column(
        sqlalchemy.INTEGER,
        primary_key=True,
        autoincrement=True
    )

    update_date = sqlalchemy.Column(
        sqlalchemy.TIME()
    )

    start_date = sqlalchemy.Column(
        sqlalchemy.TIME()
    )

    finish_date = sqlalchemy.Column(
        sqlalchemy.TIME()
    )
