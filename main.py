import argparse
from network import network
from path import path
from connector import Connector
import sys


def main():
    """process command-line arguments, help accessible with -h or --help"""
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()

    parser_network = subparsers.add_parser('network', help='get network of URL\'s')
    parser_network.add_argument('START_URL', type=str, help='starting URL')
    parser_network.add_argument('--depth', '-d', type=int, default=2, help='max depth of search')
    parser_network.set_defaults(func=network)

    parser_path = subparsers.add_parser('path', help='find shortest path')
    parser_path.add_argument('START_URL', type=str, help='starting URL')
    parser_path.add_argument('END_URL', type=str, help='target URL')
    parser_path.set_defaults(func=path)

    args = parser.parse_args()

    """show help if no arguments were given"""
    if not len(sys.argv) > 1:
        parser.print_help()
        sys.exit(0)

    connector = Connector()

    """call corresponding function"""
    args.func(args, connector)


if __name__ == '__main__':
    main()


