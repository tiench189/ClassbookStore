__author__ = 'Tien'

import sys
import json
import requests
import urllib


def clear_solr():
    try:
        headers = {'Content-Type': 'application/json'}
        url_detele = "http://localhost:8189/solr/cblib/update?stream.body=<delete><query>*:*</query></delete>&commit=true"
        req1 = requests.post(url_detele,  headers=headers)
        print(req1)
        return dict(res=str(req1))
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def import_solr():
    clear_solr()
    headers = {'Content-Type': 'application/json'}
    url_update = "http://localhost:8189/solr/cblib/update/json/docs"
    url_commit = "http://localhost:8189/solr/cblib/update?stream.body=<commit/>"
    try:
        print("import")
        select_product = db(db.clsb_product.product_status == "Approved")\
                (db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product.id == db.clsblib_category_product.product_id)\
                (db.clsblib_category_product.category_code == db.clsblib_category.category_code)\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id)\
                (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                (db.clsb_product.product_category == db.clsb_category.id).select()
        all_data = []
        for product in select_product:
            data = {}
            print(product['clsb_product']['product_code'])
            data['id'] = str(product['clsb_product']['id'])
            data['product_title'] = product['clsb_product']['product_title']
            data['product_description'] = product['clsb_product']['product_description']
            data['product_category'] = product['clsb_category']['category_parent']
            data['product_class'] = product['clsb_subject_class']['class_id']
            data['product_subject'] = product['clsb_subject_class']['subject_id']
            data['product_price'] = product['clsb_product']['product_price']
            data['product_code'] = product['clsb_product']['product_code']
            co_author = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id)\
                (db.clsb_dic_metadata.metadata_name == "co_author").select()
            product_author = ""
            if len(co_author) > 0:
                product_author = str(co_author.first()['clsb_product_metadata']['metadata_value']).replace("#", " ")
            data['product_co_author'] = product_author
            data['product_creator'] = product['clsb_dic_creator']['creator_name']

            cover_price = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id)\
                (db.clsb_dic_metadata.metadata_name == "cover_price").select()
            data['cover_price'] = 0
            if len(cover_price) > 0:
                data['cover_price'] = cover_price.first()['clsb_product_metadata']['metadata_value']
            all_data.append(data)
        req = requests.post(url_update, data=json.dumps(all_data),  headers=headers)
        req1 = requests.post(url_commit,  headers=headers)
        return dict(res=str(req))
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def test_select():
    headers = {'Content-Type': 'application/json'}
    url_update = "http://localhost:8189/solr/cblib/update/json/docs"
    url_commit = "http://localhost:8189/solr/cblib/update?stream.body=<commit/>"
    try:
        print("import")
        select_product = db(db.clsb_product.product_status == "Approved")\
                (~db.clsb_product.product_code.like("Exer%"))\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id)\
                (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                (db.clsb_product.product_category == db.clsb_category.id).select()
        for product in select_product:
            data = {}
            print(product['clsb_product']['product_code'])
            data['id'] = str(product['clsb_product']['id'])
            data['product_title'] = product['clsb_product']['product_title']
            data['product_description'] = product['clsb_product']['product_description']
            data['product_category'] = product['clsb_category']['category_parent']
            data['product_class'] = product['clsb_subject_class']['class_id']
            data['product_subject'] = product['clsb_subject_class']['subject_id']
            data['product_price'] = product['clsb_product']['product_price']
            data['product_code'] = product['clsb_product']['product_code']
            co_author = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id)\
                (db.clsb_dic_metadata.metadata_name == "co_author").select()
            product_author = ""
            if len(co_author) > 0:
                product_author = str(co_author.first()['clsb_product_metadata']['metadata_value']).replace("#", " ")
            data['product_co_author'] = product_author
            data['product_creator'] = product['clsb_dic_creator']['creator_name']

            cover_price = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id)\
                (db.clsb_dic_metadata.metadata_name == "cover_price").select()
            data['cover_price'] = 0
            if len(cover_price) > 0:
                data['cover_price'] = cover_price.first()['clsb_product_metadata']['metadata_value']
            req = requests.post(url_update, data=json.dumps(data),  headers=headers)
            #print(data)
            print(req)
        req1 = requests.post(url_commit,  headers=headers)
        return dict(res=str(req1))
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def update_solr():
    headers = {'Content-Type': 'application/json'}
    url_update = "http://localhost:8189/solr/cblib/update/json/docs"
    url_commit = "http://localhost:8189/solr/cblib/update?stream.body=<commit/>"
    try:
        product_id = list()
        select_id = db(db.clsb30_update_product_log.table_name == "clsb_product")\
            .select(db.clsb30_update_product_log.record_id, distinct=True)
        for mid in select_id:
            product_id.append(str(mid[db.clsb30_update_product_log.record_id]))
        select_product = db(db.clsb_product.id.belongs(product_id)).select()
        for product in select_product:
            data = {}
            data['id'] = str(product['id'])
            data['product_title'] = product['product_title']
            data['product_description'] = product['product_description']
            print(product['product_description'])
            co_author = db(db.clsb_product_metadata.product_id == product['id'])\
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id)\
                (db.clsb_dic_metadata.metadata_name == "co_author").select()
            if len(co_author) > 0:
                product_author = str(co_author.first()['clsb_product_metadata']['metadata_value']).replace("#", " ")
                print(product_author)
                data['product_creator'] = product_author
            #print(data)
            req = requests.post(url_update, data=json.dumps(data),  headers=headers)
            print(req.status_code, req.reason)
            if str(req.reason) == "OK":
                db(db.clsb30_update_product_log.table_name == "clsb_product")\
                        (db.clsb30_update_product_log.record_id == product['id']).delete()
        select_from_metadata = db(db.clsb30_update_product_log.table_name == "clsb_product_metadata")\
                (db.clsb30_update_product_log.record_id == db.clsb_product_metadata.id)\
                (~db.clsb_product_metadata.product_id.belongs(product_id))\
                (db.clsb_product_metadata.product_id == db.clsb_product.id)\
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id)\
                (db.clsb_dic_metadata.metadata_name == "co_author").select()
        for product in select_from_metadata:
            data = {}
            data['id'] = str(product['clsb_product']['id'])
            data['product_title'] = product['clsb_product']['product_title']
            data['product_description'] = product['clsb_product']['product_description']
            data['product_author'] = product['clsb_product_metadata']['metadata_value']
            print(data)
            req = requests.post(url_update, data=json.dumps(urllib.urlencode(data)),  headers=headers)
            print(req.status_code, req.reason)
            if str(req.reason) == "OK":
                db(db.clsb30_update_product_log.id == product['clsb30_update_product_log']['id']).delete()
        req1 = requests.post(url_commit,  headers=headers)
        print(req1.status_code, req1.reason)
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
