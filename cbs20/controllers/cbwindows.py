# coding: utf8
# try something like

#@author: vuongtm
import sys
from contrib.pbkdf2 import *
from datetime import *
import string
import random
import os
import re
import fs.path
import json
#cbMsg.CB_0000
SUCCESS = CB_0000
#cbMsg.CB_0005
EXISTENT = CB_0005
#cbMsg.CB_0002
LACK_ARGS = CB_0002
#cbMsg.CB_0006
FAILURE = CB_0006
#cbMsg.CB_0003
DB_RQ_FAILD = CB_0003
#cbMsg.CB_0007
DATA_ERROR = CB_0007
PWD_ERR = CB_0008
DISABLE = CB_0009
NOT_EXIST = CB_0001
USER_NAME_NOT_EXIST = CB_0010
INVALID_DEVICE_SERIAL = CB_0016
P_2_D_KEY = 'c-p3d*b'
CB_0027 = "CB-0027: License không hợp lệ"


def register_trial():

    if len(request.vars) < 4:
        return dict(error=CB_0002)

    lic_key = request.vars['license_key']
    dev_uuid = request.vars['device_serial']
    vuser_name = request.vars['user_name']
    vcompany = request.vars['company']

    license_available = db(db.cbapp_windows_activated_key.license_key == lic_key)\
        .select(db.cbapp_windows_activated_key.license_key).as_list()

    #CB_0027 ="CB-0027: License không hợp lệ, da dang ky roi"
    if len(license_available) > 0:

        return dict(error=CB_0027)

    else:

        db.cbapp_windows_activated_key.insert(license_key=lic_key, device_serial=dev_uuid, user_name=vuser_name,
                                              company=vcompany)
        return dict(message=CB_0000)


def register():

    try:
            if len(request.vars) < 4:
                return dict(error=CB_0002)

            lic_key = request.vars['license_key']
            dev_uuid = request.vars['device_serial']
            vuser_name = request.vars['user_name']
            vcompany = request.vars['company']

            license_available = db(db.cbapp_windows_key_available.license_key == lic_key)\
                .select(db.cbapp_windows_key_available.license_key).as_list()

            #CB_0027 ="CB-0027: License không hợp lệ"
            if len(license_available) == 0:
                return dict(error=CB_0027)

            #===========================Thuc hien dang ky license=======================================================

            #Kiem tra da dang ky chua
            lic = db(db.cbapp_windows_activated_key.device_serial == dev_uuid)\
                .select(db.cbapp_windows_activated_key.license_key)

            #chua dang ky
            if len(lic) == 0:

                db.cbapp_windows_activated_key.insert(license_key=lic_key, device_serial=dev_uuid, user_name=vuser_name,
                                                      company=vcompany)

            #Da dang ky trial or dang dung trial (da tai sach trai nghiem)
            elif lic.first()['license_key'].startswith('0000-0000'):

                db(db.cbapp_windows_activated_key.device_serial == dev_uuid).update(license_key=lic_key,
                                                                                    user_name=vuser_name,
                                                                                    company=vcompany)
            else:
                return dict(error=CB_0027)

            #db.person.update_or_insert(db.cbapp_windows_activated_key.device_serial == dev_uuid,
            #                           license_key=lic_key, device_serial=dev_uuid)
            return dict(message=CB_0000)

    except Exception as ex:
            print ex
            return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


'''
Kiem tra trang thai dang ky license theo uuid
'''


def license_state():

    try:

        if len(request.vars) == 0:
                return dict(error=CB_0002)

        dev_uuid = request.vars['device_serial']

        license_k = db(db.cbapp_windows_activated_key.device_serial == dev_uuid)\
            .select().as_list()

        return dict(license_state=license_k)

    except Exception as e:
            print e
            return dict(error=CB_0004)


def cbapp_trial_gift():
    try:
        product_title = "Tiếng Anh 3, tập 1"
        product_id = 677
        category_id = 56
        token = request.vars.user_token
        users = db(db.clsb_user.user_token == token).select()
        if len(users) == 0:
            return dict(error=CB_0012)
        user_id = users.first()['id']
        history = db(db.clsb30_product_history.product_id == product_id)\
                (db.clsb30_product_history.user_id == user_id).select()
        if len(history) == 0:
            db.clsb30_product_history.insert(product_title=product_title,
                                             product_id=product_id,
                                             user_id=user_id,
                                             category_id=category_id,
                                             product_price=0)
        history_media = db(db.clsb30_media_history.product_id == product_id)\
                (db.clsb30_media_history.user_id == user_id).select()
        if len(history_media) == 0:
            db.clsb30_media_history.insert(product_title=product_title,
                                           product_id=product_id,
                                           user_id=user_id,
                                           category_id=category_id,
                                           product_price=0)
        return dict(mess="OK")
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def script_insert_license_key():
    try:
        file_key = "/home/temp/cbwin_key.txt"
        if request.vars and 'path' in request.vars:
            file_key = request.vars.path
        with open(file_key) as f:
            lines = f.readlines()
        for key in lines:
            try:
                db.cbapp_windows_key_available.insert(license_key=key.strip())
            except Exception as err:
                print(str(err))
        return dict(mess="OK")
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))