import os

import requests

url = 'https://dvmn.org/media/HST-SM4.jpeg'
spacex_api_url = 'https://api.spacexdata.com/v5/launches/61fc0243e0dc5662b76489ae'
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


def get_pucture_from_spacex(url):
    response = requests.get(url)
    response.raise_for_status()

    print(response.json()['links']['flickr']['original'])


if __name__ == '__main__':
    #get_picture(url, path)

    #print(requests.get('https://api.ipify.org', proxies=proxies).text)

    get_pucture_from_spacex(spacex_api_url)
