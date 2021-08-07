import urllib
import requests
import json
import webbrowser
from collections import namedtuple
from itertools import islice


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
    # let user choose the correct subtitle to download
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
        user_input = input(f'[{(p+1)*limit: >3} / {len(results)}] | #id, (n)ext or (q)uit >>> ')
        if user_input.lower() == 'q':
            return
        if user_input.lower() == 'n' or user_input == '':
            continue
        chosen_id = int(user_input) - 1
        chosen_link = results[chosen_id].link
        webbrowser.get().open_new(chosen_link)
        break
