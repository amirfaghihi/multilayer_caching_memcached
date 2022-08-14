from datetime import datetime, timedelta

import pandas as pd
from flask_restful import Resource, reqparse

from multilayer_caching_memcached.src.log import Logger
from multilayer_caching_memcached.src.repositories.SearchQueryRepo import SearchQueryRepo


class TFReport(Resource):
    def __init__(self, logger: Logger, conf: dict, search_query_repo: SearchQueryRepo):
        self._logger = logger
        self._search_query_repo = search_query_repo
        self._conf = conf

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('recent_hours', type=int, default=1, location='json')
            parser.add_argument('num_of_tokens', type=int, default=10, location='json')
            args = parser.parse_args()

            end = datetime.now()
            start = (datetime.now() - timedelta(hours=args['recent_hours']))
            num_of_tokens = args['num_of_tokens']

            response = self._search_query_repo.find_tf_grouped_by_token(start, end, num_of_tokens)

            response = list(map(lambda x: {'token': x[0], 'search_count': x[1]}, response))
            df = pd.DataFrame(response)
            df.to_csv(
                f"{self._conf['save_path']}/{str(start.timestamp())}_{str(end.timestamp())}_{str(num_of_tokens)}.csv", index=False)

            return {'response': response}, 200
        except Exception as e:
            return {"response": "Error occurred"}, 500
