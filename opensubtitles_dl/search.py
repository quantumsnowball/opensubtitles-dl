import urllib
import requests
import json
import webbrowser
from collections import namedtuple
from itertools import islice
import logging


BASE_URL = 'https://rest.opensubtitles.org/search'
USER_AGENT = 'TemporaryUserAgent'


def search(words, lang, limit, file_hash=None, file_size=None):
    # prepare the rest url
    query_string = urllib.parse.quote(f'query-{" ".join(words)}')
    language_string = f'sublanguageid-{lang}'
    url = f'{BASE_URL}/{query_string}/{language_string}'
    logging.debug(f'url = "{url}"')
    # make rest request using the Agent
    session = requests.Session()
    session.headers.update({'user-agent': USER_AGENT})
    resp = session.get(url)
    # make sure the response is successful
    logging.debug(f'response code = {resp.status_code}')
    if resp.status_code != 200:
        print(
            f'Server returned {resp.status_code}. Please try other keywords or languages.')
        return
    raw = json.loads(resp.content)
    # if no result returned, quit the program
    logging.debug(f'len(raw) = {len(raw)}')
    if len(raw) <= 0:
        print('No result. Please try other keywords or languages.')
        return
    # parse and filter the json response
    entry = namedtuple('entry', 'name language link')
    results = [entry(r['SubFileName'], r['SubLanguageID'], r['ZipDownloadLink'])
               for r in raw]
    # let user choose the correct subtitle to download
    N = len(results)
    print('Please select subtitle by id:')

    def get_batch():
        itr = iter(results)
        batch = list(islice(itr, limit))
        while batch:
            yield batch
            batch = list(islice(itr, limit))
    for p, batch in enumerate(get_batch()):
        for i, en in enumerate(batch):
            print(f'{p*limit+i+1: >3}. {en.language}, {en.name}')
        user_input = input(
            f'[{min(N, (p+1)*limit): >3} / {N}] | #id, (n)ext or (q)uit >>> ')
        if user_input.lower() == 'q':
            return
        if user_input.lower() == 'n' or user_input == '':
            continue
        chosen_id = int(user_input) - 1
        chosen_link = results[chosen_id].link
        webbrowser.get().open_new(chosen_link)
        break
