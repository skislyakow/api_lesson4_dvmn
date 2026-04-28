import argparse
import os

import requests
from environs import Env

from utils import DEFAULT_PATH, DEMO_KEY
from utils import get_file_extension, get_picture, get_proxies


def fetch_apod(
        count: int = 10,
        output_dir: str = DEFAULT_PATH,
        use_proxy: bool = False
):
    env = Env()
    env.read_env()
    api_key = env.str('NASA_API_KEY', DEMO_KEY)
    proxies = get_proxies() if use_proxy else None

    url = 'https://api.nasa.gov/planetary/apod'
    try:
        params = {'api_key': api_key, 'count': count}
        response = requests.get(url, params=params, proxies=proxies)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(
                f'Ошибка - Соединение с API ключом {api_key} не прошло (403)'
            )
            params = {'api_key': DEMO_KEY, 'count': count}
            try:
                response = requests.get(url, params=params, proxies=proxies)
                response.raise_for_status()
                api_key = DEMO_KEY
            except requests.exceptions.HTTPError as e2:
                print(f'Ошибка - Соединение с API ключом "DEMO_KEY": {e2}')
                return
        else:
            print(f'HTTP ошибка: {e}')
            return
    except requests.exceptions.RequestException as e:
        print(f'Ошибка сети: {e}')
        return

    apod_list = response.json()

    os.makedirs(output_dir, exist_ok=True)

    for index, apod in enumerate(apod_list):
        url_photo = apod.get('hdurl') or apod.get('url')
        if not url_photo:
            print(f'Фото {index} не имеет URL, пропускаю...')
            continue
        ext = get_file_extension(url_photo)
        filepath = os.path.join(output_dir, f'apod_{index}{ext}')
        try:
            get_picture(url_photo, filepath, proxies)
            print(f'Загружено: apod_{index}{ext}')
        except requests.exceptions.RequestException as e:
            print(f'Ошибка загрузки {url_photo}: {e}')
            continue


def main():
    parser = argparse.ArgumentParser(description='Скачать APOD-фото NASA')
    parser.add_argument(
        '-n', '--count', type=int, default=10, help='Количество ФОТО'
    )
    parser.add_argument(
        '-p', '--use-proxy', action='store_true', help='Использовать прокси'
    )
    args = parser.parse_args()

    fetch_apod(args.count)


if __name__ == '__main__':
    main()
