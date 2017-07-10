# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Name:        download
#
# Purpose:     
#
# Version:     1.1
#
# Author:      manhtd
#
# Created:     1/16/14
# Updated:     1/16/14
#
# Copyright:   (c) Tinh Vân Books
#
# Todo: 
#-----------------------------------------------------------------------------
"""


def demo():
    try:
        from fs.osfs import OSFS

        file_server = OSFS('/home/demo/')

        if len(request.args) != 1:
            raise HTTP(400)
        path = request.args[0]
        if file_server.exists(path):
            response.headers['Content-Length'] = file_server.getinfo(path)['size']
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = "attachment; filename=%s" % path
            return response.stream(file_server.open(path=path, mode='rb'))
        else:
            raise HTTP(404)
    except:
        raise HTTP(200, "ERROR")
