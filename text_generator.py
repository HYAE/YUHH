import requests
import random


def generate_insult():
    link = r'https://insult.mattbas.org/api/insult'
    r = requests.get(url=link, params={'address': '127.0.0.1'})
    return r.text


def generate_joke():
    link = r'https://v2.jokeapi.dev/joke/Any?type=twopart'
    r = requests.get(url=link, params={'address': '127.0.0.1'})
    data = r.json()
    return (data['setup'], data['delivery'])


def generate_quote():
    link = r'https://type.fit/api/quotes'
    r = requests.get(url=link, params={'address': '127.0.0.1'})
    data = r.json()
    data = random.choice(data)
    return (data['text'], data['author'])


def generate_compliment():
    link = r'https://complimentr.com/api'
    r = requests.get(url=link, params={'address': '127.0.0.1'})
    data = r.json()
    return data['compliment']


def generate_pickup_line():
    link = r'https://vinuxd.vercel.app/api/pickup'
    r = requests.get(url=link, params={'address': '127.0.0.1'})
    data = r.json()
    return data['pickup']
