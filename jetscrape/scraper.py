import requests


def get(username, password):
    with requests.Session() as s:
        login(s, username, password)
        accounts = get_accounts(s)
        account_ids = [account['id'] for account in accounts]
        transactions = [get_transactions(s, account_id) for account_id in account_ids]
    return transactions


def get_transactions(session, account_id):
    request = session.get('https://www.access-online.com.au/white/api/channel/transaction/v3s/transactions',
                          params={'account-id': account_id})
    request.raise_for_status()
    return request.json()['data']


def get_accounts(session):
    request = session.get('https://www.access-online.com.au/white/api/channel/account/v3s/accounts-facilities')
    request.raise_for_status()
    return request.json()['data'][0]['accounts']


def login(session, username, password):
    body = {
        'username': username,
        'password': password,
        'login-form-type': 'pwd'
    }
    request = session.post('https://www.access-online.com.au/pkmslogin.form', data=body)
    request.raise_for_status()
