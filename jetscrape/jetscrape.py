import requests


class Configuration:

    session = None

    @staticmethod
    def configure(username, password):
        Configuration.session = Configuration.create_session(password, username)

    @staticmethod
    def create_session(password, username):
        session = requests.Session()
        params = {'username': username, 'password': password, 'login-form-type': 'pwd'}
        request = session.post('https://www.access-online.com.au/pkmslogin.form', data=params)
        request.raise_for_status()
        return session


class Account:

    url_list = 'https://www.access-online.com.au/white/api/channel/account/v3s/accounts-facilities'

    def __init__(self, data):
        self.data = data

    @staticmethod
    def list():
        accounts = Account.get(Account.url_list, Account, lambda d: d['data'][0]['accounts'])
        for account in accounts:
            yield account

    @staticmethod
    def get(url, clazz, path):
        request = Configuration.session.get(url)
        request.raise_for_status()
        return list(map(lambda a: clazz(a), path(request.json())))

