# coding: utf8
# try something like

# @author: hant 27-02-2013

from contrib.pbkdf2 import *
from datetime import *
import string
import random
import os
import re
import fs.path
import pdf2dev
import json
import requests

SUCCESS = CB_0000  # cbMsg.CB_0000
EXISTENT = CB_0005  # cbMsg.CB_0005
LACK_ARGS = CB_0002  # cbMsg.CB_0002
FAILURE = CB_0006  # cbMsg.CB_0006
DB_RQ_FAILD = CB_0003  # cbMsg.CB_0003
DATA_ERROR = CB_0007  # cbMsg.CB_0007
PWD_ERR = CB_0008
DISABLE = CB_0009
NOT_EXIST = CB_0001
USER_NAME_NOT_EXIST = CB_0010
INVALID_DEVICE_SERIAL = CB_0016
P_2_D_KEY = 'c-p3d*b'

myTable = db.clsb_user
table = 'clsb_user'
P_2_D_KEY = 'c-p3d*b'
GOOGLE = "google"
FACEBOOK = "facebook"


def genT(name, time):
    #    name = request.args(0)
    if not table in db.tables(): return dict(error=NOT_EXIST)
    if name:
        s = os.urandom(10)  # ''.join(random.choice(string.letters + string.digits) for x in range(10))
        t = pbkdf2_hex(name, s)
        try:
            # db[table].update_or_insert(db[table].username == name, user_token = t, lastLoginTime = time)
            myTable.update_or_insert(myTable.username == name, lastLoginTime=time)
            token = db(db.clsb_user.username == name).select(db.clsb_user.user_token).first()['user_token']
            if token is None or token == "":
                db[table].update_or_insert(db[table].username == name, user_token=t, lastLoginTime=time)
                token = t
            return token
            # return t
        except Exception as e:
            return DB_RQ_FAILD + str(e) + " on line " + str(sys.exc_traceback.tb_lineno)
    else:
        return LACK_ARGS


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
            request.vars.pop('password')
            request.vars.update(password=pwd)
            if request.vars.lastName == "":
                request.vars.update(lastName="User")
            if request.vars.firstName == "":
                request.vars.update(firstName="Guest")
            myTable.insert(**request.vars)
            return dict(item=SUCCESS)
        except Exception as e:
            print str(e)
            if (str(e).find("Duplicate") >= 0) & (str(e).find("username") >= 0):
                return dict(error="Tài khoản đã tồn tại")
            if (str(e).find("Duplicate") >= 0) & (str(e).find("email") >= 0):
                return dict(error="Email này đã bị được dùng để đăng kí")
            return dict(error=DB_RQ_FAILD)
    elif request.args and len(request.args) >= nbargsrequired and not request.vars:
        if db(myTable.username.like(request.args(0))).select() or db(myTable.email.like(request.args(4))).select():
            return dict(error=EXISTENT)
        else:
            lname = request.args(3)
            fname = request.args(2)
            if lname == "":
                lname = "User"
            if fname == "":
                fname = "Guest"
            myTable.update_or_insert(
                username=request.args(0), password=pbkdf2_hex(P_2_D_KEY, request.args(1)),
                lastLoginTime=request.now, firstName=lname,
                lastName=fname, email=request.args(4),
                phoneNumber=request.args(5), address=(request.args(6) or "ND"), district=request.args(7))
            return dict(item=SUCCESS)
    else:
        return dict(error=LACK_ARGS)


def authentication_gg():  # param: access_token
    try:
        if len(request.args) > 0:
            access_token = request.args[0]
        if len(request.vars) > 0:
            access_token = request.vars.access_token
        url_info = "https://www.googleapis.com/oauth2/v1/userinfo?access_token=" + access_token
        get_data = urllib2.urlopen(url_info)
        get_data = json.loads(get_data.read())
        if get_data.has_key('error'):
            return dict(error=CB_0026)
        first_name = get_data['given_name']
        last_name = get_data['family_name']
        email = get_data['email']
        username = email + ".gg"
        check_user_exit = db(db.clsb_user.username == username).select()
        if len(check_user_exit) > 0:
            t = genT(str(username), request.now)
            return dict(token=t, username=username, display=check_user_exit.first()['firstName'])
        new_user = db.clsb_user.insert(username=username,
                                       password=pbkdf2_hex(P_2_D_KEY, "clsb_gg"),
                                       lastLoginTime=request.now,
                                       firstName=first_name,
                                       lastName=last_name,
                                       email=(email + ".gg"),
                                       type_user=GOOGLE)
        t = genT(str(username), request.now)
        return dict(token=t, username=username, display=first_name)
    except Exception as err:
        print(str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno), url=url_info)


def authentication_fb():  # param: access_token
    try:
        if len(request.args) > 0:
            access_token = request.args[0]
        if len(request.vars) > 0:
            access_token = request.vars.access_token
        url_info = "https://graph.facebook.com/me?access_token=" + access_token
        # print(url_info)
        get_data = urllib2.urlopen(url_info)
        get_data = json.loads(get_data.read())
        if get_data.has_key('error'):
            return dict(error=CB_0025)
        id = get_data['id']
        name = get_data['name']
        if 'first_name' in get_data:
            first_name = get_data['first_name']
            last_name = get_data['last_name']
        else:
            first_name = ""
            last_name = name
        check_user_exit = db(db.clsb_user.username == id).select()
        if len(check_user_exit) > 0:
            t = genT(str(id), request.now)
            return dict(token=t, username=id, display=check_user_exit.first()['firstName'])
        new_user = db.clsb_user.insert(username=id,
                                       password=pbkdf2_hex(P_2_D_KEY, "clsb_fb"),
                                       lastLoginTime=request.now,
                                       firstName=first_name,
                                       lastName=last_name,
                                       email=id,
                                       type_user=FACEBOOK)
        data = dict(record_id=new_user['id'], table_name='clsb_user', key_unique='username')
        t = genT(str(id), request.now)
        return dict(token=t, username=id, display=(first_name + last_name))
    except Exception as err:
        print(str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(err))


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
                                                                                        db.clsb_device.in_use)
                res = dict()
                #                res['id'] = userSelected[0]['id']
                res['username'] = userSelected[0]['username']
                # res['password'] = userSelected[0]['password']
                res['lastLoginTime'] = '%s' % userSelected[0]['lastLoginTime']
                res['firstName'] = userSelected[0]['firstName']
                res['lastName'] = userSelected[0]['lastName']
                res['email'] = userSelected[0]['email']
                res['phoneNumber'] = userSelected[0]['phoneNumber']
                res['address'] = userSelected[0]['address']
                res['valid_time'] = userSelected[0]['valid_time']
                res['valid_time_message'] = "Bạn đã thay đổi thiết bị mặc định " \
                                            + str(userSelected[0]['valid_time']) \
                                            + " lần.\nBạn còn lại " + str(
                    MAX_VALID_TIME_SET_DEFAULT - userSelected[0]['valid_time']) \
                                            + " lần thay đổi thiết bị mặc định."
                res['fund'] = userSelected[0]['fund']
                if devices:
                    i = 0
                    tmp = ''
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
                        if device_uid != last_uid:
                            #                             if i != 0:
                            tmp += '#'
                            tmp += d['device_serial']

                        i += 1

                    res['devices'] = tmp  # ""+tmp[0:]
                    res['device_in_use'] = d_in_use
                #                     print "------"
                #                     print res['devices']
                else:
                    res['devices'] = ''
                    res['device_in_use'] = ''

                if re.search(r'^#', res['devices']):
                    res['devices'] = res['devices'][1:]

                # print res['devices']

                return dict(items=res)
            else:
                return dict(error=USER_NAME_NOT_EXIST)
        except Exception as e:
            return dict(error=DB_RQ_FAILD + str(e))
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
def adddevice():
    table = 'clsb_device'
    if not table in db.tables(): return dict(error=NOT_EXISTED)

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
            userid = db(db.clsb_user.username == username).select(db.clsb_user._id).as_list()
            if len(userid) != 1:
                return dict(error=DATA_ERROR)

                # limite the maximum nb of device to 3 devices
            #             result = verifyNbDevice(userid[0]['id'])
            #             if result != SUCCES:
            #                 return dict(error=result)

            request.vars.pop('username')
            request.vars.pop('user_token')
            request.vars.update(user_id=userid[0]['id'])

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
            # if not, then this is the new device, insert it and add some cash
            if not device:
                db[table].insert(**request.vars)
                # add cash to user's account
                fund(username)
                return dict(item=SUCCESS)
                # else this devices is the old one, check if this is deleted by someone or not.
            else:
                row = db(db.clsb_device.device_serial == device[0]['device_serial']).select(db.clsb_device.last_uid,
                                                                                            db.clsb_device.user_id).as_list()
                last_uid = row[0]['last_uid']
                device_uid = row[0]['user_id']
                #                 print userid[0]['id']
                #                 print device_uid
                #                 print device[0]['device_serial']
                # this is deleted by someone then other can add it. IF YOU CHANGE THIS FUNC PLS VALIDATE THE FUNC DELETE_DEVICE
                if device_uid == last_uid:
                    db(db.clsb_device.device_serial == request.vars.device_serial).update(user_id=userid[0]['id'],
                                                                                          last_uid=None)
                    #                     print "add"
                    return dict(item=SUCCESS)
                else:
                    #                     print "dont add"
                    return dict(error=CB_0018)  # DEVICE_EXISTED

        except Exception as e:
            return dict(error=DB_RQ_FAILD + str(e))
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
            userid = db(db.clsb_user.username == request.vars.username).select(db.clsb_user._id).as_list()
            userid = userid[0]['id']

            res = db(db[table].device_serial == request.vars.device_serial).select(db[table].in_use)
            res = res[0]['in_use']
            if res == True:
                return dict(error=CB_0022)  # DEVICE_IS_IN_USE
            else:
                #                 db(db[table].user_id==userid)(db[table].device_serial==request.vars.device_serial).delete()
                res = db(db[table].user_id == userid)(db[table].device_serial == request.vars.device_serial).update(
                    last_uid=userid)
                # print res
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

            db(db[table].user_id == userid)(db[table].device_serial == request.vars.device_serial).update(in_use=False)
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

    if not table in db.tables(): return dict(error=NOT_EXISTED)

    if request.vars and len(request.vars) == 4 and not request.args:
        result = checkTimeOut(request.vars.username, request.vars.user_token)
        if result != SUCCES:
            return dict(error=result)
        userSecleted = db(db[table].username.like(request.vars.username)).select().as_list(
            db[table].password,
            db[table].username)
        if userSecleted:
            password = userSecleted[0]['password']
            username = userSecleted[0]['username']
            if password == pbkdf2_hex(P_2_D_KEY, request.vars.old):
                db(db[table].username == username).update(password=pbkdf2_hex(P_2_D_KEY, request.vars.new))
                updateLogTime(username)

                return dict(item=SUCCES)
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
            result = checkTimeOut(request.vars.username, request.vars.user_token)
            if result != SUCCES:
                return dict(error=result)
            # pop out all field that are not allowed to modify by user when using this func
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
    #        return user_id
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
    if request.vars:
        return dict(error=LACK_ARGS)
    if not request.args or len(request.args) != 2:
        return dict(error=LACK_ARGS)
    # check token
    result = checkTimeOut(request.args(0), request.args(1))
    if result != SUCCES:
        return dict(error=result)
    try:
        user_id = db(db.clsb_user.username == request.args(0)).select(db.clsb_user._id).as_list()
        user_id = user_id[0]['id']
    #        return user_id
    except Exception as e:
        return dict(error=CB_0010)  # username is not exist
    try:
        #                (db.clsb_product.product_creator == db.clsb_dic_creator.id)\
        #                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id)\
        #                (db.clsb_category.category_type == db.clsb_product_type.id)\
        #                (db.clsb_product.product_category == db.clsb_category.id)
        rows = db(db.clsb_download_archieve.user_id == user_id) \
            (db.clsb_download_archieve.product_id == db.clsb_product._id).select(db.clsb_download_archieve.product_id,
                                                                                 db.clsb_download_archieve.download_time,
                                                                                 db.clsb_download_archieve.device_serial,
                                                                                 db.clsb_download_archieve.status,
                                                                                 db.clsb_product.product_title,
                                                                                 db.clsb_product.product_code,
                                                                                 orderby=~db.clsb_download_archieve.download_time).as_list()
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


@request.restful()
def check_user_buy_product():
    """
        vars : device_serial, product_code, token
    """
    response.view = 'generic.json'

    def GET(*args, **vars):

        return dict(error="Trang này không tồn tại!")

    def POST(*args, **vars):

        try:
            if len(vars) != 3:
                return dict(result=False, mess='Yều cầu không hợp lệ.', code='TOKEN_ERROR')

            device_serial = vars['device_serial']
            product_code = vars['product_code']
            token = vars['token']

            check_ios = db(db.clsb30_ios_identifier.unique_id == device_serial).select()
            # if len(check_ios) > 0 and server_version() == 'server_mp':
            #     return dict(result=True, mess='Đã mua.', code='BOUGHT')

            user_info = db(db.clsb_user.user_token == token).select(db.clsb_user.username, db.clsb_user.id).as_list()

            if len(user_info) == 0:
                return dict(result=False,
                            mess='Hết phiên làm việc hoặc tài khoản được đăng nhập trên thiết bị khác, vui lòng đăng nhập lại.',
                            code='TOKEN_ERROR')

            user_info = user_info[0]

            device_info = db(db.clsb_device.device_serial == device_serial).select(db.clsb_device.user_id).as_list()

            if len(device_info) == 0:
                return dict(result=False, mess='Thiết bị chưa được đăng kí', code='DEVICE_UNREGISTER')

            device_info = device_info[0]
            if device_info['user_id'] is None or device_info['user_id'] == 'None':
                return dict(result=False, mess='Thiết bị chưa được đăng kí', code='DEVICE_UNREGISTER')

            if device_info['user_id'] != user_info['id']:
                return dict(result=False,
                            mess='Thiết bị không thuộc sở hữu của tài khoản ' + str(user_info['username']) + '.',
                            code='DEVICE_REGISTERED')

            product_info = db(db.clsb_product.product_code == product_code).select(db.clsb_product.id,
                                                                                   db.clsb_product.product_title).as_list()

            if len(product_info) == 0:
                return dict(result=False, mess='Sản phẩm không tồn tại', code="PRODUCT_NOT_EXITS")

            product_info = product_info[0]
            # check addition
            info_addition = dict()
            # media
            info_addition['has_media'] = check_media(product_code)['check']
            media_price_info = db(db.clsb30_product_extend.product_id == product_info['id']) \
                (db.clsb30_product_extend.extend_id == 1).select()
            if len(media_price_info) > 0:
                info_addition['media_price'] = media_price_info.first()['price']
            else:
                info_addition['media_price'] = settings.fake_fund_media
            check_buy = db(db.clsb30_media_history.product_id == product_info['id'])(
                db.clsb30_media_history.user_id == user_info['id']).select()
            if len(check_buy) > 0 or info_addition['media_price'] == 0:
                info_addition['buy_media'] = True
            else:
                info_addition['buy_media'] = False
            # quiz
            price_quiz = db(db.clsb30_product_extend.product_id == product_info['id']) \
                (db.clsb30_product_extend.extend_id == 2).select()
            if len(price_quiz) == 0:
                info_addition['quiz_price'] = settings.fake_fund_quiz
            else:
                info_addition['quiz_price'] = price_quiz.first()['price']
            hasquiz = db(db.clsb_product.product_code == 'Exer' + product_code).select()
            if len(hasquiz) > 0:
                info_addition['has_quiz'] = True
                quiz_id = hasquiz.first()['id']
                check_quiz = db(db.clsb30_product_history.product_id == quiz_id) \
                    (db.clsb30_product_history.user_id == user_info['id']).select()
                if len(check_quiz) > 0 or info_addition['quiz_price'] == 0:
                    info_addition['buy_quiz'] = True
                else:
                    info_addition['buy_quiz'] = False
                pass
            else:
                info_addition['has_quiz'] = False
                info_addition['buy_quiz'] = False
            pass
            info_addition['device_support'] = settings.device_support

            # check user buy product?

            download_archive = db(db.clsb_download_archieve.user_id == user_info['id'])(
                db.clsb_download_archieve.product_id == product_info['id']).select(
                db.clsb_download_archieve.id).as_list()

            if len(download_archive) > 0:
                return dict(result=True, mess='Đã mua', code='BOUGHT', addition=info_addition)

            download_history = db(db.clsb30_product_history.user_id == user_info['id'])(
                db.clsb30_product_history.product_id == product_info['id']).select(
                db.clsb30_product_history.id).as_list()

            if len(download_history) > 0:
                return dict(result=True, mess='Đã mua.', code='BOUGHT', addition=info_addition)

            return dict(result=False,
                        mess='Sản phẩm ' + product_info['product_title'] + 'chưa được mua cho tài khoản' + user_info[
                            'username'], code='NOT_YET_BUY')
        except Exception as e:
            print e

    return locals()


def check_valid_fund():  # token, pay
    if len(request.args) < 2:
        return dict(result=False, mess="Tham số không hợp lệ", code="INVALID_PARAMS")
    token = request.args[0]
    pay = int(request.args[1])
    user_info = db(db.clsb_user.user_token == token).select()
    if len(user_info) == 0:
        return dict(result=False, mess="Hết thời gian đăng nhập. Vui lòng đăng nhập lại", code="INVALID_TOKEN")
    user = user_info.first()
    if int(user['fund']) >= pay:
        return dict(result=True, mess="Hợp lệ", code="SUCCESS")
    else:
        return dict(result=False, mess="Tài khoản của bạn không đủ để thanh toán", code="NOT_ENOUGHT_FUND")


def confirm_buy_classbookapp():  # token, confirm_pass, pay
    if len(request.args) < 3:
        return dict(result=False, mess="Tham số không hợp lệ", code="INVALID_PARAMS")
    token = request.args[0]
    confirm_pass = request.args[1]
    pay = int(request.args[2])
    user_info = db(db.clsb_user.user_token == token).select()
    if len(user_info) == 0:
        return dict(result=False, mess="Hết thời gian đăng nhập. Vui lòng đăng nhập lại", code="INVALID_TOKEN")
    user = user_info.first()
    if user['password'] == pbkdf2_hex(P_2_D_KEY, confirm_pass):
        if int(user['fund']) >= pay:
            return dict(result=True, mess="Hợp lệ", code="SUCCESS")
        else:
            return dict(result=False, mess="Tài khoản của bạn không đủ để thanh toán", code="NOT_ENOUGHT_FUND")
    else:
        return dict(result=False, mess="Mật khẩu xác nhận không đúng", code="INVALID_PASSWORD")


def check_available_payment():  # token, pay:
    try:
        token = request.args[0]
        pay = int(request.args[1])
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) == 0:
            return dict(err="Hết phiên đăng nhập", code="INVALID_LOGIN")
        user = user.first()
        user_fund = int(user['fund'])
        if user_fund < pay:
            return dict(err="Tài khoản của bạn không đủ để thực hiện thanh toán", code="NOT_ENOUGHT_FUND")
        return dict(result="Hợp lệ", code="AVAILABLE")
    except Exception as err:
        return dict(err=err, code="UNDEFINE")


def increase_regtimes_device():
    if request.vars and 'user_token' in request.vars:
        token = request.vars.user_token
        user = db(db.clsb_user.user_token == token).select()
        if len(user) == 0:
            return dict(result=False, code="INVALID_TOKEN", error="INVALID_TOKEN: Token không hợp lệ!")
        user = user.first()
        if int(user['valid_time']) >= 5:
            return dict(result=False, code="LIMIT_VALID_TIME", error="LIMIT_VALID_TIME: Đăng kí đủ số lần cho phép!")
        try:
            db(db.clsb_user.user_token == token).update(valid_time=(user['valid_time'] + 1))
            return dict(result=True)
        except Exception as err:
            return dict(result=False, code="EXCEPTION", error="EXCEPTION: " + str(err))


def check_valid_fund():  # token, price
    token = request.args[0]
    price = request.args[1]
    user = db(db.clsb_user.user_token == token).select()
    if len(user) == 0:
        return dict(result=False, code="TOKEN_INVALID", mess="Hết phiên đăng nhập")
    user = user.first()
    if int(user['fund']) < int(price):
        return dict(result=False, code="FUND_INVALID", mess="Tài khoản không đủ")
    return dict(result=True)


def check_valid_token():
    try:
        username = request.vars.username
        user_token = request.vars.user_token
        check = timeOut(username, user_token)
        if "CB_0012" in check:
            return dict(item=dict(code="CB_0012",
                                  message="CB_0012: Tài khoản đã đăng nhập ở nơi khác, vui lòng đăng nhập lại!"))
        elif "CB_0011" in check:
            return dict(item=dict(code="CB_0011", message=CB_0011))
        elif "OK" in check:
            return dict(item=dict(code="CB_0000", message=CB_0000))
        else:
            return dict(item=dict(code="CB_0010", message=CB_0010))
    except Exception as err:
        return dict(item=dict(code="CB_0004", message=CB_0004 + " " + str(err)))


def add_support_email():
    try:
        data = dict()
        email = request.vars.email
        data['email'] = email
        if 'from_site' in request.vars:
            data['from_site'] = request.vars.from_site
        if '@' in email and '.' in email:
            select_email = db(db.clsb30_support_email.email == email).select()
            if len(select_email) > 0:
                return dict(error="Email đã được đăng kí rồi", result=False)
            else:
                if 'from_site' in request.vars:
                    db.clsb30_support_email.insert(email=email, from_site=request.vars.from_site)
                else:
                    db.clsb30_support_email.insert(email=email)
                return dict(result=True)
        else:
            return dict(error="Email không hợp lệ", result=False)
    except Exception as e:
        return dict(error=str(e) + " on line " + str(sys.exc_traceback.tb_lineno), result=False)


def payment():
    try:
        user_token = request.vars.user_token
        fund = int(request.vars.fund)
        user = db(db.clsb_user.user_token.like(user_token)).select()
        if len(user) == 0:
            return dict(error=CB_0012)
        user = user.first()
        old_fund = int(user['fund'])
        if old_fund < fund:
            return dict(error=CB_0023, old_fund=old_fund)
        new_fund = old_fund - fund
        db(db.clsb_user.id == user['id']).update(fund=new_fund)
        return dict(result="SUCCESS")
    except Exception as e:
        return dict(error=str(e) + " on line " + str(sys.exc_traceback.tb_lineno), result=False)


def check_username_exist():
    try:
        username = request.vars.username
        select_username = db(db.clsb_user.username.like(username)).select()
        if len(select_username) > 0:
            return dict(result=True)
        else:
            return dict(result=False)
    except Exception as ex:
        return dict(result=False, error=ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def delete_trunglb():
    try:
        db(db.clsb_user.username.like("trunglbict@gmail.com")).delete()
        return "SUCCESS"
    except Exception as ex:
        return dict(result=False, error=ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))


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


def thiquocgia_tranfer_fund():
    try:
        user_token = request.vars.user_token
        base_fund = int(request.vars.fund)
        use_discount = False
        fund = base_fund
        if "discount_code" in request.vars:
            discount_code = request.vars.discount_code
            if discount_code != "":
                check_code = check_tvt_code(discount_code)
                if check_code['result']:
                    use_discount = True
                    fund = int(request.vars.real_fund)
                else:
                    return dict(error="CB", mess=check_code['mess'])
        user = db(db.clsb_user.user_token == user_token).select()
        if len(user) == 0:
            return dict(error="Hết phiên đăng nhập, vui lòng đăng nhập lại")
        user = user.first()
        sum_pay = int(sum_pay_tqg(user['username'])['total'])
        if fund > int(user['fund']):
            db.clsb30_tqg_log_tranfer.insert(user_id=user['id'],
                                             fund=base_fund,
                                             status="FAIL",
                                             description="Không đủ tiền")
            return dict(error="Số tiền trong tài khoản Classbook không đủ")
        if use_discount:
            if sum_pay > 750000:
                fund = int(base_fund * 0.75)
            else:
                fund = int(base_fund * 0.9)
                if sum_pay + base_fund * 0.9 >= 750000:
                    base_fund = int((sum_pay + base_fund * 0.9 - 750000) * 1.334 + \
                                (1000000 - int(sum_discount(user['username'])['total'])))
        tranfer = tranfer_fund(user['username'], base_fund)
        if tranfer['type'] == 'success':
            new_fund = int(user['fund']) - fund
            db(db.clsb_user.id == user['id']).update(fund=new_fund)
            db.clsb30_tqg_log_tranfer.insert(user_id=user['id'],
                                             fund=base_fund,
                                             status="SUCCESS",
                                             description="chuyen_tien")
            if use_discount:
                db.clsb30_tvt_log.insert(user_id=user['id'],
                                        action_type="TRANFER",
                                        before_discount=fund,
                                        after_discount=base_fund,
                                        time_used=datetime.now(),
                                        discount_code=discount_code)
            return dict(result=True, base_fund=base_fund, fund=fund)
        db.clsb30_tqg_log_tranfer.insert(user_id=user['id'],
                                         fund=base_fund,
                                         status="FAIL",
                                         description=tranfer['value'])
        return dict(error="Chuyển tiền không thành công")
    except Exception as ex:
        return dict(error=ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def tranfer_fund(username, fund):
    try:
        url = 'http://thiquocgia.vn/userpanel/service_ajax.php'
        sesskey = "trungdepzai"
        data = dict(u=username, s=md5_string(sesskey + username), f=fund, type="tranfer_fund")
        r = requests.post(url, data=data, allow_redirects=True)
        return json.loads(r.content)
    except Exception as ex:
        return dict(type='error', value=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def md5_string(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def tqg_tranfer_pay():
    try:
        user_token = request.vars.user_token
        purchase_type = request.vars.purchase_type
        package = request.vars.package
        email = request.vars.email
        pack_type = request.vars.pack_type
        fund = int(request.vars.fund)
        select_user = db(db.clsb_user.user_token.like(user_token)).select()
        if len(select_user) == 0:
            return dict(error="Vui lòng đăng nhập lại")
        user = select_user.first()
        if fund > int(user['fund']):
            db.clsb30_tqg_log_tranfer.insert(user_id=user['id'],
                                             fund=fund,
                                             status="FAIL",
                                             description="Không đủ tiền")
            return dict(error="Số tiền trong tài khoản Classbook không đủ")
        if purchase_type == "gift":
            url = 'http://thiquocgia.vn/userpanel/gift_ajax2.php'
            data = dict(email=email, gift=package, sesskey="trungdepzai", type=pack_type, username=user['username'],
                        token=user_token, fund=fund)
            r = requests.post(url, data=data, allow_redirects=True)
            result = json.loads(r.content)
        else:
            url = 'http://thiquocgia.vn/userpanel/service2.php'
            data = dict(package_code=package, sesskey="trungdepzai", type=pack_type, username=user['username'],
                        token=user_token, fund=fund)
            r = requests.post(url, data=data, allow_redirects=True)
            result = json.loads(r.content)
        if result['type'] == "success":
            new_fund = int(user['fund']) - fund
            db(db.clsb_user.id == user['id']).update(fund=new_fund)
            db.clsb30_tqg_log_tranfer.insert(user_id=user['id'],
                                             fund=fund,
                                             status="SUCCESS")
            return dict(result=True)
        elif result['type'] == "charge":
            new_fund = int(user['fund']) - fund
            db(db.clsb_user.id == user['id']).update(fund=new_fund)
            db.clsb30_tqg_log_tranfer.insert(user_id=user['id'],
                                             fund=fund,
                                             status="SUCCESS")
            return dict(error=result['value'])
        else:
            return dict(error=result['value'])
    except Exception as ex:
        return dict(error=ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))
