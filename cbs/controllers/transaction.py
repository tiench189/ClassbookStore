# coding=utf-8
import hashlib
import urllib2
import urllib3
import json
from datetime import datetime
from xml.dom import expatbuilder
import sys

sesskey = "trungdepzai"

nl_version = "3.1"
nl_function = "SetExpressCheckout"
nl_service = "https://www.nganluong.vn/checkout.api.nganluong.post.php"

nl_card_function = "CardCharge"
nl_card_version = "2.0"
nl_card_service = "http://exu.vn/mobile_card.api.post.v2.php"

# tk ducmanh86@gmail.com
# nl_merchant_id = '28528'
# nl_merchant_password = 'CLBVN2013@)!#'
# nl_receiver_email = 'ducmanh86@gmail.com'

# tk nganluong@tinhvan.com
nl_merchant_id = '30468'
nl_merchant_password = 'NL@20!#'
nl_receiver_email = 'nganluong@tinhvan.com'

nl_minimum_cost = 2000

TIME_OUT = timedelta(minutes=60)
table_transaction = 'clsb_transaction'
table_user = 'clsb_user'


# DOMAIN_VDC = "123.30.179.205"
# DOMAIN_VDC = "classbook.vn"


def nl_fetch_url(service_vars=None, method='POST', service=nl_service):
    if service == nl_service:
        http = urllib3.connection_from_url('https://www.nganluong.vn/')
    else:
        http = urllib3.connection_from_url('http://exu.vn/')
    fetch_data = http.request(method, service, service_vars)
    try:
        if fetch_data.status == 200:
            return fetch_data.data
        else:
            raise Exception(fetch_data.status)
    except Exception as ex:
        print "Error: " + str(ex)
        return None


class NganLuongCheckout(object):
    merchant_id = ''
    merchant_password = ''
    receiver_email = ''
    cur_code = 'vnd'

    def __init__(self, merchant_id, merchant_password, receiver_email):
        md5 = hashlib.md5()
        md5.update(merchant_password)
        self.merchant_password = md5.hexdigest()
        self.merchant_id = merchant_id
        self.receiver_email = receiver_email

    def get_transaction_detail(self, token):
        params = {
            'merchant_id': self.merchant_id,
            'merchant_password': self.merchant_password,
            'version': nl_version,
            'function': 'GetTransactionDetail',
            'token': token
        }
        result = nl_fetch_url(service_vars=params)
        if result is not None:
            try:
                result = result.replace('&', '&amp;')
                nl_xml = expatbuilder.parseString(result)
                data = dict(token=token)
                tags = nl_xml.getElementsByTagName("error_code")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["error_code"] = ""
                    else:
                        error_code = tags.item(0).firstChild.data
                        data["error_code"] = error_code
                        if not error_code == "00":
                            data["error_code"] = self.get_error_message(
                                error_code)
                else:
                    data["error_code"] = ""

                tags = nl_xml.getElementsByTagName("total_amount")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["total_amount"] = ""
                    else:
                        data["total_amount"] = tags.item(0).firstChild.data
                else:
                    data["total_amount"] = ""

                tags = nl_xml.getElementsByTagName("order_description")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["order_description"] = ""
                    else:
                        data["order_description"] = tags.item(0).firstChild.data
                else:
                    data["order_description"] = ""

                tags = nl_xml.getElementsByTagName("order_code")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["order_code"] = ""
                    else:
                        data["order_code"] = tags.item(0).firstChild.data
                else:
                    data["order_code"] = ""

                tags = nl_xml.getElementsByTagName("transaction_id")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["transaction_id"] = ""
                    else:
                        data["transaction_id"] = tags.item(0).firstChild.data
                else:
                    data["transaction_id"] = ""

                return data
            except Exception as ex:
                print "Error NganLuong: " + str(ex)
                return None
        return None

    def checkout(self, payment_method, bank_code, order_code, total_amount,
                 order_description,
                 return_url, cancel_url, buyer_fullname, buyer_email,
                 buyer_mobile, buyer_address):
        """
        Hàm lấy link thanh toán dùng số dư ví ngân lượng
        ===============================
        Tham số truyền vào bắt buộc phải có
                 order_code
                 total_amount
                 payment_method

                 buyer_fullname
                 buyer_email
                 buyer_mobile
        ===============================
         array_items mảng danh sách các item name theo quy tắc
         item_name1
         item_quantity1
         item_amount1
         item_url1
         .....

         payment_type Kiểu giao dịch:
            1 - Ngay;
            2 - Tạm giữ; Nếu không truyền hoặc bằng rỗng thì lấy theo chính
            sách của NganLuong.vn
        """
        params = {
            'cur_code': self.cur_code,
            'receiver_email': self.receiver_email,
            'function': nl_function,
            'version': nl_version,
            'merchant_id': self.merchant_id,
            # Mã merchant khai báo tại NganLuong.vn
            'merchant_password': self.merchant_password,
            # MD5(Mật khẩu kết nối giữa merchant và NganLuong.vn)
            'order_code': order_code,  # Mã hóa đơn do website bán hàng sinh ra
            'total_amount': total_amount,  # Tổng số tiền của hóa đơn
            'payment_method': payment_method,  # Phương thức thanh toán
            'bank_code': bank_code,  # Mã Ngân hàng
            'payment_type': 1,
            'order_description': order_description,  # Mô tả đơn hàng
            'tax_amount': 0,  # Tổng số tiền thuế
            'fee_shipping': 0,  # Phí vận chuyển
            'discount_amount': 0,  # Số tiền giảm giá
            'return_url': return_url,
            # Địa chỉ website nhận thông báo giao dịch thành công
            'cancel_url': cancel_url,  # Địa chỉ website nhận "Hủy giao dịch"
            'buyer_fullname': buyer_fullname,  # Tên người mua hàng
            'buyer_email': buyer_email,  # Địa chỉ Email người mua
            'buyer_mobile': buyer_mobile,  # Điện thoại người mua
            'buyer_address': buyer_address,  # Địa chỉ người mua hàng
        }

        result = nl_fetch_url(service_vars=params)
        get_error = NganLuongCheckout.get_error_message
        if result is not None:
            try:
                result = result.replace('&', '&amp;')
                nl_xml = expatbuilder.parseString(result)
                data = dict()
                tags = nl_xml.getElementsByTagName("error_code")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["error_code"] = ""
                    else:
                        error_code = tags.item(0).firstChild.data
                        data["error_code"] = error_code
                        if not error_code == "00":
                            data["error_code"] = get_error(error_code)
                else:
                    data["error_code"] = ""

                tags = nl_xml.getElementsByTagName("token")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["token"] = ""
                    else:
                        data["token"] = tags.item(0).firstChild.data
                else:
                    data["token"] = ""

                tags = nl_xml.getElementsByTagName("description")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["description"] = ""
                    else:
                        data["description"] = tags.item(0).firstChild.data
                else:
                    data["description"] = ""

                tags = nl_xml.getElementsByTagName("time_limit")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["time_limit"] = ""
                    else:
                        data["time_limit"] = tags.item(0).firstChild.data
                else:
                    data["time_limit"] = ""

                tags = nl_xml.getElementsByTagName("checkout_url")
                if tags.length > 0:
                    if tags.item(0).firstChild is None:
                        data["checkout_url"] = ""
                    else:
                        data["checkout_url"] = tags.item(0).firstChild.data
                else:
                    data["checkout_url"] = ""

                return data
            except Exception as ex:
                print "Error NganLuong: " + str(ex)
                return dict(error_code=str(ex))
        return None

    @staticmethod
    def get_error_message(error_code):
        arr_code = {
            "00": "Không có lỗi",
            "99": "Lỗi không được định nghĩa hoặc không rõ nguyên nhân",
            "01": "Lỗi tại NL nên không sinh được phiếu thu hoặc giao dịch",
            "02": "Địa chỉ IP của merchant gọi tới NL không được chấp nhận",
            "03": "Sai tham số gửi tới NL(sai tên hoặc kiểu dữ liệu)",
            "04": "Tên hàm API do merchant gọi tới không hợp lệ(không tồn tại)",
            "05": "Sai version của API",
            "06": "Mã merchant không tồn tại hoặc chưa được kích hoạt",
            "07": "Sai mật khẩu của merchant",
            "08": "Tài khoản người bán hàng không tồn tại",
            "09": "Tài khoản người nhận tiền đang bị phong tỏa",
            "10": "Hóa đơn thanh toán không hợp lệ",
            "11": "Số tiền thanh toán không hợp lệ",
            "12": "Đơn vị tiền tệ không hợp lệ",
            "13": "Sai số lượng sản phẩm",
            "14": "Tên sản phẩm không hợp lệ",
            "15": "Sai số lượng sản phẩm/hàng hóa trong chi tiết đơn hàng",
            "16": "Số tiền trong chi tiết đơn hàng không hợp lệ",
            "17": "Phương thức thanh toán không được hỗ trợ",
            "18": "Tài khoản hoặc mật khẩu NL không chính xác",
            "19": "Tài khoản người thanh toán đang bị phong tỏa",
            "20": "Số dư khả dụng không đủ thực hiện giao dịch",
            "21": "Giao dịch đã được thanh toán, không thể thực hiện lại",
            "22": "Ngân hàng từ chối thanh toán(do thẻ/tài khoản"
                  " ngân hàng bị khóa hoặc chưa đăng ký sử dụng dịch vụ IB)",
            "23": "Lỗi kết nối tới hệ thống Ngân hàng",
            "24": "Thẻ/tài khoản hết hạn sử dụng",
            "25": "Thẻ/Tài khoản không đủ số dư để thanh toán",
            "26": "Nhập sai tài khoản truy cập Internet-Banking",
            "27": "Nhập sai OTP quá số lần quy định",
            "28": "Lỗi chưa rõ nguyên nhân hoặc lỗi này chưa được mô tả",
            "29": "Mã token không tồn tại",
            "30": "Giao dịch không tồn tại "}
        try:
            return arr_code[error_code]
        except KeyError:
            return "Không xác định"


# 00|28528|ducmanh86@gmail.com|1125857563958|11323632797|VIETTEL|ducmanh86|
# Manh Tran Duc|ducmanh86@gmail.com|01656093458|10000|7800|3552550
class MobiCard:
    def __init__(self):
        pass

    @staticmethod
    def get_error_message(error_code):
        arr_code = {
            '00': 'Giao dịch thành công',
            '99': 'Lỗi chưa định nghĩa hoặc chưa xác định được nguyên nhân',
            '01': 'Lỗi địa chỉ IP truy cập API của NgânLượng.vn bị từ chối',
            '02': 'Lỗi tham số gọi từ merchant tới NL chưa chính xác ',
            '03': 'Mã merchant không tồn tại hoặc merchant đang bị khóa',
            '04': 'Mã checksum không chính xác (lỗi này thường xảy ra khi mật'
                  ' khẩu giao tiếp giữa merchant và NL không chính xác, hoặc'
                  ' cách sắp xếp các tham số trong biến params không đúng)',
            '05': 'Tài khoản nhận tiền nạp của merchant không tồn tại',
            '06': 'Tài khoản nhận tiền merchant đang bị khóa hoặc bị phong tảa,'
                  ' không thể thực hiện được giao dịch nạp tiền',
            '07': 'Thẻ đã được sử dụng ',
            '08': 'Thẻ bị khóa',
            '09': 'Thẻ hết hạn sử dụng',
            '10': 'Thẻ chưa được kích hoạt hoặc không tồn tại',
            '11': 'Mã thẻ sai định dạng',
            '12': 'Sai số serial của thẻ',
            '13': 'Mã thẻ và số serial không khớp',
            '14': 'Thẻ không tồn tại',
            '15': 'Thẻ không sử dụng được',
            '16': 'Số lần nhập sai liên tiếp của thẻ quá giới hạn cho phép',
            '17': 'Hệ thống Telco bị lỗi hoặc quá tải, thẻ chưa bị trừ',
            '18': 'Hệ thống Telco bị lỗi hoặc quá tải, thẻ có thể bị trừ,'
                  ' cần phối hợp với NgânLượng.vn để tra soát',
            '19': 'Kết nối từ NgânLượng.vn tới hệ thống Telco bị lỗi, '
                  'thẻ chưa bị trừ (thường do lỗi kết nối giữa NL với Telco, '
                  'ví dụ sai tham số kết nối, mà không liên quan đến merchant)',
            '20': 'Kết nối thành công, thẻ bị trừ nhưng chưa cộng tiền trên NL'
        }

        return arr_code[error_code]

    def card_pay(self, pin_card, card_serial, type_card, order_id,
                 client_fullname, client_mobile, client_email):
        md5 = hashlib.md5()
        md5.update(nl_merchant_id + "|" + nl_merchant_password)
        merchant_password = md5.hexdigest()
        params = {
            'func': nl_card_function,
            'version': nl_card_version,
            'merchant_id': nl_merchant_id,
            'merchant_password': merchant_password,
            'merchant_account': nl_receiver_email,
            'pin_card': pin_card,
            'card_serial': card_serial,
            'type_card': type_card,
            'ref_code': order_id,
            'client_fullname': client_fullname,
            'client_email': client_email,
            'client_mobile': client_mobile
        }

        result = nl_fetch_url(service_vars=params, service=nl_card_service)
        if result is not None:
            result = result.split('|')
            error_code = self.get_error_message(result[0]) \
                if not result[0] == "00" else result[0]
            data = {
                'error_code': error_code,
                'merchant_id': result[1],
                'merchant_account': result[2],
                'pin_card': result[3],
                'card_serial': result[4],
                'type_card': result[5],
                'order_id': result[6],
                'client_fullname': result[7],
                'client_email': result[8],
                'client_mobile': result[9],
                'card_amount': result[10],
                'amount': result[11],
                'transaction_id': result[12],
            }
            return data
        return None


@request.restful()
def index():
    from applications.cbs.modules.transaction import encrypt
    response.view = 'generic.json'

    def post(*args, **vas):
        """
            user_token
            username
            nl_function
            nl_version
            order_code
            total_amount
            payment_method,
        """
        if not len(args) == 1 or \
                (not args[0] == nl_function and not args[0] == nl_card_function):
            raise HTTP(400, "Function Error")
        else:
            function = args[0]

        if not "user_token" in vas or \
                not "user_name" in vas or not "version" in vas:
            raise HTTP(400, "Key Error")
        else:
            user_token = vas["user_token"]
            user_name = vas["user_name"]
            version = vas["version"]

        if (function == nl_function and not version == nl_version) or \
                (function == nl_card_function and not version == nl_card_version):
            raise HTTP(400, "Version Error")

        user_query = db((db[table_user].username == user_name) &
                        (db[table_user].user_token == user_token))
        user = user_query.select(db[table_user].lastLoginTime,
                                 db[table_user].email,
                                 db[table_user].phoneNumber,
                                 db[table_user].address,
                                 db[table_user].firstName,
                                 db[table_user].lastName,
                                 db[table_user].id)

        if len(user) == 0:
            raise HTTP(401)  # ValueError("Authentical Error")

        buyer_id = user[0].id
        buyer_email = user[0].email
        buyer_mobile = user[0].phoneNumber
        buyer_address = user[0].address
        buyer_fullname = "%s %s" % (user[0].firstName, user[0].lastName)

        if function == nl_function and version == nl_version:
            service = NganLuongCheckout(nl_merchant_id, nl_merchant_password,
                                        nl_receiver_email)
            if "token" in vas:
                nl_token = vas["token"]
                trans_token_count = db(
                    db.clsb_transaction.token == nl_token).count()
                if trans_token_count > 0:
                    raise HTTP(400, "Giao dịch đã tồn tại!")
                nl_data = service.get_transaction_detail(nl_token)
                if nl_data is not None:
                    error_code = nl_data["error_code"]
                    if not error_code == "00":
                        db(db.clsb_transaction.id == nl_data[
                            "order_code"]).update(status="FAIL",
                                                  token=error_code)
                        raise HTTP(400, error_code)
                    else:
                        try:
                            old_fund = db(db.clsb_user.id == buyer_id).select(
                                db.clsb_user.fund)[0].fund
                            if isinstance(old_fund, (int, long)):
                                new_fund = int(old_fund)
                                new_fund += int(nl_data["total_amount"])
                                data_sum = encrypt(new_fund, user_name)
                                db(db.clsb_user.id == buyer_id).update(
                                    fund=new_fund, data_sum=data_sum)
                            else:
                                return dict(error="Error fund")
                            order_code = nl_data["order_code"]
                            q = db(db.clsb_transaction.id == order_code)
                            payment_type = q.select().first()['payment_type']
                            amount = int(nl_data["total_amount"])
                            face_value = amount
                            real_value = amount
                            if payment_type == "VISA":
                                face_value = amount
                                real_value = amount * 0.97 - 5500
                            elif payment_type == "ATM_ONLINE":
                                face_value = amount
                                real_value = amount * 0.985 - 500
                            q.update(status="COMPLETE",
                                     amount=nl_data["total_amount"],
                                     token=nl_token,
                                     face_value=face_value,
                                     real_value=real_value,
                                     order_code=nl_data["order_code"],
                                     merchant_id=nl_data["transaction_id"])
                            return nl_data["total_amount"]
                        except Exception as ex:
                            raise HTTP(404, str(ex))
                else:
                    raise HTTP(400, "Undefine")
            elif "payment_method" in vas or "bank_code" in vas or \
                            "success_url" in vas or "cancel_url" in vas or \
                            "buyer_amount" in vas or "description" in vas:
                payment_method = vas["payment_method"]
                bank_code = vas["bank_code"]
                buyer_amount = vas["buyer_amount"]
                description = vas["description"]
                success_url = vas["success_url"]
                cancel_url = vas["cancel_url"]
                # print("nl: " + str(vas))
                if nl_minimum_cost > int(buyer_amount):
                    str_err = "Số tiền nạp ít nhất là %d VNĐ" % nl_minimum_cost
                    raise HTTP(400, str_err)

                mid = nl_merchant_id
                site = ""
                if "site" in vas:
                    site = vas['site']
                discount_code = ""
                if "discount_code" in vas:
                    discount_code = vas['discount_code']
                tid = db.clsb_transaction.insert(user_id=int(buyer_id),
                                                 merchant_account=mid,
                                                 amount=int(buyer_amount),
                                                 payment_type=payment_method,
                                                 description=description,
                                                 nl_version=version,
                                                 nl_function=function,
                                                 bank_code=bank_code,
                                                 site=site,
                                                 discount_code=discount_code)
                # if "purchase_type" in request.vars and request.vars.purchase_type != "":
                #     db.clsb30_elearning_transaction.insert(user_id=int(buyer_id),
                #                                            package_code=request.vars.package,
                #                                            purchase_type=request.vars.purchase_type,
                #                                            email_receiver=request.vars.email,
                #                                            pack_type=request.vars.pack_type,
                #                                            transaction_id=int(tid))
                db.commit()
                try:
                    nl_data = service.checkout(payment_method, bank_code,
                                               int(tid), int(buyer_amount),
                                               description,
                                               success_url, cancel_url,
                                               buyer_fullname, buyer_email,
                                               buyer_mobile, buyer_address)
                    if nl_data is not None:
                        error_code = nl_data["error_code"]
                        if not error_code == "00":
                            db(db.clsb_transaction.id == tid).update(
                                status="FAIL", token=error_code)
                            raise HTTP(400, error_code)
                        else:
                            return nl_data["checkout_url"]
                    else:
                        db(db.clsb_transaction.id == tid).update(status="FAIL")
                        raise HTTP(400, "Undefine")
                except Exception as ex:
                    db(db.clsb_transaction.id == tid).update(status="FAIL")
                    raise HTTP(400, str(ex))

        elif (function == nl_card_function and version == nl_card_version) and \
                ("pin_card" in vas or "card_serial" in vas or "type_card" in vas):
            pin_card = vas["pin_card"]
            card_serial = vas["card_serial"]
            type_card = vas["type_card"]
            site = ""
            if "site" in vas:
                site = vas['site']
            discount_code = ""
            if "discount_code" in vas:
                discount_code = vas['discount_code']
            card_service = MobiCard()
            tid = db.clsb_transaction.insert(user_id=int(buyer_id),
                                             merchant_account=nl_merchant_id,
                                             payment_type=type_card,
                                             nl_version=version,
                                             nl_function=function,
                                             card_serial=card_serial,
                                             card_pin=pin_card, site=site,
                                             discount_code=discount_code)
            # if "purchase_type" in request.vars and request.vars.purchase_type != "":
            #     db.clsb30_elearning_transaction.insert(user_id=int(buyer_id),
            #                                            package_code=request.vars.package,
            #                                            purchase_type=request.vars.purchase_type,
            #                                            email_receiver=request.vars.email,
            #                                            pack_type=request.vars.pack_type,
            #                                            transaction_id=int(tid))
            db.commit()
            nl_data = card_service.card_pay(pin_card, card_serial, type_card,
                                            int(tid),
                                            buyer_fullname, buyer_mobile,
                                            buyer_email)
            if nl_data is not None:
                # print(nl_data)
                error_code = nl_data["error_code"]
                #print(error_code)
                if error_code == "00":
                    try:
                        old_fund = db(db.clsb_user.email == buyer_email).select(
                            db.clsb_user.fund)[0]['fund']
                        if isinstance(old_fund, (int, long)):
                            new_fund = old_fund + int(nl_data["card_amount"])
                            data_sum = encrypt(new_fund, user_name)
                            db(db.clsb_user.id == buyer_id).update(
                                    fund=new_fund, data_sum=data_sum)
                        else:
                            raise HTTP(400, "Undefine")
                        db(db.clsb_transaction.id == tid).update(
                            status="COMPLETE", amount=nl_data["amount"],
                            card_amount=nl_data["card_amount"],
                            face_value=nl_data["card_amount"],
                            real_value=nl_data["amount"],
                            merchant_id=nl_data["transaction_id"])
                        return nl_data["card_amount"]
                    except Exception as ex:
                        print(str(ex) + str(sys.exc_traceback.tb_lineno))
                        raise HTTP(404, str(ex) + str(sys.exc_traceback.tb_lineno))
                else:
                    try:
                        db(db.clsb_transaction.id == tid).update(status="FAIL",
                                                                 token=error_code)
                        #print("error code " + error_code)
                        raise HTTP(300, error_code)
                    except Exception as ex:
                        print(str(ex) + str(sys.exc_traceback.tb_lineno))
                        raise HTTP(400, str(ex) + str(sys.exc_traceback.tb_lineno))

        raise HTTP(400, "Key Error")

    return locals()


def get_transaction_info():
    nl_checkout = NganLuongCheckout(nl_merchant_id, nl_merchant_password,
                                    nl_receiver_email)
    json_res = nl_checkout.get_transaction_detail(request.args[0])
    return dict(json=json_res)


def report_authorize(func):
    def wrapper():
        allowed_clients = ['192.168.56.81', '192.168.52.130', '192.168.52.129', '10.0.71.2']
        if str.startswith(request.env.http_host, '192.168.50.75') and request.client in allowed_clients:
            return func()
        else:
            raise HTTP(401, 'Bạn không có quyền truy cập vào khu vực này!')

    return wrapper


# @report_authorize
def report_card():
    this_month = datetime.today().month
    this_year = datetime.today().year
    if 'month' in request.vars:
        try:
            str_date = request.vars.month.split('-')
            cur_month = int(str_date[0])
            cur_year = int(str_date[1])
        except:
            raise HTTP(400, "Parameter is not valid!")
    else:
        cur_month = (this_month - 1) if this_month > 1 else this_month
        cur_year = this_year
    lst_date = list()
    for i in range(0, 12):
        if this_month - i > 0:
            lst_date.append('%d-%d' % (this_month - i, this_year))
        else:
            lst_date.append('%d-%d' % (12 + this_month - i, this_year - 1))
    lst_date.reverse()
    return dict(data=get_card_data(cur_month, cur_year), month='%d-%d' % (cur_month, cur_year), dates=lst_date)


# @report_authorize
def report_checkout():
    this_month = datetime.today().month
    this_year = datetime.today().year
    if 'month' in request.vars:
        try:
            str_date = request.vars.month.split('-')
            cur_month = int(str_date[0])
            cur_year = int(str_date[1])
        except:
            raise HTTP(400, "Parameter is not valid!")
    else:
        cur_month = (this_month - 1) if this_month > 1 else this_month
        cur_year = this_year
    lst_date = list()
    for i in range(0, 12):
        if this_month - i > 0:
            lst_date.append('%d-%d' % (this_month - i, this_year))
        else:
            lst_date.append('%d-%d' % (12 + this_month - i, this_year - 1))
    lst_date.reverse()
    return dict(data=get_checkout_data(cur_month, cur_year), month='%d-%d' % (cur_month, cur_year), dates=lst_date)


@report_authorize
def export():
    try:
        month = int(request.args[0])
        year = int(request.args[1])
    except:
        import traceback
        traceback.print_exc()
        raise HTTP(400, 'Parameter is not valid!')

    import xlwt
    from applications.cbs.modules.transaction import money
    book = xlwt.Workbook(encoding='utf-8')

    checkout_sheet = book.add_sheet("Checkout Report")
    checkout_sheet.col(0).width = 0x0d00 + 4
    for i in range(1, 11):
        checkout_sheet.col(i).width = 0x0d00 + 12

    card_sheet = book.add_sheet("Card Report")
    card_sheet.col(0).width = 0x0d00 + 4
    for i in range(1, 8):
        card_sheet.col(i).width = 0x0d00 + 12

    border = xlwt.Borders()
    border.left = 1
    border.right = 1
    border.top = 1
    border.bottom = 1

    center_alignment = xlwt.Alignment()
    center_alignment.horz = xlwt.Alignment.HORZ_CENTER
    center_alignment.vert = xlwt.Alignment.VERT_CENTER

    right_alignment = xlwt.Alignment()
    right_alignment.horz = xlwt.Alignment.HORZ_RIGHT
    right_alignment.vert = xlwt.Alignment.VERT_CENTER

    left_alignment = xlwt.Alignment()
    left_alignment.horz = xlwt.Alignment.HORZ_LEFT
    left_alignment.vert = xlwt.Alignment.VERT_CENTER

    style_header = xlwt.XFStyle()
    style_header.font.height = 16 * 20
    style_header.font.bold = True
    style_header.alignment = left_alignment

    style_table_head = xlwt.XFStyle()
    style_table_head.font.height = 12 * 20
    style_table_head.font.bold = True
    style_table_head.alignment = center_alignment
    style_table_head.borders = border

    style_table_cell = xlwt.XFStyle()
    style_table_cell.alignment = center_alignment
    style_table_cell.borders = border

    style_table_cell_right = xlwt.XFStyle()
    style_table_cell_right.alignment = right_alignment
    style_table_cell_right.borders = border

    ### Write report for checkout
    data = get_checkout_data(month, year)
    checkout_sheet.write_merge(0, 0, 0, 3, 'Ngân Lượng Report - Checkout', style_header)
    checkout_sheet.write_merge(2, 2, 0, 2, 'Xem report trong tháng %d-%d' % (month, year))

    checkout_sheet.write(3, 0, 'STT', style_table_head)
    checkout_sheet.write(3, 1, 'Mã HĐ', style_table_head)
    checkout_sheet.write(3, 2, 'Mã GD', style_table_head)
    checkout_sheet.write(3, 3, 'Loại GD', style_table_head)
    checkout_sheet.write(3, 4, 'Mã NH', style_table_head)
    checkout_sheet.write(3, 5, 'Số Tiền', style_table_head)
    checkout_sheet.write(3, 6, 'Phí GD', style_table_head)
    checkout_sheet.write(3, 7, 'Doanh Thu', style_table_head)
    checkout_sheet.write(3, 8, '% Phí', style_table_head)
    checkout_sheet.write(3, 9, 'Ngày GD', style_table_head)
    checkout_sheet.write(3, 10, 'Thời Gian', style_table_head)

    count = 0
    for d in data['trans']:
        count += 1
        checkout_sheet.write(count + 3, 0, count, style_table_cell)
        checkout_sheet.write(count + 3, 1, d.order_code, style_table_cell)
        checkout_sheet.write(count + 3, 2, d.merchant_id, style_table_cell)
        checkout_sheet.write(count + 3, 3, d.payment_type, style_table_cell)
        checkout_sheet.write(count + 3, 4, d.bank_code, style_table_cell)
        checkout_sheet.write(count + 3, 5, money(d.amount), style_table_cell_right)
        checkout_sheet.write(count + 3, 6, money(d.fee), style_table_cell_right)
        checkout_sheet.write(count + 3, 7, money(d.profit), style_table_cell_right)
        checkout_sheet.write(count + 3, 8, d.fee_ratio, style_table_cell)
        checkout_sheet.write(count + 3, 9, str(d.created_on.date()), style_table_cell)
        checkout_sheet.write(count + 3, 10, str(d.created_on.time()), style_table_cell)
    if count == 0:
        count += 1
        checkout_sheet.write_merge(count + 3, count + 3, 0, 10,
                                   "Không có giao dịch nào trong tháng này!", style_table_cell)

    checkout_sheet.write_merge(count + 4, count + 4, 0, 4, "TỔNG", style_table_head)
    checkout_sheet.write(count + 4, 5, money(data['total'].amount), style_table_cell_right)
    checkout_sheet.write(count + 4, 6, money(data['total'].fee), style_table_cell_right)
    checkout_sheet.write(count + 4, 7, money(data['total'].profit), style_table_cell_right)

    ### Write report for card
    data = get_card_data(month, year)
    card_sheet.write_merge(0, 0, 0, 3, 'Ngân Lượng Report - Card', style_header)
    card_sheet.write_merge(2, 2, 0, 2, 'Xem report trong tháng %d-%d' % (month, year))

    card_sheet.write(3, 0, 'STT', style_table_head)
    card_sheet.write(3, 1, 'Mã GD', style_table_head)
    card_sheet.write(3, 2, 'Loại Thẻ', style_table_head)
    card_sheet.write(3, 3, 'Mệnh Giá', style_table_head)
    card_sheet.write(3, 4, 'Phí GD', style_table_head)
    card_sheet.write(3, 5, 'Doanh Thu', style_table_head)
    card_sheet.write(3, 6, 'Ngày GD', style_table_head)
    card_sheet.write(3, 7, 'Thời Gian', style_table_head)

    count = 0
    for d in data['trans']:
        count += 1
        card_sheet.write(count + 3, 0, count, style_table_cell)
        card_sheet.write(count + 3, 1, d.merchant_id, style_table_cell)
        card_sheet.write(count + 3, 2, d.payment_type, style_table_cell)
        card_sheet.write(count + 3, 3, money(d.card_amount), style_table_cell_right)
        card_sheet.write(count + 3, 4, money(d.fee), style_table_cell_right)
        card_sheet.write(count + 3, 5, money(d.amount), style_table_cell_right)
        card_sheet.write(count + 3, 6, str(d.created_on.date()), style_table_cell)
        card_sheet.write(count + 3, 7, str(d.created_on.time()), style_table_cell)
    if count == 0:
        count += 1
        card_sheet.write_merge(count + 3, count + 3, 0, 7, "Không có giao dịch nào trong tháng này!", style_table_cell)

    card_sheet.write(count + 4, 0, 'STT', style_table_head)
    card_sheet.write(count + 4, 1, 'Nhà Mạng', style_table_head)
    card_sheet.write(count + 4, 2, 'Số Lượng', style_table_head)
    card_sheet.write(count + 4, 3, 'Tổng GD', style_table_head)
    card_sheet.write(count + 4, 4, 'Tổng Phí', style_table_head)
    card_sheet.write(count + 4, 5, 'Tổng Thu', style_table_head)
    card_sheet.write(count + 4, 6, '% Phí', style_table_head)

    card_sheet.write(count + 5, 0, 1, style_table_cell)
    card_sheet.write(count + 5, 1, "Viettel", style_table_cell)
    card_sheet.write(count + 5, 2, data['vtt'].card, style_table_cell)
    card_sheet.write(count + 5, 3, money(data['vtt'].amount), style_table_cell_right)
    card_sheet.write(count + 5, 4, money(data['vtt'].fee), style_table_cell_right)
    card_sheet.write(count + 5, 5, money(data['vtt'].profit), style_table_cell_right)
    card_sheet.write(count + 5, 6, "{0}%".format(data['vtt'].ratio), style_table_cell)

    card_sheet.write(count + 6, 0, 2, style_table_cell)
    card_sheet.write(count + 6, 1, "Mobiphone", style_table_cell)
    card_sheet.write(count + 6, 2, data['vms'].card, style_table_cell)
    card_sheet.write(count + 6, 3, money(data['vms'].amount), style_table_cell_right)
    card_sheet.write(count + 6, 4, money(data['vms'].fee), style_table_cell_right)
    card_sheet.write(count + 6, 5, money(data['vms'].profit), style_table_cell_right)
    card_sheet.write(count + 6, 6, "{0}%".format(data['vms'].ratio), style_table_cell)

    card_sheet.write(count + 7, 0, 3, style_table_cell)
    card_sheet.write(count + 7, 1, "Vinaphone", style_table_cell)
    card_sheet.write(count + 7, 2, data['vnp'].card, style_table_cell)
    card_sheet.write(count + 7, 3, money(data['vnp'].amount), style_table_cell_right)
    card_sheet.write(count + 7, 4, money(data['vnp'].fee), style_table_cell_right)
    card_sheet.write(count + 7, 5, money(data['vnp'].profit), style_table_cell_right)
    card_sheet.write(count + 7, 6, "{0}%".format(data['vnp'].ratio), style_table_cell)

    card_sheet.write_merge(count + 8, count + 8, 0, 1, "TỔNG", style_table_head)
    card_sheet.write(count + 8, 2, data['total'].card, style_table_cell)
    card_sheet.write(count + 8, 3, money(data['total'].amount), style_table_cell_right)
    card_sheet.write(count + 8, 4, money(data['total'].fee), style_table_cell_right)
    card_sheet.write(count + 8, 5, money(data['total'].profit), style_table_cell_right)

    import StringIO
    year = datetime.today().year
    output_xls = StringIO.StringIO()
    book.save(output_xls)
    response.headers['Content-type'] = 'application/vnd.ms-excel'
    response.headers['Content-Disposition'] = 'attachment; filename=report_nganluong_{0}_{1}.xls'.format(month, year)
    response.headers['Content-Title'] = 'report_nganluong_{0}_{1}.xls'.format(month, year)
    response.headers['Content-Length'] = output_xls.len
    return output_xls.getvalue()


def get_card_data(month=datetime.today().month, year=datetime.today().year):
    month = str(month) if len(str(month)) == 2 else "0%s" % str(month)
    year = str(year)
    query = db(db.clsb_transaction.created_on.like('%s-%s-%%' % (year, month)))
    query = query(db.clsb_transaction.status == 'COMPLETE')
    query = query(db.clsb_transaction.nl_function == 'CardCharge')
    data = query.select(db.clsb_transaction.merchant_id,
                        db.clsb_transaction.amount,
                        db.clsb_transaction.payment_type,
                        db.clsb_transaction.card_amount,
                        db.clsb_transaction.created_on)
    vms = Storage()
    vnp = Storage()
    vtt = Storage()
    vms.profit = 0
    vms.amount = 0
    vms.card = 0
    vnp.profit = 0
    vnp.amount = 0
    vnp.card = 0
    vtt.profit = 0
    vtt.amount = 0
    vtt.card = 0
    for d in data:
        if d.payment_type == "VMS":
            vms.profit += int(d.amount)
            vms.amount += int(d.card_amount)
            vms.card += 1
        if d.payment_type == "VNP":
            vnp.profit += int(d.amount)
            vnp.amount += int(d.card_amount)
            vnp.card += 1
        if d.payment_type == "VIETTEL":
            vtt.profit += int(d.amount)
            vtt.amount += int(d.card_amount)
            vtt.card += 1
        d.fee = d.card_amount - d.amount
    vtt.fee = vtt.amount - vtt.profit
    vms.fee = vms.amount - vms.profit
    vnp.fee = vnp.amount - vnp.profit
    vtt.ratio = float((vtt.amount - vtt.profit) * 100) / float(vtt.amount) if vtt.amount > 0 else 0
    vms.ratio = float((vms.amount - vms.profit) * 100) / float(vms.amount) if vms.amount > 0 else 0
    vnp.ratio = float((vnp.amount - vnp.profit) * 100) / float(vnp.amount) if vnp.amount > 0 else 0
    total = Storage()
    total.amount = vtt.amount + vms.amount + vnp.amount
    total.fee = vtt.fee + vms.fee + vnp.fee
    total.profit = vtt.profit + vms.profit + vnp.profit
    total.card = vtt.card + vms.card + vnp.card
    return dict(trans=data, vms=vms, vnp=vnp, vtt=vtt, total=total)


def get_checkout_data(month=datetime.today().month, year=datetime.today().year):
    month = str(month) if len(str(month)) == 2 else "0%s" % str(month)
    year = str(year)
    query = db(db.clsb_transaction.created_on.like('%s-%s-%%' % (year, month)))
    query = query(db.clsb_transaction.status == 'COMPLETE')
    query = query(db.clsb_transaction.nl_function == 'SetExpressCheckout')
    data = query.select(db.clsb_transaction.merchant_id,
                        db.clsb_transaction.order_code,
                        db.clsb_transaction.amount,
                        db.clsb_transaction.payment_type,
                        db.clsb_transaction.bank_code,
                        db.clsb_transaction.created_on)
    total = Storage()
    total.amount = 0
    total.fee = 0
    for d in data:
        total.amount += int(d.amount)
        d.fee_ratio = "5000 + 3%" if d.payment_type == "VISA" else "500 + 1.5%"
        d.fee = int(5000 + int(d.amount) * 0.03) if d.payment_type == "VISA" else int(500 + int(d.amount) * 0.015)
        d.profit = d.amount - d.fee
        total.fee += d.fee
    total.profit = total.amount - total.fee
    return dict(trans=data, total=total)


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
        from datetime import datetime
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
        return dict(total=total_nl + total_card, total_nl=total_nl, total_card=total_card)
    except Exception as err:
            return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
