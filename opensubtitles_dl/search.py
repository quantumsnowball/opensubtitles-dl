import requests
from bs4 import BeautifulSoup


def make_url(*words, lang):
    string = '+'.join(words)
    url = (f'https://www.opensubtitles.org/en/search2/sublanguageid-{lang}/'
           f'moviename-{string}')
    return url


def search(*words, lang):
    url = make_url(*words, lang=lang)
    session = requests.Session()
    session.headers.update({'user-agent': 'Mozilla/5.0'})
    resp = session.get(url)
    with open('html.html', 'wb') as f:
        f.write(resp.content)
    soup = BeautifulSoup(resp.content)
    table = soup.select_one('#search_results')

    

    return url
