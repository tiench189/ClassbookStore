# -*- coding: utf-8 -*-

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


def get_product_history():
    """
    service list all book/app that user bought on classbook store
    params: app.version/serial/token/page/item_per_page
    """
    metadata_version_name = 'version'
    try:
        if len(request.args) < 3:
            return dict(error="Lỗi request")
        app_ver = request.args[0]
        serial = request.args[1]
        token = request.args[2]
        #type = request.args[3]
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")
        result = checkTimeOut(user.first()['username'], token)
        if result != "OK":
            return dict(error=result)
        page = 0
        items_per_page = settings.items_per_page
        if len(request.args) > 3:
            page = int(request.args[3])
        if len(request.args) > 4:
            items_per_page = int(request.args[4])
        limitby = (page * items_per_page, (page + 1) * items_per_page)

        # get metadata named: version
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()

        list_free = list()
        cat_free = db(db.clsb30_category_classbook_device).select()
        for cat in cat_free:
            list_free.append(cat['product_category'])
        total_items = db(db.clsb_product.product_status.like('Approved'))(db.clsb30_product_history.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb30_product_history.product_id)(
            db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                 groupby=db.clsb_product.id)
        list_buy = list()
        for product in total_items:
            list_buy.append(product['id'])

        total_items = len(total_items)
        total_items_a = db((db.clsb_product.product_status.like('Approved')) & (~db.clsb_product.id.belongs(list_buy)))(
            (db.clsb_download_archieve.user_id == user.first()['id']) & (db.clsb_download_archieve.status.like("Completed")))(
            db.clsb_product.id == db.clsb_download_archieve.product_id)(
            db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (~db.clsb_category.id.belongs(list_free) & ~db.clsb_category.category_parent.belongs(list_free)) \
                (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                 groupby=db.clsb_product.id)
        total_items_a = len(total_items_a)
        total_items_tmp = total_items

        total_items += total_items_a
        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page
        products = list()

        db_product = db(db.clsb_product.product_status.like('Approved'))(
            db.clsb30_product_history.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb30_product_history.product_id)(
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
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['buy_time'] = row['clsb30_product_history']['created_on']
                temp['version'] = metadata_version_value['metadata_value']
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

                products.append(temp)

        if len(products) < items_per_page:
            if len(products) > 0:
                limitby = (0, items_per_page - len(products))
            else:
                print 'total item' + str(total_items_tmp)
                start = (page * items_per_page) - total_items_tmp
                end = ((page + 1) * items_per_page) - total_items_tmp
                print 'start: ' + str(start)
                print 'end: ' + str(end)
                if start < 0L:
                    start = 0
                if end < 0L:
                    end = 0
                limitby = (start, end)


            db_product_a = db((db.clsb_product.product_status.like('Approved')) & (~db.clsb_product.id.belongs(list_buy)))((db.clsb_download_archieve.user_id == user.first()['id']) & (db.clsb_download_archieve.status.like("Completed")))(
                db.clsb_product.id == db.clsb_download_archieve.product_id)(
                db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
                    (db.clsb_product.product_category == db.clsb_category.id)\
                    (~db.clsb_category.id.belongs(list_free) & ~db.clsb_category.category_parent.belongs(list_free)) \
                    (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                          db.clsb_category.ALL,
                                                                                          db.clsb_download_archieve.ALL,
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
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                                args=row['clsb_product'][
                                                    'product_code']) #row['clsb_product']['product_cover']
                    temp['product_code'] = row['clsb_product']['product_code']
                    temp['product_price'] = row['clsb_product']['product_price']
                    temp['buy_time'] = row['clsb_download_archieve']['created_on']
                    temp['version'] = metadata_version_value['metadata_value']
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

                    products.append(temp)

        return dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
                    products=products)
    except Exception as ex:
        print str(ex)
        return dict(error=ex.message)


def search_in_product_history():
    """
    service list all book/app that user bought on classbook store
    params: ver=app.version&key=key_word&token=token&page=page&item=item_per_page
    """

    metadata_version_name = 'version'
    try:
        if len(request.vars) < 3:
            return dict(error="Lỗi request")
        app_ver = request.vars.ver
        key_word = request.vars.key
        token = request.vars.token
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")
        result = checkTimeOut(user.first()['username'], token)
        if result != "OK":
            return dict(error=result)
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

        # get list creator name like keyword
        list_creator = db(db.clsb_dic_creator.creator_name.like('%' + key_word + "%")).select(
            db.clsb_dic_creator.id).as_list()
        list_free = list()
        cat_free = db(db.clsb30_category_classbook_device).select()
        for cat in cat_free:
            list_free.append(cat['product_category'])
        total_items = db(db.clsb_product.product_status.like('Approved'))(
            db.clsb30_product_history.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb30_product_history.product_id)
        if len(list_creator) > 0:
            total_items = total_items(db.clsb_product.product_creator.belongs(list_creator))
        total_items = total_items(db.clsb_product.product_title.like('%' + key_word + '%')) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                 groupby=db.clsb_product.id)
        list_buy = list()
        for product in total_items:
            list_buy.append(product['id'])

        total_items = len(total_items)
        total_items_a = db((db.clsb_product.product_status.like('Approved')) & (~db.clsb_product.id.belongs(list_buy)))(
            db.clsb_download_archieve.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb_download_archieve.product_id)
        if len(list_creator) > 0:
            total_items_a = total_items_a(db.clsb_product.product_creator.belongs(list_creator))
        total_items_a = total_items_a(db.clsb_product.product_title.like('%' + key_word + '%')) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                (~db.clsb_category.id.belongs(list_free) & ~db.clsb_category.category_parent.belongs(list_free)) \
                (db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.id,
                                                                                 groupby=db.clsb_product.id)
        total_items_a = len(total_items_a)
        total_items_tmp = total_items

        total_items += total_items_a
        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page
        products = list()

        db_product = db(db.clsb_product.product_status.like('Approved'))(
            db.clsb30_product_history.user_id == user.first()['id'])(
            db.clsb_product.id == db.clsb30_product_history.product_id)
        if len(list_creator) > 0:
            db_product = db_product(db.clsb_product.product_creator.belongs(list_creator))
        db_product = db_product(db.clsb_product.product_title.like('%' + key_word + '%'))(
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
                temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                            args=row['clsb_product'][
                                                'product_code']) #row['clsb_product']['product_cover']
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['buy_time'] = row['clsb30_product_history']['created_on']
                temp['version'] = metadata_version_value['metadata_value']
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

                products.append(temp)

        if len(products) < items_per_page:
            if len(products) > 0:
                limitby = (0, items_per_page - len(products))
            else:
                start = (page * items_per_page) - total_items_tmp
                end = ((page + 1) * items_per_page) - total_items_tmp
                if start < 0L:
                    start = 0
                if end < 0L:
                    end = 0
                limitby = (start, end)

            db_product_a = db(
                (db.clsb_product.product_status.like('Approved')) & (~db.clsb_product.id.belongs(list_buy)))(
                db.clsb_download_archieve.user_id == user.first()['id'])(
                db.clsb_product.id == db.clsb_download_archieve.product_id)(
                db.clsb_download_archieve.status.like("Completed"))

            if len(list_creator) > 0:
                db_product_a = db_product_a(db.clsb_product.product_creator.belongs(list_creator))
            db_product_a = db_product_a(db.clsb_product.product_title.like('%' + key_word + '%'))(
                db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                    (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                    (db.clsb_category.category_type == db.clsb_product_type.id) \
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
                    # select product version metadata
                    metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == row['clsb_product']['id'])).select(
                    db.clsb_product_metadata.metadata_value).first()

                    if metadata_version_value is None:
                        metadata_version_value = dict()
                        metadata_version_value['metadata_value'] = 0

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
                    temp['product_cover'] = URL(a='cbs', c='download', f='thumb', scheme=True, host=True,
                                                args=row['clsb_product'][
                                                    'product_code']) #row['clsb_product']['product_cover']
                    temp['product_code'] = row['clsb_product']['product_code']
                    temp['product_price'] = row['clsb_product']['product_price']
                    temp['buy_time'] = row['clsb_download_archieve']['created_on']
                    temp['version'] = metadata_version_value['metadata_value']
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

                    products.append(temp)

        return dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
                    products=products)
    except Exception as ex:
        print str(ex)
        return dict(error=ex.message)


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


def free_for_classbook(): #category_id
    category_id = int(request.args[0])
    return dict(result=check_free_for_classbook(category_id))


def check_buy_product(): #product_id, token
    token = request.args[1]
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    result = checkTimeOut(user.first()['username'], token)
    if result != "OK":
        return dict(error=result)

    check_buy = db(db.clsb30_product_history.product_id == int(request.args[0]))(db.clsb30_product_history.user_id == user.first()['id']).select()

    productData = db(db.clsb_product.id == int(request.args[0])).select().first()

    if not check_free_for_classbook(productData['product_category']):
        downloaded = db(db.clsb_download_archieve.product_id == productData['id'])(db.clsb_download_archieve.status.like("Completed"))(db.clsb_download_archieve.user_id == user.first()['id']).select()
        if len(downloaded) > 0 or len(check_buy) > 0:
            return dict(result=True)
    elif len(check_buy) > 0:
            return dict(result=True)

    return dict(result=False)