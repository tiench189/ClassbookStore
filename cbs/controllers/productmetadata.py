#@author: hant

SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_product_metadata'

def get():
    if not table in db.tables(): NOT_EXIST
    
    rows = db(db[table].metadata_id == db.clsb_dic_metadata._id)\
            (db[table].product_id == db.clsb_product._id).select(db[table]._id,
                                                                 db[table].metadata_value,
                                                                 db.clsb_product.product_title,
                                                                 db.clsb_dic_metadata.metadata_name).as_list()
            
    d = list()
    for row in rows:
        temp = dict()
        temp['product_metadata_id'] = row['clsb_product_metadata']['id']
        temp['metadata'] = row['clsb_dic_metadata']['metadata_name']
        temp['product_title'] = row['clsb_product']['product_title']
        temp['metadata_value'] = row['clsb_product_metadata']['metadata_value']
        d.append(temp)
        
    return dict(items=d)

def getinfo(): #params id
    if not table in db.tables(): NOT_EXIST
    
    rows = db(db.clsb_product_metadata._id == request.args(0))\
            (db[table].metadata_id == db.clsb_dic_metadata._id)\
            (db[table].product_id == db.clsb_product._id).select(db[table]._id,
                                                         db[table].metadata_value,
                                                         db.clsb_product.product_title,
                                                         db.clsb_dic_metadata.metadata_name)
        
    l = list()
    for row in rows:
        temp = dict()
        temp['product_metadata_id'] = row['clsb_product_metadata']['id']
        temp['metadata'] = row['clsb_dic_metadata']['metadata_name']
        temp['product_title'] = row['clsb_product']['product_title']
        temp['metadata_value'] = row['clsb_product_metadata']['metadata_value']
        l.append(temp)
    return dict(items=l)

    