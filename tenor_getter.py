import requests, random

parameters = {
    'q': 'apple',
    'media_filter': 'minimal',
    'limit': '20',  # Number of gifs returned per query (ie. how many gifs in a 'page')
    'pos': '0'      # At which position does the json start showing the results (ie. pos = 8 means the first result returned is the 7th result on Tenor; The 'next' response tells us the pos of the 1st pic of the next 'page')
    }


def get_gif(query, limit = 20, pos = 0):
    """Return a random GIF from query, None if no images found."""
    print(f'Tenor Query: {query}')
    parameters.update({'q': query, 'limit': limit})
    r = requests.get(r'https://api.tenor.com/v1/search?', params=parameters)
    raw_json = r.json()

    if not raw_json['results']:
        return None

    result_selected = random.choice(raw_json['results'])
    gif_url = result_selected['media'][0]['gif']['url']

    print(f'Tenor URL: {gif_url}')

    gif_bin = requests.get(gif_url).content
    return gif_bin


# Test Code:
# x = get_gif('dog')
# with open('testgif.gif', 'wb') as file:
#     file.write(x)
