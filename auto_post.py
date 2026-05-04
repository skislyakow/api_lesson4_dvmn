import argparse
import os
import random
import time

import telegram
from telegram.error import BadRequest, NetworkError, TimedOut
from telegram.utils.request import Request
from environs import Env




def main():
    env = Env()
    env.read_env()
    parser = argparse.ArgumentParser(
        description="Авто-постинг фото в Telegram канал"
    )
    parser.add_argument(
        "directory", nargs="?", default="images", help="Папка с изображениями"
    )
    parser.add_argument(
        "--interval",
        type=float,
        default=4.0,
        help="Интервал публикации в часах",
    )
    parser.add_argument(
        "-p", "--use-proxy", action="store_true", help="Использовать прокси"
    )
    args = parser.parse_args()

    hours = args.interval
    interval_seconds = hours * 3600
    print(f"Интервал публикации: {hours} ч. ({interval_seconds} сек.)")

    request = None
    if args.use_proxy:
        http_proxy = os.environ.get("HTTP_PROXY")
        https_proxy = os.environ.get("HTTPS_PROXY")
        proxy_url = None
        if http_proxy and https_proxy:
            proxy_url = https_proxy or http_proxy
        if proxy_url:
            request = Request(proxy_url=proxy_url)

    bot_token = env.str("TELEGRAM_BOT_TOKEN")
    channel_id = env.str("TELEGRAM_CHANNEL_ID")
    bot = None
    while bot is None:
        try:
            bot = telegram.Bot(token=bot_token, request=request)
            me = bot.get_me()
            print(f"Бот {me.username} запущен.")
        except (NetworkError, TimedOut) as e:
            print(f"Ошибка подключения к Telegram: {e}. Повтор через 60 с.")
            time.sleep(60)
        except BadRequest as e:
            print(f"Ошибка авторизации (неверный токен?): {e}.")
            exit(1)

    image_exts = (".jpg", ".jpeg", ".png", ".gif")
    while True:
        files = [
            f
            for f in os.listdir(args.directory)
            if os.path.isfile(os.path.join(args.directory, f))
            and f.lower().endswith(image_exts)
        ]

        if not files:
            print("Нет файлов для публикации. Жду час...")
            time.sleep(3600)
            continue
        random.shuffle(files)
        print(f"Начинаю цикл из {len(files)} фото.")
        for filename in files:
            filepath = os.path.join(args.directory, filename)
            try:
                with open(filepath, "rb") as photo:
                    bot.send_photo(chat_id=channel_id, photo=photo)
                print(f"Отправлено: {filename}")
            except (NetworkError, TimedOut) as e:
                print(f"Ошибка отправки {filename}: {e}. Повтор через 60 с.")
                time.sleep(60)
                continue
            except BadRequest as e:
                print(f"Ошибка запроса {filename}: {e}")
            print(f"Ожидание {hours} ч. до следующего поста...")
            time.sleep(interval_seconds)


if __name__ == "__main__":
    main()
