#@author: hant
SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

"""
    Get a list of all district in database.
"""

table = 'clsb_district'
def get():
    if not table in db.tables(): NOT_EXIST
    try:
        rows =  db().select(db.clsb_district.ALL,
                            orderby = db.clsb_district.district_code)
        
        l = list()
        for row in rows:
            temp = dict()
            temp['district_id'] = row['id']
            temp['district_name'] = row['district_name']
            temp['district_code'] = row['district_code']
            temp['district_description'] = row['description']

            l.append(temp)
        return dict(items=l)
    except Exeption as e:
        return dict(error = str(e))