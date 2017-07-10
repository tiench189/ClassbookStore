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

def resize_thumb(path_in, path_out):
    try:
        import os
        import PIL
        from PIL import Image
        basewidth = 160
        thumb = Image.open(path_in)
        wper = (basewidth / float(thumb.size[0]))
        hsize = int(float(thumb.size[1]) * float(wper))
        new_thumb = thumb.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        new_thumb.save(path_out)
    except Exception as err:
        print str(err)
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))