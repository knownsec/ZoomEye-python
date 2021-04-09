#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
* Filename: file.py
* Description: here is used to process operation files
* Time: 2020.11.30
* Author: liuf5
*/
"""
import os

from zoomeye import config

zoomeye_dir = os.path.expanduser(config.ZOOMEYE_CONFIG_PATH)


def get_api_key(path) -> str:
    """
    obtain api key from local configuration when querying data
    :param path:
    :return:
    """
    key_file = zoomeye_dir + "/apikey"
    # api key config does not exits
    # raise FileNotFoundError
    if not os.path.exists(key_file):
        raise FileNotFoundError("not found api key config")
    # determine whether the permission of the configuration file is read-only,
    # if not, set it to read-only
    if not oct(os.stat(key_file).st_mode).endswith("600"):
        os.chmod(key_file, 0o600)
    # return read file content
    with open(key_file, 'r') as f:
        return f.read().strip()


def get_jwt_token(path) -> str:
    """
    obtain json web token from local configuration when querying data
    :param path:
    :return:
    """
    key_file = zoomeye_dir + "/jwt"
    # json web token does not exits
    # raise FileNotFoundError
    if not os.path.exists(key_file):
        raise FileNotFoundError("not found access token config")

    # determine whether the permission of the configuration file is read-only,
    # if not, set it to read-only
    if not oct(os.stat(key_file).st_mode).endswith("600"):
        os.chmod(key_file, 0o600)
    # return read config content
    with open(key_file, 'r') as f:
        return f.read().strip()


def get_auth_key():
    """
    read configuration file
    :return:
    """
    api_key = None
    access_token = None
    try:
        # read the api key from the configuration file,
        # if not, it will throw an exception that the file is not found.
        api_key = get_api_key(zoomeye_dir + "/apikey")
        return api_key, access_token
        # catch file not found exception
    except FileNotFoundError:
        # try to get the json web token in the configuration file
        try:
            access_token = get_jwt_token(zoomeye_dir + "/jwt")
            return api_key, access_token
        except FileNotFoundError:
            print("please run 'zoomeye init -apikey <api key>' "
                  "or 'zoomeye init -username <username> -password <password>before using this command")
            exit(0)
        # catch other exceptions
    except Exception:
        # there is no past api key and json web token in the configuration file
        # tell users that they need to be initialized before use
        print("please run 'zoomeye init -apikey <api key>' "
              "or 'zoomeye init -username <username> -password <password>before using this command")
        exit(0)


def check_exist(file):
    # whether the zoomeye configuration folder exists
    if not os.path.isdir(file):
        try:
            # create folder when folder does not exits
            os.makedirs(file)
        except OSError as e:
            # raise error when create failed time
            raise Exception("init folder failed {}, error:{}".format(zoomeye_dir, e))


def add_to_file(path, data):
    """
    append data to local file
    :param path: str, local path
    :param data: str, date write to local file
    :return:
    """
    with open(path, 'a') as f:
        f.write(data + '\n')
