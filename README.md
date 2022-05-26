# opensubtitles-dl

## Overview
Search and download from opensubtitles.org from the command line.

## Install
To install from PyPi, simply run:

    pip install opensubtitles-dl
    
To install the `master` branch from git:

    pip install --force git+https://github.com/quantumsnowball/opensubtitles-dl.git

To install the `dev` branch including the most updated features:

    pip install --force git+https://github.com/quantumsnowball/opensubtitles-dl.git@dev

## Usage
    Usage: opensubtitles-dl [OPTIONS] [KEYWORDS]...

      KEYWORDS is the list of keywords to be search on opensubtitles.org

    Options:
      -l, --lang TEXT      Subtitle language  [default: eng]
      -n, --limit INTEGER  Maximum number of result to show  [default: 10]
      -t, --target TEXT    Target file path used to calculate target file hash and size for more accurate search
      --auto-save          Switch on to save directly to the same directory if target is provided
      --debug              Switch on to print debug message
      --help               Show this message and exit.
