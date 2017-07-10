# -*- coding: utf-8 -*-
__author__ = 'Tien'
import sys
import fs.path
import hashlib
from time import gmtime, strftime
import usercp
from datetime import date, timedelta, datetime
import json
import myredis


SECRET = "cblib20!^"


def hash_file(afile):
    blocksize=65536
    md5 = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        md5.update(buf)
        buf = afile.read(blocksize)
    return md5.hexdigest()


def get_categories(root):
    try:
        db_query = db(db.clsblib_category.category_type == db.clsb_product_type.id)
        db_query = db_query(db.clsblib_category.category_parent == root['category_id'])
        children = list()

        rows = db_query.select(db.clsblib_category.id,
                                    db.clsblib_category.category_name,
                                    db.clsblib_category.category_code,
                                    db.clsb_product_type.type_name,
                                    db.clsblib_category.category_parent,
                                    db.clsblib_category.category_order,
                                    orderby=~db.clsblib_category.category_order)

        for child in rows:
            temp = dict()
            temp['category_id'] = child.clsblib_category.id
            temp['category_name'] = child.clsblib_category.category_name
            temp['category_code'] = child.clsblib_category.category_code
            temp['category_parent'] = child.clsblib_category.category_parent
            temp['category_type'] = child.clsb_product_type.type_name
            temp['category_order'] = child.clsblib_category.category_order
            temp['buy_package'] = True
            temp = get_categories(temp)
            children.append(temp)
        root['children'] = children
        return root
    except Exception as ex:
        import sys
        print(ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))
        
        
def category_tree():
    try:
        check_cache = myredis.get_cache(HL_CATE_TREE)
        if check_cache['result'] and check_cache['data'] is not None:
            data = json.loads(check_cache['data'])
            data['cache'] = True
            return data
        root = list()
        db_query = db(db.clsblib_category.category_type == db.clsb_product_type.id)
        if request.args:
            root_id = request.args[0]
            db_query = db_query(db.clsblib_category.id == root_id)
        else:
            db_query = db_query(db.clsblib_category.category_parent==None)
        rows = db_query.select(db.clsblib_category.id,
                                db.clsblib_category.category_name,
                                db.clsblib_category.category_order,
                                db.clsblib_category.category_code,
                                db.clsblib_category.category_parent,
                                db.clsb_product_type.type_name,
                                orderby = ~db.clsblib_category.category_order)

        for row in rows:
            temp = dict()
            temp['category_id'] = row.clsblib_category.id
            temp['category_name'] = row.clsblib_category.category_name
            temp['category_order'] = row.clsblib_category.category_order
            temp['category_parent'] = row.clsblib_category.category_parent if row.clsblib_category.category_parent else 0
            temp['category_code'] = row.clsblib_category.category_code
            temp['category_type'] = row.clsb_product_type.type_name
            temp['buy_package'] = True
            temp = get_categories(temp)
            root.append(temp)
        data = dict(categories=root)
        myredis.write_cache(HL_CATE_TREE, str(json.dumps(data)), DEFAULT_TIME)
        data['cache'] = False
        return data
    except Exception as ex:
        import sys
        print(ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def get_product():
    try:
        products = list()
        db_product = list()
        page = 0
        items_per_page = settings.items_per_page
        product_query = db(db.clsb_product.product_status.like('Approved'))
        cat_id = ""
        if request.args:
            cat_id = request.args[0]
            check_child = db(db.clsblib_category.category_parent == cat_id).select()
            if len(check_child) == 0:
                product_query = product_query(db.clsb_product.id == db.clsblib_category_product.product_id)\
                    (db.clsblib_category_product.category_code == db.clsblib_category.category_code)\
                    (db.clsblib_category.id == cat_id)
            else:
                product_query = product_query(db.clsb_product.id == db.clsblib_category_product.product_id)\
                    (db.clsblib_category_product.category_code == db.clsblib_category.category_code)\
                    (db.clsblib_category.category_parent == cat_id)

            #Pagination
            try:
                if len(request.args) > 1: page = int(request.args[1])
                if len(request.args) > 2: items_per_page = int(request.args[2])
                if len(request.args) > 3:
                    version_view = request.args[3]
                    product_query = product_query(db.clsb_product.show_on.like("%" + version_view + "%"))
            except (TypeError, ValueError):
                pass
        else:
            product_query = product_query(db.clsb_product.id > 0)
        check_cache = myredis.get_cache(HL_GET_PRODUCT + cat_id)
        if check_cache['result'] and check_cache['data'] is not None:
            data = json.loads(check_cache['data'])
            data['cache'] = True
            return data

        limitby = (page * items_per_page, (page + 1) * items_per_page)

        total_items = product_query(db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsblib_category.category_type == db.clsb_product_type.id).count()

        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

        db_product = product_query(db.clsb_product.product_creator == db.clsb_dic_creator.id) \
                (db.clsb_product.product_publisher == db.clsb_dic_publisher.id) \
                (db.clsblib_category.category_type == db.clsb_product_type.id) \
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id).select(db.clsb_product.id,
                                                                                      db.clsblib_category.ALL,
                                                                                      db.clsb_product_type.type_name,
                                                                                      db.clsb_dic_creator.creator_name,
                                                                                      db.clsb_dic_publisher.publisher_name,
                                                                                      db.clsb_product.id,
                                                                                      db.clsb_product.product_title,
                                                                                      db.clsb_product.product_code,
                                                                                      db.clsb_product.product_price,
                                                                                      db.clsb_device_shelf.device_shelf_code,
                                                                                      db.clsb_device_shelf.device_shelf_type,
                                                                                      db.clsb_device_shelf.device_shelf_name,
                                                                                      orderby=~db.clsb_product.created_on,
                                                                                      limitby=limitby).as_list()

        if db_product:
            for row in db_product:
                temp = dict()
                temp['id'] = row['clsb_product']['id']
                temp['category_id'] = row['clsblib_category']['id']
                temp['free'] = False
                temp['category_name'] = row['clsblib_category']['category_name']
                temp['category_code'] = row['clsblib_category']['category_code']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_code'] = row['clsb_device_shelf']['device_shelf_code']
                temp['device_self_type'] = row['clsb_device_shelf']['device_shelf_type']
                temp['device_shelf_name'] = row['clsb_device_shelf']['device_shelf_name']

                temp['creator_name'] = row['clsb_dic_creator']['creator_name']
                temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                temp['product_title'] = row['clsb_product']['product_title']
                temp['product_cover'] = "http://classbook.vn/static/covers/" + \
                                        row['clsb_product']['product_code'] + "/thumb.png"
                temp['product_code'] = row['clsb_product']['product_code']
                temp['product_price'] = row['clsb_product']['product_price']
                temp['cover_price'] = 0
                products.append(temp)
        data = dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
                    products=products)
        myredis.write_cache(HL_GET_PRODUCT + cat_id, str(json.dumps(data)), DEFAULT_TIME)
        data['cache'] = False
        return data
    except Exception as ex:
        return dict(type='error', value=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def get_home_topic():
    try:
        # list_cate = [2, 10, 13, 42]
        list_cate = [2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13]
        cates = list()
        select_cate = db(db.clsblib_category.id.belongs(list_cate)).select()
        for row in select_cate:
            temp = dict()
            temp['title'] = row['category_name']
            temp['url'] = URL(a='cbs20', c='cblibrary', f='get_product',
                                            scheme=True, host=True, args=row['id'])
            temp['id'] = row['id']
            cates.append(temp)
        return dict(cates=cates)
    except Exception as ex:
        return dict(type='error', value=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))


def check_data_for_CB02(version):
    isCB02 = True
    try:
        version_list = version.split('.')
        device_w = int(version_list[len(version_list) - 2])
        device_h = int(version_list[len(version_list) - 1])

        divide = int(device_w * 100 / device_h)
        if divide > 65:
            isCB02 = False
        else:
            isCB02 = True
    except Exception as err:
        print(err)
    return isCB02


def encrypt_product_pdf(code, serial, isCB02):
    """
        Encryt product's file pdf by product code, device serial.
    """
    result = dict()
    try:
        #add for demo
        # serial = "CA4504415cac714a"
        import pdf2dev
        data_type = 'pdf'
        #print "vuongtm start  encrypt product pdf " + code
        check_cp = db(db.clsb_product.product_code.like(code))(db.clsb20_product_cp.product_code.like(code)).select()
        data_product = db(db.clsb_product.product_code.like(code)).select()
        data_type = data_product.first()[db.clsb_product.data_type]
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', code)

        elif serial.lower().startswith('ca') or serial.lower().startswith('eh') or serial.lower().startswith('ef'):  # may cb02 hoac cac may cai dat classbook app
            if isCB02:
                product_code_temp = code + "_01/" + code
                path = product_code_temp
            else:
                path = code
            #print "vuongtm 0 path " + path
        # result['path'] = pdf_file
        if data_type == 'epub':
            result['path'] = path + "/" + code + ".epub"
        elif data_type == 'html':
            result['path'] = path + "/" + code + ".html"
        else:
            try:
                pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]
                #print "vuongtm start finding pdf_file=" + pdf_file
                if len(pdf_file) == 0:
                    #print "vuongtm not found pdf_file=" + pdf_file
                    path = code
                    pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]

            except:
                e = sys.exc_info()[0]
                #print "vuongtm exception " + str(e)
                path = code
                pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]

            ##########
            # skip encrypt for test
            pdf_path = settings.home_dir + pdf_file
            result['path'] = pdf_file + '.' + serial
            pdf2dev.encrypt(serial, pdf_path, pdf_path + '.' + serial)
        #     pdf2dev.encrypt(serial, "/home/pylibs/other_device/abc.pdf", pdf_path + '.' + serial)
        #####################
        result['size'] = osFileServer.getinfo(result['path'])['size']
        result['hash'] = hash_file(osFileServer.open(path=result['path'], mode='rb'))
    except Exception as ex:
        #print "vuongtm error 2 "
        print str(ex)
        result['error'] = (str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno))
        osFileServer.close()
    return result


def check_valid_download(token, serial, product_code):
    return dict(result=True, mess="SUCCESS")


def download_pdf(): #params: product_code, device_serial, store_version, token, isDownMedia (gia tri = CLASSBOOKAPP)
    isCB02 = True
    product_code = request.args[0]
    device_serial = request.args[1]
    user_token = request.args[3]
    try:
        version = request.args[2]
        isCB02 = check_data_for_CB02(version)
    except Exception as err:
        print(err)
    try:
        check_valid = check_valid_download(user_token, device_serial, product_code)
        if not check_valid['result']:
            raise HTTP(404, check_valid['mess'])
        encrypt_data = encrypt_product_pdf(product_code, device_serial, isCB02)
        if encrypt_data.has_key('error'):
            raise HTTP(404, "Encrypt: " + encrypt_data['error'])

        path = encrypt_data['path']
        response.headers['Content-Length'] = encrypt_data['size']
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=" + encrypt_data['hash'] + '.pdf'
        response.headers['X-Sendfile'] = settings.home_dir + path
    except Exception as ex:
        raise HTTP(404, "Request false")
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)


def download_data():#params: product_code, device_serial, store_version, token, classbook_app
    product_code = request.args[0]
    serial = request.args[1]
    user_token = request.args[3]
    isCB02 = True
    try:
        version = request.args[2]
        isCB02 = check_data_for_CB02(version)
    except Exception as err:
        print(err)
    check_valid = check_valid_download(user_token, serial, product_code)
    if not check_valid['result']:
        raise HTTP(404, check_valid['mess'])
    try:
        product_category = db(db.clsb_product.product_code == product_code).select(db.clsb_product.product_category).as_list()[0]['product_category']
        product_type = db(db.clsb_category.id == product_category).select(db.clsb_category.category_type).as_list()[0]['category_type']

        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)

        elif serial.lower().startswith('ca') or serial.lower().startswith('eh'):  # may cb02 hoac cac may cai dat classbook app
            if isCB02:
                product_code_temp = product_code + "_01/" + product_code
                path = product_code_temp
            else:
                path = product_code
        try:
            product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
            if len(product_files) == 0:  # khong tim thay file cua version khac
                #path = "./%s" % product_code
                path = product_code
                product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
                if len(product_files) == 0:
                    raise Exception("File Not Found")
        except:
            path = "./%s" % product_code
            product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
            if len(product_files) == 0:
                raise Exception("File Not Found")


        # increament total download to 1
        product_type = db(db.clsb_product.product_code.like(product_code))(db.clsb_product.product_category == db.clsb_category.id)(db.clsb_category.category_type == db.clsb_product_type.id).select().first()
        if product_type['clsb_product_type']['type_name'].upper() == "BOOK" and len(request.args) >= 5:
            path = make_zip_nomedia(path, product_code, product_files[0])
        else:
            path = fs.path.pathjoin(path, product_files[0])

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
    except Exception as ex:
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)


def download_data_json():#params: product_code, device_serial, store_version, token, classbook_app
    product_code = request.args[0]
    data_json_prefix = product_code + '_json'
    serial = request.args[1]
    user_token = request.args[3]
    isCB02 = True
    try:
        version = request.args[2]
        isCB02 = check_data_for_CB02(version)
    except Exception as err:
        print(err)
    check_valid = check_valid_download(user_token, serial, product_code)
    if not check_valid['result']:
        raise HTTP(404, check_valid['mess'])
    try:
        product_category = db(db.clsb_product.product_code == product_code).select(db.clsb_product.product_category).as_list()[0]['product_category']
        product_type = db(db.clsb_category.id == product_category).select(db.clsb_category.category_type).as_list()[0]['category_type']

        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)

        elif serial.lower().startswith('ca') or serial.lower().startswith('eh'):  # may cb02 hoac cac may cai dat classbook app
            if isCB02:
                product_code_temp = product_code + "_01/" + product_code
                path = product_code_temp
            else:
                path = product_code
        try:
            product_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if len(product_files) == 0:  # khong tim thay file cua version khac
                #path = "./%s" % product_code
                path = product_code
                product_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
                if len(product_files) == 0:
                    raise Exception("File Not Found")
        except:
            path = "./%s" % product_code
            product_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if len(product_files) == 0:
                raise Exception("File Not Found")


        # increament total download to 1
        product_type = db(db.clsb_product.product_code.like(product_code))(db.clsb_product.product_category == db.clsb_category.id)(db.clsb_category.category_type == db.clsb_product_type.id).select().first()
        if product_type['clsb_product_type']['type_name'].upper() == "BOOK" and len(request.args) >= 5:
            path = make_zip_nomedia(path, product_code, product_files[0])
        else:
            path = fs.path.pathjoin(path, product_files[0])

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
    except Exception as ex:
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)


def check_valid_sub():
    try:
        user_token = request.vars.user_token
        select_user = db(db.clsb_user.user_token == user_token).select()
        if len(select_user) == 0:
            return dict(result=False, mess="token_not_valid")
        # user_id = select_user.first()['id']
        # select_sub = db(db.clsblib_subscription_status.user_id == user_id).select()
        # if len(select_sub) == 0:
        #     return dict(result=False, mess="sub_not_yet")
        # end = select_sub.first()['end_time']
        # if datetime.now() > end + timedelta(days=7):
        #     return dict(result=False, mess="sub_expire")
        return dict(result=True, mess="Valid")
    except Exception as ex:
        return dict(result=False, mess=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def str2md5(str_root):
    import hashlib
    m = hashlib.md5()
    m.update(str_root)
    return m.hexdigest()


def make_sign(mvars):
    try:
        import collections
        sign = ""
        if mvars and len(mvars) > 0:
            od = collections.OrderedDict(sorted(mvars.items()))
            for k, v in od.iteritems():
                if k != 'signature':
                    sign += v
        sign += SECRET
        current = datetime.now().strftime('%Y%m%d')
        sign += current
        return str2md5(sign)
    except Exception as ex:
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)


def test_sign():
    try:
        sign = make_sign(request.vars)
        return dict(sign=sign)
    except Exception as ex:
        return dict(result=False, mess=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def update_sub():
    try:
        sign = make_sign(request.vars)
        if sign != request.vars.signature:
            return dict(result=False, mess="signature_fail")
        username = request.vars.username
        time_expire = int(request.vars.time_expire)
        select_user = db(db.clsb_user.username == username).select()
        if len(select_user) == 0:
            return dict(result=False, mess="signature_fail")
        user_id = select_user.first()['id']
        time_start = datetime.now()
        time_end = time_start + timedelta(days=time_expire)
        db.clsblib_subscription_log.insert(user_id=user_id, start_time=time_start, end_time=time_end)
        db.clsblib_subscription_status.update_or_insert(db.clsblib_subscription_status.user_id == user_id,
                                                        user_id=user_id,
                                                        start_time=time_start,
                                                        end_time=time_end)
        return dict(result=True, mess="success")
    except Exception as ex:
        return dict(result=False, mess=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def auto_get_relation():
    try:
        limit = 11
        relations = list()
        list_ids = list()
        list_fix_relation = list()
        product_id = request.vars.product_id
        version_app = ""
        if 'version' in request.vars:
            version_app = request.vars.version
        current_product = db(db.clsb_product.id == product_id).select().first()
        select_fix_relation = db(db.clsb_product_relation.product_id == product_id).select()
        for fix in select_fix_relation:
            list_fix_relation.append(fix['relation_id'])

        query = db(db.clsb_product.product_status.like("Approved"))\
                (db.clsb_product.show_on.like('%' + version_app + '%'))\
                (~db.clsb_product.id.belongs(list_fix_relation))\
                (~db.clsb_product.product_code.like("Exer%"))\
                (db.clsb_product.id != product_id)\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id)\
                (db.clsb_product.id == db.clsblib_category_product.product_id)
        if current_product['subject_class'] != 262:
            select_relation = query(db.clsb_product.subject_class == current_product['subject_class'])\
                    (~db.clsb_product.id.belongs(list_ids))\
                    (db.clsb_product.product_category == current_product['product_category']).select(db.clsb_product.id,
                                                                                                     db.clsb_product.product_code,
                                                                                                    db.clsb_product.product_title,
                                                                                                    db.clsb_product.product_price,
                                                                                                    db.clsb_dic_creator.creator_name,
                                                                                                     db.clsb_product.total_download,
                                                                                                     orderby=db.clsb_product.total_download,
                                                                                                     limitby=(0, limit))
            for product in select_relation:
                list_ids.append(product[db.clsb_product.id])
                relations.append(convert2product(product))
            if len(list_ids) < limit:
                select_relation = query(db.clsb_product.subject_class == current_product['subject_class'])\
                        (~db.clsb_product.id.belongs(list_ids)).select(db.clsb_product.id,
                                                                       db.clsb_product.product_code,
                                                                    db.clsb_product.product_title,
                                                                    db.clsb_product.product_price,
                                                                    db.clsb_dic_creator.creator_name,
                                                                    db.clsb_product.total_download,
                                                                    orderby=db.clsb_product.total_download,
                                                                    limitby=(0, limit - len(list_ids)))
                for product in select_relation:
                    list_ids.append(product[db.clsb_product.id])
                    relations.append(convert2product(product))
        if len(list_ids) < limit:
            select_relation = query(db.clsb_product.product_category == current_product['product_category'])\
                        (~db.clsb_product.id.belongs(list_ids)).select(db.clsb_product.id,
                                                                       db.clsb_product.product_code,
                                                                    db.clsb_product.product_title,
                                                                    db.clsb_product.product_price,
                                                                    db.clsb_dic_creator.creator_name,
                                                                    db.clsb_product.total_download,
                                                                    orderby=db.clsb_product.total_download,
                                                                    limitby=(0, limit - len(list_ids)))
            for product in select_relation:
                list_ids.append(product[db.clsb_product.id])
                relations.append(convert2product(product))
        return dict(products=relations)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def convert2product(product):
    temp = dict()
    temp['id'] = product[db.clsb_product.id]
    temp['product_code'] = product[db.clsb_product.product_code]
    temp['product_title'] = product[db.clsb_product.product_title]
    temp['product_price'] = product[db.clsb_product.product_price]
    temp['creator_name'] = product[db.clsb_dic_creator.creator_name]
    temp['cover_price'] = 0
    return temp


def top_new():
    try:
        check_cache = myredis.get_cache(HL_TOP_NEW)
        if check_cache['result'] and check_cache['data'] is not None:
            data = json.loads(check_cache['data'])
            data['cache'] = True
            return data
        qset = db(db.clsb_product.product_category == db.clsb_category.id)
        qset = qset(db.clsb_product.product_creator == db.clsb_dic_creator.id)
        qset = qset(db.clsb_product.product_publisher == db.clsb_dic_publisher.id)
        qset = qset(db.clsb_product.id == db.clsblib_category_product.product_id)

        rows = qset.select(db.clsb_product.id,
                           db.clsb_product.created_on,
                           db.clsb_product.product_category,
                           db.clsb_product.product_title,
                           db.clsb_product.product_code,
                           db.clsb_product.product_price,
                           db.clsb_dic_publisher.publisher_name,
                           db.clsb_category.category_name,
                           db.clsb_category.category_code,
                           db.clsb_dic_creator.creator_name,
                           orderby=~db.clsb_product.created_on, limitby=(0, 12))
        d = list()
        for row in rows:
            temp = dict()
            temp['id'] = row['clsb_product']['id']
            temp['cover_price'] = 0
            temp['product_category'] = row['clsb_product']['product_category']
            temp['created_on'] = str(row['clsb_product']['created_on'])
            temp['creator_name'] = row['clsb_dic_creator']['creator_name']
            temp['product_publisher'] = row['clsb_dic_publisher']['publisher_name']
            temp['product_title'] = row['clsb_product']['product_title']
            temp['product_code'] = row['clsb_product']['product_code']
            temp['product_cover'] = "http://classbook.vn/static/covers/" + \
                                        row['clsb_product']['product_code'] + "/thumb.png"
            temp['product_price'] = row['clsb_product']['product_price']
            temp['category_name'] = row['clsb_category']['category_name']
            temp['category_code'] = row['clsb_category']['category_code']
            temp['category_type'] = "book"
            d.append(temp)
        data = dict(items=d)
        myredis.write_cache(HL_TOP_NEW, str(json.dumps(data)), DEFAULT_TIME)
        data['cache'] = False
        return data
    except Exception as e:
        return dict(error=e.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def toppay():
    try:
        check_cache = myredis.get_cache(HL_TOP_PAY)
        if check_cache['result'] and check_cache['data'] is not None:
            data = json.loads(check_cache['data'])
            data['cache'] = True
            return data
        query = db(db.clsb_download_archieve.product_id == db.clsb_product.id)
        query = query(db.clsb_product.product_creator == db.clsb_dic_creator.id)
        query = query(db.clsb_product.id == db.clsblib_category_product.product_id)
        query = query(db.clsb_product.product_category == db.clsb_category.id)
        import datetime
        from dateutil.relativedelta import relativedelta
        end = datetime.datetime.now()
        start = end - relativedelta(months=2)
        query = query(db.clsb_download_archieve.download_time > start)\
                (db.clsb_download_archieve.download_time < end)\
                (db.clsb_download_archieve.price > 0)
        count = db.clsb_download_archieve.id.count()
        select_product = query.select(db.clsb_product.ALL, count,
                                      db.clsb_dic_creator.creator_name,
                                     groupby=db.clsb_download_archieve.product_id,
                                     orderby=~count,
                                     limitby=(0, 12))
        products = list()
        for row in select_product:
            temp = dict()
            temp['id'] = row['clsb_product']['id']
            temp['cover_price'] = 0
            temp['product_category'] = ""
            temp['creator_name'] = row['clsb_dic_creator']['creator_name']
            temp['product_publisher'] = ""
            temp['product_title'] = row['clsb_product']['product_title']
            temp['product_code'] = row['clsb_product']['product_code']
            temp['product_cover'] = "http://classbook.vn/static/covers/" + \
                                        row['clsb_product']['product_code'] + "/thumb.png"
            temp['product_price'] = row['clsb_product']['product_price']
            temp['category_name'] = ""
            temp['category_code'] = ""
            temp['count'] = row[count]
            temp['category_type'] = "book"
            products.append(temp)
        data = dict(items=products)
        myredis.write_cache(HL_TOP_PAY, str(json.dumps(data)), DEFAULT_TIME)
        data['cache'] = False
        return data
    except Exception as e:
        print (str(e) + " on line " + str(sys.exc_traceback.tb_lineno))
        return str(e) + " on line " + str(sys.exc_traceback.tb_lineno)
