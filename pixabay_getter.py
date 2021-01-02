import requests, json, random
from dotenv import load_dotenv
from os import getenv

load_dotenv()   # To load .env file where PIXABAY_KEY resides
parameters = {
    'key' : getenv('PIXABAY_KEY'),
    'q' : 'yellow flowers',
    'image_type' : 'photo',
    'per_page' : '50',
    'page' : '1'
    }


def get_images(query, qty = 1):
    # Returns list of images, if qty not met: returns number of pictures found (int)
    print(f'Pixabay Query: {query}')
    parameters.update({'q': query})
    r = requests.get(r'https://pixabay.com/api/', params = parameters)
    raw_json = r.json()

    if int(raw_json['total']) < qty:
        return int(raw_json['total'])

    hits_selected = random.sample(raw_json['hits'], qty)
    urls = [hit['webformatURL'] for hit in hits_selected]

    print(f'Pixabay URL: {urls}')

    images_bin = [requests.get(url).content for url in urls]
    return images_bin
