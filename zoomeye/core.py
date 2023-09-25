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
from zoomeye.data import CliZoomEye, HistoryDevice, IPInformation, DomainSearch

# save zoomeye config folder
zoomeye_dir = os.path.expanduser(config.ZOOMEYE_CONFIG_PATH)


def init_key(key): #初始化API密钥并将其保存在本地配置文件中

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
    with open(key_file, 'w') as f:
        f.write(key)
    show.printf("successfully initialized", color="green")
    # change the permission of the configuration file to read-only
    os.chmod(key_file, 0o600)


def init(args):#根据用户输入的参数来选择初始化方法，可以通过API密钥来进行初始化
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
    show.printf("input parameter error!", color="red")
    show.printf("please run <zoomeye init -h> for help.", color="red")


def search(args):#进行搜索操作，根据用户输入的搜索条件进行搜索
    dork = args.dork
    num = int(args.num)
    facet = args.facet
    filters = args.filter
    stat = args.stat
    save = args.save
    count_total = args.count
    figure = args.figure
    force = args.force
    resource = args.type

    cli_zoom = CliZoomEye(dork, num, resource=resource, facet=facet, force=force)
    if filters:
        cli_zoom.filter_data(filters, save)
        return
    if facet:
        cli_zoom.facets_data(facet, figure)
        return
    if count_total:
        cli_zoom.count()
        return
    if stat:
        cli_zoom.statistics(stat, figure)
        return
    if save:
        cli_zoom.save(save)
        return
    if filters is None and facet is None and stat is None:
        cli_zoom.default_show()
        return
    show.printf("please run <zoomeye search -h> for help.")


def info(args):#打印当前用户的身份和本月剩余的数据配额
    """
    used to print the current identity of the user and the remaining data quota for the month
    :param args:
    :return:
    """
    api_key = file.get_auth_key()
    zm = ZoomEye(api_key=api_key)
    # get user information
    user_data = zm.resources_info()
    if user_data:
        # show in the terminal
        show.printf("Role: {}".format(user_data["plan"]))
        show.printf("Quota: {}".format(user_data["resources"].get("search")))
        show.printf("user_info: {}".format(user_data["user_info"]))
        show.printf("quota_info: {}".format(user_data["quota_info"]))


def ip_history(args):#查询设备的历史信息
    """
    query device history
    please see: https://www.zoomeye.org/doc#history-ip-search
    :param args:
    :return:
    """
    ip = args.ip
    filters = args.filter
    force = args.force
    number = args.num
    # determine whether the input is an IP address by regular
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
                             '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    # IP format error，exit program
    if not compile_ip.match(ip):
        show.printf("[{}] it is not an IP address, please check!".format(ip), color='red')
        return

    zm = HistoryDevice(ip, force, number)
    # user input filter field
    if filters:
        filter_list = filters.split(',')
        zm.filter_fields(filter_list)
        return
    # no filter field,
    # print [timestamp,service,port,country,raw_data] fields
    zm.show_fields()


def clear_file(args):#清除用户设置和ZoomEye缓存数据
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


def information_ip(args):#获取特定IP的信息
    ip = args.ip
    filters = args.filter
    # determine whether the input is an IP address by regular
    compile_ip = re.compile('^(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|[1-9])\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.'
                            '(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.(1\d{2}|2[0-4]\d|25[0-5]|[1-9]\d|\d)$')
    # IP format error，exit program
    if not compile_ip.match(ip):
        show.printf("[{}] it is not an IP address, please check!".format(ip), color='red')
        return

    infor = IPInformation(ip)
    if filters:
        filter_list = filters.split(',')
        infor.filter_information(filter_list)
        return

    infor.show_information()


def associated_domain_query(args):#关联域名查询
    q = args.q
    resource = args.type
    page = args.page
    dot = args.dot
    if dot:
        # generate network map
        DomainSearch(q, resource, page).generate_dot()
    else:
        # show information for user
        DomainSearch(q, resource, page).show_information()
    return None

