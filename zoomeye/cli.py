#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Filename: cli.py
* Description: cli program entry
* Time: 2020.11.30
* Author: liuf5
*/
"""

import os
import sys
import argparse

module_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
sys.path.insert(1, module_path)

from zoomeye import core


class ZoomEyeParser(argparse.ArgumentParser):
    def error(self, message):
        self.print_help()
        sys.exit(2)


def main():
    """
    parse user input args
    :return:
    """

    parser = ZoomEyeParser()
    subparsers = parser.add_subparsers()

    # zoomeye account info
    parser_info = subparsers.add_parser("info", help="Show ZoomEye account info")
    parser_info.set_defaults(func=core.info)

    # query zoomeye data
    parser_search = subparsers.add_parser(
        "search",
        help="Search the ZoomEye database"
    )

    parser_search.add_argument(
        "dork",
        help="The ZoomEye search keyword or ZoomEye exported file"
    )
    parser_search.add_argument(
        "-num",
        default=20,
        help="The number of search results that should be returned",
        type=int,
        metavar='value'
    )
    parser_search.add_argument(
        "-facet",
        default=None,
        nargs='?',
        const='app,device,service,os,port,country,city',
        type=str,
        help=('''
            Perform statistics on ZoomEye database,
            field: [app,device,service,os,port,country,city]
        '''),
        metavar='field'
    )
    parser_search.add_argument(
        "-filter",
        default=None,
        metavar='field=regexp',
        nargs='?',
        const='app',
        type=str,
        help=('''
              Output more clearer search results by set filter field,
              field: [app,version,device,port,city,country,asn,banner,*]
        ''')
    )
    parser_search.add_argument(
        '-stat',
        default=None,
        metavar='field',
        nargs='?',
        const='app,device,service,os,port,country,city',
        type=str,
        help=('''
              Perform statistics on search results,
              field: [app,device,service,os,port,country,city]
        ''')
    )
    parser_search.add_argument(
        "-save",
        default=None,
        metavar='field=regexp',
        help=('''
              Save the search results with ZoomEye json format,
              if you specify the field, it will be saved with JSON Lines
        '''),
        nargs='?',
        type=str,
        const='all'
    )
    parser_search.add_argument(
        "-count",
        help="The total number of results in ZoomEye database for a search",
        action="store_true"
    )
    parser_search.add_argument(
        "-figure",
        help="Pie chart or bar chart showing data，can only be used under facet and stat",
        choices=('pie', 'hist'),
        default=None
    )
    parser_search.set_defaults(func=core.search)

    # initial account configuration related commands
    parser_init = subparsers.add_parser("init", help="Initialize the token for ZoomEye-python")
    parser_init.add_argument("-apikey", help="ZoomEye API Key", default=None, metavar='[api key]')
    parser_init.add_argument("-username", help="ZoomEye account username", default=None, metavar='[username]')
    parser_init.add_argument("-password", help="ZoomEye account password", default=None, metavar='[password]')
    parser_init.set_defaults(func=core.init)

    args = parser.parse_args()

    try:
        args.func(args)
    except AttributeError:
        parser.print_help()


if __name__ == '__main__':
    main()
