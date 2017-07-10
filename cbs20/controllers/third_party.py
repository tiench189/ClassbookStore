# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys
from datetime import datetime


def log():
    try:
        username = request.vars.username
        time = request.vars.time
        price = request.vars.fund
        name = request.vars.name
        code = request.vars.code
        type = request.vars.type
        from_system = request.vars.from_system

        # kiem tra user
        select_user = db(db.clsb_user.username.like(username)).select()
        if len(select_user) == 0:
            return dict(error="User not exist")

        time = datetime.strptime(time, '%Y%m%d%H%M%S')
        db.clsb30_third_party_log.insert(username=username,
                                         time_set=time,
                                         party_code=code,
                                         party_name=name,
                                         party_type=type,
                                         price=price,
                                         from_system=from_system)
        return dict(result="SUCCESS")
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
