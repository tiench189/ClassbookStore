__author__ = 'Tien'

from gcv import verify
import hashlib
import sys
import requests
import json
from datetime import datetime

def a2b(s): # convert hex string to byte sequence, e.g '89ABCDEF' -> '\x89\xab\xcd\xef'
    res = ''
    for i in range(len(s)/2):
        res += chr(int(s[i*2:i*2+2], 16))
    return res

Signature = 'Classbook'

def check(code):
    value, serial, checksum = code[:4], code[5:9] + code[10:14], code[15:]
    serial, checksum = a2b(serial), a2b(checksum)
    return hashlib.md5(Signature + value + serial).digest()[-2:] == checksum

def test():
    #print verify('0100 1AC8 DC9F 559E')
    #print verify('0150 4D18 577A 1801')

    #print verify('0100 1AC8 DC9F 559E', True)
    #print verify('0150 4D18 577A 1801', True)

    #print check('0100 1AC8 DC9F 559E')
    #print check('0150 055A 42E2 C852')
    return dict(verify=verify('1150 0151 2221 0180'))

def test_insert():
    #print(request.args[0])
    gift_code = str(request.args[0]).replace("%20", " ").replace("_", " ").upper()
    return dict(verify=verify(gift_code), check=check(gift_code), gift_code=gift_code)


def test_code():
    gift_code = request.args[0]
    gift_code = gift_code.replace("_", " ").upper()
    return dict(code=gift_code, check_real=check(gift_code),
                verify_real=verify(gift_code))


def verify_with_token():#gift_code, token
    try:
        project_code = "01"
        gift_code = request.args[0]
        gift_code = gift_code.replace("_", " ").upper()
        token = request.args[1]
        if len(request.args) > 2:
            project_code = request.args[2].upper()
            if project_code == "FPT":
                project_code = "F1"
        return verify_code(gift_code, project_code, token)
    except Exception as err:
        return dict(error="CB_0004", mess=CB_0004 + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def verify_code(gift_code, project_code, token):
    try:
        try:
            if gift_code[:2] == "01" or (project_code == "SS2016" and gift_code.startswith("1")):
                gift_fund = int(gift_code[1:4]) * 1000
            else:
                gift_fund = int(gift_code[2:4]) * 10000
        except Exception as err:
            print(err)
            return dict(error="CB_GCV_0002", mess=CB_GCV_0002)

        #Verify Gift code
        if not verify(gift_code):
            return dict(error="CB_GCV_0002", mess=CB_GCV_0002)

        #Kiem tra token hop le
        user = db(db.clsb_user.user_token == token).select()
        if len(user) == 0:
            return dict(error="CB_0012", mess=CB_0012)
        user_id = user.first()['id']

        #Kiem tra user nhap code chưa neu la ma samsung
        if project_code == "SS2016":
            user_use_gift = db(db.clsb30_gift_code_log.user_id == user_id)\
                    (db.clsb30_gift_code_log.project_code == project_code).select()
            if len(user_use_gift) > 0:
                return dict(error="CB_GCV_0001", mess="Bạn đã dùng mã ưu đãi " + str(len(user_use_gift)) + " lần. Bạn không thể dùng thêm nữa.")

        #Kiem tra gift code da su dung chua
        check_gift_use = db(db.clsb30_gift_code_log.gift_code == gift_code).select()
        if len(check_gift_use) > 0:
            return dict(error="CB_GCV_0003", mess=CB_GCV_0003)

        # Truong hop hop le, insert log
        old_fund = int(user.first()['fund'])
        new_fund = old_fund + gift_fund
        db(db.clsb_user.id == user_id).update(fund=new_fund)
        db.clsb30_gift_code_log.insert(user_id=user_id, gift_code=gift_code,
                                       project_code=project_code, code_value=gift_fund)
        return dict(result=True, fund=gift_fund,
                    mess="Chúc mừng bạn đã được cộng thêm " + str(gift_fund) + " đ vào tài khoản")
    except Exception as err:
        return dict(error="CB_0004", mess=CB_0004 + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def test_url():
    import urllib2
    get_data = urllib2.urlopen("https://www.nganluong.vn")
    return dict(data=get_data.read())

def check_available_user():#token
    try:
        #project_code = "01"
        #user_token = request.args[0]
        #if len(request.args) > 1:
        #    project_code = request.args[1]
        #user = db(db.clsb_user.user_token == user_token).select()
        #if len(user) == 0:
        #    return dict(result=False, error="ERROR TOKEN")
        #user_use_gift = db(db.clsb30_gift_code_log.user_id == user.first()['id'])\
        #        (db.clsb30_gift_code_log.project_code == project_code).select()
        #if len(user_use_gift) > 0:
        #    return dict(result=False, error="NOT AVAILABLE")
        return dict(result=True)
    except Exception as err:
        return dict(result=False, error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def payment_code():#code, token
    try:
        if request.args and len(request.args) > 0:
            gift_code = format_code(request.args[0]).upper()
            token = request.args[1]
            # if len(request.args) > 2:
            #     project_code = request.args[2].upper()
            # if gift_code[:2] == "IN":
            #     project_code = "IN"
        if request.vars and len(request.vars) > 0:
            gift_code = format_code(request.vars.code).upper()
            token = request.vars.user_token
            # if "project" in request.vars:
            #     project_code = request.vars.project
        if gift_code.startswith("K"):
            project_code = "K"
        elif gift_code.startswith("1150"):
            project_code = "SS2016"
        else:
            project_code = gift_code[:2]


        #Kiem tra token hop le
        user = db(db.clsb_user.user_token == token).select()
        if len(user) == 0:
            return dict(error="CB_0012", mess=CB_0012)
        user_id = user.first()['id']
        if project_code == "K":
            try:
                gift_fund = int(gift_code[2:4]) * 10000
            except Exception as err:
                return dict(error="CB_GCV_0002", mess="Mã thẻ không hợp lệ")
             #Verify Gift code
            if not verify(gift_code):
                return dict(error="CB_GCV_0002", mess="Mã thẻ không hợp lệ")
            #lay ma goi san pham
            collection = gift_code[1:2]
            #Kiem tra code da su dung chua
            check_use = db(db.cbcode_log.pin_code == gift_code).select()
            if len(check_use) > 0:
                return dict(error="CB_GCV_0003", mess="Mã thẻ đã được sử dụng")
            #Kiem tra tai khoan da nap code cho goi nay chua
            check_user_collect = db(db.cbcode_log.user_id == user_id)\
                (db.cbcode_log.collection_id == collection).select()
            bs = db(db.cbcode_collection.id == collection).select().first()
            if len(check_user_collect) > 0:
                return dict(error="CB_GCV_0003", mess="Tài khoản của bạn đã sở hữu bộ sách \"" +
                                                      bs['collection_name'] + "\" rồi")
            #Truong hop hop le
            adduser = add_to_user(user_id, collection)
            if 'error' in adduser:
                return dict(error="CB_0004", mess=adduser['error'])
            db.cbcode_log.insert(user_id=user_id,
                                 collection_id=collection,
                                 pin_code=gift_code,
                                 code_value=gift_fund,
                                 project=project_code)
            return dict(result=True, fund="bộ sách \"" + bs['collection_name'],
                        mess="Chúc mừng bạn đã sở hữu bộ sách \"" + bs['collection_name'] + "\"")
        else:
            return verify_code(gift_code, project_code, token)
    except Exception as err:
        return dict(error="CB_0004", mess=CB_0004 + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def add_to_user(user_id, collection_id):
    try:
        select_product = db(db.cbcode_product_collection.collection_id == collection_id) \
            (db.cbcode_product_collection.product_id == db.clsb_product.id).select()
        data_download_archieve = list()
        data_product_history = list()
        data_media_history = list()
        for p in select_product:
            temp_history = dict()
            temp_history['product_title'] = p['clsb_product']['product_title']
            temp_history['product_price'] = 0
            temp_history['product_id'] = p['clsb_product']['id']
            temp_history['category_id'] = p['clsb_product']['product_category']
            temp_history['user_id'] = user_id
            data_product_history.append(temp_history)
            select_quiz = db(db.clsb_product.product_code == "Exer" + p['clsb_product']['product_code']).select()
            if len(select_quiz) > 0:
                temp_quiz = dict()
                quiz = select_quiz.first()
                temp_quiz['product_title'] = quiz['product_title']
                temp_quiz['product_price'] = 0
                temp_quiz['product_id'] = quiz['id']
                temp_quiz['category_id'] = quiz['product_category']
                temp_quiz['user_id'] = user_id
                data_product_history.append(temp_quiz)
            temp_media = dict()
            temp_media['product_title'] = p['clsb_product']['product_title']
            temp_media['product_price'] = 0
            temp_media['product_id'] = p['clsb_product']['id']
            temp_media['category_id'] = p['clsb_product']['product_category']
            temp_media['user_id'] = user_id
            data_media_history.append(temp_media)
        db.clsb30_product_history.bulk_insert(data_product_history)
        db.clsb30_media_history.bulk_insert(data_media_history)
        return dict(r="SC")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


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


def thiquocgia():
    try:
        project_code = "T1"
        gift_code = request.vars.card
        token = request.vars.token
        discount_code = ""
        use_discount = False
        if "discount_code" in request.vars:
            discount_code = request.vars.discount_code
            if discount_code != "":
                check_code = check_tvt_code(discount_code)
                if check_code['result']:
                    use_discount = True
                else:
                    return dict(error="CB", mess=check_code['mess'])
        user = db(db.clsb_user.user_token == token).select()
        if len(user) == 0:
            return dict(error="CB_0012", mess="Lỗi thông tin đăng nhập")
        user_id = user.first()['id']
        username = user.first()['username']
        sum_pay = int(sum_pay_tqg(username)['total'])
        card_serial = ""
        import re
        gift_code = re.sub('[^a-zA-Z0-9 \n\.]', '', gift_code).upper().replace(" ", "")
        if len(gift_code) == 12:
            check_tqg = check_tqg_code(gift_code)
            if check_tqg['result']:
                card_serial = check_tqg['serial']
                gift_fund = check_tqg['value']
                gift_code = gift_code[:4] + " " + gift_code[4:8] + " " + gift_code[8:]
            else:
                return dict(error="CB_GCV", mess=check_tqg['mess'])
        else:
            gift_code = gift_code[:4] + " " + gift_code[4:8] + " " + gift_code[8:12] + " " + gift_code[12:]
            # card_serial = gift_code
            if not gift_code.startswith(project_code):
                return dict(error="CB_GCV_0002", mess="Mã thanh toán không hợp lệ")
            gift_fund = 0
            try:
                gift_fund = int(gift_code[2:4]) * 10000
            except Exception as err:
                print(err)
                return dict(error="CB_GCV_0002", mess="Mã thẻ không hợp lệ")
            #Verify Gift code
            if not verify(gift_code):
                return dict(error="CB_GCV_0002", mess="Mã thẻ không hợp lệ")
            check_gift_use = db(db.clsb30_gift_code_log.gift_code == gift_code).select()
            if len(check_gift_use) > 0:
                return dict(error="CB_GCV_0003", mess="CB_GCV_0003: Mã thanh toán đã được sử dụng")
            check_card_use = db(db.clsb30_tqg_card_log.card_pin == gift_code).select()
            if len(check_card_use) > 0:
                return dict(error="CB_GCV_0003", mess="CB_GCV_0003: Mã thanh toán đã được sử dụng")

        # Truong hop hop le, insert log
        card_fund = gift_fund
        if use_discount:
            if sum_pay < 750000:
                if sum_pay + gift_fund < 750000:
                    card_fund = gift_fund * 1.112
                else:
                    card_fund = (sum_pay + gift_fund - 750000) * 1.334 + \
                                (1000000 - int(sum_discount(username)['total']))
            else:
                card_fund = int(gift_fund * 1.334)
        tranfer  = tranfer_fund(user.first()['username'], card_fund)
        tranfer_result = True
        description="SUCCESS"
        if tranfer['type'] != 'success':
            description = tranfer['value']
            old_fund = int(user.first()['fund'])
            new_fund = old_fund + card_fund
            db(db.clsb_user.id == user_id).update(fund=new_fund)
            tranfer_result = False
        # db.clsb30_gift_code_log.insert(user_id=user_id, gift_code=gift_code, project_code=project_code, description=description)
        db.clsb30_tqg_card_log.insert(user_id=user_id, card_serial=card_serial, card_pin=gift_code,
                                      card_value=gift_fund, description=description)
        if use_discount:
            db.clsb30_tvt_log.insert(user_id=user_id, action_type="TQG_CARD",
                                    before_discount=gift_fund,
                                    after_discount=card_fund,
                                    time_used=datetime.now(),
                                    discount_code=discount_code)
        return dict(result=True, fund=card_fund, tranfer=tranfer_result)
    except Exception as err:
        return dict(error="CB_0004", mess=CB_0004 + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def test_tqg():
    try:
        return check_tqg_code(request.args[0])
    except Exception as err:
        return dict(result=False, mess=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def check_tqg_code(code):
    try:
        from datetime import datetime
        import hashlib
        hashcode = hashlib.md5(code).hexdigest()[-16:].upper()
        card_end = code[-4:]
        select_card = db(db.clsb30_tqg_card.hash_code.like(hashcode))\
            (db.clsb30_tqg_card.card_value.like(card_end)).select()
        if len(select_card) == 0:
            return dict(result=False, mess="Mã thẻ không tồn tại", hashcode=hashcode)
        card = select_card.first()
        if int(card['serial_activate']) == 0:
            return dict(result=False, mess="Thẻ chưa được kích hoạt")
        if card['time_valid'] is not None and card['time_valid'] < datetime.now():
            return dict(result=False, mess="Mã thẻ đã hết hạn sử dụng")
        code = code[:4] + " " + code[4:8] + " " + code[8:]
        check_card_use = db(db.clsb30_tqg_card_log.card_pin == code).select()
        if len(check_card_use) > 0:
            return dict(result=False, mess="Mã thẻ đã được sử dụng")
        value = int(card['card_serial'][:4]) * 1000
        return dict(result=True, value=value, hashcode=hashcode, serial=card['card_serial'])
    except Exception as err:
        return dict(result=False, mess=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def pay_tqg():
    try:
        project_code = "T1"
        gift_code = request.args[0]
        gift_code = gift_code.replace("_", "").upper()
        gift_code = gift_code.replace(" ", "")
        gift_code = gift_code[:4] + " " + gift_code[4:8] + " " + gift_code[8:12] + " " + gift_code[12:]
        if not gift_code.startswith(project_code):
            return dict(error="CB_GCV_0002", mess="CB_GCV_0002: Mã thanh toán không hợp lệ")
        token = request.args[1]
        gift_fund = 0
        try:
            gift_fund = int(gift_code[2:4]) * 10000
        except Exception as err:
            print(err)
            return dict(error="CB_GCV_0002", mess=CB_GCV_0002)
        #Kiem tra token hop le
        user = db(db.clsb_user.user_token == token).select()
        if len(user) == 0:
            return dict(error="CB_0012", mess=CB_0012)
        user_id = user.first()['id']

        #Verify Gift code
        if not verify(gift_code):
            return dict(error="CB_GCV_0002", mess="CB_GCV_0002: Mã thanh toán không hợp lệ")
        #print(gift_code)

        #Kiem tra gift code da su dung chua
        check_gift_use = db(db.clsb30_gift_code_log.gift_code == gift_code).select()
        if len(check_gift_use) > 0:
            return dict(error="CB_GCV_0003", mess="CB_GCV_0003: Mã thanh toán đã được sử dụng")

        # Truong hop hop le, insert log
        purchase_type = request.vars.purchase_type
        package = request.vars.package
        email = request.vars.email
        pack_type = request.vars.pack_type

        if purchase_type == "gift":
            url = 'http://thiquocgia.vn/userpanel/gift_ajax2.php'
            data = dict(email=email, gift=package, sesskey="trungdepzai", type=pack_type, username=user.first()['username'],
                        token=token, fund=gift_fund)
            r = requests.post(url, data=data, allow_redirects=True)
            result = json.loads(r.content)
        else:
            url = 'http://thiquocgia.vn/userpanel/service2.php'
            data = dict(package_code=package, sesskey="trungdepzai", type=pack_type, username=user.first()['username'],
                        token=token, fund=gift_fund)
            r = requests.post(url, data=data, allow_redirects=True)
            result = json.loads(r.content)
        if result['type'] == "success":
            db.clsb30_gift_code_log.insert(user_id=user_id, gift_code=gift_code, project_code=project_code)
            return dict(result=True)
        elif result['type'] == "charge":
            db.clsb30_gift_code_log.insert(user_id=user_id, gift_code=gift_code, project_code=project_code)
            return dict(error=result['value'])
        else:
            return dict(error=result['value'])
    except Exception as err:
        return dict(error="CB_0004", mess=CB_0004 + str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


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
        return dict(type='error', value=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def md5_string(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()


def format_code(code):
    try:
        code = code.replace(" ", "")
        import re
        nstr = re.sub(r'[?|$|.|!]',r'',code)
        print nstr
        nestr = re.sub(r'[^a-zA-Z0-9 ]',r'',nstr)
        result = ""
        for idx in range(0, len(nestr)):
            if idx % 4 == 0 and idx != 0:
                result += " "
            result += nestr[idx]
        return result
    except Exception as ex:
        return str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno)


def test_format():
    if request.args:
        return dict(code=format_code(request.args[0]))
    elif request.vars:
        return dict(code=format_code(request.vars.code))


def classbook_giftcode():
    try:
        code = request.vars.code

    except Exception as ex:
        return dict(result=False, mess=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def check_cb_gift(code):
    return dict(result=True)


def fix_fund_ss():
    try:
        select_log = db(db.clsb30_gift_code_log.gift_code.like("1150%"))\
            (db.clsb30_gift_code_log.code_value == 500000).select(db.clsb30_gift_code_log.user_id)
        user_ids = list()
        for log in select_log:
            user_ids.append(log[db.clsb30_gift_code_log.user_id])
        count = "COUNT(DISTINCT clsb30_gift_code_log.id)"
        select_user = db(db.clsb_user.id.belongs(user_ids))\
                (db.clsb_user.id == db.clsb30_gift_code_log.user_id)\
                (db.clsb30_gift_code_log.gift_code.like("1150%"))\
                (db.clsb30_gift_code_log.code_value == 500000).select(db.clsb_user.ALL, count,
                                                                      groupby=(db.clsb30_gift_code_log.user_id))
        users = list()
        for u in select_user:
            temp = dict()
            temp['id'] = u[db.clsb_user.id]
            temp['username'] = u[db.clsb_user.username]
            temp['fund'] = u[db.clsb_user.fund]
            temp['phone'] = u[db.clsb_user.phoneNumber]
            temp['firstName'] = u[db.clsb_user.firstName]
            temp['lastName'] = u[db.clsb_user.firstName]
            temp['count'] = u[count]
            new_fund = int(temp['fund']) - int(temp['count']) * 350000
            temp['new_fund'] = new_fund
            # db(db.clsb_user.id == temp['id']).update(fund=new_fund)
            users.append(temp)
        return dict(user_ids=user_ids)
    except Exception as ex:
        return dict(result=False, mess=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))