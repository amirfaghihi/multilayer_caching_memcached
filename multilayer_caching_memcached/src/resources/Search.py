from flask_restful import Resource, reqparse

from multilayer_caching_memcached.src.log import Logger
import threading
import json

from multilayer_caching_memcached.src.models import SearchQuery
from multilayer_caching_memcached.src.tokenizer.tokenizer import standard_tokenizer


class SearchCache(Resource):
    def __init__(self, logger: Logger, elastic_client, multilayer_cache, search_query_repo):
        self._logger = logger
        self._elastic_client = elastic_client
        self._multilayer_cache = multilayer_cache
        self._search_query_repo = search_query_repo

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('query_string', type=str, required=True, location='args')
            args = parser.parse_args()

            query_string = args['query_string']
            query_string_tokenized = standard_tokenizer(query_string)

            # bulk insert all of token queries into postgres
            qs_dicts = [{'query_string': qs} for qs in query_string_tokenized]
            if len(query_string_tokenized) > 1:
                qs_dicts.append({'query_string': query_string})
            self._search_query_repo.bulk_insert(qs_dicts)

            query_string = query_string.encode('utf-8')
            query_string_tokenized = list(map(lambda x: x.encode('utf-8'), query_string_tokenized))

            result1 = self._multilayer_cache.cache1.get_multi(query_string_tokenized)
            # At least one token in First cache misses --> consider whole query a miss
            if len(result1.keys()) != len(query_string_tokenized):
                result2 = self._multilayer_cache.cache2.get_multi(query_string_tokenized)
                # At least one token in Second cache misses
                if len(result1.keys()) != len(query_string_tokenized):
                    result3 = self._multilayer_cache.cache3.get_multi(query_string_tokenized)
                    # At least one token in Third cache misses
                    if len(result1.keys()) != len(query_string_tokenized):
                        result0 = [f"{t.decode('utf-8')}_value" for t in query_string_tokenized]

                        # Real Query to Elasticsearch service ########

                        # elastic_query = {"bool": {"must": [{"match_phrase": {"transcription": query_string}}]}}
                        # result = self._elastic_client.search(index=query_string, query=elastic_query)
                        # response = result['hits']['hits']
                        # result0 = response

                        ##############

                        cache_update_thread = threading.Thread(target=self._multilayer_cache.multilayer_cache_update,
                                                               args=[0, query_string_tokenized, result0])
                        cache_update_thread.start()
                        return {'response': result0}, 200
                    # Third cache hit
                    else:
                        cache_update_thread = threading.Thread(target=self._multilayer_cache.multilayer_cache_update,
                                                               args=[3, query_string_tokenized, result3])
                        cache_update_thread.start()
                        return {"response": result3[query_string_tokenized[0]].decode('utf-8')}, 200
                # Second cache hit
                else:
                    cache_update_thread = threading.Thread(target=self._multilayer_cache.multilayer_cache_update,
                                                           args=[2, query_string_tokenized, result2])
                    cache_update_thread.start()
                    return {"response": result2[query_string_tokenized[0]].decode('utf-8')}, 200
            # First cache hit
            else:
                return {"response": result1[query_string_tokenized[0]]}, 200
        except Exception as e:
            return {"response": "error occurred"}, 500
