import click
from opensubtitles_dl.search import search
import logging
from opensubtitles_dl.utils import file_hash, file_size


@click.command(short_help='Keywords to search')
@click.argument('keywords', nargs=-1, required=True)
@click.option('-l', '--lang', default='eng', show_default=True, help='Subtitle language')
@click.option('-n', '--limit', default=10, show_default=True, help='Maximum number of result to show')
@click.option('-t', '--target', default=None, help='Will calculate target file hash and size for more accurate search')
@click.option('--debug', is_flag=True, help='Switch on to print debug message')
def cli(keywords, lang, limit, target, debug):
    """KEYWORDS is the list of keywords to be search on opensubtitles.org"""
    # default params
    movie_hash, movie_size = None, None
    # if debug is on lower logging level to zero
    if debug:
        logging.basicConfig(level=0)
    # calculate file hash and size if target path is set
    if target:
        movie_hash = file_hash(target)
        movie_size = file_size(target)
        logging.debug(f'target: {target}')
        logging.debug(f'movie_hash: {movie_hash}')
        logging.debug(f'movie_size: {movie_size}')
    # call the search function
    search(keywords, lang, limit, movie_hash, movie_size)


if __name__ == '__main__':
    # cli(('spider', 'man'))
    # cli(('nomadland'))
    cli(('lalaland'), 'all')
