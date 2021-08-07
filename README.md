# opensubtitles-dl

## Overview
Search and download from opensubtitles.org from the command line.

## Install
To install the `master` branch by default:

    pip install --force git+https://github.com/quantumsnowball/opensubtitles-dl.git

To install the `dev` branch including the most updated features:

    pip install --force git+https://github.com/quantumsnowball/opensubtitles-dl.git@dev

## Usage
    Usage: opensubtitles-dl [OPTIONS] KEYWORDS...

      KEYWORDS is the list of keywords to search on opensubtitles.org

    Options:
      -l, --lang TEXT      Subtitle language  [default: eng]
      -n, --limit INTEGER  Maximum number of result to show  [default: 10]
      --debug              Switch on to print debug message
      --help               Show this message and exit.
