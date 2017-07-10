########################################
#hant 04-03-2013 
#import cbMsg
SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_home_topic'

def get():
    if not table in db.tables(): NOT_EXIST
    rows = db(db[table].category_id == db.clsb_category._id).select(db[table]._id,
                       db[table].topic_name,
                       db[table].topic_order,
                       db[table].category_id,
                       db[table].used_for,
                       db.clsb_category.category_type,
                       orderby=db[table].topic_order).as_list()
                       
    d = list()
    for row in rows:
        temp = dict()
        temp['id'] = row['clsb_home_topic']['id']
        temp['topic_name'] = row['clsb_home_topic']['topic_name']
        temp['topic_order'] = row['clsb_home_topic']['topic_order']
        temp['category_id'] = row['clsb_home_topic']['category_id']
        temp['used_for'] = row['clsb_home_topic']['used_for']
        temp['category_type'] = row['clsb_category']['category_type']
        d.append(temp)
    return dict(items=d)
    #return dict(tbl=rows)

# exp:  /CBS/download_archieve/selectByID?id=7
def getinfo():
    if not table in db.tables(): return NOT_EXIST

    if request.vars and len(request.vars) == 1:
        try:
            rows = db(db[table]._id ==request.vars.id)(db[table].category_id == db.clsb_category._id).select().as_list()
            d = list()
            for row in rows:
                temp = dict()
                temp['id'] = row['clsb_home_topic']['id']
                temp['topic_name'] = row['clsb_home_topic']['topic_name']
                temp['topic_order'] = row['clsb_home_topic']['topic_order']
                temp['category_id'] = row['clsb_home_topic']['category_id']
                temp['used_for'] = row['clsb_home_topic']['used_for']
                temp['category_type'] = row['clsb_category']['category_type']
                d.append(temp)
            return dict(items=d)
        except Exception:
            return DB_RQ_FAILD
    else:
        return LACK_ARGS
