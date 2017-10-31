#!/usr/bin/python3
# -*- coding: UTF-8 -*-


def del_list2_in_list1(list1, list2):
    """
    从 list1 中删除与 list2相同的元素
    :param list1:
    :param list2:
    :return:
    """
    for ele in list2:
        list1.remove(ele)