__author__ = 'Tien'

import sys
import datetime
import os.path

# Content

STREAM_PATH = "/home/www-data/web2py/applications/stream/static/"

def image():
    try:
        root_path = "/home/www-data/web2py/applications/stream/static/a0tech/a0tect/package/"
        image_type = request.args[0]
        pakage_id = request.args[1]
        response.headers['Content-Type'] = 'image'
        response.headers['Content-Disposition'] = "attachment; filename=thumb.png"
        return response.stream(open(root_path + image_type + "/" + pakage_id + ".png"))
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def teacher_avata():
    try:
        root_path = "/home/www-data/web2py/applications/stream/static/a0tech/a0tect/teacher/"
        teacher_id = request.args[0]
        response.headers['Content-Type'] = 'image'
        response.headers['Content-Disposition'] = "attachment; filename=avata.png"
        return response.stream(open(root_path + "/" + teacher_id + ".png"))
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_root_package():
    try:
        pakages = list()
        parent_id = None
        if request.args and len(request.args) > 0:
            parent_id = request.args[0]
        package_db = db(db.cbless_package.parent_id == parent_id).select(orderby=db.cbless_package.package_order)
        for package in package_db:
            temp = dict()
            temp['id'] = package['id']
            temp['package_name'] = package['package_name']
            temp['package_description'] = package['package_description']
            temp['thumb'] = '/cbs20/subscription/image/thumb/' + str(package['id'])
            temp['banner'] = '/cbs20/subscription/image/banner/' + str(package['id'])
            temp['video_overview'] = package['video_overview']
            pakages.append(temp)
        if parent_id is not None:
            root_package = db(db.cbless_package.id == parent_id).select(orderby=db.cbless_package.package_order)
            proot = root_package.first()
            temp = dict()
            temp['id'] = proot['id']
            temp['package_name'] = proot['package_name']
            temp['package_description'] = proot['package_description']
            temp['thumb'] = '/cbs20/subscription/image/thumb/' + str(proot['id'])
            temp['banner'] = '/cbs20/subscription/image/banner/' + str(proot['id'])
            temp['video_overview'] = proot['video_overview']
            pakages.append(temp)
        return dict(pakages=pakages)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_sub_package():
    try:
        pakages = list()
        parent_id = None
        if request.args and len(request.args) > 0:
            parent_id = request.args[0]
        package_db = db(db.cbless_package.parent_id == parent_id).select()
        for package in package_db:
            temp = dict()
            temp['id'] = package['id']
            temp['package_name'] = package['package_name']
            temp['package_description'] = package['package_description']
            temp['thumb'] = '/cbs20/subscription/image/thumb/' + str(package['id'])
            temp['banner'] = '/cbs20/subscription/image/banner/' + str(package['id'])
            temp['video_overview'] = package['video_overview']
            pakages.append(temp)
        return dict(pakages=pakages)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_tree_package():
    try:
        packages = get_package_child(None)
        return dict(packages=packages)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_package_child(parent_id):
    child_list = list()
    package_child = db(db.cbless_package.parent_id == parent_id).select()
    for child in package_child:
        temp = dict()
        temp['id'] = child['id']
        temp['package_name'] = child['package_name']
        temp['parent_id'] = parent_id
        temp['package_description'] = child['package_description']
        temp['child'] = get_package_child(child['id'])
        child_list.append(temp)
    return child_list

def get_pakage_by_parent():
    try:
        list_packages = list()
        parent_id = request.args[0]
        package_child = db(db.cbless_package.parent_id == parent_id).select(orderby=db.cbless_package.package_order)
        for child in package_child:
            temp = dict()
            temp['id'] = child['id']
            temp['package_name'] = child['package_name']
            temp['parent_id'] = parent_id
            temp['package_description'] = child['package_description']
            temp['items'] = get_item_from_package(child['id'])
            list_packages.append(temp)
        stk = dict()
        stk['id'] = '0'
        stk['package_name'] = "Sách tham khảo"
        stk['parent_id'] = parent_id
        stk['package_description'] = 'STK'
        relation_stk = db(db.cbless_relation_book.package_id == parent_id)\
                (db.cbless_relation_book.product_id == db.clsb_product.id)\
                (db.cbless_relation_book.relation_type == "STK").select()
        stk['items'] = list()
        if len(relation_stk) > 0:
            list_packages.append(stk)
        #
        dt = dict()
        dt['id'] = '0'
        dt['package_name'] = "Đề thi"
        dt['parent_id'] = parent_id
        dt['package_description'] = 'DT'
        relation_dt = db(db.cbless_relation_book.package_id == parent_id)\
                (db.cbless_relation_book.product_id == db.clsb_product.id)\
                (db.cbless_relation_book.relation_type == "STK").select()
        dt['items'] = list()
        if len(relation_dt) > 0:
            list_packages.append(dt)
        return dict(packages=list_packages)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_parent_root(package_id):
    try:
        parent = db(db.cbless_package.id == package_id).select()
        if len(parent) == 0:
            return 0
        parent_id = parent.first()['parent_id']
        if parent_id is None or parent_id == 1:
            return package_id
        return get_parent_root(parent_id)
    except Exception as err:
        return package_id

def get_item_from_package(package_id):
    list_item = list()
    parent_id = int(get_parent_root(package_id))
    items = db(db.cbless_item.package_id == package_id).select(orderby=db.cbless_item.item_order)
    parent_480 = [2, 3, 4, 5, 6]
    for item in items:
        temp = dict()
        temp['id'] = item['id']
        temp['title'] = item['title']
        temp['description'] = item['description']
        temp['item_path'] = item['item_path']
        if parent_id in parent_480:
            temp['item_path'] = str(item['item_path']).replace(".mp4", ".480.mp4")
        #path_480 = str(item['item_path']).replace(".mp4", ".480.mp4")
        #if os.path.exists(STREAM_PATH + path_480):
        #    temp['item_path'] = path_480
        temp['item_type'] = item['item_type']
        temp['presenter'] = item['presenter']
        temp['creator'] = item['creator']
        temp['publisher'] = item['publisher']
        list_item.append(temp)
    return list_item

def get_seek_notes(): #video_id
    try:
        notes = list()
        item_id = request.args[0]
        select_notes = db(db.cbless_item_seek_point.item_id == item_id).select(orderby=db.cbless_item_seek_point.seek_point)
        for note in select_notes:
            temp = dict()
            temp['point'] = note['seek_point']
            temp['label'] = note['seek_point_label']
            notes.append(temp)
        return dict(notes=notes)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_level_subscription(): #package_id
    try:
        package_id = request.args[0]
        package_price = db(db.cbless_package_price.package_id == package_id)\
                (db.cbless_package_price.level_id == db.cbless_subscription_level.id).select()
        data = list()
        for price in package_price:
            temp = dict()
            temp['level_id'] = price[db.cbless_package_price.level_id]
            temp['level_name'] = price[db.cbless_subscription_level.level_name]
            temp['duration'] = price[db.cbless_subscription_level.duration]
            temp['price'] = price[db.cbless_package_price.price]
            data.append(temp)
        return dict(package_price=data)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_relation_book():
    try:
        package_id = request.args[0]
        relation_type = request.args[1]
        relation_books = db(db.cbless_relation_book.package_id == package_id)\
                (db.cbless_relation_book.product_id == db.clsb_product.id)\
                (db.cbless_relation_book.relation_type == relation_type).select()
        list_item = list()
        for book in relation_books:
            temp = dict()
            temp['id'] = book[db.clsb_product.id]
            temp['title'] = book[db.clsb_product.product_title]
            temp['item_path'] = book[db.clsb_product.product_code]
            temp['item_type'] = "book"
            temp['price'] = book[db.clsb_product.product_price]
            list_item.append(temp)
        return dict(items=list_item)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_content_overview():
    try:
        list_packages = list()
        parent_id = request.args[0]
        package_group = db(db.cbless_package.parent_id == parent_id).select()
        for group in package_group:
            temp = dict()
            temp['id'] = group['id']
            temp['package_name'] = group['package_name']
            temp['parent_id'] = parent_id
            temp['package_description'] = group['package_description']
            list_child = list()
            package_child = db(db.cbless_package.parent_id == group['id']).select()
            for child in package_child:
                temp_child = dict()
                temp_child['id'] = child['id']
                temp_child['package_name'] = child['package_name']
                temp_child['parent_id'] = parent_id
                temp_child['package_description'] = child['package_description']
                list_child.append(temp_child)
            temp['children'] = list_child
            list_packages.append(temp)
        return dict(packages=list_packages)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def get_teacher_by_package():
    try:
        package_id = request.args[0]
        teacher_select = db(db.cbless_teacher_package.package_id == package_id)\
                (db.cbless_teacher_package.teacher_id == db.cbless_teacher.id).select()
        teachers = list()
        for teacher in teacher_select:
            temp = dict()
            temp['id'] = teacher[db.cbless_teacher.id]
            temp['teacher_name'] = teacher[db.cbless_teacher.teacher_name]
            temp['university'] = teacher[db.cbless_teacher.university]
            temp['description'] = teacher[db.cbless_teacher.description]
            temp['avata_url'] = "/cbs20/subscription/teacher_avata/" + str(teacher[db.cbless_teacher.id])
            teachers.append(temp)
        return dict(teachers=teachers)
    except Exception as ex:
        return dict(result=False, code="", mess=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))

###########################User###############################################
def active_subscription(): #user_token, package_id, level_id
    try:
        user_token = request.vars.user_token
        package_id = request.vars.package_id
        level_id = request.vars.level_id
        auto_renew = request.vars.auto_renew
        if auto_renew == "true":
            auto_renew = True
        else:
            auto_renew = False
        user = db(db.clsb_user.user_token == user_token).select()
        if len(user) == 0:
            return dict(result=False, code="INVALID_TOKEN", mess="Hết phiên đăng nhập")
        user = user.first()
        old_fund = int(user['fund'])
        package_price = db(db.cbless_package_price.package_id == package_id)\
                (db.cbless_package_price.level_id == level_id).select()
        price = int(package_price.first()['price'])

        level = db(db.cbless_subscription_level.id == level_id).select()
        duration = int(level.first()['duration'])

        if old_fund < price:
            return dict(result=False, code="NOT_ENOUGHT_FUND", mess="Tài khoản của bạn không đủ để thưc hiện thanh toán")
        new_fund = old_fund - price
        db(db.clsb_user.id == user['id']).update(fund=new_fund)
        time_end = datetime.datetime.now() + datetime.timedelta(days=duration)
        db.cbless_purcharsing.update_or_insert((db.cbless_purcharsing.user_id==user['id'])&(db.cbless_purcharsing.package_id==package_id),
                                               user_id=user['id'],
                                               package_id=package_id,
                                               subscription_level_id=level_id,
                                               time_active=datetime.datetime.now(),
                                               time_end=time_end,
                                               auto_renew=auto_renew)
        db.cbless_purcharsing_log.insert(user_id=user['id'],
                                    package_id=package_id,
                                    subscription_level_id=level_id,
                                    time_active=datetime.datetime.now(),
                                    time_end=time_end,
                                    auto_renew=auto_renew)
        return dict(result=True, time_end=time_end.strftime("%H:%M:%S %d-%m-%Y"))
    except Exception as ex:
        return dict(result=False, code="", mess=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))

def check_package_available_for_user():# user_token, package_id
    try:
        user_token = request.vars.user_token
        package_id = request.vars.package_id
        time_end = datetime.datetime.now()
        device_serial = ""
        if "device_serial" in request.vars:
            device_serial = request.vars.device_serial
        device = False
        if device_serial != "":
            check_device = db(db.a0tech_sms_pay_log.device_serial == device_serial)\
                    (db.a0tech_sms_pay_log.package_id == package_id)\
                    (db.a0tech_sms_pay_log.time_end > datetime.datetime.now()).select()
            if len(check_device) > 0:
                time_end = check_device.first()[db.a0tech_sms_pay_log.time_end]
                device = True
        user = db(db.clsb_user.user_token == user_token).select()
        if len(user) == 0:
            if not device:
                return dict(result=False, code="INVALID_TOKEN", mess="Hết phiên đăng nhập")
            else:
                return dict(result=True, time_end=time_end.strftime("%H:%M:%S %d-%m-%Y"))
        user = user.first()
        parent_id = db(db.cbless_package.id == package_id).select().first()['parent_id']
        parent = False
        if parent_id is not None:
            subscript_parent = db(db.cbless_purcharsing.user_id == user['id'])\
                (db.cbless_purcharsing.package_id == parent_id).select()
            if len(subscript_parent) > 0:
                parent_end = subscript_parent.first()['time_end']
                if parent_end > datetime.datetime.now():
                    parent = True
                    time_end = parent_end if parent_end > time_end else time_end
        check_subscript = db(db.cbless_purcharsing.user_id == user['id'])\
                (db.cbless_purcharsing.package_id == package_id).select()
        if len(check_subscript) == 0:
            if device or parent:
                return dict(result=True, time_end=time_end.strftime("%H:%M:%S %d-%m-%Y"))
            else:
                return dict(result=False, code="CHUA_MUA", mess="Chưa đăng kí thuê bao")
        package_end = check_subscript.first()['time_end']
        time_end = package_end if package_end > time_end else time_end
        if time_end < datetime.datetime.now():
            if device or parent:
                return dict(result=True, time_end=time_end.strftime("%H:%M:%S %d-%m-%Y"))
            else:
                return dict(result=False, code="HET_HAN", mess="Hết hạn thuê bao",
                        renew=check_subscript.first()['auto_renew'],
                        level=check_subscript.first()['subscription_level_id'])
        return dict(result=True, time_end=time_end.strftime("%H:%M:%S %d-%m-%Y"))
    except Exception as ex:
        return dict(result=False, code="", mess=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))

def active_buy_pay_code():
    try:
        device_serial = request.vars.device_serial
        package_id = request.vars.package_id
        pay_code = request.vars.pay_code

        query_valid_code = db(db.a0tech_sms_pay_code.paycode == pay_code)\
                (db.a0tech_sms_pay_code.package_id == db.cbless_package.id).select()
        if len(query_valid_code) == 0:
            return dict(result=False, code="INVALID_CODE", mess="Mã thanh toán không hợp lệ")
        if str(package_id) != str(query_valid_code.first()[db.cbless_package.id]):
            return dict(result=False, code="WRONG_PACKAGE", mess="Mã thanh toán dành cho gói " +
                                                                 query_valid_code.first()[db.cbless_package.package_name])
        query_used_code = db(db.a0tech_sms_pay_log.paycode == pay_code).select()
        if len(query_used_code) > 0:
            return dict(result=False, code="USED_CODE", mess="Mã thanh toán đã được sử dụng trên thiết bị khác")
        duration = query_valid_code.first()[db.a0tech_sms_pay_code.duration]
        time_end = datetime.datetime.now() + datetime.timedelta(days=duration)
        db.a0tech_sms_pay_log.insert(device_serial=device_serial,
                                     package_id=package_id,
                                     paycode=pay_code,
                                     time_active=datetime.datetime.now(),
                                     time_end=time_end)
        return dict(result=True, time_end=time_end.strftime("%H:%M:%S %d-%m-%Y"))
    except Exception as ex:
        return dict(result=False, code="", mess=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def sms_structure():
    try:
        map_pkg = dict()
        map_pkg['2'] = "LY"
        map_pkg['3'] = "HOA"
        map_pkg['4'] = "SINH"
        map_pkg['5'] = "TOAN"
        map_pkg['6'] = "ANH"
        package_id = request.args[0]
        structures = list()
        header7 = dict()
        header7['number'] = "8775"
        header7['duration'] = "7 ngày"
        header7['structure'] = "AT " + map_pkg[package_id]
        header7['price'] = "15.000đ"
        structures.append(header7)
        header6 = dict()
        header6['number'] = "8675"
        header6['duration'] = "3 ngày"
        header6['structure'] = "AT " + map_pkg[package_id]
        header6['price'] = "10.000đ"
        structures.append(header6)
        header5 = dict()
        header5['number'] = "8575"
        header5['duration'] = "1 ngày"
        header5['structure'] = "AT " + map_pkg[package_id]
        header5['price'] = "5.000đ"
        structures.append(header5)
        return dict(structures=structures)
    except Exception as ex:
        return dict(result=False, code="", mess=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


from A0techSMS import SMSCode


@request.restful() #Luu y: bat buoc
def get_a0tec_sms_pay_code():

    '''
    $id = $_POST["MessageID"];
    $number = $_POST["SendNumber"];
    $service = $_POST["ServiceNumber"];
    $info = $_POST["Info"];
    $gendate = $_POST["GenDate"];

    <root>
        <Message Type="1" >(MT tính cước)
            <ReceiverNumber>84977575686</ReceiverNumber> (Số máy người nhận)
            <Info>Chao mung toi 8x75!</Info> (Nội dung text)
            <ContentType>0</ContentType> (Loại nội dung là text)
        </Message>
           <Message Type="2">(MT không tham gia tính cước)
                <ReceiverNumber>84977575686</ReceiverNumber> (Số máy người nhận)
                <Info> Nhac chuong:http://8x75.vn/download.jsp?param=123456</Info> (link  wappush)
                <ContentType>8</ContentType> (Loại nội dung là wappush)
           </Message>
    </root>

    '''

    def GET(*args, **vars):

        return "Trang này không tồn tại!"

    def POST(*args, **vars):

        response.headers['Content-Type'] = 'text/xml'

        try:

            if len(vars) < 4:

                return "Reques not valid"

            msgid = vars['MessageID']
            sendnum = vars['SendNumber']
            info = vars['Info']
            service_num = vars['ServiceNumber']


            package_id = 0

            #process info
            info = info.strip()

            info_arr = info.split()  #default is space

            if len(info_arr) < 2:
                message = '<?xml version="1.0" ?>' \
                          '<root><Message Type = "0">' \
                          '<ReceiverNumber>' + sendnum + '</ReceiverNumber>' \
                                                         '<Info>Tin nhan sai cu phap, ban se khong bi tru tien.' \
                                                         'Lien he p.CSKH: 0473020888 de duoc ho tro' \
                          '</Info>' \
                          '<ContentType>0</ContentType> ' \
                          '</Message>' \
                          '</root>'
                return message

            prefix = info_arr[0].strip()
            posfix = info_arr[1].strip()

            if not (prefix.lower() == 'at'):
                message = '<?xml version="1.0" ?>' \
                          '<root><Message Type = "0">' \
                          '<ReceiverNumber>' + sendnum + '</ReceiverNumber>' \
                                                         '<Info>Tin nhan sai cu phap, ban se khong bi tru tien.' \
                                                         'Lien he p.CSKH: 0473020888 de duoc ho tro' \
                          '</Info>' \
                          '<ContentType>0</ContentType> ' \
                          '</Message>' \
                          '</root>'
                return message

            if posfix.lower() == 'ly':
                package_id = 2
            elif posfix.lower() == 'hoa':
                package_id = 3
            elif posfix.lower() == 'sinh':
                package_id = 4
            elif posfix.lower() == 'toan':
                package_id = 5
            elif posfix.lower() == 'anh':
                package_id = 6
            else:
                message = '<?xml version="1.0" ?>' \
                          '<root><Message Type = "0">' \
                          '<ReceiverNumber>' + sendnum + '</ReceiverNumber>' \
                                                         '<Info>Tin nhan sai cu phap, ban se khong bi tru tien.' \
                                                         'Lien he p.CSKH: 0473020888 de duoc ho tro' \
                          '</Info>' \
                          '<ContentType>0</ContentType> ' \
                          '</Message>' \
                          '</root>'
                return message
            #Phan biet dau so
            if service_num == '8775':
                duration_val = 7
            elif service_num == '8675':
                duration_val = 3
            elif service_num == '8575':
                duration_val = 1

            smcode = SMSCode(msgid, sendnum)

            try:

                row = db((db.a0tech_sms_pay_code.send_number == sendnum) & (db.a0tech_sms_pay_code.message_id == msgid)).select().first()

                if row is None:

                    exist_code = smcode.gen_sms_pay_code()
                    db.a0tech_sms_pay_code.insert(package_id=package_id,
                                                  paycode=exist_code,
                                                  send_number=sendnum,
                                                  service_number=service_num,
                                                  duration=duration_val,
                                                  message_id=msgid)
                else:
                    exist_code = row['paycode']

                message = '<?xml version="1.0" ?>'\
                          '<root><Message Type = "1">' \
                          '<ReceiverNumber>' + sendnum + '</ReceiverNumber>' \
                          '<Info>Ban da dang ky hoc thanh cong mon ' + posfix.upper() + '(thoi han: ' + str(duration_val) + \
                          ' ngay), PM Luyen thi vao 10 chuyen. Ma kich hoat cua ban la:' + \
                          exist_code + '</Info>' \
                          '<ContentType>0</ContentType> ' \
                          '</Message>' \
                          '</root>'

            except Exception as ex:

                print ex.message
                message = '<?xml version="1.0" ?>' \
                          '<root><Message Type = "0">' \
                          '<ReceiverNumber>' + sendnum + '</ReceiverNumber>' \
                          '<Info>Da co loi xay ra.' \
                          ' Ban se khong bi tru tien. Lien he p.CSKH: 0473020888 de duoc ho tro' \
                          '</Info>' \
                          '<ContentType>0</ContentType> ' \
                          '</Message>' \
                          '</root>'

            #from gluon.serializers import xml
            #response.write(message, escape=False)
            return message
        except Exception as ex:
            return ex.message
    return locals()
    #return dict(paycode=msg1)
