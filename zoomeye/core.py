"""
* Filename: core.py
* Description: cli core function, processing various requests
* Time: 2020.11.30
* Author: liuf5
*/
"""

import re
import os
from zoomeye import config, file, show
from zoomeye.sdk import ZoomEye
from zoomeye.data import CliZoomEye, HistoryDevice

# save zoomeye config folder
zoomeye_dir = os.path.expanduser(config.ZOOMEYE_CONFIG_PATH)


def key_init(key):
    """
    initialize through the api key, write the api key to the local configuration file,
    theoretically it will never expire unless you remake the api key
    :param key: user input API key
    :return:
    """
    file.check_exist(zoomeye_dir)
    key = key.strip()
    try:
        zoom = ZoomEye(api_key=key)
    except Exception:
        return
    # api key save path
    key_file = zoomeye_dir + "/apikey"
    # display the remaining resources of the current account
    user_data = zoom.resources_info()
    show.printf("Role: {}".format(user_data["plan"]))
    show.printf("Quota: {}".format(user_data["resources"].get("search")))
    # save api key
    file.write_file(key_file, key)
    show.printf("successfully initialized", color="green")
    # change the permission of the configuration file to read-only
    os.chmod(key_file, 0o600)


def jwt_init(username, password):
    """
    initialize through the user name and password, write jwt to the local configuration file,
    the expiration time is about 12 hours, so it is recommended to initialize through the api key.
    :param username: str, login zoomeye account
    :param password: str, login zoomeye account password
    :return:
    """
    file.check_exist(zoomeye_dir)
    try:
        zoom = ZoomEye(username=username, password=password)
        access_token = zoom.login()
    except Exception:
        return
    jwt_file = zoomeye_dir + "/jwt"
    if access_token:
        # display the remaining resources of the current account
        user_data = zoom.resources_info()
        show.printf("Role: {}".format(user_data["plan"]))
        show.printf("Quota: {}".format(user_data["resources"].get("search")))

        file.write_file(jwt_file, access_token)
        show.printf("successfully initialized", color="green")
        # change the permission of the configuration file to read-only
        os.chmod(jwt_file, 0o600)
    else:
        show.printf("failed initialized!", color="red")


def init(args):
    """
    the initialization processing function will select the initialization method according to the user's input.
    :param args:
    :return:
    """
    api_key = args.apikey
    username = args.username
    password = args.password
    # use api key init
    if api_key and username is None and password is None:
        key_init(api_key)
        return
    # use username and password init
    if api_key is None and username and password:
        jwt_init(username, password)
        return
    # invalid parameter
    show.printf("input parameter error", color="red")
    show.printf("please run <zoomeye init -h> for help.", color="red")


def search(args):
    """
    search for dork functions, support filtering and view detailed data
    :param args:
    :return:
    """
    dork = args.dork
    num = args.num
    facet = args.facet
    filters = args.filter
    stat = args.stat
    save = args.save
    count_total = args.count
    figure = args.figure
    force = args.force

    cli_zoom = CliZoomEye(dork, num, facet=facet, force=force)
    # load local zoomeye export file
    if os.path.exists(dork):
        dork_data, facet_data, total = cli_zoom.load()
    # get data by cache file or api
    else:
        dork_data, facet_data, total = cli_zoom.from_cache_or_api()
    # print data total
    if count_total:
        show.printf(total)
    else:
        # user saves data to local folder
        if save:
            cli_zoom.save(save)
            return
        # print filter
        if filters:
            cli_zoom.cli_filter(filters)
            return
        # when facets is not None print facets data
        if facet:
            show.print_facets(facet, facet_data, total, figure)
            return
        if stat:
            cli_zoom.statistics(stat, figure)
            return
        # when facets is None print dork data
        if filters is None and facet is None and stat is None:
            show.print_data(dork_data)
            return
        # others
        show.printf("please run <zoomeye dork -h> for help.")


def info(args):
    """
    used to print the current identity of the user and the remaining data quota for the month
    :param args:
    :return:
    """
    api_key, access_token = file.get_auth_key()
    zm = ZoomEye(api_key=api_key, access_token=access_token)
    # get user information
    user_data = zm.resources_info()
    if user_data:
        # show in the terminal
        show.printf("Role: {}".format(user_data["plan"]))
        show.printf("Quota: {}".format(user_data["resources"].get("search")))


def ip_history(args):
    """
    query device history
    please see: https://www.zoomeye.org/doc#history-ip-search
    :param args:
    :return:
    """
    ip = args.ip
    filters = args.filter
    force = args.force
    # determine whether the input is an IP address by regular
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
                             '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    # IP format error，exit program
    if not compile_ip.match(ip):
        show.printf("[{}] it is not an IP address, please check!".format(ip), color='red')
        return

    zm = HistoryDevice(ip, force)
    # user input filter field
    if filters:
        filter_list = filters.split(',')
        zm.filter_fields(filter_list)
        return
    # no filter field,
    # print [timestamp,service,port,country,raw_data] fields
    zm.show_fields()


def clear_file(args):
    """
    clear user setting and zoomeye cache data
    """
    setting = args.setting
    cache = args.cache
    target_dir = None
    # clear user setting
    if setting:
        target_dir = zoomeye_dir
    # clear local cache file
    if cache:
        target_dir = os.path.expanduser(config.ZOOMEYE_CACHE_PATH)
    # user input error
    if target_dir is None:
        show.printf("Please run <zoomeye clear -h> for help!", color='red')
        return
    # remove all files under the folder
    file_list = os.listdir(target_dir)
    for item in file_list:
        os.remove(os.path.join(target_dir, item))
    show.printf("clear complete!", color='green')


