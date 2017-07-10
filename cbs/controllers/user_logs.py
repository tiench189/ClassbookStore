########################################
#hant 04-03-2013 

#import cbMsg
SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_user_log'

# to manage
#def index():
#    if not table in db.tables(): return NOT_EXIST #table do not exist
    
#    try:
#        form = SQLFORM.grid(db[table], args = request.args[:1],
#                            onupdate = auth.archive,
#                            showbuttontext = False,
#                            user_signature = False)
#        return dict(form = form)
#    except Exception as ex: 
#        if request.is_local: 
#            return ex 
#        else: 
#            raise DB_RQ_FAILD
        
# usage: /CBS/user_logs/insert?user_id=...&user_action=...&date_log=...&search_text=...&product_code=...&ip_address=...&from_system=...
def insert():
    if request.vars and request.vars > 2:
        try:
            db[table].insert(**request.vars)
            return SUCCESS
        except Exception as e:
            return e#DB_RQ_FAILD
    return LACK_ARGS

#def selectAll():
#    if not table in db.tables(): redirect(URL('error'))
#    tbl = db().select(db[table].ALL, orderby=db[table].user_id)
#    return dict(tbl=tbl)

#def deleteRow(): # by id
#    if not table in db.tables(): return NOT_EXIST

#    if request.vars.id:
#        try:
#            db(db[table]._id == request.vars.id).delete()
#            return SUCCESS
#        except Exception:
#            return DB_RQ_FAILD
#    else:
#        return LACK_ARGS
    
# exp: /CBS/user_log/deleteMultipleRow?delete=delete&id1=4&id2=6
#def deleteMultipleRow(): # by id
#    if not table in db.tables(): return NOT_EXIST
    
#    if request.vars and len(request.vars)>1:
#        rows = request.vars.pop("delete")
#        for archieve in request.vars:
#            db(db[table]._id == request.vars[archieve]).delete()
#        return SUCCESS
#    else:
#        return LACK_ARGS
    
# exp: /CBS/user_log/update?id=7&product_code=1249435634673463
#def update(): # by id
#    if not table in db.tables(): return NOT_EXIST
    
#    if request.vars and request.vars > 1:
#        try:
#            db(db[table]._id==request.vars.id).update(**request.vars)
#            return SUCCESS
#        except Exception:
#            return DB_RQ_FAILD
#    else:
#        return LACK_ARGS


# exp:  /CBS/user_log/selectByID?id=7
#def selectByID():
#    if not table in db.tables(): return NOT_EXIST

#    if request.vars and len(request.vars) == 1:
#        try:
#            seletedID = db(db[table]._id.like(request.vars.id)).select() 
#            return seletedID
#        except Exception:
#            return DB_RQ_FAILD
#    else:
#        return LACK_ARGS