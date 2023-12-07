from .download import download_data
from .format import format_url, format_file
from .save import save_json


def run_download_process(namespace):
    resource_name = namespace.name
    resource_url_dict = namespace.url_dict
    resource_type = namespace.type

    url = format_url(resource_url_dict, resource_type, resource_name)
    json_obj = list(download_data(url))

    file = format_file(namespace)
    save_json(json_obj, file)
