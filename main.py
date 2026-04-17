import os

import requests

#url = 'https://dvmn.org/media/HST-SM4.jpeg'
spacex_api_url = 'https://api.spacexdata.com/v5/launches/61fc0243e0dc5662b76489ae'
path = 'images'

proxies = {
    'http': 'socks5://89.169.168.25:1080',
    'https': 'socks5://89.169.168.25:1080',
    }

def get_picture(url, path, index):
    os.makedirs(path, exist_ok=True)

    #response = requests.get(url, proxies=proxies)
    response = requests.get(url, proxies=proxies)
    response.raise_for_status()
    
    with open(f'{path}/spacex_{index}.jpeg', 'wb') as file:
        file.write(response.content)
        


def fetch_spacex_last_launch(url):
    response = requests.get(url)
    response.raise_for_status()

    url_photos_json = response.json()['links']['flickr']['original']
    print(url_photos_json)    
    
    for index, url in enumerate(url_photos_json):
        
        get_picture(url, path, index)
       


if __name__ == '__main__':
    #get_picture(url, path)

    #print(requests.get('https://api.ipify.org', proxies=proxies).text)

    get_pucture_from_spacex(spacex_api_url)
