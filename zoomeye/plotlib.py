#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""
* Filename: plotlib.py
* Description: display the statistical graph on the terminal,
    refer to:https://github.com/nschloe/termplotlib
* Time: 2021.02.03
* Author: liuf5
*/
"""
import sys
import math


from zoomeye import config


def char_by_atan(stat, at, color):
    """
    :param stat: list, all data and label
    :param at: float, percentage
    :param color: list, color
    """
    at = round(at, 5)
    if not stat:
        return config.BLANK
    if at <= stat[0][1]:
        return color[0] + config.CHARACTER + config.COLOR_RESET
    return char_by_atan(stat[1:], at - stat[0][1], color[1:])


def show_pie_chart(stat):
    """
    print pie chart in terminal
    :param stat: list, all data and label
    """

    if len(stat) > len(config.COLOR_TABLE):
        raise ("max support 10 items")

    diameter = range(-config.RADIUS, config.RADIUS)
    count = 0
    # row
    for y in diameter:
        ch = ""
        # column
        for x in diameter:
            if x * x + y * y < config.RADIUS * config.RADIUS:
                # math.atan2 => calculate arctangent value
                # /math.pi/2 => calculate the ratio of the value to the circle angle
                # +0.5  => convert to a positive number
                at = math.atan2(y, x) / math.pi / 2 + 0.5
                ch = ch + char_by_atan(stat, at, config.COLOR_TABLE)
            else:
                ch = ch + config.BLANK

        if count < len(stat):
            text = config.COLOR_TABLE[count] + "%-6s: %.2f%%" % (stat[count][0],
                                                        stat[count][1] * 100) + config.COLOR_RESET
            print(ch + "\t" * 2 + text)
        else:
            print(ch)
        count += 1


def unicode_output():
    """
    unicode standard output
    """
    return hasattr(sys.stdout, "encoding") and sys.stdout.encoding.lower() in (
        "utf-8",
        "utf8",
    )


def trim_zeros(lst):
    """

    """
    k = 0
    for item in lst[::-1]:
        if item != 0:
            break
        k += 1
    return lst[:-k] if k > 0 else lst


def get_matrix(counts, max_size, bar_width):
    """
    get the length of the histogram corresponding to each data
    :param counts: list, all data
    :param max_size: int, the max length
    :param bar_width: int, width
    """
    max_count = max(counts)

    # translate to eighths of a textbox
    eighths = [int(round(count / max_count * max_size * 8)) for count in counts]

    # prepare matrix
    matrix = [[0] * max_size for _ in range(len(eighths))]
    for i, eighth in enumerate(eighths):
        num_full_blocks = eighth // 8
        remainder = eighth % 8
        for j in range(num_full_blocks):
            matrix[i][j] = 8
        if remainder > 0:
            matrix[i][num_full_blocks] = remainder

    # Account for bar width
    out = []
    for i in range(len(matrix)):
        for _ in range(bar_width):
            out.append(matrix[i])
    return out


def generate_histogram(values, labels=None, force_ascii=False):
    """
    print histogram in terminal
    take the largest data as the standard, that is, the largest data is the longest
    :param vaules: list, all data
    :param labels: list, data label
    :param force_ascii: bool, unicode or ascii output
    return :None
    """
    # max length and bar width
    matrix = get_matrix(values, 36, 1)

    if unicode_output() and not force_ascii:
        chars = [" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉", "█"]
    else:
        chars = [" ", "#", "#", "#", "#", "#", "#", "#", "#"]

    fmt = []
    if labels is not None:
        cfmt = "{{:{}s}}".format(max([len(str(label)) for label in labels]))
        fmt.append(cfmt)
    # show values
    all_int = all(val == int(val) for val in values)
    if all_int:
        cfmt = "{{:{}d}}".format(max([len(str(val)) for val in values]))
    else:
        cfmt = "{}"
    fmt.append("[" + cfmt + "]")

    fmt.append("{}")
    fmt = "  ".join(fmt)

    out = []
    for k, (val, row) in enumerate(zip(values, matrix)):
        data = []
        if labels is not None:
            data.append(str(labels[k]))
        data.append(val)

        # cut off trailing zeros
        r = trim_zeros(row)
        data.append("".join(chars[item] for item in r))
        out.append(fmt.format(*data))
    for item in out:
        print(' ' + item)








