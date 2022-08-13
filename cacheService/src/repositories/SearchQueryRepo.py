from sqlalchemy import func

from cacheService.src.log import Logger
from cacheService.src.models import SearchQuery
from cacheService.src.postgres.postgres import BaseRepo, Postgres


class SearchQueryRepo(BaseRepo):
    def __init__(self, logger: Logger, postgres_db: Postgres):
        super(SearchQueryRepo, self).__init__(logger, postgres_db)

    @BaseRepo.safe_exec
    def insert(self, search_query: SearchQuery):
        self.postgres_client.session.add(search_query)

    @BaseRepo.safe_exec
    def bulk_insert(self, search_queries):
        self.postgres_client.session.bulk_insert_mappings(SearchQuery, search_queries)

    @BaseRepo.safe_exec
    def find_tf_grouped_by_token(self, start: int, end: int, limit: int):
        query = self.postgres_client.session \
            .query(SearchQuery, func.count(SearchQuery.query_string)) \
            .filter(SearchQuery.created_at.between(start, end)) \
            .group_by(SearchQuery.query_string).limit(limit)

        result = query.all()
        return result
