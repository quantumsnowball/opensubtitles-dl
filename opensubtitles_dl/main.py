import os
import click
from opensubtitles_dl.search import search
import logging
from opensubtitles_dl.utils import file_hash, file_size


@click.command(short_help='Keywords to search')
@click.argument('keywords', nargs=-1)
@click.option('-l', '--lang', default='eng', show_default=True, help='Subtitle language')
@click.option('-n', '--limit', default=10, show_default=True, help='Maximum number of result to show')
@click.option('-t', '--target', default=None,
              help='Target file path used to calculate target file hash and size for more accurate search')
@click.option('--auto-save', is_flag=True, help='Switch on to save directly to the same directory if target is provided')
@click.option('--debug', is_flag=True, help='Switch on to print debug message')
def cli(keywords, lang, limit, target, auto_save, debug):
    """KEYWORDS is the list of keywords to be search on opensubtitles.org"""
    # default params
    movie_hash, movie_size = None, None
    save_path = None
    # if no keywords or target file provided, display help and quit
    if len(keywords) == 0 and target is None:
        click.echo(click.get_current_context().get_help())
        return
    # if debug is on lower logging level to zero
    if debug:
        logging.basicConfig(level=0)
    # calculate file hash and size if target path is set
    if target:
        logging.debug(f'target = "{target}"')
        movie_hash = file_hash(target)
        movie_size = file_size(target)
        logging.debug(f'movie_hash = {movie_hash}')
        logging.debug(f'movie_size = {movie_size}')
        # append file name to list of keywords to increase search accuracy
        keywords += (os.path.basename(target), )
        if auto_save:
            save_path = os.path.splitext(target)[0]
    # call the search function
    search(keywords, lang, limit, movie_hash, movie_size, save_path)
