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

def search_test():
    try:
        return "aaaaaaaaaaa"
        key_word = request.vars.key
        key_word = key_word.replace(" ", "+")
        key_word = khongdau(key_word)
        start = 0
        row = 5
        if "start" in request.vars:
            start = request.vars.start
        if "row" in request.vars:
            row = request.vars.row
        url_search = "http://192.168.95.229:8189/solr/db/select?q=" + key_word + \
                     "&wt=json&indent=true&defType=dismax" \
                     "&fl=id,product_title"
        try:
            get_data = urllib2.urlopen(url_search)
            str_json = str(get_data.read())
            get_data = json.loads(str_json)
            return get_data['response']
        except urllib2.HTTPError, error:
            contents = error.read()
            return dict(contents=contents)
    except Exception as e:
            return str(e) + " on line " + str(sys.exc_traceback.tb_lineno)
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
        #url_search = "http://192.168.95.229:8189/solr/db/select?q=" + key_word + \
        #            "&start=" + str(start) + "&rows=" + str(row) +\
        #             "&fl=id,product_title,product_creator," +\
        #            "product_code,product_price,cover_price" +\
        #             "&wt=json&indent=false" +\
        #             "&defType=dismax&qf=product_title+product_description+product_creator&q.op=AND"
        url_search = "http://192.168.95.229:8189/solr/db/select?q=" + key_word + \
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


def search_mini():
    try:
        key_word = request.vars.key
        key_word = key_word.replace(" ", "+")
        key_word = khongdau(key_word)
        start = 0
        row = 5
        if "start" in request.vars:
            start = request.vars.start
        if "row" in request.vars:
            row = request.vars.row
        #url_search = "http://192.168.95.229:8189/solr/db/select?q=" + key_word + \
        #            "&start=" + str(start) + "&rows=" + str(row) +\
        #             "&fl=id,product_title" +\
        #             "&wt=json&indent=false" +\
        #             "&defType=dismax&qf=product_title+product_description+product_creator&q.op=AND"
        url_search = "http://192.168.95.229:8189/solr/db/select?q=" + key_word + \
                    "&start=" + str(start) + "&rows=" + str(row) +\
                     "&wt=json&indent=true&defType=edismax" \
                     "&qf=product_title%5E5+product_description+product_creator&mm=3%3C75%25" \
                     "&fl=id,product_title"
        get_data = urllib2.urlopen(url_search)
        str_json = str(get_data.read())
        get_data = json.loads(str_json)
        return get_data['response']
    except Exception as e:
            return str(e) + " on line " + str(sys.exc_traceback.tb_lineno)


def search_from_app():
    try:
        key_word = request.vars.key
        key_word = key_word.replace(" ", "+")
        key_word = khongdau(key_word)
        start = 0
        row = 5
        if "start" in request.vars:
            start = request.vars.start
        if "row" in request.vars:
            row = request.vars.row
        url_search = "http://192.168.95.229/cbs20/solr/search.json?key=" + key_word + "&row=" + str(row) + "&start=" + str(start)
        #url_search = "http://192.168.95.229:8001/cbs20/solr/search.json?key=" + key_word + "&row=" + str(row) + "&start=" + str(start)
        if 'category_id' in request.vars:
            url_search += "&category_id=" + request.vars.category_id
        if 'subject_id' in request.vars:
            url_search += "&subject_id=" + request.vars.subject_id
        if 'class_id' in request.vars:
            url_search += "&class_id=" + request.vars.class_id
        get_data = urllib2.urlopen(url_search)
        str_json = str(get_data.read())
        get_data = json.loads(str_json)
        return get_data
    except Exception as e:
            return str(e) + " on line " + str(sys.exc_traceback.tb_lineno)


def search_from_app_mini():
    try:
        key_word = request.vars.key
        key_word = key_word.replace(" ", "+")
        key_word = khongdau(key_word)
        start = 0
        row = 5
        if "start" in request.vars:
            start = request.vars.start
        if "row" in request.vars:
            row = request.vars.row
        url_search = "http://192.168.95.229/cbs20/solr/search_mini.json?key=" + key_word + "&row=" + str(row) + "&start=" + str(start)
        #url_search = "http://192.168.95.229:8001/cbs20/solr/search.json?key=" + key_word + "&row=" + str(row) + "&start=" + str(start)
        get_data = urllib2.urlopen(url_search)
        str_json = str(get_data.read())
        get_data = json.loads(str_json)
        return get_data
    except Exception as e:
            return str(e) + " on line " + str(sys.exc_traceback.tb_lineno)