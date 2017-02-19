import logging
import json_client
from datetime import datetime

logger = logging.getLogger(__name__)


def auth(username, password):
    params = {'username': username, 'password': password, 'login-form-type': 'pwd'}
    json_client.authenticator = lambda s: s.post('https://www.access-online.com.au/pkmslogin.form', data=params)


class Paged:

    @classmethod
    def get_page(cls, response):
        limit = response.get('limit', None)
        offset = response.get('offset', None)
        return int(limit or 100), int(offset or 0)

    @classmethod
    def set_page(cls, request, limit, offset):
        request['limit'] = limit
        request['offset'] = offset


class Account(json_client.Listable):

    list_url = 'https://www.access-online.com.au/white/api/channel/account/v3s/accounts-facilities'

    @staticmethod
    def list_path(d): return d['data'][0]['accounts']

    def __init__(self, data):
        self.id = data['id']

    @property
    def transactions(self):
        return Transaction.list({'account-id': self.id})


class Transaction(Paged, json_client.PagedListable):

    list_url = 'https://www.access-online.com.au/white/api/channel/transaction/v3s/transactions'

    @staticmethod
    def list_path(d): return d['data']

    def __init__(self, data):
        self.amount = data['amount']
        self.date = datetime.strptime(data['transactionDate'], '%Y-%m-%d').date()
        self.description = data['description']
        self.debit = data['crDrCode'] == 'DR'

