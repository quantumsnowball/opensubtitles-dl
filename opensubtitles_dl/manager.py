import click
from opensubtitles_dl.search import search


def cli():
    print(search('hello', 'world', lang='abc'))


if __name__ == '__main__':
    cli()
