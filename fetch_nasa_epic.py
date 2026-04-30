import argparse
import os
import time

import requests

from utils import DEFAULT_PATH, DEMO_KEY
from utils import get_picture, get_proxies, load_env


def fetch_epic(
    api_key: str,
    count: int | None = None,
    output_dir: str = DEFAULT_PATH,
    use_proxy: bool = False,
):
    proxies = get_proxies() if use_proxy else None

    url = "https://api.nasa.gov/EPIC/api/natural/"
    try:
        params = {"api_key": api_key}
        response = requests.get(url, params=params, proxies=proxies)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 403:
            print(
                f"Ошибка - Соединение с API ключом {api_key} не прошло (403)"
            )
            params = {"api_key": DEMO_KEY, "count": count}
            try:
                response = requests.get(url, params=params, proxies=proxies)
                response.raise_for_status()
                api_key = DEMO_KEY
            except requests.exceptions.HTTPError as e2:
                print(f'Ошибка - Соединение с API ключом "DEMO_KEY": {e2}')
                return
        else:
            print(f"HTTP ошибка: {e}")
            return
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        return

    images = response.json()

    if count:
        images = images[:count]

    print(f"Получено {len(images)} фото из EPIC")
    os.makedirs(output_dir, exist_ok=True)

    for image_data in images:
        filename = image_data["image"]
        date_str = filename[8:16]

        year = date_str[:4]
        month = date_str[4:6]
        day = date_str[6:8]

        archive_url = (
            f"https://api.nasa.gov/EPIC/archive/natural/"
            f"{year}/{month}/{day}/png/{filename}.png"
        )
        final_url = f"{archive_url}?api_key={api_key}"

        time.sleep(0.5)

        ext = ".png"
        filepath = os.path.join(output_dir, f"epic_{filename}{ext}")
        try:
            get_picture(final_url, filepath, proxies)
            print(f"Загружено: epic_{filename}{ext}")
        except requests.exceptions.RequestException as e:
            print(f"Ошибка загрузки {filename}: {e}")
            continue


def main():
    env = load_env()
    api_key = env.str("NASA_API_KEY", DEMO_KEY)
    parser = argparse.ArgumentParser(description="Скачать EPIC-фото NASA")
    parser.add_argument(
        "-n",
        "--count",
        type=int,
        default=None,
        help="Количество фото (по умолчанию все)",
    )
    parser.add_argument(
        "-p", "--use-proxy", action="store_true", help="Использовать прокси"
    )
    args = parser.parse_args()

    fetch_epic(api_key, args.count)


if __name__ == "__main__":
    main()
