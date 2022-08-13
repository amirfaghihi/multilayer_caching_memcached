from datetime import datetime, timedelta

from flask_restful import Resource, reqparse

from cacheService.src.log import Logger
from cacheService.src.repositories.SearchQueryRepo import SearchQueryRepo


class TFReport(Resource):
    def __init__(self, logger: Logger, search_query_repo: SearchQueryRepo):
        self._logger = logger
        self._search_query_repo = search_query_repo

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('recent_hours', type=int, default=1, location='json')
            parser.add_argument('num_of_tokens', type=int, default=10, location='json')
            args = parser.parse_args()

            end = datetime.now().timestamp()
            start = (datetime.now() - timedelta(hours=args['recent_hours'])).timestamp()
            num_of_tokens = args['num_of_tokens']

            response = self._search_query_repo.find_tf_grouped_by_token(int(start), int(end), num_of_tokens)

            return response.to_json(), 200
        except Exception as e:
            return {"response": "Error occurred"}, 500
