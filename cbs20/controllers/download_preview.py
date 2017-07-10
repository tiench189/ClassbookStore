# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys
import os
import usercp

PREFIX = "_PREVIEW"

def product(): #params: product_code
    try:
        product_code = request.args[len(request.args) - 1].split(".")[0]
        client_type = "ANDROID"
        if len(request.args) >= 2:
            client_type = request.args[0]
        select_product = db(db.clsb_product.product_code.like(product_code)).select()
        if len(select_product) == 0:
            raise HTTP(400, T("Product not exist"))
        product_id = select_product.first()['id']
        db.clsb30_preview_log.insert(product_id=product_id, client_type=client_type)
        path = settings.home_dir + product_code + PREFIX + "/" + product_code + PREFIX + ".pdf"
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = settings.home_dir + settings.cp_dir + "CP" + str(cpid) + "/published/" + \
                   product_code + PREFIX + "/" + product_code + PREFIX + ".pdf"
        response.headers['Content-Length'] = os.path.getsize(path)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=" + product_code + '.pdf'
        #response.headers['X-Sendfile'] = path
        response.stream(path)
    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        raise HTTP(404, "Request false")


def data(): #params: product_code, user_token
    try:
        if len(request.args) == 2:
            user_token = request.args[1]
            try:
                user_id = db(db.clsb_user.user_token.like(user_token)).select().first()
                user_id = user_id['id']
            except Exception as ex:
                raise HTTP(400, T("Token is false"))
        product_code = request.args[0]
        path = settings.home_dir + product_code + PREFIX + "/" + product_code + PREFIX + ".zip"
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = settings.home_dir + settings.cp_dir + "CP" + str(cpid) + "/published/" + \
                   product_code + PREFIX + "/" + product_code + PREFIX + ".zip"
        response.headers['Content-Length'] = os.path.getsize(path)
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + product_code + '.zip'
        response.headers['X-Sendfile'] = path
    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        raise HTTP(404, "Request false")


def check_available(): #params: product_code
    try:
        product_code = request.args[0]
        path = settings.home_dir + product_code + PREFIX + "/" + product_code + PREFIX + ".pdf"
        check_cp = db(db.clsb_product.product_code.like(product_code))\
                (db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = settings.home_dir + settings.cp_dir + "CP" + str(cpid) + "/published/" + product_code + PREFIX + \
                   "/" + product_code + PREFIX + ".pdf"
        return dict(result=os.path.isfile(path))
    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return dict(result=False)