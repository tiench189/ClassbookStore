# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys


def check_tvt_code():
    try:
        code = str(request.vars.code).strip().upper()
        select_code = db(db.clsb30_tvt_code.promotion_code.like(code)).select()
        if len(select_code) == 0:
            return dict(result=False, mess="Mã giảm giá không hợp lệ", code=code)
        return dict(result=True)
    except Exception as err:
        return dict(result=False, mess=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


#def update_price_20_11():
#    try:
#        select_product1 = db(db.clsb_product.product_status.like("Approved"))\
#                (db.clsb_product.product_category == db.clsb_category.id)\
#                (db.clsb_category.category_parent.belongs([1, 2, 108])).select(db.clsb_product.id,
#                                                                         db.clsb_product.product_price)
#        for product in select_product1:
#            product_id = product[db.clsb_product.id]
#            product_price = int(product[db.clsb_product.product_price])
#            new_price = int(product_price * 2 / 3)
#            db(db.clsb_product.id == product_id).update(product_price=new_price)
#
#        select_product2 = db(db.clsb_product.product_status.like("Approved"))\
#                (db.clsb_product.product_category == db.clsb_category.id)\
#                (db.clsb_category.category_parent == 26).select(db.clsb_product.id,
#                                                                         db.clsb_product.product_price)
#        for product in select_product2:
#            product_id = product[db.clsb_product.id]
#            new_price = 2000
#            db(db.clsb_product.id == product_id).update(product_price=new_price)
#    except Exception as err:
#        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
#
#
#def backup_price():
#    try:
#        select_product = db(db.clsb_product).select()
#        for product in select_product:
#            db.clsb30_backup_price.update_or_insert(product_id=product['id'], product_price=product['product_price'])
#        return "FINISHED"
#    except Exception as err:
#        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
#
#
#def restore_price():
#    try:
#        restore_product = db(db.clsb30_backup_price).select()
#        for product in restore_product:
#            db(db.clsb_product.id == product['product_id']).update(product_price=product['product_price'])
#        return "FINISHED"
#    except Exception as err:
#        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
#
#
#def update_price_04_12():
#    try:
#        select_product = db(db.clsb30_backup_price).select()
#        for product in select_product:
#            product_id = product["product_id"]
#            product_price = int(product['product_price'])
#            new_price = int(product_price * 2 / 3)
#            db(db.clsb_product.id == product_id).update(product_price=new_price)
#        return "FINISHED"
#    except Exception as err:
#        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))