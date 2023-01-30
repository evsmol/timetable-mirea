import sqlalchemy as sa
import sqlalchemy.orm as orm
from sqlalchemy.orm import Session
import sqlalchemy.ext.declarative as dec

SqlAlchemyBase = dec.declarative_base()

__factory = None


def global_init(db_url):
    global __factory

    if __factory:
        return

    if not db_url or not db_url.strip():
        raise Exception("Необходимо указать ссылку на базу данных.")

    # print(f"Подключение к базе данных по адресу {db_url}")

    engine = sa.create_engine(db_url, echo=False)
    __factory = orm.sessionmaker(bind=engine)

    from . import __all_models

    SqlAlchemyBase.metadata.create_all(engine)


def create_session() -> Session:
    global __factory
    return __factory()
