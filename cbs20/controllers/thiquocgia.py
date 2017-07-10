__author__ = 'vuong'

from contrib.pbkdf2 import *
from datetime import *
import urllib
import time
import string
import random
import os
import re
import fs.path
import pdf2dev
import sys

SUCCESS = CB_0000#cbMsg.CB_0000
EXISTENT = CB_0005#cbMsg.CB_0005
LACK_ARGS = CB_0002#cbMsg.CB_0002
FAILURE = CB_0006#cbMsg.CB_0006
DB_RQ_FAILD = CB_0003#cbMsg.CB_0003
PWD_ERR = CB_0008
DISABLE = CB_0009
NOT_EXIST = CB_0001
USER_NAME_NOT_EXIST = CB_0010
INVALID_DEVICE_SERIAL = CB_0016
DOMAIN_VDC = "123.30.179.205"
# DOMAIN_VDC = "classbook.vn"

myTable = db.clsb_user
table = 'clsb_user'
P_2_D_KEY = 'c-p3d*b'
from datetime import datetime


def genT(name, time):
#    name = request.args(0)
    if not table in db.tables(): return dict(error=NOT_EXIST)
    if name:
        s = os.urandom(10)#''.join(random.choice(string.letters + string.digits) for x in range(10))
        t = pbkdf2_hex(name, s)
        try:
            #myTable.update_or_insert(myTable.username == name, user_token=t, lastLoginTime=time)
            myTable.update_or_insert(myTable.username == name, lastLoginTime=time)
            token = db(myTable.username == name).select(myTable.user_token).first()['user_token']
            if token is None or token == "":
                myTable.update_or_insert(myTable.username == name, user_token=t, lastLoginTime=time)
                token = t
            return token
        except Exception as e:
            return DB_RQ_FAILD + str(e) + name
    else:
        return LACK_ARGS


@request.restful()
def gen_token():
    def GET(*args, **vars):
        try:
            username = vars['username']
            select_by_username = db(db.clsb_user.username.like(username)).select()
            if len(select_by_username) == 0:
                type_user = vars['type_user']
                if type_user == 'classbook':
                    type_user = 'normal'
                db.clsb_user.insert(username=vars['username'],
                                        password=vars['password'],
                                        firstName=vars['firstName'],
                                        lastName=vars['lastName'],
                                        email=vars['email'],
                                        phoneNumber=vars['phoneNumber'],
                                        address=vars['address'],
                                        type_user=type_user,
                                        register_from='thiquocgia.vn',
                                        created_on=datetime.now())
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
                return dict(status='new', token=token)
            token = select_by_username.first()['user_token']
            return dict(status='old', token=token)
        except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

    def POST(*args, **vars):
        try:
            username = vars['username']
            select_by_username = db(db.clsb_user.username.like(username)).select()
            if len(select_by_username) == 0:
                type_user = vars['type_user']
                if type_user == 'classbook':
                    type_user = 'normal'
                db.clsb_user.insert(username=vars['username'],
                                        password=vars['password'],
                                        firstName=vars['firstName'],
                                        lastName=vars['lastName'],
                                        email=vars['email'],
                                        phoneNumber=vars['phoneNumber'],
                                        address=vars['address'],
                                        type_user=type_user,
                                        register_from='thiquocgia.vn',
                                        created_on=datetime.now())
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
                return dict(status='new', token=token)
            token = select_by_username.first()['user_token']
            return dict(status='old', token=token)
        except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
    return locals()

import hashlib
@request.restful()
def auto_login():
    def GET(*args, **vars):
        try:
            username = vars['username']
            select_by_username = db(db.clsb_user.username.like(username)).select()
            seskey = "trungdepzai"
            secret = hashlib.md5((str(vars['username']) + seskey)).hexdigest()
            if secret != str(vars['secret']):
                return dict(error="L?i request")
            if len(select_by_username) == 0:
                type_user = vars['type_user']
                if type_user == 'classbook':
                    type_user = 'normal'
                db.clsb_user.insert(username=vars['username'],
                                        password=vars['password'],
                                        firstName=vars['firstName'],
                                        lastName=vars['lastName'],
                                        email=vars['email'],
                                        phoneNumber=vars['phoneNumber'],
                                        address=vars['address'],
                                        type_user=type_user,
                                        register_from='thiquocgia.vn',
                                        created_on=datetime.now())
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
                return dict(status='new', token=token)
            token = select_by_username.first()['user_token']
            if token is None:
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
            return dict(status='old', token=token)
        except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

    def POST(*args, **vars):
        try:
            username = vars['username']
            select_by_username = db(db.clsb_user.username.like(username)).select()
            seskey = "trungdepzai"
            secret = hashlib.md5((str(vars['username']) + seskey)).hexdigest()
            if secret != str(vars['secret']):
                return dict(error="L?i request")
            if len(select_by_username) == 0:
                type_user = vars['type_user']
                if type_user == 'classbook':
                    type_user = 'normal'
                db.clsb_user.insert(username=vars['username'],
                                        password=vars['password'],
                                        firstName=vars['firstName'],
                                        lastName=vars['lastName'],
                                        email=vars['email'],
                                        phoneNumber=vars['phoneNumber'],
                                        address=vars['address'],
                                        type_user=type_user,
                                        register_from='thiquocgia.vn',
                                        created_on=datetime.now())
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
                return dict(status='new', token=token)
            token = select_by_username.first()['user_token']
            if token is None:
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
            return dict(status='old', token=token)
        except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
    return locals()


@request.restful()
def auto_login_third():
    def GET(*args, **vars):
        try:
            username = vars['username']
            select_by_username = db(db.clsb_user.username.like(username)).select()
            seskey = "clsb"
            secret = hashlib.md5((str(vars['username']) + seskey)).hexdigest()
            if secret != str(vars['secret']):
                return dict(error="L?i request")
            if len(select_by_username) == 0:
                type_user = vars['type_user']
                if type_user == 'classbook':
                    type_user = 'normal'
                db.clsb_user.insert(username=vars['username'],
                                        password=vars['password'],
                                        firstName=vars['firstName'],
                                        lastName=vars['lastName'],
                                        email=vars['email'],
                                        phoneNumber=vars['phoneNumber'],
                                        address=vars['address'],
                                        type_user=type_user,
                                        register_from='thiquocgia.vn',
                                        created_on=datetime.now())
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
                return dict(status='new', token=token)
            token = select_by_username.first()['user_token']
            if token is None:
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
            return dict(status='old', token=token)
        except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

    def POST(*args, **vars):
        try:
            username = vars['username']
            select_by_username = db(db.clsb_user.username.like(username)).select()
            seskey = "clsb"
            secret = hashlib.md5((str(vars['username']) + seskey)).hexdigest()
            if secret != str(vars['secret']):
                return dict(error="L?i request")
            if len(select_by_username) == 0:
                type_user = vars['type_user']
                if type_user == 'classbook':
                    type_user = 'normal'
                db.clsb_user.insert(username=vars['username'],
                                        password=vars['password'],
                                        firstName=vars['firstName'],
                                        lastName=vars['lastName'],
                                        email=vars['email'],
                                        phoneNumber=vars['phoneNumber'],
                                        address=vars['address'],
                                        type_user=type_user,
                                        register_from='thiquocgia.vn',
                                        created_on=datetime.now())
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
                return dict(status='new', token=token)
            token = select_by_username.first()['user_token']
            if token is None:
                token = genT(vars['username'], datetime.now())
                db(db.clsb_user.username.like(username)).update(user_token=token)
            return dict(status='old', token=token)
        except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
    return locals()


def sum_pay_tqg():
    try:
        from datetime import datetime
        username = request.vars.username
        datestart = datetime.strptime("2016-01-01", "%Y-%m-%d")
        sum_nl = db.clsb_transaction.face_value.sum()
        total_nl = db(db.clsb_transaction.user_id == db.clsb_user.id)\
            (db.clsb_user.username.like(username))\
            (db.clsb_transaction.status == "COMPLETE")\
            (db.clsb_transaction.created_on >= datestart).select(sum_nl).first()[sum_nl]
        if total_nl is None:
            total_nl = 0
        sum_card = db.clsb30_tqg_card_log.card_value.sum()
        total_card = db(db.clsb30_tqg_card_log.user_id == db.clsb_user.id)\
            (db.clsb_user.username.like(username))\
            (db.clsb30_tqg_card_log.created_on >= datestart).select(sum_card).first()[sum_card]
        if total_card is None:
            total_card = 0

        sum_tranfer = db.clsb30_tqg_log_tranfer.fund.sum()
        total_tranfer = db(db.clsb30_tqg_log_tranfer.user_id == db.clsb_user.id)\
            (db.clsb_user.username.like(username))\
            (db.clsb30_tqg_log_tranfer.status.like("SUCCESS"))\
            (db.clsb30_tqg_log_tranfer.created_on >= datestart).select(sum_tranfer).first()[sum_tranfer]
        if total_tranfer is None:
            total_tranfer = 0
        return dict(total=total_nl + total_card + total_tranfer, total_nl=total_nl,
                    total_card=total_card, total_tranfer=total_tranfer)
    except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

