import logging
import requests
import jsonclient
from functools import lru_cache

logger = logging.getLogger(__name__)
authenticator = None
pager = None


@lru_cache()
def session():
    logger.debug('creating session')
    new_session = requests.Session()
    if jsonclient.authenticator is not None:
        request = jsonclient.authenticator(new_session)
        request.raise_for_status()
    return new_session


class Getable:

    @classmethod
    def get(cls, url, path, params=None):
        logger.debug('getting %s to serialise into %s for %s with %s', url, cls, path, params)
        request = session().get(url, params=params)
        request.raise_for_status()
        return list(map(lambda a: cls(a), path(request.json())))


class Listable(Getable):

    @classmethod
    def list(cls, params={}):
        while True:
            if jsonclient.pager is not None:
                jsonclient.pager(params)
            logger.debug('listing for %s with %s', cls, params)
            results = super().get(cls.list_url, cls.list_path, params)
            for result in results:
                yield result
