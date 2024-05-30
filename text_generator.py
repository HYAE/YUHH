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
    link = r'https://zenquotes.io/api/random'
    r = requests.get(url=link)
    data = r.json()[0]
    return data['q'], data['a']


def generate_compliment():
    return "Aw mans! You don't deserve compliments tho!"
    link = r'https://complimentr.com/api'
    r = requests.get(url=link, params={'address': '127.0.0.1'})
    data = r.json()
    return data['compliment']


def generate_pickup_line():
    link = r'https://rizzapi.vercel.app/random'
    r = requests.get(url=link)
    data = r.json()
    return data['text']
