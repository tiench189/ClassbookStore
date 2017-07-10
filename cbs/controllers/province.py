#@author: hant
SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_province'
def get():
    if not table in db.tables(): NOT_EXIST
    try:
        rows =  db().select(db.clsb_province.ALL,
                            orderby = db.clsb_province.province_code)
        
        l = list()
        for row in rows:
            temp = dict()
            temp['province_id'] = row['id']
            temp['province_name'] = row['province_name']
            temp['province_code'] = row['province_code']
            temp['province_description'] = row['description']

            l.append(temp)
        return dict(items=l)
    except Exeption as e:
        return dict(error = str(e))
    
def district(): #args: province_id
    print 'test'
    if len(request.args) != 1:
        return dict(error = CB_0002)#LACK_ARGS
    try:
        province_id = request.args(0)
        
        rows =  db(db.clsb_district.province_id == province_id).select(db.clsb_district.ALL, 
                                                                       orderby = db.clsb_district.district_code)
        
#         return dict(d= rows)
        
        l = list()
        for row in rows:
            temp = dict()
            temp['district_id'] = row['id']
            temp['district_name'] = row['district_name']
            temp['district_code'] = row['district_code']
            temp['district_description'] = row['description']
            l.append(temp)
        return dict(items=l)
    except Exception as e:
        return dict(error = str(e))