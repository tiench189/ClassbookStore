# -*- coding: utf-8 -*-
import myredis
import sys
import json


# def get_product_history():
#     """
#     service list all book/app that user bought on classbook store
#     params: app.version/serial/token/page/item_per_page
#     """
#     try:
#         if len(request.args) < 3:
#             return dict(error="Lỗi request")
#         app_ver = request.args[0]
#         serial = request.args[1]
#         token = request.args[2]
#         user = db(db.clsb_user.user_token.like(token)).select()
#         if len(user) <= 0:
#             return dict(error="Sai token")
#         result = checkTimeOut(user.first()['username'], token)
#         if result != "OK":
#             return dict(error=result)
#         page = 0
#         items_per_page = settings.items_per_page
#         if len(request.args) > 3:
#             page = int(request.args[3])
#         if len(request.args) > 4:
#             items_per_page = int(request.args[4])
#         limitby = (page * items_per_page, (page + 1) * items_per_page)
#         list_free = list()
#         cat_free = db(db.clsb30_category_classbook_device).select()
#         for cat in cat_free:
#             list_free.append(cat['product_category'])
#
#         product_query = db(db.clsb_product.product_status.like('Approved'))\
#                                 (db.clsb_product.product_creator == db.clsb_dic_creator.id)\
#                                 (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
#                                 (db.clsb_category.category_type == db.clsb_product_type.id) \
#                                 (db.clsb_product.product_category == db.clsb_category.id) \
#                                 (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id)\
#                                 (db.clsb_category.id == db.clsb_product.product_category)\
#                                 (db.clsb30_product_history.user_id == user.first()['id'])\
#                                 (db.clsb_download_archieve.user_id == user.first()['id'])\
#                                 ((db.clsb_product.id == db.clsb30_product_history.product_id) | ((db.clsb_product.id == db.clsb_download_archieve.product_id) & ((~db.clsb_category.id.belongs(list_free)) & (~db.clsb_category.category_parent.belongs(list_free)))))\
#
#         # return dict(ms=product_query)
#
#         total_items = product_query.count(db.clsb_product.id)
#         total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page
#
#         products = list()
#
#         db_product = product_query.select(db.clsb_product.id,
#                                           db.clsb_category.ALL,
#                                           db.clsb_dic_creator.creator_name,
#                                           db.clsb_dic_publisher.publisher_name,
#                                           db.clsb_product.product_title,
#                                           db.clsb_product_type.type_name,
#                                           db.clsb_product.product_code,
#                                           db.clsb_product.product_price,
#                                           db.clsb_device_shelf.device_shelf_code,
#                                           db.clsb_device_shelf.device_shelf_type,
#                                           db.clsb_device_shelf.device_shelf_name,
#                                           db.clsb30_product_history.created_on,
#                                           orderby=~db.clsb_product.total_download,
#                                           limitby=limitby,
#                                           groupby=db.clsb_product.id).as_list()
#
#
#
#         if db_product:
#             for row in db_product:
#                 temp = dict()
#                 temp['id'] = row['clsb_product']['id']
#                 temp['category_id'] = row['clsb_category']['id']
#                 temp['category_name'] = row['clsb_category']['category_name']
#                 temp['category_code'] = row['clsb_category']['category_code']
#                 temp['category_type'] = row['clsb_product_type']['type_name']
#                 temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
#                 temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
#                 temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
#
#                 temp['creator_name'] = row['clsb_dic_creator']['creator_name']
#                 temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
#                 temp['product_title'] = row['clsb_product']['product_title']
#                 temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
#                                             args=row['clsb_product'][
#                                                 'product_code']) #row['clsb_product']['product_cover']
#                 temp['product_code'] = row['clsb_product']['product_code']
#                 temp['product_price'] = row['clsb_product']['product_price']
#                 temp['buy_time'] = row['clsb30_product_history']['created_on']
#                 cover_price = db(db.clsb_product_metadata.product_id == row['clsb_product']['id']) \
#                         (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
#                         (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
#                     db.clsb_product_metadata.metadata_value).as_list()
#                 if cover_price:
#                     try:
#                         temp['cover_price'] = int(cover_price[0]['metadata_value'])
#                     except Exception as e:
#                         pass
#                 else:
#                     temp['cover_price'] = 0
#
#                 products.append(temp)
#
#                 products.append(temp)
#
#         return dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
#                     products=products)
#     except Exception as ex:
#         print str(ex)
#         return dict(error=ex.message)

"""
Note for trick
Su dung function get_product_history tren, mat nhieu tg tinh toan hon so voi function dang dung ben duoi
//Do độ trễ của Framework khi tính toán ra query và xử lý dữ liệu
"""
# from scripts.extract_pgsql_models import query

# SERVER_VER = CB_SERVER_VER

def get_product_history():
    """
    service list all book/app that user bought on classbook store
    params: app.version/serial/token/page/item_per_page
    """
    metadata_version_name = 'version'
    metadata_product_size_name = 'product_size'
    try:
        if len(request.args) < 3:
            return dict(error="Lỗi request")
        app_ver = request.args[0]
        serial = request.args[1]
        token = request.args[2]
        #type = request.args[3]
        version_app = ""
        if 'android' in app_ver.lower():
            version_app = "ANDROID_APP"
        if 'ios' in app_ver.lower():
            version_app = "IOS_APP"
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")
        # if check_version_mp(app_ver):
        #     return get_product_mp()

        result = checkTimeOut(user.first()['username'], token)
        if result != "OK":
            return dict(error=result)
        page = 0
        except_type = ['Exercise', 'Application']
        items_per_page = settings.items_per_page
        if len(request.args) > 3:
            page = int(request.args[3])
        if len(request.args) > 4:
            items_per_page = int(request.args[4])
        if len(request.args) > 5:
            except_type = ['Exercise', 'Application']

        else:
            except_type = ['Exercise']

        limitby = (page * items_per_page, page * items_per_page + items_per_page)

        # get metadata named: version
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()

        metadata_product_size = db(db.clsb_dic_metadata.metadata_name == metadata_product_size_name).select(
            db.clsb_dic_metadata.id).first()
        if metadata_product_size is None:
            metadata_product_size = 0

        list_free = list()
        cat_free = db(db.clsb30_category_classbook_device).select()
        for cat in cat_free:
            list_free.append(cat['product_category'])
        total_items = db(db.clsb_product.product_status.like('Approved'))(
            db.clsb30_product_history.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb30_product_history.product_id)(
            db.clsb_product.product_creator == db.clsb_dic_creator.id)(
            db.clsb_product.show_on.like('%' + version_app + '%')) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (~db.clsb_product_type.type_name.belongs(except_type))\
                (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                           groupby=db.clsb_product.id)
        list_buy = list()
        for product in total_items:
            list_buy.append(product['id'])
        total_items = len(total_items)
        total_items_a = db((db.clsb_product.product_status.like('Approved')) & (~db.clsb_product.id.belongs(list_buy)))(
            db.clsb_product.show_on.like('%' + version_app + '%'))(
            (db.clsb_download_archieve.user_id == user.first()['id']) & (
                db.clsb_download_archieve.status.like("Completed")))(
            db.clsb_product.id == db.clsb_download_archieve.product_id)(
            db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (~db.clsb_product_type.type_name.belongs(except_type))\
                (~db.clsb_category.id.belongs(list_free) & ~db.clsb_category.category_parent.belongs(list_free)) \
                (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                       groupby=db.clsb_product.id)
        total_items_a = len(total_items_a)
        total_items_tmp = total_items

        total_items += total_items_a
        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page
        products = list()
        db_product = db(db.clsb_product.product_status.like('Approved'))(
            db.clsb_product.show_on.like('%' + version_app + '%'))(
            db.clsb30_product_history.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb30_product_history.product_id)(
            db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (~db.clsb_product_type.type_name.belongs(except_type))\
                (db.clsb_product.product_category == db.clsb_category.id) \
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                      db.clsb_category.ALL,
                                                                                      db.clsb_dic_creator.creator_name,
                                                                                      db.clsb_dic_publisher.publisher_name,
                                                                                      db.clsb_product.id,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                      db.clsb_product.product_description,
                                                                                      db.clsb_device_shelf.device_shelf_code,
                                                                                      db.clsb_device_shelf.device_shelf_type,
                                                                                      db.clsb_device_shelf.device_shelf_name,
                                                                                      db.clsb30_product_history.created_on,
                                                                                      orderby=~db.clsb30_product_history.created_on,
                                                                                      limitby=limitby,
                                                                                      groupby=db.clsb_product.id).as_list()
        if db_product:

            for row in db_product:

                temp = dict()
                # select product version metadata
                metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_version_value is None:
                    metadata_version_value = dict()
                    metadata_version_value['metadata_value'] = 0
                # print(row)
                metadata_product_size_value = db((db.clsb_product_metadata.metadata_id == metadata_product_size['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_product_size_value is None:
                    metadata_product_size_value = dict()
                    metadata_product_size_value['metadata_value'] = 0

                metadata_product_size_value['metadata_value']  = int(metadata_product_size_value['metadata_value']) * 1048576

                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsb_category']['id']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
                temp['product_description'] = row['clsb_product']['product_description']
                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['buy_time'] = row['clsb30_product_history']['created_on']
                temp['version'] = metadata_version_value['metadata_value']
                temp['product_size'] =  metadata_product_size_value['metadata_value']

                price_media = db(db.clsb30_product_extend.product_id == temp['id'])\
                    (db.clsb30_product_extend.extend_id == 1).select()
                if len(price_media) == 0:
                    temp['media_price'] = settings.fake_fund_media
                else:
                    temp['media_price'] = price_media.first()['price']
                price_quiz = db(db.clsb30_product_extend.product_id == temp['id'])\
                    (db.clsb30_product_extend.extend_id == 2).select()
                if len(price_quiz) == 0:
                    temp['quiz_price'] = settings.fake_fund_quiz
                else:
                    temp['quiz_price'] = price_quiz.first()['price']
                cover_price = db(db.clsb_product_metadata.product_id == row['clsb_product']['id']) \
                        (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                        (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                    db.clsb_product_metadata.metadata_value).as_list()
                if cover_price:
                    try:
                        temp['cover_price'] = int(cover_price[0]['metadata_value'])
                    except Exception as e:
                        pass
                else:
                    temp['cover_price'] = 0
                try:
                    #check media
                    temp['has_media'] = check_media(temp['product_code'])['check']
                    check_buy = db(db.clsb30_media_history.product_id == temp['id'])(
                            db.clsb30_media_history.user_id == user.first()['id']).select()
                    if len(check_buy) > 0 or temp['media_price'] == 0:
                        temp['buy_media'] = True
                    else:
                        temp['buy_media'] = False
                    pass
                    #check_quiz
                    hasquiz = db(db.clsb_product.product_code == 'Exer' + temp['product_code'])\
                            (db.clsb_product.product_status == 'Approved').select()
                    if len(hasquiz) > 0:
                        temp['has_quiz'] = True
                        quiz_id = hasquiz.first()['id']
                        check_quiz = db(db.clsb30_product_history.product_id == quiz_id)\
                            (db.clsb30_product_history.user_id == user.first()['id']).select()
                        if len(check_quiz) > 0 or temp['quiz_price'] == 0:
                            temp['buy_quiz'] = True
                        else:
                            temp['buy_quiz'] = False
                        pass
                    else:
                        temp['has_quiz'] = False
                        temp['buy_quiz'] = False
                    pass

                except Exception as err:
                    print(err)
                    temp['buy_media'] = False
                    temp['has_quiz'] = False
                    temp['buy_quiz'] = False
                    temp['has_media'] = False
                temp['log'] = "history"
                if temp['category_type'] != 'Exercise':
                    if 'ios' not in request.args[0].lower() or 'app' not in temp['category_type'].lower():
                        products.append(temp)

        if len(products) < items_per_page:
            if len(products) > 0:
                limitby = (0, items_per_page - len(products))
            else:
                start = (page * items_per_page) - total_items_tmp
                end = start + items_per_page
                if start < 0L:
                    start = 0
                if end < 0L:
                    end = 0
                limitby = (start, end)

            db_product_a = db(
                (db.clsb_product.product_status.like('Approved')) & (~db.clsb_product.id.belongs(list_buy)))(
            db.clsb_product.show_on.like('%' + version_app + '%'))(
                (db.clsb_download_archieve.user_id == user.first()['id']) & (
                    db.clsb_download_archieve.status.like("Completed")))(
                db.clsb_product.id == db.clsb_download_archieve.product_id)(
                db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (~db.clsb_product_type.type_name.belongs(except_type))\
                    (db.clsb_product.product_category == db.clsb_category.id) \
                    (~db.clsb_category.id.belongs(list_free) & ~db.clsb_category.category_parent.belongs(list_free)) \
                    (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                          db.clsb_category.ALL,
                                                                                          db.clsb_download_archieve.ALL,
                                                                                          db.clsb_product_type.type_name,
                                                                                          db.clsb_dic_creator.creator_name,
                                                                                          db.clsb_dic_publisher.publisher_name,
                                                                                          db.clsb_product.id,
                                                                                          db.clsb_product.product_title,
                                                                                          db.clsb_product.product_description,
                                                                                          db.clsb_product.product_code,
                                                                                          db.clsb_product.product_price,
                                                                                          db.clsb_device_shelf.device_shelf_code,
                                                                                          db.clsb_device_shelf.device_shelf_type,
                                                                                          db.clsb_device_shelf.device_shelf_name,
                                                                                          db.clsb_download_archieve.created_on,
                                                                                          orderby=~db.clsb_download_archieve.created_on,
                                                                                          limitby=limitby,
                                                                                          groupby=db.clsb_product.id).as_list()
            #print db._lastsql
            if db_product_a:
                for row in db_product_a:
                    temp = dict()

                    # select product version metadata
                    metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                        db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                        db.clsb_product_metadata.metadata_value).first()

                    if metadata_version_value is None:
                        metadata_version_value = dict()
                        metadata_version_value['metadata_value'] = 0

                    metadata_product_size_value = db((db.clsb_product_metadata.metadata_id == metadata_product_size['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                    if metadata_product_size_value is None:
                        metadata_product_size_value = dict()
                        metadata_product_size_value['metadata_value'] = 0

                    metadata_product_size_value['metadata_value'] *= 1048576

                    temp['id'] = row['clsb_product']['id']
                    temp['category_id'] = row['clsb_category']['id']
                    temp['category_name'] = row['clsb_category']['category_name']
                    temp['category_code'] = row['clsb_category']['category_code']
                    temp['category_type'] = row['clsb_product_type']['type_name']
                    temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                    temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                    temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
                    temp['product_description'] = row['clsb_product']['product_description']
                    temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                    temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                    temp['product_title'] = row['clsb_product']['product_title']
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                                args=row['clsb_product'][
                                                    'product_code']) #row['clsb_product']['product_cover']
                    temp['product_code'] = row['clsb_product']['product_code']
                    temp['product_price'] = row['clsb_product']['product_price']
                    temp['buy_time'] = row['clsb_download_archieve']['created_on']
                    temp['version'] = metadata_version_value['metadata_value']
                    temp['product_size'] =  metadata_product_size_value['metadata_value']

                    price_media = db(db.clsb30_product_extend.product_id == temp['id'])\
                        (db.clsb30_product_extend.extend_id == 1).select()
                    if len(price_media) == 0:
                        temp['media_price'] = settings.fake_fund_media
                    else:
                        temp['media_price'] = price_media.first()['price']
                    price_quiz = db(db.clsb30_product_extend.product_id == temp['id'])\
                        (db.clsb30_product_extend.extend_id == 2).select()
                    if len(price_quiz) == 0:
                        temp['quiz_price'] = settings.fake_fund_quiz
                    else:
                        temp['quiz_price'] = price_quiz.first()['price']
                    cover_price = db(db.clsb_product_metadata.product_id == row['clsb_product']['id']) \
                            (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                            (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                        db.clsb_product_metadata.metadata_value).as_list()
                    if cover_price:
                        try:
                            temp['cover_price'] = int(cover_price[0]['metadata_value'])
                        except Exception as e:
                            pass
                    else:
                        temp['cover_price'] = 0
                    try:
                        temp['has_media'] = check_media(temp['product_code'])['check']
                        check_buy = db(db.clsb30_media_history.product_id == temp['id'])(
                            db.clsb30_media_history.user_id == user.first()['id']).select()
                        if len(check_buy) > 0 or temp['media_price'] == 0:
                            temp['buy_media'] = True
                        else:
                            temp['buy_media'] = False
                        pass
                        #check_quiz
                        hasquiz = db(db.clsb_product.product_code == 'Exer' + temp['product_code'])\
                            (db.clsb_product.product_status == 'Approved').select()
                        if len(hasquiz) > 0:
                            temp['has_quiz'] = True
                            quiz_id = hasquiz.first()['id']
                            check_quiz = db(db.clsb30_product_history.product_id == quiz_id)\
                                (db.clsb30_product_history.user_id == user.first()['id']).select()
                            if len(check_quiz) > 0 or temp['quiz_price'] == 0:
                                temp['buy_quiz'] = True
                            else:
                                temp['buy_quiz'] = False
                            pass
                        else:
                            temp['has_quiz'] = False
                            temp['buy_quiz'] = False
                        pass

                    except Exception as  err:
                        print(err)
                        temp['buy_media'] = False
                        temp['has_quiz'] = False
                        temp['buy_quiz'] = False
                        temp['has_media'] = False
                    # print("Buy media:" + str(temp['buy_media']))
                    temp['log'] = 'download'
                    if temp['category_type'] != 'Exercise':
                        if 'ios' not in request.args[0].lower() or 'app' not in temp['category_type'].lower():
                            products.append(temp)
        #total_items = len(products)

        return dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
                    products=products, version_mp=check_version_mp(app_ver), version_app=app_ver,
                    device_support=settings.device_support, item_in_page=len(products), total_buy=total_items_tmp,
                    total_down=total_items_a)
    except Exception as ex:
        print str(ex)
        return dict(error=ex.message)

def search_in_product_history():
    """
    service list all book/app that user bought on classbook store
    params: ver=app.version&key=key_word&token=token&page=page&item=item_per_page
    """

    metadata_version_name = 'version'
    metadata_product_size_name = 'product_size'
    try:
        if len(request.vars) < 3:
            return dict(error="Lỗi request")
        app_ver = request.vars.ver
        key_word = request.vars.key
        token = request.vars.token
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")
        page = 0

        items_per_page = settings.items_per_page
        if len(request.vars) > 3:
            page = int(request.vars.page)
        if len(request.vars) > 4:
            items_per_page = int(request.vars.item)

        limitby = (page * items_per_page, (page + 1) * items_per_page)

        # get metadata named: version
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()

        metadata_product_size = db(db.clsb_dic_metadata.metadata_name == metadata_product_size_name).select(
            db.clsb_dic_metadata.id).first()

        total_items = db(db.clsb_product.product_status.like('Approved'))(
            db.clsb30_product_history.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb30_product_history.product_id)
        total_items = total_items(db.clsb_product.product_title.like('%' + key_word + '%'))
        total_items = total_items(db.clsb_product.product_publisher == db.clsb_dic_publisher.id)\
                (db.clsb_category.category_type == db.clsb_product_type.id)\
                (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                 groupby=db.clsb_product.id)

        total_items = len(total_items)
        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page
        products = list()

        db_product = db(db.clsb_product.product_status.like('Approved'))(
            db.clsb30_product_history.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb30_product_history.product_id)
        db_product = db_product(db.clsb_product.product_title.like('%' + key_word + '%'))

        db_product = db_product(db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id) \
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                      db.clsb_category.ALL,
                                                                                      db.clsb_dic_creator.creator_name,
                                                                                      db.clsb_dic_publisher.publisher_name,
                                                                                      db.clsb_product.id,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product.product_description,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                      db.clsb_device_shelf.device_shelf_code,
                                                                                      db.clsb_device_shelf.device_shelf_type,
                                                                                      db.clsb_device_shelf.device_shelf_name,
                                                                                      db.clsb30_product_history.created_on,
                                                                                      orderby=~db.clsb30_product_history.created_on,
                                                                                      limitby=limitby,
                                                                                      groupby=db.clsb_product.id).as_list()

        if db_product:
            for row in db_product:
                # select product version metadata
                metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_version_value is None:
                    metadata_version_value = dict()
                    metadata_version_value['metadata_value'] = 0

                # select product size metadata
                metadata_product_size_value = db((db.clsb_product_metadata.metadata_id == metadata_product_size['id']) & (
                db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                db.clsb_product_metadata.metadata_value).first()

                if metadata_product_size_value is None:
                    metadata_product_size_value = dict()
                    metadata_product_size_value['metadata_value'] = 0

                metadata_product_size_value['metadata_value'] *= 1048576

                temp = dict()
                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsb_category']['id']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
                temp['product_description'] =row['clsb_product']['product_description']
                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['buy_time'] = row['clsb30_product_history']['created_on']
                temp['version'] = metadata_version_value['metadata_value']
                temp['product_size'] = metadata_product_size_value['metadata_value']
                price_media = db(db.clsb30_product_extend.product_id == temp['id'])\
                    (db.clsb30_product_extend.extend_id == 1).select()
                if len(price_media) == 0:
                    temp['media_price'] = settings.fake_fund_media
                else:
                    temp['media_price'] = price_media.first()['price']
                price_quiz = db(db.clsb30_product_extend.product_id == temp['id'])\
                    (db.clsb30_product_extend.extend_id == 2).select()
                if len(price_quiz) == 0:
                    temp['quiz_price'] = settings.fake_fund_quiz
                else:
                    temp['quiz_price'] = price_quiz.first()['price']
                cover_price = db(db.clsb_product_metadata.product_id == row['clsb_product']['id']) \
                        (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                        (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                    db.clsb_product_metadata.metadata_value).as_list()
                if cover_price:
                    try:
                        temp['cover_price'] = int(cover_price[0]['metadata_value'])
                    except Exception as e:
                        pass
                else:
                    temp['cover_price'] = 0

                try:
                    #check media
                    temp['has_media'] = check_media(temp['product_code'])['check']
                    check_buy = db(db.clsb30_media_history.product_id == temp['id'])(
                            db.clsb30_media_history.user_id == user.first()['id']).select()
                    if len(check_buy) > 0 or int(temp['media_price']) == 0:
                        temp['buy_media'] = True
                    else:
                        temp['buy_media'] = False
                    pass
                    #check_quiz
                    hasquiz = db(db.clsb_product.product_code == 'Exer' + temp['product_code'])\
                            (db.clsb_product.product_status == 'Approved').select()
                    if len(hasquiz) > 0:
                        temp['has_quiz'] = True
                        quiz_id = hasquiz.first()['id']
                        check_quiz = db(db.clsb30_product_history.product_id == quiz_id)\
                            (db.clsb30_product_history.user_id == user.first()['id']).select()
                        if len(check_quiz) > 0 or int(temp['quiz_price']) == 0:
                            temp['buy_quiz'] = True
                        else:
                            temp['buy_quiz'] = False
                        pass
                    else:
                        temp['has_quiz'] = False
                        temp['buy_quiz'] = False
                    pass

                except Exception as err:
                    print(err)
                    temp['buy_media'] = False
                    temp['has_quiz'] = False
                    temp['buy_quiz'] = False
                    temp['has_media'] = False

                if temp['category_type'] != 'Exercise':
                    if 'ios' not in request.vars.ver.lower() or 'app' not in temp['category_type'].lower():
                        products.append(temp)
        return dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
                    products=products, device_support=settings.device_support)
    except Exception as ex:
        print str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno)
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def buy_product():
    """
    service checkout when user buy book/app on classbook store
    params: product_code/app.version/token/classbook_device
    Neu mua cho thiet bi classbook can truyen them params 'classbook_device'
    """
    try:
        product = db(db.clsb_product.product_code.like(request.args[0]))(
            db.clsb_category.id == db.clsb_product.product_category).select().first()
    except:
        return dict(error="Mã sách không đúng")
    token = request.args[2]
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)
    classbook_device = False
    if len(request.args) > 3:
        classbook_device = True
    result = pay_to_log(user.first(), product, classbook_device)
    if result is True:
        return dict(result=result)
    else:
        return dict(error=result['error'])

def buy_product_divide():#[product_code, version, token, isMedia, pay]
    """
    service checkout when user buy book/app on classbook store
    params: product_code/app.version/token/classbook_device
    Neu mua cho thiet bi classbook can truyen them params 'classbook_device'
    """
    try:
        product = db(db.clsb_product.product_code.like(request.args[0]))(
            db.clsb_category.id == db.clsb_product.product_category).select().first()
    except:
        return dict(error="Mã sách không đúng")
    token = request.args[2]
    isMedia = request.args[3]
    if isMedia is True or isMedia.lower() == 'true':
        media_price_info = db(db.clsb30_product_extend.product_id == product['clsb_product']['id'])\
                    (db.clsb30_product_extend.extend_id == 1).select()
        if len(media_price_info) > 0:
            pay = int(media_price_info.first()['price'])
        else:
            pay = settings.fake_fund_media
    elif 'Exer' in request.args[0]:
        pay = settings.fake_fund_quiz
    else:
        pay = int(product['clsb_product']['product_price'])
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)
    classbook_device = False
    if len(request.args) > 3:
        classbook_device = True
    result = pay_to_log_divide(user.first(), product, classbook_device, isMedia, pay)
    if 'error' not in result:
        return dict(result=result)
    else:
        return dict(error=result['error'])


def free_for_classbook(): #category_id
    category_id = int(request.args[0])
    return dict(result=check_free_for_classbook(category_id))
def check_buy_quiz(): #product_id, token
    token = request.args[1]
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)
    product = db(db.clsb_product.id == request.args[0]).select().first()
    quiz_code = 'Exer' + product['product_code']
    quiz = db(db.clsb_product.product_code == quiz_code).select();
    if len(quiz) == 0:
        return False;
    quiz_id = quiz[0]['id']
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

def check_buy_product(): #product_id, token
    try:
        token = request.args[1]
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")
        result = checkTimeOut(user.first()['username'], token)
        if result != "OK":
            return dict(error=result)
        check_buy = db(db.clsb30_product_history.product_id == int(request.args[0]))(
            db.clsb30_product_history.user_id == user.first()['id']).select()
        productData = db(db.clsb_product.id == int(request.args[0])).select().first()
        price = db(db.clsb_product.id == request.args(0)).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']
        if not check_free_for_classbook(productData['product_category']):
            downloaded = db(db.clsb_download_archieve.product_id == productData['id'])(
                db.clsb_download_archieve.status.like("Completed"))(
                db.clsb_download_archieve.user_id == user.first()['id'])\
                    (db.clsb_download_archieve.price >= price).select()
            if len(downloaded) > 0 or len(check_buy) > 0:
                return dict(result=True)
        elif len(check_buy) > 0:
            return dict(result=True)
    except Exception as err:
        return dict(error=str(err))

    return dict(result=False)

def check_token():
    token = request.args[0]
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)
    return dict(result='login')

def check_buy_media(): #product_id, token
    token = request.args[1]
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)

    check_buy = db(db.clsb30_media_history.product_id == int(request.args[0]))(
        db.clsb30_media_history.user_id == user.first()['id']).select()

    # productData = db(db.clsb_product.id == int(request.args[0])).select().first()
    if len(check_buy) > 0:
        return dict(result=True)

    return dict(result=False)

def check_product_free_for_classbook():
    if len(request.args) < 1 or request.vars:
        return dict(error="Lỗi")

    product_code = request.args[0]

    product_info = db(db.clsb_product.product_code == product_code).select(db.clsb_product.product_category).first()

    #check category code in table clsb30_category_classbook_device
    #category_classbook = db(db.clsb30_category_classbook_device.product_category == product_info['product_category'])\
    #    .select(db.clsb30_category_classbook_device.product_category).as_list()
    parent_id = db(db.clsb_category.id == product_info['product_category']).select().first()['category_parent']
    list = db((db.clsb30_category_classbook_device.product_category == product_info['product_category']) | (db.clsb30_category_classbook_device.product_category == parent_id)).select()

    if len(list) > 0:
        return dict(result = True)

    return dict(result = False)

def get_data_price():# product_id
    product_id = request.args[0]
    product_data = db(db.clsb30_product_extend.extend_id == db.clsb30_data_extend.id)\
        (db.clsb30_product_extend.product_id == product_id).select()
    result = dict()
    for data in product_data:
        result[data[db.clsb30_data_extend.name]] = data[db.clsb30_product_extend.price]
    return result

def check_server_version(): #vesion
    version = request.args[0]
    # path = settings.home_dir + "server_ver.txt"
    # server_ver = open(path).read()
    # print(server_ver)
    # if len(request.args) > 0:
    #     file_w = open(path, 'w')
    #     file_w.write(request.args[0])
    #     file_w.close()
    #     return dict(result=True)
    if check_version_mp(version):
        return dict(server='server_mp')
    else:
        return dict(server='server_kmp')

def search_product_mp(key_word):
    # key_word = request.args[0]
    metadata_version_name = 'version'
    metadata_product_size_name = 'product_size'
    list_book_id = list()
    list_book_id.append(485)
    list_book_id.append(484)
    list_book_id.append(481)

    category_list = db(db.clsb_category.category_parent == 1).select(db.clsb_category.id)
    for catefory in category_list:
        product_list = db(db.clsb_product.product_category == catefory['id']).select(db.clsb_product.id, limitby=(0,3))
        for product in product_list:
            list_book_id.append(product['id'])

    list_product = db(db.clsb_product.id.belongs(list_book_id))\
        (db.clsb_product.product_title.like('%' + key_word +'%')).select(db.clsb_product.id)
    list_id = list()
    for pr in list_product:
        list_id.append(pr['id'])
    try:
        # get metadata named: version
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()

        metadata_product_size = db(db.clsb_dic_metadata.metadata_name == metadata_product_size_name).select(
            db.clsb_dic_metadata.id).first()
        if metadata_product_size is None:
            metadata_product_size = 0
        products = list()
        db_product = db(db.clsb_product.id.belongs(list_id))(
            db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id) \
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                      db.clsb_category.ALL,
                                                                                      db.clsb_dic_creator.creator_name,
                                                                                      db.clsb_dic_publisher.publisher_name,
                                                                                      db.clsb_product.id,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                      db.clsb_product.product_description,
                                                                                      db.clsb_device_shelf.device_shelf_code,
                                                                                      db.clsb_device_shelf.device_shelf_type,
                                                                                      db.clsb_device_shelf.device_shelf_name,
                                                                                      db.clsb30_product_history.created_on,
                                                                                      orderby=~db.clsb30_product_history.created_on,
                                                                                      groupby=db.clsb_product.id).as_list()

        if db_product:

            for row in db_product:

                temp = dict()
                # select product version metadata
                metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_version_value is None:
                    metadata_version_value = dict()
                    metadata_version_value['metadata_value'] = 0
                metadata_product_size_value = db((db.clsb_product_metadata.metadata_id == metadata_product_size['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_product_size_value is None:
                    metadata_product_size_value = dict()
                    metadata_product_size_value['metadata_value'] = 0

                metadata_product_size_value['metadata_value']  = int(metadata_product_size_value['metadata_value']) * 1048576

                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsb_category']['id']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
                temp['product_description'] = row['clsb_product']['product_description']
                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['buy_time'] = row['clsb30_product_history']['created_on']
                temp['version'] = metadata_version_value['metadata_value']
                temp['product_size'] =  metadata_product_size_value['metadata_value']
                price_media = db(db.clsb30_product_extend.product_id == temp['id'])\
                    (db.clsb30_product_extend.extend_id == 1).select()
                if len(price_media) == 0:
                    temp['media_price'] = settings.fake_fund_media
                else:
                    temp['media_price'] = price_media.first()['price']
                price_quiz = db(db.clsb30_product_extend.product_id == temp['id'])\
                    (db.clsb30_product_extend.extend_id == 2).select()
                if len(price_quiz) == 0:
                    temp['quiz_price'] = settings.fake_fund_quiz
                else:
                    temp['quiz_price'] = price_quiz.first()['price']
                cover_price = db(db.clsb_product_metadata.product_id == row['clsb_product']['id']) \
                        (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                        (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                    db.clsb_product_metadata.metadata_value).as_list()
                if cover_price:
                    try:
                        temp['cover_price'] = int(cover_price[0]['metadata_value'])
                    except Exception as e:
                        pass
                else:
                    temp['cover_price'] = 0

                temp['has_quiz'] = False
                temp['buy_quiz'] = False
                temp['buy_media'] = False
                temp['has_media'] = False
                if temp['id'] == 481 or temp['id'] == 484 or temp['id'] == 485:
                    temp['buy_media'] = True
                    temp['has_media'] = True
                if temp['category_type'] != 'Exercise':
                    products.append(temp)
        return dict(page=0, items_per_page=0, total_items=len(products), total_pages=0,
                    products=products)
    except Exception as err:
        return dict(error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_product_mp():
    metadata_version_name = 'version'
    metadata_product_size_name = 'product_size'
    list_book_id = list()
    list_book_id.append(485)
    list_book_id.append(484)
    list_book_id.append(481)

    category_list = db(db.clsb_category.category_parent == 1).select(db.clsb_category.id)
    for catefory in category_list:
        product_list = db(db.clsb_product.product_category == catefory['id']).select(db.clsb_product.id, limitby=(0,3))
        for product in product_list:
            list_book_id.append(product['id'])
    try:
        # get metadata named: version
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()

        metadata_product_size = db(db.clsb_dic_metadata.metadata_name == metadata_product_size_name).select(
            db.clsb_dic_metadata.id).first()
        if metadata_product_size is None:
            metadata_product_size = 0
        products = list()
        db_product = db(db.clsb_product.id.belongs(list_book_id))(
            db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id) \
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                      db.clsb_category.ALL,
                                                                                      db.clsb_dic_creator.creator_name,
                                                                                      db.clsb_dic_publisher.publisher_name,
                                                                                      db.clsb_product.id,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                      db.clsb_product.product_description,
                                                                                      db.clsb_device_shelf.device_shelf_code,
                                                                                      db.clsb_device_shelf.device_shelf_type,
                                                                                      db.clsb_device_shelf.device_shelf_name,
                                                                                      db.clsb30_product_history.created_on,
                                                                                      orderby=~db.clsb30_product_history.created_on,
                                                                                      groupby=db.clsb_product.id).as_list()

        if db_product:

            for row in db_product:

                temp = dict()
                # select product version metadata
                metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_version_value is None:
                    metadata_version_value = dict()
                    metadata_version_value['metadata_value'] = 0
                metadata_product_size_value = db((db.clsb_product_metadata.metadata_id == metadata_product_size['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_product_size_value is None:
                    metadata_product_size_value = dict()
                    metadata_product_size_value['metadata_value'] = 0

                metadata_product_size_value['metadata_value']  = int(metadata_product_size_value['metadata_value']) * 1048576

                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsb_category']['id']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
                temp['product_description'] = row['clsb_product']['product_description']
                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['buy_time'] = row['clsb30_product_history']['created_on']
                temp['version'] = metadata_version_value['metadata_value']
                temp['product_size'] =  metadata_product_size_value['metadata_value']
                price_media = db(db.clsb30_product_extend.product_id == temp['id'])\
                    (db.clsb30_product_extend.extend_id == 1).select()
                if len(price_media) == 0:
                    temp['media_price'] = settings.fake_fund_media
                else:
                    temp['media_price'] = price_media.first()['price']

                price_quiz = db(db.clsb30_product_extend.product_id == temp['id'])\
                    (db.clsb30_product_extend.extend_id == 2).select()
                if len(price_quiz) == 0:
                    temp['quiz_price'] = settings.fake_fund_quiz
                else:
                    temp['quiz_price'] = price_quiz.first()['price']
                cover_price = db(db.clsb_product_metadata.product_id == row['clsb_product']['id']) \
                        (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                        (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                    db.clsb_product_metadata.metadata_value).as_list()
                if cover_price:
                    try:
                        temp['cover_price'] = int(cover_price[0]['metadata_value'])
                    except Exception as e:
                        pass
                else:
                    temp['cover_price'] = 0

                temp['has_quiz'] = False
                temp['buy_quiz'] = False
                temp['buy_media'] = False
                temp['has_media'] = False
                if temp['id'] == 481 or temp['id'] == 484 or temp['id'] == 485:
                    temp['buy_media'] = True
                    temp['has_media'] = True
                if temp['category_type'] != 'Exercise':
                    products.append(temp)
        return dict(page=0, items_per_page=0, total_items=len(products), total_pages=0,
                    products=products)
    except Exception as err:
        return dict(error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))

def read_json_file():
    path = settings.home_dir + "addtional.txt";
    import json

    # with open(path) as json_file:
    #     json_data = json.load(json_file)
    #     print(len(json_data))
    #     for page in json_data:
    #         print(page)
    json_file = open(path)
    json_str = json_file.read()
    json_data = json.loads(json_str)
    keyliststr = json_data.keys()
    keylist = list()
    for keystr in keyliststr:
        keylist.append(int(keystr))
    keylist.sort()
    list_data = list()
    for i in range(0, len(keylist)):
        key = str(keylist[i])
        list_media = json_data[key]
        for media in list_media:
            data = dict()
            data['page'] = key
            data['title'] = media['title']
            data['type'] = media['type']
            list_data.append(data)
    # for i in range(0, len(list_data)):
    #     print(list_data[i])

    return dict(media=list_data)

def get_list_media(): #product_code:
    import os
    type_dict = dict()
    type_dict['1'] = 'image'
    type_dict['2'] = 'wiki'
    type_dict['3'] = 'wiki'
    type_dict['4'] = 'sound'
    type_dict['5'] = 'sound'
    type_dict['6'] = 'video'
    type_dict['7'] = 'quiz'
    type_dict['108'] = 'app'
    type_dict['109'] = 'wiki'
    list_data = list()
    try:
        if len(request.args) == 0:
            return dict(error='Thieu tham so')
        product_code = request.args[0]
        path = settings.home_dir + product_code + "/" + product_code + "_json/addtional.txt"
        if os.path.isdir(settings.home_dir + product_code + "_01"):
            path = settings.home_dir + product_code + "_01/" + product_code + "/" + product_code + "_json/addtional.txt"
        # if not os.path.exists(path):
        #     return dict(media=list_data, path=path)
        import json

        json_file = open(path, 'r')

        json_str = json_file.read()
        json_data = json.loads(json_str)
        keyliststr = json_data.keys()
        keylist = list()
        for keystr in keyliststr:
            keylist.append(int(keystr))
        keylist.sort()
        for i in range(0, len(keylist)):
            key = str(keylist[i])
            list_media = json_data[key]
            for media in list_media:
                data = dict()
                data['page'] = key
                # str_title = str(media['title'])
                # str_u = unicode(str_title)
                # data['title'] = str_u.replace("\n", "")
                data['title'] = media['title']
                data['type'] = type_dict[str(media['type'])]
                list_data.append(data)
        # for i in range(0, len(list_data)):
        #     print(list_data[i])

        return dict(media=list_data)
    except Exception as err:
        return dict(media=list_data, err=str(err))

def change_fake():
    try:
        fake_value = int(request.args[0])
        db(db.clsb30_fake_ios.fake_name == 'ios').update(fake_value=fake_value)
        return dict(result=True)
    except Exception as err:
        return dict(result=str(err))

def test_check_version():
    if check_version_mp('Classbook.ios-1.6'):
        return True
    else:
        return False

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
            check_cache = myredis.get_cache(GET_INFO + product_id)
            if check_cache['result'] and check_cache['data'] is not None:
                data = json.loads(check_cache['data'])
                data['cache'] = True
                return data
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
                                                                                          db.clsb_product.data_type,
                                                                                          db.clsb_product.product_description, ).first()
            product_code = db_product['clsb_product']['product_code']
            cpid = None
            check_cp = db(db.clsb_product.product_code.like(product_code))(
                db.clsb20_product_cp.product_code.like(product_code)).select()
            if len(check_cp) > 0:
                cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            seller = ""
            if cpid == None:
                seller = "NXB Giáo Dục"
            else:
                seller = db(db.auth_user.id == cpid).select().first()
                seller = seller.first_name + " " + seller.last_name

            # if not (request.args(1)):
            #     if check_product_for_old_version(product_code):
            #         msg = "<h3 style='color: red;'>Phiên bản phần mềm bạn trên thiết bị cần cập nhật bản mới nhất để tải sản phẩm này</h3><br/>"
            #     elif db_product['clsb_product']['product_price'] > 0:
            #         msg = "<h3 style='color: red;'>Bạn phải trả phí cho sản phẩm này cho lần tải đầu tiên, các lần tải lại khi bị lỗi hoặc tải thêm là miễn phí</h3><br/>"
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
                if db_product['clsb_product']['data_type'] == 'epub' or db_product['clsb_product']['data_type'] == 'html':
                    product['category_type'] = db_product['clsb_product']['data_type']
                product['device_self_code'] = db_product['clsb_device_shelf']['device_shelf_code']
                product['device_self_type'] = db_product['clsb_device_shelf']['device_shelf_type']
                product['device_shelf_name'] = db_product['clsb_device_shelf']['device_shelf_name']
                product['version'] = metadata_version_value['metadata_value']
                product['seller'] = seller
                product['purchase'] = get_purchase_description(db_product['clsb_product']['product_code'])
                product['collection_name'] = db_relation['collection_name'] or ''
                product['creator_name'] = db_product['clsb_dic_creator']['creator_name']
                product['publisher_name'] = db_product['clsb_dic_publisher']['publisher_name']
                product['product_title'] = db_product['clsb_product']['product_title']
                product['data_type'] = db_product['clsb_product']['data_type']
                product['product_code'] = db_product['clsb_product']['product_code']
                product['product_cover'] = "http://classbook.vn/static/covers/" + \
                                            db_product['clsb_product']['product_code'] + "/cover.clsbi"
                product['product_thumb'] = "http://classbook.vn/static/covers/" + \
                                            db_product['clsb_product']['product_code'] + "/thumb.png"
                product['product_data'] = URL(a='cbs', c='download', f='data',
                                              scheme=True, host=True, args=db_product['clsb_product']['product_code'])
                product['product_pdf'] = URL(a='cbs', c='download', f='product',
                                             scheme=True, host=True, args=db_product['clsb_product']['product_code'])
                product['product_price'] = db_product['clsb_product']['product_price']
                product['product_description'] = msg + db_product['clsb_product']['product_description']
                product['free'] = check_free_for_classbook(product['category_id'])

                metadata = getmetadata(db_product['clsb_product']['id'])
                if metadata is None or 'error' in metadata:
                    metadata = dict()
                else:
                    metadata = metadata['item']
                    if 'cover_price' in metadata:
                        if int(metadata['cover_price']) > int(product['product_price']):
                            if product['product_price'] == 0:
                                metadata['discount'] = '100%'
                            else:
                                metadata['discount'] = str(
                                    100 - float(product['product_price']) / float(metadata['cover_price'])
                                    * 100) + '%'
                            #metadata['cover_price'] = str2price(metadata['cover_price'])
                            product['cover_price'] = int(metadata['cover_price'])
                            product['discount'] = metadata['discount']
                        else:
                            metadata['cover_price'] = 0
                            product['cover_price'] = 0
                    else:
                        product['cover_price'] = 0
                author = list()
                author.append(product['creator_name'])
                if 'co_author' in metadata:

                    metadata['co_author'] = metadata['co_author'].replace('<br>', '')
                    co_authors = metadata['co_author'].split("#", metadata['co_author'].count("#"))
                    for co_author in co_authors:
                        author.append(co_author)
                product['creator_name'] = author

                if len(request.args) >= 3 and product['free']:
                    product['product_price'] = 0
                # if product['free'] and isStoreApp:
                #     product['product_price'] = 0
                price_media = db(db.clsb30_product_extend.product_id == product['id'])\
                    (db.clsb30_product_extend.extend_id == 1).select()
                if len(price_media) == 0:
                    product['media_price'] = settings.fake_fund_media
                else:
                    product['media_price'] = price_media.first()['price']
                price_quiz = db(db.clsb30_product_extend.product_id == product['id'])\
                    (db.clsb30_product_extend.extend_id == 2).select()
                if len(price_quiz) == 0:
                    product['quiz_price'] = settings.fake_fund_quiz
                else:
                    product['quiz_price'] = price_quiz.first()['price']
                try:
                    #check media
                    product['has_media'] = check_media(product['product_code'])['check']
                    #check_quiz
                    hasquiz = db(db.clsb_product.product_code == 'Exer' + product['product_code'])\
                            (db.clsb_product.product_status == 'Approved').select()
                    if len(hasquiz) > 0:
                        product['has_quiz'] = True
                    else:
                        product['has_quiz'] = False
                    pass

                except Exception as err:
                    print(err)
                    product['buy_media'] = False
                    product['has_quiz'] = False
                    product['buy_quiz'] = False
                    product['has_media'] = False
        data = dict(product=product)
        myredis.write_cache(GET_INFO + request.args[0], str(json.dumps(data)), DEFAULT_TIME)
        data['cache'] = False
        return data
    except Exception as ex:
        print(str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))

def get_product_class(): #product_id
    product_class = 200
    try:
        product_id = request.args[0]
        class_sequent = db(db.clsb_product.id == product_id)\
                        (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                        (db.clsb_subject_class.class_id == db.clsb_class.id).select(db.clsb_class.class_sequent)
        if len(class_sequent) > 0:
            product_class = int(class_sequent.first()[db.clsb_class.class_sequent])
        return dict(product_class=product_class)
    except Exception as err:
        return dict(error=str(err))

def get_product_gift():
    try:
        list_id = list()
        list_id.append(677)
        #list_id.append(16)
        #list_id.append(481)
        list_product = list()

        # get metadata named: version
        metadata_version_name = 'version'
        metadata_product_size_name = 'product_size'
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()

        metadata_product_size = db(db.clsb_dic_metadata.metadata_name == metadata_product_size_name).select(
            db.clsb_dic_metadata.id).first()
        if metadata_product_size is None:
            metadata_product_size = 0
        db_product = db(db.clsb_product.id.belongs(list_id))(
                db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id) \
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                      db.clsb_category.ALL,
                                                                                      db.clsb_dic_creator.creator_name,
                                                                                      db.clsb_dic_publisher.publisher_name,
                                                                                      db.clsb_product.id,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                      db.clsb_product.product_description,
                                                                                      db.clsb_device_shelf.device_shelf_code,
                                                                                      db.clsb_device_shelf.device_shelf_type,
                                                                                      db.clsb_device_shelf.device_shelf_name,
                                                                                      groupby=db.clsb_product.id).as_list()
        if db_product:

            for row in db_product:

                temp = dict()
                # select product version metadata
                metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_version_value is None:
                    metadata_version_value = dict()
                    metadata_version_value['metadata_value'] = 0
                # print(row)
                metadata_product_size_value = db((db.clsb_product_metadata.metadata_id == metadata_product_size['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_product_size_value is None:
                    metadata_product_size_value = dict()
                    metadata_product_size_value['metadata_value'] = 0

                metadata_product_size_value['metadata_value'] = int(metadata_product_size_value['metadata_value']) * 1048576

                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsb_category']['id']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
                temp['product_description'] = row['clsb_product']['product_description']
                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['version'] = metadata_version_value['metadata_value']
                class_sequent = db(db.clsb_product.id == temp['id'])\
                                (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                                (db.clsb_subject_class.class_id == db.clsb_class.id).select(db.clsb_class.class_sequent)
                if len(class_sequent) > 0:
                    temp['class'] = int(class_sequent.first()[db.clsb_class.class_sequent])
                else:
                    temp['class'] = 0
                list_product.append(temp)
        return dict(products=list_product)
    except Exception as err:
        return dict(error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def get_product_has_media():
    try:
        list_categories = list()
        categories = db(db.clsb_category.category_parent == 1).select()
        for category in categories:
            cate = dict()
            cate['id'] = category['id']
            cate['category_name'] = category['category_name']
            cate['category_code'] = category['category_code']
            cate['product'] = list()
            products = db(db.clsb_product.product_category == cate['id']).select()
            for product in products:
                if check_media(product['product_code'])['check']:
                    temp = dict()
                    temp['id'] = product['id']
                    temp['product_title'] = product['product_title']
                    temp['product_code'] = product['product_code']
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                             args=temp['product_code'])
                    cate['product'].append(temp)
            list_categories.append(cate)
        return dict(categories=list_categories)
    except Exception as err:
        return dict(error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def get_gift_by_category():#category_id, token
    try:
        token = request.args[1]
        category_id = request.args[0]
        list_product = list()
        user = db(db.clsb_user.user_token == token).select()
        if len(user) == 0:
            return dict(error="TOKEN ERROR")
        else:
            user_id = user.first()['id']
        products = db(db.clsb_product.product_category == category_id)\
                (db.clsb_product.product_status.like("Approved")).select()
        for product in products:
            if check_media(product['product_code'])['check']:
                temp = dict()
                temp['id'] = product['id']
                temp['product_title'] = product['product_title']
                temp['product_code'] = product['product_code']
                temp['product_price'] = product['product_price']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=temp['product_code'])
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
                temp['bought'] = check_user_buy(product['id'], user_id)
                list_product.append(temp)
        return dict(products=list_product)
    except Exception as err:
        return dict(error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def check_user_buy(product_id, user_id):
    try:
        check = db(db.clsb30_product_history.user_id == user_id)\
                (db.clsb30_product_history.product_id == product_id).select()
        if len(check) == 0:
            return False
        else:
            return True
    except Exception as err:
        return False

MAX_GIFT = 2
def get_category_child(): #parent_id
    try:
        parent_id = request.args[0]
        list_categories = list()
        categories = db(db.clsb_category.category_parent == parent_id).select()
        for category in categories:
            cate = dict()
            cate['id'] = category['id']
            cate['category_name'] = category['category_name']
            cate['category_code'] = category['category_code']
            list_categories.append(cate)
        return dict(max_gift=MAX_GIFT, categories=list_categories)
    except Exception as err:
        return dict(error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def get_category_gift():
    try:
        list_id = list()
        list_id.append(54)
        list_id.append(55)
        list_id.append(56)
        list_id.append(57)
        list_id.append(58)
        list_id.append(59)
        list_id.append(60)
        list_id.append(61)
        list_id.append(62)
        list_id.append(63)
        list_id.append(64)
        list_id.append(65)
        list_categories = list()
        categories = db(db.clsb_category.id.belongs(list_id)).select()
        for category in categories:
            cate = dict()
            cate['id'] = category['id']
            cate['category_name'] = category['category_name']
            cate['category_code'] = category['category_code']

            list_categories.append(cate)
        return dict(max_gift=MAX_GIFT, categories=list_categories)
    except Exception as err:
        return dict(error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def get_gift_by_id():
    try:
        list_id = list()
        for arg in request.args:
            list_id.append(arg)
        device_serial = request.vars.device_serial
        token = request.vars.user_token
        user = db(db.clsb_user.user_token == token).select()
        if len(user) == 0:
            return dict(error="token error")

        #list_id.append(16)
        #list_id.append(481)
        list_product = list()

        # get metadata named: version
        metadata_version_name = 'version'
        metadata_product_size_name = 'product_size'
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()

        metadata_product_size = db(db.clsb_dic_metadata.metadata_name == metadata_product_size_name).select(
            db.clsb_dic_metadata.id).first()
        if metadata_product_size is None:
            metadata_product_size = 0
        db_product = db(db.clsb_product.id.belongs(list_id))(
                db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id) \
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                      db.clsb_category.ALL,
                                                                                      db.clsb_dic_creator.creator_name,
                                                                                      db.clsb_dic_publisher.publisher_name,
                                                                                      db.clsb_product.id,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                      db.clsb_product.product_description,
                                                                                      db.clsb_device_shelf.device_shelf_code,
                                                                                      db.clsb_device_shelf.device_shelf_type,
                                                                                      db.clsb_device_shelf.device_shelf_name,
                                                                                      groupby=db.clsb_product.id).as_list()
        if db_product:

            for row in db_product:

                temp = dict()
                # select product version metadata
                metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_version_value is None:
                    metadata_version_value = dict()
                    metadata_version_value['metadata_value'] = 0
                # print(row)
                metadata_product_size_value = db((db.clsb_product_metadata.metadata_id == metadata_product_size['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                if metadata_product_size_value is None:
                    metadata_product_size_value = dict()
                    metadata_product_size_value['metadata_value'] = 0

                metadata_product_size_value['metadata_value']  = int(metadata_product_size_value['metadata_value']) * 1048576

                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsb_category']['id']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']
                temp['product_description'] = row['clsb_product']['product_description']
                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['version'] = metadata_version_value['metadata_value']
                class_sequent = db(db.clsb_product.id == temp['id'])\
                                (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                                (db.clsb_subject_class.class_id == db.clsb_class.id).select(db.clsb_class.class_sequent)
                if len(class_sequent) > 0:
                    temp['class'] = int(class_sequent.first()[db.clsb_class.class_sequent])
                else:
                    temp['class'] = 0
                list_product.append(temp)
                db.clsb30_media_history.insert(
                                        product_title=temp['product_title'],
                                        product_id=temp['id'],
                                        user_id=user.first()['id'],
                                        category_id=row['clsb_category']['id'],
                                        product_price=0)
                db.clsb30_product_history.insert(
                                        product_title=temp['product_title'],
                                        product_id=temp['id'],
                                        user_id=user.first()['id'],
                                        category_id=row['clsb_category']['id'],
                                        product_price=0)
        db.clsb30_samsung_promotion.insert(device_serial=device_serial, user_id=user.first()['id'])
        return dict(products=list_product)
    except Exception as err:
        return dict(error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def feature_image(): #product_code
    try:
        product_code = request.args[0];
        images = db(db.clsb20_product_image.product_code == product_code).select()
        imgs = list()
        user_cp = db(db.clsb20_product_cp.product_code == product_code).select(db.clsb20_product_cp.created_by);
        if len(user_cp) == 0:
            return dict(images=imgs)
        user_cp_path = find_cp_root(str(user_cp.first()['created_by']))
        for image in images:
            imgs.append(URL(a='cpa',c='download', f='image',args=[user_cp_path, 'upload', image['image']]))
        return dict(images=imgs)
    except Exception as err:
        return dict(error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def find_cp_root(cp_id):
    try:
        query = "SELECT created_by from auth_user where id=" + str(cp_id)
        cp = db.executesql(query, as_dict=True)
        if cp[0]['created_by'] == None:
            return "CP" + str(cp_id)
        root_id = cp[0]['created_by']
        return find_cp_root(str(root_id))
    except Exception as err:
        return err.message + " on line: "+ str(sys.exc_traceback.tb_lineno)

def cp_root():
    return find_cp_root("43")

def update_access_view():
    try:
        db(db.clsb_product.show_on.like("%ANDROID_APP%")).update(show_on="ANDROID_APP/STORE_WEB/STORE_APP")
        return dict(success=True)
    except Exception as err:
        return err.message + " on line: "+ str(sys.exc_traceback.tb_lineno)

def check_samsung_promotion():
    try:
        device_serial = request.args[0]
        check_device = db(db.clsb30_samsung_promotion.device_serial == device_serial).select()
        if len(check_device) > 0:
            return dict(result=False)
        if len(request.args) == 2:
            token = request.args[1]
            user = db(db.clsb_user.user_token == token).select()
            if len(user) == 0:
                return dict(result=False, mess="token error")
            check_user = db(db.clsb30_samsung_promotion.user_id == user.first()['id']).select()
            if len(check_user) > 0:
                return dict(result=False)
        return dict(result=True)
    except Exception as err:
        return dict(result=False, error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def update_description_app():
    try:
        list_id = list()
        apps = db(db.clsb_product.show_on == "ANDROID_APP/STORE_WEB/STORE_APP")\
                (db.clsb_product.product_code.like("%.%")).select()
        for app in apps:
            db(db.clsb_product.id == app['id']).update(product_description="<h4>Chỉ hỗ trợ thiết bị máy tính bảng</h4>\n" + app['product_description'])
        return dict(result="SUCCESS")
    except Exception as err:
        return dict(result=False, error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def update_quiz_price():
    try:
        list_insert = list()
        quizs = db(db.clsb_product.product_code.like("Exer%")).select()
        for quiz in quizs:
            code = str(quiz['product_code']).replace("Exer", "")
            product = db(db.clsb_product.product_code == code).select()
            if len(product) > 0:
                temp = dict()
                temp['product_id'] = product.first()['id']
                temp['extend_id'] = 2
                temp['price'] = 5000
                list_insert.append(temp)
        db.clsb30_product_extend.bulk_insert(list_insert)
        return dict(result=True)
    except Exception as err:
        return dict(result=False, error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def get_version():
    try:
        metadata_version_name = 'version'
        data = list()
        ids = request.vars.id
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()
        if str(type(ids)) == "<type 'str'>":
            temp = dict()
            temp['id'] = ids
            metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == ids)).select(
                    db.clsb_product_metadata.metadata_value).first()
            if metadata_version_value is None:
                metadata_version_value = dict()
                metadata_version_value['metadata_value'] = 0
            temp['version'] = metadata_version_value['metadata_value']
            data.append(temp)
            return dict(products=data)

        for product_id in ids:
            temp = dict()
            temp['id'] = product_id
            metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == product_id)).select(
                    db.clsb_product_metadata.metadata_value).first()
            if metadata_version_value is None:
                metadata_version_value = dict()
                metadata_version_value['metadata_value'] = 0
            temp['version'] = metadata_version_value['metadata_value']
            data.append(temp)
        return dict(products=data)
    except Exception as err:
        return dict(result=False, error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def test_openpyxl():
    try:
        import openpyxl
        workbook = openpyxl.load_workbook(filename='/tmp/sgk-sgv.xlsx')
        worksheet = workbook.get_sheet_by_name('sheet1')
        for row in worksheet.iter_rows():
            data = {
                'id':  row[0].value,
                'product_code': row[1].value, # Column B
                'product_title':  row[2].value, # Column C
            }
    except Exception as err:
        return err.message + " on line: "+ str(sys.exc_traceback.tb_lineno)


def get_all_history():
    """
    service list all book/app that user bought on classbook store
    params: app.version/serial/token/page/item_per_page
    """
    try:
        if len(request.args) < 3:
            return dict(error="Lỗi request")
        app_ver = request.args[0]
        token = request.args[2]
        version_app = ""
        if 'android' in app_ver.lower():
            version_app = "ANDROID_APP"
        if 'ios' in app_ver.lower():
            version_app = "IOS_APP"
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")

        if len(request.args) > 5:
            except_type = ['Exercise', 'Application']
        else:
            except_type = ['Exercise']
        products = list()
        db_product = db(db.clsb_product.product_status.like('Approved'))\
                (db.clsb30_product_history.user_id == user.first()['id'])\
                (db.clsb_product.id == db.clsb30_product_history.product_id)\
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (~db.clsb_product_type.type_name.belongs(except_type))\
                (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                      db.clsb_category.ALL,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                    db.clsb30_product_history.created_on,
                                                                                      orderby=~db.clsb30_product_history.created_on,
                                                                                      groupby=db.clsb_product.id).as_list()
        if db_product:

            for row in db_product:
                temp = dict()
                temp['id'] = row['clsb_product']['id']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['created_on'] = row['clsb30_product_history']['created_on']
                products.append(temp)

        return dict(total_items=len(products), total_buy=len(products),
                    products=products)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_history_detail():
    try:
        if len(request.args) < 3:
            return dict(error="Lỗi request")
        app_ver = request.args[0]
        serial = request.args[1]
        token = request.args[2]
        version_app = ""
        if 'android' in app_ver.lower():
            version_app = "ANDROID_APP"
        if 'ios' in app_ver.lower():
            version_app = "IOS_APP"
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")
        user_id = user.first()['id']
        page = 0
        except_type = ['Exercise', 'Application']
        items_per_page = settings.items_per_page
        if len(request.args) > 3:
            page = int(request.args[3])
        if len(request.args) > 4:
            items_per_page = int(request.args[4])
        limitby = (page * items_per_page, page * items_per_page + items_per_page)
        select_history = db(db.clsb30_product_history.user_id == user_id)\
            (db.clsb30_product_history.product_id == db.clsb_product.id)\
            (db.clsb_product.show_on.like('%' + version_app + '%'))\
            (db.clsb_product.product_category == db.clsb_category.id)\
            (db.clsb_category.category_type == db.clsb_product_type.id)\
            (~db.clsb_product_type.type_name.belongs(except_type))\
            (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.id,
                                                                               db.clsb_product.product_title,
                                                                               db.clsb_product.product_code,
                                                                               db.clsb_category.category_name,
                                                                               db.clsb_dic_creator.creator_name,
                                                                               db.clsb_product_type.type_name,
                                                                               orderby=~db.clsb30_product_history.created_on,
                                                                               limitby=limitby,
                                                                               groupby=db.clsb_product.id)
        products = list()
        for p in select_history:
            temp = dict()
            temp['id'] = p[db.clsb_product.id]
            temp['product_title'] = p[db.clsb_product.product_title]
            temp['product_code'] = p[db.clsb_product.product_code]
            temp['category_name'] = p[db.clsb_category.category_name]
            temp['creator_name'] = p[db.clsb_dic_creator.creator_name]
            temp['product_type'] = p[db.clsb_product_type.type_name]
            temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=temp['product_code'])
            products.append(temp)
        return dict(items=products, page=page, items_per_page=items_per_page, total_items=len(products),
                    total_pages=len(products) / items_per_page + 1)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_cate_item(version_app, cat_id, page, items_per_page):
    try:
        products = list()
        db_product = list()
        product_query = db(db.clsb_product.product_status.like('Approved'))
        if version_app != "":
            product_query = product_query(db.clsb_product.show_on.like('%' + version_app + '%'))
        product_query = product_query(db.clsb_product.product_category == cat_id)

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
        return dict(err=str(ex))


def category_top_product():
    try:
        version_app = ""
        if 'version' in request.vars:
            version_app = request.vars.version
        parent_id = request.args[0]
        select_child = db(db.clsb_category.category_parent == parent_id).select()
        child_id = 1
        if len(select_child) > 0:
            child_id = select_child.first()['id']
        return get_cate_item(version_app, child_id, 0, 5)
    except Exception as ex:
        print str(ex)
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_product_by_creator():
    try:
        page = 0
        item_per_page = 18
        products = list()
        creator_name = request.vars.creator
        version_app = ""
        if 'version' in request.vars:
            version_app = request.vars.version
        if 'page' in request.vars:
            page = int(request.vars.page)
        if 'item_per_page' in request.vars:
            item_per_page = int(request.vars.item_per_page)
        query = db(db.clsb_product.product_status.like("Approved"))\
                (db.clsb_product.show_on.like('%' + version_app + '%'))\
                (~db.clsb_product.product_code.like("Exer%"))
        get_by_creator = query(db.clsb_product.product_creator == db.clsb_dic_creator.id)\
                (db.clsb_dic_creator.creator_name.like(creator_name)).select(db.clsb_product.id)
        products_id = list()
        for product in get_by_creator:
            products_id.append(product[db.clsb_product.id])
        get_by_co_author = query(~db.clsb_product.id.belongs(products_id))\
                (db.clsb_product.id == db.clsb_product_metadata.product_id)\
                (db.clsb_product_metadata.metadata_id == 1)\
                (db.clsb_product_metadata.metadata_value.like('%' + creator_name + '%')).select(db.clsb_product.id)
        for product in get_by_co_author:
            products_id.append(product[db.clsb_product.id])
        select_product = db(db.clsb_product.id.belongs(products_id))\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.id,
                                                                                db.clsb_product.product_code,
                                                                                db.clsb_product.product_title,
                                                                                db.clsb_product.product_price,
                                                                                db.clsb_dic_creator.creator_name,
                                                                                limitby=(page*item_per_page, (page + 1) * item_per_page))
        for product in select_product:
            temp = dict()
            temp['product_id'] = product[db.clsb_product.id]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['product_title'] = product[db.clsb_product.product_title]
            temp['product_price'] = product[db.clsb_product.product_price]
            temp['product_creator'] = product[db.clsb_dic_creator.creator_name]
            temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                            scheme=True, host=True, args=temp['product_code'])
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
            products.append(temp)
        total_pages = (len(products_id) / item_per_page)
        if (total_pages * item_per_page) < len(products_id):
            total_pages += 1
        return dict(products=products, total_items=len(products_id),
                    total_pages=total_pages, page=page)
    except Exception as ex:
        print str(ex)
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


#def update_cp_name():
#    select_cp = db(db.auth_user).select()
#    for cp in select_cp:
#        new_name = cp['first_name'] + " " + cp['last_name']
#        db(db.auth_user.id == cp['id']).update(first_name=new_name)
#    return "SUCCESS"


def get_product_by_cp():
    try:
        page = 0
        item_per_page = 18
        products = list()
        product_id = request.vars.product_id
        version_app = ""
        if 'version' in request.vars:
            version_app = request.vars.version
        if 'page' in request.vars:
            page = int(request.vars.page)
        if 'item_per_page' in request.vars:
            item_per_page = int(request.vars.item_per_page)
        products_id = list()
        current_product = db(db.clsb_product.id == product_id).select().first()
        product_code = current_product['product_code']
        query = db(db.clsb_product.product_status.like("Approved"))\
                (db.clsb_product.show_on.like('%' + version_app + '%'))\
                (~db.clsb_product.product_code.like("Exer%"))
        cpid = None
        check_cp = db(db.clsb_product.product_code.like(product_code))(
                db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
        print(cpid)
        if cpid == None:
            select1 = query(db.clsb_product.product_category == current_product['product_category']).select(db.clsb_product.id)
            for product in select1:
                products_id.append(product[db.clsb_product.id])
        else:
            select2 = query(db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
                    (db.clsb20_product_cp.created_by == cpid).select(db.clsb_product.id)
            for product in select2:
                products_id.append(product[db.clsb_product.id])
        select_product = db(db.clsb_product.id.belongs(products_id))\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.id,
                                                                                db.clsb_product.product_code,
                                                                                db.clsb_product.product_title,
                                                                                db.clsb_product.product_price,
                                                                                db.clsb_dic_creator.creator_name,
                                                                                limitby=(page*item_per_page, (page + 1) * item_per_page))
        for product in select_product:
            temp = dict()
            temp['product_id'] = product[db.clsb_product.id]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['product_title'] = product[db.clsb_product.product_title]
            temp['product_price'] = product[db.clsb_product.product_price]
            temp['product_creator'] = product[db.clsb_dic_creator.creator_name]
            temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                            scheme=True, host=True, args=temp['product_code'])
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
            products.append(temp)
        total_pages = (len(products_id) / item_per_page)
        if (total_pages * item_per_page) < len(products_id):
            total_pages += 1
        return dict(products=products, total_items=len(products_id),
                    total_pages=total_pages, page=page)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_product_by_publisher():
    try:
        page = 0
        item_per_page = 18
        products = list()
        product_id = request.vars.product_id
        version_app = ""
        if 'version' in request.vars:
            version_app = request.vars.version
        if 'page' in request.vars:
            page = int(request.vars.page)
        if 'item_per_page' in request.vars:
            item_per_page = int(request.vars.item_per_page)
        query = db(db.clsb_product.product_status.like("Approved"))\
                    (db.clsb_product.show_on.like('%' + version_app + '%'))\
                    (~db.clsb_product.product_code.like("Exer%"))
        products_id = list()
        current_product = db(db.clsb_product.id == product_id).select().first()
        product_code = current_product['product_code']
        cpid = None
        check_cp = db(db.clsb_product.product_code.like(product_code))(
                db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
        print(cpid)
        if cpid == None:
            select2 = query(db.clsb_product.product_category == current_product['product_category']).select(db.clsb_product.id)
            for product in select2:
                products_id.append(product[db.clsb_product.id])
        else:
            publisher_id = current_product['product_publisher']
            select1 = query(db.clsb_product.product_publisher == publisher_id).select(db.clsb_product.id)
            for product in select1:
                products_id.append(product[db.clsb_product.id])
        select_product = db(db.clsb_product.id.belongs(products_id))\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.id,
                                                                                db.clsb_product.product_code,
                                                                                db.clsb_product.product_title,
                                                                                db.clsb_product.product_price,
                                                                                db.clsb_dic_creator.creator_name,
                                                                                limitby=(page*item_per_page, (page + 1) * item_per_page))
        for product in select_product:
            temp = dict()
            temp['product_id'] = product[db.clsb_product.id]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['product_title'] = product[db.clsb_product.product_title]
            temp['product_price'] = product[db.clsb_product.product_price]
            temp['product_creator'] = product[db.clsb_dic_creator.creator_name]
            temp['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                            scheme=True, host=True, args=temp['product_code'])
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
            products.append(temp)
        total_pages = (len(products_id) / item_per_page)
        if (total_pages * item_per_page) < len(products_id):
            total_pages += 1
        return dict(products=products, total_items=len(products_id),
                    total_pages=total_pages, page=page)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def update_total_download():
    try:
        top_fake_id = list()
        select_top_fake = db(db.clsb_product.id > 0).select(db.clsb_product.total_download, db.clsb_product.id,
                                                            orderby=db.clsb_product.total_download,
                                                            limitby=(0, 20))
        for fake in select_top_fake:
            top_fake_id.append(fake[db.clsb_product.id])
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        select_download = db(db.clsb_download_archieve.id > 0).select(count, db.clsb_download_archieve.product_id,
                                                                      groupby=db.clsb_download_archieve.product_id)
        for down in select_download:
            if down[db.clsb_download_archieve.product_id] not in top_fake_id:
                db(db.clsb_product.id == down[db.clsb_download_archieve.product_id]).update(total_download=down[count])
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def auto_get_relation():
    try:
        limit = 11
        relations = list()
        list_ids = list()
        list_fix_relation = list()
        product_id = request.vars.product_id
        version_app = ""
        if 'version' in request.vars:
            version_app = request.vars.version
        current_product = db(db.clsb_product.id == product_id).select().first()
        select_fix_relation = db(db.clsb_product_relation.product_id == product_id).select()
        for fix in select_fix_relation:
            list_fix_relation.append(fix['relation_id'])

        query = db(db.clsb_product.product_status.like("Approved"))\
                (db.clsb_product.show_on.like('%' + version_app + '%'))\
                (~db.clsb_product.id.belongs(list_fix_relation))\
                (~db.clsb_product.product_code.like("Exer%"))\
                (db.clsb_product.id != product_id)\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id)
        if current_product['subject_class'] != 262:
            select_relation = query(db.clsb_product.subject_class == current_product['subject_class'])\
                    (~db.clsb_product.id.belongs(list_ids))\
                    (db.clsb_product.product_category == current_product['product_category']).select(db.clsb_product.id,
                                                                                                     db.clsb_product.product_code,
                                                                                                    db.clsb_product.product_title,
                                                                                                    db.clsb_product.product_price,
                                                                                                    db.clsb_dic_creator.creator_name,
                                                                                                     db.clsb_product.total_download,
                                                                                                     orderby=db.clsb_product.total_download,
                                                                                                     limitby=(0, limit))
            for product in select_relation:
                list_ids.append(product[db.clsb_product.id])
                relations.append(convert2product(product))
            if len(list_ids) < limit:
                select_relation = query(db.clsb_product.subject_class == current_product['subject_class'])\
                        (~db.clsb_product.id.belongs(list_ids)).select(db.clsb_product.id,
                                                                       db.clsb_product.product_code,
                                                                    db.clsb_product.product_title,
                                                                    db.clsb_product.product_price,
                                                                    db.clsb_dic_creator.creator_name,
                                                                    db.clsb_product.total_download,
                                                                    orderby=db.clsb_product.total_download,
                                                                    limitby=(0, limit - len(list_ids)))
                for product in select_relation:
                    list_ids.append(product[db.clsb_product.id])
                    relations.append(convert2product(product))
        if len(list_ids) < limit:
            select_relation = query(db.clsb_product.product_category == current_product['product_category'])\
                        (~db.clsb_product.id.belongs(list_ids)).select(db.clsb_product.id,
                                                                       db.clsb_product.product_code,
                                                                    db.clsb_product.product_title,
                                                                    db.clsb_product.product_price,
                                                                    db.clsb_dic_creator.creator_name,
                                                                    db.clsb_product.total_download,
                                                                    orderby=db.clsb_product.total_download,
                                                                    limitby=(0, limit - len(list_ids)))
            for product in select_relation:
                list_ids.append(product[db.clsb_product.id])
                relations.append(convert2product(product))
        return dict(products=relations)
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


def update_category_lv3():
    try:
        ids = list()
        select_product = db(db.clsb_product.product_category == 125).select(db.clsb_product.id, limitby=(0, 20))
        for product in select_product:
            ids.append(product[db.clsb_product.id])
        db(db.clsb_product.id.belongs(ids)).update(product_category=129)
        return "SUCCESS"
    except Exception as ex:
        print str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno)
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))