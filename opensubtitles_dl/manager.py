import click
from opensubtitles_dl.search import search
import logging


@click.command(short_help='Keywords to search')
@click.argument('keywords', nargs=-1, required=True)
@click.option('-l', '--lang', default='eng', show_default=True, help='Subtitle language')
@click.option('-n', '--limit', default=10, show_default=True, help='Maximum number of result to show')
@click.option('--debug', is_flag=True, help='Switch on to print debug message')
def cli(keywords, lang, limit, debug):
    """KEYWORDS is the list of keywords to be search on opensubtitles.org"""
    if debug:
        logging.basicConfig(level=0)
    search(keywords, lang, limit)


if __name__ == '__main__':
    # cli(('spider', 'man'))
    # cli(('nomadland'))
    cli(('lalaland'), 'all')
