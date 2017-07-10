# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys


def change_cp():
    try:
        cp_id = 73
        list_id = [4391, 4386, 4384, 4081]
        select_product = db(db.clsb_product.id.belongs(list_id)) \
            (db.clsb20_product_cp.product_code == db.clsb_product.product_code).select()
        for product in select_product:
            old_cp = product[db.clsb20_product_cp.created_by]
            db(db.clsb20_product_cp.id == product[db.clsb20_product_cp.id]).update(created_by=cp_id)
            try:
                product_code = product['product_code']
                copyanything("/home/CBSData/CPData/CP" + str(old_cp) + "/upload/" + product_code + "/thumb.png",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/upload/" + product_code +
                             "/thumb.png", True)
                copyanything("/home/CBSData/CPData/CP" + str(old_cp) + "/upload/" + product_code + "/cover.clsbi",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/upload/" + product_code +
                             "/cover.clsbi", True)
                copyanything(
                    "/home/CBSData/CPData/CP" + str(old_cp) + "/upload/" + product_code + "/" + product_code + ".zip",
                    "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                    "/" + product_code + ".zip", True)
                copyanything(
                    "/home/CBSData/CPData/CP" + str(old_cp) + "/upload/" + product_code + "/" + product_code + ".E.pdf",
                    "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                    "/" + product_code + ".E.pdf", True)
                copyanything("/home/CBSData/CPData/CP" + str(old_cp) + "/upload/" + product_code + "/thumb.png",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                             "/thumb.png", True)
                copyanything("/home/CBSData/CPData/CP" + str(old_cp) + "/upload/" + product_code + "/cover.clsbi",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                             "/cover.clsbi", True)
                copyanything(
                    "/home/CBSData/CPData/CP" + str(old_cp) + "/upload/" + product_code + "/" + product_code + "_json/",
                    "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                    "/" + product_code + "_json/", True)
            except:
                pass

        return "SUCCESS"
    except Exception as ex:
        print(str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def move_cp():
    try:
        cp_id = 73
        list_id = [3635, 3516, 3851, 3390, 3382, 2102]
        select_product = db(db.clsb_product.id.belongs(list_id)).select()
        list_product = list()
        purchased_items = list()
        for product in select_product:
            temp = dict()
            temp['product_code'] = product['product_code']
            temp['product_category'] = product['product_category']
            temp['device_shelf_code'] = product['device_shelf_code']
            # select_creator = db(db.clsb_dic_creator.id == product['product_creator']) \
            #     (db.clsb_dic_creator.creator_name == db.clsb20_dic_creator_cp.creator_name).select()
            # if len(select_creator) > 0:
            #     temp['product_creator'] = select_product.first()[db.clsb20_dic_creator_cp.id]
            # else:
            #     creator_name = db(db.clsb_dic_creator.id == product['product_creator']).select().first()['creator_name']
            #     temp['product_creator'] = db.clsb20_dic_creator_cp.insert(creator_name=creator_name)
            temp['product_publisher'] = product['product_publisher']
            temp['subject_class'] = product['subject_class']
            temp['product_title'] = product['product_title']
            temp['product_description'] = product['product_description']
            temp['product_status'] = 'Published'
            temp['product_price'] = product['product_price']
            temp['data_type'] = product['data_type']
            temp['created_by'] = cp_id
            list_product.append(temp)
            # try:
            #     print("")
            #     # copy_product(product['product_code'], str(cp_id))
            #     product_code = product['product_code']
            #     copyanything("/home/CBSData/" + product_code + "/thumb.png",
            #                  "/home/CBSData/CPData/CP" + str(cp_id) + "/upload/" + product_code +
            #                  "/thumb.png", True)
            #     copyanything("/home/CBSData/" + product_code + "/cover.clsbi",
            #                  "/home/CBSData/CPData/CP" + str(cp_id) + "/upload/" + product_code +
            #                  "/cover.clsbi", True)
            # except:
            #     pass
            temp2 = dict()
            temp2['product_code'] = product['product_code']
            temp2['purchase_item'] = 7
            purchased_items.append(temp2)
        # db.clsb20_product_cp.bulk_insert(list_product)
        db.clsb20_product_purchase_item.bulk_insert(purchased_items)
        # return dict(list_product=len(list_product), ready_product=len(ready_product))
        return "SUCCESS"
    except Exception as ex:
        print(str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def fix_cp_66():
    try:
        cp_id = 66
        select_product = db(db.clsb20_product_cp.created_by == cp_id).select(db.clsb20_product_cp.product_code)
        for product in select_product:
            product_code = product[db.clsb20_product_cp.product_code]
            try:
                copyanything("/home/CBSData/" + product_code + "/" + product_code + ".ZIP",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                             "/" + product_code + ".ZIP", True)
                copyanything("/home/CBSData/" + product_code + "/" + product_code + ".E.pdf",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                             "/" + product_code + ".E.pdf", True)
                copyanything("/home/CBSData/" + product_code + "/thumb.png",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                             "/thumb.png", True)
                copyanything("/home/CBSData/" + product_code + "/cover.clsbi",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                             "/cover.clsbi", True)
                copyanything("/home/CBSData/" + product_code + "/" + product_code + "_json/",
                             "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                             "/" + product_code + "_json/", True)
            except:
                pass
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def copy_product(product_code, cp_id):
    try:
        # product_code = request.args[0]
        # cp_id = request.args[1]
        if not os.path.exists("/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                                      "/" + product_code + ".E.pdf"):
            # if True:
            copyanything("/home/CBSData/" + product_code + "/" + product_code + ".zip",
                         "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                         "/" + product_code + ".zip", True)
            copyanything("/home/CBSData/" + product_code + "/" + product_code + ".E.pdf",
                         "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                         "/" + product_code + ".E.pdf", True)
            copyanything("/home/CBSData/" + product_code + "/thumb.png",
                         "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                         "/thumb.png", True)
            copyanything("/home/CBSData/" + product_code + "/cover.clsbi",
                         "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                         "/cover.clsbi", True)
            copyanything("/home/CBSData/" + product_code + "/" + product_code + "_json/",
                         "/home/CBSData/CPData/CP" + str(cp_id) + "/published/" + product_code +
                         "/" + product_code + "_json/", True)
    except Exception as ex:
        print(str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


import shutil, errno, os


def copyanything(src, dst, ovewrite=False):
    try:
        if not os.path.exists(dst):
            os.makedirs(dst)
        if ovewrite & os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else:
            raise


def add_chuyen_de():
    try:
        parrent = 14
        names = ["Ba đường cônic", "Đường thẳng và mặt phẳng trong không gian", "Khối đa diện và thể tích của chúng",
                 "Mặt cầu mặt trụ mặt nón", "Phương pháp tọa độ trong không gian", "Lượng giác"]
        data = list()
        for idx in range(0, len(names)):
            temp = dict()
            temp['cate_title'] = names[idx]
            temp['cate_parent'] = parrent
            data.append(temp)
        db.clsb30_chuyen_de.bulk_insert(data)
        return dict(result="OK")
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def add_bt_chuyen_de():
    try:
        cate_id = request.args[0]
        import xlrd
        path = "/temp/bt_chuyen_de.xls"
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        data = list()
        for idx in range(0, int(request.args[1])):
            temp = dict()
            temp['chuyen_de'] = cate_id
            temp['exer_title'] = sheet.cell(idx, 0).value
            temp['exer_code'] = sheet.cell(idx, 1).value
            data.append(temp)
        db.clsb30_bt_chuyen_de.bulk_insert(data)
        return dict(data=data)
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def fix_bt_chuyen_de():
    try:
        parent_id = request.args[0]
        select_bt1 = db(db.clsb30_bt_chuyen_de.chuyen_de == parent_id).select()
        select_bt2 = db(db.clsb30_bt_chuyen_de.chuyen_de == db.clsb30_chuyen_de.id) \
            (db.clsb30_chuyen_de.cate_parent == parent_id).select()
        data_chuyen_de = list()
        codes = list()
        for bt in select_bt1:
            temp = dict()
            temp['cate_code'] = bt[db.clsb30_bt_chuyen_de.exer_code]
            temp['cate_title'] = bt[db.clsb30_bt_chuyen_de.exer_title]
            temp['cate_parent'] = bt[db.clsb30_bt_chuyen_de.chuyen_de]
            data_chuyen_de.append(temp)
            codes.append(temp['cate_code'])
        for bt in select_bt2:
            temp = dict()
            temp['cate_code'] = bt[db.clsb30_bt_chuyen_de.exer_code]
            temp['cate_title'] = bt[db.clsb30_bt_chuyen_de.exer_title]
            temp['cate_parent'] = bt[db.clsb30_bt_chuyen_de.chuyen_de]
            data_chuyen_de.append(temp)
            codes.append(temp['cate_code'])
        db.clsb30_chuyen_de.bulk_insert(data_chuyen_de)
        db(db.clsb30_bt_chuyen_de.chuyen_de == parent_id).delete()
        select_cd_child = db(db.clsb30_chuyen_de.cate_parent == parent_id).select()
        children = list()
        for cd in select_cd_child:
            children.append(cd[db.clsb30_chuyen_de.id])
        db(db.clsb30_bt_chuyen_de.chuyen_de.belongs(children)).delete()
        return dict(data="success")
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def add_dap_dan():
    try:
        import xlrd
        path = "/home/vuongtm/toan.xls"
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        data = list()
        for idx in range(0, 19):
            count = int(sheet.cell(idx, 1).value)
            code = sheet.cell(idx, 0).value
            select_cate = db(db.clsb30_chuyen_de.cate_code.like(code)).select()
            if len(select_cate) > 0:
                cate_id = select_cate.first()['id']
                if count < 2:
                    temp = dict()
                    temp['exer_code'] = sheet.cell(idx, 0).value
                    temp['exer_title'] = "Bài tập"
                    temp['chuyen_de'] = cate_id
                    data.append(temp)
                    temp1 = dict()
                    temp1['exer_code'] = str(sheet.cell(idx, 0).value) + "_DA"
                    temp1['exer_title'] = "Đáp án"
                    temp1['chuyen_de'] = cate_id
                    data.append(temp1)
                else:
                    for num in range(1, count + 1):
                        temp = dict()
                        temp['exer_code'] = str(num) + "_" + str(sheet.cell(idx, 0).value)
                        temp['exer_title'] = "Bài tập " + str(num)
                        temp['chuyen_de'] = cate_id
                        data.append(temp)
                        temp1 = dict()
                        temp1['exer_code'] = str(num) + "_" + str(sheet.cell(idx, 0).value) + "_DA"
                        temp1['exer_title'] = "Đáp án " + str(num)
                        temp1['chuyen_de'] = cate_id
                        data.append(temp1)
        db.clsb30_bt_chuyen_de.bulk_insert(data)
        return dict(data="success")
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def read_xls():
    try:
        import xlrd
        path = "/home/vuongtm/bt_chuyen_de.xls"
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        data = list()
        for idx in range(0, 76):
            temp = dict()
            temp['code'] = sheet.cell(idx, 0).value
            temp['count'] = sheet.cell(idx, 1).value
            data.append(temp)
        return dict(data=data)
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


# def import_tqg_card():
#     try:
#         data = list()
#         min = 80000
#         max = 100000
#         path = "/home/ScratchCards.txt"
#         idx = 0
#         with open(path, "r") as f:
#             for line in f:
#                 if idx < max and idx >= min:
#                     split = str(line).split("\t")
#                     temp = dict()
#                     temp['card_serial'] = split[0].strip()
#                     temp['hash_code'] = split[1].strip()
#                     temp['card_value'] = split[2].strip()
#                     data.append(temp)
#                 idx += 1
#         db.clsb30_tqg_card.bulk_insert(data)
#         return dict(data="SC")
#     except Exception as ex:
#         return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def tqg_add_suffix():
    try:
        select_card = db(db.clsb30_gift_code_log.project_code == "T1")\
                (db.clsb30_gift_code_log.code_suffix == db.clsb30_tqg_card.card_value)\
                (db.clsb30_tqg_card.serial_activate == 1).select()
        data = list()
        for card in select_card:
            temp = dict()
            if len(card['clsb30_gift_code_log']['gift_code']) < 16:
                temp['user_id'] = card['clsb30_gift_code_log']['user_id']
                temp['card_serial'] = card['clsb30_tqg_card']['card_serial']
                temp['card_pin'] = card['clsb30_gift_code_log']['gift_code']
                temp['card_value'] = int(card['clsb30_tqg_card']['card_serial'][:4]) * 1000
                # temp['created_on'] = card['created_on']
                data.append(temp)
        db.clsb30_tqg_card_log.bulk_insert(data)
        return dict(sc="SC")
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def export_game_gd():
    try:
        select_product = db(db.clsb_product.product_category == 85)\
            (db.clsb_product.product_status == "Approved")\
            (db.clsb_product.product_publisher == db.clsb_dic_publisher.id)\
            (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.id,
                                                                               db.clsb_product.product_code,
                                                                               db.clsb_product.product_title,
                                                                               db.clsb_dic_publisher.publisher_name,
                                                                               db.clsb_dic_creator.creator_name)
        data = list()
        for product in select_product:
            temp = dict()
            temp['id'] = product[db.clsb_product.id]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['product_title'] = product[db.clsb_product.product_title]
            temp['publisher_name'] = product[db.clsb_dic_publisher.publisher_name]
            temp['creator_name'] = product[db.clsb_dic_creator.creator_name]
            data.append(temp)
        return dict(datas=data)
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def import_bo_sach():
    try:
        bs_id = 9
        import xlrd
        path = "/home/TEMP_DATA/tvcva.xls"
        workbook = xlrd.open_workbook(path)
        sheet = workbook.sheet_by_index(0)
        data = list()
        for idx in range(0, 95):
            temp = dict()
            temp['bs_id'] = bs_id
            temp['product_id'] = sheet.cell(idx, 0).value
            data.append(temp)
        db.clsb30_sach_trong_bo.bulk_insert(data)
        return dict(data="SC")
        # return dict(data=data)
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def import_key_window():
    try:
        data = list()
        with open('/tmp/500key.txt') as f:
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                temp = dict()
                temp['license_key'] = line
                temp['gender'] = 0
                data.append(temp)
        db.cbapp_windows_key_available.bulk_insert(data)
        return dict(data="SC")
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def check_domain():
    return "classbook"


def insert_collection():
    try:
        collection_id = request.args[0]
        cate_id = request.args[1]
        data = list()
        select_product = db(db.clsb_product.product_category == cate_id)\
            (db.clsb_product.product_status == 'Approved').select(db.clsb_product.id)
        for p in select_product:
            temp = dict()
            temp['collection_id'] = collection_id
            temp['product_id'] = p[db.clsb_product.id]
            data.append(temp)
        db.cbcode_product_collection.bulk_insert(data)
        return dict(data='SC')
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def export_with_storage():
    try:
        import os
        data = list()
        select_product = db(db.clsb_product.product_status == 'Approved')\
            (db.clsb_product.product_category == db.clsb_category.id)\
            (db.clsb_category.category_parent == 1).select()
        for p in select_product:
            temp = dict()
            temp['id'] = p[db.clsb_product.id]
            temp['title'] = p[db.clsb_product.product_title]
            temp['code'] = p[db.clsb_product.product_code]
            if os.path.isfile("/home/CBSData/" + temp['code'] + "/" + temp['code'] + ".E.pdf"):
                temp['pdf'] = os.path.getsize("/home/CBSData/" + temp['code'] + "/" + temp['code'] + ".E.pdf")
                temp['zip'] = os.path.getsize("/home/CBSData/" + temp['code'] + "/" + temp['code'] + ".zip")
                data.append(temp)
        return dict(data=data)
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def test_function():
    try:
        from gluon.contrib.memcache import MemcacheClient
        mc = MemcacheClient(['127.0.0.1:11211'], debug=0)

        mc.set("some_key", "Some value")
        value = mc.get("some_key")

        mc.set("another_key", 3)
        mc.delete("another_key")

        mc.set("key", "1")   # note that the key used for incr/decr must be a string.
        mc.incr("key")
        mc.decr("key")
        return dict(result="SC")
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def create_user():
    try:
        utemp = db(db.clsb_user.id == 123272).select().first()
        data = list()
        prefix = "tvxl"
        for idx in range(1, 8):
            temp = dict()
            temp['username'] = prefix + str(idx) + "@edcom.vn"
            temp['email'] = prefix + str(idx) + "@edcom.vn"
            temp['district'] = utemp['district']
            temp['password'] = utemp['password']
            temp['status'] = utemp['status']
            temp['firstName'] = "xl"
            temp['lastName'] = str(idx)
            data.append(temp)
        db.clsb_user.bulk_insert(data)
        return dict(data="SC")
    except Exception as ex:
        return dict(error=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))

