# -*- coding: utf-8 -*-
__author__ = 'tanbm'

def search():
    str = ""
    start = int(request.vars.start)
    num = int(request.vars.num)
    limitby=(start,start+num)
    if request.vars.publisher_name:
        str = request.vars.publisher_name
    data = db(db.clsb_dic_publisher.publisher_name.like("%"+str+"%")).select(limitby=limitby)
    result = list()
    for item in data:
        temp = dict()
        temp['publisher_id'] = item.id
        temp['publisher_name'] = item.publisher_name
        temp['publisher_description'] = item.publisher_name
        result.append(temp)
    return dict(creators=result)