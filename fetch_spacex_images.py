import argparse
import os

import requests
from environs import Env

from utils import DEFAULT_PATH, get_file_extension, get_picture, get_proxies


def fetch_spacex(launch_id: str | None = None, output_dir: str = DEFAULT_PATH):
    env = Env()
    env.read_env()
    proxies = get_proxies()

    if launch_id:
        url = f'https://api.spacexdata.com/v5/ launches/{launch_id}'
    else:
        url = 'https://api.spacexdata.com/v5/launches/query'

    if launch_id:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        data = response.json()
    else:
        payload = {
            'query': {}, 'options': {'limit': 1, 'sort': {'date_utc': 'desc'}}
        }
        response = requests.post(url, json=payload, proxies=proxies)
        response.raise_for_status()
        data = response.json['docs'][0]

    photos = data['links']['flickr']['original']
    os.makedirs(output_dir, exist_ok=True)

    for index, photo_url in enumerate(photos):
        ext = get_file_extension(photo_url)
        filepath = os.path.join(output_dir, f'spacex_{index}{ext}')
        get_picture(photo_url, filepath, proxies)


def main():
    parser = argparse.ArgumentParser(description='Скачать фото SpaceX')
    parser.add_argument('-i', '--launch-id', help='ID запуска (опционально)')
    args = parser.parse_args()

    fetch_spacex(args.launch_id)


if __name__ == '__main__':
    main()
