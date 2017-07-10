# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys

except_id = [3, 5, 6]

def select_chuyen_de(cd_id):
    try:
        data = dict()
        select_cd = db(db.clsb30_chuyen_de.id == cd_id).select().first()
        data['id'] = cd_id
        data['code'] = select_cd['cate_code']
        data['title'] = select_cd['cate_title']
        select_child = db(db.clsb30_chuyen_de.cate_parent == cd_id)\
                (db.clsb30_chuyen_de.show_status == 1).select()
        children = list()
        for child in select_child:
            children.append(select_chuyen_de(child['id']))
        baitap = list()
        select_bt = db(db.clsb30_bt_chuyen_de.chuyen_de == cd_id)\
            (db.clsb30_bt_chuyen_de.show_status == 1).select()
        for bt in select_bt:
            temp = dict()
            temp['id'] = bt['id']
            temp['code'] = bt['exer_code']
            temp['title'] = bt['exer_title']
            baitap.append(temp)
        data['children'] = children
        data['bai_tap'] = baitap
        return data
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_all():
    try:
        chuyen_de = list()
        select_parent = db(db.clsb30_chuyen_de.cate_parent == None)\
                (db.clsb30_chuyen_de.show_status == 1).select()
        for parent in select_parent:
            chuyen_de.append(select_chuyen_de(parent['id']))
        return dict(chuyen_de=chuyen_de)
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def baitap_info():
    try:
        code = request.args[0]
        select_bt = db(db.clsb30_bt_chuyen_de.exer_code == code).select().first()
        bt = dict()
        bt['id'] = select_bt['id']
        bt['code'] = select_bt['exer_code']
        bt['title'] = select_bt['exer_title']
        return bt
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_root():
    try:
        chuyen_de = list()
        select_parent = db(db.clsb30_chuyen_de.cate_parent == None)\
                (db.clsb30_chuyen_de.show_status == 1).select()
        data = list()
        for parent in select_parent:
            temp = dict()
            data['id'] = parent['id']
            data['code'] = parent['cate_code']
            data['title'] = parent['cate_title']
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))