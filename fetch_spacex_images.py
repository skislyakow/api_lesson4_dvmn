import argparse
import os

import requests
from environs import Env

from utils import DEFAULT_PATH, get_file_extension, get_picture, get_proxies


def fetch_spacex(
        launch_id: str | None = None,
        output_dir: str = DEFAULT_PATH,
        use_proxy: bool = False
):
    env = Env()
    env.read_env()
    proxies = get_proxies() if use_proxy else None

    if launch_id:
        url = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    else:
        url = 'https://api.spacexdata.com/v5/launches/latest'

    if launch_id:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        data = response.json()
    else:
        response = requests.get(url, proxies=proxies)
        response.raise_for_status()
        data = response.json()

    photos = data['links']['flickr']['original']
    if not photos:
        print('Нет фотографий в этом запуске')
        return

    print(f'Обнаружено {len(photos)} фото, загружаю...')
    os.makedirs(output_dir, exist_ok=True)

    for index, photo_url in enumerate(photos):
        ext = get_file_extension(photo_url)
        filepath = os.path.join(output_dir, f'spacex_{index}{ext}')
        get_picture(photo_url, filepath, proxies)


def main():
    parser = argparse.ArgumentParser(description='Скачать фото SpaceX')
    parser.add_argument('-i', '--launch-id', help='ID запуска (опционально)')
    parser.add_argument(
        '-p', '--use-proxy', action='store_true', help='Использовать прокси'
    )
    args = parser.parse_args()

    fetch_spacex(args.launch_id, use_proxy=args.use_proxy)


if __name__ == '__main__':
    main()
