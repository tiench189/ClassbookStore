#"com.tinhvan.tvb.bookshelf"#@author: hant 27-02-2013
def index():
    import sys
    return sys.version

def get():# software
    
    software_pck = dict()
    software_pck.update({"bookshelf_pck": "com.tinhvan.tvb.bookshelf"})
    software_pck.update({"ereader_pck": "com.tinhvan.tvb.classbook"})
    software_pck.update({"resetbookshelf_pck": "com.tinhvan.tvb.re"})
    software_pck.update({"storeapp_pck": "com.tvb.classbook.store"})

    if len(request.args) > 0:
        software = request.args(0)
        if software == "BOOKSHELF":
            soft_pck = software_pck["bookshelf_pck"]
        elif software == "EREADER":
            soft_pck = software_pck["ereader_pck"]
        elif software == "RESETBOOKSHELF":
            soft_pck = software_pck["resetbookshelf_pck"]
        elif software == "STOREAPP":
            soft_pck = software_pck["storeapp_pck"]
        else:
            soft_pck = ""     
        try:
            rows = db(db.clsb_version.software == software).select(db.clsb_version.ALL, orderby = db.clsb_version.release_date).as_list()
            d = list()
            for row in rows:
                temp = dict()
                temp['software'] = row['software']
                temp['lastest_version'] = row['lastest_version']
                temp['description'] = row['description']
                temp['release_date'] = str(row['release_date'])
                temp['software_pck'] = soft_pck
    
                d.append(temp)
            return dict(items=d, message=CB_MSG_0000)
        except Exception as e:
            return dict(error =  CB_0003 + str(e)) #DB_RQ_FAILD
    else:
        try:
            rows = db().select(db.clsb_version.ALL, orderby=db.clsb_version.release_date).as_list()
            d = list()
            for row in rows:
                temp = dict()
                temp['software'] = row['software']
                temp['lastest_version'] = row['lastest_version']
                temp['description'] = row['description']
                temp['release_date'] = str(row['release_date'])
                
                software = row['software']
                if software == "BOOKSHELF":
                    soft_pck = software_pck["bookshelf_pck"]
                elif software == "EREADER":
                    soft_pck = software_pck["ereader_pck"]
                elif software == "RESETBOOKSHELF":
                    soft_pck = software_pck["resetbookshelf_pck"]
                else:
                    soft_pck = ""     
                temp['software_pck'] = soft_pck
   
                d.append(temp)
                
            return dict(items=d, message=CB_MSG_0000)
        except Exception as e:
            return dict(error =  CB_0003 + str(e)) #DB_RQ_FAILD
        
