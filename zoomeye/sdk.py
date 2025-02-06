#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
* Filename: zoomeye.py
* Description:
* Time: 2020.11.25
* Author: wh0am1i
*/
"""

import base64

import requests


class ZoomEyeDict:

    def __init__(self, data):
        self.dict = dict(data)

    def find(self, key):
        """
        get the value in the nested dictionary by <"key1.key2.key3">
        :param key: str, dictionary key like: "a.b.c"
        :return:
        """
        values = None
        # is dict?
        if isinstance(self.dict, dict):
            keys = key.split(".")
            inputData = self.dict
            for k in keys:
                if k == 'geoinfo' and inputData.get(k) == None:
                    k = "aiweninfo" if inputData.get("aiweninfo") else "ipipinfo"
                if inputData.get(k) is not None:
                    values = inputData.get(k)
                else:
                    values = None
                if isinstance(values, list):
                    if len(values) != 0:
                        values = values[0]
                    else:
                        values = '[unknown]'
                inputData = values
            return values
        else:
            raise TypeError("the parameter you pass in must be a dictionary, not a {}".format(type(self.dict)))


class ZoomEye:

    def __init__(self, api_key=""):
        self.api_key = api_key

        # 3.0.0
        self.search_api = "https://api.zoomeye.org/v2/search"
        self.userinfo_api = "https://api.zoomeye.org/v2/userinfo"

    def _request(self, url, params=None, headers=None, method='GET'):
        """
        encapsulate the requests part
        :param url: send request url
        :param params: request params
        :param headers: request header
        :param method: send request method， only support method GET and POST
        :return: json data
        """
        # if method is "GET" use requests.get
        if method == "GET":
            resp = requests.get(url, params=params, headers=headers)
        # post json body
        elif method == "POST" and headers.get("Content-Type", "") == "application/json":
            resp = requests.post(url, json=params, headers=headers)
        # request method is "POST"
        else:
            resp = requests.post(url, data=params, headers=headers)
            # print(resp.text)
        # if response succeed and status code is 200 return json data
        if resp and resp.status_code == 200:
            data = resp.json()
            return data
        # Request data exceeds the total amount of ZoomEye data,
        # return all data instead of throwing an exception
        elif resp.status_code == 403 and 'specified resource' in resp.text:
            return None
        # if response succeed and status code is not 200 return error format json
        # others error return unknown error
        else:
            raise ValueError(resp.json().get('message'))

    def _check_header(self):
        """
        2023-04 remove username & password authenticate
        only support API-KEY authenticate
        """
        if self.api_key:
            headers = {
                'API-KEY': self.api_key,
            }
        else:
            headers = {}
        # add user agent
        headers[
            "User-Agent"] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
        return headers

    """
    version: 3.0.0
    """

    def userinfo(self):
        headers = self._check_header()
        resp = self._request(self.userinfo_api,
                             method='POST',
                             params={},
                             headers=headers)
        return resp

    def search(self, dork, qbase64='', page=1, pagesize=20, sub_type='all', fields='', facets='') -> dict:
        """
         get network asset information based on query conditions.
         mainly used to search asset data from zoomeye.
        please see: https://www.zoomeye.org/doc
        :param dork:str,
                    ex: country=cn
                    dork to search
        :param qbase64:str,
                    ex: country=cn
                    base64 dork to search
        :param sub_type:str,
                    specify the type of data to search
                    supported : 'v4', 'v6', 'web', 'all
        :param page: int,
                    specify the number of pages to return data, each page contains 20 data
        :param pagesize: int,
                    specify the number of pagesize to search
        :param fields: str,
                        display data based on input fields
        :param facets: str,
                     if this parameter is specified,
                     the corresponding data will be displayed
                     at the end of the returned result.
                     supported : 'product', 'device', 'service', 'os', 'port', 'country', 'subdivisions', 'city'
        :return: dict

        """
        if qbase64:
            dork = qbase64
        elif qbase64 == '' and dork != '':
            dork = base64.b64encode(dork.encode('utf-8')).decode('utf-8')
        else:
            raise Exception("dork and qbase64 can't be empty at the same time")
        headers = self._check_header()
        headers["Content-Type"] = "application/json"
        params = {"qbase64": dork, "sub_type": sub_type, "page": page, "facets": facets, "fields": fields,
                  "pagesize": pagesize}
        resp = self._request(self.search_api,
                             method='POST',
                             params=params,
                             headers=headers)
        return resp


def zoomeye_api_test():
    zoomeye = ZoomEye()
    zoomeye.api_key = input('ZoomEye API-KEY:')

    """
    version: 3.0.0
    """
    print(zoomeye.userinfo())

    data = zoomeye.search('country=cn')
    print(data)


if __name__ == "__main__":
    zoomeye_api_test()
