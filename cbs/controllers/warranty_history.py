########################################
#hant 04-03-2013 

SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_warranty_history'


def get():
    try:
        rows = db().select(db[table].ALL).as_list()
        return dict(items=rows)
    except Exception as e:
        return dict(error=DB_RQ_FAILD + str(e)) 


@request.restful()
def api():
    response.view = 'generic.json'

    def POST(*ars, **vas):
        if len(ars) == 0:
            if "token" in vas and "username" in vas:
                db_user = db(db.clsb_user.username == vas["username"])(db.clsb_user.user_token == vas["token"])\
                    .select(db.clsb_user.id).first()
                if db_user is not None:
                    db_devices = db(db.clsb_device.user_id == db_user.id).select(db.clsb_device.device_serial)
                    ret = list()
                    for device in db_devices:
                        db_query = db(db.clsb_warranty_history.device_serial == device.device_serial)
                        db_ret = db_query.select(db.clsb_warranty_history.ALL).as_list()
                        ret.extend(db_ret)
                    return dict(result=ret)
        return dict()

    return locals()
