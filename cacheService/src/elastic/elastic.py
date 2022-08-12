from elasticsearch import Elasticsearch

from cacheService.src.log import Logger


class Elastic:
    def __init__(self, elastic_host: str, elastic_port: str, logger: Logger):
        self.client = Elasticsearch(f"{elastic_host}:{elastic_port}", timeout=30)
        self.logger = logger.logger
        if not self.client.ping():
            error_message = 'Elastic failed to connect to {}!'.format(elastic_host)
            exception = Exception(error_message)
            self.logger.exception(exception)
            raise exception
