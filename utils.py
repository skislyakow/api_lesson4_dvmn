import os
from pathlib import Path
from urllib.parse import unquote, urlsplit

import requests
from environs import Env

DEFAULT_PATH = "images"
DEMO_KEY = "DEMO_KEY"


def load_env():
    env = Env()
    env.read_env()
    return env


def get_file_extension(url: str) -> str:
    path_only = urlsplit(url).path
    decoded_url = unquote(path_only)
    filename = os.path.basename(decoded_url)
    _, extension = os.path.splitext(filename)
    return extension


def get_proxies() -> dict | None:
    http_proxy = os.environ.get("HTTP_PROXY")
    https_proxy = os.environ.get("HTTPS_PROXY")
    if http_proxy and https_proxy:
        return {"http": http_proxy, "https": https_proxy}
    return None


def get_picture(url, filepath: str, proxies=None):
    Path(filepath).parent.mkdir(parents=True, exist_ok=True)
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    with open(filepath, "wb") as file:
        file.write(response.content)
