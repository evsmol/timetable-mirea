from datetime import datetime

import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

from logging_func import logging

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_file):
    global __factory

    if __factory:
        return

    if not db_file or not db_file.strip():
        logging(datetime.now(), 'ERROR_DB', 'Отсутствует адрес базы данных')
        raise Exception('Необходимо указать адрес базы данных')

    conn_str = f'sqlite:///{db_file.strip()}?check_same_thread=False'
    logging(datetime.now(), 'INFO_DB',
            f'Подключение к базе данных по адресу «{db_file}»')

    engine = sa.create_engine(conn_str, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
