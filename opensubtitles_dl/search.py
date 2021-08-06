import requests
from bs4 import BeautifulSoup


def make_url(*words, lang):
    string = '+'.join(words)
    url = (f'https://www.opensubtitles.org/en/search2/sublanguageid-{lang}/'
           f'moviename-{string}')
    return url


def extract_innerhtml(ct):
    for i in range(1, len(ct)-1):
        if str(ct[i-1]) == '<br/>' and str(ct[i+1]) == '<br/>':
            try:
                return ct[i].text.strip()
            except AttributeError:
                return str(ct[i])
    return ''


def search(*words, lang):
    url = make_url(*words, lang=lang)
    session = requests.Session()
    session.headers.update({'user-agent': 'Mozilla/5.0'})
    resp = session.get(url)
    with open('html.html', 'wb') as f:
        f.write(resp.content)
    soup = BeautifulSoup(resp.content, 'lxml')
    table = soup.select_one('#search_results')
    trs = table.select('tr[id^=name]')
    for i, tr in enumerate(trs):
        td = tr.select_one('td[id^=main]')
        title = extract_innerhtml(td.contents)
        print(f'{i+1: >2}. {title}')

    return url
