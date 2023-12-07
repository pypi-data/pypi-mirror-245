from redstat.cli import parse_download_args


def run_download_process():
    namespace = parse_download_args()

    if namespace.func is None:
        raise Exception(f'Invalid input {namespace}')

    namespace.func(namespace)
