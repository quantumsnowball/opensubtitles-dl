import requests
from bs4 import BeautifulSoup
import pandas as pd


DOMAIN = 'www.opensubtitles.org'


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


def extract_movie_links(table):
    trs = table.select('tr[id^=name]')
    movie_links = []
    for tr in trs:
        link_tag = tr.select_one('td strong a')
        movie_name = link_tag.text.replace('\n', '').strip()
        movie_link = f'https://{DOMAIN}{link_tag["href"]}'
        movie_links.append((movie_name, movie_link, ))
    return movie_links


def extract_subtitle_links(table):
    def extract_innerhtml(ct):
        for i in range(1, len(ct)-1):
            if str(ct[i-1]) == '<br/>' and str(ct[i+1]) == '<br/>':
                try:
                    return ct[i].text.strip()
                except AttributeError:
                    return str(ct[i])
        return ''
    trs = table.select('tr[id^=name]')
    subtitle_links = []
    for tr in trs:
        td_name = tr.select_one('td[id^=main]')
        subtitle_name = extract_innerhtml(td_name.contents)
        tds = tr.select('td')
        subtitle_link = f"https://{DOMAIN}{tds[4].select_one('a')['href']}"
        subtitle_links.append((subtitle_name, subtitle_link, ))
    return subtitle_links


def search(*words, lang):
    # make search request
    url = make_url(*words, lang=lang)
    session = requests.Session()
    session.headers.update({'user-agent': 'Mozilla/5.0'})
    resp = session.get(url)
    # parse html page
    soup = BeautifulSoup(resp.content, 'lxml')
    table = soup.select_one('#search_results')
    if not table:
        print('No search result. Please try other keywords or languages.')
        return
    # check if it is a valid movie list or subtitle list
    head = table.select_one('tr.head')
    if len(head) not in (4, 9):
        print('Unknown html page format. Please try other keywords or languages.')
        return
    # if it is a movie list, let user choose the correct movie
    if len(head) == 4:
        movie_links = extract_movie_links(table)
        print('Please select movie:')
        for i, (movie_name, _, ) in enumerate(movie_links):
            print(f'{i+1: >2}. {movie_name}')
        chosen = int(input('Movie ID: ')) - 1
        # requests again if user has choosen the movie
        url = movie_links[chosen][1]
        print(f'new url: {url}')
        resp = session.get(url)
        soup = BeautifulSoup(resp.content, 'lxml')
        table = soup.select_one('#search_results')
    # extract the search results
    trs = table.select('tr[id^=name]')
    # extract the titles and links
    subtitle_links = extract_subtitle_links(table)
    # let user choose the correct subtitle to download
    print('Please select subtitle:')
    for i, (subtitle_name, _, ) in enumerate(subtitle_links):
        print(f'{i+1: >2}. {subtitle_name}, {_}')
