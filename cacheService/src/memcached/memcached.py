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

        self.cache_dict = {1: self.cache1, 2: self.cache2, 3: self.cache3}

    def _update_tf_for_key(self, level: int, key: str, cache_hit: bool, result: dict = None):
        conf_index = {1: 'one', 2: 'two', 3: 'three'}

        if cache_hit:
            res = self.cache_dict[level].get(key)
            new_res = res
            new_res['freq'] += 1
            self.cache_dict[level].replace(key, new_res, expire=self._conf[conf_index[level]]['expire'])
        else:
            res = {'result': result, 'freq': 1}
            self.cache_dict[level].set(key, res, expire=self._conf[conf_index[level]]['expire'])

    def dummy_wait(self, t):
        for _ in range(t):
            time.sleep(1)
            self._logger.debug("sleeping for a second")

    def multilayer_cache_update(self, mode: int, key: str, result: dict):
        if mode == 1:
            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(self._update_tf_for_key, 1, key, True)
                executor.submit(self._update_tf_for_key, 2, key, True)
                executor.submit(self._update_tf_for_key, 3, key, True)
        elif mode == 2:
            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(self._update_tf_for_key, 1, key, False, result)
                executor.submit(self._update_tf_for_key, 2, key, True)
                executor.submit(self._update_tf_for_key, 3, key, True)
        elif mode == 3:
            with ThreadPoolExecutor(max_workers=3) as executor:
                executor.submit(self._update_tf_for_key, 1, key, False, result)
                executor.submit(self._update_tf_for_key, 2, key, False, result)
                executor.submit(self._update_tf_for_key, 3, key, True)
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
