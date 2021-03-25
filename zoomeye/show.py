"""
* Filename: show.py
* Description: used to print different data on the terminal.
* Time: 2020.11.30
* Author: liuf5
*/
"""
import re
from colorama import init

from zoomeye import config, data, plotlib

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
        if ord(c) > 0xff or ord(c) in range(32, 127):
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
        "red":      '\033[31m',  # red
        "green":    '\033[32m',  # green
        "yellow":   '\033[33m',  # yellow
        "blue":     '\033[34m',  # blue
        "white":    '\033[37m',  # white
    }

    # default color
    default = '\033[0m'  # item default color
    print('{}{}{}'.format(colors.get(color, "WHITE"), s, default))


def print_data(data_list):
    """
    display the dork data searched by the user on the terminal,
    if facet is specified, it will also be displayed
    :param data_list: dork data , list
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


def print_filter(keys, data_list, condition=None):
    """
    used to display user filtered data on the terminal
    :param keys: user input key, is str
    :param data_list: filter data ,is list
    :param condition: list,
    :return:
    """
    total = 0
    # print title
    title = ""
    for key in keys.split(","):
        title += "{:<30}".format(key)
    printf("{}".format(title), color="green")

    # print data
    for i in data_list:
        items = ""
        for j in i:
            j_hex = convert_str(str(j))
            # match to content highlight
            if condition:
                for item in condition:
                    k, v = item.split('=')
                    result_re = re.search(v, j_hex, re.I | re.M)
                    if result_re:
                        # replace to highlight
                        color_content = "\033[31m{}\033[0m".format(result_re.group())
                        j_hex = j_hex.replace(result_re.group(), color_content)
            items += "{:<30}".format(j_hex)
        total += 1
        printf(items)
    print()
    printf("total: {}".format(total))


def print_facets(facets, facet_data, total, figure):
    """
    used to print data that users need to count
    :param facets: str, statistical data
    :param facet_data:list, all facets data
    :param total:int, data total
    :param figure:int, data total
    {"app": [{"name": 'xx', 'count': xxx}{"name": 'xx', 'count': xxx}{"name": 'xx', 'count': xxx}]}
    :return:
    """
    if not facet_data:
        return
    # print facet data

    print(' ' + '-' * 40)
    printf(" ZoomEye total data:{}".format(total))
    for facet in facets.split(","):
        names = []
        counts = []
        pie_info = []
        facet_total = {}
        facet_count = 0
        print(' {:-^40}'.format(facet + " Top 10"))
        if facets_filed_table.get(facet.strip()) is None:
            support_fields = ','.join(list(facets_filed_table.keys()))
            printf("facet command has unsupport fields [{}], support fields has [{}]".format(facet.strip(),
                                                                                             support_fields),
                   color='red')
            exit(0)
        if figure is None:
            printf(" {:<35}{:<20}".format(facet, "count"), color="green")
        f = facets_filed_table.get(facet)
        for t in facet_data.get(f):
            facet_count += t.get('count')
        facet_total[facet] = facet_count

        for d in facet_data.get(f):
            name = d.get("name")
            if len(str(name)) == 0:
                name = "[unknown]"

            count = d.get("count")
            # get histogram data
            names.append(name)
            counts.append(count)
            # get pie chart data
            # three decimal places
            pie = (name, round(count / facet_total.get(facet), 3))
            pie_info.append(pie)
            if figure is None:
                printf(" {:<35}{:<20}".format(name, count))
        # pie chart
        if figure and figure == 'pie':
            plotlib.show_pie_chart(pie_info)
        # histogram
        if figure and figure == 'hist':
            plotlib.generate_histogram(counts, names, force_ascii=True)


def print_stat(keys, stat_data, num, figure):
    """
    print current data aggregation
    :param keys: str, field
    :param figure: str, pie or hist
    :param num: int, local total data
    :param stat_data: {'app': {'Gunicorn': 2, 'nginx': 14, 'Apache httpd': 9, '[unknown]': 3, 'Tornado httpd': 2}, 'port': {443: 29, 8443: 1}}
    :return:
    """
    if not stat_data:
        return
    print(' ' + '-' * 40)
    printf(" current total data:{}".format(num), color='green')
    for key in keys.split(','):
        print(' {:-^40}'.format(key + " data"))
        # print title
        if figure is None:
            printf(" {:<35}{:<20}".format(key, "count"), color="green")

        # sort by the amount of each data
        item = stat_data.get(key)
        sorted_item = sorted(item.items(), key=lambda x: x[1], reverse=True)
        # print result
        if figure is None:
            for name, count in sorted_item:
                printf(" {:<35}{:<20}".format(name, count))

        names = []
        counts = []
        pie_info = []
        for name, count in sorted_item:
            names.append(name)
            counts.append(count)
            # get pie chart data
            # three decimal places
            pie = (name, round(count / num, 3))
            pie_info.append(pie)
        # pie chart
        if figure and figure == 'pie':
            plotlib.show_pie_chart(pie_info)
        # histogram
        if figure and figure == 'hist':
            plotlib.generate_histogram(counts, names, force_ascii=True)


def print_host_data(host_data):
    """
    :param host_data, list,
    """
    # host data is None
    if len(host_data) == 0:
        return
    # parser hostname,country,city... information
    first_item = host_data[0]
    all_data, port_count = data.filter_history_data(data.fields_tables_history_host.keys(), host_data)
    printf(first_item.get('ip'))
    dict_first_item = data.ZoomEyeDict(first_item)
    # print title
    for dict_item in data.tables_history_info.keys():
        result = dict_first_item.find(data.tables_history_info.get(dict_item))
        if result == "" or result is None or result == "Unknown":
            result = "[unknown]"
        printf("{:<30}{}".format(dict_item.capitalize() + ":", result))
    printf("{:30}{}".format("Number of open ports:", len(port_count)))
    printf("{:30}{}".format("Number of historical probes:", len(host_data)))
    printf('')
    printf("{:<27}{:<27}{:<27}{:<27}".format("timestamp", "port/service", "app", "raw_data"), color='green')
    # print detail and process port/service
    for data_item in all_data:
        content = ''
        for item_item in data_item:
            if data_item.index(item_item) == 1:
                res = item_item
                continue
            if data_item.index(item_item) == 2:
                item_item = "{}/{}".format(res, item_item)
            content += "{:<27}".format(item_item)
        printf(content)


def print_filter_history(fileds, hist_data, condition=None):
    """
    print user filter history data,
    :param fileds list,user input field
    :param hist_data dict, from ZoomEye API get data
    :param condition list, filter condition
    """
    filter_title = ''
    first_item = hist_data[0]
    # filter data
    all_data, port_count = data.filter_history_data(fileds, hist_data, omit=False)
    printf(first_item.get('ip'))
    dict_first_item = data.ZoomEyeDict(first_item)
    # parser filter data title
    for dict_item in data.tables_history_info.keys():
        result = dict_first_item.find(data.tables_history_info.get(dict_item))
        if result == "" or result is None or result == "Unknown":
            result = "[unknown]"
        printf("{:<30}{}".format(dict_item.capitalize() + ":", result))
    printf("{:30}{}".format("Number of open ports:", len(port_count)))
    printf("{:30}{}".format("Number of historical probes:", len(hist_data)))
    printf('')
    # print title
    for item in fileds:
        filter_title += "{:<27}".format(item)
    printf(filter_title, color='green')
    # print data
    for data_item in all_data:
        content = ""
        for item_item in data_item:
            # match to content highlight
            if condition:
                for condition_item in condition:
                    k, v = condition_item.split('=')
                    re_result = re.search(str(v), str(item_item), re.I | re.M)
                    # replace to highlight
                    if re_result:
                        content_item = "\033[31m{}\033[0m".format(re_result.group())
                        item_item = str(item_item).replace(re_result.group(), content_item)
            content += "{:<27}".format(item_item)
        printf(content)
