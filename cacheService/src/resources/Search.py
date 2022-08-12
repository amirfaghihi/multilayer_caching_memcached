from flask_restful import Resource, reqparse

from cacheService.src.log import Logger
import threading
import json


class SearchCache(Resource):
    def __init__(self, logger: Logger, elastic_client, multilayer_cache):
        self._logger = logger
        self._elastic_client = elastic_client
        self._multilayer_cache = multilayer_cache

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('query_string', type=str, required=True, location='args')
            args = parser.parse_args()

            query_string = args['query_string']

            result1 = self._multilayer_cache.cache1.get(query_string)
            # First cache miss
            if result1 is None:
                result2 = self._multilayer_cache.cache2.get(query_string)
                # Second cache miss
                if result2 is None:
                    result3 = self._multilayer_cache.cache3.get(query_string)
                    # Third cache miss
                    if result3 is None:
                        elastic_query = {"bool": {"must": [{"match_phrase": {"transcription": query_string}}]}}
                        result = self._elastic_client.search(index=query_string, query=elastic_query)
                        response = result['hits']['hits']
                        result0 = {'result': response, 'freq': 1}
                        cache_update_thread = threading.Thread(target=self._multilayer_cache.multilayer_cache_update,
                                                               args=[0, query_string, result0])
                        cache_update_thread.start()
                        return {'response': response}, 200
                    # Third cache hit
                    else:
                        cache_update_thread = threading.Thread(target=self._multilayer_cache.multilayer_cache_update,
                                                               args=[3, query_string, json.loads(result3)])
                        cache_update_thread.start()
                        return {"response": json.loads(result3)}, 200
                # Second cache hit
                else:
                    cache_update_thread = threading.Thread(target=self._multilayer_cache.multilayer_cache_update,
                                                           args=[2, query_string, json.loads(result2)])
                    cache_update_thread.start()
                    return {"response": json.loads(result2)}, 200
            # First cache hit
            else:
                cache_update_thread = threading.Thread(target=self._multilayer_cache.multilayer_cache_update,
                                                       args=[1, query_string, json.loads(result1)])
                cache_update_thread.start()
                return {"response": json.loads(result1)}, 200
        except Exception as e:
            return {"response": "error occurred"}, 500
