from argparse import ArgumentParser

from redstat.functions.download import run_download_process


def register_function_default() -> ArgumentParser:
    default_parser = ArgumentParser(add_help=False)
    default_parser.set_defaults(func=run_download_process)
    return default_parser
