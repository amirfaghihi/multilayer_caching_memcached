from flask import Flask
from flask_restful import Api

from multilayer_caching_memcached.src.log import Logger
from multilayer_caching_memcached.src.repositories.SearchQueryRepo import SearchQueryRepo
from multilayer_caching_memcached.src.resources.Report import TFReport
from multilayer_caching_memcached.src.resources.Search import SearchCache


class Server:
    def __init__(self, logger: Logger, conf: dict, search_query_repo: SearchQueryRepo, elastic_client=None,
                 multilayer_cache=None):
        self._logger = logger
        self._elastic_client = elastic_client
        self._multilayer_cache = multilayer_cache
        self._search_query_repo = search_query_repo
        self._config = conf
        self._app = self._create_app()
        self.api = Api(self._app)

    def _create_app(self):
        app = Flask(__name__, instance_relative_config=True)

        app.config['ENV'] = self._config['env']
        app.config['DEBUG'] = self._config['debug']
        app.config['SECRET_KEY'] = self._config['secretKey']
        app.config['CORS_HEADERS'] = 'Content-Type'
        return app

    def add_routes(self):
        self.api.add_resource(TFReport, '/v1/report',
                              resource_class_args=(self._logger, self._config, self._search_query_repo))
        self.api.add_resource(SearchCache, '/v1/search',
                              resource_class_args=(
                                  self._logger, self._elastic_client, self._multilayer_cache,
                                  self._search_query_repo))

    def get_app(self):
        return self._app
