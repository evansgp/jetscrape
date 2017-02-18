import requests
import logging
from functools import lru_cache

configuration = None
logger = logging.getLogger(__name__)


class Configuration:

    def __init__(self, username, password):
        self.username = username
        self.password = password
        # herp
        global configuration
        configuration = self

    @property
    @lru_cache()
    def session(self):
        logger.debug('creating session')
        session = requests.Session()
        params = {'username': self.username, 'password': self.password, 'login-form-type': 'pwd'}
        request = session.post('https://www.access-online.com.au/pkmslogin.form', data=params)
        request.raise_for_status()
        return session


class Getable:

    @classmethod
    def get(cls, url, path, params=None):
        logger.debug('getting %s to serialise into %s for %s with %s', url, cls, path, params)
        request = configuration.session.get(url, params=params)
        request.raise_for_status()
        return list(map(lambda a: cls(a), path(request.json())))


class Listable(Getable):

    @classmethod
    def list(cls, params=None):
        logger.debug('listing for %s with %s', cls, params)
        # TODO add paging into an infinite generator...
        results = super().get(cls.list_url, cls.list_path, params)
        for result in results:
            yield result


class Account(Listable):

    list_url = 'https://www.access-online.com.au/white/api/channel/account/v3s/accounts-facilities'

    @staticmethod
    def list_path(d): return d['data'][0]['accounts']

    def __init__(self, data):
        self.id = data['id']

    @property
    @lru_cache()
    def transactions(self):
        return Transaction.list({'account-id': self.id})


class Transaction(Listable):

    list_url = 'https://www.access-online.com.au/white/api/channel/transaction/v3s/transactions'

    @staticmethod
    def list_path(d): return d['data']

    def __init__(self, data):
        self.amount = data['amount']
        self.date = data['transactionDate']
        self.description = data['description']
        self.debit = data['crDrCode'] == 'DR'

