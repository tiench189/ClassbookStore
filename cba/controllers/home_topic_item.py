# -*- coding: utf-8 -*-
#@author: hant 08-03-2013

from gluon.tools import Auth
#import cbMsg
import sys
from datetime import datetime, timedelta
SUCCESS = CB_0000#cbMsg.CB_0000
LACK_ARGS = CB_0002#cbMsg.CB_0002
DB_RQ_FAILD = CB_0003#cbMsg.CB_0003

def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/home_topic_item/delete(ids, table) " + str(e)

def home_topic_item_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')

def home_topic_item_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')

def home_topic_item_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


# @auth.requires_login()
@auth.requires_authorize()
def index():
    # check_is_root()

    current_table = "clsb_home_topic_item"
#     if request.url.find('/clsb_home_topic_item/???.') >= 0:
#         current_table = "????"
    selectable = lambda ids: delete(ids, current_table)
    
    try:
        table = 'clsb_home_topic_item'
        if not table in db.tables(): redirect(URL('error'))
        form = smartgrid(db[table], 
                                 oncreate = home_topic_item_on_create,
                                 onupdate = home_topic_item_on_update,
                                 ondelete = home_topic_item_on_delete,
                                 linked_tables=['clsb_home_topic'],
                                 showbuttontext = False,
                                 user_signature = False,
                                 create=True, editable=True, details=True, 
                            #links=links,
                                 selectable=selectable )
        if form.element('.web2py_table input[type=submit]'):
            form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
            form.element('.web2py_table input[type=submit]')['_onclick'] = \
            "return confirm('"+ CONFIRM_DELETE +"');"
        #return locals()
        return dict(form = form)
    except Exception as ex: 
        if request.is_local: 
            return ex 
        else: 
            raise HTTP(400)


@auth.requires_authorize()
def random_top_recomend():
    try:
        select_product = db(db.clsb_home_topic_item.topic_id == 1)\
            (db.clsb_home_topic_item.product_type.like("BOOK")).select(db.clsb_home_topic_item.id,
                                                                       db.clsb_home_topic_item.topic_item_order)
        import random
        nums = [x for x in range(len(select_product))]
        random.shuffle(nums)
        for i in range(0, len(select_product)):
            db(db.clsb_home_topic_item.id == select_product[i]['id']).update(topic_item_order=nums[i] + 1)
        return "SUCCESS"
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


@auth.requires_authorize()
def set_up_recomend():
    try:
        categories = list()

        except_id = list()

        #SGK - SBT
        cate = dict()
        cate['name'] = "SGK-BT"
        cate['id'] = 1
        except_id.append(cate['id'])
        cate['products'] = get_product_top_buy(cate['id'])
        categories.append(cate)

        #STK
        cate = dict()
        cate['name'] = "Tham khảo"
        cate['id'] = 2
        except_id.append(cate['id'])
        cate['products'] = get_product_top_buy(cate['id'])
        categories.append(cate)

        #SGV
        cate = dict()
        cate['name'] = "Giáo viên"
        cate['id'] = 26
        except_id.append(cate['id'])
        cate['products'] = get_product_top_buy(cate['id'])
        categories.append(cate)

        #Kim Đồng
        cate = dict()
        cate['name'] = "Kim Đồng"
        cate['id'] = 108
        except_id.append(cate['id'])
        cate['products'] = get_product_top_buy(cate['id'])
        categories.append(cate)

        #Ôn thi
        cate = dict()
        cate['name'] = "Ôn thi"
        cate['id'] = 102
        except_id.append(cate['id'])
        cate['products'] = get_product_top_buy(cate['id'])
        categories.append(cate)

        #Sách truyện
        cate = dict()
        cate['name'] = "Sách truyện"
        cate['id'] = 94
        except_id.append(cate['id'])
        cate['products'] = get_product_top_buy(cate['id'])
        categories.append(cate)

        #Khoa học đời sống
        cate = dict()
        cate['name'] = "KH&ĐS"
        cate['id'] = 96
        except_id.append(cate['id'])
        cate['products'] = get_product_top_buy(cate['id'])
        categories.append(cate)

        # Khac
        cate = dict()
        cate['name'] = "Khác"
        cate['id'] = 0
        limit = 30
        time_over = 14 #days
        count = db.clsb30_product_history.id.count()
        select_product = db(db.clsb_product.product_category == db.clsb_category.id)\
            (~db.clsb_category.category_parent.belongs(except_id))\
            (~db.clsb_product.product_code.like("Exer%"))\
            (db.clsb_product.id == db.clsb30_product_history.product_id)\
            (db.clsb30_product_history.product_price > 0)\
            (db.clsb30_product_history.user_id == db.clsb_user.id)\
            (db.clsb_user.test_user != 1)\
            (db.clsb30_product_history.created_on > datetime.now() - timedelta(days=time_over)).select(count,
                                                         db.clsb30_product_history.product_id,
                                                         db.clsb_product.product_title,
                                                         db.clsb_product.product_code,
                                                         groupby=db.clsb30_product_history.product_id,
                                                         orderby=~count,
                                                         limitby=(0, limit))
        products = list()
        for product in select_product:
            temp = dict()
            temp['product_id'] = product[db.clsb30_product_history.product_id]
            temp['product_title'] = product[db.clsb_product.product_title]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['count'] = product[count]
            products.append(temp)
        cate['products'] = products
        categories.append(cate)

        # get current recomends
        select_recomend = db(db.clsb_home_topic_item.topic_id == 1)\
            (db.clsb_home_topic_item.product_type.like("BOOK"))\
            (db.clsb_home_topic_item.product_id == db.clsb_product.id).select(db.clsb_home_topic_item.product_id,
                                                                              db.clsb_product.product_title,
                                                                       db.clsb_home_topic_item.topic_item_order,
                                                                       orderby=db.clsb_home_topic_item.topic_item_order)
        recomends = list()
        olds = list()
        for r in select_recomend:
            recomends.append(r[db.clsb_home_topic_item.product_id])
            temp = dict()
            temp['product_id'] = r[db.clsb_home_topic_item.product_id]
            temp['product_title'] = r[db.clsb_product.product_title]
            olds.append(temp)
        return dict(categories=categories, recomends=recomends, olds=olds)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_product_top_buy(cate_id):
    try:
        limit = 30
        time_over = 14 #days
        count = db.clsb30_product_history.id.count()
        select_product = db(db.clsb_product.product_category == db.clsb_category.id)\
            (db.clsb_category.category_parent == cate_id)\
            (~db.clsb_product.product_code.like("Exer%"))\
            (db.clsb_product.id == db.clsb30_product_history.product_id)\
            (db.clsb30_product_history.product_price > 0)\
            (db.clsb30_product_history.user_id == db.clsb_user.id)\
            (db.clsb_user.test_user != 1)\
            (db.clsb30_product_history.created_on > datetime.now() - timedelta(days=time_over)).select(count,
                                                         db.clsb30_product_history.product_id,
                                                         db.clsb_product.product_title,
                                                         db.clsb_product.product_code,
                                                         groupby=db.clsb30_product_history.product_id,
                                                         orderby=~count,
                                                         limitby=(0, limit))
        products = list()
        for product in select_product:
            temp = dict()
            temp['product_id'] = product[db.clsb30_product_history.product_id]
            temp['product_title'] = product[db.clsb_product.product_title]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['count'] = product[count]
            products.append(temp)
        return products
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def submit_recommend():
    try:
        db(db.clsb_home_topic_item.topic_id == 1)\
            (db.clsb_home_topic_item.product_type.like("BOOK")).delete()
        data = list()
        my_order = 1
        for p_id in request.args:
            temp = dict()
            temp['topic_id'] = 1
            temp['product_id'] = p_id
            temp['product_type'] = "BOOK"
            temp['topic_item_order'] = my_order
            my_order += 1
            data.append(temp)
        db.clsb_home_topic_item.bulk_insert(data)
        return dict(result=True)
    except Exception as ex:
        return dict(result=False, error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))