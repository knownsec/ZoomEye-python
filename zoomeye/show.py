"""
* Filename: show.py
* Description: used to print different data on the terminal.
* Time: 2020.11.30
* Author: liuf5
*/
"""
from colorama import init

from zoomeye import config, data

# solve the color display error under windows terminal
init(autoreset=True)


facets_filed_table = {
    'app':      'product',
    'device':   'device',
    'service':  'service',
    'os':       'os',
    'port':     'port',
    'country':  'country',
    'city':     'city'
}


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
        '\t': '\\t'
    }
    for c in s:
        if ord(c) in range(32, 127):
            res.append(c)
        elif c in d.keys():
            res.append(d[c])
        else:
            res.append('\\x%.2x' % ord(c))
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


def printf(s, color="white"):
    """
    print result in terminal
    :param s: str, printed string
    :param color: str, printed string color
    :return:
    """
    colors = {
        "red":      '\033[31m',         # red
        "green":    '\033[32m',         # green
        "yellow":   '\033[33m',         # yellow
        "blue":     '\033[34m',         # blue
        "white":    '\033[37m',         # white
    }

    # default color
    default = '\033[0m'  # item default color
    print('{}{}{}'.format(colors.get(color, "WHITE"), s, default))


def print_data(data_list):
    """
    display the dork data searched by the user on the terminal,
    if facet is specified, it will also be displayed
    :param data_list: dork data , list
    :param facet_data: facet data, list
    :return:
    """
    total = 0
    # print title
    printf("{:<25}{:<20}{:<20}{:<30}{:<30}".format(
        "ip:port", "service", "country", "app", "banner"), color="green")

    # process data
    for d in data_list:
        ip, country, port, app, banner, service = data.get_item(d)
        # content length too long, truncated
        app_name = omit_str(app, 5)

        # str --> hex
        banner_content = omit_str(convert_str(omit_str(banner)))

        # print result
        total += 1
        printf('{:<25}{:<20}{:<20}{:<30}{:30}'.format(
            "{}:{}".format(ip, port), service, country, app_name,
            banner_content)
        )
    print()
    printf("total: {}".format(total))


def print_filter(keys, data):
    """
    used to display user filtered data on the terminal
    :param keys: user input key, is str
    :param data: filter data ,is list
    :return:
    """
    total = 0
    # print title
    title = ""
    for key in keys.split(","):
        title += "{:<30}".format(key)
    printf("{}".format(title), color="green")

    # print data
    for i in data:
        items = ""
        for j in i:
            j_hex = convert_str(str(j))
            items += "{:<30}".format(j_hex)
        total += 1
        printf(items)
    print()
    printf("total: {}".format(total))


def print_facets(facets, facet_data):
    """
    used to print data that users need to count
    :param facets: str, statistical data
    :param facet_data:list, all facets data
    {"app": [{"name": 'xx', 'count': xxx}{"name": 'xx', 'count': xxx}{"name": 'xx', 'count': xxx}]}
    :return:
    """
    # print facet data
    if facet_data:
        for facet in facets.split(","):
            if facets_filed_table.get(facet.strip()) is None:
                support_fields = ','.join(list(facets_filed_table.keys()))
                printf("facet command has unsupport fields [{}], support fields has [{}]".format(facet.strip(), support_fields),
                       color='red')
                exit(0)
            printf("{:<35}{:<20}".format(facet, "count"), color="green")
            f = facets_filed_table.get(facet)
            for d in facet_data.get(f):
                name = d.get("name")
                if len(str(name)) == 0:
                    name = "[unknown]"
                printf("{:<35}{:<20}".format(name, d.get("count")))
    else:
        pass


def print_stat(keys, stat_data):
    """
    print current data aggregation
    :param keys:
    :param stat_data: {'app': {'Gunicorn': 2, 'nginx': 14, 'Apache httpd': 9, '[unknown]': 3, 'Tornado httpd': 2}, 'port': {443: 29, 8443: 1}}
    :return:
    """
    if not stat_data:
        return

    for key in keys.split(','):
        # print title
        printf("{:<35}{:<20}".format(key, "count"), color="green")

        # sort by the amount of each data
        item = stat_data.get(key)
        sorted_item = sorted(item.items(), key=lambda x: x[1], reverse=True)

        # print result
        for name, count in sorted_item:
            printf("{:<35}{:<20}".format(name, count))
