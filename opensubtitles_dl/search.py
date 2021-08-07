import urllib
import requests
import json
import webbrowser
from collections import namedtuple


BASE_URL = 'https://rest.opensubtitles.org/search'
USER_AGENT = 'TemporaryUserAgent'


def search(words, lang, limit):
    # prepare the rest url
    query_string = urllib.parse.quote(f'query-{" ".join(words)}')
    language_string = f'sublanguageid-{lang}'
    url = f'{BASE_URL}/{query_string}/{language_string}'
    # make rest request using the Agent
    session = requests.Session()
    session.headers.update({'user-agent': USER_AGENT})
    resp = session.get(url)
    raw = json.loads(resp.content)
    # if no result returned, quit the program
    if len(raw) <= 0:
        print('No result. Please try other keywords or languages.')
        return
    # parse and filter the json response
    entry = namedtuple('entry', 'name language link')
    results = [entry(r['SubFileName'], r['SubLanguageID'], r['ZipDownloadLink'])
               for r in raw]
    print(f'Showing top {limit} out of {len(results)} results.')
    # let user choose the correct subtitle to download
    print('Please select subtitle:')
    for i, en in enumerate(results[:limit]):
        print(f'{i+1: >2}. {en.language}, {en.name}')
    chosen_id = int(input('ID: ')) - 1
    chosen_link = results[chosen_id].link
    webbrowser.get().open_new(chosen_link)
