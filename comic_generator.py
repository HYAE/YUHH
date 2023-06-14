import requests
import random
import urllib.request
from PIL import Image


class Comic:
    def __init__(self):
        self.data = self.generate_xkcd_comic()

    def generate_xkcd_comic(self):
        # Ok so they have an endpoint api, but they don't have a way to generate random
        # comicIDs, nor a way to get the max amount. Wikipedia says they have 2402 as of right now,
        # So ill set the randint max to 2403. maybe find some nice codey way of getting the max int the future
        comic_ID = random.randint(0, 2403)
        link = r'https://xkcd.com/{}/info.0.json'.format(comic_ID)

        r = requests.get(url=link)
        data = r.json()

        return data

    def get_title(self):
        data = self.data
        if data is None:
            print("no comic loaded")
            return

        return data["title"]

    def get_image(self):
        # Returns a PIL Image. converts the url from data["img"]
        data = self.data
        if data is None:
            print("no comic loaded")
            return

        img_url = data["img"]
        img = Image.open(urllib.request.urlopen(img_url))

        return img

    def get_alt_text(self):
        data = self.data
        if data is None:
            print("no comic loaded")
            return

        return data["alt"]
