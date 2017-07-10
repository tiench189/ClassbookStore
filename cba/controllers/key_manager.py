__author__ = 'Tien'

import sys
import usercp

@auth.requires_authorize()
def gen_key():
    try:
        key_available = list()
        if "limit" not in request.vars:
            return dict(key_available=key_available)
        limit = int(request.vars.limit)
        des = ""
        if "des" in request.vars:
            des = request.vars.des
        query_active = db(db.cbapp_windows_activated_key.license_key != "").select()
        key_active = list()
        for key in query_active:
            key_active.append(key['license_key'])
        query_avalable = db(db.cbapp_windows_key_available.gender != 1)\
                (~db.cbapp_windows_key_available.license_key.belongs(key_active)).select(db.cbapp_windows_key_available.license_key,
                                                                                         limitby=(0, limit))
        for avalable in query_avalable:
            key_available.append(avalable['license_key'])
        db(db.cbapp_windows_key_available.license_key.belongs(key_available)).update(gender=1, description=des)
        return dict(key_available=key_available)
    except Exception as err:
        print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))
