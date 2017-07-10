# -*- coding: utf-8 -*-
__author__ = 'tanbm'

import hashlib


def computeMD5hash(string):
    m = hashlib.md5()
    m.update(string.encode('utf-8'))
    return m.hexdigest()


def select_list(list=None, name=None, valueof=None, selected=None):
    item = []
    for i in list:
        node = {'value': 0, 'selected': False, 'name': ''}
        node['value'] = i[valueof]
        if i[valueof] == selected:
            node['selected'] = True
        node['name'] = i[name]
        item.append(node)
    return item;


def style_money(num):
    num = str(num)
    money = ""
    k = 0
    i = len(num)-1
    while i >= 0:
        k += 1
        if (k == 3) & (i != 0):
            money = "." + num[i] + money
            k = 0
        else:
            money = num[i] + money
        i -= 1
    return money