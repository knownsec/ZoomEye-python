"""
* Filename: core.py
* Description: cli core function, processing various requests
* Time: 2020.11.30
* Author: wh0am1i
*/
"""
import re
import os
import time
import json
from zoomeye import config, file, show
from zoomeye.tools import Cache
from zoomeye.sdk import ZoomEye

# save zoomeye config folder
zoomeye_dir = os.path.expanduser(config.ZOOMEYE_CONFIG_PATH)


def init_key(key):

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
    user_data = zoom.userinfo()
    if user_data.get("code") == 60000:
        show.printf("Username: {}".format(user_data.get('data', {}).get('username', {})))
        show.printf("Role: {}".format(user_data.get('data', {}).get('subscription', {}).get('plan', '')))
        show.printf("Points: {}".format(user_data.get('data', {}).get('subscription', {}).get("points", 0)))
        show.printf("Zoomeye Points: {}".format(user_data.get('data', {}).get('subscription', {}).
                                                get("zoomeye_points", 0)))
    # save api key
    with open(key_file, 'w') as f:
        f.write(key)
    show.printf("successfully initialized", color="green")
    # change the permission of the configuration file to read-only
    os.chmod(key_file, 0o600)


def init(args):
    """
    the initialization processing function will select the initialization method according to the user's input.
    :param args:
    :return:
    """
    api_key = args.apikey
    # use api key init
    if api_key:
        init_key(api_key)
        return
    # invalid parameter
    show.printf("input parameter error", color="red")
    show.printf("please run <zoomeye init -h> for help.", color="red")


def search(args):
    dork = args.dork
    page = int(args.page)
    pagesize = int(args.pagesize)
    facets = args.facets
    fields = args.fields
    sub_type = args.sub_type
    figure = args.figure
    save = args.save
    force = args.force

    api_key = file.get_auth_key()
    zm = ZoomEye(api_key=api_key)
    cahce = Cache(dork, page=page, pagesize=pagesize, facets=facets, fields=fields, sub_type=sub_type)
    if cahce.check() and force is False:
        data = cahce.load()
    else:
        data = zm.search(dork, page=page, pagesize=pagesize, facets=facets, fields=fields, sub_type=sub_type)
        cahce.save(data)

    data_list = data.get('data', [])
    facets_data = data.get('facets', {})
    total = data.get('total', {})

    if len(data_list) > 0:
        keys = data_list[0].keys()
        show.print_filter(",".join(keys), [[i.get(key) for key in keys] for i in data_list], total)
        # save file to local file, json fire
        if save:
            name = re.findall(r"[a-zA-Z0-9_\u4e00-\u9fa5]+", dork)
            re_name = '_'.join(name)
            filename = "{}_{}_{}.json".format(re_name, pagesize, int(time.time()))
            with open(filename, 'w') as f:
                f.write(json.dumps(data_list))
            show.printf("save file to {}/{} successful!".format(os.getcwd(), filename), color='green')

    if facets_data:
        show.print_facets(facets, facets_data, total, figure, {
            'type': 'type',
            'product': 'product',
            'device': 'device',
            'service': 'service',
            'os': 'os',
            'port': 'port',
            'subdivisions': 'subdivisions',
            'country': 'country',
            'city': 'city',
        })

    # show.printf("please run <zoomeye search -h> for help.")


def info(args):
    """
    used to print the current identity of the user and the remaining data quota for the month
    :return:
    """
    api_key = file.get_auth_key()
    zm = ZoomEye(api_key=api_key)
    # get user information
    user_response = zm.userinfo()

    if user_response and user_response.get('code') == 60000:
        user_data = user_response.get('data')
        # show in the terminal
        show.printf("username: {}".format(user_data["username"]))
        show.printf("email: {}".format(user_data["email"]))
        show.printf("phone: {}".format(user_data["phone"]))
        show.printf("created_at: {}".format(user_data["created_at"]))
        show.printf("Subscription:: {}".format(user_data["subscription"]))


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
