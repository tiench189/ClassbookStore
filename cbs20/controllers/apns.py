__author__ = 'Tien'
import ssl
import json
import socket
import struct
import binascii

def register():
    try:
        date_now = request.now
        user_email = request.vars.user_email
        apns_token = request.vars.apns_token

        check_exist = db(db.clsb30_apns.user_email == user_email)(db.clsb30_apns.apns_token == apns_token).select()
        check_token_exist = db(db.clsb30_apns.apns_token == apns_token).select()
        if len(check_exist) > 0:
            return dict(result=False, code='REGISTER_EXIST', mess="Email và token đã được đăng kí rồi")
        elif len(check_token_exist) > 0:
            db(db.clsb30_apns.apns_token == apns_token).update(user_email=user_email, date_modify=date_now)
            return dict(result=True, code='SUCCESS', mess="Cập nhật tài khoản thành công")
        else:
            db.clsb30_apns.insert(user_email=user_email,
                                  apns_token=apns_token,
                                  date_created=date_now,
                                  date_modify=date_now)
            return dict(result=True, code='SUCCESS', mess="Đăng kí thành công")
    except Exception as err:
        print(err)
        return dict(result=False, code='UNDEFINE_ERR', mess=str(err))

def get_ios_unique_key():
    try:
        user_name = request.vars.user_name
        user_token = request.vars.user_token

        return dict(result=True, time_valid=0, unique_key="CA942766bda2e47f", ios_id="813f2a4d8d1a882c")
    except Exception as err:
        print(err)
        return dict(result=False, error=str(err))

def test_apns():
    if len(request.args) == 0:
        return dict()
    print(request.args)
    token_hex = request.args[0]
    mess = str(request.args[1])
    ver = str(request.args[2])
    # mess = "s\u00E1ch m\u1EDBi"
    # mess = unicode(mess, "utf-8")
    # mess = mess.encode('ascii', 'replace')
    # number = int(request.args[2])
    try:
        from apns import APNs, Payload
        pem_file = settings.home_dir + "apns_dev.pem"
        apns = APNs(use_sandbox=True, cert_file=pem_file, key_file=pem_file)
        # product_list = list()
        # for i in range(0, number):
        custom = dict()
        product_list = list()
        product = dict()
        product['id'] = '519'
        product['code'] = '09GKGDCD'
        product['version'] = ver
        product_list.append(product)
        custom['product_list'] = product_list
        print(mess)
        # print(product_list)
        payload = Payload(alert=mess.encode('UTF-8'), badge=1, sound='default', custom=custom)
        print(payload)
        apns.gateway_server.send_notification(token_hex, payload)
        return dict(result=True)
    except Exception as err:
        print("error: " + str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(result=False, mess=err)

def send_push():
    token = request.args[0]
    payload = {
        'aps': {
            'alert': 'sách mới',
            'sound': 'default'
        }
    }
    cert = settings.home_dir + "apns_dev.pem"

    # APNS development server
    apns_address = ('gateway.sandbox.push.apple.com', 2195)

    # Use a socket to connect to APNS over SSL
    s = socket.socket()
    sock = ssl.wrap_socket(s, ssl_version=ssl.PROTOCOL_SSLv3, certfile=cert)
    sock.connect(apns_address)

    # Generate a notification packet
    token = binascii.unhexlify(token)
    fmt = '!cH32sH{0:d}s'.format(len(payload))
    cmd = '\x00'
    message = struct.pack(fmt, cmd, len(token), token, len(payload), payload)
    sock.write(message)
    sock.close()
