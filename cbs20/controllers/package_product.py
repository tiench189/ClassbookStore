__author__ = 'Tien'

import sys
import usercp
from datetime import datetime


def check_price_package():
    try:
        user_token = request.vars.user_token
        category_id = request.vars.category_id
        user = db(db.clsb_user.user_token.like(user_token)).select()
        #if len(user) <= 0:
        #    return dict(error="Sai token")
        #user = user.first()
        total_price = 0
        total_pay = 0
        total_cover_price = 0
        list_products = db(db.clsb_product.product_category == category_id)\
                (db.clsb_product.product_status.like("Approved")).select()
        for product in list_products:
            price_pdf = int(product[db.clsb_product.product_price])
            total_price += price_pdf
            if len(user) > 0:
                check_buy_pdf = db(db.clsb30_product_history.product_id == product[db.clsb_product.id])(
                                    db.clsb30_product_history.user_id == user.first()['id']).select()
                if len(check_buy_pdf) == 0:
                    total_pay += price_pdf
            else:
                total_pay += price_pdf

            price_media = db(db.clsb30_product_extend.product_id == product[db.clsb_product.id])\
                        (db.clsb30_product_extend.extend_id == 1).select()
            if len(price_media) > 0:
                price_media = int(price_media.first()['price'])
                total_price += price_media
                if len(user) > 0:
                    check_buy_media = db(db.clsb30_media_history.product_id == product[db.clsb_product.id])(
                                    db.clsb30_media_history.user_id == user.first()['id']).select()
                    if len(check_buy_media) == 0:
                        total_pay += price_media
                else:
                    total_pay += price_media
                total_cover_price += price_media
            has_quiz = db(db.clsb_product.product_code == 'Exer' + product[db.clsb_product.product_code])\
                        (db.clsb_product.product_status == 'Approved').select()
            if len(has_quiz) > 0:
                total_price += settings.fake_fund_quiz
                quiz_id = has_quiz.first()['id']
                if len(user) > 0:
                    check_quiz = db(db.clsb30_product_history.product_id == quiz_id)\
                                    (db.clsb30_product_history.user_id == user.first()['id']).select()
                    if len(check_quiz) == 0:
                        total_pay += settings.fake_fund_quiz
                else:
                    total_pay += settings.fake_fund_quiz
                total_cover_price += settings.fake_fund_quiz
            cover_price = db(db.clsb_product_metadata.product_id == product[db.clsb_product.id]) \
                        (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                        (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                    db.clsb_product_metadata.metadata_value).as_list()
            if cover_price:
                try:
                    total_cover_price += int(cover_price[0]['metadata_value'])
                except Exception as e:
                        print str(e)
        return dict(total_pay=total_pay, total_price=total_price, total_cover_price=total_cover_price)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def check_price_by_user():
    try:
        user_token = request.vars.user_token
        category_id = request.vars.category_id
        user = db(db.clsb_user.user_token.like(user_token)).select()
        if len(user) <= 0:
            return dict(error="INVALID_TOKEN")
        total_price = 0
        total_pay = 0
        total_cover_price = 0
        list_products = db(db.clsb_product.product_category == category_id)\
                (db.clsb_product.product_status.like("Approved")).select()
        for product in list_products:
            price_pdf = int(product[db.clsb_product.product_price])
            total_price += price_pdf
            check_buy_pdf = db(db.clsb30_product_history.product_id == product[db.clsb_product.id])(
                                    db.clsb30_product_history.user_id == user.first()['id']).select()
            if len(check_buy_pdf) == 0:
                total_pay += price_pdf

            price_media = db(db.clsb30_product_extend.product_id == product[db.clsb_product.id])\
                        (db.clsb30_product_extend.extend_id == 1).select()
            if len(price_media) > 0:
                price_media = int(price_media.first()['price'])
                total_price += price_media
                check_buy_media = db(db.clsb30_media_history.product_id == product[db.clsb_product.id])(
                                    db.clsb30_media_history.user_id == user.first()['id']).select()
                if len(check_buy_media) == 0:
                    total_pay += price_media
                total_cover_price += price_media
            has_quiz = db(db.clsb_product.product_code == 'Exer' + product[db.clsb_product.product_code])\
                        (db.clsb_product.product_status == 'Approved').select()
            if len(has_quiz) > 0:
                total_price += settings.fake_fund_quiz
                quiz_id = has_quiz.first()['id']
                check_quiz = db(db.clsb30_product_history.product_id == quiz_id)\
                                    (db.clsb30_product_history.user_id == user.first()['id']).select()
                if len(check_quiz) == 0:
                    total_pay += settings.fake_fund_quiz
                total_cover_price += settings.fake_fund_quiz
            cover_price = db(db.clsb_product_metadata.product_id == product[db.clsb_product.id]) \
                        (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                        (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                    db.clsb_product_metadata.metadata_value).as_list()
            if cover_price:
                try:
                    total_cover_price += int(cover_price[0]['metadata_value'])
                except Exception as e:
                        print str(e)
        return dict(total_pay=total_pay, total_price=total_price, total_cover_price=total_cover_price)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def user_buy_package():
    try:
        user_token = request.vars.user_token
        category_id = request.vars.category_id
        total_pay = int(request.vars.total_pay)
        user = db(db.clsb_user.user_token.like(user_token)).select()
        if len(user) <= 0:
            return dict(error="INVALID_TOKEN")
        user = user.first()
        user_fund = int(user['fund'])
        if user_fund < total_pay:
            return dict(error="INVALID_FUND")
        data_buy_pdf = list()
        data_buy_media = list()
        data_download = list()
        products = list()

        list_products = db(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_category.id == category_id)\
                (db.clsb_category.category_type == db.clsb_product_type.id)\
                (db.clsb_product.product_status.like("Approved")).select()
        for product in list_products:
            price_pdf = int(product[db.clsb_product.product_price])
            check_buy_pdf = db(db.clsb30_product_history.product_id == product[db.clsb_product.id])(
                                db.clsb30_product_history.user_id == user['id']).select()
            if len(check_buy_pdf) == 0:
                temp = dict()
                temp['category_code'] = product[db.clsb_category.category_code]
                temp['product_code'] = product[db.clsb_product.product_code]
                temp['product_price'] = product[db.clsb_product.product_price]
                temp['category_type'] = str(product[db.clsb_product_type.type_name]).lower()
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=product[db.clsb_product.product_code])
                temp['category_name'] = product[db.clsb_category.category_name]
                temp['id'] = product[db.clsb_product.id]
                temp['product_title'] = product[db.clsb_product.product_title]
                products.append(temp)

                data_buy_pdf.append(dict(product_title=product[db.clsb_product.product_title],
                    product_id=product[db.clsb_product.id],
                    user_id=user['id'],
                    category_id=category_id,
                    product_price=price_pdf))
                discount = 98
                select_cp = db(db.clsb20_product_cp.product_code == db.clsb_product.product_code)\
                            (db.clsb_product.id == product[db.clsb_product.id]).select()
                if len(select_cp) > 0:
                    discount = usercp.get_discount_value(select_cp.first()['clsb20_product_cp']['created_by'], db)
                elif product[db.clsb_category.category_parent] is not None and int(product[db.clsb_category.category_parent]) not in [1, 26]:
                    discount = 30
                pay_provider = price_pdf * discount / 100
                pay_cp = price_pdf - pay_provider
                data_download.append(dict(user_id=user['id'],
                        product_id=product[db.clsb_product.id],
                        price=price_pdf,
                        pay_provider=pay_provider,
                        pay_cp=pay_cp,
                        download_time=datetime.now(),
                        purchase_type="WEB_PAY",
                        rom_version="",
                        device_serial="",
                        status="COMPLETE"))

            price_media = db(db.clsb30_product_extend.product_id == product[db.clsb_product.id])\
                        (db.clsb30_product_extend.extend_id == 1).select()
            if len(price_media) > 0:
                price_media = int(price_media.first()['price'])
                check_buy_media = db(db.clsb30_media_history.product_id == product[db.clsb_product.id])(
                                db.clsb30_media_history.user_id == user['id']).select()
                if len(check_buy_media) == 0:
                    data_buy_media.append(dict(product_title=product[db.clsb_product.product_title],
                            product_id=product[db.clsb_product.id],
                            user_id=user['id'],
                            category_id=category_id,
                            product_price=price_media))
            has_quiz = db(db.clsb_product.product_code == 'Exer' + product[db.clsb_product.product_code])\
                        (db.clsb_product.product_status == 'Approved').select()
            if len(has_quiz) > 0:
                quiz_id = has_quiz.first()['id']
                check_quiz = db(db.clsb30_product_history.product_id == quiz_id)\
                                (db.clsb30_product_history.user_id == user['id']).select()
                if len(check_quiz) == 0:
                    data_buy_pdf.append(dict(product_title=has_quiz.first()['product_title'],
                            product_id=has_quiz.first()['id'],
                            user_id=user['id'],
                            category_id=category_id,
                            product_price=settings.fake_fund_quiz))
        db.clsb30_product_history.bulk_insert(data_buy_pdf)
        db.clsb30_media_history.bulk_insert(data_buy_media)
        db.clsb_download_archieve.bulk_insert(data_download)
        return dict(result="OK", products=products)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_list_package():
    try:
        enable_package = [54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68]
        select_category = db(db.clsb_category.id.belongs(enable_package)).select()
        categories = list()
        for cate in select_category:
            temp = dict()
            temp['id'] = cate['id']
            temp['category_name'] = cate['category_name']
            temp['category_code'] = cate['category_code']
            categories.append(temp)
        return dict(categories=categories)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))
