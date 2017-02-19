import logging
import requests
import jsonclient
from functools import lru_cache

logger = logging.getLogger(__name__)
authenticator = None


@lru_cache()
def session():
    logger.debug('creating session')
    new_session = requests.Session()
    if jsonclient.authenticator is not None:
        logger.debug('authing')
        request = jsonclient.authenticator(new_session)
        request.raise_for_status()
        logger.debug('authed')
    return new_session


class Getable:

    @classmethod
    def get(cls, url, path, params=None):
        request = session().get(url, params=params)
        request.raise_for_status()
        json = request.json()
        results = list(map(lambda a: cls(a), path(json)))
        return results, json


class Listable(Getable):

    @classmethod
    def list(cls, params=None):
        (results, _) = super().get(cls.list_url, cls.list_path, params)
        for result in results:
            yield result


class PagedListable(Getable):

    @classmethod
    def list(cls, params=None):
        while True:
            (results, json) = super().get(cls.list_url, cls.list_path, params)
            for result in results:
                yield result
            (limit, offset) = cls.get_page(json)
            if limit == len(results):
                cls.set_page(params, limit, offset+limit)
                logger.debug('getting new page with limit={}, offset={}'.format(limit, offset))
            else:
                logger.debug('no more pages')
                break
