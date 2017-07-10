# coding=utf-8

import json
import urllib3
import CaptchasDotNet


######SERVICE GET FUNCTIONS######

#########TienCH##################
def service_buy_history():
    return fetch_url(settings.service_buy_history, service_args=['STORE_WEB', 'SERIAL', session.token])


def service_feature_image(product_code):
    return fetch_url(settings.service_feature_image, service_args=[product_code])


def service_submit_add_free_product(token, product_code):
    return fetch_url(settings.service_add_free_product, service_vars=dict(token=token, product_code=product_code))


def service_get_free_added(token):
    test = fetch_url(settings.service_get_free_product, service_vars=dict(token=token))
    return  test


def service_check_product(product_code, token):
    return fetch_url(settings.service_check_user_product, service_vars=dict(product_code=product_code, token=token))


def service_check_elearning(username):
    return fetch_url(settings.service_check_elearning, service_vars=dict(username=username))


def service_check_free_cp(product_code):
    return fetch_url(settings.service_check_free_cp, service_args=[product_code])


def check_buy_product(product_id):
    return fetch_url(settings.check_buy_product_20, service_args=[product_id, session.token])


def check_buy_quiz(product_id):
    return fetch_url(settings.check_buy_quiz, service_args=[product_id, session.token])


def check_buy_media(product_id):
    return fetch_url(settings.check_buy_media, service_args=[product_id, session.token])


def service_get_info_by_code(code):
    return fetch_url(settings.service_get_info_by_code, service_args=[code, "WEB", "WEB"])


def service_get_data_price(product_id):
    return fetch_url(settings.service_get_data_price, service_args=[product_id])


def service_check_payment(args):
    return fetch_url(settings.service_check_payment, service_args=args)


def get_list_media(product_code):
    return fetch_url(settings.get_list_media, service_args=[product_code])


def service_buy_product(args):
    return fetch_url(settings.service_buy_product, service_args=args)


def service_buy_product_divide(args):
    return fetch_url(settings.service_buy_product_divide, service_args=args)


def service_check_classbook_device(device_serial):
    return fetch_url(settings.service_check_classbook, service_args=device_serial, method="GET")


def check_available_payment(pay):
    return fetch_url(settings.service_check_available_payment, service_args=[session.token, pay])


def get_detail_list(args, vars):
    return fetch_url(settings.service_get_detail_list, service_args=args, service_vars=vars)


def service_login_fb(access_token):
    return fetch_url(settings.service_login_fb, service_vars=dict(access_token=access_token))


def service_login_gg(access_token):
    return fetch_url(settings.service_login_gg, service_vars=dict(access_token=access_token))


def service_category_top_item(args):
    return fetch_url(settings.service_category_top_item, service_args=args, service_vars={'version': 'STORE_WEB'})


def service_solr_search(vars):
    return fetch_url(settings.service_solr_search, service_vars=vars)


def service_product_by_cp(vars):
    vars['version'] = 'STORE_WEB'
    return fetch_url(settings.service_product_by_cp, service_vars=vars)


def service_product_by_creator(vars):
    vars['version'] = 'STORE_WEB'
    return fetch_url(settings.service_product_by_creator, service_vars=vars)


def service_product_by_publisher(vars):
    vars['version'] = 'STORE_WEB'
    return fetch_url(settings.service_product_by_publisher, service_vars=vars)


def service_auto_get_relation(product_id):
    vars = dict()
    vars['product_id'] = product_id
    vars['version'] = 'STORE_WEB'
    return fetch_url(settings.service_auto_get_relation, service_vars=vars)


def service_set_info(vars):
    return fetch_url(settings.service_set_info, service_vars=vars)


def service_get_published_topic():
    return fetch_url(settings.service_get_published_topic)


def service_check_preview(product_code):
    return fetch_url(settings.service_check_preview, service_args=[product_code])


def service_gcv_thiquocgia(tqg_card, discount_code=""):
    return fetch_url(settings.service_gcv_thiquocgia, service_vars=dict(card=tqg_card, token=session.token,
                                                                        discount_code=discount_code))


def service_gcv_pay_tqg(tqg_card, purchase_type, package, email, pack_type):
    return fetch_url(settings.service_gcv_pay_tqg, service_args=[tqg_card, session.token],
                     service_vars=dict(purchase_type=purchase_type,
                                       package=package, email=email,
                                       pack_type=pack_type))


def service_tranfer_thiquocgia(fund, real_fund, discount_code=""):
    return fetch_url(settings.service_tranfer_thiquocgia, service_vars=dict(user_token=session.token, fund=fund,
                                                                            real_fund=real_fund, discount_code=discount_code))


def service_tqg_tranfer_pay(purchase_type, package, email, pack_type, fund):
    return fetch_url3(settings.service_tqg_tranfer_pay, service_vars=dict(purchase_type=purchase_type,
                                                                          user_token=session.token,
                                                                          package=package, email=email,
                                                                          pack_type=pack_type, fund=fund))


def service_chuyen_de():
    return fetch_url(settings.service_chuyen_de)


def service_tranfer_to_tqg(username):
    return fetch_url(settings.service_tranfer_to_tqg, service_vars=dict(username=username))


def service_tranfer_to_third(username, service_tranfer):
    return fetch_url(settings.service_tranfer_to_third, service_vars=dict(username=username, service_tranfer=service_tranfer))


def service_bai_tap_chuyen_de(exer_code):
    return fetch_url(settings.service_bai_tap_chuyen_de, service_args=[exer_code])


def service_auto_login(username, secret, password, firstName, lastName, email, phoneNumber,
                       address, type_user, site_back):
    return fetch_url(settings.service_auto_login, service_vars=dict(username=username,
                                                                    secret=secret,
                                                                    password=password,
                                                                    firstName=firstName,
                                                                    lastName=lastName,
                                                                    email=email,
                                                                    phoneNumber=phoneNumber,
                                                                    address=address,
                                                                    type_user=type_user,
                                                                    site_back=site_back))


def service_auto_login_third(username, secret, password, firstName, lastName, email, phoneNumber,
                       address, type_user, site_back):
    return fetch_url(settings.service_auto_login_third, service_vars=dict(username=username,
                                                                    secret=secret,
                                                                    password=password,
                                                                    firstName=firstName,
                                                                    lastName=lastName,
                                                                    email=email,
                                                                    phoneNumber=phoneNumber,
                                                                    address=address,
                                                                    type_user=type_user,
                                                                    site_back=site_back))


def service_check_tvt_code(code):
    return fetch_url(settings.service_check_tvt_code, service_vars=dict(code=code))


def service_sum_pay_tqg(username):
    return fetch_url(settings.service_sum_pay_tqg, service_vars=dict(username=username))


def service_get_exam(exam_index):
    return fetch_url(settings.service_get_exam, service_vars=dict(exam=exam_index))


def service_get_active_exam():
    return fetch_url(settings.service_get_active_exam)


def service_changepass(oldpass, newpass):
    return fetch_url(settings.service_changepass, service_vars=dict(old=oldpass, new=newpass,
                                                                    username=session.username, user_token=session.token))


def service_payment_code(code):
    return fetch_url(settings.service_payment_code, service_vars=dict(code=code, user_token=session.token))

#########END TienCH##############

def service_check_media(product_code):
    return fetch_url(settings.service_check_media, service_args=[product_code])

def service_user_info(username):
    return fetch_url(settings.service_user_info, service_args=[username, session.token])


def service_get_device_detail(device_serial):
    return fetch_url(settings.service_get_device_detail, service_vars=dict(device_serial=device_serial))


def service_user_download(username):
    return fetch_url(settings.service_user_download, service_args=[username, session.token])


def service_user_get_warranty_history(username, field, value):
    return fetch_url(settings.service_user_get_warranty_history, service_args=[username, session.token, field, value])


def service_get_warranty_history(username, token):
    return fetch_url(settings.service_get_warranty_history, service_vars=dict(username=username, token=token),
                     method="POST")


def service_get_list_user_device(username, token):
    return fetch_url(settings.service_user_device, service_args=[username, token])


def service_order_send(email, hoten, dienthoai, number_devices, dia_chi, noi_dung, province, district):
    service_vars = {'email': email, 'customer_name': hoten, 'phone': dienthoai, 'number_devices': number_devices,
                    'address': dia_chi, 'note': noi_dung, 'province': province, 'district': district}
    return fetch_url(settings.service_order_send, service_vars=service_vars)


def service_comment_send(email, binh_luan, product_code, status):
    service_vars = {'email': email, 'comment_content': binh_luan, 'product_code': product_code, 'status': status}
    return fetch_url(settings.service_comment_send, service_vars=service_vars)


def service_device(serial):
    return fetch_url(settings.service_device, service_args=[serial])


def service_device_registed(serial):
    return fetch_url(settings.service_device_registed, service_args=[serial])


def service_user_auth(username, password):
    service_vars = {'username': username, 'password': password}
    return fetch_url(settings.service_user_auth, service_vars=service_vars)


def service_change_device_name(device_serial, new_device_name):
    service_vars = {'device_serial': device_serial, 'new_device_name': new_device_name}
    return fetch_url(settings.service_change_device_name, service_vars=service_vars)


def service_confirm_password(password, username, token):
    service_args = [username, password, token]
    return fetch_url(settings.service_confirm_password, service_args=service_args)


def service_check_user_buy_a_book(username, product_id, token):
    print 'call me'
    service_args = [username, product_id, token]
    print 'call me ok'
    return fetch_url(settings.service_check_buy_product, service_args=service_args)


def service_delete_device(username, device_serial, token):
    service_vars = {'username': username, 'device_serial': device_serial, 'user_token': token}
    return fetch_url(settings.service_delete_device, service_vars=service_vars)


def service_verify_token_rspwd(token_rs_pwd):
    service_args = [token_rs_pwd]
    return fetch_url(settings.service_verify_request_rspwd, service_args=service_args)


def service_renew_pwd(token_rs_pwd, newPwd):
    service_args = [token_rs_pwd, newPwd]
    return fetch_url(settings.service_renew_pwd, service_args=service_args)

def service_category_get():
    return fetch_url(settings.service_category_get)


def service_category_getall():
    return fetch_url(settings.service_category_getall)


def service_product_get(args):
    return fetch_url(settings.service_product_get, service_args=args, service_vars={'version': 'STORE_WEB'})


def service_product_search(store_search, args):
    return fetch_url(settings.service_product_search, service_args=args, service_vars={'store_search': store_search, 'version': 'STORE_WEB'})


def service_product_search_by_creator(creator_name, args):
    return fetch_url(settings.service_product_search_by_creator, service_args=args,
                     service_vars={'creator_name': creator_name})

# def service_product_search_advance(field_name, field_value, args):
#     return fetch_url(settings.service_product_search_advance, service_args=args,
#                      service_vars={field_name: field_value})

def service_product_search_advance(args, vars):
    vars['version'] = "STORE_WEB"
    print 'cbw function ' + str(vars)
    return fetch_url(settings.service_product_search_advance, service_args=args,
                     service_vars=vars)


def service_product_info(product_id):
    return fetch_url(settings.service_product_info, service_args=[product_id, 'web'])

def service_product_all(product_id):
    return fetch_url(settings.service_product_all, service_args=[product_id, 'web'])


def service_product_getquizinfo(args):
    return fetch_url(settings.service_product_getquizinfo, service_args=args)


def service_comment_info(product_code):
    return fetch_url(settings.service_comment_info, service_args=product_code)


def service_product_relation(product_id):
    return fetch_url(settings.service_product_relation, service_args=product_id)


def service_product_metadata(product_id):
    return fetch_url(settings.service_product_metadata, service_args=product_id)


def service_product_top_download(product_type):
    return fetch_url(settings.service_product_top_download, service_vars=dict(product_type=product_type, version='STORE_WEB'))

def service_product_top_pay(product_type):
    return fetch_url(settings.service_product_top_pay, service_vars=dict(product_type=product_type, version='STORE_WEB'))


def service_product_top_new(product_type):
    return fetch_url(settings.service_product_top_new, service_vars=dict(product_type=product_type, version='STORE_WEB'))


def service_home_topic_item_get(cat_id):
    return fetch_url(settings.service_home_topic_item_get, service_args=cat_id, service_vars=dict(version='STORE_WEB'))


def service_home_topic_get():
    return fetch_url(settings.service_home_topic_get)


def service_paygate_info(trans_id):
    return fetch_url(settings.service_paygate, service_args=('v1', 'transaction'), service_vars={"trans_id": trans_id})


def service_classes_get():
    return fetch_url(settings.service_classes_get)


def service_category_getall():
    return fetch_url(settings.service_category_getall)


def service_subject_get():
    return fetch_url(settings.service_subject_get)


def service_subject_get_classes(args):
    return fetch_url(settings.service_subject_get_classes, service_args=args)


def service_product_getquiz(args):
    return fetch_url(settings.service_product_getquiz, service_args=args)


def service_country_get():
    return fetch_url(settings.service_country_get)


def service_province_get():
    return fetch_url(settings.service_province_get)


def service_district_get():
    return fetch_url(settings.service_district_get)


def service_get_cb_price():
    return fetch_url(settings.service_get_cb_price)


def service_province_get_district(province_id):
    return fetch_url(settings.service_province_get_district, service_args=province_id)


def service_rating_get(product_id):
    return fetch_url3(settings.service_rating, service_args=product_id)


def service_rating_check(user_name, product_id):
    return fetch_url3(settings.service_rating, service_args=(user_name, product_id))


######SERVICE POST FUNCTIONS######

def service_rating_rate(user_name, user_token, product_id, score):
    service_vars = dict(user_name=user_name, user_token=user_token, product_id=product_id, score=score)
    return fetch_url3(settings.service_rating, service_vars=service_vars, method="POST")


def service_user_update(username, firstname, lastname, phone, address):
    service_vars = {'username': username, 'firstName': firstname,
                    'lastName': lastname, 'phoneNumber': phone,
                    'address': address, 'user_token': session.token}
    return fetch_url(settings.service_user_update, service_vars=service_vars)


def service_user_register(username, password, email, firstname, lastname, phone, address, district):
    if firstname == "":
        firstname = "Guest"
    if lastname == "":
        lastname = "User"
    service_vars = {'username': username, 'firstName': firstname,
                    'lastName': lastname, 'phoneNumber': phone,
                    'address': address, 'password': password, 'email': email, 'district': district}
    return fetch_url(settings.service_user_register, service_vars=service_vars)


def service_user_add_device(device_serial, fullname, phone, email, address, ngay_mua):
    service_vars = {'device_serial': device_serial, 'full_name': fullname, 'phone': phone, 'email': email,
                    'address': address, 'purchase_date': ngay_mua}
    return fetch_url(settings.service_user_add_device, service_vars=service_vars)


def service_user_send_message(email, name, phone, category, subject, content):
    service_vars = {'email': email, 'name': name, 'phone': phone, 'contact_category_id': category,
                    'contact_subject': subject, 'contact_content': content}
    return fetch_url(settings.service_user_send_message, service_vars=service_vars)


def service_user_deposit(username, fund):
    service_args = (username, fund, session.token)
    return fetch_url(settings.service_user_deposit, service_args=service_args, method="POST")


def service_paygate_confirm(trans_id):
    return fetch_url(settings.service_paygate, service_args=('v1', 'transaction', 'confirm'),
                     service_vars={"trans_id": trans_id}, method="PUT")


def service_paygate_cancel(trans_id):
    return fetch_url(settings.service_paygate, service_args=('v1', 'transaction', 'cancel'),
                     service_vars={"trans_id": trans_id}, method="PUT")


def service_paygate_order(order_code, net_cost, desc, callback_success, callback_fail):
    return fetch_url(settings.service_paygate, service_args=('v1', 'order'),
                     service_vars={"order_code": order_code, "net_cost": net_cost, "desc": desc,
                                   "callback_success": callback_success, "callback_fail": callback_fail}, method="POST")


def service_transaction_checkout(user_name, user_token, payment_method, bank_code, buyer_amount,
                                 description, success_url, cancel_url,
                                 purchase_type, package, email, pack_type):
    return fetch_url2(settings.service_transaction, service_args=settings.nl_function,
                      service_vars={"version": settings.nl_version, "user_name": user_name,
                                    "user_token": user_token, "payment_method": payment_method,
                                    "bank_code": bank_code, "buyer_amount": buyer_amount,
                                    "description": description, "success_url": success_url,
                                    "cancel_url": cancel_url,
                                    "purchase_type": purchase_type, "package": package,
                                    "email": email, "pack_type": pack_type}, method="POST")


def service_tqg_checkout(user_name, user_token, payment_method, bank_code, buyer_amount,
                                 description, success_url, cancel_url,
                                 purchase_type, package, email, pack_type, site, discount_code=""):
    return fetch_url2(settings.service_transaction, service_args=settings.nl_function,
                      service_vars={"version": settings.nl_version, "user_name": user_name,
                                    "user_token": user_token, "payment_method": payment_method,
                                    "bank_code": bank_code, "buyer_amount": buyer_amount,
                                    "description": description, "success_url": success_url,
                                    "cancel_url": cancel_url,
                                    "purchase_type": purchase_type, "package": package,
                                    "email": email, "pack_type": pack_type, "site": site,
                                    "discount_code": discount_code}, method="POST")


def service_transaction_cardpay(user_name, user_token, pin_card, card_serial, type_card,
                                purchase_type, package, email, pack_type):
    return fetch_url2(settings.service_transaction, service_args=settings.nl_card_function,
                      service_vars={"version": settings.nl_card_version, "user_name": user_name,
                                    "user_token": user_token, "pin_card": pin_card,
                                    "card_serial": card_serial, "type_card": type_card,
                                    "purchase_type": purchase_type, "package": package,
                                    "email": email, "pack_type": pack_type}, method="POST")


def service_tqg_cardpay(user_name, user_token, pin_card, card_serial, type_card,
                                purchase_type, package, email, pack_type, site, discount_code=""):
    return fetch_url2(settings.service_transaction, service_args=settings.nl_card_function,
                      service_vars={"version": settings.nl_card_version, "user_name": user_name,
                                    "user_token": user_token, "pin_card": pin_card,
                                    "card_serial": card_serial, "type_card": type_card,
                                    "purchase_type": purchase_type, "package": package,
                                    "email": email, "pack_type": pack_type, "site": site,
                                    "discount_code": discount_code}, method="POST")



def service_transaction_confirm(user_name, user_token, token):
    return fetch_url2(settings.service_transaction, service_args=settings.nl_function,
                      service_vars={"version": settings.nl_version, "user_name": user_name,
                                    "user_token": user_token, "token": token}, method="POST")


def service_check_free_classbook(category_code):
    return fetch_url(settings.service_check_free_classbook, service_args=category_code, method="GET")

######UTIL FUNCTIONS######
pool = None


def fetch_url3(service_url, service_args=None, service_vars=None, method='GET'):
    global pool
    if pool is None:
        pool = urllib3.HTTPConnectionPool(settings.service_host, settings.service_port)

    try:
        url = get_url(service_url, service_args)
        fetch_data = pool.request(method, url, service_vars)
        return dict(status=fetch_data.status, data=fetch_data.data)
    except Exception as ex:
        return dict(status=500, data=ex)


def fetch_url2(service_url, service_args=None, service_vars=None, method='GET'):
    global pool
    if pool is None:
        pool = urllib3.HTTPConnectionPool(settings.service_host, settings.service_port)

    try:
        url = get_url(service_url, service_args)
        fetch_data = pool.request(method, url, service_vars)
        result = dict(status=fetch_data.status, data=fetch_data.data)
        return result
    except Exception as ex:
        print ex
        return None


def fetch_url(service_url, service_args=None, service_vars=None, method='GET'):
    global pool
    if pool is None:
        pool = urllib3.HTTPConnectionPool(settings.service_host, settings.service_port)

    try:
        url = get_url(service_url, service_args)

        fetch_data = pool.request(method, url, service_vars)

        if fetch_data.status == 200:

            return json.loads(fetch_data.data)
        else:
            raise Exception(fetch_data.status)
    except Exception as ex:
        return None


def get_url(service=None, service_args=None, service_vars=None):
    if not service:
        service = dict(app='cbs', controller=None, function=None)

    return URL(a=service['app'], c=service['controller'], f=service['function'],
               r=request, args=service_args, vars=service_vars,
               extension=settings.service_extension)


def get_captchas_object():
    return CaptchasDotNet.CaptchasDotNet(client=settings.captchas_client,
                                         secret=settings.captchas_secret,
                                         alphabet=settings.captchas_alphabet,
                                         letters=settings.captchas_letters,
                                         width=settings.captchas_width,
                                         height=settings.captchas_height)


def validate_captchas(captchas, random, value):
    if not captchas.validate(random):
        return 1
    if not captchas.verify(value):
        return 2
    return 0


def add_alert(title="Thông báo", content="Đăng nhập thất bại!"):
    session.alerts = dict(title=title, content=content)


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
    return u'Miễn phí' if price == '0' else price + u'₫'


def price2str(value):
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
    return price + u'₫'


def service_user_auth_by_token(username, token):
    service_vars = {'username': username, 'token': token}
    return fetch_url(settings.service_user_auth_by_token, service_vars=service_vars)


import re
INTAB = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ"
INTAB = [ch.encode('utf8') for ch in unicode(INTAB, 'utf8')]

OUTTAB = "a"*17 + "o"*17 + "e"*11 + "u"*11 + "i"*5 + "y"*5 + "d"

r = re.compile("|".join(INTAB))
replaces_dict = dict(zip(INTAB, OUTTAB))

def khongdau(utf8_str):
    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def test_func():
    return 'test_func'


USE_CACHE = True


def get_menu():
    if USE_CACHE:
        return service_category_get()['categories']
    else:
        if not session.categories:
            menu = service_category_get()
            if menu is not None and not 'error' in menu:
                session.categories = menu['categories']
        return session.categories