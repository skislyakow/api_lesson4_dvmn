import argparse
import os

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
        default='Путь к изображению (например: images/spacex_0.jpg)'
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
            if not os.path.exists(args.image):
                print(f'Файл не найден: {args.image}')
                return
            with open(args.image, 'rb') as image:
                bot.send_photo(chat_id=channel_id, photo=image)
            print(f'Фото {args.image} отправлено')
        else:
            message_text = 'Привет от Python-бота!'
            bot.send_message(chat_id=channel_id, text=message_text)

    except BadRequest as e:
        print(f'Ошибка запроса (неверный chat_id?): {e}')
    except (NetworkError, TimedOut) as e:
        print(f'Ошибка сети при подключении к Telegram: {e}')
    except Exception as e:
        print(f'Неизвестная ошибка: {e}')


if __name__ == '__main__':
    main()
