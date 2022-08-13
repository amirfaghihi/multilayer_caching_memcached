from datetime import datetime

from sqlalchemy import String, Column, DateTime, Integer

from cacheService.src.postgres.postgres import BASE_MODEL


class SearchQuery(BASE_MODEL):
    def __init__(self, dict1):
        self.__dict__.update(dict1)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    __tablename__ = 'SearchQuery'
    id = Column(Integer, primary_key=True, autoincrement=True)
    query_string = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
