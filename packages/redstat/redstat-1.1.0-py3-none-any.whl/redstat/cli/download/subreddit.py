from argparse import ArgumentParser

from .arguments import optional, positional
from redstat.cli.download.defaults import register_function_default
from redstat.variables.download.url_types import SUBREDDIT_URL_TYPES


def register_post_parser(subparser):
    parents = [
        positional.register_name_argument('subreddit name'),
        register_function_default(),
        optional.register_type_parser(SUBREDDIT_URL_TYPES),
        optional.register_output_argument()
    ]
    default_parser: ArgumentParser = subparser.add_parser('subreddit', help='subreddit parser', parents=parents)
