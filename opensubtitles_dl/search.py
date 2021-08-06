import requests


def make_url(*words, lang):
    string = '+'.join(words)
    url = (f'https://www.opensubtitles.org/en/search2/sublanguageid-{lang}/'
           f'moviename-{string}')
    return url


def search(*words, lang):
    url = make_url(*words, lang=lang)
    resp = requests.get(url)

    return url
