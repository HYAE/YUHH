import requests


def generateQuestion():
    """Generate a trivia question.

    For now, just generates an easy question from any category
    Add more stuff here. pretty good api https://opentdb.com/api_config.php
    """
    link = r'https://opentdb.com/api.php?amount=1&type=multiple'
    r = requests.get(url=link, params={'address': '127.0.0.1'})
    data = r.json()
    results = data['results'][0]

    return results
