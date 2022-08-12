from flask_restful import Resource, reqparse

from cacheService.src.log import Logger


class TFReport(Resource):
    def __init__(self, logger: Logger, elastic_client, multilayer_cache):
        self._logger = logger
        self._elastic_client = elastic_client
        self._multilayer_cache = multilayer_cache

    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('recent_hours', type=int, default=1, location='json')
            parser.add_argument('num_of_tokens', type=int, default=10, location='json')
            args = parser.parse_args()

            return response.to_json(), response.http_status_code
        except (EntityAlreadyExistException, DatabaseException) as e:
            return e.to_json(), e.http_status_code
