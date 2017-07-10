# -*- coding: utf-8 -*-

import os.path
from applications.cba.modules import clsbUltils
from gluon.contrib.aes import ECBMode
import usercp
import urllib2
import sys
import json
"""
    Get all products.
"""

import string
import re

INTAB = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ"
INTAB = [ch.encode('utf8') for ch in unicode(INTAB, 'utf8')]

OUTTAB = "a"*17 + "o"*17 + "e"*11 + "u"*11 + "i"*5 + "y"*5 + "d"

r = re.compile("|".join(INTAB))
replaces_dict = dict(zip(INTAB, OUTTAB))

def khongdau(utf8_str):
    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)


def get():
    #print(request.vars)
    try:
        version_app = ""
        if 'version' in request.vars:
            version_app = request.vars.version
        products = list()
        db_product = list()
        page = 0
        items_per_page = settings.items_per_page
        product_query = db(db.clsb_product.product_status.like('Approved'))
        if version_app != "":
            product_query = product_query(db.clsb_product.show_on.like('%' + version_app + '%'))
        if request.args:
            cat_id = request.args[0]
            product_query = product_query(db.clsb_product.product_category == cat_id)

            #Pagination
            try:
                if len(request.args) > 1: page = int(request.args[1])
                if len(request.args) > 2: items_per_page = int(request.args[2])
                if len(request.args) > 3:
                    version_view = request.args[3]
                    product_query = product_query(db.clsb_product.show_on.like("%" + version_view + "%"))
            except (TypeError, ValueError):
                pass
        else:
            product_query = product_query(db.clsb_product.id > 0)

        limitby = (page * items_per_page, (page + 1) * items_per_page)

        total_items = product_query(db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id).count()

        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

        db_product = product_query(db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id) \
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                      db.clsb_category.ALL,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_dic_creator.creator_name,
                                                                                      db.clsb_dic_publisher.publisher_name,
                                                                                      db.clsb_product.id,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                      db.clsb_device_shelf.device_shelf_code,
                                                                                      db.clsb_device_shelf.device_shelf_type,
                                                                                      db.clsb_device_shelf.device_shelf_name,
                                                                                      orderby=~db.clsb_product.created_on,
                                                                                      limitby=limitby).as_list()

        if db_product:
            for row in db_product:
                temp = dict()
                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsb_category']['id']
                free = check_free_for_classbook(temp['category_id'])
                temp['free'] = free
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']

                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                            scheme=True, host=True, args=row['clsb_product'][
                        'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                cover_price = db(db.clsb_product_metadata.product_id == row['clsb_product']['id']) \
                        (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                        (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                    db.clsb_product_metadata.metadata_value).as_list()
                if cover_price:
                    try:
                        temp['cover_price'] = int(cover_price[0]['metadata_value'])
                    except Exception as e:
                        print str(e)
                else:
                    temp['cover_price'] = 0

                products.append(temp)
        return dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
                    products=products)
    except Exception as ex:
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))


"""
    get all quiz product (has metadata subject_class )
"""


def getAllQuizProduct():
    products = list()
    db_product = list()

    db_product = db(db.clsb_product.subject_class != None).select(db.clsb_product.id,
                                                                  db.clsb_product.product_code,
                                                                  db.clsb_product.product_title,
                                                                  db.clsb_product.product_category,
                                                                  db.clsb_product.subject_class,
    ).as_list()
    if db_product:
        for row in db_product:
            temp = dict()
            temp['product_id'] = row['id']
            temp['product_code'] = row['product_code']
            temp['category_id'] = row['id']
            temp['subject_class'] = row['subject_class']
            products.append(temp)

    return dict(count=len(products), products=products)


"""
    Get all quiz by category id, subject id, class id.
"""


def getquiz():#args: cat_id/subject_id/class_id/page/item_per_page
    if request.args and len(request.args) < 3:
        return dict(error=CB_0019) #ILLEGAL_ARGUMENT
    try:
        products = list()
        db_product = list()
        page = 0
        items_per_page = settings.items_per_page
        product_query = db(db.clsb_product.product_status.like('Approved'))

        cat_id = request.args[0]
        product_query = product_query(db.clsb_product.product_category == cat_id)

        # get product's subject, class
        subject_id = int(request.args[1])
        class_id = int(request.args[2])
        subject_class_id = db(db.clsb_subject_class.subject_id == subject_id) \
                (db.clsb_subject_class.class_id == class_id).select(db.clsb_subject_class.id).as_list()
        subject_class_id = subject_class_id[0]['id']
        product_query = product_query(db.clsb_product.subject_class == subject_class_id)

        #Pagination
        try:
            if len(request.args) > 1: page = int(request.args[1])
            if len(request.args) > 2: items_per_page = int(request.args[2])
        except (TypeError, ValueError):
            pass

        limitby = (page * items_per_page, (page + 1) * items_per_page)

        total_items = 1

        total_items = product_query(db.clsb_category.id == db.clsb_product.product_category) \
                (db.clsb_device_shelf.id == db.clsb_product.device_shelf_code) \
                (db.clsb_dic_creator.id == db.clsb_product.product_creator) \
                (db.clsb_dic_publisher.id == db.clsb_product.product_publisher) \
                (db.clsb_category.category_type == db.clsb_product_type.id).count()

        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

        db_product = product_query(db.clsb_category.id == db.clsb_product.product_category) \
                (db.clsb_device_shelf.id == db.clsb_product.device_shelf_code) \
                (db.clsb_dic_creator.id == db.clsb_product.product_creator) \
                (db.clsb_dic_publisher.id == db.clsb_product.product_publisher) \
                (db.clsb_category.category_type == db.clsb_product_type.id).select(db.clsb_category.category_code,
                                                                                   db.clsb_category.category_name,
                                                                                   db.clsb_category.category_parent,
                                                                                   db.clsb_category.id,

                                                                                   db.clsb_product.product_code,
                                                                                   db.clsb_product.id,
                                                                                   db.clsb_product.product_collection,
                                                                                   db.clsb_product.product_status,
                                                                                   db.clsb_product.subject_class,
                                                                                   db.clsb_product.product_title,
                                                                                   db.clsb_product.total_download,
                                                                                   db.clsb_product.product_description,
                                                                                   db.clsb_product.product_price,

                                                                                   db.clsb_device_shelf.device_shelf_code,
                                                                                   db.clsb_device_shelf.device_shelf_name,
                                                                                   db.clsb_device_shelf.id,

                                                                                   db.clsb_dic_creator.creator_name,
                                                                                   db.clsb_dic_publisher.publisher_name,
                                                                                   db.clsb_product_type.type_name,
        ).as_list()
        #         return dict(d= db_product)
        if db_product:
            for row in db_product:
                temp = dict()
                temp['product_id'] = row['clsb_product']['id']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                            scheme=True, host=True, args=row['clsb_product'][
                        'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['product_collection'] = row['clsb_product']['product_collection']
                temp['product_status'] = row['clsb_product']['product_status']
                temp['total_download'] = row['clsb_product']['total_download']
                temp['product_description'] = row['clsb_product']['product_description']

                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_parent'] = row['clsb_category']['category_parent']
                temp['category_id'] = row['clsb_category']['id']

                temp['device_shelf_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
                temp['device_shelf_id'] = row['clsb_device_shelf']['id']

                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['type_name'] = row['clsb_product_type']['type_name']

                #                 print row['clsb_dic_metadata']['metadata_name']
                if row['clsb_product']['subject_class']:
                    temp['subject_class'] = row['clsb_product']['subject_class']
                else:
                    temp['subject_class'] = ""
                #                 print "-----------------------------"

                products.append(temp)
        return dict(products=products, page=page, items_per_page=items_per_page, total_items=total_items,
                    total_pages=total_pages)
    except Exception as ex:
        return dict(error=ex)

#         redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))

"""
    Get product relation.
"""


def relation(): #params: id
    try:
        cover_price = "cover_price"
        cover_price_metadata = db(db.clsb_dic_metadata.metadata_name == cover_price).select(db.clsb_dic_metadata.id).first()

        products = list()
        for relationID in db(db.clsb_product_relation.product_id == request.args(0)).select(
                db.clsb_product_relation.relation_id):
            db_product = db(db.clsb_product.id == relationID.relation_id) \
                    (db.clsb_product.product_status == 'Approved') \
                    (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                     db.clsb_category.ALL,
                                                                                     db.clsb_product_type.type_name,
                                                                                     db.clsb_dic_creator.creator_name,
                                                                                     db.clsb_dic_publisher.publisher_name,
                                                                                     db.clsb_product.product_title,
                                                                                     db.clsb_product.product_code,
                                                                                     db.clsb_product.product_price).as_list()
            for row in db_product:

                metadata_value = db((db.clsb_product_metadata.metadata_id == cover_price_metadata['id']) & (
                db.clsb_product_metadata.product_id == row['clsb_product']['id'] )).select(
                    db.clsb_product_metadata.metadata_value).first()

                temp = dict()
                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsb_category']['id']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_code'] = row['clsb_product']['product_code']
                try:
                    temp['cover_price'] = metadata_value['metadata_value']
                except Exception as err:
                    temp['cover_price'] = 0

                temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                            scheme=True, host=True,
                                            args=row['clsb_product']['product_code'])#row['clsb_product']['product_cover']
                temp['product_price'] = row['clsb_product']['product_price']
                products.append(temp)
        return dict(products=products)
    except Exception as ex:
        return dict(error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))

########################################
#hant 04-03-2013 
SUCCESS = CB_0000
BAD_REQUEST = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001
table = 'clsb_product'

"""
    Get the product's total download.
"""
#update totalDownload field. TODO: Must be combined with service cbs/download 
def totalDownload():
    if not table in db.tables(): return NOT_EXIST
    if request.args and len(request.args) == 4:
        try:
            product = db(db[table].product_code == request.args(0)).select().first()
            nb = 0
            if product['total_download']:
                nb = product['total_download']
            nb += 1
            db(db[table].product_code == request.args(0)).update(total_download=nb)
            return SUCCESS
        except Exception as e:
            return e
    else:
        return BAD_REQUEST


"""
    Get a top n download. n is the args that it can be set by request or the default value is 10

"""
#get top download, n is the args that it can be set by request or the default value is 10
def topdownload():
    if not table in db.tables(): return NOT_EXIST
    n = 0
    product_type = None
    version_app = ""
    if not request.args:
        n = 10
    elif len(request.args) == 1:
        n = int(request.args(0))
    else:
        return BAD_REQUEST
    if request.vars.product_type:
        product_type = request.vars.product_type
    if 'version' in request.vars:
        version_app = request.vars.version
    try:
        qset = db(db[table].product_category == db.clsb_category.id)
        qset = qset(db[table].product_creator == db.clsb_dic_creator.id)
        qset = qset(db.clsb_category.category_type == db.clsb_product_type.id)
        qset = qset(db[table].product_publisher == db.clsb_dic_publisher.id)
        qset = qset(db[table].product_status == "Approved")
        if version_app != "":
            qset = qset(db[table].show_on.like('%' + version_app.upper() + '%'))
        if product_type:
            qset = qset(db.clsb_product_type.type_name == product_type)
        rows = qset.select(db[table].id,
                           db[table].product_category,
                           db[table].product_title,
                           db[table].product_code,
                           db[table].total_download,
                           db[table].product_price,
                           db.clsb_dic_publisher.publisher_name,
                           db.clsb_category.category_name,
                           db.clsb_category.category_code,
                           db.clsb_product_type.type_name,
                           db.clsb_dic_creator.creator_name,
                           orderby=~db[table].total_download, limitby=(0, n)).as_list()
        d = list()
        for row in rows:
            temp = dict()
            temp['product_id'] = row['clsb_product']['id']
            cover_price = db(db.clsb_product_metadata.product_id == temp['product_id']) \
                    (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                    (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                db.clsb_product_metadata.metadata_value).as_list()
            if cover_price:
                try:
                    temp['cover_price'] = int(cover_price[0]['metadata_value'])
                except Exception as e:
                    print str(e)
            else:
                temp['cover_price'] = 0
            temp['product_category'] = row['clsb_product']['product_category']
            temp['product_creator'] = row['clsb_dic_creator']['creator_name']
            temp['product_publisher'] = row['clsb_dic_publisher']['publisher_name']
            temp['product_title'] = row['clsb_product']['product_title']
            temp['product_code'] = row['clsb_product']['product_code']
            temp['total_download'] = row['clsb_product']['total_download']
            temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                        scheme=True, host=True, args=temp['product_code'])
            temp['product_price'] = row['clsb_product']['product_price']
            temp['category_name'] = row['clsb_category']['category_name']
            temp['category_code'] = row['clsb_category']['category_code']
            temp['category_type'] = row['clsb_product_type']['type_name']
            temp['free'] = check_free_for_classbook(temp['product_category'])
            #print(temp['free'])
            d.append(temp)
            #return dict(topdownload=rows)
        return dict(items=d)
    except Exception as e:
        print(e)
        return e


"""
    Get top n new product.
"""


def topnew():
    #print(request.args)
    #print(request.vars)
    if not table in db.tables(): return NOT_EXIST
    n = 0
    product_type = None

    if not request.args:
        n = 10
    elif len(request.args) == 1:
        n = int(request.args(0))
    else:
        return BAD_REQUEST
    if request.vars.product_type:
        product_type = request.vars.product_type
    version_app = ""
    if 'version' in request.vars:
        version_app = request.vars.version
    try:
        qset = db(db[table].product_category == db.clsb_category.id)
        qset = qset(db[table].product_creator == db.clsb_dic_creator.id)
        qset = qset(db.clsb_category.category_type == db.clsb_product_type.id)
        qset = qset(db[table].product_publisher == db.clsb_dic_publisher.id)
        qset = qset(db[table].product_status == "Approved")
        if version_app != "":
            qset = qset(db[table].show_on.like('%' + version_app.upper() + '%'))

        if product_type:
            qset = qset(db.clsb_product_type.type_name == product_type)

        rows = qset.select(db[table]._id,
                           db[table].product_category,
                           db[table].created_on,
                           db[table].product_title,
                           db[table].product_code,
                           db[table].total_download,
                           db[table].product_price,
                           db.clsb_dic_publisher.publisher_name,
                           db.clsb_category.category_name,
                           db.clsb_category.category_code,
                           db.clsb_product_type.type_name,
                           db.clsb_dic_creator.creator_name,
                           orderby=~db[table].created_on, limitby=(0, 100)).as_list()
        d = list()
        for row in rows:
            if len(d) < n:
                product_code = row['clsb_product']['product_code']
                check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
                if len(check_cp) > 0:
                    cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
                    path = settings.cp_dir + "CP" + str(cpid) + '/published/' + product_code
                else:
                    path = product_code
                print path
                import os.path
                if os.path.exists(settings.home_dir + path):
                    temp = dict()
                    temp['product_id'] = row['clsb_product']['id']
                    cover_price = db(db.clsb_product_metadata.product_id == temp['product_id']) \
                            (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                            (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                        db.clsb_product_metadata.metadata_value).as_list()
                    if cover_price:
                        try:
                            temp['cover_price'] = int(cover_price[0]['metadata_value'])
                        except Exception as e:
                            print str(e)
                    else:
                        temp['cover_price'] = 0
                    temp['product_category'] = row['clsb_product']['product_category']
                    temp['created_on'] = str(row['clsb_product']['created_on'])
                    temp['product_creator'] = row['clsb_dic_creator']['creator_name']
                    temp['product_publisher'] = row['clsb_dic_publisher']['publisher_name']
                    temp['product_title'] = row['clsb_product']['product_title']
                    temp['product_code'] = row['clsb_product']['product_code']
                    temp['total_download'] = row['clsb_product']['total_download']
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                scheme=True, host=True, args=temp['product_code'])
                    temp['product_price'] = row['clsb_product']['product_price']
                    temp['category_name'] = row['clsb_category']['category_name']
                    temp['category_code'] = row['clsb_category']['category_code']
                    temp['category_type'] = row['clsb_product_type']['type_name']
                    temp['free'] = check_free_for_classbook(temp['product_category'])
                    d.append(temp)
                else:
                    pass
            #return dict(topdownload=rows)
        return dict(items=d)
    except Exception as e:
        return e


def getmetadata(product_id):
    try:
        if product_id:
            product = db(db.clsb_product.id == product_id)\
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id).select().as_list()
            product_code = product[0]['clsb_product']['product_code']
            category_type = product[0]['clsb_product_type']['type_name']
            rows = db(db.clsb_product_metadata.product_id == product_id) \
                    (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                    (db.clsb_product_metadata.product_id == db.clsb_product.id).select(
                db.clsb_dic_metadata.metadata_name,
                db.clsb_product_metadata.metadata_value, ).as_list()
            #            l = list()
            d = dict()
            for row in rows:
                if row['clsb_dic_metadata']['metadata_name'] == 'co_author' and d.has_key(
                        row['clsb_dic_metadata']['metadata_name']):
                    d[row['clsb_dic_metadata']['metadata_name']] += "#" + row['clsb_product_metadata']['metadata_value']
                else:
                    d.update(
                        {row['clsb_dic_metadata']['metadata_name']: row['clsb_product_metadata']['metadata_value']})
                if row['clsb_dic_metadata']['metadata_name'] == 'product_exercise':
                    quizz = db(db.clsb_product.product_code == "Exer%s" % product_code).select(db.clsb_product.id)
                    if len(quizz) > 0:
                        d["quiz"] = URL(a="cbw", c="default", f="store_detail", args=quizz.first().id, extension="")

            if os.path.exists('applications/cbw/static/flash/' + product_code):
                d.update({'preview': URL(a='cbw', c='static/flash/' + product_code, f='index.html', host=True)})
            else:
                d.update({'preview': ''})
            if category_type == 'Book':
                try:
                    if d.has_key('product_price'):
                        d.update({'product_price': d['cover_price']})
                    else:
                        d['product_price'] = d['cover_price']
                except Exception as err:
                    print(str(err))

            #print(d)
            return dict(item=d)
    except Exception as e:
        return e

def metadatainfo():
    """
        Get product's metadatainfo. (by product id)
    """
    try:
        if request.args:
            product = db(db.clsb_product.id == request.args(0))\
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id).select().as_list()
            product_code = product[0]['clsb_product']['product_code']
            category_type = product[0]['clsb_product_type']['type_name']
            rows = db(db.clsb_product_metadata.product_id == request.args(0)) \
                    (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                    (db.clsb_product_metadata.product_id == db.clsb_product.id).select(
                db.clsb_dic_metadata.metadata_name,
                db.clsb_product_metadata.metadata_value, ).as_list()
            #            l = list()
            d = dict()
            for row in rows:
                if row['clsb_dic_metadata']['metadata_name'] == 'co_author' and d.has_key(
                        row['clsb_dic_metadata']['metadata_name']):
                    d[row['clsb_dic_metadata']['metadata_name']] += "#" + row['clsb_product_metadata']['metadata_value']
                else:
                    d.update(
                        {row['clsb_dic_metadata']['metadata_name']: row['clsb_product_metadata']['metadata_value']})
                if row['clsb_dic_metadata']['metadata_name'] == 'product_exercise':
                    quizz = db(db.clsb_product.product_code == "Exer%s" % product_code).select(db.clsb_product.id)
                    if len(quizz) > 0:
                        d["quiz"] = URL(a="cbw", c="default", f="store_detail", args=quizz.first().id, extension="")

            if os.path.exists('applications/cbw/static/flash/' + product_code):
                d.update({'preview': URL(a='cbw', c='static/flash/' + product_code, f='index.html', host=True)})
            else:
                d.update({'preview': ''})
            if category_type == 'Book':
                try:
                    if d.has_key('product_price'):
                        d.update({'product_price': d['cover_price']})
                    else:
                        d['product_price'] = d['cover_price']
                except Exception as err:
                    print(str(err))

            #print(d)
            return dict(item=d)
    except Exception as e:
        return e


"""
    Get product's version.
"""


def version(): # product_code
    if len(request.args) == 1:
        try:
            product_id = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id).as_list()[0][
                'id']
        except Exception as e:
            return dict(error=CB_0015)#PRODUCT_CODE_NOT_EXIST
        try:
            rows = db(db.clsb_product_metadata.product_id == product_id) \
                    (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                    (db.clsb_product_metadata.product_id == db.clsb_product.id).select(
                db.clsb_dic_metadata.metadata_name,
                db.clsb_product_metadata.metadata_value).as_list()

            d = dict()
            version = "-1"
            for row in rows:
                if row['clsb_dic_metadata']['metadata_name'] == "version":
                    val = row['clsb_product_metadata']['metadata_value']
                    if val >= version:
                        version = val
            d.update({"version": version})
            return dict(items=d)
        except Exception as e:
            return dict(error=CB_0003) #DB_RQ_FAILD
    else:
        return dict(error=BAD_REQUEST)


"""
    Get product's detail.
"""


def getinfo(): #args: product_id, store_version
    try:
        msg = ""
        # remove for old version Store, CBM, CBW
        # if not (request.args(1)):
        #     msg = "<h3 style='color: red;'>Phiên bản phần mềm bạn trên thiết bị cần cập nhật bản mới nhất để tải sản phẩm này</h3>"
        # isStoreApp = False
        # try:
        #     if 'store_app' in request.vars:
        #         isStoreApp = True
        # except Exception as err:

        product = dict()
        if request.args:
            product_id = request.args[0]

            db_product = db(db.clsb_product.id == product_id) \
                    (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id) \
                    (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                          db.clsb_category.ALL,
                                                                                          db.clsb_product_type.type_name,
                                                                                          db.clsb_product.product_collection,
                                                                                          db.clsb_dic_creator.creator_name,
                                                                                          db.clsb_dic_publisher.publisher_name,
                                                                                          db.clsb_product.product_title,
                                                                                          db.clsb_product.created_on,
                                                                                          db.clsb_product.product_code,
                                                                                          db.clsb_product.product_status,
                                                                                          db.clsb_device_shelf.device_shelf_code,
                                                                                          db.clsb_device_shelf.device_shelf_type,
                                                                                          db.clsb_device_shelf.device_shelf_name,
                                                                                          db.clsb_product.product_price,
                                                                                          db.clsb_product.product_description, ).first()
            product_code = db_product['clsb_product']['product_code']
            cpid = None
            check_cp = db(db.clsb_product.product_code.like(product_code))(
                db.clsb20_product_cp.product_code.like(product_code)).select()
            if len(check_cp) > 0:
                cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            seller = ""
            if cpid == None:
                seller = "Nhà xuất bản giáo dục"
            else:
                seller = db(db.auth_user.id == cpid).select().first()
                seller = seller.first_name + " " + seller.last_name

            if not (request.args(1)):
                if check_product_for_old_version(product_code):
                    msg = "<h3 style='color: red;'>Phiên bản phần mềm bạn trên thiết bị cần cập nhật bản mới nhất để tải sản phẩm này</h3><br/>"
                elif db_product['clsb_product']['product_price'] > 0:
                    msg = "<h3 style='color: red;'>Bạn phải trả phí cho sản phẩm này cho lần tải đầu tiên, các lần tải lại khi bị lỗi hoặc tải thêm là miễn phí</h3><br/>"

            if db_product and db_product['clsb_product']['product_status'] == 'Approved':
                db_relation = dict()
                db_relation['collection_name'] = None
                if db_product['clsb_product']['product_collection']:
                    db_relation = db(db.clsb_collection.id == db_product['clsb_product']['product_collection']).select(
                        db.clsb_collection.ALL).first()
                product['id'] = db_product['clsb_product']['id']
                product['category_id'] = db_product['clsb_category']['id']
                if db_product['clsb_product']['created_on'] is None:
                    product['product_time'] = '01 - 01 - 2013'
                else:
                    product['product_time'] = db_product['clsb_product']['created_on'].strftime('%d - %m - %Y')
                product['category_name'] = db_product['clsb_category']['category_name']
                product['category_code'] = db_product['clsb_category']['category_code']
                product['category_type'] = db_product['clsb_product_type']['type_name']
                product['device_self_code'] = db_product['clsb_device_shelf']['device_shelf_code']
                product['device_self_type'] = db_product['clsb_device_shelf']['device_shelf_type']
                product['device_shelf_name'] = db_product['clsb_device_shelf']['device_shelf_name']
                product['seller'] = seller
                product['purchase'] = get_purchase_description(db_product['clsb_product']['product_code'])
                product['collection_name'] = db_relation['collection_name'] or ''
                product['creator_name'] = db_product['clsb_dic_creator']['creator_name']
                product['publisher_name'] = db_product['clsb_dic_publisher']['publisher_name']
                product['product_title'] = db_product['clsb_product']['product_title']
                product['product_code'] = db_product['clsb_product']['product_code']
                product['product_cover'] = URL(a='cbs', c='download', f='cover',scheme=True, host=True, args=db_product['clsb_product']['product_code'])
                product['product_thumb'] = URL(a='cbs', c='download', f='thumb',
                                               scheme=True, host=True, args=db_product['clsb_product']['product_code'])
                product['product_data'] = URL(a='cbs', c='download', f='data',
                                              scheme=True, host=True, args=db_product['clsb_product']['product_code'])
                product['product_pdf'] = URL(a='cbs', c='download', f='product',
                                             scheme=True, host=True, args=db_product['clsb_product']['product_code'])
                product['product_price'] = db_product['clsb_product']['product_price']
                product['product_description'] = msg + db_product['clsb_product']['product_description']
                product['free'] = check_free_for_classbook(product['category_id'])
                if len(request.args) >= 3 and product['free']:
                    product['product_price'] = 0
                # if product['free'] and isStoreApp:
                #     product['product_price'] = 0

        return dict(product=product)
    except Exception as ex:
        print(str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def get_list_product_by_id():
    list_products = list()
    try:
        token = request.vars.token
        select_db_product = db(db.clsb_product.id.belongs(request.args)) \
                    (db.clsb_product.product_status.like("Approved"))\
                    (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id) \
                    (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                          db.clsb_category.category_name,
                                                                                          db.clsb_product_type.type_name,
                                                                                          db.clsb_dic_creator.creator_name,
                                                                                          db.clsb_product.product_title,
                                                                                          db.clsb_product.product_code,
                                                                                          db.clsb_product.product_status,
                                                                                          db.clsb_product.product_price)
        for db_product in select_db_product:
            product = dict()
            product['id'] = db_product['clsb_product']['id']
            product['category_type'] = db_product['clsb_product_type']['type_name']
            product['category_name'] = db_product['clsb_category']['category_name']
            product['creator_name'] = db_product['clsb_dic_creator']['creator_name']
            product['product_title'] = db_product['clsb_product']['product_title']
            product['product_code'] = db_product['clsb_product']['product_code']
            product['product_cover'] = URL(a='cbs', c='download', f='cover', args=db_product['clsb_product']['product_code'])
            product['product_price'] = db_product['clsb_product']['product_price']
            metadata = getmetadata(product['id'])
            if metadata is None or 'error' in metadata:
                metadata = dict()
            else:
                metadata = metadata['item']
                if 'cover_price' in metadata:
                    if int(metadata['cover_price']) > int(product['product_price']):
                        product['cover_price'] = int(metadata['cover_price'])
                    else:
                        metadata['cover_price'] = 0
                        product['cover_price'] = 0
                else:
                    product['cover_price'] = 0
            check_buy = check_buy_product(product['id'], token)
            if 'result' in check_buy:
                check_buy = check_buy['result']
            else:
                check_buy = False
            check_media = check_buy_media(product['id'], token)
            if 'result' in check_media:
                check_media = check_media['result']
            else:
                check_media = False
            check_quiz = check_buy_quiz(product['id'], token)
            if 'result' in check_quiz:
                check_quiz = check_quiz['result']
            else:
                check_quiz = False

            has_quiz = False
            has_media = check_has_media(product['product_code'])['check']
            has_quiz = check_product_exist("Exer"+product['product_code'])
            data_price = get_data_price(product['id'])
            price_media = 0
            price_quiz = 0
            if has_quiz:
                if 'quiz' in data_price:
                    price_quiz = data_price['quiz']
                else:
                    price_quiz = 5000
            if has_media:
                if 'media' in data_price:
                    price_media = data_price['media']
            total_media = 0
            if not check_quiz and price_quiz > 0:
                total_media += price_quiz
            if not check_media and price_media > 0:
                total_media += price_media
            total_price = 0
            if not check_buy:
                total_price = total_media + product['product_price']
            total_cover = total_price
            if product['cover_price'] > 0 and total_price > 0:
                total_cover = total_media + product['cover_price']
            payment = dict(price_media=price_media, price_quiz=price_quiz)
            product['check_buy'] = check_buy
            product['check_media'] = check_media
            product['check_quiz'] = check_quiz
            product['has_media'] = has_media
            product['has_quiz'] = has_quiz
            product['payment'] = payment
            product['total_media'] = total_media
            product['total_price'] = total_price
            product['total_cover'] = total_cover
            list_products.append(product)
        return dict(product=list_products)
    except Exception as ex:
        print(str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def get_info_by_code(): #args: product_code, store_version
    try:
        msg = ""
        # remove for old version Store, CBM, CBW
        # if not (request.args(1)):
        #     msg = "<h3 style='color: red;'>Phiên bản phần mềm bạn trên thiết bị cần cập nhật bản mới nhất để tải sản phẩm này</h3>"
        product = dict()
        if request.args:
            product_code = request.args[0]

            db_product = db(db.clsb_product.product_code == product_code) \
                    (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id) \
                    (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                          db.clsb_category.ALL,
                                                                                          db.clsb_product_type.type_name,
                                                                                          db.clsb_product.product_collection,
                                                                                          db.clsb_dic_creator.creator_name,
                                                                                          db.clsb_dic_publisher.publisher_name,
                                                                                          db.clsb_product.product_title,
                                                                                          db.clsb_product.created_on,
                                                                                          db.clsb_product.product_code,
                                                                                          db.clsb_product.product_status,
                                                                                          db.clsb_device_shelf.device_shelf_code,
                                                                                          db.clsb_device_shelf.device_shelf_type,
                                                                                          db.clsb_device_shelf.device_shelf_name,
                                                                                          db.clsb_product.product_price,
                                                                                          db.clsb_product.product_description, ).first()

            cpid = None
            check_cp = db(db.clsb_product.product_code.like(product_code))(
                db.clsb20_product_cp.product_code.like(product_code)).select()
            if len(check_cp) > 0:
                cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            seller = ""
            if cpid == None:
                seller = "Nhà xuất bản giáo dục"
            else:
                seller = db(db.auth_user.id == cpid).select().first()
                seller = seller.first_name + " " + seller.last_name

            if not (request.args(1)):
                if check_product_for_old_version(product_code):
                    msg = "<h3 style='color: red;'>Phiên bản phần mềm bạn trên thiết bị cần cập nhật bản mới nhất để tải sản phẩm này</h3><br/>"
                elif db_product['clsb_product']['product_price'] > 0:
                    msg = "<h3 style='color: red;'>Bạn phải trả phí cho sản phẩm này cho lần tải đầu tiên, các lần tải lại khi bị lỗi hoặc tải thêm là miễn phí</h3><br/>"

            # get metadata named: version
            metadata_version = db(db.clsb_dic_metadata.metadata_name == 'version').select(
                db.clsb_dic_metadata.id).first()

            if db_product and db_product['clsb_product']['product_status'] == 'Approved':
                metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == db_product['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_version_value is None:
                    metadata_version_value = dict()
                    metadata_version_value['metadata_value'] = 0
                db_relation = dict()
                db_relation['collection_name'] = None
                if db_product['clsb_product']['product_collection']:
                    db_relation = db(db.clsb_collection.id == db_product['clsb_product']['product_collection']).select(
                        db.clsb_collection.ALL).first()
                product['id'] = db_product['clsb_product']['id']
                product['category_id'] = db_product['clsb_category']['id']
                if db_product['clsb_product']['created_on'] is None:
                    product['product_time'] = '01 - 01 - 2013'
                else:
                    product['product_time'] = db_product['clsb_product']['created_on'].strftime('%d - %m - %Y')
                product['category_name'] = db_product['clsb_category']['category_name']
                product['category_code'] = db_product['clsb_category']['category_code']
                product['category_type'] = db_product['clsb_product_type']['type_name']
                product['device_self_code'] = db_product['clsb_device_shelf']['device_shelf_code']
                product['device_self_type'] = db_product['clsb_device_shelf']['device_shelf_type']
                product['device_shelf_name'] = db_product['clsb_device_shelf']['device_shelf_name']
                product['seller'] = seller
                product['version'] = metadata_version_value['metadata_value']
                product['purchase'] = get_purchase_description(db_product['clsb_product']['product_code'])
                product['collection_name'] = db_relation['collection_name'] or ''
                product['creator_name'] = db_product['clsb_dic_creator']['creator_name']
                product['publisher_name'] = db_product['clsb_dic_publisher']['publisher_name']
                product['product_title'] = db_product['clsb_product']['product_title']
                product['product_code'] = product_code
                product['product_cover'] = URL(a='cbs', c='download', f='cover',
                                               scheme=True, host=True, args=product_code)
                product['product_thumb'] = URL(a='cbs', c='download', f='thumb',
                                               scheme=True, host=True, args=product_code)
                product['product_data'] = URL(a='cbs', c='download', f='data',
                                              scheme=True, host=True, args=product_code)
                product['product_pdf'] = URL(a='cbs', c='download', f='product',
                                             scheme=True, host=True, args=product_code)
                product['product_price'] = db_product['clsb_product']['product_price']
                product['product_description'] = msg + db_product['clsb_product']['product_description']
                product['free'] = check_free_for_classbook(product['category_id'])
                product['cpid'] = cpid

        return dict(product=product)
    except Exception as ex:
    #        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
        return "D" + ex.message + str(sys.exc_traceback.tb_lineno)


"""
    Get quiz's detail.
"""


def getquizinfo(): #args:  product_id/subject_id/class_id
    try:
        product = dict()
        if request.args and len(request.args) == 3:
            product_id = request.args[0]
            subject_id = request.args[1]
            class_id = request.args[2]

            subject_class_id = db(db.clsb_subject_class.subject_id == subject_id) \
                    (db.clsb_subject_class.class_id == class_id).select(db.clsb_subject_class.id).as_list()
            subject_class_id = subject_class_id[0]['id']

            db_product = db(db.clsb_product.id == product_id) \
                    (db.clsb_product.product_status == 'Approved') \
                    (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                    (db.clsb_product.subject_class == subject_class_id) \
                    (db.clsb_product.subject_class == db.clsb_subject_class.id) \
                    (db.clsb_subject_class.subject_id == db.clsb_subject.id) \
                    (db.clsb_subject_class.class_id == db.clsb_class.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id) \
                    (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                          db.clsb_category.ALL,
                                                                                          db.clsb_product_type.type_name,
                                                                                          db.clsb_product.product_collection,
                                                                                          db.clsb_dic_creator.creator_name,
                                                                                          db.clsb_dic_publisher.publisher_name,
                                                                                          db.clsb_product.product_title,
                                                                                          db.clsb_product.created_on,
                                                                                          db.clsb_product.product_code,
                                                                                          db.clsb_product.product_status,
                                                                                          db.clsb_product.product_price,
                                                                                          db.clsb_product.product_description,
                                                                                          db.clsb_product.subject_class,

                                                                                          db.clsb_device_shelf.device_shelf_code,
                                                                                          db.clsb_device_shelf.device_shelf_type,
                                                                                          db.clsb_device_shelf.device_shelf_name,

                                                                                          db.clsb_subject.subject_name,
                                                                                          db.clsb_subject.subject_code,
                                                                                          db.clsb_subject.id,

                                                                                          db.clsb_class.class_name,
                                                                                          db.clsb_class.class_code,
                                                                                          db.clsb_class.id,

            ).first()
            if db_product and db_product['clsb_product']['product_status'] == 'Approved':
                db_relation = dict()
                db_relation['collection_name'] = None
                if db_product['clsb_product']['product_collection']:
                    db_relation = db(db.clsb_collection.id == db_product['clsb_product']['product_collection']).select(
                        db.clsb_collection.ALL).first()
                product['id'] = db_product['clsb_product']['id']
                product['category_id'] = db_product['clsb_category']['id']
                product['product_time'] = db_product['clsb_product']['created_on'].strftime('%d - %m - %Y')
                product['category_name'] = db_product['clsb_category']['category_name']
                product['category_code'] = db_product['clsb_category']['category_code']
                product['category_type'] = db_product['clsb_product_type']['type_name']
                product['device_self_code'] = db_product['clsb_device_shelf']['device_shelf_code']
                product['device_self_type'] = db_product['clsb_device_shelf']['device_shelf_type']
                product['device_shelf_name'] = db_product['clsb_device_shelf']['device_shelf_name']

                product['collection_name'] = db_relation['collection_name'] or ''
                product['creator_name'] = db_product['clsb_dic_creator']['creator_name']
                product['publisher_name'] = db_product['clsb_dic_publisher']['publisher_name']
                product['product_title'] = db_product['clsb_product']['product_title']
                product['product_code'] = db_product['clsb_product']['product_code']
                product['subject_class'] = int(db_product['clsb_product']['subject_class'])
                #                 product['product_cover'] = URL(a = 'cbs', c = 'download', f = 'cover',
                #                  scheme = True, host = True, args = db_product['clsb_product']['product_code'])
                #                 product['product_thumb'] = URL(a = 'cbs', c = 'download', f = 'thumb',
                #                  scheme = True, host = True, args = db_product['clsb_product']['product_code'])
                product['product_data'] = URL(a='cbs', c='download', f='data',
                                              scheme=True, host=True, args=db_product['clsb_product']['product_code'])
                product['product_pdf'] = URL(a='cbs', c='download', f='product',
                                             scheme=True, host=True, args=db_product['clsb_product']['product_code'])
                product['product_price'] = db_product['clsb_product']['product_price']
                product['product_description'] = db_product['clsb_product']['product_description']

                product['subject_name'] = db_product['clsb_subject']['subject_name']
                product['subject_id'] = db_product['clsb_subject']['id']

                product['class_name'] = db_product['clsb_class']['class_name']
                product['class_code'] = db_product['clsb_class']['class_code']
                product['class_id'] = db_product['clsb_class']['id']

        return dict(product=product)
    except Exception as ex:
        print 'Loi : ' + str(ex)
        #        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
        return ex

# hant
"""
    Search advance with category name, creator name, class id, subject id, keyword.
"""


def search_advance():

    try:
        category_type = None
        page = 0
        items_per_page = 18
        #Pagination
        try:
            if len(request.args) > 0: page = int(request.args[0])
            if len(request.args) > 1: items_per_page = int(request.args[1])
            #if len(request.args) > 2: category_type = request.args[2]
        except (TypeError, ValueError):
            pass
        limitby = (page * items_per_page, (page + 1) * items_per_page)

        creator_name = request.vars["creator_name"]
        category_id = request.vars["category_id"]
        class_id = request.vars["class_id"]
        subject_id = request.vars["subject_id"]
        store_search = request.vars["store_search"]
        version = ""
        if 'version' in request.vars:
            version = request.vars.version

        if 'creator_name' not in request.vars:
            return search_multiple(store_search, category_id, subject_id, class_id, page, items_per_page, limitby,
                                   category_type, version)
        elif creator_name:
        #             print '*************'
        #             print search_by_creator(creator_name, page, items_per_page, limitby)
            return search_by_creator(creator_name, page, items_per_page, limitby, version)

    except Exception as e:
        return dict(error=str(e))


def search_multiple(store_search, category_id, subject_id, class_id, page, items_per_page, limitby, category_type, version=""):
    try:
        if store_search:
            result_id = list()
            key_word = store_search.replace(" ", "+")
            key_word = khongdau(key_word)
            url_search = "http://app.classbook.vn/cbs20/solr/search.json?key=" + key_word + "&row=500"
            print("url: " + url_search)
            get_data = urllib2.urlopen(url_search)
            str_json = str(get_data.read())
            get_data = json.loads(str_json)
            for product_id in get_data['docs']:
                result_id.append(int(product_id['id']))
            #print("result_id: " + str(result_id))

        products = list()
        queries = []

        queries.append(db.clsb_product.product_status.like('Approved'))
        queries.append(~db.clsb_product.product_code.like('Exer%'))
        queries.append(db.clsb_product.product_creator == db.clsb_dic_creator.id)
        queries.append(db.clsb_product.product_publisher == db.clsb_dic_publisher.id)
        queries.append(db.clsb_category.category_type == db.clsb_product_type.id)
        queries.append(db.clsb_product.product_category == db.clsb_category.id)

        fields = list()
        fields.append(db.clsb_product.id)
        fields.append(db.clsb_product.product_title)
        fields.append(db.clsb_product.product_price)
        fields.append(db.clsb_product.product_code)
        fields.append(db.clsb_product.created_on)
        fields.append(db.clsb_product.id)
        fields.append(db.clsb_product_type.type_name)
        fields.append(db.clsb_dic_creator.creator_name)
        fields.append(db.clsb_dic_publisher.publisher_name)
        fields.append(db.clsb_category.ALL)

        if category_id:
            queries.append(db.clsb_category.category_parent == category_id)
        #         else :
        #             if category_code :
        #                 category_id = db(db.clsb_category.category_code.like('%' + category_code + '%')).select(db.clsb_category.id)
        #                 queries.append(db.clsb_category.id == category_id[0])
        #                 print category_id
        if category_type:
            category_type_id = db(db.clsb_product_type.type_name.like('%' + category_type + '%')).select(
                db.clsb_product_type.id)
            queries.append(db.clsb_category.category_type == category_type_id[0].id)

        if subject_id:
            queries.append(db.clsb_subject.id == subject_id)
            queries.append(db.clsb_product.subject_class == db.clsb_subject_class.id)
            queries.append(db.clsb_subject_class.subject_id == db.clsb_subject.id)
            queries.append(db.clsb_subject_class.class_id == db.clsb_class.id)

            fields.append(db.clsb_subject.subject_name)
            fields.append(db.clsb_class.class_name)

        if class_id:
            queries.append(db.clsb_class.id == class_id)
            queries.append(db.clsb_product.subject_class == db.clsb_subject_class.id)
            queries.append(db.clsb_subject_class.class_id == db.clsb_class.id)
            queries.append(db.clsb_subject_class.subject_id == db.clsb_subject.id)

            fields.append(db.clsb_subject.subject_name)
            fields.append(db.clsb_class.class_name)

        if store_search:
            queries.append(db.clsb_product.id.belongs(result_id))
        if version != "":
            queries.append((db.clsb_product.show_on.like('%' + version.upper() + '%')))

        query = reduce(lambda a, b: a & b, queries)

        rows = db(query).select(*fields, orderby=~db.clsb_product.created_on).as_list()
        if rows:
            if store_search:
                query_id = list()
                for row in rows:
                    query_id.append(int(row['clsb_product']['id']))
                for result in result_id:
                    if result in query_id:
                        index = query_id.index(int(result))
                        row = rows[index]
                        products.append(row2dict(row))
            else:
                for row in rows:
                    products.append(row2dict(row))
        total_items = len(products)
        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page
        products = products[limitby[0]:limitby[1]]

        return dict(page=page, total_items=str(total_items), total_pages=str(total_pages),
                    items_per_page=items_per_page, products=products)

    except Exception as e:
        print(str(e) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(e) + " on line " + str(sys.exc_traceback.tb_lineno))

def row2dict(row):
    temp = dict()
    temp['id'] = row['clsb_product']['id']
    temp['co_author'] = ''
    co_authors = db(db.clsb_dic_metadata.metadata_name == 'co_author') \
                            (db.clsb_product_metadata.product_id == temp['id']) \
                            (db.clsb_dic_metadata.id == db.clsb_product_metadata.metadata_id).select(
                        db.clsb_product_metadata.metadata_value).as_list()
    if co_authors:
        for item in co_authors:
            temp['co_author'] += "#" + item['metadata_value']

    cover_price = db(db.clsb_product_metadata.product_id == row['clsb_product']['id']) \
                            (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                            (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                        db.clsb_product_metadata.metadata_value).as_list()
    if cover_price:
        try:
            temp['cover_price'] = int(cover_price[0]['metadata_value'])
        except Exception as e:
            print str(e)
    else:
        temp['cover_price'] = 0

    temp['category_id'] = row['clsb_category']['id']
    temp['category_name'] = row['clsb_category']['category_name']
    temp['category_code'] = row['clsb_category']['category_code']
    temp['category_type'] = row['clsb_product_type']['type_name']
    temp['creator_name'] = row['clsb_dic_creator']['creator_name']
    temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
    temp['product_title'] = row['clsb_product']['product_title']
    temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                scheme=True, host=True, args=row['clsb_product']['product_code'])
    temp['product_code'] = row['clsb_product']['product_code']
    temp['product_price'] = row['clsb_product']['product_price']

    if 'clsb_subject' in row and row['clsb_subject']['subject_name']:
        temp['subject_name'] = row['clsb_subject']['subject_name']
    else:
        temp['subject_name'] = ''
    if 'clsb_class' in row and row['clsb_class']['class_name']:
        temp['class_name'] = row['clsb_class']['class_name']
    else:
        temp['class_name'] = ''
    return temp

def cal_set_price(set_id):

    rows = db(db.clsb30_set_product.set_purchase_id == set_id).select(db.clsb30_set_product.ALL)

    price = 0
    for row in rows:
        product = db(db.clsb_product.id == row.product_id).select(db.clsb_product.product_price).first()
        price += float(product.product_price)
    return price

def search_set_purchase(key_world):
    rows = db(db.clsb30_set_purchase)
    pass


# hant
def search_by_creator(creator_name, page, items_per_page, limitby, version=""):
    try:
        products = list()
        total_pages = 0
        if creator_name:
            query = db(db.clsb_product.product_status.like('Approved')) \
                    (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id)
            if version != "":
                query = query(db.clsb_product.show_on.like('%' + version.upper() + '%'))
            #             creator_name = request.vars["creator_name"]

            query1 = query((db.clsb_product_metadata.metadata_value.contains(creator_name)) &
                           (db.clsb_dic_metadata.metadata_name == 'co_author') &
                           (db.clsb_product.id == db.clsb_product_metadata.product_id) &
                           (db.clsb_dic_metadata.id == db.clsb_product_metadata.metadata_id))

            query2 = query((db.clsb_product.product_creator == db.clsb_dic_creator.id) &
                           (db.clsb_dic_creator.creator_name.contains(creator_name))) \
 \
            #             total_items = query1.count() + query2.count()

            #             print "total_items " + str(total_items)


            products1 = query1.select(db.clsb_product.id,
                                      db.clsb_category.ALL,
                                      db.clsb_product_type.type_name,
                                      db.clsb_dic_creator.creator_name,
                                      db.clsb_dic_publisher.publisher_name,
                                      db.clsb_product.product_title,
                                      db.clsb_product.product_price,
                                      db.clsb_product.product_code,
                                      db.clsb_product_metadata.metadata_value).as_list()

            products2 = query2.select(db.clsb_product.id,
                                      db.clsb_category.ALL,
                                      db.clsb_product_type.type_name,
                                      db.clsb_dic_creator.creator_name,
                                      db.clsb_dic_publisher.publisher_name,
                                      db.clsb_product.product_title,
                                      db.clsb_product.product_price,
                                      db.clsb_product.product_code,
                                      db.clsb_product.created_on,
                                      order_by=~db.clsb_product.created_on).as_list()

            if products2:
                for row in products2:
                #                     dup = False
                    temp = dict()
                    temp['id'] = row['clsb_product']['id']
                    temp['co_author'] = ''
                    co_authors = db(db.clsb_dic_metadata.metadata_name == 'co_author') \
                            (db.clsb_product_metadata.product_id == temp['id']) \
                            (db.clsb_dic_metadata.id == db.clsb_product_metadata.metadata_id).select(
                        db.clsb_product_metadata.metadata_value).as_list()
                    if co_authors:
                        for item in co_authors:
                            temp['co_author'] += "#" + item['metadata_value']
                    temp['category_id'] = row['clsb_category']['id']
                    free = check_free_for_classbook(temp['category_id'])
                    temp['free'] = free["result"]
                    temp['category_name'] = row['clsb_category']['category_name']
                    temp['category_code'] = row['clsb_category']['category_code']
                    temp['category_type'] = row['clsb_product_type']['type_name']
                    temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                    temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                    temp['product_title'] = row['clsb_product']['product_title']
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                scheme=True, host=True, args=row['clsb_product']['product_code'])
                    temp['product_code'] = row['clsb_product']['product_code']
                    temp['product_price'] = row['clsb_product']['product_price']
                    products.append(temp)

            if products1:
                for row in products1:
                    dup = False
                    temp = dict()
                    temp['id'] = row['clsb_product']['id']
                    temp['category_id'] = row['clsb_category']['id']
                    free = check_free_for_classbook(temp['category_id'])
                    temp['free'] = free["result"]
                    temp['category_name'] = row['clsb_category']['category_name']
                    temp['category_code'] = row['clsb_category']['category_code']
                    temp['category_type'] = row['clsb_product_type']['type_name']
                    temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                    temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                    temp['product_title'] = row['clsb_product']['product_title']
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                scheme=True, host=True, args=row['clsb_product']['product_code'])
                    temp['product_code'] = row['clsb_product']['product_code']
                    temp['product_price'] = row['clsb_product']['product_price']
                    temp['co_author'] = row['clsb_product_metadata']['metadata_value']
                    for elem in products:
                        if temp['id'] == elem['id']:
                            elem['co_author'] += "#" + temp['co_author']
                            dup = True
                    if dup == False:
                        products.append(temp)
        total_items = len(products)

        products = products[limitby[0]:limitby[1]]
        #         print p

        #             return dict(row1 = a_products, row2 = b_products)

        #             total_items = product_query.count()

        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page
        #         print "------------------------------"
        #         print str(limitby[0]) + " " + str(limitby[1])
        #
        #         print total_itemss
        #         print total_pages

        return dict(page=page, total_items=str(total_items), total_pages=str(total_pages),
                    items_per_page=items_per_page, products=products)
    except Exception as e:
        return dict(error=e)

def search():
    try:
        products = list()
        page = 0
        category_type = None
        items_per_page = settings.items_per_page
        if request.vars:
            keyword = request.vars["store_search"]
            if len(keyword) <= 0:
                return dict(page=page, total_items=0, total_pages=0, items_per_page=items_per_page, products=list())
                #Pagination
            try:
                if len(request.args) > 0:
                    page = int(request.args[0])
                if len(request.args) > 1:
                    items_per_page = int(request.args[1])
                    #PhuongNH : request.args[2] : category_type
                #if len(request.args) > 2:
                    #category_type = request.args[2]
            except (TypeError, ValueError):
                pass
            limitby = (page * items_per_page, (page + 1) * items_per_page)
            # if request containt category_type
            search_query = db(((db.clsb_product.product_code == keyword) \
                                  | (db.clsb_product.product_title.contains(keyword)) \
                                  | (db.clsb_dic_creator.creator_name.contains(keyword)) \
                                  | (db.clsb_dic_publisher.publisher_name.contains(keyword)) \
                                  | (db.clsb_product.product_description.contains(keyword)) \
                                  | (db.clsb_category.category_name.contains(keyword))))
            if 'version' in request.vars:
                search_query = search_query(db.clsb_product.show_on.like('%' + request.vars.version.upper() + '%'))
            if category_type is not None:
                category_id = db(db.clsb_product_type.type_name.like('%' + category_type + '%')).select(
                    db.clsb_product_type.id)
                total_items = search_query((db.clsb_category.category_type == int(category_id[0]) )) \
                        (db.clsb_product.product_status.like('Approved')) \
                        (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                        (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                        (db.clsb_category.category_type == db.clsb_product_type.id) \
                        (db.clsb_product.product_category == db.clsb_category.id).count()

                total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

                db_product = search_query((db.clsb_category.category_type == int(category_id[0]))) \
                        (db.clsb_product.product_status.like('Approved')) \
                        (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                        (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                        (db.clsb_category.category_type == db.clsb_product_type.id) \
                        (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                         db.clsb_category.ALL,
                                                                                         db.clsb_product_type.type_name,
                                                                                         db.clsb_dic_creator.creator_name,
                                                                                         db.clsb_dic_publisher.publisher_name,
                                                                                         db.clsb_product.product_title,
                                                                                         db.clsb_product.product_price,
                                                                                         db.clsb_product.product_code,
                                                                                         limitby=limitby).as_list()
            else:
                total_items = search_query(db.clsb_product.product_status.like('Approved')) \
                        (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                        (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                        (db.clsb_category.category_type == db.clsb_product_type.id) \
                        (db.clsb_product.product_category == db.clsb_category.id).count()

                total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

                db_product = search_query(db.clsb_product.product_status.like('Approved')) \
                        (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                        (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                        (db.clsb_category.category_type == db.clsb_product_type.id) \
                        (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                         db.clsb_category.ALL,
                                                                                         db.clsb_product_type.type_name,
                                                                                         db.clsb_dic_creator.creator_name,
                                                                                         db.clsb_dic_publisher.publisher_name,
                                                                                         db.clsb_product.product_title,
                                                                                         db.clsb_product.product_price,
                                                                                         db.clsb_product.product_code,
                                                                                         limitby=limitby).as_list()

            if db_product:
                for row in db_product:
                    temp = dict()
                    temp['id'] = row['clsb_product']['id']
                    temp['category_id'] = row['clsb_category']['id']
                    free = check_free_for_classbook(temp['category_id'])
                    temp['free'] = free
                    temp['category_name'] = row['clsb_category']['category_name']
                    temp['category_code'] = row['clsb_category']['category_code']
                    temp['category_type'] = row['clsb_product_type']['type_name']
                    temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                    temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                    temp['product_title'] = row['clsb_product']['product_title']
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                scheme=True, host=True, args=row['clsb_product']['product_code'])
                    temp['product_code'] = row['clsb_product']['product_code']
                    temp['product_price'] = row['clsb_product']['product_price']
                    #                    temp['product_description'] = row['clsb_product']['product_description']
                    products.append(temp)
        return dict(page=page, total_items=total_items, total_pages=total_pages, items_per_page=items_per_page,
                    products=products)
    except Exception as ex:
        raise HTTP(500, "Bad request")

#
# def version(): #args: product_code, device_serial

def change_version():
    category_code = request.args[0]
    category = db(db.clsb_category.category_code == category_code).select().first()
    if category:
        cate_id = category['id']
        product_list = db(db.clsb_product.product_category == cate_id).select()
        if product_list:
            metadata_id = db(db.clsb_dic_metadata.metadata_name == 'version').select().first()
            if metadata_id:
                metadata_id = metadata_id['id']
                for product in product_list:
                    product_id = product['id']
                    created_date = str(product['created_on'])
                    index = created_date.rfind(' ')
                    created_date = created_date[:index]
                    created_date = created_date.replace('-', '')
                    db.clsb_product_metadata.insert(product_id=product_id, metadata_id=metadata_id,
                                                    metadata_value=str(created_date))


def getVersionByCate():
    if request.args and len(request.args) > 0:
        cate_code = request.args[0]
        productsList = list()
        cate_id = db(db.clsb_category.category_code == cate_code).select().first()

        if cate_id:
            cate_id = cate_id['id']

            metadata_version = db(db.clsb_dic_metadata.metadata_name == 'version').select().first()

            if metadata_version:
                metadata_version = metadata_version['id']
            else:
                db.clsb_dic_metadata.insert(metadata_name='version', metadata_label='version',
                                            metadata_description='version')
                metadata_version = db(db.clsb_dic_metadata.metadata_name == 'version').select().first()
                metadata_version = metadata_version['id']

            product_list = db((db.clsb_product.product_category == cate_id) & (
            db.clsb_product.product_status.like("Approved"))).select()
            if product_list:
                for product in product_list:
                    product_metadata_version = db(db.clsb_product_metadata.product_id == product['id']) \
                            (db.clsb_product_metadata.metadata_id == metadata_version).select().first()
                    if product_metadata_version is None:
                        version = -1
                    else:
                        version = product_metadata_version['metadata_value']
                    temp = dict()
                    temp['id'] = product['id']
                    temp['product_code'] = product['product_code']
                    temp['product_title'] = product['product_title']
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                scheme=True, host=True, args=temp['product_code'])
                    temp['version'] = str(version)
                    productsList.append(temp)
        return dict(product=productsList)
    else:
        return dict(product=None)


def other_download_link():
    dataList = db(db.clsb30_link_download_app).select().as_list()
    return dict(apps=dataList)

#from applications.cbs
def check_free_classbook():

    result = check_free_for_classbook(request.args[0])

    return dict(result=result)


def convert_serialable():
    productCode = request.args[0]

    import subprocess

    #print settings.home_dir
    #print productCode
    subprocess.call(
        ['java', '-jar', '/home/libs/ToolConvertSerialable/ToolConvertSerialable.jar', settings.home_dir, productCode])


def gen_data():
    import os
    import subprocess

    path = settings.home_dir
    dirs = os.listdir(path)
    result = list()
    for file in dirs:
        if os.path.isdir(path + file):
            try:
                subprocess.call(
                    ['java', '-jar', '/home/libs/ToolConvertSerialable/ToolConvertSerialable.jar', settings.home_dir,
                     file])
            except Exception as e:
                result.append(str(file) + " Lỗi " + str(e))
    return dict(result=result)

def insert_3a():
    try:
        token = request.args[0]
        device_serial = request.args[1]

        user = db(db.clsb_user.user_token == token).select()
        if len(user) == 0:
            return dict(error="Hết phiên đăng nhập")
        user = user.first()
        #print(user['id'])
        check_serial = db(db.clsb30_3a_register.device_serial == device_serial).select()
        if len(check_serial) > 0:
            return dict(error="Thiết bị được đồng bộ rồi")

        fh = open(settings.home_dir + "3a_id.txt", "r")
        arr_lines = fh.readlines()
        for line in arr_lines:
            product_id = line.split("$")[0]
            product = db(db.clsb_product.id == product_id)(db.clsb_category.id == db.clsb_product.product_category).select().first()
            #print(product)
            if len(db(db.clsb30_product_history.product_id == product_id)(db.clsb30_product_history.user_id == user['id']).select()) <= 0:
                db.clsb30_product_history.insert(
                    product_title=product['clsb_product']['product_title'],
                    product_id=product['clsb_product']['id'],
                    user_id=user['id'],
                    category_id=product['clsb_category']['id'],
                    product_price=product['clsb_product']['product_price']
                )

        db.clsb30_3a_register.insert(
            device_serial=device_serial,
            user_id=user['id'],
            insert_time=request.now,
        )
        return dict(result="success")
    except Exception as err:
        return dict(error=err)
#for cart
def get_data_price(product_id):# product_id
    product_data = db(db.clsb30_product_extend.extend_id == db.clsb30_data_extend.id)\
        (db.clsb30_product_extend.product_id == product_id).select()
    result = dict()
    for data in product_data:
        result[data[db.clsb30_data_extend.name]] = data[db.clsb30_product_extend.price]
    return result

def check_product_exist(product_code):
    product = db(db.clsb_product.product_code == product_code)\
        (db.clsb_product.product_status == "Approved").select()
    if len(product) > 0:
        return True
    return False

def check_media():
    product_code = request.args[0]
    try:
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        import Image
        import fs

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        else:
            path = fs.path.pathjoin(product_code)
        product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
        if len(product_files) == 0:
            return  dict(check=False)
        else:
            check = check_media_in_zip(fs.path.pathjoin(settings.home_dir, path, product_files[0]), product_code)
            #print('check' + str(check))
            return dict(check=check)
    except Exception as ex:
        print('tiench' + str(ex))
        return dict(check=False, error=str(ex))
def check_has_media(product_code):#params: product_code
    try:
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        import Image
        import fs

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        else:
            path = fs.path.pathjoin(product_code)
        product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
        if len(product_files) == 0:
            return  dict(check=False)
        else:
            check = check_media_in_zip(fs.path.pathjoin(settings.home_dir, path, product_files[0]), product_code)
            #print('check' + str(check))
            return dict(check=check)
    except Exception as ex:
        #print('tiench' + str(ex))
        return dict(check=False, error=str(ex))

def check_buy_quiz(product_id, token): #product_id, token
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)
    product = db(db.clsb_product.id == product_id).select().first()
    quiz_code = 'Exer' + product['product_code']
    quiz = db(db.clsb_product.product_code == quiz_code).select();
    if len(quiz) == 0:
        return dict(result=False)
    quiz_id = quiz[0]['id']
    #print("quiz id: " + str(quiz_id))
    check_buy = db(db.clsb30_product_history.product_id == quiz_id)(
        db.clsb30_product_history.user_id == user.first()['id']).select()
    productData = db(db.clsb_product.id == quiz_id).select().first()

    if not check_free_for_classbook(productData['product_category']):
        downloaded = db(db.clsb_download_archieve.product_id == productData['id'])(
            db.clsb_download_archieve.status.like("Completed"))(
            db.clsb_download_archieve.user_id == user.first()['id']).select()
        if len(downloaded) > 0 or len(check_buy) > 0:
            return dict(result=True)
    elif len(check_buy) > 0:
        return dict(result=True)

    return dict(result=False)


def check_buy_media(product_id, token): #product_id, token
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)

    check_buy = db(db.clsb30_media_history.product_id == int(product_id))(
        db.clsb30_media_history.user_id == user.first()['id']).select()

    # productData = db(db.clsb_product.id == int(request.args[0])).select().first()
    #print("check media: " + str(check_buy))
    if len(check_buy) > 0:
        return dict(result=True)

    return dict(result=False)

def check_buy_product(product_id, token):
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)
    #print('check_buy id:' + request.args[0])
    check_buy = db(db.clsb30_product_history.product_id == int(product_id))(
        db.clsb30_product_history.user_id == user.first()['id']).select()
    productData = db(db.clsb_product.id == int(product_id)).select().first()

    if not check_free_for_classbook(productData['product_category']):
        downloaded = db(db.clsb_download_archieve.product_id == productData['id'])(
            db.clsb_download_archieve.status.like("Completed"))(
            db.clsb_download_archieve.user_id == user.first()['id']).select()
        if len(downloaded) > 0 or len(check_buy) > 0:
            return dict(result=True)
    elif len(check_buy) > 0:
        return dict(result=True)

    return dict(result=False)



