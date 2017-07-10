# -*- coding: utf-8 -*-

__author__ = 'tanbm'


import sys
import fs.path
import hashlib
from time import gmtime, strftime
import usercp

DEVICE_NOT_EXIST = CB_0013
ID_NOT_EXIST = CB_0014
PRODUCT_CODE_NOT_EXIST = CB_0015
SUCCES = CB_0000
DB_RQ_FAILD = CB_0003
ERROR_DATA = CB_0007
VIETSKILL_TOKEN = "e9f112bc88f42efa165d"


def hash_file(afile):
    blocksize=65536
    md5 = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        md5.update(buf)
        buf = afile.read(blocksize)
    return md5.hexdigest()

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
        result['error'] = (str(ex) + str(serial))
        osFileServer.close()
    return result


def product(): #params: product_code, device_serial, store_version, token, isDownMedia (gia tri = CLASSBOOKAPP)
    if not (request.args(3)):
        raise HTTP(404, T("Version application is old, need update..."))
    #adding for old store and CMB old version
    isCB02 = True
    version = ""
    try:
        version = request.args[2]
        if "APPWINDOW" in version:
            # check_win = check_window_download(request.args[1])
            # if not check_win['result']:
            #     raise HTTP(404, T(str(check_win['error'])))
            #     return
            # else:
            #     if check_win['mess'] == 'trial':
            if request.args[0] == 'GK03ENG101':
                download_product(request.args[0], request.args[1], version)
                    # else:
                    #     raise HTTP(404, "Ban dung thu")
                    #     return
        isCB02 = check_data_for_CB02(version)
        # if check_version_mp(version):
        #     download_product(request.args[0], request.args[1], request.args[2])
    except Exception as err:
        print(err)
    try:
        if request.args(3) != VIETSKILL_TOKEN:
            try:
                user_id = db(db.clsb_user.user_token.like(request.args(3))).select().first()
                user_id = user_id['id']
            except Exception as ex:
                raise HTTP(404, T("Token is false"))
            # try:
            #     username = db(db.clsb_user._id == user_id).select(db.clsb_user.username, db.clsb_user.fund).as_list()
            #     old_fund = username[0]['fund']
            #     username = username[0]['username']
            #     purchase = db(db.clsb20_product_purchase_item.product_code == request.args(0))\
            #             (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
            #             (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type).select()
            #     purchase_type = ""
            #     if len(purchase) > 0:
            #         purchase_type = purchase.first()['clsb20_purchase_item']['description']
            # except Exception as ex:
            # #   return ID_NOT_EXIST
            #     raise HTTP(404, T(ID_NOT_EXIST))
            #
            #
            # res = checkTimeOut(username, request.args(3))
            # if res != SUCCES:
            #     raise HTTP(404, T(str(res)))
            # price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price).as_list()
            # price = price[0]['product_price']

            ##############################

            select_product = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id,
                                                                                        db.clsb_product.product_price).first()
            if not select_product:
                raise HTTP(404, T(CB_0001))
            product_id = select_product[db.clsb_product.id]
            price = select_product[db.clsb_product.product_price]
            check_buy = db(db.clsb30_product_history.product_id == product_id)(db.clsb30_product_history.user_id == user_id).select()

            # product = db(db.clsb_product.product_code.like(request.args[0]))(
            #     db.clsb_category.id == db.clsb_product.product_category).select().first()
            # if not check_free_for_classbook(product['clsb_category']['id']):
            #     downloaded = db(db.clsb_download_archieve.status.like("Completed"))\
            #             (db.clsb_download_archieve.product_id == product['clsb_product']['id'])\
            #             (db.clsb_download_archieve.user_id == user_id)\
            #             (db.clsb_download_archieve.price >= price).select()# kiem tra truong hop insert log khong dung
            #     if len(downloaded) <= 0 and len(check_buy) <= 0:
            #         if str(price) != '0':
            #             return dict(error="Bạn chưa mua sách này")
            #         else:
            #             db.clsb30_product_history.insert(product_title=product['clsb_product']['product_title'],
            #                                              product_price=0,
            #                                              product_id=product_id,
            #                                              category_id=product['clsb_category']['id'],
            #                                              user_id=user_id)
            if len(check_buy) <= 0:
                if str(price) != '0':
                    return dict(error="Bạn chưa mua sách này")
                # else:
                #     db.clsb30_product_history.insert(product_title=product['clsb_product']['product_title'],
                #                                      product_price=0,
                #                                      product_id=product_id,
                #                                      category_id=product['clsb_category']['id'],
                #                                      user_id=user_id)

            # product_category = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_category).as_list()[0]['product_category']
            # product_type = db(db.clsb_category.id == product_category).select(db.clsb_category.category_type).as_list()[0]['category_type']
            #print 'Get product type   : ' + str(product_category) + ' --- ' + str(product_type)

        encrypt_data = encrypt_product_pdf(request.args(0), request.args(1), isCB02)
        if encrypt_data.has_key('error'):
            raise HTTP(404, encrypt_data['error'])

        path = encrypt_data['path']
        response.headers['Content-Length'] = encrypt_data['size']
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=" + encrypt_data['hash'] + '.pdf'

        # n = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.total_download).as_list()[0]['total_download']
        # if not n:
        #     n = 0
        # db(db.clsb_product.product_code == request.args(0)).update(total_download=(n + 1))
        response.headers['X-Sendfile'] = settings.home_dir + path
    except Exception as ex:
        raise HTTP(404, "Request false")
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex

def product_test(): #params: product_code, device_serial

    try:
        encrypt_data = encrypt_product_pdf(request.args(0), request.args(1), True)
        if encrypt_data.has_key('error'):
            raise HTTP(404, encrypt_data['error'])

        path = encrypt_data['path']
        response.headers['Content-Length'] = encrypt_data['size']
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=" + encrypt_data['hash'] + '.pdf'

        n = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.total_download).as_list()[0]['total_download']
        if not n:
            n = 0
        db(db.clsb_product.product_code == request.args(0)).update(total_download=(n + 1))
        response.headers['X-Sendfile'] = settings.home_dir + path
    except Exception as ex:
        raise HTTP(404, "Request false")
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex

def android_app():
    redirect("http://rrs.cdn.vnn.vn/cdn/?server=index.php&type=files&method=get&fid=4hjAA8esB9&fname=classbookappss.apk&uid=40")

def data_cdn():
    redirect("http://rrs.cdn.vnn.vn/cdn/?server=index.php&type=files&method=get&foldername=cbsdata&fname=" +\
             str(request.args[0]).lower() + ".zip&uid=40")

def data(): #params: product_code, device_serial, store_version, token, classbook_app
    if not (request.args(3)):
        raise HTTP(404, T("Version application is old, need update..."))
    isCB02 = True
    try:
        version = request.args[2]
        if "APPWINDOW" in version:
            # check_win = check_window_download(request.args[1])
            # if not check_win['result']:
            #     raise HTTP(404, T(str(check_win['error'])))
            #     return
            # else:
            #     if check_win['mess'] == 'trial':
            if request.args[0] == 'GK03ENG101':
                download_data(request.args[0], request.args[1], version)
                    # else:
                    #     raise HTTP(404, "Ban dung thu")
                    #     return
        isCB02 = check_data_for_CB02(version)
        # if check_version_mp(version):
        #     download_data(request.args[0], request.args[1], request.args[2])
    except Exception as err:
        print(err)
    try:
        product_code = request.args(0)
        serial = request.args(1)

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

        if len(request.args) >= 5:
            path = make_zip_nomedia(path, product_code, product_files[0])
        else:
            path = fs.path.pathjoin(path, product_files[0])

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
        #return response.stream(osFileServer.open(path))

    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)

def data_test(): #params: product_code, device_serial, store_version, token, classbook_app
    try:
        product_code = request.args(0)
        serial = request.args(1)

        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)

        elif serial.lower().startswith('ca') or serial.lower().startswith('eh'):  # may cb02 hoac cac may cai dat classbook app
            product_code_temp = product_code + "_01/" + product_code
            path = product_code_temp
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
        path = make_zip_nomedia(path, product_code, product_files[0])
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
        #return response.stream(osFileServer.open(path))

    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)

def data_json(): #params: product_code, device_serial, store_version, token, classbook_app
    if not (request.args(3)):
        raise HTTP(404, T("Version application is old, need update..."))
    isCB02 = True
    try:
        version = request.args[2]
        isCB02 = check_data_for_CB02(version)
        if check_version_mp(version):
            download_data_json(request.args[0], request.args[1], request.args[2])
    except Exception as err:
        print(err)
    data_json_prefix = request.args(0) + '_json.zip'
    #adding for old store and CMB old version
    #try:
    #    user_id = db(db.clsb_device.device_serial.like(request.args(1))).select(db.clsb_device.user_id).first()
    #    user_id = user_id.user_id
    #
    #except Exception as ex:
    #    if check_purchase_somedevice(request.args[0]) is True:
    #        # return DEVICE_NOT_EXIST
    #        raise HTTP(400, T(DEVICE_NOT_EXIST))
    #    else:
    try:
        user_id = db(db.clsb_user.user_token.like(request.args(3))).select().first()
        user_id = user_id['id']
    except Exception as ex:
        raise HTTP(400, T("Token is false"))

    try:
        price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']

        ##############################

        product_code = request.args(0)
        serial = request.args(1)

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
            data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if not os.path.exists(settings.home_dir + path):
                path = product_code
                data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if not os.path.exists(settings.home_dir + path):
                raise HTTP(400, T("FILE NOT FOUND " + str(data_json_files)))
        except:  # TH khong tim thay file cua version khac thi gan lai duong dan cho ban goc
            e = sys.exc_info()[0]
            path = product_code
            data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)

        path = fs.path.pathjoin(path, data_json_prefix)

        #print "vuongtm data() size of zip " + str(path) + " " + str(osFileServer.getinfo(path)['size'])
        #if not os.path.exists(path):
        #    raise HTTP(400, T("FILE NOT FOUND " + path))

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
        #print "vuongtm data() return " + path
        #return response.stream(osFileServer.open(path))

    except Exception as ex:
        raise HTTP(400, T(str(ex)))

def download_data_json(product_code, serial, version):
    data_json_prefix = product_code + '_json.zip'
    #adding for old store and CMB old version
    isCB02 = True
    try:
        isCB02 = check_data_for_CB02(version)
    except Exception as err:
        print(err)
    try:


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
            data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if not os.path.exists(settings.home_dir + path):
                path = product_code
                data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if not os.path.exists(settings.home_dir + path):
                raise Exception("File Not Found")
        except:  # TH khong tim thay file cua version khac thi gan lai duong dan cho ban goc
            e = sys.exc_info()[0]
            path = product_code

        # increament total download to 1

        product_type = db(db.clsb_product.product_code.like(product_code))(db.clsb_product.product_category == db.clsb_category.id)(db.clsb_category.category_type == db.clsb_product_type.id).select().first()
        if product_type['clsb_product_type']['type_name'].upper() == "BOOK" and len(request.args) >= 5:
            path = make_zip_nomedia(path, product_code, data_json_prefix[0])

        else:
            path = fs.path.pathjoin(path, data_json_prefix)
        #print(settings.home_dir + path)
        #print(str(os.path.exists(settings.home_dir + path)))
        #print "vuongtm data() size of zip " + str(path) + " " + str(osFileServer.getinfo(path)['size'])

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
        #print "vuongtm data() return " + path
        #return response.stream(osFileServer.open(path))

    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)

def data_json_preload(): #params: product_code, device_serial

    data_json_prefix = request.args(0) + '_json.zip'
    #adding for old store and CMB old version
    isCB02 = True
    try:
        version = request.args[2]
        isCB02 = check_data_for_CB02(version)
    except Exception as err:
        print(err)
    try:
        product_code = request.args(0)
        serial = request.args(1)

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
            data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if not os.path.exists(settings.home_dir + path):
                path = product_code
                data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if not os.path.exists(settings.home_dir + path):
                raise Exception("File Not Found")
        except:  # TH khong tim thay file cua version khac thi gan lai duong dan cho ban goc
            e = sys.exc_info()[0]
            path = product_code

        # increament total download to 1

        # product_type = db(db.clsb_product.product_code.like(product_code))(db.clsb_product.product_category == db.clsb_category.id)(db.clsb_category.category_type == db.clsb_product_type.id).select().first()
        # if check_version_mp(version):
        #     path = make_zip_nomedia(path, product_code, data_json_prefix[0])
        #
        # else:
        path = fs.path.pathjoin(path, data_json_prefix)
        #print(settings.home_dir + path)
        #print(str(os.path.exists(settings.home_dir + path)))
        #print "vuongtm data() size of zip " + str(path) + " " + str(osFileServer.getinfo(path)['size'])

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
        #print "vuongtm data() return " + path
        #return response.stream(osFileServer.open(path))

    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)

def download_data(product_code, serial, version):
    isCB02 = True
    try:
        isCB02 = check_data_for_CB02(version)
    except Exception as err:
        print(err)
    try:
        price = db(db.clsb_product.product_code == product_code).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']

        ##############################

        product_id = db(db.clsb_product.product_code == product_code).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))

        product = db(db.clsb_product.product_code.like(product_code))(
            db.clsb_category.id == db.clsb_product.product_category).select().first()

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
            if len(product_files) == 0:
                #print "vuongtm data() not found " + path
                path = product_code
                product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
            if len(product_files) == 0:
                raise Exception("File Not Found")
        except:  # TH khong tim thay file cua version khac thi gan lai duong dan cho ban goc
            e = sys.exc_info()[0]
            path = product_code
            product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)


        # increament total download to 1
        db(db.clsb_product.product_code == product_code).update(total_download=db.clsb_product.total_download+1)
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
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)

def data_preload(): #params: product_code, device_serial
    isCB02 = True
    try:
        version = request.args[2]
        isCB02 = check_data_for_CB02(version)
    except Exception as err:
        print(err)
    try:
        price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']

        ##############################

        product_id = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))

        product = db(db.clsb_product.product_code.like(request.args[0]))(
            db.clsb_category.id == db.clsb_product.product_category).select().first()

        product_code = request.args(0)
        serial = request.args(1)

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
            if len(product_files) == 0:
                #print "vuongtm data() not found " + path
                path = product_code
                product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
            if len(product_files) == 0:
                raise Exception("File Not Found")
        except:  # TH khong tim thay file cua version khac thi gan lai duong dan cho ban goc
            e = sys.exc_info()[0]
            path = product_code
            product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)


        # increament total download to 1
        db(db.clsb_product.product_code == request.args(0)).update(total_download=db.clsb_product.total_download+1)
        product_type = db(db.clsb_product.product_code.like(product_code))(db.clsb_product.product_category == db.clsb_category.id)(db.clsb_category.category_type == db.clsb_product_type.id).select().first()
        if len(request.args) >= 5:
            path = make_zip_nomedia(path, product_code, product_files[0])
        else:
            path = fs.path.pathjoin(path, product_files[0])

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path

    except Exception as ex:
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)


def direct_app(): #param: product_code
    try:
        if len(request.args) == 0:
            return 'Không thấy file'
        product_code = request.args[0]
        download_time = request.now
        try:
            db.clsb30_direct.insert(product_code=product_code, download_time=download_time)
        except Exception as err:
            print(err)
        path = product_code + "/" + product_code + ".apk"
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.apk'
        response.headers['X-Sendfile'] = settings.home_dir + path

    except Exception as ex:
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)

def download_app():
    file_name = "ClassbookApp.apk"
    #print(file_name)
    try:
        path = file_name
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/apk'
        response.headers['Content-Disposition'] = "attachment; filename=ClassbookApp.apk"
        response.headers['X-Sendfile'] = settings.home_dir + path

    except Exception as ex:
        return ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)

def download_product(product_code, device_serial, version):
    try:
        isCB02 = True
        try:
            isCB02 = check_data_for_CB02(version)
        except Exception as err:
            print(err)
        product_id = db(db.clsb_product.product_code == product_code).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(404, T(CB_0001))

        product = db(db.clsb_product.product_code.like(product_code))(
            db.clsb_category.id == db.clsb_product.product_category).select().first()

        product_category = db(db.clsb_product.product_code == product_code).select(db.clsb_product.product_category).as_list()[0]['product_category']
        product_type = db(db.clsb_category.id == product_category).select(db.clsb_category.category_type).as_list()[0]['category_type']

        encrypt_data = encrypt_product_pdf(product_code, device_serial, isCB02)
        if encrypt_data.has_key('error'):
            raise HTTP(404, encrypt_data['error'])

        path = encrypt_data['path']
        response.headers['Content-Length'] = encrypt_data['size']
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=" + encrypt_data['hash'] + '.pdf'

        n = db(db.clsb_product.product_code == product_code).select(db.clsb_product.total_download).as_list()[0]['total_download']
        if not n:
            n = 0
        # db(db.clsb_product.product_code == product_code).update(total_download=(n + 1))
        response.headers['X-Sendfile'] = settings.home_dir + path
    except Exception as ex:
        raise HTTP(404, "Request false")
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex

def product_preload(): #params: product_code, device_serial, store_version

    try:
        isCB02 = True
        try:
            version = request.args[2]
            isCB02 = check_data_for_CB02(version)
        except Exception as err:
            print(err)
        product_id = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(404, T(CB_0001))

        product = db(db.clsb_product.product_code.like(request.args[0]))(
            db.clsb_category.id == db.clsb_product.product_category).select().first()

        product_category = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_category).as_list()[0]['product_category']
        product_type = db(db.clsb_category.id == product_category).select(db.clsb_category.category_type).as_list()[0]['category_type']

        encrypt_data = encrypt_product_pdf(request.args(0), request.args(1), isCB02)
        if encrypt_data.has_key('error'):
            raise HTTP(404, encrypt_data['error'])

        path = encrypt_data['path']
        response.headers['Content-Length'] = encrypt_data['size']
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=" + encrypt_data['hash'] + '.pdf'

        n = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.total_download).as_list()[0]['total_download']
        if not n:
            n = 0
        db(db.clsb_product.product_code == request.args(0)).update(total_download=(n + 1))
        response.headers['X-Sendfile'] = settings.home_dir + path
    except Exception as ex:
        raise HTTP(404, "Request false")
        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex

"""
    Confirm when a download is finished. Update user log with status Completed.
"""


def get_new_fund_for_pay_20(username, total, product_id):
    try:
        user_id = db(db.clsb_user.username == username).select(db.clsb_user.id).as_list()[0]['id']
        if not user_id:
            return False
        user_cash = db(db.clsb_user.username == username).select(db.clsb_user.fund, db.clsb_user.data_sum).as_list()
        user_cash = user_cash[0]['fund']
        #print user_cash, total
        # if user_cash < total or user_cash < 0:
        #     return -1
        new_fund = user_cash

        # if not check_free_for_classbook(product())

        query = db(db["clsb_product"].id == product_id)
        query = query(db["clsb20_product_purchase_item"].product_code == db["clsb_product"].product_code)
        query = query(db["clsb20_purchase_item"].id == db["clsb20_product_purchase_item"].purchase_item)
        query = query(db["clsb20_purchase_type"].id == db["clsb20_purchase_item"].purchase_type)
        product_purchases = query.select(
                                        # db["clsb20_product_purchase_item"].discount,
                                        db["clsb20_purchase_type"].name,
                                        # db["clsb20_purchase_type"].name, db["clsb20_purchase_item"].times,
                                        db["clsb20_purchase_item"].duration, db['clsb20_purchase_item'].id)
        if len(product_purchases) == 0:
            rows = db((db.clsb_download_archieve.user_id == user_id) & (db.clsb_download_archieve.product_id == product_id) & (db.clsb_download_archieve.status.like("Completed") | db.clsb_download_archieve.status.like("TestSuccess"))).select(db.clsb_download_archieve.status)
            if len(rows) > 0:
                pass
            else:
                new_fund -= total
        else:
            from datetime import datetime
            from datetime import timedelta
            product_purchase = product_purchases.first()
            if product_purchase.clsb20_purchase_type.name.upper() != "FREE":
                if product_purchase.clsb20_purchase_type.name.upper() != "NONCONSUMABLE" and  product_purchase.clsb20_purchase_type.name.upper() != "SOMEDEVICE":
                    new_fund -= total
                else:
                    change_time_first = db(db.clsb20_product_price_history.product_id == product_id)\
                            (db.clsb20_product_price_history.purchase_item == product_purchase.clsb20_purchase_item.id).select(orderby=db.clsb20_product_price_history.changing_time)
                    if len(change_time_first) > 0:
                        #print "change_time_first"
                        change_time_first = change_time_first.first()
                        rows = db(db.clsb_download_archieve.user_id == user_id)(db.clsb_download_archieve.product_id == product_id)\
                            (db.clsb_download_archieve.download_time >=  change_time_first.changing_time).select(db.clsb_download_archieve.status)
                        if len(rows) > 0:
                            pass
                        else:
                            new_fund -= total
                    else:
                        rows = db((db.clsb_download_archieve.user_id == user_id) & (db.clsb_download_archieve.product_id == product_id) & (db.clsb_download_archieve.status.like("Completed") | db.clsb_download_archieve.status.like("TestSuccess"))).select(db.clsb_download_archieve.status)
                        if len(rows) > 0:
                            pass
                        else:
                            new_fund -= total
        #print "New fund: "+str(new_fund)
        return new_fund
    except Exception as e:
        print "Get False: " + str(e) + " on line: "+str(sys.exc_traceback.tb_lineno)
        return False


def check_purchase_somedevice(product_code):
    query = db(db["clsb_product"].product_code == product_code)
    query = query(db["clsb20_product_purchase_item"].product_code == db["clsb_product"].product_code)
    query = query(db["clsb20_purchase_item"].id == db["clsb20_product_purchase_item"].purchase_item)
    query = query(db["clsb20_purchase_type"].id == db["clsb20_purchase_item"].purchase_type)
    product_purchases = query.select(db["clsb20_purchase_type"].name, db["clsb20_purchase_item"].duration, db['clsb20_purchase_item'].id)
    if len(product_purchases) == 0:
        return True
    product_purchase = product_purchases.first()
    if product_purchase.clsb20_purchase_type.name.upper() != "SOMEDEVICE":
        return True

    return False


def build():
    import os
    import zipfile

    msg = "<h1>Encrypt Start</h1>"
    msg += "<h5>####################</h5>"
    devices = request.args
    dir_home = "/home/DataSX/IN"
    for device in devices:
        for f in os.listdir(dir_home):
            code = f.replace(".E.pdf", "")
            result = encrypt_product_pdf_for_build(dir_home + "/" + f, code, device)
            msg += "<br/>["+device+"]"+str(code)+":"+str(result)

        input_path = '/home/DataSX/OUT/' + device
        output_path = "/home/www-data/web2py/applications/cbs20/static/%s.zip" % device
        output_zip = zipfile.ZipFile(output_path, "w", compression=zipfile.ZIP_DEFLATED)
        rootlen = len(input_path) + 1
        for dirname, subdirs, files in os.walk(input_path):
            for file in files:
                fn = os.path.join(dirname, file)
                output_zip.write(fn, fn[rootlen:])
        output_zip.close()
        dl_link = URL('static', '%s.zip' % device)
        msg += '<br/>[%s]Link Download: <a href="%s">%s</a>' % (device, dl_link, '%s.zip' % device)
    msg += "<h5>####################</h5>"
    msg += "<h1>Encrypt End</h1>"
    return dict(result=XML(msg))


def encrypt_product_pdf_for_build(path, code, serial):
    try:
        home_path = "/home/DataSX/OUT/"+serial
        create_dir(home_path)
        create_dir(home_path + "/" + code)
        import pdf2dev
        pdf2dev.encrypt(serial, path, home_path + "/" + code + "/" + code + ".pdf")
    except Exception as ex:
        return ex.message + str(sys.exc_traceback.tb_lineno)
    return "OK"


def create_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)



def test_download():
    response.headers['Content-Length'] = osFileServer.getinfo("06GKDIALI_01/06GKDIALI/06GKDIALI.zip")['size']
    response.headers['Content-Type'] = 'application/zip'
    response.headers['Content-Disposition'] = "attachment; filename=06GKDIALI.zip"
    # response.headers['X-Sendfile'] = settings.home_dir + "SBT11BTTNGA_new_update.zip"
    return response.stream(osFileServer.open("06GKDIALI_01/06GKDIALI/06GKDIALI.zip"))


#args : device_serial, product_code, status, token
def confirm_download():

    #if request.vars or len(request.args) != 4:
    #    return dict(error="Sai thông số.")

    device_serial = request.args[0]
    product_code = request.args[1]
    if request.args[2] == "user_download_complete":
        status = 'Completed'
    else:
        status = 'False'
    token = request.args[3]

    prefix_version = "_01"

    # check token:
    item = db(db.clsb_user.user_token == token).select(db.clsb_user.id).as_list()

    if len(item) == 0:
        return dict(error="Sai token")
    is_delete = False
    try:
        params = {'searchTxt': 'ND',
                  'clientIP': '',
                  'dserial': device_serial,
                  'pcode': product_code,
                  'purchase_type': '',
                  'rom_version': "CLASSBOOK.APP",
                  'userID': item[0]['id'],
                  'price': 0,
                  'status': status}
        log_20(params, True)
        try:
            path = fs.path.pathjoin(product_code)
            ff = osFileServer.listdir(path)
            for f in ff:
                res = f.find(device_serial)
                if res != -1:
                    osFileServer.remove(fs.path.pathjoin(path, f))
                    is_delete = True
                    break
            if not is_delete:
                product_code += prefix_version
                path = fs.path.pathjoin(product_code)
                ff = osFileServer.listdir(path)
                for f in ff:
                    res = f.find(device_serial)
                    if res != -1:
                        osFileServer.remove(fs.path.pathjoin(path, f))
                        break
        except Exception as err:
            print(err)
        return dict(item=SUCCES)
    except Exception as e:
        return dict(error=str(e) + " on line: "+str(sys.exc_traceback.tb_lineno))

def free_apk(): #product_id, user_id
    import zipfile
    try:
        if request.args and len(request.args) >= 2:
            product_id = request.args[0]
            user_id = request.args[1]
            product = db(db.clsb_product.id == product_id).select()
            if len(product) == 0:
                return dict(error="Sản phẩm không tồn tại")
            product = product.first()
            product_code = product['product_code']
            product_title = product['product_title']
            product_title = remove_viet_accents(product_title)
            #print (product_title)
            check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
            # return check_cp
            if len(check_cp) > 0:
                cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
                home_path = settings.home_dir + fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published')
                dir_path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
            else:
                home_path = settings.home_dir
                dir_path = product_code
            path = dir_path + "/" + product_code + ".apk"
            # return dict(path=settings.home_dir + path)
            if not os.path.exists(settings.home_dir + path):
                fh = open(settings.home_dir + dir_path + "/" + product_code + ".zip")
                zfile = zipfile.ZipFile(fh)
                for name in zfile.namelist():
                    (dirName, fileName) = os.path.split(name)
                    if fileName == '':
                        # directory
                        newDir = home_path + '/' + dirName
                        if not os.path.exists(newDir):
                            os.mkdir(newDir)
                    else:
                        # file
                        fd = open(home_path + '/' + name, 'w+')
                        fd.write(zfile.read(name))
                        fd.close()
                zfile.close()
            db.clsb_download_archieve.insert(user_id=user_id,
                        product_id=product_id,
                        price=0,
                        download_time=request.now,
                        rom_version="WEB",
                        device_serial="WEB",
                        status="WEB_COMPLETE")
            # return dict(path=settings.home_dir + path)
            response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
            response.headers['Content-Type'] = 'application/zip'
            response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                      product_title + '.apk'
            #print(settings.home_dir + path)
            response.headers['X-Sendfile'] = settings.home_dir + path
            # return response.stream(settings.home_dir + path)
    except Exception as err:
        return dict(error=str(err)+ " on line: "+str(sys.exc_traceback.tb_lineno))

def check_free_cp():#product_code
    free_cp = [35]
    try:
        if request.args:
            product_code = request.args[0]
            check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
            if len(check_cp) > 0:
                cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
                if cpid in free_cp:
                    return dict(result=True)
                else:
                    return dict(result=False)
            else:
                return dict(result=True)
    except Exception as err:
        return dict(result=False)

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

def download_mspdict():
    try:
        import os
        file_path = "/home/www-data/web2py/applications/cbw/static/mspdict/mspdict.zip"
        response.headers['Content-Length'] = os.path.getsize(file_path)
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=mspdict.zip"
        response.headers['X-Sendfile'] = file_path
    except Exception as err:
        return dict(error=str(err))


def check_window_download(device_serial):
    try:
        cb_license = db(db.cbapp_windows_activated_key.device_serial == device_serial).select()
        if len(cb_license) == 0:
            return dict(result=False, error="Chua dang ki")
        else:
            license_key = cb_license.first()
            key = license_key['license_key']
            if key is None:
                return dict(result=False, error="Ban dung thu")
            elif key.startswith("0000-0000"):
                return dict(result=True, mess="trial")
            else:
                return dict(result=True, mess="normal")
    except Exception as err:
        return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))


def install(): #param: product_code
    import os
    try:
        if len(request.args) == 0:
            return 'Không thấy file'
        file_type = request.args[0]
        if file_type == 'android':
            path = "/home/file/ClassbookWS.apk"
            filename = "Classbook.apk"
        else:
            return 'Không thấy file'
        response.headers['Content-Length'] = os.path.getsize(path)
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  filename
        response.headers['X-Sendfile'] = path

    except Exception as ex:
        return ex.message


def test_xsend_file():
    import os
    try:
        product_code = request.args[0]
        path = settings.home_dir + product_code + "/" + product_code + ".zip"
        response.headers['Content-Length'] = os.path.getsize(path)
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  product_code + ".zip"
        response.headers['X-Sendfile'] = path
    except Exception as err:
        return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
