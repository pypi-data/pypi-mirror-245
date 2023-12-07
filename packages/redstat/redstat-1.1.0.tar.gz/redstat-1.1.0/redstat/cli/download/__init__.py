from argparse import ArgumentParser
from sys import argv

from redstat.cli.download.subreddit import register_post_parser
from redstat.cli.download.user import register_user_parser


def parse_download_args():
    default_parser = ArgumentParser()
    subparser = default_parser.add_subparsers()

    register_subparsers(subparser)

    if len(argv) == 1:
        default_parser.print_help()
        exit()

    return default_parser.parse_args()


def register_subparsers(subparser):
    register_post_parser(subparser)
    register_user_parser(subparser)
