import os
import urllib
import requests
import gzip
import json
import webbrowser
from collections import namedtuple
from itertools import islice
import logging


BASE_URL = 'https://rest.opensubtitles.org/search'
USER_AGENT = 'TemporaryUserAgent'


def _save_sub_link_as(sub_link, save_path, ext):
    resp = urllib.request.urlopen(sub_link)
    save_to = f'{save_path}{ext}'
    with open(save_to, 'wb') as f:
        f.write(gzip.decompress(resp.read()))
    logging.debug(f'save_to = {save_to}')


def search(keywords, lang, limit, file_hash=None, file_size=None, save_path=None):
    # prepare the rest url
    file_hash_string, file_size_string = None, None
    if file_hash and file_size:
        file_hash_string = f'moviebytesize-{file_hash}'
        file_size_string = f'moviehash-{file_size}'
    query_string = urllib.parse.quote(
        f'query-{" ".join(keywords)}') if len(keywords) > 0 else None
    language_string = f'sublanguageid-{lang}'
    non_empty_fields = list(filter(
        None, [file_hash_string, file_size_string, query_string, language_string]))
    logging.debug(f'non_empty_fields = {non_empty_fields}')
    url_suffix = '/'.join(non_empty_fields)
    url = f'{BASE_URL}/{url_suffix}'
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
    entry = namedtuple('entry', 'name language sub_link zip_link')
    results = [entry(r['SubFileName'], r['SubLanguageID'], r['SubDownloadLink'], r['ZipDownloadLink'])
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
        # print all item on each page
        for i, en in enumerate(batch):
            print(f'{p*limit+i+1: >3}. {en.language}, {en.name}')
        # ask for user input
        user_input = input(
            f'[{min(N, (p+1)*limit): >3} / {N}] | #id, (n)ext or (q)uit >>> ')
        if user_input.lower() == 'q':
            return
        if user_input.lower() == 'n' or user_input == '':
            continue
        # if user has chosen a valid id, open or save the links
        chosen_id = int(user_input) - 1
        if save_path:
            sub_link = results[chosen_id].sub_link
            ext = os.path.splitext(results[chosen_id].name)[-1]
            _save_sub_link_as(sub_link, save_path, ext)
        else:
            zip_link = results[chosen_id].zip_link
            webbrowser.get().open_new_tab(zip_link)
        break
