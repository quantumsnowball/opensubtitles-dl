import click
from opensubtitles_dl.search import search


def cli():
    search('nomadland', lang='eng')


if __name__ == '__main__':
    cli()
