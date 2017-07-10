#@author: hant

SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_country'

"""
    Get all country from country table.
"""
def get():
    if not table in db.tables(): NOT_EXIST
    try:
        rows =  db().select(db.clsb_country.ALL,
                            orderby = db.clsb_country.country_code)
        
        l = list()
        for row in rows:
            temp = dict()
            temp['country_id'] = row['id']
            temp['country_name'] = row['country_name']
            temp['country_code'] = row['country_code']
            temp['country_description'] = row['description']

            l.append(temp)
        return dict(items=l)
    except Exeption as e:
        return dict(error = str(e))