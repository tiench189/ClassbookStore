__author__ = 'TienCH'
import xlrd
import sys
import os


HOME_DIR = "/home/CBSData/"
CP_DIR = "CPData/"


def import_product():
    try:
        bs_id = request.args[0]
        path = "/home/TEMP_DATA/importfile/products/" + bs_id + ".xls"
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        data = list()
        for idx in range(sheet.nrows):
            temp = dict()
            temp['bs_id'] = bs_id
            temp['product_id'] = sheet.cell(idx, 0).value
            data.append(temp)
        db.clsb30_sach_trong_bo.bulk_insert(data)
        return dict(data="SC")
        # return dict(data=data)
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


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


def create_dir(path):
    try:
        if not os.path.exists(path):
            os.makedirs(path)
        return True
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def write_text_file(path, content):
    try:
        with open(path, "w") as text_file:
            text_file.write(content)
        return dict(content=content)
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


def put_product_category():
    try:
        bs_id = request.args[0]
        cate_id = request.args[1]
        select_product = db(db.clsb_product.product_category == cate_id).select(db.clsb_product.id)
        data = list()
        for product in select_product:
            temp = dict()
            temp['bs_id'] = bs_id
            temp['product_id'] = product[db.clsb_product.id]
            data.append(temp)
        db.clsb30_sach_trong_bo.bulk_insert(data)
        return dict(data="SC")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def add_to_user():
    try:
        bs_id = request.args[0]
        user_id = request.args[1]
        select_product = db(db.clsb30_sach_trong_bo.bs_id == bs_id) \
            (db.clsb30_sach_trong_bo.product_id == db.clsb_product.id).select()
        data_product_history = list()
        data_media_history = list()
        for p in select_product:
            temp_media = dict()
            temp_media['product_title'] = p['clsb_product']['product_title']
            temp_media['product_price'] = 0
            temp_media['product_id'] = p['clsb_product']['id']
            temp_media['category_id'] = p['clsb_product']['product_category']
            temp_media['user_id'] = user_id
            data_media_history.append(temp_media)
            data_product_history.append(temp_media)
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
        db.clsb30_product_history.bulk_insert(data_product_history)
        db.clsb30_media_history.bulk_insert(data_media_history)
        return dict(r="SC")
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
