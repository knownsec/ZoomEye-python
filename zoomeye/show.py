"""
* Filename: show.py
* Description: used to print different data on the terminal.
* Time: 2020.11.30
* Author: wh0am1i
*/
"""
import re
import operator
from colorama import init
from zoomeye import config, tools, plotlib
from zoomeye.sdk import ZoomEyeDict
import json

# solve the color display error under windows terminal
init(autoreset=True)


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
    Default = '\033[0m'  # item default color
    print('{}{}{}'.format(colors.get(color, "WHITE"), s, Default))


def print_filter(keys, data_list, data_total, condition=None):
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
            if len(str(j)) != 0 and isinstance(j, list):
                if len(j) == 0:
                    j = '[unknown]'
                elif isinstance(j[0], str):
                    j = j[0]
                elif isinstance(j[0], dict):
                    j = j[0].get('name', '[unknown]')
                else:
                    j = j
            elif isinstance(j, dict):
                j = j.get('name', '[unknown]')
            else:
                if len(str(j)) == 0:
                    j = '[unknown]'
            j_hex = tools.convert_str(str(j))
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
    printf("\ntotal: {}/{}".format(total, data_total))


def print_facets(facets, facet_data: dict, total, figure, table):
    """
    used to print data that users need to count
    :param facets: str, statistical data
    :param facet_data: dict, all facets data
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

        if table.get(facet.strip()) is None:
            support_fields = ','.join(list(table.keys()))
            printf("facet command has unsupport fields [{}], support fields has [{}]".format(facet.strip(),
                                                                                             support_fields),
                   color='red')
            exit(0)
        print(' {:-^40}'.format(facet + " Top 10"))
        if figure is None:
            printf(" {:<35}{:<20}".format(facet, "count"), color="green")
        f = table.get(facet)
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




