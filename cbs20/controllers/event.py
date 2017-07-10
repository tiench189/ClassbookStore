# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys
from datetime import datetime, timedelta


def register():
    try:
        user_token = request.vars.user_token
        product_id = request.vars.product_id
        time_now = datetime.now()
        time = datetime.strptime(str(time_now.year) + " " + str(time_now.month) + " " + str(time_now.day), "%Y %m %d")
        select_user = db(db.clsb_user.user_token.like(user_token)).select()
        if len(select_user) == 0:
            return dict(result=False, error="Tài khoản đã đăng nhập ở nơi khác, vui lòng đăng nhập lại")
        user = select_user.first()
        select_product = db(db.clsb_product.id == product_id)\
                (db.clsb_product.product_status.like("Approved")).select()
        if len(select_product) == 0:
            return dict(result=False, error="Sản phẩm không tồn tại")
        product = select_product.first()
        if product['product_price'] == 0:
            return dict(result=False, error="Sản phẩm này là miễn phí, vui lòng chọn sản phẩm khác")
        select_history = db(db.clsb30_product_history.product_id == product_id)\
            (db.clsb30_product_history.user_id == user['id']).select()
        if len(select_history) > 0:
            return dict(result=False, error="Bạn đã mua sản phẩm này rồi, vui lòng chọn sản phẩm khác")
        select_promotion = db(db.clsb30_event_promotion.user_id == user['id'])\
            (db.clsb30_event_promotion.product_id == product_id)\
            (db.clsb30_event_promotion.created_on > time)\
            (db.clsb30_event_promotion.created_on < time + timedelta(days=1)).select()
        if len(select_promotion) > 0:
            return dict(result=False, error="Bạn đã chọn sản phẩm này rồi")
        select_user_in_day = db(db.clsb30_event_promotion.user_id == user['id'])\
            (db.clsb30_event_promotion.created_on > time)\
            (db.clsb30_event_promotion.created_on < time + timedelta(days=1)).select()
        if len(select_user_in_day) > 0:
             db(db.clsb30_event_promotion.user_id == user['id'])\
                    (db.clsb30_event_promotion.created_on > time)\
                    (db.clsb30_event_promotion.created_on < time + timedelta(days=1)).update(product_id=product_id,
                                                                                             created_on=datetime.now())
        else:
            db.clsb30_event_promotion.update_or_insert(user_id=user['id'],
                                                       product_id=product_id)
        promotion = db(db.clsb30_event_promotion.user_id == user['id']).select().last()
        return dict(result=True, id=promotion['id'])
    except Exception as ex:
        return dict(result=False, error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def check_user_get_promotion():
    try:
        return dict(result=False)
    except Exception as ex:
        return dict(result=False, error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))