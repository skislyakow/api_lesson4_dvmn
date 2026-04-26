import argparse
import os

import requests
from environs import Env

from utils import DEFAULT_PATH, DEMO_KEY
from utils import get_file_extension, get_picture, get_proxies


def fetch_apod(count: int = 10, output_dir: str = DEFAULT_PATH):
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY', DEMO_KEY)
    proxies = get_proxies()

    url = 'https://api.nasa.gov/planetary/apod'
    params = {'api_key': api_key, 'count': count}

    response = requests.get(url, params=params, proxies=proxies)
    response.raise_for_status()
    apod_list = response.json()

    os.makedirs(output_dir, exist_ok=True)

    for index, apod in enumerate(apod_list):
        url_photo = apod.get('hdurl') or apod.get('url')
        if not url_photo:
            continue
        ext = get_file_extension(url_photo)
        filepath = os.path.join(output_dir, f'apod_{index}{ext}')
        get_picture(url_photo, filepath, proxies)


def main():
    parser = argparse.ArgumentParser(description='Скачать APOD-фото NASA')
    parser.add_argument(
        '-n', '--count', type=int, default=10, help='Количество ФОТО'
    )
    args = parser.parse_args()

    fetch_apod(args.count)


if __name__ == '__main__':
    main()
