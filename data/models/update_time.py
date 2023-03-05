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
        sqlalchemy.VARCHAR(length=19)
    )

    start_date = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=10)
    )

    finish_date = sqlalchemy.Column(
        sqlalchemy.VARCHAR(length=10)
    )
