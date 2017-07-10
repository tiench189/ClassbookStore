import sys
import fs.path
import hashlib
from time import gmtime, strftime
from unittest.case import _UnexpectedSuccess
import usercp

DEVICE_NOT_EXIST = CB_0013
ID_NOT_EXIST = CB_0014
PRODUCT_CODE_NOT_EXIST = CB_0015
SUCCES = CB_0000
DB_RQ_FAILD = CB_0003
ERROR_DATA = CB_0007

import shutil

def hash_file(afile):
    blocksize=65536
    md5 = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        md5.update(buf)
        buf = afile.read(blocksize)
    return md5.hexdigest()

def encrypt_test():
    try:
        product_code = request.args[0]
        serial = request.args[1]
        result = encrypt_product_pdf(product_code, serial)
        shutil.copy(settings.home_dir + result['path'], "/home/temp/")
        return dict(result=result)
    except Exception as e:
        print e
        return dict(error=str(e))

def copyLargeFile(src, dest, buffer_size=16000):
    with open(src, 'rb') as fsrc:
        with open(dest, 'wb') as fdest:
            shutil.copyfileobj(fsrc, fdest, buffer_size)

def encrypt_pdf_du_an(code, serial):
    result = dict()
    try:
#        ok = False;
#        for p in sys.path:
#            if p == 'C:\Python27\Lib\site-packages\pdf2dev.zip':
#                ok = True
#        if ok == False :
#            sys.path.append('C:\Python27\Lib\site-packages\pdf2dev.zip') # Add zip file to search path
        import pdf2dev

        check_cp = db(db.clsb_product.product_code.like(code))(db.clsb20_product_cp.product_code.like(code)).select()

        if len(check_cp) > 0:

            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', code)

        elif serial.lower().startswith('ca') or serial.lower().startswith('eh'):  # may cb02 hoac cac may cai dat classbook app:
            # check device_serial, if CB02 or other device -> path = code + prefix "_01"
            path = code + "_01" + "/" + code

        # if not str.startswith(code, 'CP'):
        #     path = code
        # else:
        #     try:
        #         cpid = int(code[2:-17])
        #         path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', code)
        #     except TypeError:
        #         raise HTTP(500, 'Product Code Invalid!')
        try:
            pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]
            if len(pdf_file) == 0:  #TH khong tim thay vien
                path = code
                pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]
        except:
            path = code
            pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]

        pdf_path = settings.home_dir + pdf_file

        result['path'] = pdf_file + '.' + serial

        # if osFileServer.exists(result['path']):
        #     osFileServer.remove(result['path'])
        # pdf2dev.encrypt(serial, pdf_path, pdf_path + '.' + serial)
        if not osFileServer.exists(result['path']):
            pdf2dev.encrypt(serial, pdf_path, pdf_path + '.' + serial)

        result['size'] = osFileServer.getinfo(result['path'])['size']
        result['hash'] = hash_file(osFileServer.open(path=result['path'], mode='rb'))
    except Exception as ex:
        result['error'] = ex
        osFileServer.close()
    return result
def encrypt_product_pdf(code, serial):
    """
        Encryt product's file pdf by product code, device serial.
    """
    result = dict()
    try:
#        ok = False;
#        for p in sys.path:
#            if p == 'C:\Python27\Lib\site-packages\pdf2dev.zip':
#                ok = True
#        if ok == False :
#            sys.path.append('C:\Python27\Lib\site-packages\pdf2dev.zip') # Add zip file to search path
        import pdf2dev

        check_cp = db(db.clsb_product.product_code.like(code))(db.clsb20_product_cp.product_code.like(code)).select()

        if len(check_cp) > 0:

            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', code)

        elif serial.lower().startswith('ca') or serial.lower().startswith('eh'):  # may cb02 hoac cac may cai dat classbook app:
            # check device_serial, if CB02 or other device -> path = code + prefix "_01"
            path = code + "_01" + "/" + code

        # if not str.startswith(code, 'CP'):
        #     path = code
        # else:
        #     try:
        #         cpid = int(code[2:-17])
        #         path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', code)
        #     except TypeError:
        #         raise HTTP(500, 'Product Code Invalid!')
        try:
            pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]
            if len(pdf_file) == 0:  #TH khong tim thay vien
                path = code
                pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]
        except:
            path = code
            pdf_file = osFileServer.listdir(path, '*.E.pdf', True, files_only=True)[0]

        pdf_path = settings.home_dir + pdf_file

        result['path'] = pdf_file + '.' + serial

        # if osFileServer.exists(result['path']):
        #     osFileServer.remove(result['path'])
        # pdf2dev.encrypt(serial, pdf_path, pdf_path + '.' + serial)
        if not osFileServer.exists(result['path']):
            pdf2dev.encrypt(serial, pdf_path, pdf_path + '.' + serial)

        result['size'] = osFileServer.getinfo(result['path'])['size']
        result['hash'] = hash_file(osFileServer.open(path=result['path'], mode='rb'))
    except Exception as ex:
        result['error'] = ex
        osFileServer.close()
    return result


def cover(): #params: product_code
    """
        Service download product's cover.
        (CB_Manager da tra ve device in_use)
    """
    try:
        product_code = request.args(0)
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        import Image

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        else:
            path = fs.path.pathjoin(product_code)

        if len(request.args) == 2 and request.args(1) == "nomedia":
            name_out = "cover.clsbi"
        else:
            name_out = make_cover_media(path, product_code, 'cover', 'clsbi')
        # if (not str.startswith(product_code, 'CP')) & (not str.startswith(product_code, 'ExerCP')):
        #     path = fs.path.pathjoin(request.args(0), 'cover.clsbi')
        # else:
        #     try:
        #         cpid = None
        #         if str.find(product_code, ".") >= 0:
        #             cpid = int(product_code.split('.')[0][2:-3])
        #         elif str.startswith(product_code, 'ExerCP'):
        #             cpid = int(product_code[6:-17])
        #         else:
        #             cpid = int(product_code[2:-17])
        #         path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code, 'cover.clsbi')
        #     except TypeError:
        #         raise HTTP(500, 'Product Code Invalid!')
        response.headers['Content-Length'] = osFileServer.getinfo(fs.path.pathjoin(path, name_out))['size']
        response.headers['Content-Type'] = 'image/png'
        response.headers['Content-Disposition'] = "attachment; filename=cover.png"
        return response.stream(osFileServer.open(path=fs.path.pathjoin(path, name_out), mode='rb'))
    except Exception as ex:
        #raise HTTP(200, str(ex))
        print str("Download cover error: " + str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        try:
            path = "exercise.jpg"
            response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
            response.headers['Content-Type'] = 'image/png'
            response.headers['Content-Disposition'] = "attachment; filename=cover.png"
            return response.stream(osFileServer.open(path = path, mode = 'rb'))
        except Exception as ex:
            redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
def check_has_media(product_code):
    try:
        response.generic_patterns = ['*']
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        import Image

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        else:
            path = fs.path.pathjoin(product_code)
        product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
        if len(product_files) == 0:
            return  dict(check=False)
        else:
            check = check_media_in_zip(fs.path.pathjoin(settings.home_dir, path, product_files[0]), product_code)
            return dict(check=check)

    except Exception as ex:
        print('tiench' + str(ex))
        return dict(check=False)

def check_media():#params: product_code
    try:
        response.generic_patterns = ['*']
        product_code = request.args(0)
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        import Image

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        else:
            path = fs.path.pathjoin(product_code)
        product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
        if len(product_files) == 0:
            return  dict(check=False)
        else:
            check = check_media_in_zip(fs.path.pathjoin(settings.home_dir, path, product_files[0]), product_code)
            return dict(check=check)
    except Exception as ex:
        print('tiench' + str(ex))
        return dict(check=False)

from applications.cba.modules import clsbUltils


def data(): #params: product_code, device_serial, token, oldCBM, ROM_version, store_version
    rom_version = ""
    if not (request.args(5)):
        #adding for old store and CBM old version
        rom_version = "CB.OLD.1.0"
        if check_product_for_old_version(request.args[0]):
            raise HTTP(404, T("Version application is old, need update..."))
    #adding for old store and CMB old version
    else:
        rom_version = request.args[4]

    """
        Service download product's zip file.
        (CB_Manager da tra ve device in_use)
    """
    # check Token
    try:
        user_id = db(db.clsb_device.device_serial.like(request.args(1))).select(db.clsb_device.user_id).first()
        user_id = user_id.user_id
#        d_in_use = db(db.clsb_device.user_id == userID)\
#            (db.clsb_device.in_use == True).select(db.clsb_device.device_serial).as_list()

    except Exception as e:
#        return DEVICE_NOT_EXIST + str(e)
        print e
        raise HTTP(400, T(DEVICE_NOT_EXIST))

    try:

        user = db(db.clsb_user._id == user_id).select(db.clsb_user.username, db.clsb_user.status, db.clsb_user.fund).as_list()


        #return dict(d=username)
        username = user[0]['username']

        userstatus = user[0]['status']
        user_cash = user[0]['fund']
        purchase = db(db.clsb20_product_purchase_item.product_code == request.args(0))\
                (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
                (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type).select()
        purchase_type = ""
        if len(purchase) > 0:
            purchase_type = purchase.first()['clsb20_purchase_item']['description']

        #user is banned
        if not userstatus:
            return dict(error=CB_0009)
#            raise HTTP(400, T(str(CB_0009)))
        res = checkTimeOut(username, request.args(2))
        if res != SUCCES:
#            return res
#             print res
            raise HTTP(400, T(str(res)))

    except Exception as ex:
#        return ID_NOT_EXIST + str(ex)
        raise HTTP(400, T(ID_NOT_EXIST))

    try:

        ####### haha TODEL ###########
        price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']


        ##############################
        ### Add check fund for download
        product_id = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không t?n t?i.
        # remove pay when start download, adding check_for_pay
        oldCBM = False
        if not (request.args(3)):
            oldCBM = True
        new_fund = get_new_fund_for_pay(username, price, oldCBM, product_id)


        if (not new_fund) & (new_fund != 0):
            return dict(error="Error")
        if new_fund < 0:
            return dict(error=CB_0023)

        product_code = request.args(0)
        serial = request.args[1]

        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        elif serial.lower().startswith('ca') or serial.lower().startswith('eh'):  # may cb02 hoac cac may cai dat classbook app:
            product_code_tmp = product_code + "_01/" + product_code
            #path = "./%s" % product_code_tmp
            path = product_code_tmp

        # if (not str.startswith(product_code, 'CP')) & (not str.startswith(product_code, 'ExerCP')):
        #     path = "./%s" % product_code
        # else:
        #     try:
        #         cpid = None
        #         if str.find(product_code, ".") >= 0:
        #             cpid = int(product_code.split('.')[0][2:-3])
        #         elif str.startswith(product_code, 'ExerCP'):
        #             cpid = int(product_code[6:-17])
        #         else:
        #             cpid = int(product_code[2:-17])
        #         path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        #     except TypeError:
        #         raise HTTP(500, 'Product Code Invalid!')
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
        db(db.clsb_product.product_code == request.args(0)).update(total_download=db.clsb_product.total_download+1)


        ##################################
        # Pay truoc khi confirm voi store ban cu
        price = 0
        status = "Inprogress"

        if len(request.args) <= 5:
            price = user_cash - new_fund
            status = "Completed"
            testDevice = False
            #If this is device for test status confirm change to TestSuccess
            except_device = db(db.clsb20_device_exception.device_serial.like(request.args(1))).select()
            if len(except_device) > 0:
                status = 'TestSuccess'
                testDevice = True
            pay_when_confirm(product_code, user_id, price, oldCBM, testDevice)
        ####################################


        params = {'searchTxt': 'ND',
                  'clientIP': request.client,
                  'dserial': request.args(1),
                  'pcode': request.args(0),
                  'purchase_type': purchase_type,
                  'rom_version': rom_version,
                  'userID': user_id,
                  'price': price,
                  'status': status}
#        return userstatus

        # write log
        id_log = 0
        if len(request.args) > 5:
            id_log = log_20(params, True)
        else:
            lr = log(params, True)

        path = fs.path.pathjoin(path, product_files[0])
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-LogID'] = id_log
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
        #return response.stream(osFileServer.open(path=path, mode='rb'))
    except Exception as ex:
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))


def data_json(): #params: product_code, device_serial, token, oldCBM, ROM_version, store_version
    rom_version = ""

    if not (request.args(5)):
        #adding for old store and CBM old version
        rom_version = "CB.OLD.1.0"
        if check_product_for_old_version(request.args[0]):
            raise HTTP(404, T("Version application is old, need update..."))
    #adding for old store and CMB old version
    else:
        rom_version = request.args[4]

    data_json_prefix = request.args(0) + '_json'
    """
        Service download product's json zip file.
        (CB_Manager da tra ve device in_use)
    """
    # check Token
    try:
        user_id = db(db.clsb_device.device_serial.like(request.args(1))).select(db.clsb_device.user_id).first()
        user_id = user_id.user_id

    except Exception as e:
        print e
        raise HTTP(400, T(DEVICE_NOT_EXIST))

    try:
        user = db(db.clsb_user._id == user_id).select(db.clsb_user.username, db.clsb_user.status, db.clsb_user.fund).as_list()

        username = user[0]['username']

        userstatus = user[0]['status']
        user_cash = user[0]['fund']
        purchase = db(db.clsb20_product_purchase_item.product_code == request.args(0))\
                (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
                (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type).select()
        purchase_type = ""
        if len(purchase) > 0:
            purchase_type = purchase.first()['clsb20_purchase_item']['description']

        #user is banned
        if not userstatus:
            return dict(error=CB_0009)
#            raise HTTP(400, T(str(CB_0009)))
        res = checkTimeOut(username, request.args(2))
        if res != SUCCES:
#            return res
#             print res
            raise HTTP(400, T(str(res)))

    except Exception as ex:
#        return ID_NOT_EXIST + str(ex)
        raise HTTP(400, T(ID_NOT_EXIST))

    try:

        ####### haha TODEL ###########
        price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']


        ##############################
        ### Add check fund for download
        product_id = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không t?n t?i.
        # remove pay when start download, adding check_for_pay
        oldCBM = False
        if not (request.args(3)):
            oldCBM = True
        new_fund = get_new_fund_for_pay(username, price, oldCBM, product_id)


        if (not new_fund) & (new_fund != 0):
            return dict(error="Error")
        if new_fund < 0:
            return dict(error=CB_0023)

        product_code = request.args(0)
        serial = request.args[1]

        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        elif serial.lower().startswith('ca') or serial.lower().startswith('eh'):  # may cb02 hoac cac may cai dat classbook app:
            product_code_tmp = product_code + "_01/" + product_code
            #path = "./%s" % product_code_tmp
            path = product_code_tmp

        # if (not str.startswith(product_code, 'CP')) & (not str.startswith(product_code, 'ExerCP')):
        #     path = "./%s" % product_code
        # else:
        #     try:
        #         cpid = None
        #         if str.find(product_code, ".") >= 0:
        #             cpid = int(product_code.split('.')[0][2:-3])
        #         elif str.startswith(product_code, 'ExerCP'):
        #             cpid = int(product_code[6:-17])
        #         else:
        #             cpid = int(product_code[2:-17])
        #         path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        #     except TypeError:
        #         raise HTTP(500, 'Product Code Invalid!')
        try:
            data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if len(data_json_files) == 0:  # khong tim thay file cua version khac
                #path = "./%s" % product_code
                path = product_code
                data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
                if len(data_json_files) == 0:
                    raise Exception("File Not Found")
        except:
            path = "./%s" % product_code
            data_json_files = osFileServer.listdir(path=path, wildcard=data_json_prefix + ".[Zz][Ii][Pp]", files_only=True)
            if len(data_json_files) == 0:
                raise Exception("File Not Found")

        # increament total download to 1
        db(db.clsb_product.product_code == request.args(0)).update(total_download=db.clsb_product.total_download+1)


        ##################################
        # Pay truoc khi confirm voi store ban cu
        #price = 0
        #status = "Inprogress"
        #
        #if len(request.args) <= 5:
        #    price = user_cash - new_fund
        #    status = "Completed"
        #    testDevice = False
        #    #If this is device for test status confirm change to TestSuccess
        #    except_device = db(db.clsb20_device_exception.device_serial.like(request.args(1))).select()
        #    if len(except_device) > 0:
        #        status = 'TestSuccess'
        #        testDevice = True
        #    pay_when_confirm(product_code, user_id, price, oldCBM, testDevice)
        ####################################


        #params = {'searchTxt': 'ND',
        #          'clientIP': request.client,
        #          'dserial': request.args(1),
        #          'pcode': request.args(0),
        #          'purchase_type': purchase_type,
        #          'rom_version': rom_version,
        #          'userID': user_id,
        #          'price': price,
        #          'status': status}
#        return userstatus

        # write log
        #id_log = 0
        #if len(request.args) > 5:
        #    id_log = log_20(params, True)
        #else:
        #    print log(params, True)

        path = fs.path.pathjoin(path, data_json_files[0])

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        response.headers['X-Sendfile'] = settings.home_dir + path
        #return response.stream(osFileServer.open(path=path, mode='rb'))
    except Exception as ex:
        print ex
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))


"""
    Service download product's pdf file. When user download a product, cover service, data service and product service
    are called. But only the last one take care to write user log with the status Inprogress and call payment service.
"""
# TODO: thay device_serial ? request b?ng username, t? ?ó l?y device ín_use và ch? cho phép user download vào máy in_use
#(CB_Manager da tra ve device in_use)
def product(): #params: product_code, device_serial, token, oldCBM, ROM_version, store_version
    '''
        PhuongNH: edit service for multi-version download
        - check device serial
    '''
    rom_version = ""
    if not (request.args(5)): # neu khong co tham so thu 6 (tinh tu 0) tuc la request duoc gui tu cac app cu, chua cap nhat
        #adding for old store and CBM old version
        rom_version = "CB.OLD.1.0"
        if check_product_for_old_version(request.args[0]):
            raise HTTP(404, T("Version application is old, need update..."))
    #adding for old store and CMB old version
    else:
        rom_version = request.args[4]
    try:
        user_id = db(db.clsb_device.device_serial.like(request.args(1))).select(db.clsb_device.user_id).first()
        user_id = user_id.user_id

        # params = {'searchTxt': 'ND',
        #           'clientIP' : request.client,
        #           'dserial': request.args(1),
        #           'pcode': request.args(0),
        #           'userID': user_id,
        #           'status': 'Inprogress',
        #           'price': 0
        #           }
#        d_in_use = db(db.clsb_device.user_id == params['userID'])\
#                    (db.clsb_device.in_use == True).select(db.clsb_device.device_serial).as_list()
    except Exception as ex:
        # return DEVICE_NOT_EXIST
        raise HTTP(400, T(DEVICE_NOT_EXIST))


    try:
        username = db(db.clsb_user._id == user_id).select(db.clsb_user.username, db.clsb_user.fund).as_list()
        old_fund = username[0]['fund']
        username = username[0]['username']
    except Exception as ex:
#         return ID_NOT_EXIST
        raise HTTP(400, T(ID_NOT_EXIST))


    res = checkTimeOut(username, request.args(2))
    if res != SUCCES:
#         return res
        raise HTTP(400, T(str(res)))


    try:

        ####### haha TODEL ###########
        price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']

        ##############################

        product_id = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không t?n t?i.
        # remove pay when start download, adding check_for_pay
        oldCBM = False
        if not (request.args(3)):
            oldCBM = True
        new_fund = get_new_fund_for_pay(username, price, oldCBM, product_id)
        if (not new_fund) & (new_fund != 0):
            return dict(error="Error")
        if new_fund < 0:
            return dict(error=CB_0023)
#         if not (request.args(3)):
#             res = pay(username, price, product_id, True)
#             print 'old download'
#         else:
#             res = pay(username, price, product_id, False)
#             print 'new download'
#         if res != SUCCES:
# #             return res
#             raise HTTP(400, T(str(res)))
        #write log with status Inprogress
        # new_fund = db(db.clsb_user._id == params['userID']).select(db.clsb_user.fund).as_list()[0]['fund']
        # params['price'] = old_fund-new_fund
        # res = log(params, True) #insert log
        # print 'Ket qua ' + res
        #get product_type
        product_category = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_category).as_list()[0]['product_category']
        product_type = db(db.clsb_category.id == product_category).select(db.clsb_category.category_type).as_list()[0]['category_type']
        path = ""
        # product_type is Book or Application
        if product_type == 1 or product_type == 2:
            #encrypt_data = encrypt_product_pdf(request.args(0), d_in_use)
            encrypt_data = encrypt_product_pdf(request.args(0), request.args(1))
            if encrypt_data.has_key('error'):
                raise encrypt_data['error']

            path = encrypt_data['path']
            response.headers['Content-Length'] = encrypt_data['size']
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = "attachment; filename=" + encrypt_data['hash'] + '.pdf'

        elif product_type == 3 or product_type == 4:  # or product_type == 5: #product_type is Exam or Exercise (Quiz)
            product_code = request.args(0)
            check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
            if len(check_cp) > 0:
                cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
                path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published',
                                            product_code, product_code + '.qz')
            else:
                path = fs.path.pathjoin(product_code, product_code + '.qz')
            # if (not str.startswith(product_code, 'CP')) & (not str.startswith(product_code, 'ExerCP')):
            #     path = fs.path.pathjoin(product_code, product_code + '.qz')
            # else:
            #     try:
            #         cpid = None
            #         if str.find(product_code, ".") >= 0:
            #             cpid = int(product_code.split('.')[0][2:-3])
            #         elif str.startswith(product_code, 'ExerCP'):
            #             cpid = int(product_code[6:-17])
            #         else:
            #             cpid = int(product_code[2:-17])
            #         path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published',
            #                                 product_code, product_code + '.qz')
            #     except TypeError:
            #         raise HTTP(500, 'Product Code Invalid!')
            response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                      hash_file(osFileServer.open(path=path, mode='rb')) + '.qz'

        n = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.total_download).as_list()[0]['total_download']
        if not n:
            n = 0
        db(db.clsb_product.product_code == request.args(0)).update(total_download = n + 1)
        response.headers['X-Sendfile'] = settings.home_dir + path
        #return response.stream(osFileServer.open(path = path, mode = 'rb'))
    except Exception as ex:
#         redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
#        print ex.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        return ex
"""
    Confirm when a download is finished. Update user log with status Completed.
"""


def pay_when_confirm(product_code, user_id, price_sub, oldCBM, testDevice):
    try:
        ####### haha TODEL ###########
        price = db(db.clsb_product.product_code == product_code).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']
        """
        adding for cbs20 buy product
        """


        product = db(db.clsb_product.product_code == product_code)(db.clsb_category.id == db.clsb_product.product_category).select().first()
        check_buy = db(db.clsb30_product_history.product_id == product['clsb_product']['id'])(db.clsb30_product_history.user_id == user_id).select()
        if len(check_buy) > 0:
            price = 0
        if check_free_for_classbook(product['clsb_category']['id']):
            price = 0
        else:
            product = db(db.clsb_product.product_code.like(product_code))(db.clsb_category.id == db.clsb_product.product_category).select().first()
            user = db(db.clsb_user.id == user_id).select().first()
            pay_to_log(user, product, True, True)

        #############
        ##############################

        product_id = db(db.clsb_product.product_code == product_code).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(200, T(CB_0001))#Không t?n t?i.


        username = db(db.clsb_user._id == user_id).select(db.clsb_user.username, db.clsb_user.fund).as_list()[0]['username']
        res = None

        res = pay(username, price, product_id, oldCBM)
        if res != SUCCES:
    #       return res
            raise HTTP(200, str(res))
        if not testDevice:
            try:
                resutlt = send_mail_cp_confirm_download(product_code, price_sub)
            except Exception as e:
                print e
                pass
            # if resutlt != "OK":
            #     raise HTTP(200, "Send mail Error: "+str(resutlt['error']))
    except Exception as e:
        print e.message + " on line: "+str(sys.exc_traceback.tb_lineno)
        raise HTTP(200, e.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def confirm():
    """
        # user confirm download --> delete encrypt file downloaded on server
        # product_code, device_serial --> Old apps
        # log_id, store_version, ROM_version, oldCBM --> Store 2.0
    """
    if len(request.args) < 3 & check_product_for_old_version(request.args[0]):
        raise HTTP(200, T("Version application is old, need update..."))
    try:
        if len(request.args) < 3:
            try:
                user_id = db(db.clsb_device.device_serial.like(request.args(1))).select(db.clsb_device.user_id).as_list()
                user_id = user_id[0]['user_id']
            except Exception as ex:
                return DEVICE_NOT_EXIST
            device_serial = request.args[1]
            price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price, db.clsb_product.id).as_list()
            product_id = price[0]['id']
            price = price[0]['product_price']
            product_code = request.args[0]

            # Check and payment for product when download complete

            #remove tam thoi cho CBM va Store cu tru 100% gia tien
            # if not (request.args(4)):
            #     oldCBM = True
        else:
            log_data = db(db.clsb_download_archieve.id == int(request.args[0])).select().first()
            user_id = log_data['user_id']
            device_serial = log_data['device_serial']
            product_id = log_data['product_id']
            price = db(db.clsb_product.id == product_id).select(db.clsb_product.product_price, db.clsb_product.product_code, db.clsb_product.id).as_list()
            product_code = price[0]['product_code']
            price = price[0]['product_price']
    except Exception as e:
        return dict(error=str(e))
    try:
        oldCBM = False
        username = db(db.clsb_user.id == user_id).select()
        old_fund = username[0]['fund']
        username = username[0]['username']
        new_fund = get_new_fund_for_pay(username, price, oldCBM, product_id)
        status = 'Completed'
        testDevice = False
        #If this is device for test status confirm change to TestSuccess
        except_device = db(db.clsb20_device_exception.device_serial.like(device_serial)).select()
        if len(except_device) > 0:
            status = 'TestSuccess'
            testDevice = True

        price_sub = old_fund-new_fund
        if len(request.args) >= 3:
            pay_when_confirm(product_code, user_id, price_sub, oldCBM, testDevice)
        if len(request.args) < 3:
            params = {
                'searchTxt': 'ND',
                'clientIP': request.client,
                'dserial': request.args(1),
                'pcode': request.args(0),
                'userID': user_id,
                'status': status,
                'price': old_fund-new_fund
            }
            # res = log(params, False)
            #confirm roi khong cho phep tru tien confirm lan tiep theo
            # if res != "OK":
            #     return dict(item=SUCCES)
        else:
            params = {
                'searchTxt': 'ND',
                'clientIP': request.client,
                'pcode': product_code,
                'userID': user_id,
                'log_id': int(request.args[0]),
                'status': status,
                'price': old_fund-new_fund
            }
            res = log_20(params, False)
            #confirm roi khong cho phep tru tien confirm lan tiep theo
            if not res:
                return dict(item=SUCCES)

    except Exception as ex:
        print ex
        return ex.message + "On line: "+str(sys.exc_traceback.tb_lineno)
    try:
        path = fs.path.pathjoin(product_code)
        ff = osFileServer.listdir(path)
        for f in ff:
            res = f.find(device_serial)
            if res != -1:
                osFileServer.remove(fs.path.pathjoin(path, f))
        return dict(item=SUCCES)
    except Exception as e:
        return dict(error=str(e))


def rename_cover_media():
    try:
        select_product = db(db.clsb_product.product_status.like("Approved"))\
                (~db.clsb_product.product_code.like("%.%"))\
                (~db.clsb_product.product_code.like("%Exer%")).select(db.clsb_product.product_code)

        for product in select_product:
            folder = product[db.clsb_product.product_code]
            product_code = product[db.clsb_product.product_code]
            #print(product_code)
            check_cp = db(db.clsb_product.product_code.like(product_code))
            check_cp = check_cp(db.clsb20_product_cp.product_code.like(product_code))
            check_cp = check_cp.select(db.clsb20_product_cp.created_by)
            if len(check_cp) > 0:
                cpid = usercp.user_get_id_cp(check_cp.first().created_by, db)
                path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
            else:
                path = fs.path.pathjoin(folder)
            convert_cover_media(path, product_code, 'thumb', 'png')
            convert_cover_media(path, product_code, 'cover', 'clsbi')
    except Exception as ex:
        pass


def thumb(): #product_code
    """
        Service download thumb nail.
    """
#    return URL(c='download', f='thumb', host=True)
#     db.auth_user.created_by.readable = True
    try:
        folder = request.args(0)
        product_code = request.args(0)
        check_cp = db(db.clsb_product.product_code.like(product_code))
        check_cp = check_cp(db.clsb20_product_cp.product_code.like(product_code))
        check_cp = check_cp.select(db.clsb20_product_cp.created_by)
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first().created_by, db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        else:
            path = fs.path.pathjoin(folder)

        if len(request.args) == 2 and request.args(1) == "nomedia":
            name_out = "thumb.png"
        else:
            name_out = make_cover_media(path, product_code, 'thumb', 'png')

        response.headers['Content-Length'] = osFileServer.getinfo(fs.path.pathjoin(path, name_out))['size']
        response.headers['Content-Type'] = 'image'
        response.headers['Content-Disposition'] = "attachment; filename=thumb.png"
        return response.stream(osFileServer.open(path=fs.path.pathjoin(path, name_out), mode = 'rb'))
    except Exception as ex:
        pass
        #return dict(error=str(ex)+" on line: "+str(sys.exc_traceback.tb_lineno))
        try:
            path = "exercise.jpg"
            response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
            response.headers['Content-Type'] = 'image'
            response.headers['Content-Disposition'] = "attachment; filename=thumb.png"
            return response.stream(osFileServer.open(path = path, mode = 'rb'))
        except Exception as ex:
            #return str(ex)
            redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
#        return e


def get_cp_path(product_code):
    pass


def cb_apps(): #args: app_namem, room_version
    """
        Service download classbook app. This is for example a apk file compressed in zip file.
    """
    rom_version = None
#    return URL(c='download', f='thumb', host=True)
    if len(request.args) < 1:
        return CB_0002
    if len(request.args) > 1:
        rom_version = request.args(1)
    FOLDER = "Update"

    if request.args(0) == 'clsBook':
        if rom_version != None:
            rom_version = rom_version.strip()
            if rom_version.startswith('CBT'):

                file_name = request.args(0) + ".sqlite"
                response.headers['Content-Type'] = 'database/sqlite'
            else:
                file_name = request.args(0) + ".sqlite"
                response.headers['Content-Type'] = 'database/sqlite'
        else:
            file_name = request.args(0) + ".sqlite"
            response.headers['Content-Type'] = 'database/sqlite'
    elif request.args(0) == 'FIREWALL':
        if rom_version != None:
            rom_version = rom_version.strip()
            if rom_version.startswith('CBT'):
                file_name = 'cbt.1.zip'
                response.headers['Content-Type'] = 'zip'
            else:
                file_name = 'cb.1.zip'
                response.headers['Content-Type'] = 'zip'
    else:
        file_name = request.args(0) + ".zip"
        response.headers['Content-Type'] = 'application/zip'

    try:
        path = fs.path.pathjoin(FOLDER, file_name)

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Disposition'] = "attachment; filename=" + file_name
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    except Exception as ex:
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))


def cb_ota_apps(): #params: product_code, device_serial, token, oldCBM, ROM_version, store_version
    rom_version = ""
    FOLDER = "OTAUPDATE"
    if not (request.args(5)):
        #adding for old store and CBM old version
        rom_version = "CB.OTA.1.0"
        if (check_product_for_old_version(request.args[0])) and (not check_ota_update(request.args[0])):
            raise HTTP(404, T("Version application is old, need update..."))
        if check_ota_update(request.args[0]):
            try:
                path = fs.path.pathjoin(FOLDER, request.args[0] +".zip")
                response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
                response.headers['Content-Type'] = 'application/zip'
                response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                          hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
                return response.stream(osFileServer.open(path=path, mode='rb'))
            except Exception as e:
                raise HTTP(404, "File not found")
    #adding for old store and CMB old version
    else:
        rom_version = request.args[4]
    """
        Service download product's zip file.
        (CB_Manager da tra ve device in_use)
    """
    # check Token
    try:
        user_id = db(db.clsb_device.device_serial.like(request.args(1))).select(db.clsb_device.user_id).first()

        if str.startswith(request.args(1), "EH"):
           FOLDER = "CB02OTA"
        user_id = user_id.user_id
#        d_in_use = db(db.clsb_device.user_id == userID)\
#            (db.clsb_device.in_use == True).select(db.clsb_device.device_serial).as_list()

    except Exception as e:
#        return DEVICE_NOT_EXIST + str(e)
        print e
        raise HTTP(400, T(DEVICE_NOT_EXIST))

    try:

        user = db(db.clsb_user._id == user_id).select(db.clsb_user.username, db.clsb_user.status, db.clsb_user.fund).as_list()


        #return dict(d=username)
        username = user[0]['username']

        userstatus = user[0]['status']
        user_cash = user[0]['fund']

        purchase = db(db.clsb20_product_purchase_item.product_code == request.args(0))\
                (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
                (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type).select()
        purchase_type = ""
        if len(purchase) > 0:
            purchase_type = purchase.first()['clsb20_purchase_item']['description']

        #user is banned
        if not userstatus:
            return dict(error=CB_0009)
#            raise HTTP(400, T(str(CB_0009)))
        res = checkTimeOut(username, request.args(2))
        if res != SUCCES:
#            return res
#            print res
            raise HTTP(400, T(str(res)))

    except Exception as ex:
       # return ID_NOT_EXIST + str(ex)
        print ex
        raise HTTP(400, T(ID_NOT_EXIST))

    try:

        ####### haha TODEL ###########
        price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price).as_list()
        price = price[0]['product_price']


        ##############################
        ### Add check fund for download
        product_id = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không tồn tại.
        # remove pay when start download, adding check_for_pay
        oldCBM = False
        if not (request.args(3)):
            oldCBM = True
        new_fund = get_new_fund_for_pay(username, price, oldCBM, product_id)
        if (not new_fund) & (new_fund != 0):
            return dict(error="Error")
        if new_fund < 0:
            return dict(error=CB_0023)

        product_code = request.args(0)
        ##################################
        # Pay truoc khi confirm voi store ban cu
        price = 0
        status = "Inprogress"

        if len(request.args) <= 5:
            price = user_cash - new_fund
            status = "Completed"
            testDevice = False
            #If this is device for test status confirm change to TestSuccess
            except_device = db(db.clsb20_device_exception.device_serial.like(request.args(1))).select()
            if len(except_device) > 0:
                status = 'TestSuccess'
                testDevice = True
            pay_when_confirm(product_code, user_id, price, oldCBM, testDevice)
        ####################################
        params = {'searchTxt': 'ND',
                  'clientIP': request.client,
                  'dserial': request.args(1),
                  'pcode': request.args(0),
                  'purchase_type': purchase_type,
                  'rom_version': rom_version,
                  'userID': user_id,
                  'price': price,
                  'status': status}
#        return userstatus


        # write log
        id_log = 0
        if len(request.args) > 5:
            id_log = log_20(params, True)
        else:
            lr = log(params, True)


        path = fs.path.pathjoin(FOLDER, product_code +".zip")
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-LogID'] = id_log
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        return response.stream(osFileServer.open(path=path, mode='rb'))
    except Exception as ex:
        print ex
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))


########################################################
# Remove Functions download OTA old, change and save log
#######################################################
# def cb_ota_apps(): #args: app_namem, room_version
#     """
#         Service download classbook app. This is for example a apk file compressed in zip file.
#     """
#     rom_version = None;
# #    return URL(c='download', f='thumb', host=True)
#     if len(request.args) < 1:
#         return CB_0002
#     if len(request.args) > 1:
#         rom_version = request.args(1)
#         print rom_version
#     FOLDER = "OTAUPDATE"
#
#     file_name = request.args(0) + ".zip"
#     response.headers['Content-Type'] = 'application/zip'
#
#     try:
#         path = fs.path.pathjoin(FOLDER, file_name)
#
#         response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
#         response.headers['Content-Disposition'] = "attachment; filename=" + hash_file(osFileServer.open(path = path, mode = 'rb'))  + '.zip'
#         return response.stream(osFileServer.open(path = path, mode = 'rb'))
#     except Exception as ex:
#         redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))

"""
    Service download Classbook Manager 32 bit.
"""
import os
def manager():
    path = "manager/manager32bit.exe"
    try:
        if request.wsgi['environ']['HTTP_USER_AGENT'].lower().find('wow64') > -1 or request.wsgi['environ']['HTTP_USER_AGENT'].lower().find('win64') > -1 or request.wsgi['environ']['HTTP_USER_AGENT'].lower().find('x64') > -1:
            path = "manager/manager64bit.exe"
    except Exception as ex:
        raise ex
    if osFileServer.exists(path):
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = "attachment; filename=ClassbookManagerSetup.exe"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    else:
        return None

"""
    Service download Classbook Manager 64 bit.
"""
def manager64():
    path = "manager/manager64bit.exe"
    if osFileServer.exists(path):
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = "attachment; filename=manager64bit.exe"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    else:
        return None

"""
    Service download guild to install.
"""
def guide():
    path = "huong_dan_cai_dat.pdf"
    if osFileServer.exists(path):
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=huong_dan_cai_dat.pdf"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    else:
        return None

def helpdoc():
    path = "help.pdf"
    if osFileServer.exists(path):
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=help.pdf"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    else:
        return None

"""
    Service download Classbook driver.
"""
def driver():
    path = "cbdriver.zip"
    if osFileServer.exists(path):
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = "attachment; filename=cbdriver.zip"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    else:
        return None


def driver_intel():
    path = "IntelDriver.rar"
    if osFileServer.exists(path):
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/octet-stream'
        response.headers['Content-Disposition'] = "attachment; filename=cbdriver.zip"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    else:
        return None

def video():
    path = "huongdan.avi"
    if osFileServer.exists(path):
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'video/x-msvideo'
        response.headers['Content-Disposition'] = "attachment; filename=huongdan.avi"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    else:
        return None

# def updated_bookshelf():
#     path = "Update/Bookshelf.zip"
#     if osFileServer.exists(path):
#         response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
#         response.headers['Content-Type'] = 'application/octet-stream'
#         response.headers['Content-Disposition'] = "attachment; filename=bookshelf.zip"
#         return response.stream(osFileServer.open(path = path, mode = 'rb'))
#     else:
#         return None
# 
# def updated_reader():
#     path = "Update/e_reader.zip"
#     if osFileServer.exists(path):
#         response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
#         response.headers['Content-Type'] = 'application/octet-stream'
#         response.headers['Content-Disposition'] = "attachment; filename=reader.zip"
#         return response.stream(osFileServer.open(path = path, mode = 'rb'))
#     else:
#         return None
# 
# def updated_resetbookshelf():
#     path = "Update/resetBookshelf.zip"
#     if osFileServer.exists(path):
#         response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
#         response.headers['Content-Type'] = 'application/octet-stream'
#         response.headers['Content-Disposition'] = "attachment; filename=resetbookshelf.zip"
#         return response.stream(osFileServer.open(path = path, mode = 'rb'))
#     else:
#         return None


def cb_check_ota_apps(): #args: app_namem, room_version
    """
        Service download classbook app. This is for example a apk file compressed in zip file.
    """
    rom_version = None
#    return URL(c='download', f='thumb', host=True)
    if len(request.args) < 1:
        # return CB_0002
        rom_version = "CB.OTA.1.0"
        if check_product_for_old_version(request.args[0]):
            return dict(error='Error')
    if len(request.args) > 1:
        rom_version = request.args(1)
    FOLDER = "OTAUPDATE"

    file_name = request.args(0) + ".zip"
    #response.headers['Content-Type'] = 'application/zip'

    try:
        path = fs.path.pathjoin(FOLDER, file_name)
        path = os.path.join(settings.home_dir, path)
        if not os.path.exists(path):
            return dict(error='Error')
        else:
            return dict(result='Ok')
    except Exception as ex:
        #redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
        print str(ex)
    return dict(error='Error')


def check_payment(): #args: product_code, token, oldCBM, not_classbook_device
    try:
        username = db(db.clsb_user.user_token.like(request.args[1])).select(db.clsb_user.username, db.clsb_user.fund).as_list()
        old_fund = username[0]['fund']
        username = username[0]['username']
    except Exception as ex:
#         return ID_NOT_EXIST
        print ex
        raise HTTP(400, T(ID_NOT_EXIST))
    try:
        ####### haha TODEL ###########
        price = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.product_price).as_list()

        total = price[0]['product_price']

        ##############################

        product_id = db(db.clsb_product.product_code == request.args(0)).select(db.clsb_product.id).as_list()[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không tồn tại.
        oldCBM = False
        if not request.args(2):
            oldCBM = True
        not_classbook_device = False
        if len(request.args) > 3:
            not_classbook_device = True

        new_fund = get_new_fund_for_pay(username, total, oldCBM, product_id, not_classbook_device)
        if (not new_fund) & (new_fund != 0):
            return dict(error="Error")
        fund = old_fund-new_fund

        return dict(price=fund, total=total)
    except Exception as ex:
        print "ERROR"+ex.message+" on line: "+str(sys.exc_traceback.tb_lineno)
        return dict(error="Error: "+ex.message)


def get_new_fund_for_pay(username, total, oldCBM, product_id, not_classbook_device=False):
    try:
        user_cash = db(db.clsb_user.username == username).select(db.clsb_user.fund, db.clsb_user.data_sum).as_list()
        user_cash = user_cash[0]['fund']
        if username == 'testapp2508@gmail.com':
            fo = open("/home/www-data/tmp_log.txt", "w")
            fo.write("param : username" + str(username))
            fo.write("param : total" + str(total))
            fo.write("param : oldCBM" + str(oldCBM))
            fo.write("param : product_id" + str(product_id))
            fo.write("param : not_classbook_device" + str(not_classbook_device))

        """
        adding for cbs20 buy product
        """
        product = db(db.clsb_product.id == product_id)(db.clsb_category.id == db.clsb_product.product_category).select().first()
        #if not not_classbook_device and check_free_for_classbook(product['clsb_category']['id']):
        #    if username == 'testapp2508@gmail.com':
        #        fo.write("param : username" + str(username))
        #    return user_cash
        #############
        user_id = db(db.clsb_user.username == username).select(db.clsb_user.id).as_list()[0]['id']
        if not user_id:
            return False

        check_buy = db(db.clsb30_product_history.product_id == product_id)(db.clsb30_product_history.user_id == user_id).select()
        product = db(db.clsb_product.id == product_id)(
            db.clsb_category.id == db.clsb_product.product_category).select().first()

        if not check_free_for_classbook(product['clsb_category']['id']):
            downloaded = db(db.clsb_download_archieve.product_id == product['clsb_product']['id'])(db.clsb_download_archieve.status.like("Completed"))(db.clsb_download_archieve.user_id == user_id).select()
            if len(downloaded) > 0 or len(check_buy) > 0:
                if username == 'testapp2508@gmail.com':
                    fo.write("sách không free cho classbook và đã từng download")
                return user_cash
        elif len(check_buy) > 0:
            if username == 'testapp2508@gmail.com':
                fo.write("free classbook và đã mua: ")
            return user_cash

        check_buy = db(db.clsb30_product_history.product_id == product_id)(db.clsb30_product_history.user_id == user_id).select()
        if len(check_buy) > 0:
            if username == 'testapp2508@gmail.com':
                fo.write("đã từng mua lần 2")
            return user_cash

        new_fund = user_cash
        query = db(db["clsb_product"].id == product_id)
        query = query(db["clsb20_product_purchase_item"].product_code == db["clsb_product"].product_code)
        query = query(db["clsb20_purchase_item"].id == db["clsb20_product_purchase_item"].purchase_item)
        query = query(db["clsb20_purchase_type"].id == db["clsb20_purchase_item"].purchase_type)
        product_purchases = query.select(
                                        # db["clsb20_product_purchase_item"].discount,
                                        db["clsb20_purchase_type"].name,
                                        # db["clsb20_purchase_type"].name, db["clsb20_purchase_item"].times,
                                        db["clsb20_purchase_item"].duration, db['clsb20_purchase_item'].id)
        if username == 'testapp2508@gmail.com':
            fo.write("db query: " + str(db._lastsql))
        if len(product_purchases) == 0:
            if oldCBM:
                new_fund -= total / 2
            else:
                new_fund -= total
        else:
            from datetime import datetime
            from datetime import timedelta
            product_purchase = product_purchases.first()
            if product_purchase.clsb20_purchase_type.name.upper() != "FREE":
                if product_purchase.clsb20_purchase_type.name.upper() != "NONCONSUMABLE" and product_purchase.clsb20_purchase_type.name.upper() != "SOMEDEVICE":
                    if oldCBM:
                        new_fund -= total / 2
                    else:
                        new_fund -= total
                else:
                    change_time_first = db(db.clsb20_product_price_history.product_id == product_id)\
                            (db.clsb20_product_price_history.purchase_item == product_purchase.clsb20_purchase_item.id).select(orderby=db.clsb20_product_price_history.changing_time)
                    if len(change_time_first) > 0:
                        change_time_first = change_time_first.first()
                        rows = db(db.clsb_download_archieve.user_id == user_id)(db.clsb_download_archieve.product_id == product_id)\
                            (db.clsb_download_archieve.download_time >=  change_time_first.changing_time).select(db.clsb_download_archieve.status)
                        if len(rows) > 0:
                            pass
                        else:
                            if oldCBM:
                                new_fund -= total / 2
                            else:
                                new_fund -= total
                    else:
                        if oldCBM:
                            new_fund -= total / 2
                        else:
                            new_fund -= total
        if username == 'testapp2508@gmail.com':
            fo.close()
        return new_fund
    except Exception as e:
        # return "Get False: " + str(e) + " on line: "+str(sys.exc_traceback.tb_lineno)
        return user_cash


def send_mail_cp_confirm_download(product_code, price):

    try:
        product_info = db(db.clsb_product.product_code == product_code).select().first()
        product_category = db(db.clsb_category.id == product_info['product_category']).select().first()
        price_metadata = db(db.clsb_dic_metadata.metadata_name == 'cover_price').select().first()
        purchase = db(db.clsb20_product_purchase_item.product_code == product_code)\
                (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
                (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type).select()

        if len(purchase) > 0:
            purchase = purchase.first()["clsb20_purchase_type"]["description"]
        else:
            purchase = "Thanh toán cho lần đầu tiên tải về"

        product_price = db((db.clsb_product_metadata.metadata_id == price_metadata['id']) & (db.clsb_product_metadata.product_id == product_info['id'])).select().first()

        cp_path = ""

        #user_info = db(db.clsb_user.id == user_id).select().first()
        product_info = db(db.clsb_product.product_code == product_code).select().first()

        category_info = db(db.clsb_category.id == product_info['product_category'])\
                (db.clsb_product_type.id == db.clsb_category.category_type).select().first()

        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        cp_id = 0
        if len(check_cp) > 0:
            cp_id = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)

        cp_info = db(db.auth_user.id == int(cp_id)).select()

        if len(cp_info) < 1:
            return dict(error="Not CP Info")

        cp_info = cp_info.first()
        cp_email = cp_info['email']
        message = '<html><table border="0" cellpadding="0" cellspacing="0" style="font-size:inherit;font-weight:inherit;font-style:inherit;font-variant:inherit;border-top:0pt none;vertical-align:top;width:600px;margin:30px auto;">  <tbody><tr><td style="font-family:arial, sans-serif;margin:0px;background: #fff; border: 1px solid #e3e3e3; padding: 15px 9px;"><a href="https://www.classbook.vn" target="_blank"><table><tr><td><img style="vertical-align: middle;" height="47" width="200" border="0" src="http://tintuc.classbook.vn/templates/classbook.vn/img/img_logo_classbook.png" class="en-media"></td><td> <img style="vertical-align: middle;" width="300px" height="55px" src="http://tintuc.classbook.vn/images/Classbook_Store.png" /></td></tr></table></a></td></tr>  <tr><td style="height: 10px;"></td>  </tr>  <tr>    <td style="font-family:arial, sans-serif; background: #fff; border: 1px solid #e3e3e3; padding: 15px 9px;"><table border="0" cellpadding="0" cellspacing="10" width="100%" style="font-size:inherit;font-weight:inherit;font-style:inherit;font-variant:inherit;width:100%;"><tbody><tr><td colspan="2" align="left" style="font-family:arial, sans-serif;margin:0px;">' \
              '<span style="color:rgb(255,132,0); font-weight:bold;font-size:16px;">THÔNG BÁO GIAO DỊCH MỚI</span></td></tr>  <tr><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;">' \
              '<p>Xin chào <strong>"'+str(cp_info['first_name'])+' '+str(cp_info['last_name'])+'"</strong>,</p>' \
              ' Sản phẩm  <strong>"'+str(product_info['product_title'])+'"</strong> vừa được tải về.</td>  </tr>     ' \
              '<tr><td style="font-family:arial, sans-serif;margin:0px;">' \
              '<p style="margin-bottom:0px;margin-top:5px;">Thông tin chi tiết giao dịch:</td></tr>    <tr>  <td style="font-family:arial, sans-serif;margin:0px;"><table border="0" cellpadding="0" cellspacing="7" style="font-size:12px;font-weight:inherit; font-style:inherit;font-variant:inherit; vertical-align:top;width:100%;">  <tbody>' \
              '<tr><td style="font-family:arial, sans-serif;margin:0px;text-align:right;width:150px;vertical-align:middle;">' \
              'Mã sản phẩm: </td><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;padding-left:5px;">' \
              '<strong>' + str(product_code) + '</strong></td>  </tr>  ' \
              '<tr><td style="font-family:arial, sans-serif;margin:0px;text-align:right;width:150px;vertical-align:middle;padding-top:5px;">' \
              'Loại: </td><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;padding-left:5px;padding-top:5px;">' \
              '' + str(product_category['category_name']) + '</td>  </tr>' \
              '<tr><td style="font-family:arial, sans-serif;margin:0px;text-align:right;width:150px;vertical-align:middle;padding-top:5px;">' \
              'Giá bán: </td><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;padding-left:5px;padding-top:5px;">' \
              '<strong>' + str(product_info['product_price']) + '</strong> VNĐ</td>  </tr>   <tr><td style="font-family:arial, sans-serif;margin:0px;text-align:right;width:150px;vertical-align:middle;padding-top:5px;">' \
              'Hình thức trả tiền: </td><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;padding-left:5px;padding-top:5px;">' \
              ''+str(purchase)+'</td>  </tr>  <tr><td style="font-family:arial, sans-serif;margin:0px;text-align:right;width:150px;vertical-align:middle;padding-top:5px;">' \
              'Phí tải về cho lần tải này: </td><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;padding-left:5px;padding-top:5px;">' \
              '<strong>' + str(price) + '</strong> VNĐ</td>  </tr>  <tr><td style="font-family:arial, sans-serif;margin:0px;text-align:right;width:150px;vertical-align:middle;padding-top:5px;">' \
              'Chiết khấu phải trả: </td><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;padding-left:5px;padding-top:5px;">' \
              '<strong>' + str(price*usercp.get_discount_value(cp_id, db)/100) + '</strong> VNĐ</td>  </tr>  <tr><td style="font-family:arial, sans-serif;margin:0px;text-align:right;width:150px;vertical-align:middle;padding-top:5px;">' \
              'Thực lĩnh: </td><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;padding-left:5px;padding-top:5px;">' \
              '<strong>' + str(price - price*usercp.get_discount_value(cp_id, db)/100) + '</strong> VNĐ</td>  </tr>  <tr><td style="font-family:arial, sans-serif;margin:0px;text-align:right;width:150px;vertical-align:middle;padding-top:5px;">' \
              'Thời gian tải: </td><td style="font-family:arial, sans-serif;margin:0px;vertical-align:middle;padding-left:5px;padding-top:5px;">' \
              '<strong>' + str(strftime("%d-%m-%Y %H:%M:%S", gmtime())) + '</strong></td>  </tr></tbody></table></td>  </tr>  </tbody></table> </td>  </tr>  ' \
              '<tr><td style="height: 10px;"></td>  </tr>  <tr>    <td style="font-family:arial, sans-serif; font-size: 13px;  background: #fff; border: 1px solid #e3e3e3; padding: 15px 9px;"><div style="width: 620px; display: inline-block;"><b>Nhà xuất bản Giáo Dục Việt Nam - Công ty cổ phần Sách điện tử giáo dục EDC</b><br> <b>Trụ sở chính:</b> 187B Giảng Võ, Đống Đa, Hà Nội <br/>Bán Hàng(ĐT/FAX): 043-512-4007 | Hotline: 0902-138-004 | CSKH: 047-302-0888<br> <b>Miền Nam:</b> Tầng 4F- D1, Toà nhà Mirae Business Center, 268 Tô Hiến Thành, Phường 15, Quận 10, HCM  <br/> Hotline: +84-8-62647968<br> Email: info@edcom.vn</span></div></td>  </tr>  </tbody></table></html>'
        subject = '[CLASSBOOK] THÔNG BÁO GIAO DỊCH MỚI'

        try:
            if price > 0:
                mail.send(to=[cp_email], subject=subject, message=message, bcc=['classbook.root@gmail.com'])
            return CB_0000
        except Exception as e:
            print str(e)
            return dict(error=CB_0006)
    except Exception as e:
        print e
        return dict(error="Send Mail Error: "+e.message)