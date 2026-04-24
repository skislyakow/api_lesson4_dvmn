import os
from os.path import split, splitext
from urllib.parse import urlsplit, unquote, urlencode

import requests

from environs import Env


DEMO_KEY = 'DEMO_KEY'
PATH = 'images'


def get_picture(url, path, index):
    os.makedirs(path, exist_ok=True)
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    
    with open(f'{path}/spacex_{index}{get_file_extension(url)}', 'wb') as file:
        file.write(response.content)


def fetch_spacex_last_launch(url):
    response = requests.get(url)
    response.raise_for_status()

    url_photos_json = response.json()['links']['flickr']['original']
    print(url_photos_json)    
    
    for index, url in enumerate(url_photos_json):
        
        get_picture(url, PATH, index)


def fetch_apod(base_url, path, primary_key):
    os.makedirs(path, exist_ok=True)

    def make_request(api_key):
        params = {
            'apikey': api_key,
            'count': 10,
        }
        url = f'{base_url}?{urlencode(params)}'
        return requests.get(url)
    try:
        response = make_request(primary_key)
        response.raise_for_status()
    except requests.exceptions.HTTPError as error:
        if error.response.status_code == 403:
            print(f'{error.response.status_code}, далее использовать DEMO_KEY')
            try:
                response = make_request(DEMO_KEY)
                response.raise_for_status()
            except requests.exceptions.HTTPError as error2:
                print(f'DEMO_KEY, ошибка: {error2.response.status_code}')
                return
            
    apod_list = response.json()
    for index, apod in enumerate(apod_list):
        url_photo = apod['hdurl']
        extension = get_file_extension(url_photo)
        photo = requests.get(url_photo)
        with open(f'{path}/apod_{index}{extension}', 'wb') as file:
            file.write(photo.content) 


def get_file_extension(url: str) -> str:
    path_only = urlsplit(url).path
    decoded_url = unquote(path_only)
    _, filename = split(decoded_url)
    _, extension = splitext(filename)
    return extension


if __name__ == '__main__':
    env = Env()
    env.read_env()
    api_key = env.str("NASA_DEMO_API")
    base_apod_url = 'https://api.nasa.gov/planetary/apod'
    spacex_api_url = 'https://api.spacexdata.com/v5/launches/61fc0243e0dc5662b76489ae' 

    proxies = {
        'http': 'socks5://89.169.168.25:1080',
        'https': 'socks5://89.169.168.25:1080',
        }
    fetch_apod(base_apod_url, PATH, api_key)
