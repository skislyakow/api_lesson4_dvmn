import os
from urllib.parse import urlsplit, unquote
from pathlib import Path

import requests
from environs import Env


DEFAULT_PATH = 'images'
DEMO_KEY = 'DEMO_KEY'


def get_file_extension(url: str) -> str:
    path_only = urlsplit(url).path
    decoded_url = unquote(path_only)
    _, extension = os.path.split(decoded_url)
    return extension


def get_proxies() -> dict | None:
    env = Env()
    env.read_env()
    http_proxy = env.strOrNone('HTTP_PROXY')
    https_proxy = env.strOrNone('HTTPS_PROXY')
    if http_proxy and https_proxy:
        return {'http': http_proxy, 'https': https_proxy}
    return None


def get_picture(url: filepath, proxies=None):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    with open(filepath, 'wb') as file:
        file.write(response.content)
