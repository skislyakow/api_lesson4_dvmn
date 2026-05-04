import argparse
import os

import requests

from utils import DEFAULT_PATH, get_file_extension, get_picture


def fetch_spacex(
    launch_id: str = "latest",
    output_dir: str = DEFAULT_PATH,
    proxies: dict | None = None,
):
    url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    data = response.json()

    photos = data["links"]["flickr"]["original"]
    if not photos:
        print("Нет фотографий в этом запуске")
        return

    print(f"Обнаружено {len(photos)} фото, загружаю...")
    os.makedirs(output_dir, exist_ok=True)

    for index, photo_url in enumerate(photos):
        ext = get_file_extension(photo_url)
        filepath = os.path.join(output_dir, f"spacex_{index}{ext}")
        get_picture(photo_url, filepath, proxies)


def main():
    parser = argparse.ArgumentParser(description="Скачать фото SpaceX")
    parser.add_argument(
        "-i", "--launch-id", default=None, help="ID запуска (опционально)"
    )
    parser.add_argument(
        "-p", "--use-proxy", action="store_true", help="Использовать прокси"
    )
    args = parser.parse_args()

    proxies = None
    if args.use_proxy:
        http_proxy = os.environ.get("HTTP_PROXY")
        https_proxy = os.environ.get("HTTPS_PROXY")
        if http_proxy and https_proxy:
            proxies = {"http": http_proxy, "https": https_proxy}

    fetch_spacex(args.launch_id, proxies=proxies)


if __name__ == "__main__":
    main()
