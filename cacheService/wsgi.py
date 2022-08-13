from pymemcache.client.base import Client

from cacheService.src.elastic import Elastic
from cacheService.src.log import Logger
from cacheService import config
from cacheService.src.app import Server
from cacheService.src.memcached import JsonSerde, MultilayerCache
from cacheService.src.postgres.postgres import Postgres

if __name__ == "__main__":
    service_name = 'cache_service'

    # configs
    log_config = config['logging']
    app_config = config['app']
    elastic_config = config['elastic']
    cache_config = config['cache']
    postgres_config = config['postgres']

    logger = Logger(log_level=log_config['level'])

    postgres = Postgres(logger, postgres_config)

    # elastic_client = None  --> for test
    elastic_client = Elastic(elastic_config['host'], elastic_config['port'], logger)

    # connecting three memcache clients to three memcached services
    memcache_client1 = Client(cache_config['one']['host'], no_delay=True, serde=JsonSerde())
    memcache_client2 = Client(cache_config['two']['host'], no_delay=True, serde=JsonSerde())
    memcache_client3 = Client(cache_config['three']['host'], no_delay=True, serde=JsonSerde())

    multilayer_cache = MultilayerCache(logger, cache_config, memcache_client1, memcache_client2, memcache_client3)

    server = Server(logger=logger, multilayer_cache=multilayer_cache)
    server.add_routes()
    app = server.get_app()
    app.run()
