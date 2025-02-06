#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
* Filename: tools.py
* Description:
* Time: 2025.02.05
* Author: wh0am1i
*/
"""

import json
import os
import time
import datetime
import hashlib
from zoomeye import config
from zoomeye.sdk import ZoomEyeDict
from zoomeye import show

zoomeye_dir = os.path.expanduser(config.ZOOMEYE_CONFIG_PATH)


def md5_convert(string):
    """
    calculate the md5 of a string
    :param string: input string
    :return: md5 string
    """
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def convert_str(s):
    """
    convert arbitrary string to another string, for print and human readable
    :param:
    :return:
    """
    res = []
    d = {
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        '\b': '\\b',
        '\a': '\\a',
    }
    for c in s:
        if c in d.keys():
            res.append(d[c])
        else:
            res.append(c)
    return ''.join(res)


def omit_str(text, index=0):
    """
    ignore part of the string
    :param text: str, text to be omitted
    :param index: int, position omitted on the longest basis
    :return: str, ex: string...
    """
    if len(text) < config.STRING_MAX_LENGTH:
        return text

    return text[:config.STRING_MAX_LENGTH - index] + '...'


class Cache:
    """
    used to cache the data obtained from the api to the local,
    or directly clip the file from the local.
    """

    def __init__(self, dork, page, pagesize, facets, fields, sub_type):
        self.dork = dork
        self.page = page
        self.pagesize = pagesize
        self.facets = facets
        self.fields = fields
        self.sub_type = sub_type
        self.cache_folder = os.path.expanduser(config.ZOOMEYE_CACHE_PATH)
        cache_filename = "{}_{}_{}_{}".format(dork, facets, fields, sub_type)
        self.filename = self.cache_folder + config.FILE_NAME.format(md5_convert(cache_filename), page*pagesize)

    def check(self):
        """
        used to detect whether there is a local cache file,
        and check whether the local cache file expires.
        :return: bool
        """
        # exist?
        if not os.path.exists(self.filename):
            return False
        # check expired
        file_create_time = os.path.getatime(self.filename)
        # expired time is five day, time stamp = 60 * 60 * 24 * 5
        if int(time.time()) - int(file_create_time) > config.EXPIRED_TIME:
            # delete expired cache file
            os.remove(self.filename)
            return False
        # the cache file exists and has not expired
        else:
            return True

    def save(self, data):
        # folder is exists?
        if not os.path.isdir(self.cache_folder):
            try:
                # create folder when folder does not exists
                os.makedirs(self.cache_folder)
            except OSError:
                raise Exception("init dirs failed {}".format(self.cache_folder))
        # write to local
        with open(self.filename, 'w') as f:
            f.write(json.dumps(data))

    def load(self):
        """
        files in the cache from the local folder
        :return:
        """
        with open(self.filename, 'r') as f:
            read_data = f.read()
        data_json = json.loads(read_data)
        return data_json

    def update(self):
        pass