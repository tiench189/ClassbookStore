# -*- coding: utf-8 -*-
__author__ = 'manhtd'
import zipfile
import fs.path
from pyPdf import PdfFileReader
import sys
import re
import os


def check_missing_db():
    datas = osFileServer.listdir(dirs_only=True)
    products = db(db.clsb_product.id > 0).select(db.clsb_product.product_code)
    for product in products:
        if product.product_code in datas:
            datas.remove(product.product_code)
    datas.remove(".cache")
    datas.remove("fw")
    datas.remove("CB_STORE_IMAGES")
    datas.remove("Test")
    datas.remove("Violet")
    datas.remove("Update")
    datas.remove("manager")
    datas.remove("CB_STORE_BANNER")
    datas.remove("missing")
    for data in datas:
        import fs.errors
        try:
            print("")
            #osFileServer.copy(data + '/' + data + '.zip.bk', 'missing/' + data + '.zip', overwrite=True)
            #osFileServer.removedir(data, force=True)
            #print "copied " + data
        except fs.errors.ResourceNotFoundError as ex:
            print str(ex)
    #print "Missing Count: " + str(len(datas))
    return dict(data=datas)


def copy_missing():
    datas = osFileServer.listdir(path='missing', files_only=True)
    for data in datas:
        #osFileServer.copy('missing/' + data, data, overwrite=True)
        #print 'copied ' + data
        print("")
    return dict()


def makethumb(product_code):
    """
        product_code, example: VHNT01
    """
    from PIL import Image
    thumb_x = 100
    thumb_y = 143
    size = (thumb_x, thumb_y)

    path = os.path.join(settings.home_dir, product_code)
    cover = os.path.join(settings.home_dir, fs.path.pathjoin(product_code, 'cover.clsbi'))
    try:
        im = Image.open(cover)
        thumb = im.copy()
        thumb.thumbnail(size, Image.ANTIALIAS)
        thumb.save(os.path.join(path, 'thumb.png'))
    except:
        osFileServer.copy(fs.path.pathjoin(product_code, 'cover.clsbi'),
                          fs.path.pathjoin(product_code, 'thumb.png'), True)
    return path


def search_zip_file(code):
    files = osFileServer.listdir(wildcard=code + ".[Zz][Ii][Pp]", files_only=True)
    if len(files) == 0:
        return None
    return files[0]


def is_encrypted(path):
#     return PdfFileReader(file(path, 'rb')).isEncrypted
    return PdfFileReader(osFileServer.open(path, 'rb')).isEncrypted


def validate_data(code):
    have_e_pdf = False
    have_cover = False
    have_config = False
    have_zip = False

    if code == "cbdriver" or code.find("new_update") >= 0:
        return "Error: file not valid!"

    zip_file = search_zip_file(code)
    if zip_file is None:
        return "Error: cannot find zip file"

    z = None
    try:
        z = zipfile.ZipFile(osFileServer.open(zip_file, 'rb'))
        for name in z.namelist():
            if name.endswith('.E.pdf'):
                have_e_pdf = True
            if name.find('cover.clsbi') >= 0:
                have_cover = True
            if name.find('config.xml') >= 0:
                have_config = True
            if bool(re.search(".[Zz][Ii][Pp]$", name)):
                have_zip = True
        z.close()
    except Exception as ex:
        errors = list()
        errors.append("Error: " + str(ex))
        if z:
            z.close()
        return errors

    if not have_e_pdf or not have_cover or not have_config or not have_zip:
        errors = list()
        errors.append(" have_e_pdf = " + str(have_e_pdf) + " | ")
        errors.append(" have_cover = " + str(have_cover) + " | ")
        errors.append(" have_config = " + str(have_config) + " | ")
        errors.append(" have_zip = " + str(have_zip))
        return errors
    else:
        return "OK"


def extract_product_data(code):
    #print "Start function extract"
    zip_file = search_zip_file(code)
    if zip_file is None:
        return "Error: Cannot find zip file."

    result = validate_data(code)
    if "OK" not in result:
        return result

    zip_path = fs.path.pathjoin(code, zip_file)[:-3] + "zip"

    z = None
    zout = None
    result = "OK"
    try:
        osFileServer.makedir(code, True, True)
        z = zipfile.ZipFile(osFileServer.open(zip_file, 'rb'))
        zout = zipfile.ZipFile(osFileServer.open(zip_path, 'wb+'), mode="w")
        for name in z.namelist():
            if name.endswith('.E.pdf'):
                osFileServer.setcontents(fs.path.pathjoin(code, fs.path.basename(name)), z.read(name))
                pdf_path = fs.path.pathjoin(code, code + ".E.pdf")
                if not is_encrypted(pdf_path):
                    result = "Error: pdf file isn\'t encrypted!"
                    osFileServer.removedir(fs.path.pathjoin(code), True, True)
                    raise Exception(result)
            else:
                buffer_data = z.read(name)
                zout.writestr(name, buffer_data)
                if name.find('cover.clsbi') >= 0:
                    osFileServer.setcontents(fs.path.pathjoin(code, "cover.clsbi"), buffer_data)
        zout.close()
        z.close()
        makethumb(code)
        osFileServer.move(zip_file, zip_path + ".bk", True)
    except Exception as ex:
        if z:
            z.close()
        if zout:
            zout.close()
        result = "Extract Error:" + str(ex.message) + " on line" + str(sys.exc_traceback.tb_lineno)
    if osFileServer:
        osFileServer.close()
    return result


def insert_datas():
    #zip_list = osFileServer.listdir(wildcard='*.[Zz][Ii][Pp]', files_only=True)
    #for zip_file in zip_list:
    #    product_code = zip_file[:-4]
    #
    #    if product_code == "cbdriver" or product_code.find("new_update") >= 0:
    #        print "Error: %s file not valid!" % product_code
    #        continue
    #
    #    print "Start insert product code: " + product_code
    #    try:
    #        pid = db['clsb_product'].insert(product_category=1, product_creator=180, product_publisher=1,
    #                                        product_description='', product_code=product_code,
    #                                        total_download=0, product_price=0, device_shelf_code=14, rating_count=0,
    #                                        product_cover='http://classbook.vn/cbs/download/cover/%s' % product_code,
    #                                        product_data='http://classbook.vn/cbs/download/data/%s' % product_code,
    #                                        product_pdf='http://classbook.vn/cbs/download/product/%s' % product_code,
    #                                        product_rating=0, subject_class=15, product_title=product_code)
    #        print "Insert ok id: " + str(pid)
    #    except Exception as ex:
    #        print "Error on insert: " + str(ex)
    #    print product_code
    #    print "Extract Result: " + str(extract_product_data(product_code))
    #    print ""
    #    print "-------------"
    #    print ""
    return dict(OK="OK")


def update_datas():
    #db(db.clsb_product.id > 1386).update(product_creator=51, product_publisher=8)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT01')).update(device_shelf_code=20)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT02')).update(device_shelf_code=3)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT03')).update(device_shelf_code=4)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT04')).update(device_shelf_code=5)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT05')).update(device_shelf_code=6)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT06')).update(device_shelf_code=7)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT07')).update(device_shelf_code=8)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT08')).update(device_shelf_code=9)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT09')).update(device_shelf_code=10)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT10')).update(device_shelf_code=11)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT11')).update(device_shelf_code=12)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('SBT12')).update(device_shelf_code=13)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK00')).update(device_shelf_code=18)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK01')).update(device_shelf_code=20)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK02')).update(device_shelf_code=3)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK03')).update(device_shelf_code=4)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK04')).update(device_shelf_code=5)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK05')).update(device_shelf_code=6)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK06')).update(device_shelf_code=7)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK07')).update(device_shelf_code=8)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK08')).update(device_shelf_code=9)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK09')).update(device_shelf_code=10)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK10')).update(device_shelf_code=11)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK11')).update(device_shelf_code=12)
    #db(db.clsb_product.id > 1386 and db.clsb_product.product_title.startswith('STK12')).update(device_shelf_code=13)
    return dict(OK="OK")


def fix_cover_price():
    result = list()
    products = db(db.clsb_product.product_price > 0).select(db.clsb_product.id, db.clsb_product.product_price)
    for product in products:
        cover_price = db((db.clsb_product_metadata.product_id == product.id) & (db.clsb_product_metadata.metadata_id ==
                         2)).select(db.clsb_product_metadata.metadata_value).first()
        if not cover_price is None:
            price = product.product_price * 100 / 30
            db((db.clsb_product_metadata.product_id == product.id) & (db.clsb_product_metadata.metadata_id ==2)).update(metadata_value = price)
            result.append(cover_price)
        else:
            result.append("Product code not cover price: " + str(product.product_price))
            price = product.product_price * 100 / 30
            mid = db.clsb_product_metadata.insert(product_id=product.id, metadata_id=2, metadata_value=price)
            result.append("Updated cover price: " + str(price) + ' with id: ' + str(mid))
    return dict(data=result)


def test_pdflib():
    # import sys
    # sys.path.append("/home/pylibs/pdflib_old")
    try:
        import pdfcryptor
        pdfcryptor.encrypt('/home/sample.pdf', '/home/')
        return "OK"
    except:
        import traceback
        import StringIO
        traceback.print_exc()
        return "Error"


def test_preview():
    try:
        import sys
        import pdfcryptor
        pdfcryptor.preview("/home/CBSData/01GKTOAN/01GKTOAN.E.pdf", "/home/CBSData/01GKTOAN_PREVIEW")
        return "OK"
    except Exception as ex:
        return str(ex) + " on line " + str(sys.exc_traceback.tb_lineno)

def check_pending():
    result = list()
    query = db(db.clsb_product.id > 0)(db.clsb_product.product_status == 'Approved')
    products = query.select(db.clsb_product.product_code, db.clsb_product.product_title,
                            db.clsb_product.id)
    for product in products:
        import fs.path
        # print product.product_code
        # if osFileServer.exists(product.product_code):
            # path = fs.path.pathjoin(product.product_code, 'cover.clsbi')
        dirs = osFileServer.listdir(product.product_code, "cover.clsbi")
        if len(dirs) == 0:
            # print dirs
            result.append("Product: %s - %s - %d" % (product.product_title, product.product_code, product.id))
        # if not osFileServer.exists("%s/%s" % (product.product_code, 'cover.clsbi')):
        #     db(db.clsb_product.id == product.id).update(product_status='Pending')
        #     result.append("Product: %s - %s - %d" % (product.product_title, product.product_code, product.id))
    return dict(total=len(result), result=result)


def test_ota():
    import subprocess

    # Put stderr and stdout into pipes
    # proc = subprocess.Popen('java -jar %s %s %s "%s" "%s" %s %s' % ('/home/CBSData/SignUpdate/SignApkOTA.jar',
    #                         '/home/CBSData/com.tvb.classbook.store/com.tvb.classbook.store.zip',
    #                         'com.tvb.classbook.store', '', 'Ví dụ OTA', '/home/CBSData/OTAUPDATE/OTA_Test.zip',
    #                         '/home/CBSData/SignUpdate/convert2ota.sh'),
    #                         shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    proc = subprocess.Popen('sh %s %s %s "%s" "%s" %s' % ('/home/CBSData/SignUpdate/convert2ota.sh',
                            '/home/CBSData/com.tvb.classbook.store/com.tvb.classbook.store.zip',
                            'com.tvb.classbook.store', '', 'Ví dụ OTA',
                            '/home/developers/manhtd/CBSData/OTAUPDATE/OTA_Test.zip'),
                            shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
    # proc = subprocess.call(['sh', '/home/CBSData/SignUpdate/convert2ota.sh',
    #                         '/home/CBSData/com.tvb.classbook.store/com.tvb.classbook.store.zip',
    #                         'com.tvb.classbook.store', '_', "Ví_dụ_OTA",
    #                         '/home/CBSData/OTAUPDATE/OTA_Test.zip'])
    res = list()
    res.append('return_code: %s' % proc.wait())
    # Read from pipes
    # for line in proc.stdout:
    #     res.append("stdout: " + line.rstrip())
    # for line in proc.stderr:
    #     res.append("stderr: " + line.rstrip())
    # print len(proc.stderr)
    #print proc.stderr.readlines()
    #print proc.stdout.readlines()
    return dict(result=res)


def report():
    query = db(db.clsb_download_archieve.id > 0)
    query = query(db.clsb_product.id == db.clsb_download_archieve.product_id)
    # query = query(db.clsb_category.id == db.clsb_product.product_category)
    # query = query(db.clsb_category.category_type == 1)
    archive = query.select(db.clsb_download_archieve.id, db.clsb_product.product_price)
    count = 0
    for a in archive:
        count += a.clsb_product.product_price
    return dict(res=count)


def test():
    return db(db.clsb_product.id == 138).update(total_download=db.clsb_product.total_download+1)


def fix_app_zip():
    import zipfile
    res = list()
    query = db(db.clsb_category.category_type == 2)
    query = query(db.clsb_product.product_category == db.clsb_category.id)
    products = query.select(db.clsb_product.product_code)
    for product in products:
        files = osFileServer.listdir(product.product_code, wildcard="*.[Zz][Ii][Pp]")
        z = zipfile.ZipFile(osFileServer.open("%s/%s" % (product.product_code, files[0])))
        is_not_valid = True
        if z.namelist()[0] == '%s/' % product.product_code:
            is_not_valid = False
        z.close()
        if is_not_valid:
            res.append("Product: %s" % product.product_code)
            osFileServer.move("%s/%s" % (product.product_code, files[0]),
                              "%s/%s.bk1" % (product.product_code, files[0]), overwrite=True)
            z = zipfile.ZipFile(osFileServer.open("%s/%s.bk1" % (product.product_code, files[0])))
            zout = zipfile.ZipFile(osFileServer.open("%s/%s" % (product.product_code, files[0]), 'w'), mode="w")
            zout.writestr("%s/" % product.product_code, '')
            for filename in z.namelist():
                buffer_data = z.read(filename)
                zinfo = z.getinfo(filename)
                if zinfo.external_attr == 16:
                    zout.writestr("%s/%s" % (product.product_code, filename), '')
                else:
                    zout.writestr("%s/%s" % (product.product_code, filename), buffer_data)
            zout.close()
            z.close()
            import traceback
            import StringIO
            error_ouput = StringIO.StringIO()
            traceback.print_exc(file=error_ouput)
            res.append("Product: %s" % product.product_code)
            res.append(error_ouput.getvalue())
    return dict(result=res)

def convert_serialable():
    productCode = request.args[0]

    import subprocess

    #print settings.home_dir
    #print productCode
    subprocess.call(
        ['java', '-jar', '/home/libs/ToolConvertSerialable/ToolConvertSerialable.jar', settings.home_dir, productCode])


def gen_data():
    import os
    import subprocess

    path = settings.home_dir
    dirs = os.listdir(path)
    result = list()
    for file in dirs:
        if os.path.isdir(path + file):
            try:
                subprocess.call(
                    ['java', '-jar', '/home/libs/ToolConvertSerialable/ToolConvertSerialable.jar', settings.home_dir,
                     file])
            except Exception as e:
                result.append(str(file) + " Lỗi " + str(e))
    return dict(result=result)