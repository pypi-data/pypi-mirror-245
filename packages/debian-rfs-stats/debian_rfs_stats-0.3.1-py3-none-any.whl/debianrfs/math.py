#!/usr/bin/env python3
# debian-rfs-stats - Calculate statistics regarding sponsorship requests.
# Copyright (c) 2023 Maytham Alsudany <maytha8thedev@gmail.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.


def average(list: list[int]) -> float:
    """Calculate average of integers in list"""
    return sum(list) / len(list)


def median(orig_list: list[int]) -> float:
    """Calculate median of integers in list"""
    list = orig_list
    list.sort()
    median_pos = (len(list) + 1) / 2
    if median_pos % 1 == 0:
        return list[int(median_pos - 1)]
    else:
        return (list[int(median_pos - 0.5 - 1)] + list[int(median_pos + 0.5 - 1)]) / 2


def lower_quartile(orig_list: list[int]) -> float:
    """Calculate lower quartile of integers in list"""
    list = orig_list
    list.sort()
    if len(list) % 2 == 0:
        lower = list[: int(len(list) / 2 - 1 - 1)]
        return median(lower)
    else:
        lower = list[: int((len(list) + 1) / 2 - 1)]
        return median(lower)


def upper_quartile(orig_list: list[int]) -> float:
    """Calculate upper quartile of integers in list"""
    list = orig_list
    list.sort()
    if len(list) % 2 == 0:
        upper = list[int(len(list) / 2 + 1 - 1) :]
        return median(upper)
    else:
        upper = list[int((len(list) - 1) / 2 - 1) :]
        return median(upper)


def interquartile_range(orig_list: list[int]) -> float:
    return upper_quartile(orig_list) - lower_quartile(orig_list)


def lower_fence(orig_list: list[int]) -> float:
    return lower_quartile(orig_list) - interquartile_range(orig_list) * 1.5


def upper_fence(orig_list: list[int]) -> float:
    return upper_quartile(orig_list) + interquartile_range(orig_list) * 1.5


def filter_outliers(orig_list: list[int]):
    u_fence = upper_fence(orig_list)
    l_fence = lower_fence(orig_list)

    def filter_outfliers_fn(item: int) -> bool:
        return item <= u_fence and item >= l_fence

    return filter_outfliers_fn
