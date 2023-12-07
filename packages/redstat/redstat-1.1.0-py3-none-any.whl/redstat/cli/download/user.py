from argparse import ArgumentParser

from .arguments import optional, positional
from redstat.cli.download.defaults import register_function_default
from redstat.variables.download.url_types import USER_URL_TYPES


def register_user_parser(subparser):
    parents = [
        positional.register_name_argument('reddit username'),
        register_function_default(),
        optional.register_type_parser(USER_URL_TYPES),
        optional.register_output_argument()
    ]

    default_parser: ArgumentParser = subparser.add_parser('user', help='user parser', parents=parents)
