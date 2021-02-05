#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
* Filename: data.py
* Description: used to process various data.
* Time: 2020.11.30
* Author: liuf5
*/
"""
import re
import json
import os
import time
import hashlib

from zoomeye import config, file
from zoomeye.sdk import ZoomEye, fields_tables_host
from zoomeye.sdk import ZoomEyeDict
from zoomeye import show

zoomeye_dir = os.path.expanduser(config.ZOOMEYE_CONFIG_PATH)


stat_host_table = {
    'app':      'portinfo.app',
    'device':   'portinfo.device',
    'service':  'portinfo.service',
    'os':       'portinfo.os',
    'port':     'portinfo.port',
    'country':  'geoinfo.country.names.en',
    'city':     'geoinfo.city.names.en'
}


def get_item(data):
    """
    take out the corresponding data from the json file.
    :param data: dork data ,dict
    :return:
    """
    if data:
        ip = data.get('ip')
        country = data.get("geoinfo").get("country").get("names").get("en")
        port = data.get("portinfo").get("port")
        app = data.get("portinfo").get("app")
        banner = data.get("portinfo").get("banner")
        service = data.get("portinfo").get("service")
        return ip, country, port, app, banner, service
    else:
        show.printf("data cannot be empty", color='red')
        exit(0)


def md5_convert(string):
    """
    calculate the md5 of a string
    :param string: input string
    :return: md5 string
    """
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


class Cache:
    """
    used to cache the data obtained from the api to the local,
    or directly clip the file from the local.
    """

    def __init__(self, dork, page=0):
        self.dork = dork
        self.page = page
        self.resource = "host"
        self.cache_folder = os.path.expanduser(config.ZOOMEYE_CACHE_PATH)
        self.filename = self.cache_folder + config.FILE_NAME.format(md5_convert(dork), page)

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
        file.write_file(self.filename, data)

    def load(self):
        """
        files in the cache from the local folder
        :return:
        """
        result_data = []
        facet_data = None
        read_data = file.read_file(self.filename)
        data_json = json.loads(read_data)
        """
        process the data loaded from the cache file, 
        the processed data structure is list. like:
        [{...}, {...},{...}...]
        """
        for i in data_json.get("matches"):
            result_data.append(i)
        # get facet
        if data_json.get("facets"):
            facet_data = data_json.get("facets")
        # get data total
        total = data_json.get("total")
        # return
        return result_data, facet_data, total


class CliZoomEye:
    """
    the ZoomEye instance in cli mode has added storage compared to
    the ZoomEye instance of the API, to determine where
    to get the data, cache or api.
    By the way, cli mode supports search for "host", but "web" search is not currently supported
    """

    def __init__(self, dork, num, facet=None):
        self.dork = dork
        self.num = num
        self.facet = facet

        self.dork_data = []
        self.facet_data = None
        self.total = 0

        self.api_key, self.access_token = file.get_auth_key()
        self.zoomeye = ZoomEye(api_key=self.api_key, access_token=self.access_token)

    def handle_page(self):
        """
        convert the number of data into pages and round up.
        ex: num = 30, page = 2.
        because the API returns 20 pieces of data each time.
        :return:
        """
        num = int(self.num)
        if num % 20 == 0:
            return int(num / 20)
        return int(num / 20) + 1

    def auto_cache(self, data, page):
        """
        cache to local
        :param page:
        :param data:
        :return:
        """
        cache = Cache(self.dork, page)
        cache.save(json.dumps(data))

    def from_cache_or_api(self):
        """
        get data from cache or api
        get data from the api if there is no data in the cache.
        :return:
        """

        page = self.handle_page()

        for p in range(page):
            cache = Cache(self.dork, page=p)
            # get data from cache file
            if cache.check():
                # return dork, facet, total data
                dork_data_list, self.facet_data, self.total = cache.load()
                self.dork_data.extend(dork_data_list)
            else:
                # no cache, get data from API
                self.facet = ['app', 'device', 'service', 'os', 'port', 'country', 'city']
                try:
                    dork_data_list = self.zoomeye.dork_search(
                        dork=self.dork,
                        page=p + 1,
                        resource="host",
                        facets=self.facet
                    )
                except ValueError:
                    print("the access token expires, please re-run [zoomeye init] command. "
                          "it is recommended to use API KEY for initialization!")
                    exit(0)
                self.facet_data = self.zoomeye.facet_data
                self.total = self.zoomeye.total
                self.dork_data.extend(dork_data_list)
                if dork_data_list:
                    self.auto_cache(self.zoomeye.raw_data, p)
        # return dork, facet,total data
        return self.dork_data[:self.num], self.facet_data, self.total

    def filter_data(self, keys, data):
        """
        get the data of the corresponding field
        :param keys: list, user input field
        :param data: list, zoomeye api data
        :return: list, ex: [[1,2,3...],[1,2,3...],[1,2,3...]...]
        """
        result = []
        for d in data:
            item = []
            zmdict = ZoomEyeDict(d)
            for key in keys:
                if fields_tables_host.get(key.strip()) is None:
                    support_fields = ','.join(list(fields_tables_host.keys()))
                    show.printf("filter command has unsupport fields [{}], support fields has [{}]"
                                .format(key, support_fields), color='red')
                    exit(0)
                res = zmdict.find(fields_tables_host.get(key.strip()))
                item.append(res)
            result.append(item)
        return result

    def regexp_data(self, keys):
        """
        filter based on fields entered by the user
        AND operation on multiple fields
        :param keys: str , user input filter filed
        :return: list, ex:[{...}, {...}, {...}...]
        """
        keys = keys.split(",")
        result = []
        self.zoomeye.data_list = self.dork_data[:self.num]

        data_list = self.zoomeye.data_list
        for key in keys:
            result = []
            for da in data_list:
                zmdict = ZoomEyeDict(da)
                input_key, input_value = key.split("=")
                if fields_tables_host.get(input_key.strip()) is None:
                    # check filed effectiveness
                    support_fields = ','.join(list(fields_tables_host.keys()))
                    show.printf("filter command has unsupport fields [{}], support fields has [{}]"
                                .format(input_key, support_fields), color='red')
                    exit(0)
                # the value obtained here is of type int, and the user's input is of type str,
                # so it needs to be converted.
                if input_key == "port":
                    input_value = str(input_value)
                find_value = zmdict.find(fields_tables_host.get(input_key.strip()))
                # get the value through regular matching
                try:
                    regexp_result = re.search(str(input_value), str(find_value), re.I)
                except re.error:
                    show.printf('the regular expression you entered is incorrect, please check!', color='red')
                    exit(0)
                except Exception as e:
                    show.printf(e, color='red')
                    exit(0)
                # the matched value is neither None nor empty
                if regexp_result and regexp_result.group(0) != '':
                    result.append(da)
            # AND operation
            data_list = result
        return result

    def cli_filter(self, keys, save=False):
        """
        this function is used to filter the results.
        :param save:
        :param keys: str, filter condition. ex: 'ip, port, app=xxx'
        :return: None
        """
        has_equal = []
        not_equal = []
        # set the ip field to be displayed by default and in the first place
        key_list = keys.split(',')
        try:
            # set ip field in the first place
            key_index = key_list.index("ip")
            key_list.pop(key_index)
            key_list.insert(0, 'ip')
        # add IP to the first item when there is no IP
        except ValueError:
            key_list.insert(0, 'ip')
        # process user input fields, separating single fields from fields with equal signs.
        for key in key_list:
            res = key.split('=')
            # field with equal sign
            if len(res) == 2:
                has_equal.append(key)
                not_equal.append(res[0])
            # No field with equal sign
            if len(res) == 1:
                # handle the case where the wildcard character * is included in the filed
                # that is, query all fields
                if key == "*":
                    not_equal = list(fields_tables_host.keys())
                    continue
                else:
                    not_equal.append(key)
        # the filter condition is port, banner, app=**
        # ex:port,banner,app=MySQL
        if len(has_equal) != 0:
            equal = ','.join(has_equal)
            equal_data = self.regexp_data(equal)
        # the filter condition is app, port
        # ex: ip,port,app
        else:
            equal_data = self.dork_data[:self.num]
        # get result
        result = self.filter_data(not_equal, equal_data)
        equal = ','.join(not_equal)
        if save:
            return equal, result
        show.print_filter(equal, result)

    def save(self, fields):
        """
        save the data to a local json file,
        you cannot specify the save path, but you can specify the save data
        :param fields: str, filter fields, ex: app=xxxx
        :return:
        """
        # -save default, data format ex:
        # {"total":xxx, "matches":[{...}, {...}, {...}...], "facets":{{...}, {...}...}}
        
        # filter special characters in file names
        name = re.findall(r"[a-zA-Z0-9_\u4e00-\u9fa5]+", self.dork)
        re_name = '_'.join(name)

        if fields == 'all':
            filename = "{}_{}_{}.json".format(re_name, self.num, int(time.time()))
            data = {
                'total': self.total,
                'matches': self.dork_data[:self.num],
                'facets': self.facet_data
            }
            file.write_file(filename, json.dumps(data))
            show.printf("save file to {}/{} successful!".format(os.getcwd(), filename), color='green')
        # -save xx=xxxx, save the filtered data. data format ex:
        # {app:"xxx", "app":"httpd",.....}
        else:
            key, value = self.cli_filter(fields, save=True)
            filename = "{}_{}_{}.json".format(re_name, len(value), int(time.time()))
            # parser data
            for v in value:
                dict_save = {}
                for index in range(len(key.split(','))):
                    dict_key = key.split(',')[index]
                    dict_value = v[index]
                    dict_save[dict_key] = dict_value
                # write to local file
                file.add_to_file(filename, str(dict_save))
            show.printf("save file to {}/{} successful!".format(os.getcwd(), filename), color='green')

    def load(self):
        """
        load a local file
        it must be a json file and the data format is the format exported by zoomeye.
        format is {"total":123123, "matches":[{...}, {...}, {...}...], "facets":{{...}, {...}...}}
        :param path:
        :return:
        """
        data = file.read_file(self.dork)
        json_data = json.loads(data)
        self.total = json_data.get("total", 0)
        self.dork_data = json_data.get("matches", "")
        self.facet_data = json_data.get("facets", "")

        if self.total == 0 and self.dork_data == "" and self.facet_data:
            print("file format error!")
            exit(0)
        self.num = len(self.dork_data)
        return self.dork_data, self.facet_data, self.total

    def statistics(self, keys, figure):
        """
        perform data aggregation on the currently acquired data instead of
        directly returning the result of the data aggregation of the API.
        :param keys: str, user input filter fields
        :param figure: str, user input filter fields
        {'app': {'Gunicorn': 2, 'nginx': 14, 'Apache httpd': 9, '[unknown]': 3, 'Tornado httpd': 2}, 'port': {443: 29, 8443: 1}}
        :return: None
        """
        data = {}
        key_list = keys.split(',')
        # cycle key
        for key in key_list:
            count = {}
            for item in self.dork_data[:self.num]:
                zmdict = ZoomEyeDict(item)
                if stat_host_table.get(key.strip()) is None:
                    # check filed effectiveness
                    support_fields = ','.join(list(stat_host_table.keys()))
                    show.printf("filter command has unsupport fields [{}], support fields has [{}]"
                                .format(key, support_fields), color='red')
                    exit(0)
                fields = zmdict.find(stat_host_table.get(key.strip()))
                # the value of the result field returned by the API may be empty
                if fields == '':
                    fields = '[unknown]'
                r = count.get(fields)
                if not r:
                    count[fields] = 1
                else:
                    count[fields] = count[fields] + 1
            data[key] = count
        # print result for current data aggregation
        show.print_stat(keys, data, self.num, figure)
