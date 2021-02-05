#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
* Filename: config.py
* Description: command tool config
* Time: 2020.11.30
* Author: liuf5
*/
"""
import string


# save api key file and json web token file path
ZOOMEYE_CONFIG_PATH = "~/.config/zoomeye/setting"

# save search dork data path
ZOOMEYE_CACHE_PATH = "~/.config/zoomeye/cache"

# cache expired time, five day
EXPIRED_TIME = 60 * 60 * 24 * 5

# print data max length
STRING_MAX_LENGTH = 30

# cache file name
FILE_NAME = "/{}_{}.json"


RADIUS = 7

CHARACTER = "# "

BLANK = "  "

COLOR_TABLE = ["\x1b[90m", "\x1b[91m", "\x1b[92m", "\x1b[93m", "\x1b[94m", "\x1b[95m", "\x1b[96m", "\x1b[97m",
               "\x1b[91m", "\x1b[92m"]

COLOR_RESET = "\x1b[0m"
