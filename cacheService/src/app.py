from flask import Flask
from flask_restful import Api

from cacheService import config
from cacheService.src.log import Logger
from cacheService.src.resources.Report import TFReport
from cacheService.src.resources.Search import SearchCache
from cacheService.src.resources.Test import Test


class Server:
    def __init__(self, logger: Logger, elastic_client=None, multilayer_cache=None):
        self._app = self._create_app()
        self.api = Api(self._app)
        self._logger = logger
        self._elastic_client = elastic_client
        self._multilayer_cache = multilayer_cache

    def _create_app(self):
        app_config = config['app']
        app = Flask(__name__, instance_relative_config=True)

        app.config['ENV'] = app_config['env']
        app.config['DEBUG'] = app_config['debug']
        app.config['SECRET_KEY'] = app_config['secretKey']
        app.config['CORS_HEADERS'] = 'Content-Type'
        return app

    def add_routes(self):
        if self._elastic_client is not None:
            self.api.add_resource(TFReport, '/v1/report',
                                  resource_class_args=(self._logger, self._elastic_client, self._multilayer_cache))
            self.api.add_resource(SearchCache, '/v1/search',
                                  resource_class_args=(self._logger, self._elastic_client, self._multilayer_cache))

        self.api.add_resource(Test, '/v1/test', resource_class_args=(self._multilayer_cache,))

    def get_app(self):
        return self._app
