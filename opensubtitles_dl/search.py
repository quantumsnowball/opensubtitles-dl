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


def extract_movie_links(table):
    trs = table.select('tr[id^=name]')
    movie_links = []
    for tr in trs:
        link_tag = tr.select_one('td strong a')
        movie_name = link_tag.text.replace('\n', '').strip()
        movie_link = link_tag['href']
        movie_links.append((movie_name, movie_link, ))
    return movie_links


def extract_titles(trs):
    titles = []
    for tr in trs:
        td = tr.select_one('td[id^=main]')
        title = extract_innerhtml(td.contents)
        titles.append(title)
    return titles


def extract_links(trs, domain='www.opensubtitles.org'):
    links = []
    for tr in trs:
        tds = tr.select('td')
        link = tds[4].select_one('a')['href']
        links.append(f'https://{domain}{link}')
    return links


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
        movie_names = extract_movie_links(table)
        print('Please select movie name:')
        for i, (movie_name, movie_link, ) in enumerate(movie_names):
            print(f'{i+1: >2}. {movie_name}, {movie_link}')
        # requests again if user has choosen the movie
    return
    # extract the search results
    trs = table.select('tr[id^=name]')
    # extract the titles and links
    titles = extract_titles(trs)
    links = extract_links(trs)
    # let user choose the correct subtitle to download
    # debug
    for i, title in enumerate(titles):
        print(f'{i+1: >2}. {title}')
    for i, link in enumerate(links):
        print(f'{i+1: >2}. {link}')
