# -*- coding: utf-8 -*-
__author__ = 'tanbm'

import sys

def index():
    return dict()

def check_user_regis_device():
    try:
        device_serial = request.args[0]
        user_token = request.args[1]
        user = db(db.clsb_user.user_token == user_token).select()
        if len(user) == 0:
            return dict(result=False, code="INVALID_TOKEN", mess="Hết phiên đăng nhập")
        user = user.first()
        check_device = db(db.clsb_device.device_serial == device_serial)\
                (db.clsb_device.user_id == db.clsb_user.id).select()
        if len(check_device) == 0:
            return dict(result=False, code="DEVICE_NOT_YET", mess="Thiết bị chưa đăng kí")
        device_info = check_device.first()
        if device_info[db.clsb_user.id] == user['id']:
            return dict(result=True)
        else:
            return dict(result=False, code="DEVICE_REGISTED", mess="Thiết bị đã được đăng kí bởi tài khoản khác")
    except Exception as err:
        return dict(result=False, code="UNKNOWN", mess=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

