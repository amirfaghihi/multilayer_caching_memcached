from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from cacheService.src.log import Logger

BASE_MODEL = declarative_base()


class Postgres:
    def __init__(self, logger: Logger, conf) -> None:
        self.logger = logger.logger
        self.conf = conf

        self._engine: Engine = self._create_engine()
        self.session = sessionmaker(self._engine)()

        BASE_MODEL.metadata.create_all(self._engine)

    def _create_engine(self) -> Engine:
        try:
            self.logger.debug('Creating database engine for connection')
            engine = create_engine(
                'postgresql+psycopg2://{}:{}@{}:{}/{}'.format(self.conf['username'],
                                                              self.conf['password'],
                                                              self.conf['host'],
                                                              self.conf['port'],
                                                              self.conf['db']),
                echo=self.conf.log_level)
            return engine
        except Exception as e:
            self.logger.exception(e)


class BaseRepo:
    def __init__(self, logger: Logger, postgres: Postgres):
        self.postgres_client = postgres
        self.logger = logger.logger

    def safe_exec(func):
        def inner(self, *args):
            try:
                res = func(self, *args)
                self.postgres_client.session.commit()
                return res
            except Exception as e:
                self.logger.exception(e)
                self.postgres_client.session.rollback()
        return inner
