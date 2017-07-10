# -*- coding: utf-8 -*-
__author__ = 'tanbm'


def index():
    return dict()


def check():
    if(len(request.args)) < 2:
        raise (200, "Request fail")
    list_accept = [["EH411500041", "1400"], ["EH411500002", "2000"]]

    devicel_serial = request.args[0]
    code = request.args[1]

    for accept in list_accept:
        if (devicel_serial == accept[0]) and (code == accept[1]):
            return dict(result=True)
    return dict(result=False)