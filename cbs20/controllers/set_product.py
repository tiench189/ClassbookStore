__author__ = 'Tien'


import sys


def get():
    try:
        select_set = db(db.clsb30_set_of_product.set_status.like("show")).select()
        sets = list()
        for set in select_set:
            temp = dict()
            temp['id'] = set['id']
            temp['set_name'] = set['set_name']
            temp['set_code'] = set['set_code']
            sets.append(temp)
        return dict(sets=sets)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_product_in_set(): #vars: set_id
    try:
        products = list()
        set_id = request.vars.set_id
        select_product = db(db.clsb30_product_in_set.set_id == set_id)\
                (db.clsb30_product_in_set.product_id == db.clsb_product.id)\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.id,
                                                                                   db.clsb30_product_in_set.id,
                                                                                    db.clsb_product.product_code,
                                                                                    db.clsb_product.product_title,
                                                                                    db.clsb_product.product_price,
                                                                                    db.clsb_dic_creator.creator_name,
                                                                                    orderby=db.clsb30_product_in_set.id)
        for product in select_product:
            products.append(convert2product(product))
        return dict(products=products)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def info(): #vars: set_id
    try:
        products = list()
        set_id = request.vars.set_id
        select_product = db(db.clsb30_product_in_set.set_id == set_id)\
                (db.clsb30_product_in_set.product_id == db.clsb_product.id)\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.id,
                                                                                   db.clsb30_product_in_set.id,
                                                                                    db.clsb_product.product_code,
                                                                                    db.clsb_product.product_title,
                                                                                    db.clsb_product.product_price,
                                                                                    db.clsb_dic_creator.creator_name,
                                                                                    orderby=db.clsb30_product_in_set.id)
        for product in select_product:
            products.append(convert2product(product))

        set = db(db.clsb30_set_of_product.id == set_id).select().first()
        return dict(set_id=set['id'], set_title=set['set_name'], set_code=set['set_code'], products=products)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def convert2product(product):
    temp = dict()
    temp['id'] = product[db.clsb_product.id]
    temp['product_code'] = product[db.clsb_product.product_code]
    temp['product_title'] = product[db.clsb_product.product_title]
    temp['product_price'] = product[db.clsb_product.product_price]
    temp['creator_name'] = product[db.clsb_dic_creator.creator_name]
    cover_price = db(db.clsb_product_metadata.product_id == temp['id']) \
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
    return temp