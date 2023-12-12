#! /usr/bin/env python

import pkg_resources

__author__ = "JP Etcheber"
__email__ = "jetcheber@gmail.com"
__version__ = pkg_resources.get_distribution('j2express').version

from j2express.cli import main

if __name__ == '__main__':
    main()
