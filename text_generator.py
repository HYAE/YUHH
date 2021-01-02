import requests
import random

def generate_insult():
    link = r'https://insult.mattbas.org/api/insult'
    r = requests.get(url = link,params = {'address': '127.0.0.1'})
    return r.text

def generate_joke():
    link = r'https://us-central1-dadsofunny.cloudfunctions.net/DadJokes/random/jokes'
    r = requests.get(url = link,params = {'address': '127.0.0.1'})
    data = r.json()
    return (data['setup'], data['punchline'])

def generate_quote():
    link = r'https://type.fit/api/quotes'
    r = requests.get(url=link, params = {'address' : '127.0.0.1'})
    data = r.json()
    data = random.choice(data)
    return (data['text'], data['author'])

def generate_compliment():
    link = r'https://complimentr.com/api'
    r = requests.get(url = link, params = {'address': '127.0.0.1'})
    data = r.json()
    return data['compliment']

def generate_pickup_line():
    link = r'http://bplaas.herokuapp.com/pickup-line'
    r = requests.get(url = link, params = {'address': '127.0.0.1'})
    data = r.json()
    return data['pickup_line']
