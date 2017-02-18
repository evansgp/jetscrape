import argparse
import logging
import jetscrape
import jsonclient

logger = logging.getLogger(__name__)


def main():
    args = process_command_line()
    logging.basicConfig(level=args.level)
    logger.debug('running with arguements: %s', args)
    jsonclient.authenticator = jetscrape.auth(args.username, args.password)
    jsonclient.pager = jetscrape.pager
    for account in jetscrape.Account.list():
        logger.info('got account: %s', account)
        for transaction in account.transactions:
            logger.info('got transaction: {txn.date} {txn.description} {txn.amount} {txn.debit}'.format(txn=transaction))
    return 0


def process_command_line():
    parser = argparse.ArgumentParser(description='Download Jetstar (AU) CC data')
    parser.add_argument('-v', dest='level', action='store_const', const=logging.DEBUG, default=logging.INFO,
                        help='verbose output')
    parser.add_argument('-u', '--username', required=True, help='username to connect with')
    parser.add_argument('-p', '--password', required=True, help='password to connect with')
    return parser.parse_args()

