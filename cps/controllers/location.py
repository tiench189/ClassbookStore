# -*- coding: utf-8 -*-
__author__ = 'tanbm'


def get_district():
    try:
        id = int(request.vars.id)
        list = db(db.clsb_district.province_id == id).select().as_dict()
    except Exception as e:
        list = db(db.clsb_district).select().as_dict()
    return dict(districts=list)