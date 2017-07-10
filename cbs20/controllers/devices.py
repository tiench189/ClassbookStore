# coding: utf8
# try something like

#@author: hant 27-02-2013

#import cbMsg
SUCCESS = CB_0000#cbMsg.CB_0000
EXISTENT = CB_0005#cbMsg.CB_0005
LACK_ARGS = CB_0002#cbMsg.CB_0002
FAILURE = CB_0006#cbMsg.CB_0006
DB_RQ_FAILURE = CB_0003#cbMsg.CB_0003
NOT_EXISTED = CB_0007#cbMsg.CB_0007

table = 'clsb_device'

path = list()
path.append('/mnt/sdcard')
path.append('/storage/sdcard0')

"""
    Return a list of path to sdcard on classbook device. It's used by Classbook Manager.
"""


def path2sdcard():
    return dict(items=path)


"""
    Check valid released device serial.
"""


def device():
    if len(request.args) == 1:
        serial = request.args(0)
        realesed_device = db(db.clsb_released_serial.released_serial == serial[0:5]).count()
        if realesed_device:
            return dict(item=CB_0000)
        else:
            return dict(error=CB_0024)


def change_device_name():
    if request.args or len(request.vars) < 2:
        return dict(item=CB_0000)
    #print 'change device name'
    #print request.vars
    device_serial = request.vars['device_serial']
    new_device_name = request.vars['new_device_name']

    db(db.clsb_device.device_serial == device_serial).update(device_name=new_device_name)


def get_device_detail():
    if request.args or len(request.vars) < 1:
        return dict(item=CB_0000)
    device_detail = dict()
    device_serial = request.vars['device_serial']
    #print request.vars
    rows = db(db.clsb_device.device_serial == device_serial).select(db.clsb_device.device_serial,
                                                                    db.clsb_device.device_type)

    for row in rows:
        device_detail['device_serial'] = row['device_serial']
        device_detail['device_type'] = row['device_type']
        #print row['device_type']

    return dict(device_detail=device_detail)


def is_device_classbook():

    if request.vars or len(request.args) < 1:
        return dict(item=CB_0000)

    device_serial = request.args[0]
    device = db(db.clsb_device.device_serial == device_serial).select(db.clsb_device.ALL).first()
    if device['device_type'] == 'OTHER':
        return dict(result=False, device_name=device['device_name'])
    return dict(result=True, device_name=device['device_name'])


def is_device_register():
    if request.args or len(request.vars) < 1:
        return dict(item=CB_0000)

    device_serial = request.vars['device_serial']

    device = db(db.clsb_device.device_serial == device_serial).select(db.clsb_device.ALL).first()

    if device is None:
        #print("Thiết bị chưa đăng kí")
        return dict(result="Thiết bị chưa đăng kí", code="NOT_YET_REGISTER")
    else:
        if device['user_id'] is None:
            #print("Thiết bị chưa đăng kí")
            return dict(result="Thiết bị chưa đăng kí", code="NOT_YET_REGISTER")
        else:
            user = db(db.clsb_user.id == device['user_id']).select(db.clsb_user.ALL).first()
            #print(user["email"])
            return dict(error="Thiết bị đã được đăng kí", code="DEVICE_REGISTED_USER", email=user["email"])
    return dict(error="Thiết bị đã được đăng kí", code="DEVICE_REGISTED")



def change_device_name():
    if request.args or len(request.vars) < 3:
        return dict(item=CB_0000)
    try:
        device_serial = request.vars['device_serial']
        device_name = request.vars['name']
        token = request.vars['token']
        #print request.vars

        user = db(db.clsb_user.user_token == token).select(db.clsb_user.ALL).first()

        if user is None:
            return dict(error="Hết phiên làm việc", code="TIMEOUT")

        device_change = db(db.clsb_device.device_serial == device_serial).select()

        if len(device_change) == 0:
            return dict(result="Thiết bị chưa đăng kí", code="NOT_YET_REGISTER", serial=device_serial)

        rs = db(db.clsb_device.device_serial == device_serial).update(device_name=device_name)
        #print db._lastsql
        #print rs
        return dict(result = "Đổi tên thiết bị thành công")
    except Exception as e:
        return dict(error="Lỗi không xác định.")


#def insert():
## TODO: request authentication
#    if not table in db.tables(): return NOT_EXISTED
#
#    if request.vars and request.vars > 2:
#        try:
#            db[table].insert(**request.vars)
#            return SUCCESS
#        except Exception:
#            return DB_RQ_FAILD
#    return LACK_ARGS
#
#def selectAll():
## TODO: request authentication
#    if not table in db.tables(): NOT_EXISTED
#    tbl = db().select(db[table].ALL, orderby=db[table].device_serial)
#    return dict(tbl=tbl)
#
#def delete(): # by device_serial
## TODO: request authentication
#
#    if not table in db.tables(): return NOT_EXISTED
#
#    if request.vars.id:
#        try:
#            db(db[table].device_serial == request.vars.device_serial).delete()
#            return SUCCESS
#        except Exception:
#            return DB_RQ_FAILD
#    else:
#        return LACK_ARGS
#    
## exp: /CBS/download_archieve/deleteMultipleRow?delete=delete&id1=4&id2=6
#def deleteMultipleRow(): # by device_serial
#    if not table in db.tables(): return NOT_EXISTED
#    
#    if request.vars and len(request.vars)>1:
#        rows = request.vars.pop("delete")
#        for archieve in request.vars:
#            db(db[table].device_serial == request.vars[archieve]).delete()
#        return SUCCESS
#    else:
#        return LACK_ARGS
#    
## exp: /CBS/download_archieve/update?id=7&product_code=1249435634673463
#def update(): # by device_serial
## TODO: request authentication
#
#    if not table in db.tables(): return NOT_EXISTED
#    
#    if request.vars and request.vars > 1:
#        try:
#            db(db[table]._id==request.vars.device_serial).update(**request.vars)
#            return SUCCESS
#        except Exception:
#            return DB_RQ_FAILD
#    else:
#        return LACK_ARGS
#
## exp:  /CBS/download_archieve/selectByID?device_serial=7
#def selectBySerial():
## TODO: request authentication
#    if not table in db.tables(): return NOT_EXISTED
#
#    if request.vars and len(request.vars) == 1:
#        try:
#            seletedID = db(db[table].device_serial.like(request.vars.device_serial)).select() 
#            return seletedID
#        except Exception:
#            return DB_RQ_FAILD
#    else:
#        return LACK_ARGS
#    
## exp:  /CBS/download_archieve/selectByID?device_serial=7
#def selectByUserID():
## TODO: request authentication
#    if not table in db.tables(): return NOT_EXISTED
#
#    if request.vars and len(request.vars) == 1:
#        try:
#            seletedID = db(db[table].user_id.like(request.vars.user_id)).select() 
#            return seletedID
#        except Exception:
#            return DB_RQ_FAILD
#    else:
#        return LACK_ARGS
