# -*- coding: utf-8 -*-
""" Users
    Service quản lý thông tin tài khoản và các tài khoản dưới quyền
"""
__author__ = 'manhtd'
import usercp


def call():
    return service()


# @auth.requires_authorize
def info():
    """
     #args=[username,token]
    """
    try:
        username = request.args[0]
        token = request.args[1]
        return usercp.info_by_token(username, token, db)
    except:
        return dict(error=CB_0003)


def error_time_out():
    return dict(error=CB_0012)


@request.restful()
def authorize():

    def post(**vars):
        """
            vars: username=manhtd&password=123456
            return: token
        """
        response.view = 'generic.json'
        if not 'username' in vars or not 'password' in vars:
            return dict(error=dict(code=400, message='Parameters invalid!'))
        user = auth.login_bare(vars['username'], vars['password'])
        if not user:
            return dict(error=dict(code=401, message='Authorize failed!'))
        else:
            import os
            from gluon.contrib import pbkdf2
            from datetime import datetime

            str_regenration = os.urandom(10)
            token = pbkdf2.pbkdf2_hex(vars['username'], str_regenration)
            try:
                db(db[auth.table_user()].username == vars['username']).update(token=token, last_login=datetime.today())
            except:
                import traceback

                traceback.print_exc()
                return dict(error=dict(code=500, message='Database error!'))
            return dict(token=token)

    return locals()


def register_subscription(username, purchase_id):
    from datetime import datetime, timedelta
    user = db(db.clsb_user.username == username).select(db.clsb_user.id, db.clsb_user.fund).first()
    if not user:
        return False, u"Không tồn tại người dùng!"

    query = db(db.clsb20_user_purchase_item.user_id == user.id)
    purchase = query.select(db.clsb20_user_purchase_item.day_end).first()
    if purchase and purchase.day_end > datetime.today():
        return False, u"Thuê bao vẫn đang hoạt động!"

    query = db(db.clsb20_product_purchase_item.id == purchase_id)
    query = query(db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)
    query = query(db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type)
    query = query(db.clsb20_purchase_type.name == "SUBSCRIPTION")
    purchase = query.select(db.clsb20_product_purchase_item.price, db.clsb20_purchase_item.duration,
                            db.clsb20_product_purchase_item.product_code).first()
    if not purchase:
        return False, u"Sản phẩm không tồn tại gói thuê bao này!"
    if purchase.clsb20_product_purchase_item.price > user.fund:
        return False, u"Tài khoản người dùng không đủ thực hiện giao dịch!"

    day_end = datetime.today() + timedelta(days=purchase.clsb20_purchase_item.duration)
    query = db(db.clsb_user.username == username)
    query.update(fund=db.clsb_user.fund - purchase.clsb20_product_purchase_item.price)
    db.clsb20_user_purchase_item.update_or_insert({'user_id': user.id}, user_id=user.id,
                                                  day_end=day_end, purchase_id=purchase_id)

    query = db(db.clsb_product.product_code == purchase.clsb20_product_purchase_item.product_code)
    product = query.select(db.clsb_product.id).first()
    db.clsb20_purchase_renew_history.insert(user_id=user.id, product_id=product.id,
                                            purchase_id=purchase_id, date_do_renew=datetime.today())
    return True


@service.json
@service.jsonrpc
def get_subscriptions(product_code):
    query = db(db.clsb20_product_purchase_item.product_code == product_code)
    query = query(db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)
    query = query(db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type)
    query = query(db.clsb20_purchase_type.name == "SUBSCRIPTION")
    subscriptions = query.select(db.clsb20_product_purchase_item.id, db.clsb20_purchase_item.name,
                                 db.clsb20_purchase_item.duration, db.clsb20_product_purchase_item.price)
    return [dict(id=s.clsb20_product_purchase_item.id, name=s.clsb20_purchase_item.name,
                 duration=s.clsb20_purchase_item.duration, price=s.clsb20_product_purchase_item.price)
            for s in subscriptions]


@service.json
@service.jsonrpc
def check_subscription(username):
    from datetime import datetime
    user = db(db.clsb_user.username == username).select(db.clsb_user.id).first()
    if not user:
        return False, u"Không tồn tại người dùng!"
    query = db(db.clsb20_user_purchase_item.user_id == user.id)
    purchase = query.select(db.clsb20_user_purchase_item.day_end).first()
    if not purchase:
        return False, u"Bạn chưa đăng ký thuê bao!"
    if purchase.day_end <= datetime.today():
        return False, u"Thuê bao hết hạn!"
    return True, u"Thời hạn thuê bao đến ngày: %s" % purchase.day_end


def customer_authorize():
    status = ''
    if 'username' in request.post_vars and 'password' in request.post_vars and 'purchase' in request.post_vars:
        from gluon.contrib.pbkdf2 import pbkdf2_hex
        p_2_d_key = 'c-p3d*b'
        username = request.post_vars.username
        password = pbkdf2_hex(p_2_d_key, request.post_vars.password)
        purchase = request.post_vars.purchase
        user = db(db.clsb_user.username == username)(db.clsb_user.password == password).count()
        if user == 0:
            status = u"Đăng nhập thất bại!"
        else:
            try:
                res = register_subscription(username, purchase)
                if isinstance(res, bool):
                    return dict(message=u"Đăng ký gia hạn thuê bao thành công!")
                else:
                    status = res[1]
            except:
                import traceback
                traceback.print_exc()
                status = u"Có lỗi trong quá trình xử lý dữ liệu!"
    elif len(request.args) != 2:
        return dict(error=u"Dữ liệu không hợp lệ!")
    else:
        username = request.args[0]
        purchase = request.args[1]

    query = db(db.clsb20_product_purchase_item.id == purchase)
    query = query(db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)
    subs = query.select(db.clsb20_purchase_item.name, db.clsb20_purchase_item.duration,
                        db.clsb20_product_purchase_item.price).first()
    subs_name = subs.clsb20_purchase_item.name
    subs_duration = subs.clsb20_purchase_item.duration
    subs_price = subs.clsb20_product_purchase_item.price
    if not subs:
        return dict(error=u"Không tìm thấy gói thuê bao!")
    form = DIV(H1("Thông Tin Đăng Ký Thuê Bao"),
               FORM(DIV("Xin chào %s " % username),
                    DIV("Chúng tôi nhận được yêu cầu gia hạn/đăng ký thuê bao sau"),
                    DIV("Gói thuê bao: %s" % subs_name),
                    DIV("Thời hạn sử dụng: %d" % subs_duration),
                    DIV("Số tiền quý khách phải thanh toán sẽ là: %d₫" % subs_price),
                    DIV("Quý khách xác nhận mật khẩu để thanh toán giao dịch trên!"), BR(),
                    DIV(status, _style='color: red;'),
                    DIV(LABEL('Password:', _style='margin-right: 10px;'),
                        INPUT(_type='password', _name='password', _style='width: 150px; padding-left: 5px;'),
                        INPUT(_type='hidden', _name='username', _value=username),
                        INPUT(_type='hidden', _name='purchase', _value=purchase),
                        INPUT(_type='submit', _style='margin-right: 70px', _value="Thanh Toán")),
                    _action=URL()),
               _style='width: 400px; margin: auto;')
    return dict(form=form)
