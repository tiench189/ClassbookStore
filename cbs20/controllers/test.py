# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys
import os
import time

def gen_first_page_pdf():
    try:
        from pyPdf import PdfFileWriter, PdfFileReader
        inputpdf = PdfFileReader(open("/home/pylibs/TESTUPLOAD2.pdf", "rb"))
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(0))
        with open("/home/pylibs/first-page.pdf", "wb") as outputStream:
            output.write(outputStream)
        import PythonMagick
        img = PythonMagick.Image()
        img.read("/home/pylibs/first-page.pdf")
        print(str(img.size().width()) + "/" + str(img.size().height()))
        img.write("/home/pylibs/first-page.png")
        os.remove("/home/pylibs/first-page.pdf")
        return dict(result="success")
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def convert_pdf_img():
    try:
        import PythonMagick
        img = PythonMagick.Image()
        img.density("300")
        img.read("/home/pylibs/first-page.pdf")
        img.write("/home/pylibs/first-page.png")
        return dict(result="success")
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def stream_video():
    try:
        path = "/temp/snsd/snsd.mp4"
        filename = "snsd.mp4"
        response.headers['ContentType'] ="application/octet-stream"
        response.headers['Content-Disposition']="attachment; filename=" + filename
        return response.stream(open(path), chunk_size=4096)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def cbapp_trial_gift():
    try:
        product_title = "Tiếng Anh 3, tập 1"
        product_id = 677
        category_id = 56
        token = request.vars.user_token
        users = db(db.clsb_user.user_token == token).select()
        if len(users) == 0:
            return dict(error=CB_0012)
        user_id = users.first()['id']
        history = db(db.clsb30_product_history.product_id == product_id)\
                    (db.clsb30_product_history.user_id == user_id).select()
        if len(history) == 0:
            db.clsb30_product_history.insert(
                        product_title=product_title,
                        product_id=product_id,
                        user_id=user_id,
                        category_id=category_id,
                        product_price=0
                    )
        history_media = db(db.clsb30_media_history.product_id == product_id)\
                    (db.clsb30_media_history.user_id == user_id).select()
        if len(history_media) == 0:
            db.clsb30_media_history.insert(
                        product_title=product_title,
                        product_id=product_id,
                        user_id=user_id,
                        category_id=category_id,
                        product_price=0
                    )
        return dict(mess="SUCCESS")
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def list_file_with_extension():
    try:
        import os
        import subprocess
        path = "/home/www-data/web2py/applications/stream/static/video/a0tect"
        #print(list_file(path))
        for video in list_file(path):
            dic_video = video.replace('.mp4', '_480.mp4')
            command = 'ffmpeg -i ' + video + ' -vcodec libx264 -crf 22 -threads 0 -r 18 -s 852x480 -acodec copy ' + dic_video
            subprocess.call(command, shell=True)
        return
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def list_file(path):
    files = []
    for name in os.listdir(path):
        if os.path.isfile(os.path.join(path, name)):
            if str(name).lower().endswith('.mp4'):
                file_name = path + "/" + str(name)
                file_name = file_name.replace(' ', '\ ')
                files.append(file_name)
        else:
            files += list_file(path + "/" + str(name))
    return files

def set_user_by():
    try:
        user_id = 37422
        product_sgk = db(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_category.category_code.like('%SGK%')).select()
        list_record = list()
        for product in product_sgk:
            temp = dict(
                    product_title=product['clsb_product']['product_title'],
                    product_id=product['clsb_product']['id'],
                    user_id=user_id,
                    category_id=product['clsb_category']['id'],
                    product_price=0
                )
            list_record.append(temp)
        db.clsb30_product_history.bulk_insert(list_record)
        return "SUCCESS"
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


from A0techSMS import SMSCode

@request.restful() #Luu y: bat buoc
def get_sms_pay_code():

    '''
    $id = $_POST["MessageID"];
    $number = $_POST["SendNumber"];
    $service = $_POST["ServiceNumber"];
    $info = $_POST["Info"];
    $gendate = $_POST["GenDate"];

    <root>
     <Message Type="1" >(MT tính cước)
<ReceiverNumber>84977575686</ReceiverNumber> (Số máy người nhận)
<Info>Chao mung toi 8x75!</Info> (Nội dung text)
<ContentType>0</ContentType> (Loại nội dung là text)
   </Message>
   <Message Type="2">(MT không tham gia tính cước)
<ReceiverNumber>84977575686</ReceiverNumber> (Số máy người nhận)
<Info> Nhac chuong:http://8x75.vn/download.jsp?param=123456</Info> (link  wappush)
<ContentType>8</ContentType> (Loại nội dung là wappush)
   </Message>
</root>

    '''

    def GET(*args, **vars):

        return "Trang này không tồn tại!"

    def POST(*args, **vars):

        response.headers['Content-Type'] = 'text/xml'

        try:

            if len(vars) < 4:

                return "Reques not valid"

            msgid = vars['MessageID']
            sendnum = vars['SendNumber']
            info = vars['Info']
            service_num = vars['ServiceNumber']


            package_id = 0

            #process info
            info = info.strip()

            info_arr = info.split()  #default is space

            if len(info_arr) < 2:
                return "leninfo_arr<2 " + str(len(info_arr))
            prefix = info_arr[0]
            posfix = info_arr[1]

            if not (prefix.lower() == 'a0'):
                return "no a0"

            if posfix.lower() == 'ly':
                package_id = 2
            elif posfix.lower() == 'hoa':
                package_id = 3
            elif posfix.lower() == 'sinh':
                package_id = 4
            elif posfix.lower() == 'toan':
                package_id = 5
            elif posfix.lower() == 'anh':
                package_id = 6
            else:
                return "ngoai cung " + posfix

            if service_num == '8755':
                duration_val = 7
            elif service_num == '8655':
                duration_val = 3
            elif service_num == '8555':
                duration_val = 1

            smcode = SMSCode(msgid, sendnum)

            try:

                row = db((db.a0tech_sms_pay_code.send_number == sendnum) & (db.a0tech_sms_pay_code.message_id == msgid)).select().first()

                if row is None:

                    exist_code = smcode.gen_sms_pay_code()
                    db.a0tech_sms_pay_code.insert(package_id=package_id,
                                                  paycode=exist_code,
                                                  send_number=sendnum,
                                                  service_number=service_num,
                                                  duration=duration_val,
                                                  message_id=msgid)
                else:
                    exist_code = row['paycode']

                message = '<?xml version="1.0" ?>'\
                          '<root><Message Type = "1">' \
                          '<ReceiverNumber>' + sendnum + '</ReceiverNumber>' \
                          '<Info>Cam on ban da dang ky su dung PM Luyen thi vao 10 chuyen. Ma kich hoat cua ban la:' + exist_code + '</Info>' \
                          '<ContentType>1</ContentType> ' \
                          '</Message>' \
                          '</root>'

            except Exception as ex:

                print ex.message
                message = '<?xml version="1.0" ?>' \
                          '<root><Message Type = "1">' \
                          '<ReceiverNumber>' + sendnum + '</ReceiverNumber>' \
                          '<Info>Cam on ban da dang ky su dung PM Luyen thi vao 10 chuyen. ' \
                          'Da co loi xay ra, tin nhan se khong bi tru tien. Lien he p.CSKH: 0473020888 de duoc ho tro' \
                          '</Info>' \
                          '<ContentType>0</ContentType> ' \
                          '</Message>' \
                          '</root>'

            #from gluon.serializers import xml
            #response.write(message, escape=False)
            return message
        except Exception as ex:
            return ex.message
    return locals()
    #return dict(paycode=msg1)


import Image, PIL
from PIL import Image
import glob, os

def split_image():
    try:
        split_x = 4
        split_y = 4
        basewidth = 200
        pieces = list()
        path = "/temp/book1.jpg"
        path_out = "/temp/book1.png"
        root_img = Image.open(path)
        root_w = root_img.size[0]
        root_h = root_img.size[1]
        for i in range(0, split_y):
            for j in range(0, split_x):
                box = (cut_position(j, root_w, split_x), cut_position(i, root_h, split_y),
                       cut_position(j + 1, root_w, split_x), cut_position(i + 1, root_h, split_y))
                a = root_img.crop(box)
                new_img = Image.new("RGBA", (divide_piece(root_w, split_x), divide_piece(root_h, split_y)), (0, 0, 0, 0))
                new_img.paste(a, (0, 0))
                new_img.save("/temp/book_" + str(i) + "_" + str(j) + ".png", "PNG")
                pieces.append(a)
        img = Image.new("RGBA", (divide_piece(root_w, split_x), divide_piece(root_h, split_y) * split_x * split_y),
                        (0, 0, 0, 0))
        for i in range(0, len(pieces)):
            img.paste(pieces[i], (0, i * divide_piece(root_h, split_y)))
        img.save(path_out, "PNG")
        return "SUCCESS"
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def divide_piece(size, split):
    return (size / split) + (1 if size % split != 0 else 0)


def cut_position(i, size, split):
    result = i * divide_piece(size, split)
    return result if result < size else size


def split_file(path_in, path_out):
    try:
        print(path_in)
        split_x = 4
        split_y = 4
        root_img = Image.open(path_in)
        root_w = root_img.size[0]
        root_h = root_img.size[1]
        mindex = 0
        for i in range(0, split_y):
            for j in range(0, split_x):
                dict_out = path_out
                try:
                    if not os.path.exists(dict_out):
                        os.makedirs(dict_out)
                except Exception as err:
                    print err
                box = (cut_position(j, root_w, split_x), cut_position(i, root_h, split_y),
                       cut_position(j + 1, root_w, split_x), cut_position(i + 1, root_h, split_y))
                a = root_img.crop(box)
                new_img = Image.new("RGBA", (divide_piece(root_w, split_x), divide_piece(root_h, split_y)), (0, 0, 0, 0))
                new_img.paste(a, (0, 0))
                new_img.save(dict_out + "/" + str(mindex) + ".png", "PNG")
                mindex += 1
        os.remove(path_in);
        return "SUCCESS"
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def split_book(dict_in):
    try:
        page = 1
        for file in os.listdir(dict_in):
            if file.endswith(".png"):
                split_file(dict_in + "/" + str(file), dict_in + "/page" + str(page))
                page += 1
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def prepare_view_pdf():
    try:
        dict_in = "/temp/view_pdf"
        for file in os.listdir(dict_in):
            if os.path.isdir(dict_in + "/" + str(file)):
                print(dict_in + "/" + str(file))
                split_book(dict_in + "/" + str(file))
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def make_transparent():
    try:
        from PIL import Image
        img = Image.open('/temp/test_transparent.png')
        img = img.convert("RGBA")
        datas = img.getdata()

        newData = []
        for item in datas:
            if item[0] == 255 and item[1] == 255 and item[2] == 255:
                newData.append((255, 255, 255, 0))
            else:
                newData.append(item)

        img.putdata(newData)
        img.save("/temp/transparent.png", "PNG")
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def get_list_product():
    try:
        products = list()
        cate_ids = [54, 55, 56, 57, 58, 116]
        select_product = db(db.clsb_product.product_category.belongs(cate_ids))\
            (db.clsb_product.product_status.like("Approved"))\
            (db.clsb_product.product_publisher == db.clsb_dic_publisher.id)\
            (db.clsb_product.product_creator == db.clsb_dic_creator.id)\
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
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def copy_data_window():
    try:
        products = list()
        cate_ids = [59, 60, 61, 62, 116]
        select_product = db(db.clsb_product.product_category.belongs(cate_ids))\
            (db.clsb_product.product_status.like("Approved")).select()
        for product in select_product:
            print(product['product_code'])
            copy = copy_data_json(product['product_code'])
            products.append(copy)
        return dict(products=products)
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def copy_data_json(product_code):
    try:
        import usercp
        dst_path = "/temp/data/"
        path = settings.home_dir + product_code
        check_cp = db(db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
            path = settings.home_dir + settings.cp_dir + "CP" + str(cpid) + "/published/" + product_code
        try:
            unzip_file(path + "/" + product_code + "_json.zip", dst_path + product_code)
        except Exception as e:
            pass
        return product_code + ": SUCCESS"
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return product_code + ": " + str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno)
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def test_json():
    copy_data_json("06GKLICHSU")


def copy_data_product(product_code):
    try:
        import usercp
        dst_path = "/temp/data/"
        path = settings.home_dir + product_code
        check_cp = db(db.clsb20_product_cp.product_code.like(product_code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
            path = settings.home_dir + settings.cp_dir + "CP" + str(cpid) + "/published/" + product_code
        try:
            copyanything(path + "/" + product_code + ".E.pdf", dst_path + product_code)
        except Exception as e:
            pass
        try:
            copyanything(path + "/" + product_code + "_json", dst_path + product_code + "/" + product_code + "_json")
        except Exception as e:
            pass
        try:
            unzip_file(settings.home_dir + "Exer" + product_code + "/Exer" + product_code + ".zip", dst_path + product_code)
        except Exception as e:
            pass
        try:
            unzip_file(path + "/" + product_code + ".zip", dst_path + product_code)
        except Exception as e:
            pass
        return product_code + ": SUCCESS"
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return product_code + ": " + str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno)


import shutil, errno
def copyanything(src, dst, ovewrite=False):
    try:
        if not os.path.exists(dst):
            os.makedirs(dst)
        if ovewrite & os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise


def unzip_file(src, dst):
    try:
        import zipfile
        with zipfile.ZipFile(src, "r") as z:
            z.extractall(dst)
        return dict(result="OK")
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def test_unzip():
    return unzip_file("/home/CBSData/01GKTAPVIET01/01GKTAPVIET01.zip", "/temp/data/01GKTAPVIET01")


def add_product_history():
    try:
        username = request.args[0]
        type = request.args[1]
        if int(type) == 1:
            cate_ids = [54, 55, 56, 57, 58, 116]
        else:
            cate_ids = [59, 60, 61, 62, 116]
        user = db(db.clsb_user.username.like(username)).select()
        if len(user) == 0:
            return dict(error="User not exist")
        user = user.first()
        product_insert = list()
        media_insert = list()
        select_product = db(db.clsb_product.product_status.like("Approved"))\
            (db.clsb_product.product_category.belongs(cate_ids)).select()
        for product in select_product:
            buy_pdf = dict()
            buy_pdf['user_id'] = user['id']
            buy_pdf['category_id'] = product['product_category']
            buy_pdf['product_id'] = product['id']
            buy_pdf['product_price'] = 0
            buy_pdf['product_title'] = product['product_title']
            product_insert.append(buy_pdf)
            media_insert.append(buy_pdf)
            select_quiz = db(db.clsb_product.product_code == "Exer" + product['product_code']).select()
            if len(select_quiz) > 0:
                quiz = select_quiz.first()
                buy_quiz = dict()
                buy_quiz['user_id'] = user['id']
                buy_quiz['category_id'] = quiz['product_category']
                buy_quiz['product_id'] = quiz['id']
                buy_quiz['product_price'] = 0
                buy_quiz['product_title'] = quiz['product_title']
                product_insert.append(buy_quiz)
        db.clsb30_product_history.bulk_insert(product_insert)
        db.clsb30_media_history.bulk_insert(media_insert)
        return dict(result="SUCCESS")
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def test_request():
    try:
        import requests
        import json
        url = 'http://thiquocgia.vn/userpanel/service_ajax.php'
        sesskey = "trungdepzai"
        username = "tiench@gmail.com"
        data = dict(u=username, s=md5_string(sesskey + username), f="10000", type="tranfer_fund")
        r = requests.post(url, data=data, allow_redirects=True)
        return json.loads(r.content)
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def md5_string(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()



def test_request2():
    try:
        import requests
        url = 'http://thiquocgia.vn/userpanel/service2.php'
        payload = {'sessKey': 'trungdepzai', 'package_code': 'VIP', 'type': 'BUY', 'username': 'trunglb@tinhvan.com',
                'token': '8e7ca7fffebc32065d0e3784cfda15d126d31ee41bfc85bb'}

        r = requests.get(url, params=payload)
        print(r.text)
        print(r.status_code)
        r = requests.post(url, data=payload)
        print(r.text)
        print(r.status_code)
        import json
        r = requests.post(url, data=json.dumps(payload))

        print(r.text)
        print(r.status_code)
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))

def testprint():
    print 'chaoemcogailamhong949'

def test_request3():
    try:
        import urllib2
        import json
        url_success = "http://thiquocgia.vn/userpanel/service2.php?package_code=VIP&type=BUY&username=trunglb@tinhvan.com&sesskey=trungdepzai&token=8e7ca7fffebc32065d0e3784cfda15d126d31ee41bfc85bb"
        get_data = urllib2.urlopen(url_success)
        str_json = str(get_data.read())
        get_data = json.loads(str_json)
        if get_data['type'] == "success":
            elearning_mess = "success"
        else:
            elearning_mess = get_data['value']
        return dict(mess=elearning_mess)
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
