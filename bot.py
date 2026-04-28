import argparse

import telegram
from telegram.error import NetworkError, TimedOut
from telegram.utils.request import Request
from environs import Env

from utils import get_proxies


def main():
    parser = argparse.ArgumentParser(description='Проверка Telegram бота')
    parser.add_argument(
        '-p', '--use-proxy', action='store_true', help='Использовать прокси'
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
    except (NetworkError, TimedOut) as e:
        print(f'Ошибка сети при подключении к Telegram: {e}')
    except Exception as e:
        print(f'Неизвестная ошибка: {e}')


if __name__ == '__main__':
    main()
