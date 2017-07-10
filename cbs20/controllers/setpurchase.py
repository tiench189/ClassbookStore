__author__ = 'PhuongNH'

def get_list_set_purchase():
    rows = db().select(db.clsb30_set_purchase.ALL)
    set_list = list()

    for row in rows:
        if cal_product_in_set(row.id) > 0:
            item = dict();
            item['id'] = row.id
            item['set_code'] = row.set_code
            item['set_name'] = row.set_name
            item['description'] = row.description
            item['price'] = cal_set_price(row.id)
            set_list.append(item)

    return dict(items=set_list)


def cal_product_in_set(set_id):

    rows = db(db.clsb30_set_product.set_purchase_id == set_id).select(db.clsb30_set_product.ALL).as_list()

    if rows is None:
        return 0

    return len(rows)

def cal_set_price(set_id):

    rows = db(db.clsb30_set_product.set_purchase_id == set_id).select(db.clsb30_set_product.ALL)

    price = 0
    for row in rows:
        product = db(db.clsb_product.id == row.product_id).select(db.clsb_product.product_price).first()
        price += float(product.product_price)
    return price


def get_set_info():
    if request.vars or len(request.args) < 1:
        return dict(error="Đối số không phù hợp")
    set_id = request.args[0]
    set_item = db(db.clsb30_set_purchase.id == set_id).select(db.clsb30_set_purchase.ALL).first()

    if set_item is None:
        return dict(error="Set item not exits")
    item = dict()
    item['id'] = set_item.id
    item['set_code'] = set_item.set_code
    item['set_name'] = set_item.set_name
    item['description'] = set_item.description

    return dict(set_item = item)



def get_item_set_product():

    if request.vars or len(request.args) < 1:
        return dict(error="Đối số không phù hợp")

    metadata_version_name = 'version'
    metadata_product_size_name = 'product_size'

    set_purchase_id = request.args[0]
    product_list = list();
    rows = db(db.clsb30_set_product.set_purchase_id == set_purchase_id).select(db.clsb30_set_product.ALL)
    # get metadata named: version
    metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
        db.clsb_dic_metadata.id).first()

    metadata_product_size = db(db.clsb_dic_metadata.metadata_name == metadata_product_size_name).select(
        db.clsb_dic_metadata.id).first()

    for row in rows:
        item = dict()
        db_product = db(db.clsb_product.product_status.like('Approved'))(
            db.clsb_product.id == row.product_id)(
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
                                                                                      orderby=~db.clsb_product.created_on,
                                                                                      groupby=db.clsb_product.id).first()

        # select product version metadata
        metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
            db.clsb_product_metadata.product_id == db_product['clsb_product']['id'])).select(
            db.clsb_product_metadata.metadata_value).first()

        if metadata_version_value is None:
            metadata_version_value = dict()
            metadata_version_value['metadata_value'] = 0

        metadata_product_size_value = db((db.clsb_product_metadata.metadata_id == metadata_product_size['id']) & (
            db.clsb_product_metadata.product_id == db_product['clsb_product']['id'])).select(
            db.clsb_product_metadata.metadata_value).first()

        if metadata_product_size_value is None:
            metadata_product_size_value = dict()
            metadata_product_size_value['metadata_value'] = 0

        metadata_product_size_value['metadata_value'] *= 1048576

        item['id'] = db_product['clsb_product']['id']
        item['category_id'] = db_product['clsb_category']['id']
        item['category_name'] = db_product['clsb_category']['category_name']
        item['category_code'] = db_product['clsb_category']['category_code']
        item['category_type'] = db_product['clsb_product_type']['type_name']
        item['device_self_code'] = db_product['clsb_device_shelf']['device_shelf_code']
        item['device_self_type'] = db_product['clsb_device_shelf']['device_shelf_type']
        item['device_shelf_name'] = db_product['clsb_device_shelf']['device_shelf_name']
        item['product_description'] = db_product['clsb_product']['product_description']
        item['creator_name'] = db_product['clsb_dic_creator']['creator_name']
        item['publisher_name'] = db_product['clsb_dic_publisher']['publisher_name']
        item['product_title'] = db_product['clsb_product']['product_title']
        item['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                    args=db_product['clsb_product'][
                                        'product_code']) #row['clsb_product']['product_cover']
        item['product_code'] = db_product['clsb_product']['product_code']
        item['product_price'] = db_product['clsb_product']['product_price']
        item['buy_time'] = db_product['clsb30_product_history']['created_on']
        item['version'] = metadata_version_value['metadata_value']
        item['product_size'] =  metadata_product_size_value['metadata_value']

        cover_price = db(db.clsb_product_metadata.product_id == db_product['clsb_product']['id']) \
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
            db.clsb_product_metadata.metadata_value).as_list()
        if cover_price:
            try:
                item['cover_price'] = int(cover_price[0]['metadata_value'])
            except Exception as e:
                pass
        else:
            item['cover_price'] = 0
        product_list.append(item)

    return dict(product_list=product_list)


def buy_set_product():
    """
    params: set_id/token
    """
    try:
        if request.vars or len(request.args) < 2:
            return dict(error="Đối số không phù hợp")

        set_id = request.args[0]
        token = request.args[1]

        user = db(db.clsb_user.user_token.like(token)).select(db.clsb_user.id).first()

        user_cash = db(db.clsb_user.id == user['id']).select(db.clsb_user.fund, db.clsb_user.data_sum).first()
        if float(user_cash['fund']) < float(cal_set_price(set_id)):
            return dict(error="Tiền trong tài khoản không đủ. Bạn có muốn chuyển đến trang nạp tiền không?", code="NOT_ENOUGH_MONEY")
        try:
            rows = db(db.clsb30_set_product.set_purchase_id == set_id).select(db.clsb30_set_product.ALL)
            for row in rows:
                result = buy_product(row.product_id, token)

        except:
            return dict(error="error")
        return dict(result="success")
    except Exception as e:

        print e


def buy_product(product_id, token):
    try:
        """
        function checkout when user buy book/app on classbook store
        params: product_code/token
        """
        try:
            product = db(db.clsb_product.id == product_id)(
                db.clsb_category.id == db.clsb_product.product_category).select().first()
        except:
            return dict(error="Mã sách không đúng")

        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")

        classbook_device = False

        result = pay_to_log(user.first(), product, classbook_device)
        #print result
        if result is True:
            return dict(result=result)
        else:
            return dict(error=result['error'])
    except Exception as e:
        print e