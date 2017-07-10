#@author: hant
# Those functions are inserted in many service.

from datetime import *
from contrib.pbkdf2 import *

ERR_TIME_OUT = CB_0011
ERR_TOKEN = CB_0012
SUCCES = CB_0000
DB_RQ_FAILD = CB_0003
MAXIMUM_ALLOWABLE_DEVICE_ACTIVE= CB_0017
MAXIMUM_ALLOWABLE_DEVICE_IN_USE = CB_0020
MAXIMUM_ALLOWABLE_TIME_SET_DEVICE_IN_USE = CB_0021

def checkTimeOut(name, t):
    if not name or not t:
        return CB_0019 #NULL_ARGUMENT
    
    table = 'clsb_user'

#    name = request.args(0)
#    t = request.args(1)
    row = db(db[table].username==name).select(db[table].user_token, db[table].lastLoginTime).first()
    if not row:
        return dict(error=USER_NAME_NOT_EXIST)  
    
    if datetime.now() < row['lastLoginTime'] + TIME_OUT:
        if row['user_token'] != None and t != None  and row['user_token'] == t:
            db(db[table].username == name).update(lastLoginTime = datetime.now())
            return SUCCES
        else:
            return ERR_TOKEN
    else:
        db(db[table].username == name).update(user_token = None, lastLoginTime = datetime.now())
        return ERR_TIME_OUT
    
def updateLogTime(name):
    table = 'clsb_user'
    try:
        db(db[table].username == name).update(lastLoginTime = datetime.now())
        return SUCCES
    except Exception as e:
        return DB_RQ_FAILD
    
# get a user's number-devices-active. Params: user_id, url to disable device to have the required nb of device. maxNbD=3
def verifyNbDevice(userid):
    table = 'clsb_device'
    try:
        devices_active = db(db[table].user_id == userid)(db[table].status==True).select()
        if devices_active and len(devices_active) >= MAX_D_ACTIVE:
            return MAXIMUM_ALLOWABLE_DEVICE_ACTIVE
        else:
            return SUCCES
    except Exception as e:
        return DB_RQ_FAILD

# get a user's number-devices-in-use. Params: user_id, url to disable device to have the required nb of device. maxNbD=1
def verifyInUseDevice(userid):
    table = 'clsb_device'
    try:
        devices_active = db(db[table].user_id == id)(db[table].in_use==True).select()
        if devices_active and len(devices_active) != MAX_D_IN_USE:
            return MAXIMUM_ALLOWABLE_DEVICE_IN_USE
        else:
            return SUCCES
    except Exception as e:
        return DB_RQ_FAILD

def verifyValidTime(userid):
    table = 'clsb_user'
    try:
        valid_time = db(db[table]._id == userid).select(db[table].valid_time).as_list()
        valid_time = valid_time[0]['valid_time']
        if valid_time == None:
            return 'test'#CB_0007 # data error, for exp: value is None
        if valid_time < MAX_VALID_TIME_SET_DEFAULT:
            return SUCCES
        else:
            return MAXIMUM_ALLOWABLE_TIME_SET_DEVICE_IN_USE
    except Exception as e:
        return DB_RQ_FAILD
    
def log(params, insert):
#     STATUS = 'Completed'
    try:
        db.clsb_user_log.insert(user_id=params['userID'], user_action='DOWNLOAD',
                                date_created=datetime.now,
                                search_text=params['searchTxt'],
                                product_code=params['pcode'],
                                ip_address=params['clientIP'],
                                )
        mytable = db.clsb_download_archieve
        prodID = None
        try:
            prodID = db(db.clsb_product.product_code==params['pcode']).select(db.clsb_product._id).as_list()
            prodID = prodID[0]['id']
            if prodID :
#                and not db(mytable.user_id==params['userID'] and
#                  mytable.device_serial==params['dserial'] and
#                  mytable.product_id==prodID).select():
                
                if insert:
                    db.clsb_download_archieve.insert(user_id=params['userID'],
                                              product_id=prodID,
                                              download_time=datetime.now(),
                                              device_serial=params['dserial'],
                                              status=params['status'],)
                else:
                    db(db.clsb_download_archieve.user_id==params['userID'])\
                        (db.clsb_download_archieve.product_id==prodID)\
                        (db.clsb_download_archieve.device_serial==params['dserial']).update(download_time=datetime.now(),
                                                                                            status=params['status'],) 
            return SUCCES
        except Exception as e:
            if not prodID:
                return PRODUCT_CODE_NOT_EXIST
            return DB_RQ_FAILD + str(e)
        
    except Exception as e:
        return DB_RQ_FAILD + str(e)


def pay(username, total, product_id, oldCBM):
    import applications.cbs.modules.transaction as transaction
    #message content to send user
    message = 'Tài khoản của bạn đã bị khóa, vui lòng liên hệ với quản trị viên để biết thêm chi tiết !'
    subject = 'Tài khoản ClassBook bị khóa'
    user_id = db(db.clsb_user.username == username).select(db.clsb_user.id).as_list()[0]['id']
    if not user_id:
        return CB_0010  # Tên đăng nhập không tồn tại
    rows = db(db.clsb_download_archieve.user_id == user_id)(db.clsb_download_archieve.product_id == product_id)\
        .select(db.clsb_download_archieve.status).as_list()
    if rows:
        return CB_0000  # SUCCES

    # total = request.args(1)
    # username = request.args(0)
    user_cash = db(db.clsb_user.username == username).select(db.clsb_user.fund, db.clsb_user.data_sum).as_list()
    user_cash = user_cash[0]['fund']
    if user_cash < total or user_cash < 0:
        return dict(error=CB_0023)

    try:
        #if db.clsb_user.data_sum != transaction.encrypt(db, user_cash, username):
            #db(db.clsb_user.username == username).update(status=False)
            # send mail to user
            # get user email
            #user_email = db(db.clsb_user.username == username).select(db.clsb_user.email).as_list()
            #user_email = user_email[0]['email']
            #try:
            #    mail.send(to=[user_email], subject=subject, message=message)
            #    return dict(item=CB_0000)
            #except Exception as e:
            #    print str(e)
            #    return dict(error=CB_0006)
                #return CB_0006
        if oldCBM:
            new_fund = db.clsb_user.fund - total / 2
        else:
            new_fund = db.clsb_user.fund - total 
            
        data_sum = transaction.encrypt(db, new_fund, username)
        db(db.clsb_user.username == username).update(fund=new_fund, data_sum=data_sum)
        return CB_0000  # SUCCESS
    except Exception as e:
        print "Error at pay() in modules/transaction.py: " + str(e)
        return CB_0003  # DB_RQ_FAILD


# Temporal fct to add cash for user account when user add a new device
def fund(username):
#    username = request.args(0)
    CASH = 200000
    if db(db.clsb_user.username == username).update(fund=db.clsb_user.fund + CASH):
        return CB_0000 #SUCCESS
    else:
        return CB_0006 #Faillure

def str2price(value):
    i = 0
    price = ''
    for index in range(len(value) - 1, -1, -1):
        i += 1
        price = value[index] + price
        if i == 3:
            price = '.' + price
            i = 0
    if price[0] == '.':
        price = price[1:]
    return u'Không thu phí' if price == '0' else price + '₫'
