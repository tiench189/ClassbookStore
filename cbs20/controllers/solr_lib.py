# -*- coding: utf-8 -*-
__author__ = 'Tien'

import urllib2
import sys
import json

import string
import re

INTAB = "ạAảẢãÃàÀáÁâÂậẬầẦấẤẩẨẫẪăĂắẮằẰặẶẳẲẵẴóÓòÒọỌõÕỏỎôÔộỘổỔỗỖồỒốỐơƠờỜớỚợỢởỞỡỠ" \
        "éÉèÈẻẺẹẸẽẼêÊếẾềỀệỆểỂễỄúÚùÙụỤủỦũŨưƯựỰữỮửỬừỪứỨíÍìÌịỊỉỈĩĨýÝỳỲỷỶỵỴỹỸđĐ"
INTAB = [ch.encode('utf8') for ch in unicode(INTAB, 'utf8')]

OUTTAB = "a"*34 + "o"*34 + "e"*22 + "u"*22 + "i"*10 + "y"*10 + "d"*2

r = re.compile("|".join(INTAB))
replaces_dict = dict(zip(INTAB, OUTTAB))

def khongdau(utf8_str):
    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def search_advance():

    try:
        category_type = None
        page = 0
        items_per_page = 18
        #Pagination
        try:
            if len(request.args) > 0: page = int(request.args[0])
            if len(request.args) > 1: items_per_page = int(request.args[1])
        except (TypeError, ValueError):
            pass
        limitby = (page * items_per_page, (page + 1) * items_per_page)

        creator_name = request.vars["creator_name"]
        category_id = request.vars["category_id"]
        class_id = request.vars["class_id"]
        subject_id = request.vars["subject_id"]
        store_search = request.vars["store_search"]
        try:
            store_search = khongdau(store_search).replace(" ", "+")
        except Exception as err:
            print(err)
        version = ""
        if 'version' in request.vars:
            version = request.vars.version

        if 'creator_name' not in request.vars:
            return search_multiple(store_search, category_id, subject_id, class_id, page, items_per_page, limitby,
                                   category_type, version)
    except Exception as e:
        return dict(error=str(e) + " on line " + str(sys.exc_traceback.tb_lineno))



def search_multiple(store_search, category_id, subject_id, class_id, page, items_per_page, limitby, category_type, version=""):
    try:
        if store_search is None:
            store_search = "*"
        url_search = "http://localhost/cbs20/solr_lib/search.json?key=" + store_search + "&row=" + str(items_per_page) + "&start=" + str(items_per_page*page)
        #print(url_search)
        if category_id is not None:
            url_search += "&category_id=" + category_id
        if subject_id is not None:
            url_search += "&subject_id=" + subject_id
        if class_id is not None:
            url_search += "&class_id=" + class_id
        get_data = urllib2.urlopen(url_search)
        str_json = str(get_data.read())
        get_data = json.loads(str_json)
        total_items = int(get_data['numFound'])
        total_pages = int(total_items / items_per_page) + 1
        products = list()
        for p in get_data['docs']:
            temp = dict()
            temp['id'] = p['id']
            temp['co_author'] = p['product_creator']
            temp['cover_price'] = p['cover_price']

            temp['category_id'] = 0
            temp['category_name'] = ""
            temp['category_code'] = ""
            temp['category_type'] = "Book"
            temp['creator_name'] = p['product_creator']
            temp['publisher_name'] = ""
            temp['product_title'] = p['product_title']
            temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                        scheme=True, host=True, args=p['product_code'])
            temp['product_code'] = p['product_code']
            temp['product_price'] = p['product_price']

            temp['subject_name'] = ''

            temp['class_name'] = ''
            products.append(temp)
        return dict(page=page, total_items=str(total_items), total_pages=str(total_pages),
                    items_per_page=items_per_page, products=products)
    except Exception as e:
        print(str(e) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(e) + " on line " + str(sys.exc_traceback.tb_lineno) + " " + url_search)


def search():
    try:
        key_word = request.vars.key
        key_word = key_word.replace(" ", "+")
        key_word = key_word.replace("&", "")
        key_word = khongdau(key_word)
        if key_word == "":
            key_word = "*:*"
        start = 0
        row = 5
        if "start" in request.vars:
            start = request.vars.start
        if "row" in request.vars:
            row = request.vars.row
        url_search = "http://192.168.95.229:8189/solr/cblib/select?q=" + key_word + \
                    "&start=" + str(start) + "&rows=" + str(row) +\
                     "&wt=json&indent=true&defType=edismax" \
                     "&qf=product_title%5E5+product_description+product_creator&mm=3%3C75%25" \
                     "&fl=id,product_title,product_creator," +\
                    "product_code,product_price,cover_price"
        if 'category_id' in request.vars:
            url_search += "&fq=product_category%3A" + request.vars.category_id
        if 'subject_id' in request.vars:
            url_search += "&fq=product_subject%3A" + request.vars.subject_id
        if 'class_id' in request.vars:
            url_search += "&fq=product_class%3A" + request.vars.class_id
        get_data = urllib2.urlopen(url_search)
        str_json = str(get_data.read())
        get_data = json.loads(str_json)
        return get_data['response']
    except Exception as e:
            return str(e) + " on line " + str(sys.exc_traceback.tb_lineno)
