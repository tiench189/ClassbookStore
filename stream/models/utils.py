#@author: hant
# Those functions are inserted in many service.

from datetime import *
from contrib.pbkdf2 import *
import os
import sys
import traceback
import usercp
import fs.path
import StringIO
import urllib2
sys.path.append('/home/pylibs/pdflib')


ERR_TIME_OUT = CB_0011
ERR_TOKEN = CB_0012
SUCCES = CB_0000
db_RQ_FAILD = CB_0003
MAXIMUM_ALLOWABLE_DEVICE_ACTIVE= CB_0017
MAXIMUM_ALLOWABLE_DEVICE_IN_USE = CB_0020
MAXIMUM_ALLOWABLE_TIME_SET_DEVICE_IN_USE = CB_0021
#DOMAIN_VDC = "123.30.179.205"
DOMAIN_VDC = "classbook.vn"

def timeOut(name, t):
    if not name or not t:
        return CB_0019 #NULL_ARGUMENT

    table = 'clsb_user'

#    name = request.args(0)
#    t = request.args(1)
    row = db(db[table].username==name).select(db[table].user_token, db[table].lastLoginTime).first()
    if not row:
        return USER_NAME_NOT_EXIST
    if row['user_token'] != None and t != None  and row['user_token'] == t:
        #if datetime.now() < row['lastLoginTime'] + TIME_OUT:
        db(db[table].username == name).update(lastLoginTime = datetime.now())
        return SUCCES
        #else:
        #    return ERR_TIME_OUT
    else:
        #db(db[table].username == name).update(user_token = None, lastLoginTime = datetime.now())
        return ERR_TOKEN

def checkTimeOut(name, t):
    return SUCCES
    if not name or not t:
        return CB_0019 #NULL_ARGUMENT
    
    table = 'clsb_user'

#    name = request.args(0)
#    t = request.args(1)
    row = db(db[table].username==name).select(db[table].user_token, db[table].lastLoginTime).first()
    if not row:
        return USER_NAME_NOT_EXIST
    
    #if datetime.now() < row['lastLoginTime'] + TIME_OUT:
    if row['user_token'] != None and t != None  and row['user_token'] == t:
        db(db[table].username == name).update(lastLoginTime = datetime.now())
        return SUCCES
    else:
        return ERR_TOKEN
    #else:
    #    db(db[table].username == name).update(user_token = None, lastLoginTime = datetime.now())
    #    return ERR_TIME_OUT
    
def updateLogTime(name):
    table = 'clsb_user'
    try:
        db(db[table].username == name).update(lastLoginTime = datetime.now())
        return SUCCES
    except Exception as e:
        return db_RQ_FAILD
    
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
        return db_RQ_FAILD

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
        return db_RQ_FAILD

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
        return db_RQ_FAILD


#add log for store 2.0
def log_20(params, insert):
    try:
        db.clsb_user_log.insert(user_id=params['userID'], user_action='DOWNLOAD',
                                date_created=datetime.now,
                                search_text=params['searchTxt'],
                                product_code=params['pcode'],
                                ip_address=params['clientIP'],
                                )
        product = db(db.clsb_product.product_code == params['pcode']).select(db.clsb_product._id)
        if len(product) > 0:
            try:
                product_id = product.first()['id']
                device_serial = params['dserial']
                except_device = db(db.clsb20_device_exception.device_serial == device_serial).select(db.clsb20_device_exception.device_serial).as_list()
                if len(except_device) > 0:
                    price = 0
                else:
                    price = params['price']
                if insert:

                    new_log = db.clsb_download_archieve.insert(
                        user_id=params['userID'],
                        product_id=product_id,
                        price=price,
                        download_time=datetime.now(),
                        purchase_type=params['purchase_type'],
                        rom_version=params['rom_version'],
                        device_serial=params['dserial'],
                        status=params['status']

                    )
                    #return id from log
                    return new_log['id']
                else:
                    #update log by id
                    log_data = db((db.clsb_download_archieve.id == params['log_id']) & (db.clsb_download_archieve.status.like("Inprogress")))
                    if len(log_data.select()) > 0:
                        db(db.clsb_download_archieve.id == params['log_id']).update(price=price, status=params['status'])
                        return "OK"
                    else:
                        return False
            except Exception as e:
                print e
                return False
    except Exception as e:
        print e
        return False



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
                                              price=params['price'],#add price for download_archieve
                                              download_time=datetime.now(),
                                              purchase_type=params['purchase_type'],
                                              rom_version=params['rom_version'],
                                              device_serial=params['dserial'],
                                              status=params['status'],)
                else:
                    download_id = db(db.clsb_download_archieve.user_id == params['userID'])\
                        (db.clsb_download_archieve.product_id == prodID)\
                        (db.clsb_download_archieve.device_serial == params['dserial'])\
                        (~db.clsb_download_archieve.status.like("Completed")).select(orderby=db.clsb_download_archieve.download_time).as_list()
                    download_id = download_id[-1]['id']
                    db(db.clsb_download_archieve.id == download_id).update(price=params['price'], status=params['status'])
            return SUCCES
        except Exception as e:
            if not prodID:
                return PRODUCT_CODE_NOT_EXIST
            return db_RQ_FAILD + str(e)
        
    except Exception as e:
        return db_RQ_FAILD + str(e)


def pay(username, total, product_id, oldCBM):
    import applications.cbs.modules.transaction as transaction
    try:
        #message content to send user
        message = 'Tài khoản của bạn đã bị khóa, vui lòng liên hệ với quản trị viên để biết thêm chi tiết !'
        subject = 'Tài khoản ClassBook bị khóa'
        user_id = db(db.clsb_user.username == username).select(db.clsb_user.id).as_list()[0]['id']
        if not user_id:
            return CB_0010  # Tên đăng nhập không tồn tại

        # total = request.args(1)
        # username = request.args(0)
        user_cash = db(db.clsb_user.username == username).select(db.clsb_user.fund, db.clsb_user.data_sum).as_list()
        user_cash = user_cash[0]['fund']

        # remove check user_cash /TanBM 03/01/201
        # if user_cash < total or user_cash < 0:
        #     return dict(error=CB_0023)


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

        # check new purchase
        new_fund = user_cash
        query = db(db["clsb_product"].id == product_id)
        query = query(db["clsb20_product_purchase_item"].product_code == db["clsb_product"].product_code)
        query = query(db["clsb20_purchase_item"].id == db["clsb20_product_purchase_item"].purchase_item)
        query = query(db["clsb20_purchase_type"].id == db["clsb20_purchase_item"].purchase_type)
        product_purchases = query.select(
                                        # db["clsb20_product_purchase_item"].discount,
                                        db["clsb20_purchase_type"].name,
                                        # db["clsb20_purchase_type"].name, db["clsb20_purchase_item"].times,
                                        db["clsb20_purchase_item"].duration, db['clsb20_purchase_item'].id)
        if len(product_purchases) == 0:
            rows = db((db.clsb_download_archieve.user_id == user_id) & (db.clsb_download_archieve.product_id == product_id) & (db.clsb_download_archieve.status.like("Completed") | db.clsb_download_archieve.status.like("TestSuccess"))).select(db.clsb_download_archieve.status)
            if len(rows) > 0:
                pass
            else:
                if oldCBM:
                    new_fund -= total / 2
                else:
                    new_fund -= total
        else:
            from datetime import datetime
            from datetime import timedelta
            product_purchase = product_purchases.first()
            if product_purchase.clsb20_purchase_type.name.upper() != "FREE":
                if product_purchase.clsb20_purchase_type.name.upper() != "NONCONSUMABLE":
                    query = db(db["clsb20_user_purchase_item"].user_id == user_id)
                    query = query(db["clsb20_user_purchase_item"].purchase_id == product_purchase.clsb20_purchase_item.id)
                    user_purchases = query.select(db["clsb20_user_purchase_item"].id,
                                                  # db["clsb20_user_purchase_item"].times,
                                                  db["clsb20_user_purchase_item"].day_end)
                    is_expired_date_or_time = False
                    if len(user_purchases) > 0:
                        user_purchase = user_purchases.first()
                        # if user_purchase.times > 0:
                        #     db(db["clsb20_user_purchase_item"].id == user_purchase.id).update(times=user_purchase.times-1)
                        # elif user_purchase.times < 0 or user_purchase.day_end > datetime.today():
                        #     pass
                        # else:
                        #     if oldCBM:
                        #         new_fund -= total / 2
                        #     else:
                        #         new_fund -= total
                        #     day_end = datetime.today() + timedelta(days=product_purchase.clsb20_purchase_item.duration)
                        #     query = db(db["clsb20_user_purchase_item"].id == user_purchase.id)
                        #     query.update(day_end=day_end, times=product_purchase.clsb20_purchase_item.times)
                        #     db["clsb20_purchase_renew_history"].insert(user_id=user_id, product_id=product_id, date_do_renew=datetime.today())
                        if oldCBM:
                            new_fund -= total / 2
                        else:
                            new_fund -= total
                        day_end = datetime.today() + timedelta(days=product_purchase.clsb20_purchase_item.duration)
                        query = db(db["clsb20_user_purchase_item"].id == user_purchase.id)
                        query.update(day_end=day_end)
                            # , times=product_purchase.clsb20_purchase_item.times)
                        db["clsb20_purchase_renew_history"].insert(user_id=user_id, product_id=product_id, date_do_renew=datetime.today())
                    else:
                        if oldCBM:
                            new_fund -= total / 2
                        else:
                            new_fund -= total
                        # if product_purchase.clsb20_purchase_item.times == 0:
                        #     day_end = datetime.today() + timedelta(days=product_purchase.clsb20_purchase_item.duration)
                        #     db["clsb20_user_purchase_item"].insert(user_id=user_id, product_id=product_id,
                        #                                            times=product_purchase.clsb20_purchase_item.times,
                        #                                            day_end=day_end)
                        #     db["clsb20_purchase_renew_history"].insert(user_id=user_id, product_id=product_id,
                        #                                            date_do_renew=datetime.today())
                        day_end = datetime.today() + timedelta(days=product_purchase.clsb20_purchase_item.duration)
                        db["clsb20_user_purchase_item"].insert(user_id=user_id, purchase_id=product_purchase.clsb20_purchase_item.id,
                                                                   # times=product_purchase.clsb20_purchase_item.times,
                                                                   day_end=day_end)
                        db["clsb20_purchase_renew_history"].insert(user_id=user_id, product_id=product_id,
                                                                   date_do_renew=datetime.today())
                else:
                    change_time_first = db(db.clsb20_product_price_history.product_id == product_id)\
                            (db.clsb20_product_price_history.purchase_item == product_purchase.clsb20_purchase_item.id).select(orderby=db.clsb20_product_price_history.changing_time)

                    if len(change_time_first) > 0:
                        change_time_first = change_time_first.first()
                        rows = db(db.clsb_download_archieve.user_id == user_id)(db.clsb_download_archieve.product_id == product_id)\
                            (db.clsb_download_archieve.download_time >=  change_time_first.changing_time).select(db.clsb_download_archieve.status)
                        if len(rows) > 0:
                            pass
                        else:
                            if oldCBM:
                                new_fund -= total / 2
                            else:
                                new_fund -= total
                    else:
                        rows = db((db.clsb_download_archieve.user_id == user_id) & (db.clsb_download_archieve.product_id == product_id) & (db.clsb_download_archieve.status.like("Completed") | db.clsb_download_archieve.status.like("TestSuccess"))).select(db.clsb_download_archieve.status)
                        if len(rows) > 0:
                            pass
                        else:
                            if oldCBM:
                                new_fund -= total / 2
                            else:
                                new_fund -= total
        data_sum = transaction.encrypt(new_fund, username)
        db(db.clsb_user.username == username).update(fund=new_fund, data_sum=data_sum)

        data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
        insert_to_log_temp(data)
        # url_update_fund = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="update_user_fund",
        #                       vars=dict(fund=new_fund, data_sum=data_sum, username=username))
        # print(url_update_fund)
        # urllib2.urlopen(url_update_fund)
        return CB_0000  # SUCCESS
    except:
        import traceback
        traceback.print_exc()
        # print "Error at pay() in modules/transaction.py: " + str(e) +" on line: "+str(sys.exc_traceback.tb_lineno)
        return str(sys.exc_traceback.tb_lineno)  # db_RQ_FAILD


# Temporal fct to add cash for user account when user add a new device
def fund(username):
#    username = request.args(0)
    CASH = 200000
    if db(db.clsb_user.username == username).update(fund=db.clsb_user.fund + CASH):

        user_id = db(db.clsb_user.username == username).select().first()['id']
        data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
        insert_to_log_temp(data)
        # url_update_fund = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="update_user_fund",
        #                       vars=dict(fund=db.clsb_user.fund + CASH, data_sum="cash", username=username))
        # print(url_update_fund)
        # urllib2.urlopen(url_update_fund)
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


#add check product for old version
def check_product_for_old_version(product_code):
    query = db(db["clsb_product"].product_code == product_code)
    query = query(db["clsb20_product_purchase_item"].product_code == db["clsb_product"].product_code)
    query = query(db["clsb20_purchase_item"].id == db["clsb20_product_purchase_item"].purchase_item)
    query = query(db["clsb20_purchase_type"].id == db["clsb20_purchase_item"].purchase_type)
    product_purchases = query.select(
        db["clsb_product"].product_price,
        db["clsb20_purchase_type"].name,
        db["clsb20_purchase_item"].duration, db['clsb20_purchase_item'].id
    )
    purchase = False
    if len(product_purchases) > 0:
        product_purchase = product_purchases.first()
        if (product_purchase.clsb20_purchase_type.name.upper() != "NONCONSUMABLE") & (product_purchase.clsb20_purchase_type.name.upper() != "FREE"):
            purchase = True

    type_name = db((db.clsb_product.product_code == product_code) & (db.clsb_product.product_price > 0))\
            (db.clsb_product.product_category == db.clsb_category.id)\
            (db.clsb_category.category_type == db.clsb_product_type.id)\
            (db.clsb_product_type.type_name.like("Application") | db.clsb_product_type.type_name.like("Exercise")).select()
    if len(type_name) > 0:
        purchase = True

    return purchase


def get_purchase_description(code):
    purchase = db(db.clsb20_product_purchase_item.product_code == code)\
        (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
        (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type).select()

    if len(purchase) > 0:
        purchase = purchase.first()["clsb20_purchase_type"]["description"]
    else:
        purchase = "Thanh toán cho lần đầu tiên tải về"

    return purchase


#add check ota_update
def check_ota_update(code):
    data = db(db.clsb_ota_version.software.like(code)).select()
    if len(data) > 0:
        return True
    return False


def pay_to_log(user, product, classbook_device, end_buy=False):
    if classbook_device and check_free_for_classbook(product['clsb_category']['id']):
        return True
    if not check_free_for_classbook(product['clsb_category']['id']):
        downloaded = db(db.clsb_download_archieve.product_id == product['clsb_product']['id'])(db.clsb_download_archieve.status.like("Completed"))(db.clsb_download_archieve.user_id == user['id']).select()
        if len(downloaded) > 0:
            return True
    """
    Mua cho thiet bi class book voi gia sach SGK se ko ghi log
    """
    import applications.cbs20.modules.transaction as transaction
    check_buy = db(db.clsb30_product_history.product_id == product['clsb_product']['id'])(db.clsb30_product_history.user_id == user['id']).select()
    if len(check_buy) > 0:
        return True
    if not end_buy:
        user_cash = db(db.clsb_user.id == user['id']).select(db.clsb_user.fund, db.clsb_user.data_sum).as_list()
        user_cash = user_cash[0]['fund']
        new_fund = user_cash - product['clsb_product']['product_price']
        if new_fund < 0:
            return dict(error='Tiền trong tài khoản không đủ')

        data_sum = transaction.encrypt(new_fund, user['username'])
        db(db.clsb_user.username == user['username']).update(fund=new_fund, data_sum=data_sum)

        user_id = db(db.clsb_user.username == user['username']).select().first()['id']
        data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
        insert_to_log_temp(data)
        # url_update_fund = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="update_user_fund",
        #                       vars=dict(fund=new_fund, data_sum=data_sum, username=user['username']))
        # print(url_update_fund)
        # urllib2.urlopen(url_update_fund)
    if len(db(db.clsb30_product_history.product_id == product['clsb_product']['id'])(db.clsb30_product_history.user_id == user['id']).select()) <= 0:
        insert_buy = db.clsb30_product_history.insert(
            product_title=product['clsb_product']['product_title'],
            product_id=product['clsb_product']['id'],
            user_id=user['id'],
            category_id=product['clsb_category']['id'],
            product_price=product['clsb_product']['product_price']
        )
        data = dict(record_id=str(insert_buy), table_name='clsb30_product_history', key_unique='user_id.product_id')
        insert_to_log_temp(data)
        # url_sign = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="sign_buy_product", args=["Product",
        #                                                                                     product['clsb_product']['id'],
        #                                                                                     user['username'],
        #                                                                                     product['clsb_category']['id'],
        #                                                                                     pay])
        # print(url_sign)
        # urllib2.urlopen(url_sign)
    return True

def pay_to_log_divide(user, product, classbook_device, isMedia, pay, end_buy=False):
    # if classbook_device and check_free_for_classbook(product['clsb_category']['id']):
    #     print('return1')
    #     return "True 1"
    if isMedia.lower() == 'false':
        if not check_free_for_classbook(product['clsb_category']['id']):
            downloaded = db(db.clsb_download_archieve.product_id == product['clsb_product']['id'])(db.clsb_download_archieve.status.like("Completed"))(db.clsb_download_archieve.user_id == user['id']).select()
            if len(downloaded) > 0:
                print('return2')
                return "True 2"
    """
    Mua cho thiet bi class book voi gia sach SGK se ko ghi log
    """
    import applications.cbs20.modules.transaction as transaction

    if isMedia.lower() == 'true':
        check_buy = db(db.clsb30_media_history.product_id == product['clsb_product']['id'])(db.clsb30_media_history.user_id == user['id']).select()
        print(check_buy)
        if len(check_buy) > 0:
            print('return3')
            return "True 3"
    else:
        check_buy = db(db.clsb30_product_history.product_id == product['clsb_product']['id'])(db.clsb30_product_history.user_id == user['id']).select()
        print(check_buy)
        if len(check_buy) > 0:
            print('return4')
            return "True 4"
    if not end_buy:
        user_cash = db(db.clsb_user.id == user['id']).select(db.clsb_user.fund, db.clsb_user.data_sum).as_list()
        user_cash = user_cash[0]['fund']
        new_fund = int(user_cash) - int(pay)
        if new_fund < 0:
            print('return5')
            return dict(error='Tiền trong tài khoản không đủ')
        print('tiench new_fund: ' + str(new_fund))
        data_sum = transaction.encrypt(new_fund, user['username'])
        db(db.clsb_user.username == user['username']).update(fund=new_fund, data_sum=data_sum)

        user_id = db(db.clsb_user.username == user['username']).select().first()['id']
        data = dict(record_id=user_id, table_name='clsb_user', key_unique='username')
        insert_to_log_temp(data)
        # url_update_fund = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="update_user_fund",
        #                       vars=dict(fund=new_fund, data_sum=data_sum, username=user['username']))
        # print(url_update_fund)
        # update_result = urllib2.urlopen(url_update_fund)
        # print(update_result.read())
    if isMedia.lower() == 'true':
        print("tiench insert media: " + str(isMedia))
        if len(db(db.clsb30_media_history.product_id == product['clsb_product']['id'])(db.clsb30_media_history.user_id == user['id']).select()) <= 0:
            media_insert = db.clsb30_media_history.insert(
                product_title=product['clsb_product']['product_title'],
                product_id=product['clsb_product']['id'],
                user_id=user['id'],
                category_id=product['clsb_category']['id'],
                product_price=pay
            )

            params = {'searchTxt': 'ND',
                  'clientIP': '',
                  'dserial': "",
                  'pcode': product['clsb_product']['product_code'],
                  'purchase_type': 'WEB_PAY',
                  'rom_version': "CLASSBOOK.APP",
                  'userID': user_id,
                  'price': int(pay),
                  'status': 'Completed'}
            log_20(params, True)

            db.clsb30_payment_log.insert(user_id=user_id, product_id=product['clsb_product']['id'],
                                         product_type='MEDIA', pay=int(pay))

            data = dict(record_id=str(media_insert), table_name='clsb30_media_history', key_unique='user_id.product_id')
            insert_to_log_temp(data)
            # url_sign = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="sign_buy_media", args=["Product",
            #                                                                                 product['clsb_product']['id'],
            #                                                                                 user['username'],
            #                                                                                 product['clsb_category']['id'],
            #                                                                                 pay])
            # print(url_sign)
            # urllib2.urlopen(url_sign)
    else:
        print("tiench insert product: " + str(isMedia))
        try:
            if len(db(db.clsb30_product_history.product_id == product['clsb_product']['id'])(db.clsb30_product_history.user_id == user['id']).select()) <= 0:
                product_insert = db.clsb30_product_history.insert(
                    product_title=product['clsb_product']['product_title'],
                    product_id=product['clsb_product']['id'],
                    user_id=user['id'],
                    category_id=product['clsb_category']['id'],
                    product_price=pay
                )
                params = {'searchTxt': 'ND',
                  'clientIP': '',
                  'dserial': "",
                  'pcode': product['clsb_product']['product_code'],
                  'purchase_type': 'WEB_PAY',
                  'rom_version': "CLASSBOOK.APP",
                  'userID': user_id,
                  'price': int(pay),
                  'status': 'Completed'}
                log_20(params, True)
                db.clsb30_payment_log.insert(user_id=user_id, product_id=product['clsb_product']['id'],
                                         product_type='PRODUCT', pay=int(pay))
                data = dict(record_id=str(product_insert), table_name='clsb30_product_history', key_unique='user_id.product_id')
                insert_to_log_temp(data)

                # url_sign = URL(host=DOMAIN_VDC, a='cbs20', c="sync2vdc", f="sign_buy_product", args=["Product",
                #                                                                                      product['clsb_product']['id'],
                #                                                                                      user['username'],
                #                                                                                      product['clsb_category']['id'],
                #                                                                                      pay])
                # print(url_sign)
                # urllib2.urlopen(url_sign)
        except Exception as err:
            print("Error: " + err)
            return dict(error=str(err))
    return "True final"


def check_free_for_classbook(category_id):
    try:
        parent_id = db(db.clsb_category.id == category_id).select().first()['category_parent']
        list = db((db.clsb30_category_classbook_device.product_category == category_id) | (db.clsb30_category_classbook_device.product_category == parent_id)).select()
        if len(list) <= 0:
            return False
        return True
    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return False


def make_zip_nomedia(path, code, file):
    path_in = os.path.join(path, file)
    path_out = os.path.join(path, file+".nomedia")
    if os.path.exists(path_out):
        pass
    else:
        import zipfile
        z_in = zipfile.ZipFile(settings.home_dir+path_in, "r")
        z_out = zipfile.ZipFile(settings.home_dir+path_out, "w")
        try:
            z_out.writestr(code+"/book_config/config.xml", z_in.read(code+"/book_config/config.xml"))
            z_out.writestr(code+"/book_config/.nomedia", z_in.read(code+"/book_config/.nomedia"))
            z_out.writestr(code+"/book_config/cover.clsbi21", z_in.read(code+"/book_config/cover.clsbi21"))
            z_out.writestr(code+"/book_config/cover.clsbi21", z_in.read(code+"/book_config/cover.clsbi20"))
        except:
            pass
        z_in.close()
        z_out.close()
    return path_out

## bo dau tieng viet

#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import unicodedata

def remove_viet_accents(str):
    ''' Helper function: Remove Vietnamese accent for string '''
    nkfd_form = unicodedata.normalize('NFKD', unicode(str, 'utf-8'))
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)]).replace(u'\u0111','d').replace(u'\u0110', 'D')

def check_media(product_code):#params: product_code
    try:
        response.generic_patterns = ['*']
        # product_code = request.args(0)
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        import Image

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        else:
            path = fs.path.pathjoin(product_code)
        product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
        if len(product_files) == 0:
            return  dict(check=False)
        else:
            check = check_media_in_zip(fs.path.pathjoin(settings.home_dir, path, product_files[0]), product_code)
            print('check' + str(check))
            return dict(check=check)
    except Exception as ex:
        print('tiench' + str(ex))
        return dict(check=False)

def check_media_in_zip(path, product_code):
    try:
        import zipfile
        zip_file = zipfile.ZipFile(path, "r")
        for name in [member.filename for member in zip_file.infolist()]:
            # print(name)
            if str.startswith(name, product_code.upper()+"/media/"):
                zip_file.close()
                return True
        else:
            zip_file.close()
        return False
    except Exception as err:
        print('tiench' + str(err))
        return False

def server_version():
    return settings.server_ver;

def check_version_mp(app_ver):
    if 'ios' not in app_ver.lower():
        return False
    version = app_ver.split('_')[len(app_ver.split('_')) - 1]
    print(version)
    check = db(db.clsb30_fake_ios.fake_name == 'ios').select()
    if len(check) == 0:
        return False
    if int(check[0]['fake_value']) == 0:
        return False
    elif int(check[0]['fake_value']) == 1:
        return True
    else:
        try:
            data = parsr_data_istore("942940905")
            if int(data['resultCount']) > 0:
                if version > data['results'][0]['version']:
                    return True
                else:
                    return False
            else:
                return True
        except Exception as err:
            return True

def parsr_data_istore(id):
    import urllib, json
    url = "https://itunes.apple.com/lookup?id=" + id
    response = urllib.urlopen(url)
    data = json.loads(response.read())
    return data

#########tiench insert to log temp###################
INIT = "init"
import time
from datetime import datetime

def write_log(file_name, content):
    try:
        log_file = open("/home/www-data/web2py/applications/" + file_name + ".txt", 'a+')
        log_file.write(content + " " + str(datetime.now()) + "\n")
        log_file.close()
        return True
    except Exception as err:
        return str(err) + " on line: "+str(sys.exc_traceback.tb_lineno)

def sync_a_record():
    try:
        write_log("sync_log", "0")
        data_log = db(db.clsb30_sync_temp.status == INIT).select()
        if len(data_log) == 0:
            return dict(result=False, code="FINISH")
        write_log("sync_log", "1")
        data_log = data_log.first()
        get_data = get_data_sync(data_log['record_id'], data_log['table_name'], data_log['key_unique'])
        write_log("sync_log", "2")
        get_data['table_name'] = data_log['table_name']
        print("get_data: " + str(get_data))
        result = sync_data_to_db(get_data)
        write_log("sync_log", "3")
        db(db.clsb30_sync_temp.id == data_log['id']).delete()
        write_log("sync_log", str(result))
        if result['result']:
            return True
        else:
            db.clsb30_sync_temp.insert(record_id=data_log['record_id'], table_name=data_log['table_name'],
                                    status=INIT, key_unique=data_log['key_unique'])
            return False
        return dict(result=True)
    except Exception as err:
        write_log("sync_log", "4" + str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(result=False, code="ERROR", error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))

def insert_to_log_temp(data):
    try:
        record_id = data['record_id']
        table_name = data['table_name']
        key_unique = data['key_unique']
        check_exist = db(db.clsb30_sync_temp.record_id == str(data['record_id']))\
            (db.clsb30_sync_temp.table_name == str(data['table_name']))\
            (db.clsb30_sync_temp.status == "init").select()
        if len(check_exist) == 0:
            try:
                #get_data = get_data_sync(record_id, table_name, key_unique)
                #get_data['table_name'] = table_name
                #print("get_data: " + str(get_data))
                #result = sync_data_to_db(get_data)
                #if not result['result']:
                db.clsb30_sync_temp.insert(record_id=record_id, table_name=table_name,
                                    status=INIT, key_unique=key_unique)
                #return result
            except Exception as err:
                print(err)
    except Exception as e:
        print(e)
    return False

def sync_data_to_db(get_data):
    db_sync = connect_db_sync()
    query_bug = ""
    try:
        unique_data = get_data['unique']
        data = get_data['data']
        table_name = get_data['table_name']
        if 'username' in unique_data:
            users = db_sync.executesql("SELECT * FROM clsb_user WHERE username" + "='" + unique_data['username'] + "'")
            if len(users) == 0 and table_name != 'clsb_user':
                return dict(result=False, error=CB_0001)
            if len(users) > 0:
                user = users[0]
                if 'user_id' in data:
                    data['user_id'] = user[0]
                    unique_data['user_id'] = user[0]
                if 'username' not in data:
                    del unique_data['username']
            # return dict(data=data)
        query_unique = ""
        for key in unique_data.keys():
            if table_name != 'clsb_device' or key != 'user_id':
                if query_unique != "":
                    query_unique += " AND "
                query_unique += str(key) + "='" + str(unique_data[key]) + "'"
        check_exist = False
        query_bug = "SELECT * FROM " + table_name + " WHERE " + query_unique
        if len(unique_data) > 0:
            check_data = db_sync.executesql("SELECT * FROM " + table_name + " WHERE " + query_unique)
            if len(check_data) > 0:
                check_exist = True
        print("exist: " + str(check_exist))
        if check_exist:
            query_data_update = "UPDATE " + table_name + " SET "
            data_update = ""
            for key in data.keys():
                if key not in unique_data:
                    print(key)
                    if data_update != "":
                        data_update += ","
                    if data[key] == None:
                        data_update += str(key) + "=null"
                    else:
                        try:
                            data_update += str(key) + "='" + data[key].encode('utf-8') + "'"
                        except Exception as err:
                            try:
                                data_update += str(key) + "='" + str(data[key]) + "'"
                            except Exception as e:
                                print("ERR: " + str(e))
                        print(data_update)
            query_data_update += data_update
            query_data_update += " WHERE " + query_unique
            print(query_data_update)
            query_bug = query_data_update
            try:
                db_sync.executesql(query_data_update)
                return dict(result=True)
            except Exception as err:
                print('err sql: ' + str(err))
                return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
        else:
            str_field = ""
            str_value = ""
            for key in data.keys():
                if data.keys().index(key) > 0:
                    str_field += ","
                    str_value += ","
                str_field += str(key)
                print("data " + str(key) + ": ")
                if data[key] == None:
                    str_value += "null"
                else:
                    try:
                        str_value += "'" + data[str(key)].encode("utf-8") + "'"
                    except Exception as err:
                        print(err)
                        str_value += "'" + str(data[str(key)]) + "'"
            query_data_insert = "INSERT INTO " + table_name + "(" + str_field + ") VALUES (" + str_value + ")"
            print(query_data_insert)
            query_bug = query_data_insert
            try:
                db_sync.executesql(query_data_insert)
                return dict(result=True)
            except Exception as err:
                return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
    except Exception as err:
        return dict(result=False, error=str(err) + " - " + query_bug + " on line: "+str(sys.exc_traceback.tb_lineno) + ":" + str(get_data))

def get_data_sync(record_id, table_name, key_unique): #record_id, table_name, key_unique
    try:
        data_result = db.executesql("SELECT * FROM " + table_name + " WHERE id =" + str(record_id), as_dict=True)
        if len(data_result) == 0:
            return dict(result=False, err="no record")
        print(data_result[0])
        data = data_result[0]
        del data['id']
        unique_dict = dict()
        for unique in key_unique.split('.'):
            if unique == 'user_id':
                user = db(db.clsb_user.id == data['user_id']).select().first()
                unique_dict['username'] = user['username']
            else:
                unique_dict[unique] = data[unique]
        return dict(data=data, unique=unique_dict)
    except Exception as err:
            return dict(result=False, err=str(err)+" on line: "+str(sys.exc_traceback.tb_lineno))
    return dict(result=False, err="UNKNOWN")



def connect_db_sync():
    return DAL(settings.database_sync,
                        pool_size=1, check_reserved=['all'],
                        migrate_enabled=settings.migrate, decode_credentials=True, db_codec='UTF-8')