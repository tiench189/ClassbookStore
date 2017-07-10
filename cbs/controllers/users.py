# -*- coding: utf-8 -*-
# try something like

# @author: hant 27-02-2013

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

SUCCESS = CB_0000  # cbMsg.CB_0000
EXISTENT = CB_0005  # cbMsg.CB_0005
LACK_ARGS = CB_0002  # cbMsg.CB_0002
FAILURE = CB_0006  # cbMsg.CB_0006
DB_RQ_FAILD = CB_0003  # cbMsg.CB_0003
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

customer_care_user = ["trunggn@tinhvan.com", "tientinh@tinhvan.com", ]


def genT(name, time):
    #    name = request.args(0)
    if not table in db.tables(): return dict(error=NOT_EXIST)
    if name:
        s = os.urandom(10)  # ''.join(random.choice(string.letters + string.digits) for x in range(10))
        t = pbkdf2_hex(name, s)
        try:
            # myTable.update_or_insert(myTable.username == name, user_token=t, lastLoginTime=time)
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


def new_token(name, time):
    #    name = request.args(0)
    if not table in db.tables(): return dict(error=NOT_EXIST)
    if name:
        s = os.urandom(10)  # ''.join(random.choice(string.letters + string.digits) for x in range(10))
        t = pbkdf2_hex(name, s)
        try:
            myTable.update_or_insert(myTable.username == name, user_token=t, lastLoginTime=time)
            token = t
            return token
        except Exception as e:
            return DB_RQ_FAILD + str(e) + name
    else:
        return LACK_ARGS


def get_user_timeout():
    """
    var username
    """
    if not request.vars and len(request.vars) > 1:
        return dict(error=LACK_ARGS)
    username = request.vars['username']

    user_token = db(db.clsb_user.email == username).select(db.clsb_user.user_token).first()

    return dict(token=user_token['user_token'])


def register():
    """
    register-function registers a new ClassBook user.
    @var username, password, firstName, lastName, email, phoneNumber, address, district:
    @return: users_tbl, msgerr
    """
    # the minimum required args
    nbargsrequired = 6
    # request = ../a/c/f/login/password/firstname/lastname/email/phonenumber/address  -->args: 8
    if request.vars and not request.args:
        try:
            pwd = pbkdf2_hex(P_2_D_KEY, request.vars.password)
            username = request.vars.username
            SPECIAL_CHARACTERS = [' ', '!', '"', '#', '$', '%',
                                  '*', '+', ',', ':', '<', '=', '>', '?', '[', '\\', ']', '^',
                                  '`', '|', '~', 'À', 'Á', 'Â', 'Ã', 'È', 'É', 'Ê', 'Ì', 'Í', 'Ò',
                                  'Ó', 'Ô', 'Õ', 'Ù', 'Ú', 'Ý', 'à', 'á', 'â', 'ã', 'è', 'é', 'ê',
                                  'ì', 'í', 'ò', 'ó', 'ô', 'õ', 'ù', 'ú', 'ý', 'Ă', 'ă', 'Đ', 'đ',
                                  'Ĩ', 'ĩ', 'Ũ', 'ũ', 'Ơ', 'ơ', 'Ư', 'ư', 'Ạ', 'ạ', 'Ả', 'ả', 'Ấ',
                                  'ấ', 'Ầ', 'ầ', 'Ẩ', 'ẩ', 'Ẫ', 'ẫ', 'Ậ', 'ậ', 'Ắ', 'ắ', 'Ằ', 'ằ',
                                  'Ẳ', 'ẳ', 'Ẵ', 'ẵ', 'Ặ', 'ặ', 'Ẹ', 'ẹ', 'Ẻ', 'ẻ', 'Ẽ', 'ẽ', 'Ế',
                                  'ế', 'Ề', 'ề', 'Ể', 'ể', 'Ễ', 'ễ', 'Ệ', 'ệ', 'Ỉ', 'ỉ', 'Ị', 'ị',
                                  'Ọ', 'ọ', 'Ỏ', 'ỏ', 'Ố', 'ố', 'Ồ', 'ồ', 'Ổ', 'ổ', 'Ỗ', 'ỗ', 'Ộ',
                                  'ộ', 'Ớ', 'ớ', 'Ờ', 'ờ', 'Ở', 'ở', 'Ỡ', 'ỡ', 'Ợ', 'ợ', 'Ụ', 'ụ',
                                  'Ủ', 'ủ', 'Ứ', 'ứ', 'Ừ', 'ừ', 'Ử', 'ử', 'Ữ', 'ữ', 'Ự', 'ự', 'Ý',
                                  'Ỳ', 'Ỵ', 'Ỷ', 'Ỹ', 'ý', 'ỳ', 'ỵ', 'ỷ', 'ỹ']
            for char in SPECIAL_CHARACTERS:
                if char in username:
                    return dict(error="Tên đăng nhập chỉ được phép chứa các kí tự a-z 0-9 '@' '.'")
            request.vars.pop('password')
            request.vars.update(password=pwd)
            if request.vars.lastName == "" and request.vars.firstName == "":
                request.vars.update(lastName="User")
                request.vars.update(firstName="Guest")
            new_user = myTable.insert(**request.vars)

            data = dict(record_id=str(new_user), table_name='clsb_user', key_unique='username')
            insert_to_log_temp(data)
            # url_log = URL(host=settings.current_server, a='cbs20', c="syncmain", f="insert_to_temp",
            #               vars=dict(record_id=str(new_user), table_name='clsb_user', key_unique='username'))
            # url_sign = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="register_user", vars=request.vars)
            # print(url_sign)
            # urllib2.urlopen(url_sign)
            return dict(item=SUCCESS)
        except Exception as e:
            print "Error: " + str(e) + str(sys.exc_traceback.tb_lineno)
            if (str(e).find("Duplicate") >= 0) & (str(e).find("username") >= 0):
                return dict(error="Tài khoản đã tồn tại")
            if (str(e).find("Duplicate") >= 0) & (str(e).find("email") >= 0):
                return dict(error="Email này đã được dùng để đăng kí")
            return dict(error=DB_RQ_FAILD)
    elif request.args and len(request.args) >= nbargsrequired and not request.vars:
        if db(myTable.username.like(request.args(0))).select() or db(myTable.email.like(request.args(4))).select():
            return dict(error=EXISTENT)
        else:
            lname = request.args(3)
            fname = request.args(2)
            if lname == "" and fname == "":
                lname = "User"
                fname = "Guest"
            myTable.update_or_insert(
                username=request.args(0), password=pbkdf2_hex(P_2_D_KEY, request.args(1)),
                lastLoginTime=request.now, firstName=lname,
                lastName=fname, email=request.args(4),
                phoneNumber=request.args(5), address=(request.args(6) or "ND"), district=request.args(7))
            # url_sign = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="register_user", args=request.args)
            # urllib2.urlopen(url_sign)
            return dict(item=SUCCESS)
    else:
        return dict(error=LACK_ARGS)


def authentication():  # params: username, password. This function will gen token
    if request.vars and len(request.vars) == 2 and not request.args:
        userSelected = db(myTable.username.like(request.vars.username)).select().as_list()
        if userSelected:
            password = userSelected[0]['password']
            if password == pbkdf2_hex(P_2_D_KEY, request.vars.password):
                if userSelected[0]['status']:
                    t = genT(request.vars.username, request.now)
                    return dict(token=t, display=userSelected[0]['lastName'])
                else:
                    return dict(error=DISABLE)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    elif request.args and not request.vars and len(request.args) == 2:
        userSelected = db(myTable.username.like(request.args(0))).select().as_list()
        if userSelected:
            password = userSelected[0]['password']
            if password == pbkdf2_hex(P_2_D_KEY, request.args(1)):
                if userSelected[0]['status']:
                    t = genT(request.args(0), request.now)
                    return dict(token=t, display=userSelected[0]['lastName'])
                else:
                    return dict(error=DISABLE)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    else:
        return dict(error=LACK_ARGS)


def authentication_by_token():  # params: username, token. if username and token valid -> return token
    if request.vars and len(request.vars) == 2 and not request.args:
        userSelected = db(myTable.username.like(request.vars.username)).select().as_list()
        if userSelected:
            token = userSelected[0]['user_token']
            # print token
            # print request.vars['token']
            if token == request.vars['token']:
                if userSelected[0]['status']:
                    t = genT(request.vars.username, request.now)
                    return dict(token=t)
                else:
                    return dict(error=DISABLE)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    else:
        return dict(error=LACK_ARGS)


# use for confirm when user pay for download
# /cbs/users/confirmpwd/hant/123456/a0cdabe25a7c1248ae68de002eee5262255cd57e8716510f
def confirmpwd():
    if request.vars and len(request.vars) == 3 and not request.args:
        userSelected = db(myTable.username.like(request.vars.username)).select().as_list()
        result = checkTimeOut(userSelected[0]['username'], request.vars.token)
        if result != SUCCES:
            return dict(error=result)
        if userSelected:
            password = userSelected[0]['password']
            if password == pbkdf2_hex(P_2_D_KEY, request.vars.password):
                if userSelected[0]['status']:
                    return dict(item=CB_0000)
                else:
                    return dict(error=DISABLE)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    elif request.args and not request.vars and len(request.args) == 3:
        userSelected = db(myTable.username.like(request.args(0))).select().as_list()
        result = checkTimeOut(userSelected[0]['username'], request.args(2))
        if result != SUCCES:
            return dict(error=result)
        if userSelected:
            password = userSelected[0]['password']
            if password == pbkdf2_hex(P_2_D_KEY, request.args(1)):
                if userSelected[0]['status']:
                    return dict(item=CB_0000)
                else:
                    return dict(error=DISABLE)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    else:
        return dict(error=LACK_ARGS)


def login():  # params: username, password (without token)
    if request.vars and len(request.vars) == 2 and not request.args:
        userSecleted = db(myTable.username.like(request.vars.username)).select().as_list()
        if userSecleted:
            password = userSecleted[0]['password']
            if password == request.vars.password:
                if userSecleted[0]['status']:
                    return dict(item=SUCCES)
                else:
                    return dict(error=DISABLE)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    elif request.args and not request.vars and len(request.args) == 2:
        userSelected = db(myTable.username.like(request.args(0))).select().as_list()
        if userSelected:
            password = userSelected[0]['password']
            if password == request.args(1):
                if userSelected[0]['status']:
                    return dict(item=SUCCES)
                else:
                    return dict(error=DISABLE)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    else:
        return dict(error=LACK_ARGS)


def checkUsernameEmail():  # params: username, email
    if request.vars and len(request.vars) < 3:
        userSeleted = db(myTable.username.like(request.vars.username)).select()
        emailSeleted = db(myTable.email.like(request.vars.email)).select()
        # update login time
        updateLogTime(request.vars.username)

        if userSeleted or emailSeleted:
            return dict(error=FAILURE)
        else:
            return dict(item=SUCCESS)
    else:
        return dict(error=LACK_ARGS)


def select():  # ByUsername with token
    if request.args and len(request.args) >= 2:
        try:
            project_code = "SAMSUNG"
            # print(request.args)
            if len(request.args) > 2:
                project_code = request.args[2]
            userSelected = db(myTable.username == request.args(0)).select().as_list()
            # print(userSelected)
            if len(userSelected) == 1:
                # check token
                if userSelected[0]['user_token'] != request.args[1]:
                    return dict(error=CB_0012)
                # result = checkTimeOut(userSelected[0]['username'], request.args(1))
                # if result != SUCCES:
                #    return dict(error=result)
                #    #update login time
                # updateLogTime(request.args(0))

                #                 devices = db(db.clsb_device.user_id.like(userSelected[0]['id']))(db.clsb_device.status==True).select()
                devices = db(db.clsb_device.user_id.like(userSelected[0]['id'])).select(db.clsb_device.device_serial,
                                                                                        db.clsb_device.in_use,
                                                                                        db.clsb_device.device_name)
                res = dict()
                res['id'] = userSelected[0]['id']
                res['username'] = userSelected[0]['username']
                # res['password'] = userSelected[0]['password']
                res['lastLoginTime'] = '%s' % userSelected[0]['lastLoginTime']
                res['firstName'] = userSelected[0]['firstName']
                res['lastName'] = userSelected[0]['lastName']
                res['email'] = userSelected[0]['email']
                res['phoneNumber'] = userSelected[0]['phoneNumber']
                res['address'] = userSelected[0]['address']
                res['valid_time'] = userSelected[0]['valid_time']
                res['type_user'] = userSelected[0]['type_user']
                res['valid_time_message'] = "Bạn đã thay đổi thiết bị mặc định " \
                                            + str(userSelected[0]['valid_time']) \
                                            + " lần.\nBạn còn lại " + str(
                    MAX_VALID_TIME_SET_DEFAULT - userSelected[0]['valid_time']) \
                                            + " lần thay đổi thiết bị mặc định."
                res['valid_device_time_message'] = "Bạn đã thay đổi thiết bị " \
                                                   + str(userSelected[0]['valid_time']) \
                                                   + " lần.Bạn còn lại " + str(
                    MAX_VALID_TIME_SET_DEFAULT - userSelected[0]['valid_time']) \
                                                   + " lần thay đổi thiết bị."
                res['max_valid_device'] = MAX_VALID_TIME_SET_DEFAULT
                res['fund'] = userSelected[0]['fund']
                if devices:
                    i = 0
                    tmp = ''
                    tmp_device_name = ''
                    d_in_use = ''
                    for d in devices:
                        if d['in_use'] == True:
                            d_in_use = d['device_serial']

                        row = db(db.clsb_device.device_serial == d['device_serial']).select(db.clsb_device.last_uid,
                                                                                            db.clsb_device.user_id).as_list()
                        last_uid = row[0]['last_uid']
                        device_uid = row[0]['user_id']
                        #                 print userid[0]['id']
                        #                 print device_uid
                        #                 print device[0]['device_serial']
                        # this is deleted by someone then other can add it. IF YOU CHANGE THIS FUNC PLS VALIDATE THE FUNC DELETE_DEVICE
                        # neu last_uid == device_uid, device da bi xoa ma chua duoc dk boi tk khac
                        if device_uid != last_uid:
                            #                             if i != 0:
                            tmp += '#'
                            tmp += d['device_serial']

                            tmp_device_name += '#'
                            tmp_device_name += str(d['device_name'])

                        i += 1

                    res['devices'] = tmp  # ""+tmp[0:]
                    res['device_name'] = tmp_device_name
                    res['device_in_use'] = d_in_use
                # print "------"
                #                     print res['devices']
                else:
                    res['devices'] = ''
                    res['device_in_use'] = ''
                    res['device_name'] = ''

                if re.search(r'^#', res['devices']):
                    res['devices'] = res['devices'][1:]
                if re.search(r'^#', res['device_name']):
                    res['device_name'] = res['device_name'][1:]
                user_use_gift = db(db.clsb30_gift_code_log.user_id == userSelected[0]['id']).select()
                # if len(user_use_gift) > 0:
                res['gift_used'] = False
                # else:
                #    res['gift_used'] = False
                return dict(items=res)
            else:
                return dict(error=USER_NAME_NOT_EXIST)
        except Exception as e:
            return dict(error=DB_RQ_FAILD + str(e) + " on line: " + str(sys.exc_traceback.tb_lineno))
    else:
        return dict(error=LACK_ARGS)


def get_user_info():  # ByUsername with token
    if request.args and len(request.args) == 2:
        try:
            userSelected = db(myTable.username.like(request.args(0))).select().as_list()
            if len(userSelected) == 1:
                # check token
                result = checkTimeOut(userSelected[0]['username'], request.args(1))
                if result != SUCCES:
                    return dict(error=result)
                    # update login time
                updateLogTime(request.args(0))

                #                 devices = db(db.clsb_device.user_id.like(userSelected[0]['id']))(db.clsb_device.status==True).select()
                devices = db(db.clsb_device.user_id.like(userSelected[0]['id'])).select(db.clsb_device.device_serial,
                                                                                        db.clsb_device.in_use,
                                                                                        db.clsb_device.device_name)
                res = dict()
                res['id'] = userSelected[0]['id']
                res['username'] = userSelected[0]['username']
                # res['password'] = userSelected[0]['password']
                res['lastLoginTime'] = '%s' % userSelected[0]['lastLoginTime']
                res['firstName'] = userSelected[0]['firstName']
                res['lastName'] = userSelected[0]['lastName']
                res['email'] = userSelected[0]['email']
                res['phoneNumber'] = userSelected[0]['phoneNumber']
                res['address'] = userSelected[0]['address']
                res['valid_time'] = userSelected[0]['valid_time']
                res['type_user'] = userSelected[0]['type_user']
                res['valid_time_message'] = "Bạn đã thay đổi thiết bị mặc định " \
                                            + str(userSelected[0]['valid_time']) \
                                            + " lần.\nBạn còn lại " + str(
                    MAX_VALID_TIME_SET_DEFAULT - userSelected[0]['valid_time']) \
                                            + " lần thay đổi thiết bị mặc định."
                res['valid_device_time_message'] = "Bạn đã thay đổi thiết bị " \
                                                   + str(userSelected[0]['valid_time']) \
                                                   + " lần.Bạn còn lại " + str(
                    MAX_VALID_TIME_SET_DEFAULT - userSelected[0]['valid_time']) \
                                                   + " lần thay đổi thiết bị."
                res['max_valid_device'] = MAX_VALID_TIME_SET_DEFAULT
                res['fund'] = userSelected[0]['fund']
                device_list = list()
                if devices:
                    i = 0
                    tmp = ''
                    tmp_device_name = ''
                    d_in_use = ''
                    for d in devices:
                        if d['in_use'] == True:
                            d_in_use = d['device_serial']

                        row = db(db.clsb_device.device_serial == d['device_serial']).select(db.clsb_device.last_uid,
                                                                                            db.clsb_device.user_id).as_list()
                        last_uid = row[0]['last_uid']
                        device_uid = row[0]['user_id']
                        #                 print userid[0]['id']
                        #                 print device_uid
                        #                 print device[0]['device_serial']
                        # this is deleted by someone then other can add it. IF YOU CHANGE THIS FUNC PLS VALIDATE THE FUNC DELETE_DEVICE
                        # neu last_uid == device_uid, device da bi xoa ma chua duoc dk boi tk khac
                        if device_uid != last_uid:
                            #                             if i != 0:
                            tmp += '#'
                            tmp += d['device_serial']

                            tmp_device_name += '#'
                            tmp_device_name += str(d['device_name'])
                            tmp_dict = dict()
                            tmp_dict['device_serial'] = d['device_serial']
                            tmp_dict['device_name'] = d['device_name']
                            device_list.append(tmp_dict)

                        i += 1

                    res['devices'] = device_list
                    # res['device_name'] = tmp_device_name
                    # res['device_in_use'] = d_in_use
                #                     print "------"
                #                     print res['devices']
                else:
                    # res['devices'] = ''
                    # res['device_in_use'] = ''
                    # res['device_name'] = ''
                    res['devices'] = device_list

                # if re.search(r'^#', res['devices']):
                #    res['devices'] = res['devices'][1:]
                # if re.search(r'^#', res['device_name']):
                #    res['device_name'] = res['device_name'][1:]
                user_use_gift = db(db.clsb30_gift_code_log.user_id == userSelected[0]['id']).select()
                if len(user_use_gift) > 0:
                    res['gift_used'] = True
                else:
                    res['gift_used'] = False
                return dict(items=res)
            else:
                return dict(error=USER_NAME_NOT_EXIST)
        except Exception as e:
            return dict(error=DB_RQ_FAILD + str(e) + " on line: " + str(sys.exc_traceback.tb_lineno))
    else:
        return dict(error=LACK_ARGS)


def istimeout():  # /username/token
    username = request.args(0)
    token = request.args(1)
    result = checkTimeOut(username, token)
    if result != SUCCES:
        return dict(error=result)
    else:
        return dict(item=CB_0000)


# insert all field. USERNAME and device_serial is obligate (requires token)
# If this is the first user's device, then set it to in_use
# vars: user_name, device_serial, token, device_name(option)
def adddevice():
    table = 'clsb_device'
    if not table in db.tables():
        return dict(error=NOT_EXISTED)

    app_version = None
    if "version" in request.vars:
        app_version = request.vars['version']

    username = request.vars.username
    result = checkTimeOut(username, request.vars.user_token)
    if result != SUCCES:
        return dict(error=result)
        # update login time
    updateLogTime(username)

    if pdf2dev.isValidSerial(request.vars.device_serial) == None and request.vars.device_serial != "0160C5-121206869":
        return dict(error=INVALID_DEVICE_SERIAL)

    if request.vars and request.vars >= 2 and username:
        # update login time
        updateLogTime(username)

        try:
            userid = db(db.clsb_user.username == username).select(db.clsb_user._id, db.clsb_user.valid_time).as_list()

            if len(userid) != 1:
                return dict(error=DATA_ERROR)
            # check number of device user owned (max =5):
            user_device_list = db(db.clsb_device.user_id == userid[0]['id']).select(db.clsb_device.id).as_list()
            quota = 5
            if request.vars.username in customer_care_user:
                quota = 50
            if len(user_device_list) == quota:
                return dict(error='Đăng kí thất bại, bạn đang sở hữu đủ số thiết bị tối đa.')

            if userid[0]['valid_time'] == quota:
                return dict(error='Đăng kí thất bại, bạn đã đăng kí đủ số lần qui định.')

            # limite the maximum nb of device to 3 devices
            #             result = verifyNbDevice(userid[0]['id'])
            #             if result != SUCCES:
            #                 return dict(error=result)
            if request.vars.device_name:
                device_name = request.vars.device_name
            else:
                device_name = lambda: int(round(time.time() * 1000))
            request.vars.pop('username')
            request.vars.pop('user_token')
            request.vars.update(user_id=userid[0]['id'])
            request.vars.update(device_name=device_name)
            if request.vars.device_serial.startswith('CA') or request.vars.device_serial.startswith(
                    'CI') or request.vars.device_serial.startswith('EF'):
                request.vars.update(device_type='OTHER')

            # verify that the device is not in_use by another user.
            #             device = db(db.clsb_device.device_serial == request.vars.device_serial).select(db.clsb_device.device_serial,
            #                                                                                             db.clsb_device.in_use).as_list()
            #             if device:
            #                 return dict(error=CB_0018) # DEVICE_EXISTED
            # #                 if device[0]['in_use']:
            # #                     return dict(error=CB_0022) # error device is in_use
            # #                 else:
            # #                     db(db.clsb_device.device_serial == device[0]['device_serial']).delete()
            # if this is the first user's device then set in_use to true 
            user_has_device = db(db.clsb_device.user_id == userid[0]['id']).select(db.clsb_device.device_serial)
            if not user_has_device:
                request.vars.update(in_use=True)
                #             db[table].insert(**request.vars)

            # verify that device is registed or not
            device = db(db.clsb_device.device_serial == request.vars.device_serial).select(
                db.clsb_device.device_serial).as_list()

            # kiem tra user da dang ky device hay chua
            is_registered = db(db.clsb_device.user_id == userid[0]['id'])(
                db.clsb_device.device_serial == request.vars.device_serial).select(db.clsb_device.device_serial)
            if len(is_registered):
                return dict(item=SUCCESS)
            # if not, then this is the new device, hoac user chua dang ky (user khac co the da dang ky)
            if not device or (not is_registered and app_version == 'APPWINDOW'):
                if "version" in request.vars:
                    request.vars.pop('version')  # loai bo version ra khoi request, vi ko co truong version trong bang
                new_device = db[table].insert(**request.vars)
                # Tang tien khi dang ky thiet bi moi
                '''
                if request.vars.device_serial.startswith('CA') or request.vars.device_serial.startswith('EF'):
                    pass
                else:
                    fund(username) #Tang tien cho account dang ky device moi, defined in models/utils.py
                '''

                check_log = db(db.clsb30_device_log.user_id == userid[0]['id']) \
                    (db.clsb30_device_log.device_serial == request.vars.device_serial).select()
                # Khong tang so lan dang ky neu xoa di va dang ky lai mot thiet bi
                if len(check_log) == 0:
                    userid[0]['valid_time'] += 1
                    db(db.clsb_user.username == username).update(valid_time=userid[0]['valid_time'])
                    db.clsb30_device_log.insert(user_id=userid[0]['id'], device_serial=request.vars.device_serial)

                return dict(item=SUCCESS)
                # else this devices is the old one, check if this is deleted by someone or not.
            else:
                # Neu device da duoc dang ky sau do unregister => cap nhat lai user dang ky moi
                # print 'device is not None'
                # PhuongNH edit: check user_id is null ?
                # row = db(db.clsb_device.device_serial == device[0]['device_serial']).select(
                #    db.clsb_device.user_id).as_list()
                #
                # user_id = row[0]['user_id']
                #
                ## user id = None: thiet bi da tung duoc dang ki boi user khac, sau do bi unregister(cap nha user = null)
                # if user_id is None:
                #
                #    db(db.clsb_device.device_serial == request.vars.device_serial).update(user_id=userid[0]['id'],
                #                                                                                last_uid=None,
                #                                                                                device_name=device_name)
                #    res_id = db(db.clsb_device.device_serial == request.vars.device_serial).select().first()['id']
                #    data = dict(record_id=res_id, table_name=table, key_unique='user_id.device_serial')
                #    insert_to_log_temp(data)
                #    check_log = db(db.clsb30_device_log.user_id == userid[0]['id'])\
                #            (db.clsb30_device_log.device_serial == request.vars.device_serial).select();
                #    if len(check_log) == 0:
                #        userid[0]['valid_time'] += 1
                #        db(db.clsb_user.username == username).update(valid_time=userid[0]['valid_time'])
                #        db.clsb30_device_log.insert(user_id=userid[0]['id'], device_serial=request.vars.device_serial)
                #    userid = db(db.clsb_user.username == username).select().first()['id']
                #    data = dict(record_id=userid, table_name='clsb_user', key_unique='username')
                #    insert_to_log_temp(data)
                #    return dict(item=SUCCESS)
                ## thiet bi dang duong so huu boi user khac
                # else:
                return dict(error=CB_0018)  # DEVICE_EXISTED

                # row = db(db.clsb_device.device_serial == device[0]['device_serial']).select(db.clsb_device.last_uid,
                #                                                                            db.clsb_device.user_id).as_list()
                # last_uid = row[0]['last_uid']
                # device_uid = row[0]['user_id']
                ##                 print userid[0]['id']
                ##                 print device_uid
                ##                 print device[0]['device_serial']
                ## this is deleted by someone then other can add it. IF YOU CHANGE THIS FUNC PLS VALIDATE THE FUNC DELETE_DEVICE
                # if device_uid == last_uid:
                #    db(db.clsb_device.device_serial == request.vars.device_serial).update(user_id=userid[0]['id'],
                #                                                                          last_uid=None,
                #                                                                          device_name=device_name)
                #    #                     print "add"
                #    return dict(item=SUCCESS)
                # else:
                #                     print "dont add"
                # return dict(error=CB_0018) # DEVICE_EXISTED
        except Exception as e:
            import sys
            return dict(error=DB_RQ_FAILD + str(e) + " on line: " + str(sys.exc_traceback.tb_lineno))
    return dict(error=LACK_ARGS)


# /cbs/users/delete_device?username=phuongnh@tinhvan.com&device_serial=018373-091212050&user_token=
def delete_device():  # params: username, device_serial with user_token

    table = 'clsb_device'

    if not table in db.tables(): return dict(error=NOT_EXISTED)
    result = checkTimeOut(request.vars.username, request.vars.user_token)
    if result != SUCCES:
        return dict(error=result)

    if request.vars and request.vars >= 2 and request.vars.username:
        # update login time
        updateLogTime(request.vars.username)

        try:
            if request.vars.username in customer_care_user:
                return dict(error="Tài khoản này không có quyền xóa thiết bị")
            userid = db(db.clsb_user.username == request.vars.username).select(db.clsb_user._id,
                                                                               db.clsb_user.valid_time).as_list()
            userid = userid[0]['id']

            # res = db(db[table].device_serial == request.vars.device_serial).select(db[table].in_use)
            # res = res[0]['in_use']
            # if res == True:
            #    return dict(error=CB_0022) #DEVICE_IS_IN_USE
            # else:
            db(db[table].user_id == userid)(db[table].device_serial == request.vars.device_serial).delete()

            # Xoa device = update user_id = None, dung cho truong hop tang tien khi dang ky device moi - vuongtm
            # res = db(db[table].user_id == userid)(db[table].device_serial == request.vars.device_serial).update(
            #    user_id=None)

            return dict(item=SUCCESS)
        except Exception as e:
            return dict(error=DB_RQ_FAILD + str(e))
    return dict(error=LACK_ARGS)


# def disableDevice(): # params: username, device_serial with user_token
#     table = 'clsb_device'
#     
#     if not table in db.tables(): return NOT_EXISTED
#     result = checkTimeOut(request.vars.username, request.vars.user_token)
#     if result != SUCCES:
#         return dict(error=result)
#     if not table in db.tables(): return NOT_EXISTED
#     
#     if request.vars and request.vars >= 2 and request.vars.username:
#             #update login time
#         updateLogTime(request.vars.username)
#         
#         try:
#             userid = db(db.clsb_user.username==request.vars.username).select(db.clsb_user._id).as_list()
#             userid = userid[0]['id']
#             
#             res = db(db[table].device_serial==request.vars.device_serial).select(db[table].in_use)
#             res = res[0]['in_use']
#             if res == True:
#                 return CB_0022 #DEVICE_IS_IN_USE
#             else:
#                 db(db[table].user_id==userid)(db[table].device_serial==request.vars.device_serial).update(status = False)
#                 return dict(item=SUCCESS)
#         except Exception as e:
#             return dict(error=DB_RQ_FAILD + str(e))
#     return dict(error=LACK_ARGS)

def unset_default_device():  # params: username, device_serial with user_token
    table = 'clsb_device'

    if not table in db.tables(): return dict(error=NOT_EXISTED)
    result = checkTimeOut(request.vars.username, request.vars.user_token)
    if result != SUCCES:
        return dict(error=result)

    if request.vars and request.vars >= 2 and request.vars.username:
        # update login time
        updateLogTime(request.vars.username)

        try:
            userid = db(db.clsb_user.username == request.vars.username).select(db.clsb_user._id).as_list()
            userid = userid[0]['id']

            res = verifyValidTime(userid)
            if res != SUCCES:
                return dict(error=res)

            new_update = db(db[table].user_id == userid)(db[table].device_serial == request.vars.device_serial).update(
                in_use=False)
            data = dict(record_id=userid, table_name=table, key_unique='user_id')
            insert_to_log_temp(data)
            return dict(item=SUCCESS)
        except Exception as e:
            return dict(error=DB_RQ_FAILD + str(e))
    return dict(error=LACK_ARGS)


# set in_user device, each user can use this service maximum 5 times.
# params: username, device_serial, user_token
# exp: /cbs/users/setDefault?username=manh&device_serial=01E4BF-121200001&user_token=d289a4507bcf7af6b779a84d53a7297a209e2d61f9dde28c
def setDefault():
    table = 'clsb_device'

    result = checkTimeOut(request.vars.username, request.vars.user_token)
    if result != SUCCES:
        return dict(error=result)
        #        return 'test'
    updateLogTime(request.vars.username)
    try:
        user = db(db.clsb_user.username == request.vars.username).select(db.clsb_user._id,
                                                                         db.clsb_user.valid_time).as_list()
        userid = user[0]['id']
        valid_time = user[0]['valid_time']
        device = db(db[table].user_id == userid)(db[table].device_serial == request.vars.device_serial).select(
            db[table].device_serial)
        if not device:
            return dict(error=CB_0013)  # device not exist

        res = verifyValidTime(userid)
        if res != SUCCES:
            return dict(error=res)

        # only one device is in use
        db(db[table].user_id == userid).update(in_use=False)
        db(db[table].user_id == userid)(db[table].device_serial == request.vars.device_serial).update(in_use=True)
        db(db.clsb_user._id == userid).update(valid_time=valid_time + 1)
        data = dict(record_id=userid, table_name='clsb_user', key_unique='username')
        insert_to_log_temp(data)
        return dict(item=SUCCESS)
    except Exception as e:
        return dict(error=DB_RQ_FAILD)


# params: username. To update logTime, used for client
def checktimeout():
    return updateLogTime(request.args(0))


from contrib.pbkdf2 import *


def resetpwd():  # email
    table = 'clsb_user'
    subject = 'Lấy lại mật khẩu tài khoản ClassBook.'
    msg = 'Classbook.vn xin kính chào quý khách.\\n\
            Quý khách đã làm mất mật khẩu và yêu cầu lấy lại mật khẩu.\
            Xin vui lòng truy cập vào tài khoản với mật khẩu tạm thời và đổi lại mật khẩu cá nhân: '
    if not table in db.tables(): return dict(error=NOT_EXISTED)

    if request.args:
        try:
            rows = db(db[table].email == request.args(0)).select(db[table].email).as_list()  # db[table].password,
            if len(rows) == 1:
                email = rows[0]['email']
                p = ''.join(random.choice(string.letters + string.digits) for x in range(10))
                pe = pbkdf2_hex(P_2_D_KEY, p)
                res = db(db[table].email == request.args(0)).update(password=pe)

                user_id = db(db[table].email == request.args(0)).select().first()['id']
                data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
                insert_to_log_temp(data)
                if res:
                    try:
                        mail.send(to=[email], subject=subject, message=msg + p)
                        return dict(item=SUCCESS)
                    except Exception as e:
                        return dict(error=e)
                else:
                    return dict(error=CB_0006)  # faillure
            else:
                return dict(error=CB_0006)  # faillure
        except Exception as e:
            return dict(error=e)


def changepwd():  # params: username, old (pwd), new (pwd), user_token
    table = 'clsb_user'
    # print request.vars

    if not table in db.tables(): return dict(error=NOT_EXISTED)

    if request.vars and len(request.vars) == 4 and not request.args:
        # result = checkTimeOut(request.vars.username, request.vars.user_token)
        # if result != SUCCES:
        #     return dict(error=result)
        userSecleted = db(db[table].username.like(request.vars.username)).select().as_list(
            db[table].password,
            db[table].username)
        if userSecleted:
            password = userSecleted[0]['password']
            username = userSecleted[0]['username']
            if password == pbkdf2_hex(P_2_D_KEY, request.vars.old):
                token = new_token(username, datetime.now())
                db(db[table].username == username).update(password=pbkdf2_hex(P_2_D_KEY, request.vars.new),
                                                          user_token=token)
                return dict(item=SUCCES, token=token)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    else:
        return dict(error=LACK_ARGS)


def changepwd_tqg():# params: username, old (pwd), new (pwd), secret
    table = 'clsb_user'
    # print request.vars
    import hashlib
    if not table in db.tables(): return dict(error=NOT_EXISTED)

    if request.vars and len(request.vars) == 4 and not request.args:
        seskey = "trungdepzai"
        secret = hashlib.md5((str(request.vars.username) + seskey)).hexdigest()
        if secret != str(request.vars.secret):
            return dict(error="Lỗi request")
        userSecleted = db(db[table].username.like(request.vars.username)).select().as_list(
            db[table].password,
            db[table].username)
        if userSecleted:
            password = userSecleted[0]['password']
            username = userSecleted[0]['username']
            if password == pbkdf2_hex(P_2_D_KEY, request.vars.old):
                token = new_token(username, datetime.now())
                db(db[table].username == username).update(password=pbkdf2_hex(P_2_D_KEY, request.vars.new),
                                                          user_token=token)
                updateLogTime(username)
                user_id = db(db[table].username == username).select().first()['id']

                return dict(item=SUCCES, token=token)
            else:
                return dict(error=PWD_ERR)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    else:
        return dict(error=LACK_ARGS)

# /cbs/users/update?username=manh&password=124&firstName=jds&lastName=dkf&email=sd@sdf.csf&phoneNumber=324&address=dkj&user_token=
def update():  # params: (obligate) username
    #  TODO: Request authentication
    if request.vars and request.vars.username:
        try:
            userSelected = db(myTable.username == request.vars.username).select().as_list()
            if len(userSelected) == 1:
                if userSelected[0]['user_token'] != request.vars.user_token:
                    return dict(error=CB_0012)
            request.vars.pop('user_token')
            username = request.vars.username
            request.vars.pop('username')
            if request.vars.password:
                request.vars.pop('password')
            if request.vars.email:
                request.vars.pop('email')
            if request.vars.fund:
                request.vars.pop('fund')
            if request.vars.valid_time:
                request.vars.pop('valid_time')
            if request.vars.status:
                request.vars.pop('status')

            res = db(myTable.username == username).update(**request.vars)
            # update login time
            updateLogTime(username)
            user_id = db(myTable.username == username).select().first()['id']
            data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
            insert_to_log_temp(data)
            return dict(item=SUCCESS)
        except Exception as e:
            return dict(error=DB_RQ_FAILD + str(e))
    return dict(error=LACK_ARGS)


def get_warranty_history():  # params email, user_token, field, field_value
    table = 'clsb_warranty_history'

    if request.vars:
        return dict(error=LACK_ARGS)
    if not request.args or len(request.args) != 4:
        return dict(error=LACK_ARGS)
        # check token
    result = checkTimeOut(request.args(0), request.args(1))
    if result != SUCCES:
        return dict(error=result)

    try:
        user_id = db(db.clsb_user.email == request.args(0)).select(db.clsb_user._id).as_list()
        user_id = user_id[0]['id']
    # return user_id
    except Exception as e:
        return dict(error=CB_0010)

    field = request.args(2)
    value = request.args(3)
    #     request.pop('field')
    #     request.pop('value')
    try:
        rows = db(db.clsb_user.email == request.args(0)) \
            (db[table][field] == value).select(db[table].ALL).as_list()
        return dict(items=rows)
    except Exception as e:
        return dict(error=DB_RQ_FAILD + str(e))


def getDownloadInfo():  # params username, user_token @return: user's product
    limit = 10
    if request.vars:
        return dict(error=LACK_ARGS)
    if not request.args or len(request.args) < 2:
        return dict(error=LACK_ARGS)
        # check token
    if len(request.args) == 3:
        limit = int(request.args[2])
    result = checkTimeOut(request.args(0), request.args(1))
    if result != SUCCES:
        return dict(error=result)
    try:
        user_id = db(db.clsb_user.username == request.args(0)).select(db.clsb_user._id).as_list()
        user_id = user_id[0]['id']
    # return user_id
    except Exception as e:
        return dict(error=CB_0010)  # username is not exist
    try:
        #                (db.clsb_product.product_creator == db.clsb_dic_creator.id)\
        #                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id)\
        #                (db.clsb_category.category_type == db.clsb_product_type.id)\
        #                (db.clsb_product.product_category == db.clsb_category.id)
        rows = db(db.clsb_download_archieve.user_id == user_id) \
            (db.clsb_download_archieve.purchase_type != "WEB_PAY") \
            (db.clsb_download_archieve.product_id == db.clsb_product._id) \
            (~db.clsb_product.product_code.like("Exer%")).select(
            db.clsb_download_archieve.product_id,
            db.clsb_download_archieve.download_time,
            db.clsb_download_archieve.device_serial,
            db.clsb_download_archieve.status,
            db.clsb_product.product_title,
            db.clsb_product.product_code,
            orderby=~db.clsb_download_archieve.download_time,
            limitby=(0, limit)).as_list()
        d = list()
        for row in rows:
            temp = dict()
            temp['download_time'] = str(row['clsb_download_archieve']['download_time'])
            temp['device_serial'] = row['clsb_download_archieve']['device_serial']
            temp['download_status'] = row['clsb_download_archieve']['status']
            temp['product_title'] = row['clsb_product']['product_title']
            temp['product_id'] = row['clsb_download_archieve']['product_id']
            temp['product_code'] = row['clsb_product']['product_code']
            d.append(temp)
        return dict(items=d)
    except Exception as e:
        return dict(error=DB_RQ_FAILD)  # +str(e))


def deposit():  # args params username, fund, user_token
    table = 'clsb_user'
    if request.vars:
        return dict(error=LACK_ARGS)
    if not request.args or len(request.args) != 3:
        return dict(error=LACK_ARGS)

    # check token
    result = checkTimeOut(request.args(0), request.args(2))

    if result != SUCCES:
        return dict(error=result)
    try:
        old_fund = db(db[table].username == request.args(0)).select(db[table].fund).as_list()[0]['fund']
        if old_fund:
            db(db[table].username == request.args(0)).update(fund=(old_fund + int(request.args(1))))
            user_id = db(db[table].username == request.args(0)).select().first()['id']
            data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
            insert_to_log_temp(data)
            auth.log_event(description='User deposit ' + request.args(1) + ' VND', origin='money-' + request.args(0))
            # print old_fund + int(request.args(1))
            return dict(item=CB_0000)
    except Exception as e:
        return dict(error=DB_RQ_FAILD + str(e))


def is_my_product():  # args params username, product_code, user_token
    table = 'clsb_user'
    if request.vars:
        return dict(error=LACK_ARGS)
    if not request.args or len(request.args) != 3:
        return dict(error=LACK_ARGS)

    # check token
    result = checkTimeOut(request.args(0), request.args(2))

    if result != SUCCES:
        return dict(error=result)
    try:
        user_id = db(db[table].username == request.args(0)).select(db[table].id).as_list()[0]['id']
        if not user_id:
            return CB - 0010  # Tên đăng nhập không tồn tại
        product_id = db(db.clsb_product.product_code == request.args(1)).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            return CB - 0001  # Không tồn tại.

        # TODO: update download's status. Implement transaction
        rows = db(db.clsb_download_archieve.user_id == user_id) \
            (db.clsb_download_archieve.product_id == product_id).select(db.clsb_download_archieve.status).as_list()
        if rows:
            return dict(item=CB_0000)  # SUCCES
        else:
            return dict(item=CB_0001)  # NOT_EXISTS
    except Exception as e:
        return dict(error=DB_RQ_FAILD + str(e))


def get_list_device():
    user_selected = db(db.clsb_user.username.like(request.args(0))).select().as_list()

    devices = db(db.clsb_device.user_id.like(user_selected[0]['id'])).select(db.clsb_device.id,
                                                                             db.clsb_device.device_serial,
                                                                             db.clsb_device.device_registration,
                                                                             db.clsb_device.device_type,
                                                                             db.clsb_device.device_name)

    device_list = list()
    for d in devices:
        device = dict()
        device['id'] = d['id']
        device['device_serial'] = d['device_serial']
        device['device_registration'] = '%s' % d['device_registration']
        device['device_type'] = d['device_type']
        device['device_name'] = d['device_name']
        device_list.append(device)

    # print device_list
    return dict(items=device_list)


def get_list_device_by_id():
    user_selected = db(db.clsb_user.username.like(request.args(0))).select().as_list()

    devices = db(db.clsb_device.user_id.like(user_selected[0]['id'])).select(db.clsb_device.id,
                                                                             db.clsb_device.device_serial,
                                                                             db.clsb_device.device_registration,
                                                                             db.clsb_device.device_type,
                                                                             db.clsb_device.device_name)

    device_list = list()
    for d in devices:
        device = dict()
        device['id'] = d['id']
        device['device_serial'] = d['device_serial']
        device['device_registration'] = '%s' % d['device_registration']
        device['device_type'] = d['device_type']
        device['device_name'] = d['device_name']
        device_list.append(device)

    return dict(items=device_list)


# args: username/product_id/token
def is_user_buy_a_book():
    if request.vars:
        return dict(error=LACK_ARGS)
    if not request.args or len(request.args) != 3:
        return dict(error=LACK_ARGS)
        # print request.args
    # check token
    result = checkTimeOut(request.args(0), request.args(2))

    if result != SUCCES:
        return dict(error=result)
    try:
        user_id = db(db[table].username == request.args(0)).select(db[table].id).as_list()[0]['id']

        buy_result = db((db.clsb30_product_history.user_id == user_id) and (
            db.clsb30_product_history.product_id == request.args(1))).select(
            db.clsb30_product_history.user_id).as_list()

        if buy_result:
            return dict(result='ok')
        else:
            return dict(result='error')
    except Exception as e:
        print str(e)


def reset_user_pwd():
    table = 'clsb_user'

    subject = 'Lấy lại mật khẩu tài khoản ClassBook.'

    if not table in db.tables(): return dict(error=NOT_EXISTED)

    if request.args:
        try:
            rows = db(db[table].email == request.args(0)).select(db[table].email).as_list()  # db[table].password,

            if len(rows) == 1:
                email = rows[0]['email']
                # gen token -> update token_reset_pwd and reset_pwd_time = now
                t = genT(request.args[0], request.now)

                res = db(db[table].email == request.args(0)).update(token_reset_pwd=t)
                if not res:
                    return dict(error="Email không tồn tại, vui lòng thử lại.")  # faillure
                res = db(db[table].email == request.args(0)).update(reset_pwd_time=request.now)

                user_id = db(db[table].email == request.args(0)).select().first()['id']
                data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
                insert_to_log_temp(data)
                if not res:
                    return dict(error="Email không tồn tại, vui lòng thử lại.")  # faillure
                if res:
                    try:
                        msg = """
                            <html>
                            <body>
                                >Bạn hoặc ai đó đã sử dụng email này để xin cấp lại mật khẩu trên Classbook Store.<br>\
                                 Để đảm bảo, xin hãy nhấn vào link dưới đây để thay đổi mật khẩu: %s . <br> \
                                Trong trường hợp bạn không xác thực, hệ thống sẽ tự động xóa yêu cầu cấp lại mật khẩu của bạn sau 24h. <br> \
                                Đây là mail tự động, xin vui lòng không reply lại.<br> \
                                Trân trọng!
                            </body>
                            </html>
                            """ % (URL(a='cbw', c='default', f='forgotpwd', host=True) + '/' + str(t))
                        msg = msg.replace('.json', '')
                        mail.send(to=[email], subject=subject, message=msg)
                        return dict(item=SUCCESS)
                    except Exception as e:
                        return dict(error=e)
                else:
                    return dict(error=CB_0006)  # faillure
            else:
                return dict(error="Email không tồn tại, vui lòng thử lại")  # faillure
        except Exception as e:
            return dict(error=e)


def verify_email():
    try:
        token = request.args[0]
        row = db(db[table].token_reset_pwd == token).select(db[table].reset_pwd_time,
                                                            db[table].email).first()
        # print row
        # compare valid reset_pwd_time (24h)
        sub_time = str(request.now - row['reset_pwd_time'])
        index = str(sub_time).find(':')

        sub_time = sub_time[:index]

        if int(sub_time) >= 24:
            return dict(result=False)

        return dict(result=True)

    except Exception as e:
        return dict(result=False)
        print str(e)


def renewpwd():  # token_rs_pwd, new (pwd)
    table = 'clsb_user'
    # print request.args
    if not table in db.tables(): return dict(result=False)

    if request.args and len(request.args) == 2 and not request.vars:

        userSecleted = db(db.clsb_user.token_reset_pwd == request.args[0]).select(
            db.clsb_user.username).first()

        if userSecleted:
            password = request.args[1]

            db(db[table].username == userSecleted['username']).update(password=pbkdf2_hex(P_2_D_KEY, password))
            res = db(db[table].username == userSecleted['username']).update(token_reset_pwd='')

            user_id = db(db[table].username == userSecleted['username']).select().first()['id']
            data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
            insert_to_log_temp(data)

            return dict(result=True)

        else:
            return dict(result=False)
    else:
        return dict(result=False)


############ gen unique ios#####################
# def get_ios_unique_key():
#     try:
#         user_name = request.vars.user_name
#         user_token = request.vars.user_token
#
#         return dict(result=True, time_valid=0, unique_key="CA942766bda2e47f", ios_id="813f2a4d8d1a882c")
#     except Exception as err:
#         print(err)
#         return dict(result=False, error=str(err))

def get_ios_unique_key():
    MAX_REQUEST = 5
    try:
        if request.vars:
            user_name = request.vars.user_name
            user_token = request.vars.user_token
        elif request.args:
            user_token = request.args[0]
        prefix = "cla2sb2ok"
        # user_name = "tiench@tinhvan.com"

        # /String s = android_id + "#" + serial_no + "#" + boot_serial_no;
        # s 813f2a4d8d1a882c#EH411500071#Medfield75939EFC

        # check token and get user id

        user = db(db.clsb_user.user_token == user_token).select()
        if len(user) == 0:
            return dict(result="Hết phiên đăng nhập", code="TOKEN_INVALID", status=False)
        user = user.first()
        user_id = user['id']
        user_name = user['username']
        # print(user_name)
        # print(user_token)
        valid_time = int(user['valid_time'])
        # if valid_time >= MAX_REQUEST:
        #     return dict(status=False, result="Tài khản của bạn đã thay đổi thiết bị quá số lần quy định", code="OUT_OF_MAX")

        md5str = gen_md5(prefix + str(user_name))

        ios_id = md5str[-16:]
        serial_no = "TVB20141014"  # gen_md5(prefix + android_id)[-12(inlove)
        boot_serial_no = "Medfield20141014"  # gen_md5(prefix + serial_no)[-16(inlove)

        s = ios_id + "#" + serial_no + "#" + boot_serial_no
        smd5 = gen_md5(s)

        t = "CA" + smd5[-10:]
        tmd5 = gen_md5(t)

        checksum = tmd5[-4:]

        uniqueid = t + checksum

        #
        ios_identifier = db(db.clsb30_ios_identifier.user_id == user_id).select()
        # db(db.clsb_user.user_token == user_token).update(valid_time=(valid_time + 1))
        if len(ios_identifier) == 0:
            new_ios = db.clsb30_ios_identifier.insert(user_id=user_id, unique_id=uniqueid,
                                                      ios_id=ios_id, requested_time=1, date_created=request.now)
            data = dict(record_id=str(new_ios), table_name='clsb30_ios_identifier', key_unique='user_id')
            insert_to_log_temp(data)
        else:
            ios_identifier = ios_identifier.first()
            requested_time = int(ios_identifier['requested_time'])
            # if requested_time >= MAX_REQUEST:
            #     return dict(status=False, result="Tài khản của bạn đã thay đổi thiết bị quá số lần quy định", code="OUT_OF_MAX")
            # else:
            requested_time += 1
            db(db.clsb30_ios_identifier.user_id == user_id).update(requested_time=requested_time)
            # valid_time += 1
            # db(db.clsb_user.id == user_id).update(valid_time=valid_time)
        return dict(status=True, time_valid=valid_time, unique_key=uniqueid, ios_id=ios_id, user_name=user_name)
    except Exception as err:
        print(err)
        return dict(status=False, result=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno),
                    code="FUNCTION_ERR")


def test_unique():
    user_name = request.args[0]
    # print(user_name)
    prefix = "cla2sb2ok"
    md5str = gen_md5(prefix + str(user_name))

    ios_id = md5str[-16:]
    serial_no = "TVB20141014"  # gen_md5(prefix + android_id)[-12(inlove)
    boot_serial_no = "Medfield20141014"  # gen_md5(prefix + serial_no)[-16(inlove)

    s = ios_id + "#" + serial_no + "#" + boot_serial_no
    smd5 = gen_md5(s)

    t = "CA" + smd5[-10:]
    tmd5 = gen_md5(t)

    checksum = tmd5[-4:]

    uniqueid = t + checksum

    return dict(user_name=user_name, uniqueid=uniqueid)


def check_elearning():
    try:
        username = request.vars.username
        last_transaction = db(db.clsb_transaction.status == 'COMPLETE').select().last()
        check_transaction = db(db.clsb_user.username.like(username)) \
            (db.clsb_user.id == db.clsb30_elearning_transaction.user_id).select()
        if len(check_transaction) == 0:
            return dict(check=False)
        else:
            if last_transaction['id'] == check_transaction.last()[db.clsb30_elearning_transaction.transaction_id]:
                return dict(check=True, message=check_transaction.last()[db.clsb30_elearning_transaction.description])
            else:
                return dict(check=False, message=check_transaction.last()[db.clsb30_elearning_transaction.description])
    except Exception as ex:
        return dict(check=False, message=str(ex))


def check_tvt_code(code):
    try:
        code = code.strip().upper()
        select_code = db(db.clsb30_tvt_code.promotion_code.like(code)).select()
        if len(select_code) == 0:
            return dict(result=False, mess="Mã giảm giá không hợp lệ", code=code)
        return dict(result=True)
    except Exception as err:
        return dict(result=False, mess=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def sum_pay_tqg(username):
    try:
        # from datetime import datetime
        # datestart = datetime.strptime("2016-01-01", "%Y-%m-%d")
        # sum_nl = db.clsb_transaction.face_value.sum()
        # total_nl = db(db.clsb_transaction.user_id == db.clsb_user.id)\
        #     (db.clsb_user.username.like(username))\
        #     (db.clsb_transaction.status == "COMPLETE")\
        #     (db.clsb_transaction.created_on >= datestart)\
        #         (db.clsb_transaction.site == "TQG").select(sum_nl).first()[sum_nl]
        # if total_nl is None:
        #     total_nl = 0
        # sum_card = db.clsb30_tqg_card_log.card_value.sum()
        # total_card = db(db.clsb30_tqg_card_log.user_id == db.clsb_user.id)\
        #     (db.clsb_user.username.like(username))\
        #     (db.clsb30_tqg_card_log.created_on >= datestart).select(sum_card).first()[sum_card]
        # if total_card is None:
        #     total_card = 0
        #
        # sum_tranfer = db.clsb30_tqg_log_tranfer.fund.sum()
        # total_tranfer = db(db.clsb30_tqg_log_tranfer.user_id == db.clsb_user.id)\
        #     (db.clsb_user.username.like(username))\
        #     (db.clsb30_tqg_log_tranfer.status.like("SUCCESS"))\
        #     (db.clsb30_tqg_log_tranfer.created_on >= datestart).select(sum_tranfer).first()[sum_tranfer]
        # if total_tranfer is None:
        #     total_tranfer = 0
        # return dict(total=total_nl + total_card + total_tranfer, total_nl=total_nl,
        #             total_card=total_card, total_tranfer=total_tranfer)
        sum_tranfer = db.clsb30_tvt_log.before_discount.sum()
        total_tranfer = db(db.clsb30_tvt_log.user_id == db.clsb_user.id)\
            (db.clsb_user.username.like(username)).select(sum_tranfer).first()[sum_tranfer]
        if total_tranfer is None:
            total_tranfer = 0
        return dict(total=total_tranfer)
    except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def sum_discount(username):
    try:
        sum_tranfer = db.clsb30_tvt_log.after_discount.sum()
        total_tranfer = db(db.clsb30_tvt_log.user_id == db.clsb_user.id)\
            (db.clsb_user.username.like(username)).select(sum_tranfer).first()[sum_tranfer]
        if total_tranfer is None:
            total_tranfer = 0
        return dict(total=total_tranfer)
    except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def sum_pay():
    return sum_pay_tqg(request.vars.username)


def tranfer_to_tqg():
    dc_fund = 0
    try:
        username = request.vars.username
        select_transaction = db(db.clsb_transaction.site == "TQG")\
            (db.clsb_user.id == db.clsb_transaction.user_id)\
            (db.clsb_user.username.like(username)).select()
        if len(select_transaction) == 0:
            return dict(error="Không tìm thấy giao dịch")
        select_transaction = select_transaction.last()
        user_id = select_transaction[db.clsb_user.id]
        username = db(db.clsb_user.id == user_id).select().first()['username']
        discount_code = select_transaction[db.clsb_transaction.discount_code]
        fund = int(select_transaction(db.clsb_transaction.face_value))
        use_discount = False
        if discount_code != "":
            check_code = check_tvt_code(discount_code)
            if check_code['result']:
                use_discount = True
            else:
                use_discount = False
        sum_pay = int(sum_pay_tqg(username)['total'])
        dc_fund = fund
        if use_discount:
            if sum_pay + fund < 750000:
                dc_fund = int(fund * 1.12)
            else:
                if sum_pay >= 750000:
                    dc_fund = int(fund * 1.34)
                else:
                    dc_fund = int((sum_pay + fund - 750000) * 1.334 + (1000000 - int(sum_discount(username)['total'])))
        tranfer = tranfer_fund(username, dc_fund)
        if tranfer['type'] == 'success':
            new_fund = int(select_transaction[db.clsb_user.fund]) - fund
            db(db.clsb_user.id == user_id).update(fund=new_fund)
            db.clsb30_tqg_log_tranfer.insert(user_id=user_id,
                                             fund=dc_fund,
                                             status="SUCCESS",
                                             description="nap_tien")
            if use_discount:
                db.clsb30_tvt_log.insert(user_id=user_id, action_type="NL",
                                        before_discount=fund,
                                        after_discount=dc_fund,
                                        time_used=datetime.now(),
                                        discount_code=discount_code)
            return dict(result=True, fund=dc_fund)
        db.clsb30_tqg_log_tranfer.insert(user_id=user_id,
                                         fund=dc_fund,
                                         status="FAIL",
                                         description=tranfer['value'])
        return dict(error="Thất bại")
    except Exception as ex:
        db.clsb30_tqg_log_tranfer.insert(user_id=user_id,
                                         fund=dc_fund,
                                         status="FAIL",
                                         description=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex))


def tranfer_fund(username, fund):
    try:
        import requests
        import json
        url = 'http://thiquocgia.vn/userpanel/service_ajax.php'
        sesskey = "trungdepzai"
        data = dict(u=username, s=md5_string(sesskey + username), f=fund, type="tranfer_fund")
        r = requests.post(url, data=data, allow_redirects=True)
        return json.loads(r.content)
    except Exception as ex:
        return dict(type='error', value=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def tranfer_to_third():
    try:
        service_tranfer = request.vars.service_tranfer
        username = request.vars.username
        select_transaction = db(db.clsb_user.id == db.clsb_transaction.user_id)\
            (db.clsb_user.username.like(username)).select()
        if len(select_transaction) == 0:
            return dict(error="Không tìm thấy giao dịch")
        select_transaction = select_transaction.last()
        user_id = select_transaction[db.clsb_user.id]
        username = db(db.clsb_user.id == user_id).select().first()['username']
        fund = int(select_transaction(db.clsb_transaction.face_value))
        tranfer = tranfer_third(username, fund, service_tranfer)
        if tranfer['type'] == 'success':
            new_fund = int(select_transaction[db.clsb_user.fund]) - fund
            db(db.clsb_user.id == user_id).update(fund=new_fund)
            db.clsb30_tqg_log_tranfer.insert(user_id=user_id,
                                             fund=fund,
                                             status="SUCCESS",
                                             description="nap_tien")
            return dict(result=True, fund=fund)
        db.clsb30_tqg_log_tranfer.insert(user_id=user_id,
                                         fund=fund,
                                         status="FAIL",
                                         description=tranfer['value'])
        return dict(error="Thất bại", service=service_tranfer)
    except Exception as ex:
        db.clsb30_tqg_log_tranfer.insert(user_id=user_id,
                                         fund=fund,
                                         status="FAIL",
                                         description=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex))


def tranfer_third(username, fund, service_tranfer):
    try:
        return update_fund_vstep(username, fund)
        # import requests
        # import json
        # url = service_tranfer
        # sesskey = "clsb"
        # data = dict(u=username, s=md5_string(sesskey + username), f=fund, type="tranfer_fund")
        # r = requests.post(url, data=data, allow_redirects=True, verify=False)
        # # return dict(type='error', value=str(r.content))
        # resultdata = json.loads(r.content)
        # return resultdata
    except Exception as ex:
        return dict(type='error', value=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def test_update_vstep():
    return update_fund_vstep(request.args[0], request.args[1])


def update_fund_vstep(username, fund):
    import pymysql
    try:
        HOST = "localhost"
        USER = "vstep"
        PASS = "123vstep456"
        DATABASE = "ulisibt"
        db = pymysql.connect(host=HOST, user=USER, passwd=PASS, db=DATABASE)
        cur = db.cursor()
        sql = "UPDATE mdl_user set fund = fund + " + str(fund) + " WHERE username = \"" + username + "\""
        cur.execute(sql)
        db.commit()
        db.close()
        return dict(type='success', value="Thành công")
    except Exception as ex:
        return dict(type='error', value=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def md5_string(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def tqg_change_pass():
    table = 'clsb_user'
    # print request.vars
    import hashlib
    if not table in db.tables(): return dict(error=NOT_EXISTED)

    if request.vars and not request.args:
        seskey = "trungdepzai"
        secret = hashlib.md5((str(request.vars.username) + seskey)).hexdigest()
        if secret != str(request.vars.secret):
            return dict(error="Lỗi request")
        userSecleted = db(db[table].username.like(request.vars.username)).select().as_list(
            db[table].password,
            db[table].username)
        if userSecleted:
            username = userSecleted[0]['username']
            token = new_token(username, datetime.now())
            db(db[table].username == username).update(password=pbkdf2_hex(P_2_D_KEY, request.vars.new),
                                                          user_token=token)
            updateLogTime(username)
            user_id = db(db[table].username == username).select().first()['id']

            return dict(item=SUCCES, token=token)
        else:
            return dict(error=USER_NAME_NOT_EXIST)
    else:
        return dict(error=LACK_ARGS)
