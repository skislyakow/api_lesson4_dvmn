import argparse
import os
import random

import telegram
from telegram.error import NetworkError, TimedOut, BadRequest
from telegram.utils.request import Request
from environs import Env

from utils import get_proxies


def main():
    parser = argparse.ArgumentParser(
        description='Отправка фото через Telegram бота'
    )
    parser.add_argument(
        '-p', '--use-proxy', action='store_true', help='Использовать прокси'
    )
    parser.add_argument(
        'image',
        nargs='?',
        default=None,
        help='Путь к изображению (например: images/spacex_0.jpg)'
    )
    args = parser.parse_args()
    env = Env()
    env.read_env()

    request = None
    if args.use_proxy:
        proxies = get_proxies()
        if proxies:
            proxy_url = proxies.get('https') or proxies.get('http')
            if proxy_url:
                request = Request(proxy_url=proxy_url)

    try:
        bot = telegram.Bot(
            token=env.str('TELEGRAM_BOT_TOKEN'), request=request
        )
        print(bot.get_me())
        channel_id = env.str('TELEGRAM_CHANNEL_ID')
        if args.image:
            if '/' not in args.image and '\\' not in args.image:
                args.image = os.path.join('images', args.image)
            image_path = args.image
        else:
            images_dir = 'images'
            if not os.path.exists(images_dir):
                print(f'Папка {images_dir} не найдена!')
                return
            files = os.listdir(images_dir)
            image_files = [
                f for f in files if os.path.isfile(os.path.join(images_dir, f))
            ]
            if not image_files:
                print(f'В папке {images_dir} нет файлов!')
                return
            random_image = random.choice(image_files)
            image_path = os.path.join(images_dir, random_image)
            print(f'Выбрано случайное фото: {image_path}')
        if not os.path.exists(image_path):
            print(f'Файл не найден: {image_path}')
            return
        with open(image_path, 'rb') as image:
            bot.send_photo(chat_id=channel_id, photo=image)
        print(f'Фото {image_path} отправлено')

    except BadRequest as e:
        print(f'Ошибка запроса (неверный chat_id?): {e}')
    except (NetworkError, TimedOut) as e:
        print(f'Ошибка сети при подключении к Telegram: {e}')
    except Exception as e:
        print(f'Неизвестная ошибка: {e}')


if __name__ == '__main__':
    main()
