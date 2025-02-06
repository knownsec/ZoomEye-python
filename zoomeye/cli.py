#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Filename: cli.py
* Description: cli program entry
* Time: 2020.11.30
* Author: wh0am1i
*/
"""

import os
import sys
import argparse

module_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, module_path)

from zoomeye import core
from zoomeye.config import BANNER


def get_version():
    print(BANNER)


class ZoomEyeParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(2)


def main():
    """
    parse user input args
    :return:
    """

    parser = ZoomEyeParser(prog='zoomeye')
    subparsers = parser.add_subparsers()
    # show ZoomEye-python version number
    parser.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="show program's version number and exit"
    )

    # zoomeye account info
    parser_info = subparsers.add_parser("info", help="Show ZoomEye account info")
    parser_info.set_defaults(func=core.info)

    # initial account configuration related commands
    parser_init = subparsers.add_parser("init", help="Initialize the token for ZoomEye-python")
    parser_init.add_argument("-apikey", help="ZoomEye API Key", default=None, metavar='[api key]')
    parser_init.set_defaults(func=core.init)

    # query zoomeye data
    search_v2_parser = subparsers.add_parser("search",
                                             help="get network asset information based on query conditions.")
    search_v2_parser.add_argument("dork", type=str, help="search key word(eg=baidu.com)", default=None)

    search_v2_parser.add_argument(
        "-facets",
        default='',
        type=str,
        help=('''
                  if this parameter is specified,
                         the corresponding data will be displayed
                         at the end of the returned result.
                         supported : 'product', 'device', 'service', 'os', 'port', 'country', 'subdivisions', 'city'
              '''),
        metavar='facets'
    )
    search_v2_parser.add_argument(
        "-fields",
        default='',
        metavar='field=regexp',
        type=str,
        help=('''
                   display data based on input fields
                   please see: https://www.zoomeye.org/doc/
              ''')
    )
    search_v2_parser.add_argument("-sub_type", type=str, help="specify the type of data to search",
                                  choices=('v4', 'v6', 'web', 'all'), default='all')
    search_v2_parser.add_argument("-page", metavar='page', type=int, help="view the page of the query result",
                                  default=1)
    search_v2_parser.add_argument('-pagesize', metavar='pagesize', type=int,
                                  help="specify the number of pagesize to search", default=20)
    search_v2_parser.add_argument(
        "-figure",
        help="Pie chart or bar chart showing data，can only be used under facet and stat",
        choices=('pie', 'hist'),
        default=None
    )
    search_v2_parser.add_argument(
        "-save",
        help="Save search to local file",
        action='store_true',
    )
    search_v2_parser.add_argument(
        "-force",
        help=(
            """
            Ignore the local cache and force the data to be obtained from the API
            """
        ),
        action="store_true"
    )
    search_v2_parser.set_defaults(func=core.search)

    parser_clear = subparsers.add_parser("clear", help="Manually clear the cache and user information")
    parser_clear.add_argument(
        "-setting",
        help="clear user api key and access token",
        action="store_true"
    )
    parser_clear.add_argument(
        "-cache",
        help="clear local cache file",
        action="store_true"
    )
    parser_clear.set_defaults(func=core.clear_file)

    args = parser.parse_args()

    if args.version:
        get_version()
        exit(0)

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == '__main__':
    main()
