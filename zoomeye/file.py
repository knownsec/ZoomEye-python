#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
* Filename: file.py
* Description: here is used to process operation files
* Time: 2020.11.30
* Author: wh0am1i
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
    key_fl = zoomeye_dir + "/apikey"
    # api key config does not exits
    # raise FileNotFoundError
    if not os.path.exists(key_fl):
        raise FileNotFoundError("not found api key config")
    # determine whether the permission of the configuration file is read-only,
    # if not, set it to read-only
    if not oct(os.stat(key_fl).st_mode).endswith("600"):
        os.chmod(key_fl, 0o600)
    # return read file content
    with open(key_fl, 'r') as f:
        return f.read().strip()


def get_jwt_token(path) -> str:
    """
    obtain json web token from local configuration when querying data
    :param path:
    :return:
    """
    key_fl = zoomeye_dir + "/jwt"
    # json web token does not exits
    # raise FileNotFoundError
    if not os.path.exists(key_fl):
        raise FileNotFoundError("not found access token config")


    # determine whether the permission of the configuration file is read-only,
    # if not, set it to read-only
    if not oct(os.stat(key_fl).st_mode).endswith("600"):
        os.chmod(key_fl, 0o600)
    # return read config content
    with open(key_fl, 'r') as f:
        return f.read().strip()


def get_auth_key():
    """
    read configuration file
    :return:
    """
    api_key = None
    try:
        # read the api key from the configuration file,
        # if not, it will throw an exception that the file is not found.
        api_key = get_api_key(zoomeye_dir + "/apikey")
        return api_key
        # catch file not found exception
    except FileNotFoundError:
        print("please run 'zoomeye init -apikey <api key>' before using this command")
        exit(0)
        # catch other exceptions
    except Exception:
        # unknown error
        print("Unknown Error! Please submit issue.")
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
