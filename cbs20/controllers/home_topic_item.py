########################################
#hant 04-03-2013 
#import cbMsg
SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_home_topic_item'


def get():
    """
        Get all product by topic item id
    """
    if not table in db.tables():
        return NOT_EXIST
    version_app = ""
    if request.vars and 'version' in request.vars:
        version_app = request.vars.version
    if request.args and len(request.args) == 1:
        rows = db(db[table].topic_id == request.args(0))
        rows = rows(db[table].product_id == db.clsb_product.id)
        rows = rows(db.clsb_product.product_status == "Approved")
        if version_app != "":
            rows = rows(db.clsb_product.show_on.like('%' + version_app.upper() + '%'))
        rows = rows(db.clsb_product.product_creator == db.clsb_dic_creator.id)
        rows = rows(db.clsb_product.product_category == db.clsb_category.id)
        rows = rows(db.clsb_category.category_type == db.clsb_product_type.id)
        rows = rows(db.clsb_product.product_category == db.clsb_category.id)
        rows = rows(db.clsb_product.product_publisher == db.clsb_dic_publisher.id)
        rows = rows.select(db[table].id, db[table].topic_id, db[table].product_id, db[table].topic_item_order,
                           db[table].item_path, db.clsb_product.ALL, db.clsb_product_type.type_name,
                           db.clsb_dic_creator.creator_name, db.clsb_category.category_name,
                           db.clsb_dic_publisher.publisher_name, db.clsb_category.category_code,
                           orderby=db[table].topic_item_order).as_list()
        d = list()
        
        for row in rows:
            row['clsb_home_topic_item']['item_path'] = URL('download', args=row['clsb_home_topic_item']['item_path'],
                                                           host=True)
            temp = dict()
            temp['home_topic_item_id'] = row['clsb_home_topic_item']['id']
            temp['topic_id'] = row['clsb_home_topic_item']['topic_id']
            temp['topic_item_order'] = row['clsb_home_topic_item']['topic_item_order']
            temp['item_path'] = row['clsb_home_topic_item']['item_path']
            temp['product_id'] = row['clsb_home_topic_item']['product_id']
            cover_price = db(db.clsb_product_metadata.product_id == temp['product_id'])\
                                    (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id)\
                                    (db.clsb_dic_metadata.metadata_name == 'cover_price').select(db.clsb_product_metadata.metadata_value).as_list()
            if cover_price:
                try:
                    temp['cover_price'] = int(cover_price[0]['metadata_value'])
                except Exception as e:
                    print str(e)
            else:
                temp['cover_price'] = 0
            temp['product_category'] = row['clsb_product']['product_category']
            temp['product_collection'] = row['clsb_product']['product_collection']
            temp['product_creator'] = row['clsb_dic_creator']['creator_name']
            temp['product_publisher'] = row['clsb_dic_publisher']['publisher_name']
            temp['product_title'] = row['clsb_product']['product_title']
            temp['product_price'] = row['clsb_product']['product_price']
            temp['product_code'] = row['clsb_product']['product_code']
            temp['total_download'] = row['clsb_product']['total_download']
            temp['product_cover'] = URL(a = 'cbs', c = 'download', f = 'thumb',
                 scheme = True, host = True, args = row['clsb_product']['product_code'])
            temp['creator_name'] = row['clsb_dic_creator']['creator_name']
            temp['type_name'] = row['clsb_product_type']['type_name']
            temp['category_name'] = row['clsb_category']['category_name']
            temp['category_code'] = row['clsb_category']['category_code']
            temp['free'] = check_free_for_classbook(temp['product_category'])
            d.append(temp)
        return dict(items=d)
    else:
        return dict(error=LACK_ARGS)

"""
    Get the topic_item's info.
"""
# exp:  /CBS/home_topic_item/getinfo?id=7
def getinfo():
    if not table in db.tables(): NOT_EXIST
    rows = db(db.clsb_home_topic_item._id.like(request.vars.id))\
            (db[table].product_id==db.clsb_product._id)\
            (db.clsb_product.product_creator == db.clsb_dic_creator.id)\
            (db.clsb_product.product_category == db.clsb_category.id)\
            (db.clsb_category.category_type == db.clsb_product_type.id)\
            (db.clsb_product.product_category==db.clsb_category._id)\
            (db.clsb_product.product_publisher==db.clsb_dic_publisher._id ).select(
                       db[table].id,
                       db[table].topic_id,
                       db[table].product_id,
                       db[table].topic_item_order,
                       db[table].item_path,
                       db.clsb_product.ALL,
                       db.clsb_product_type.type_name,
                       db.clsb_dic_creator.creator_name,
                       db.clsb_category.category_name,
                       db.clsb_dic_publisher.publisher_name,
                       db.clsb_category.category_code,
                       orderby=db[table].topic_id).as_list()
    d = list()
    
    for row in rows:
        row['clsb_home_topic_item']['item_path'] = URL('download',args=row['clsb_home_topic_item']['item_path'], host = True)
        temp = dict()
        temp['home_topic_item_id'] = row['clsb_home_topic_item']['id']
        temp['product_id'] = row['clsb_home_topic_item']['product_id']
        temp['topic_id'] = row['clsb_home_topic_item']['topic_id']
        temp['topic_item_order'] = row['clsb_home_topic_item']['topic_item_order']
        temp['item_path'] = row['clsb_home_topic_item']['item_path']

        temp['product_category'] = row['clsb_product']['product_category']
        temp['product_collection'] = row['clsb_product']['product_collection']
        temp['product_creator'] = row['clsb_dic_creator']['creator_name']
        temp['product_publisher'] = row['clsb_dic_publisher']['publisher_name']
        temp['product_title'] = row['clsb_product']['product_title']
        temp['product_price'] = row['clsb_product']['product_price']
        temp['product_description'] = row['clsb_product']['product_description']
        temp['product_code'] = row['clsb_product']['product_code']
        temp['product_status'] = row['clsb_product']['product_status']
        temp['total_download'] = row['clsb_product']['total_download']
        temp['product_cover'] = URL(a = 'cbs', c = 'download', f = 'cover',
                 scheme = True, host = True, args = row['clsb_product']['product_code'])
        temp['product_data'] = URL(a = 'cbs', c = 'download', f = 'data',
                 scheme = True, host = True, args = row['clsb_product']['product_code'])
        temp['product_pdf'] = URL(a = 'cbs', c = 'download', f = 'product',
                 scheme = True, host = True, args = row['clsb_product']['product_code'])
        temp['creator_name'] = row['clsb_dic_creator']['creator_name']
        temp['type_name'] = row['clsb_product_type']['type_name']
        temp['category_name'] = row['clsb_category']['category_name']
        temp['category_code'] = row['clsb_category']['category_code']
        d.append(temp)
    return dict(items=d)

#def getinfo():
#    if not table in db.tables(): return NOT_EXIST
#
#    if request.vars and len(request.vars) == 1:
#        try:
#            rows = db(db[table]._id.like(request.vars.id)).select().as_list()
#            for row in rows:
#                row['item_path'] = URL('download',args=row['item_path'], host = True)
#            return dict(items=rows)
#        except Exception:
#            return dict(error=DB_RQ_FAILD)
#    else:
#        return dict(error=LACK_ARGS)

def download():
    return response.download(request, db)