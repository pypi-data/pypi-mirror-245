from argparse import ArgumentParser


def register_name_argument(help_message):
    parser = ArgumentParser(add_help=False)
    parser.add_argument('name', help=help_message)
    return parser
