# -*- coding: utf-8 -*-
__author__ = 'tanbm'
from datetime import datetime


def addzero(num):
    if num < 10:
        return "0" + str(num)
    else:
        return str(num)


def user_get_id_cp(member_id, db):
    info = user_get_info(member_id, db)
    try:
        return info['user_cp_info']['cp_id']
    except:
        return info['user_info']['id']


def user_get_info(member_id, db):
    data_user = db(db.auth_user.id == member_id).select()
    if len(data_user) <= 0:
        return "Không tìm thấy thông tin"
    data_user = data_user[0]
    info = dict()
    info['user_info'] = dict(id=data_user.id, first_name=data_user.first_name, last_name=data_user.last_name,
                             email=data_user.email, user_name=data_user.username)
    try:
        user_cp = db(db.auth_user.id == data_user.created_by).select()[0]
        info['user_cp_info'] = dict(cp_id=user_cp.id, cp_first_name=user_cp.first_name, cp_last_name=user_cp.last_name,
                                    cp_email=user_cp.email, cp_user_name=user_cp.username)
        info['user_info']['is_admin'] = False
    except:
        info['user_cp_info'] = "Không có thông tin"
        info['user_info']['is_admin'] = True
    return info


def user_gen_product_code(user_cp, cp_type):
    now = datetime.now()
    token = addzero(now.year) + addzero(now.month) + addzero(now.day) + addzero(now.hour) + addzero(
        now.minute) + addzero(now.second)
    code = user_cp + cp_type[:3] + token
    return code


def get_discount_value(cp_id, db):
    cp_id = user_get_id_cp(cp_id, db)
    value_discount = db(db.clsb20_discount_cp.user_id == cp_id).select()
    if len(value_discount) > 0:
        return value_discount.first()['value_discount']
    else:
        value_discount = db.clsb20_discount_cp.insert(user_id=cp_id)
        return value_discount['value_discount']