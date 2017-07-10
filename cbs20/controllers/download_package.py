# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys
import os
import zipfile
import pdf2dev
import shutil
import zipfile
import fs.path

HOME_DIR = "/home/CBSData/"
CP_DIR = "CPData/"


def make_data():
    try:
        serial = request.vars.serial
        bs_id = request.vars.bs
        data = list()
        select_id = db(db.clsb30_sach_trong_bo.bs_id == bs_id).select(db.clsb30_sach_trong_bo.product_id,
                                                                      distinct=True)
        products = list()
        path_out = '/home/TEMP_DATA/data/' + bs_id + "/" + serial + "/Unzip/"
        for p in select_id:
            idx = p[db.clsb30_sach_trong_bo.product_id]
            temp = dict()
            temp['id'] = idx
            check = check_cp(idx)
            temp['product_code'] = check['product_code']
            if check['result']:
                temp['path'] = HOME_DIR + CP_DIR + "CP" + str(check['cpid']) + \
                               "/published/" + str(check['product_code'])
            else:
                temp['path'] = HOME_DIR + check['product_code']
            products.append(temp)
        for p in products:
            r = create_data_file(p, path_out)
            data.append(r)
            e = encrypt_product(p, serial, path_out)
            data.append(e)
        shutil.copy2('/home/TEMP_DATA/data/' + bs_id + "/classbookdb.sqlite",
                     '/home/TEMP_DATA/data/' + bs_id + "/" + serial + "/")
        zipdir('/home/TEMP_DATA/data/' + bs_id + "/" + serial,
               '/home/TEMP_DATA/data/' + bs_id + "/" + serial + ".zip")
        return dict(data=data)
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def create_file_data():
    try:
        bs_id = request.args[0]
        select_id = db(db.clsb30_sach_trong_bo.bs_id == bs_id).select(db.clsb30_sach_trong_bo.product_id,
                                                                      distinct=True)
        products = list()
        path_out = "/home/TEMP_DATA/data/" + str(bs_id)
        create_dir(path_out)
        for p in select_id:
            idx = p[db.clsb30_sach_trong_bo.product_id]
            temp = dict()
            temp['id'] = idx
            check = check_cp(idx)
            temp['product_code'] = check['product_code']
            if check['result']:
                temp['path'] = HOME_DIR + CP_DIR + "CP" + str(check['cpid']) + \
                               "/published/" + str(check['product_code'])
            else:
                temp['path'] = HOME_DIR + check['product_code']
            products.append(temp)
        data = "PATH|" + path_out
        for p in products:
            data += "\n" + str(p['product_code']) + "|" + str(p['path'])
        cr = create_dir(path_out)
        return write_text_file(path_out + "/" + "data.txt", data)
        # return dict(path=path_out, data=data, cr=cr)
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def create_sh_file():
    try:
        import xlrd
        path = "/home/scripts/tvxl.xls"
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        script = ""
        for idx in range(0, 7):
            script += "python data_window.py 9 " + str(sheet.cell(idx, 0).value) + "\n"
        return write_text_file("/home/scripts/tvxl.sh", script)
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def write_text_file(path, content):
    try:
        with open(path, "w") as text_file:
            text_file.write(content)
        return dict(content=content)
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def encrypt_product(product, serial, path_out):
    try:
        pdf2dev.encrypt(serial, product['path'] + "/" + product['product_code'] + ".E.pdf",
                        path_out + product['product_code'] + "/" + product['product_code'] + ".pdf")
        return dict(result="SUCCESS")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno) + " " + serial)


def create_data_file(product, path_out):
    try:
        path = path_out + product['product_code']
        extract_zip(product['path'] + "/" + product['product_code'] + ".zip", path)
        extract_zip(product['path'] + "/" + product['product_code'] + "_json.zip", path)
        extract_zip(HOME_DIR + "Exer" + product['product_code'] + "/" + "Exer" + product['product_code'] + ".zip",
                    path)
        return dict(result="SUCCESS")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def extract_zip(path_in, path_out):
    try:
        if os.path.exists(path_in):
            create_dir(path_out)
            with zipfile.ZipFile(path_in, "r") as z:
                z.extractall(path_out)
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def check_cp(idx):
    try:
        select_cp = db(db.clsb_product.id == idx) \
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code).select()
        if len(select_cp) == 0:
            select_p = db(db.clsb_product.id == idx).select()
            return dict(result=False, mess="NOT CP", product_code=select_p.first()['product_code'])
        return dict(result=True, cpid=select_cp.first()[db.clsb20_product_cp.created_by],
                    product_code=select_cp.first()[db.clsb_product.product_code])
    except Exception as err:
        return dict(result=False, mess=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno),
                    product_code="")


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def add_sach():
    try:
        bs_id = 1
        cate_ids = [54, 55, 56, 57, 58]
        data = list()
        select_product = db(db.clsb_product.product_category.belongs(cate_ids)).select()
        for p in select_product:
            temp = dict()
            temp['bs_id'] = bs_id
            temp['product_id'] = p['id']
            data.append(temp)
        db.clsb30_sach_trong_bo.bulk_insert(data)
        return dict(data="SC")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def add_sach_tu_file():
    try:
        bs_id = 3
        data = list()
        with open("/home/temp/3.txt") as f:
            lines = f.readlines()
            for line in lines:
                temp = dict()
                temp['bs_id'] = bs_id
                temp['product_id'] = str(line)
                data.append(temp)
        db.clsb30_sach_trong_bo.bulk_insert(data)
        return dict(data="SC")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def gen_sqlite():
    try:
        bs_id = request.args[0]
        products = list()
        select_product = db(db.clsb_product.id == db.clsb30_sach_trong_bo.product_id) \
            (db.clsb30_sach_trong_bo.bs_id == bs_id) \
            (db.clsb_product.product_status.like("Approved")) \
            (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
            (db.clsb_product.product_creator == db.clsb_dic_creator.id) \
            (db.clsb_product.product_category == db.clsb_category.id).select()
        for product in select_product:
            temp = dict()
            temp['id'] = product[db.clsb_product.id]
            temp['title'] = product[db.clsb_product.product_title]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['publisher'] = product[db.clsb_dic_publisher.publisher_name]
            temp['creator'] = product[db.clsb_dic_creator.creator_name]
            temp['product_price'] = product[db.clsb_product.product_price]
            temp['category_name'] = product[db.clsb_category.category_name]
            temp['category_code'] = product[db.clsb_category.category_code]
            cover_price = db(db.clsb_product_metadata.product_id == temp['id']) \
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                (db.clsb_dic_metadata.metadata_name == 'cover_price').select(
                db.clsb_product_metadata.metadata_value).as_list()
            if cover_price:
                try:
                    temp['cover_price'] = int(cover_price[0]['metadata_value'])
                except Exception as e:
                    print str(e)
            else:
                temp['cover_price'] = 0
            products.append(temp)
        return dict(products=products)
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def zipdir(path, out):
    zipf = zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED)
    for root, dirs, files in os.walk(path):
        for file in files:
            zipf.write(os.path.join(root, file))
    zipf.close()


def add_to_user():
    try:
        bs_id = request.args[0]
        user_id = request.args[1]
        select_product = db(db.clsb30_sach_trong_bo.bs_id == bs_id) \
            (db.clsb30_sach_trong_bo.product_id == db.clsb_product.id).select()
        data_download_archieve = list()
        data_product_history = list()
        data_media_history = list()
        for p in select_product:
            temp_download_archieve = dict()
            temp_download_archieve['user_id'] = user_id
            temp_download_archieve['product_id'] = p['clsb_product']['id']
            temp_download_archieve['price'] = 0
            temp_download_archieve['pay_provider'] = 0
            temp_download_archieve['pay_cp'] = 0
            temp_download_archieve['rom_version'] = "HITEC.WINDOW"
            temp_download_archieve['device_serial'] = ""
            temp_download_archieve['status'] = "Completed"
            data_download_archieve.append(temp_download_archieve)
            select_quiz = db(db.clsb_product.product_code == "Exer" + p['clsb_product']['product_code']).select()
            if len(select_quiz) > 0:
                temp_quiz = dict()
                quiz = select_quiz.first()
                temp_quiz['product_title'] = quiz['product_title']
                temp_quiz['product_price'] = 0
                temp_quiz['product_id'] = quiz['id']
                temp_quiz['category_id'] = quiz['product_category']
                temp_quiz['user_id'] = user_id
                data_product_history.append(temp_quiz)
            temp_media = dict()
            temp_media['product_title'] = p['clsb_product']['product_title']
            temp_media['product_price'] = 0
            temp_media['product_id'] = p['clsb_product']['id']
            temp_media['category_id'] = p['clsb_product']['product_category']
            temp_media['user_id'] = user_id
            data_media_history.append(temp_media)
        db.clsb_download_archieve.bulk_insert(data_download_archieve)
        db.clsb30_product_history.bulk_insert(data_product_history)
        db.clsb30_media_history.bulk_insert(data_media_history)
        return dict(r="SC")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def add_user_xl():
    try:
        bs_id = 8
        select_product = db(db.clsb30_sach_trong_bo.bs_id == bs_id) \
            (db.clsb30_sach_trong_bo.product_id == db.clsb_product.id).select()
        data_product_history = list()
        data_media_history = list()
        for p in select_product:
            for uid in range(127342, 127366):
                temp_history = dict()
                temp_history['product_title'] = p['clsb_product']['product_title']
                temp_history['product_price'] = 0
                temp_history['product_id'] = p['clsb_product']['id']
                temp_history['category_id'] = p['clsb_product']['product_category']
                temp_history['user_id'] = uid
                data_product_history.append(temp_history)
                select_quiz = db(db.clsb_product.product_code == "Exer" + p['clsb_product']['product_code']).select()
                if len(select_quiz) > 0:
                    temp_quiz = dict()
                    quiz = select_quiz.first()
                    temp_quiz['product_title'] = quiz['product_title']
                    temp_quiz['product_price'] = 0
                    temp_quiz['product_id'] = quiz['id']
                    temp_quiz['category_id'] = quiz['product_category']
                    temp_quiz['user_id'] = uid
                    data_product_history.append(temp_quiz)
                temp_media = dict()
                temp_media['product_title'] = p['clsb_product']['product_title']
                temp_media['product_price'] = 0
                temp_media['product_id'] = p['clsb_product']['id']
                temp_media['category_id'] = p['clsb_product']['product_category']
                temp_media['user_id'] = uid
                data_media_history.append(temp_media)
        db.clsb30_product_history.bulk_insert(data_product_history)
        db.clsb30_media_history.bulk_insert(data_media_history)
        return dict(r="SC")
        # return dict(history=data_media_history, media=data_media_history)
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def data():
    try:
        import os
        bs_id = request.args[0]
        serial = request.args[1]
        path = '/home/TEMP_DATA/data/' + bs_id + "/" + serial + ".zip"
        response.headers['Content-Length'] = os.path.getsize(path)
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  serial + '.zip'
        response.headers['X-Sendfile'] = path
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def test_zip():
    try:
        import shutil
        shutil.make_archive('/home/vuongtm/thithu.zip', 'zip', '/home/vuongtm/thithu')
        return dict(r="sc")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
