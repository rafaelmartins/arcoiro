import os
from abc import ABCMeta, abstractmethod, abstractproperty
from flask import current_app
from werkzeug.contrib.cache import FileSystemCache


class BaseProvider(object):

    __metaclass__ = ABCMeta

    def __init__(self, cache_dir=None, default_timeout=60 * 60 * 24,
                 api_key=None):
        self.cache = FileSystemCache(cache_dir=cache_dir or '/tmp/__arcoiro__',
                                     default_timeout=default_timeout)
        self._api_key = api_key

    @abstractproperty
    def name(self):
        pass

    @abstractproperty
    def url(self):
        pass

    @abstractmethod
    def get_urls_from_tag(self, tag):
        pass

    @property
    def display_name(self):
        return self.name

    @property
    def api_key(self):
        if self._api_key is not None:
            return self._api_key
        config_key = '%s_API_KEY' % self.name.upper()
        key = current_app.config.get(config_key)
        if key is None:
            raise RuntimeError('%s not defined!' % config_key)
        return key

    def get_cached_urls_from_tag(self, tag):
        cache_key = '%s:%s' % (self.name, tag)
        urls = self.cache.get(cache_key)
        if urls is not None:
            return urls
        urls = self.get_urls_from_tag(tag)
        self.cache.set(cache_key, urls)
        return urls


def list_providers():
    cwd = os.path.dirname(os.path.abspath(__file__))
    for filename in os.listdir(cwd):
        if filename.startswith('_'):
            continue
        if not filename.endswith('.py'):
            continue
        __import__('%s.%s' % (__name__, filename.rstrip('.py')))
    return BaseProvider.__subclasses__()
