# -*- coding: utf-8 -*-
__author__ = 'tanbm'

def search(): #vars: start, num_item
    if request.url.find('/view') >= 0:
        id = 0
        if request.args(1):
            id = request.args[1]
        return redirect(URL(a='cpa', c='creator', f='view', args=[id], host=True))
    str = ""
    start = int(request.vars.start)
    num = int(request.vars.num)
    if request.vars.creator_name:
        str = request.vars.creator_name

    limitby = (start, start+num)
    data = db(db.clsb20_dic_creator_cp.creator_name.like("%"+str+"%")).select(limitby=limitby)
    result = list()
    for item in data:
        temp = dict()
        temp['creator_id'] = item.id
        temp['creator_name'] = item.creator_name
        temp['creator_description'] = item.creator_name
        result.append(temp)
    return dict(creators=result)