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
