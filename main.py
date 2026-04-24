import os
from os.path import split, splitext
from urllib.parse import urlsplit, unquote

import requests

from environs import Env

#url = 'https://dvmn.org/media/HST-SM4.jpeg'



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
        
        get_picture(url, path, index)


def fetch_apod():
    os.makedirs(path, exist_ok=True)
    try:
        response = requests.get(apod_url)
        response.raise_for_status()
        url_photo = response.json()['hdurl']
        apod = requests.get(url_photo)
        extension = get_file_extension(url_photo)
        with open(f'{path}/apod{extension}', 'wb') as file:
            file.write(apod.content)
    except requests.exceptions.HTTPError as error:
        print(f'Ошибка HTTP: {error}')
    except requests.exceptions.ConnectionError as error:
        print(f'Ошибка соединения: {error}')


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
    apod_url = f'https://api.nasa.gov/planetary/apod?api_key={api_key}'
    spacex_api_url = 'https://api.spacexdata.com/v5/launches/61fc0243e0dc5662b76489ae'
    path = 'images'

    proxies = {
        'http': 'socks5://89.169.168.25:1080',
        'https': 'socks5://89.169.168.25:1080',
        }
    #load_dotenv()
    #get_picture(url, path)

    #print(requests.get('https://api.ipify.org', proxies=proxies).text)

    #fetch_spacex_last_launch(spacex_api_url)
    fetch_apod()
