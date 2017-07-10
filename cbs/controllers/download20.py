# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Name:        download20
#
# Purpose:     new download for store 2.0
#
# Version:     2.0
#
# Author:      manhtd
#
# Created:     3/12/14
# Updated:     3/12/14
#
# Copyright:   (c) Tinh Vân Books
#
# Todo: 
#-----------------------------------------------------------------------------
"""


def pdf_guide():
    import fs.path
    file = "guide.pdf"
    path = fs.path.join(settings.home_dir, file)
    response.headers['Content-Length'] = osFileServer.getinfo(file)['size']
    response.headers['Content-Type'] = 'application/pdf'
    response.headers['Content-Disposition'] = "attachment; filename=huong_dan_khai_thac_du_lieu_classbook.pdf"
    response.headers['X-Sendfile'] = path
