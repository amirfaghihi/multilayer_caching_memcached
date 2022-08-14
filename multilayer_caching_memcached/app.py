import yaml
from pymemcache.client.base import Client

from multilayer_caching_memcached.src.elastic import Elastic
from multilayer_caching_memcached.src.log import Logger
from multilayer_caching_memcached.src.server import Server
from multilayer_caching_memcached.src.memcached import JsonSerde, MultilayerCache
from multilayer_caching_memcached.src.postgres.postgres import Postgres
from multilayer_caching_memcached.src.repositories.SearchQueryRepo import SearchQueryRepo

service_name = 'cache_service'

# Load configs
with open('./application.yml', 'r') as config_file:
    config = yaml.load(config_file, Loader=yaml.FullLoader)
    log_config = config['logging']
    app_config = config['app']
    elastic_config = config['elastic']
    cache_config = config['cache']
    postgres_config = config['postgres']

logger = Logger(log_level=log_config['level'])

postgres = Postgres(logger, postgres_config)

elastic_client = None  # --> for test
# elastic_client = Elastic(elastic_config['host'], elastic_config['port'], logger)

search_query_repo = SearchQueryRepo(logger, postgres)

# connecting three memcache clients to three memcached services
memcache_client1 = Client(cache_config['one']['host'], no_delay=True, serde=JsonSerde())
memcache_client2 = Client(cache_config['two']['host'], no_delay=True, serde=JsonSerde())
memcache_client3 = Client(cache_config['three']['host'], no_delay=True, serde=JsonSerde())

multilayer_cache = MultilayerCache(logger, cache_config, memcache_client1, memcache_client2, memcache_client3)

server = Server(logger=logger, conf=app_config, search_query_repo=search_query_repo, elastic_client=elastic_client,
                multilayer_cache=multilayer_cache)
server.add_routes()
app = server.get_app()
