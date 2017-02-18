from jetscrape import Configuration, Account
import logging
import argparse


logger = logging.getLogger(__name__)


def main():
    args = process_command_line()
    logging.basicConfig(level=args.level)
    Configuration.configure(args.username, args.password)
    for account in Account.list():
        print(account.data)
    return 0


def process_command_line():
    parser = argparse.ArgumentParser(description='Download Jetstar (AU) CC data')
    parser.add_argument('-u', '--username', required=True, help='username to connect with')
    parser.add_argument('-p', '--password', required=True, help='password to connect with')
    parser.add_argument('-v', dest='level', action='store_const', const=logging.DEBUG, default=logging.INFO,
                        help='verbose output')
    return parser.parse_args()

