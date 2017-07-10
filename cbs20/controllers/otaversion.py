def index():
    import sys
    return sys.version

def get():

    try:
        rows = db().select(db.clsb_ota_version.ALL, orderby = db.clsb_ota_version.release_date).as_list()
        d = list()
        for row in rows:
            temp = dict()
            temp['software'] = row['software']
            temp['lastest_version'] = row['lastest_version']
            temp['description'] = row['description']
            temp['release_date'] = str(row['release_date'])
            temp['MD5'] = str(row['MD5'])

            d.append(temp)

        return dict(items=d, message=CB_MSG_0000)
    except Exception as e:
        return dict(error =  CB_0003 + str(e))