from argparse import ArgumentParser


def register_type_parser(url_dict: dict):
    parser = ArgumentParser(add_help=False)

    choice_list = list(url_dict.keys())
    default_choice_value = choice_list[0]

    parser.add_argument(
        '-t', '--type',
        help=f'types {choice_list} default: {default_choice_value}',
        choices=url_dict,
        default=default_choice_value,
        metavar='type'
    )

    parser.set_defaults(url_dict=url_dict)

    return parser
