# Jetscraper

A python3 tool for getting Jetstar AU CC transactions for budgeting.


Requests:
- POST https://www.access-online.com.au/pkmslogin.form 
    - form data: username=*&password=*&login-form-type=pwd
    - verify: status = 302, location = https://www.access-online.com.au/sepas/serve?TAM_OP=login_success
    - persist cookies
- GET https://www.access-online.com.au/white/api/channel/account/v3s/accounts-facilities
    - embed=rates&embed=product&embed=position&embed=interest&embed=repayment&embed=borrowers&embed=securities&embed=permissions&embed=related_accounts&embed=related_parties&embed=nominated_accounts&embed=account_name&embed=card_details&limit=100&product-type=cash&product-type=credit_card&product-type=savings&product-type=transaction&product-type=mortgage&product-type=super&product-type=term_deposit&product-type=investment&product-type=super&product-type=pension&api_key=

- GET https://www.access-online.com.au/white/api/channel/transaction/v3s/transactions
    - account-id=*&limit=100&offset=0&product-type=credit_card&q=&status=posted
    - verify: status = 200
- GET https://www.access-online.com.au/white/api/channel/transaction/v3s/transactions
    - account-id=*&status=pending

