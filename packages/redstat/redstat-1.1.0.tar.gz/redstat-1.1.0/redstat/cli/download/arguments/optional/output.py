from argparse import ArgumentParser, FileType


def register_output_argument():
    parser = ArgumentParser(add_help=False)
    parser.add_argument('-o', '--output', help='output file', type=FileType('w', encoding='utf-8'))
    return parser
