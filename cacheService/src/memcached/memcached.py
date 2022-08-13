import json
import time
from concurrent.futures import ThreadPoolExecutor

from cacheService.src.log import Logger


class MultilayerCache:
    def __init__(self, logger: Logger, conf, cache1, cache2, cache3):
        self._logger = logger.logger
        self._conf = conf
        self.cache1 = cache1
        self.cache2 = cache2
        self.cache3 = cache3

    def multilayer_cache_update(self, mode: int, key: str, result: dict):
        if mode == 2:
            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(self.cache1.set, key, result, self._conf['one']['expire'])
        elif mode == 3:
            with ThreadPoolExecutor(max_workers=2) as executor:
                executor.submit(self.cache1.set, key, result, self._conf['one']['expire'])
                executor.submit(self.cache2.set, key, result, self._conf['two']['expire'])
        else:
            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(self.cache1.set, key, result, self._conf['one']['expire'])
                executor.submit(self.cache2.set, key, result, self._conf['two']['expire'])
                executor.submit(self.cache3.set, key, result, self._conf['three']['expire'])


class JsonSerde(object):
    def serialize(self, key, value):
        if isinstance(value, str):
            return value, 1
        return json.dumps(value), 2

    def deserialize(self, key, value, flags):
        if flags == 1:
            return value
        if flags == 2:
            return json.loads(value)
        raise Exception("Unknown serialization format")
