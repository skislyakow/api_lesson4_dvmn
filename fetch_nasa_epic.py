import argparse
import os
import time

import requests
from environs import Env

from utils import DEFAULT_PATH, DEMO_KEY
from utils import get_picture, get_proxies


def fetch_epic(count: int | None = None, output_dir: str = DEFAULT_PATH):
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY', DEMO_KEY)
    proxies = get_proxies()

    url = 'https://api.nasa.gov/EPIC/api/natural/'
    params = {'api_key': api_key}

    response = requests.get(url, params=params, proxies=proxies)
    response.raise_for_status()
    images = response.json()

    if count:
        images = images[:count]

    os.makedirs(output_dir, exist_ok=True)

    for image_data in images:
        filename = image_data['image']
        date_str = filename[8:16]

        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]

        archive_url = (
            f'https://api.nasa.gov/EPIC/archive/natural/'
            f'{year}/{month}/{day}/png/{filename}.png'
        )
        final_url = f'{archive_url}?api_key={api_key}'

        time.sleep(0.5)

        ext = '.png'
        filepath = os.path.join(output_dir, f'epic_{filename}{ext}')
        get_picture(final_url, filepath, proxies)


def main():
    parser = argparse.ArgumentParser(description='Скачать EPIC-фото NASA')
    parser.add_argument(
        '-n', '--count',
        type=int,
        default=None,
        help='Количество фото (по умолчанию все)'
    )
    args = parser.parse_args()

    fetch_epic(args.count)


if __name__ == '__main__':
    main()
