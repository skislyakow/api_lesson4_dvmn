import os

import requests

url = 'https://dvmn.org/media/HST-SM4.jpeg'
path = 'images'

proxies = {
    'http': 'socks5://89.169.168.25:1080',
    'https': 'socks5://89.169.168.25:1080',
    }


def get_picture(url, path):
    os.makedirs(path, exist_ok=True)

    response = requests.get(url, proxies=proxies)
    response.raise_for_status()

    with open(f'{path}/hubble.jpeg', 'wb') as file:
        file.write(response.content)


if __name__ == '__main__':
    #get_picture(url, path)

    print(requests.get('https://api.ipify.org', proxies=proxies).text)
