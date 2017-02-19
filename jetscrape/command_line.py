import sys
import argparse
import logging
import datetime
import csv
from jetscrape import jetstar_api

logger = logging.getLogger(__name__)


def main():
    args = process_command_line()
    logging.basicConfig(level=args.level)
    jetstar_api.auth(args.username, args.password)
    target = datetime.date.today() - datetime.timedelta(days=args.days)
    writer = csv.writer(args.file)
    writer.writerow(['Transaction Date', 'Description', 'Type', 'Amount'])
    for account in jetstar_api.Account.list():
        for txn in account.transactions:
            if txn.date < target:
                break
            writer.writerow(to_row(txn))

    return 0


def to_row(txn):
    return [
        txn.date.strftime('%d %b %Y'),
        txn.description,
        "DR" if txn.debit else "CR",
        txn.amount
    ]


def process_command_line():
    parser = argparse.ArgumentParser(description='Download Jetstar (AU) CC data')
    parser.add_argument('-v', dest='level', action='store_const', const=logging.DEBUG, default=logging.INFO,
                        help='verbose output')
    parser.add_argument('-u', '--username', required=True, help='username to connect with')
    parser.add_argument('-p', '--password', required=True, help='password to connect with')
    parser.add_argument('-d', '--days', default=31, type=int, help='the number of days to process')
    parser.add_argument('-f', '--file', default=sys.stdout, type=argparse.FileType('w'), help='where to direct output')
    return parser.parse_args()

