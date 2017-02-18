import logging
import jsonclient
from functools import lru_cache

logger = logging.getLogger(__name__)


def auth(username, password):
    params = {'username': username, 'password': password, 'login-form-type': 'pwd'}
    return lambda session: session.post('https://www.access-online.com.au/pkmslogin.form', data=params)


def pager(params):
    limit = params.get('limit')
    offset = params.get('offset')
    if offset is None:
        params['limit'] = 100
        params['offset'] = 0
    else:
        params['offset'] = int(limit) + int(offset)


class Account(jsonclient.Listable):

    list_url = 'https://www.access-online.com.au/white/api/channel/account/v3s/accounts-facilities'

    @staticmethod
    def list_path(d): return d['data'][0]['accounts']

    def __init__(self, data):
        self.id = data['id']

    @property
    @lru_cache()
    def transactions(self):
        return Transaction.list({'account-id': self.id})


class Transaction(jsonclient.Listable):

    list_url = 'https://www.access-online.com.au/white/api/channel/transaction/v3s/transactions'

    @staticmethod
    def list_path(d): return d['data']

    def __init__(self, data):
        self.amount = data['amount']
        self.date = data['transactionDate']
        self.description = data['description']
        self.debit = data['crDrCode'] == 'DR'

