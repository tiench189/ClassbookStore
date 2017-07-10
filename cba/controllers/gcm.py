# @auth.requires_login()
import json
import urllib2
import sys

@auth.requires_authorize()
def index():
    confirm_send_message = 'Bạn có chắc chắn muốn gửi thông báo tới các thiết bị đã chọn không?'
    # check_is_root()
    form = smartgrid(db.clsb_gcm, showbuttontext=False, selectable=lambda ids: select_for_send(ids))
    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Send message')
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
            "return confirm('" + confirm_send_message + "');"
    return dict(form=form)


def select_for_send(ids):
    redirect(URL('cba', 'gcm', 'send', args=ids))
    return

def send2samsung():
    try:
        session.list_gcm_id = list()
        session.list_device_serial = list()
        devices = db(db.clsb_gcm.serial.like("CA%")).select(db.clsb_gcm.id, db.clsb_gcm.serial, db.clsb_gcm.gcm_id)
        ids = list()
        for device in devices:
            session.list_gcm_id.append(device[db.clsb_gcm.gcm_id])
            session.list_device_serial.append(device[db.clsb_gcm.serial])
        redirect(URL('cba', 'gcm', 'send', vars=dict(samsung=True)))
        #return dict(serials=session.list_device_serial)
    except Exception as ex:
        print str(ex)
        return str(ex)  + " on line " + str(sys.exc_traceback.tb_lineno)

def send_cb_device():
    try:
        session.list_gcm_id = list()
        session.list_device_serial = list()
        devices = db(~db.clsb_gcm.serial.like("CA%")).select(db.clsb_gcm.id, db.clsb_gcm.serial, db.clsb_gcm.gcm_id)
        ids = list()
        for device in devices:
            session.list_gcm_id.append(device[db.clsb_gcm.gcm_id])
            session.list_device_serial.append(device[db.clsb_gcm.serial])
        redirect(URL('cba', 'gcm', 'send', vars=dict(samsung=False)))
        #return dict(serials=session.list_device_serial)
    except Exception as ex:
        print str(ex)
        return str(ex)  + " on line " + str(sys.exc_traceback.tb_lineno)
# @auth.requires_login()
@auth.requires_authorize()
def send():
    # check_is_root()
    split_gcm = list()
    link = ""
    if 'link' in request.vars:
        link = request.vars.link
    if 'samsung' not in request.vars:
        if "message" not in request.vars:
            list_device_serial = list()
            list_gcm_id = list()
            if request.args and len(request.args) > 0:
                for s in request.args:
                    device_serial = db(db.clsb_gcm.id == int(s)).select().first()
                    list_device_serial.append(device_serial['serial'])
                    list_gcm_id.append(device_serial['gcm_id'])
            else:
                db_gcm = db(db.clsb_gcm.id > 0).select()
                for gcm in db_gcm:
                    list_device_serial.append(gcm['serial'])
                    list_gcm_id.append(gcm['gcm_id'])
            session.list_device_serial = list_device_serial
            session.list_gcm_id = list_gcm_id
    if "message" in request.vars:
        message = request.vars.message
        list_gcm_id = list()
        list_gcm_id = session.list_gcm_id
        #         devices = db(db.clsb_gcm.serial in list_device).select(db.clsb_gcm.gcm_id)
        #
        #         dev_ids = list()
        #         for dev in devices:
        #             dev_ids.append(dev['gcm_id'])
        #             print 'Id cua device : ' + dev['gcm_id']
        #
        import urllib2
        size = 500
        split_gcm = [list_gcm_id[i:i+size] for i in range(0, len(list_gcm_id), size)]
        try:
            import json
        except ImportError:
            import simplejson as json
        #         for dev_ids in list_gcm_id :
        print message
        for list_split in split_gcm:
            url = 'https://android.googleapis.com/gcm/send'
            values = {"data": {"message": message, "link": link}, "registration_ids": list_split}
            headers = {'Authorization': 'key=' + GOOGLE_API_KEY, 'Content-Type': 'application/json'}
            try:
                data = json.dumps(values)
                req = urllib2.Request(url, data, headers)
                response = urllib2.urlopen(req)
                the_page = response.read()
                result = json.loads(the_page)
                #return result
            except Exception as ex:
                print str(ex)
                response.flash = "error"
                #return dict(error=str(ex))
    return dict(split_gcm=split_gcm)

def send_test():
    try:
        message = "abc"
        list_gcm_id = list()
        list_gcm_id.append("APA91bFOkQs3d8jfVFWkEWLR_l_HZzhMZCG_kDAo3gGZp9yyE2IJchtwINWCA2fWJYj-6CyWoaZSKVDZMLAYUPN6PARZDH895Lmxt8ue7j0av2m92pYvT1Jw3y6uDADa64ZGTgBodJYsJAX5jUo_T7e1PgPzfl47or9F8zEt4cdYPHnzxwrvNmw")
        send_gcm_multi(message, list_gcm_id)
        # url = 'https://android.googleapis.com/gcm/send'
        # values = {"data": {"message": message}, "registration_ids": list_gcm_id}
        # headers = {'Authorization': 'key=' + GOOGLE_API_KEY, 'Content-Type': 'application/json'}
        #
        # try:
        #     data = json.dumps(values)
        #     req = urllib2.Request(url, data, headers)
        #     response = urllib2.urlopen(req)
        #     the_page = response.read()
        #     result = json.loads(the_page)
        #     return result
        # except Exception as ex:
        #     print str(ex)
        #     return dict(error=str(ex))
    except Exception as err:
        print(err)
        return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
# @auth.requires_authorize()
def send_multiple():
    GCM_ON_TURN = 100
    try:
        mess = ''
        print(request.vars)
        if len(request.vars) > 0:
            mes = request.vars.message
            if 'ckAndroid' in request.vars:
                gcm = db(db.clsb_device.device_serial == db.clsb_gcm.serial).select(db.clsb_gcm.gcm_id, distinct=True).as_list()
                gcm_list = list()
                for g in gcm:
                    gcm_list.append(g['gcm_id'])
                print(len(gcm_list))
                list_gcm_list = [gcm_list[GCM_ON_TURN*i:GCM_ON_TURN*i+GCM_ON_TURN] for i in range(0,int(len(gcm_list)/GCM_ON_TURN))]
                if len(gcm_list) - int((len(gcm_list)/GCM_ON_TURN) * GCM_ON_TURN) > 0:
                    list_gcm_list.append(gcm_list[(len(gcm_list)/GCM_ON_TURN) * GCM_ON_TURN:len(gcm_list) - 1])
                print(len(list_gcm_list))
                for list_gcm in list_gcm_list:
                    send_gcm_multi(mes, list_gcm)
                mess = "Thành công Android"

            if 'ckIOS' in request.vars:
                apns = db(db.clsb30_apns).select().as_list()
                print(len(apns))
                for a in apns:
                    print(a['apns_token'])
                    send_apns(mes, a['apns_token'], dict())
                mess = "Thành công IOS"


            if 'records' in request.vars and 'ckAndroid' not in request.vars and 'ckIOS' not in request.vars:
                mes = request.vars.message
                list_id = list()
                if isinstance(request.vars.records, list):
                    for id in request.vars.records:
                        list_id.append(id)
                else:
                    list_id.append(request.vars.records)
                print(list_id)

                android = db(db.clsb_device.id.belongs(list_id))\
                        (db.clsb_device.device_serial == db.clsb_gcm.serial).select(db.clsb_gcm.gcm_id)
                list_android_gcm = list()

                if len(android) > 0:
                    for android_id in android:
                        list_android_gcm.append(android_id[db.clsb_gcm.gcm_id])
                    send_gcm_multi(mes, list_android_gcm)
                else:
                    print("Khong tim thay thiet bi android")

                ios =  db(db.clsb_device.id.belongs(list_id))\
                    (db.clsb_device.user_id == db.clsb_user.id)\
                    (db.clsb_user.email == db.clsb30_apns.user_email).select(db.clsb30_apns.apns_token)
                if len(ios) > 0:
                    for ios_id in ios:
                        send_apns(mes, ios_id[db.clsb30_apns.apns_token], dict())
                else:
                    print("Khong tim thay thiet bi ios")
                response.flash = "Success"
                mess = 'Thành công\n Android:' + str(android) + "\n IOS: " + str(ios)
        selectable = (lambda ids: execute_device_id(ids))
        fields = (db.clsb_device.id,
                      db.clsb_device.device_serial,
                      db.clsb_device.device_type,
                      db.clsb_device.device_name)
        form = SQLFORM.smartgrid(db.clsb_device, selectable=selectable, fields=fields, showbuttontext=False)
        return dict(result=True, form=form, mess=mess)
    except Exception as err:
        response.flash = 'Error: '+str(err) + " on line: "+str(sys.exc_traceback.tb_lineno)
        return dict(result=False, mess=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))

def send_apns(mess, token, custom):
    from apns import APNs, Payload
    pem_file = settings.home_dir + "apns_dev.pem"
    apns = APNs(use_sandbox=True, cert_file=pem_file, key_file=pem_file)
    payload = Payload(alert=mess, badge=1, sound='default', custom=custom)
    apns.gateway_server.send_notification(token, payload)

def send_gcm_multi(mess, list_gcm_id):
    url = 'https://android.googleapis.com/gcm/send'
    values = {"data": {"message": mess}, "registration_ids": list_gcm_id}
    headers = {'Authorization': 'key=' + GOOGLE_API_KEY, 'Content-Type': 'application/json'}

    try:
        data = json.dumps(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        result = json.loads(the_page)
    except Exception as ex:
        print str(ex)

#@auth.requires_authorize()
def send1():
    try:
        print session.product_id_list
        list_product = list()
        selectable = (lambda ids: execute_device_id(ids))
        fields = (db.clsb_device.id,
                      db.clsb_device.device_serial,
                      db.clsb_device.device_type,
                      db.clsb_device.device_name)
        form = SQLFORM.smartgrid(db.clsb_device, selectable= selectable, fields=fields,showbuttontext=False)
        product_arr = session.product_id_list.split(',')
        for product in product_arr:
            if product != '':
                temp = dict()
                product_info = db(db.clsb_product.id == product).select(db.clsb_product.product_code,
                                                                        db.clsb_product.product_title).first()
                temp['product_code'] = product_info['product_code']
                temp['product_title'] = product_info['product_title']
                temp['id'] = product
                list_product.append(temp)
        try:
            if "message" not in request.vars:

                session.device_id_list = ''

            if "message" in request.vars and request.vars.message != '':

                list_gcm_id = list()
                message = request.vars.message
                if 'ckSelectAll' in request.vars:
                    device_arr = []
                    device_list = db(db.clsb_gcm).select(db.clsb_gcm.gcm_id).as_list()
                    for device in device_list:
                        device_arr.append(device['gcm_id'])
                else:
                    device_arr = session.device_id_list.split(',')

                for device in device_arr:
                    if device != '':
                        device_serial = db(db.clsb_device.id == device).select(db.clsb_device.device_serial).first()
                        gcm_id = db(db.clsb_gcm.serial == device_serial['device_serial']).select(db.clsb_gcm.gcm_id).first()
                        list_gcm_id.append(gcm_id['gcm_id'])

                import urllib2

                try:
                    import thread
                    import json
                except ImportError:
                    import simplejson as json
                #         for dev_ids in list_gcm_id :
                product_arr = session.product_id_list.split(',')
                # get metadata named: version
                metadata_version = db(db.clsb_dic_metadata.metadata_name == 'version').select(db.clsb_dic_metadata.id).first()
                for product in product_arr:
                    if product == '':
                        continue

                    metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                                db.clsb_product_metadata.product_id == product)).select(
                                db.clsb_product_metadata.metadata_value).first()

                    if metadata_version_value is None:
                        metadata_version_value = dict()
                        metadata_version_value['metadata_value'] = 0

                    product_info = db(db.clsb_product.id == product).select(db.clsb_product.product_code,
                                                                            db.clsb_product.product_title).first()
                    #temp['version'] = metadata_version_value['metadata_value']
                    #temp['product_code'] = product_info['product_code']
                    #temp['product_title'] = product_info['product_title']
                    #temp['id'] = product


                    url = 'https://android.googleapis.com/gcm/send'
                    values = {"data": {"register":1, "content": message, "version":metadata_version_value['metadata_value'], "code": product_info['product_code']}, "registration_ids": list_gcm_id}
                    headers = {'Authorization': 'key=' + GOOGLE_API_KEY, 'Content-Type': 'application/json'}


                    data = json.dumps(values)
                    req = urllib2.Request(url, data, headers)
                    response = urllib2.urlopen(req)
                    the_page = response.read()
                    result = json.loads(the_page)

                    #thread.start_new_thread(send_gcm, (message,metadata_version_value['metadata_value'], product_info['product_code'], list_gcm_id ))
                #product_arr = session.product_id_list.split(',')
                #for product in product_arr:
                #    if product != '':
                #        temp = dict()
                #        product_info = db(db.clsb_product.id == product).select(db.clsb_product.product_code,
                #                                                                db.clsb_product.product_title).first()
                #        temp['product_code'] = product_info['product_code']
                #        temp['product_title'] = product_info['product_title']
                #        temp['id'] = product
                #        list_product.append(temp)
                session.product_id_list = ''
                #return result
        except Exception as ex:
            print str(ex)
            return dict(result=False, error=str(ex)  + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(result=True, list_product=list_product, form=form)
    except Exception as err:
        return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))


def send_gcm(message, metadata_version_value, code, list_gcm ):
    print message
    print metadata_version_value
    print code
    print list_gcm
    try:
        import json
        import urllib2
    except ImportError:
        import simplejson as json
    try:

        url = 'https://android.googleapis.com/gcm/send'
        values = {"data": {"register":1, "content": message, "version":metadata_version_value, "code": code, "registration_ids": list_gcm}}
        headers = {'Authorization': 'key=' + GOOGLE_API_KEY, 'Content-Type': 'application/json'}

        data = json.dumps(values)
        req = urllib2.Request(url, data, headers)
        response = urllib2.urlopen(req)
        the_page = response.read()
        result = json.loads(the_page)
    except Exception as e:
        print e


def execute_device_id():
    try:

        tmp = ''
        device_id = request.vars['device_id']
        device_list = session.device_id_list

        if device_list == '':
            tmp += device_id
            tmp += ','
            session.device_id_list = tmp
            return

        device_arr = device_list.split(",")

        if device_id in device_arr:
            str_tmp = ''

            for device in device_arr:
                if device == '' or device == device_id:
                    continue
                str_tmp += device
                str_tmp += ','

            session.device_id_list = str_tmp
            return

        device_list += device_id
        device_list += ','
        session.device_id_list = device_list
    except Exception as e:
        print e



def clear_session_device():

    if session.device_id_list:
        session.device_id_list = ''

    return dict()


def clear_session_product():

    if session.product_id_list:
        session.product_id_list = ''

    return dict()

def test_array():
    try:
        arr = []
        for i in range(0, 10):
            arr.append(i)
        return dict(result=arr)
    except Exception as err:
        return  dict(err=str(err))
