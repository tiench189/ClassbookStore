# -*- coding: utf-8 -*-
__author__ = 'tanbm'
import shutil, errno
import usercp

################################## Encrypted Copyright CBA

import zipfile
import fs.path

import os
import re
from PIL import Image

THUMB_X = 200
THUMB_Y = 286

STATIC_THUMB = ""

def makethumb(product_code):#product_code, example: VHNT01
#    product_code = request.args(0)
    size = (THUMB_X, THUMB_Y)
    osFileServerCP = OSFS(settings.home_dir+settings.cp_dir+product_code[:-14]+"/review/")
    path = os.path.join(settings.home_dir+settings.cp_dir+product_code[:-14]+"/review/", product_code)
    cover = os.path.join(settings.home_dir+settings.cp_dir+product_code[:-14]+"/review/", fs.path.pathjoin(product_code, 'cover.clsbi'))
    try:
        im = Image.open(cover)
        thumb = im.copy()
        thumb.thumbnail(size, Image.ANTIALIAS)
        thumb.save(os.path.join(path, 'thumb.png'))
    except:
        osFileServerCP.copy(fs.path.pathjoin(product_code, 'cover.clsbi'),
                          fs.path.pathjoin(product_code, 'thumb.png'), True)
    return path


def search_zip_file(code):
    osFileServerCP = OSFS(settings.home_dir+settings.cp_dir+code[:-14]+"/review/")
    files = osFileServerCP.listdir(wildcard=code + ".[Zz][Ii][Pp]", files_only=True)
    if len(files) == 0:
        return None
    return files[0]

import sys


def isEncrypted(code,path):
    osFileServerCP = OSFS(settings.home_dir+settings.cp_dir+code[:-14]+"/review/")
#     return PdfFileReader(file(path, 'rb')).isEncrypted
    return PdfFileReader(osFileServerCP.open(path, 'rb')).isEncrypted


def validate_data(code, product_type):
    osFileServerCP = OSFS(settings.home_dir+settings.cp_dir+code[:-14]+"/review/")
    have_pdf = True
    have_E_pdf = False
    have_cover = False
    have_config = False
    have_zip = False

    have_apk = False

    have_qz = False
    have_quiz_zip = False

    zip_file = search_zip_file(code)
    if zip_file == None:
        return "Error: cannot find zip file."#False

    z = None
    try:
        z = zipfile.ZipFile(osFileServerCP.open(zip_file, 'rb'))

        for name in z.namelist():
            if product_type == 'Book':
                if name.endswith('.pdf'):
                    if name.endswith('.E.pdf'):
                        have_E_pdf = True
                    else:
                        have_pdf = True
                if name.find('cover.clsbi') >= 0:
                    have_cover = True
                if name.find('config.xml') >= 0:
                    have_config = True
                if bool(re.search('.[Zz][Ii][Pp]$', name)):
                    have_zip = True
            elif product_type == 'Application':
                if name.find('cover.clsbi') >= 0:
                    have_cover = True
                if name.find('.apk') >= 0:
                    have_apk = True
            elif product_type == 'Exam' or product_type == 'Exercise':
                if name.endswith('.qz'):
                    have_qz = True
                    # PhuongNH : 15/8/2013 tam thoi comment check file zip vi nhieu de thi khong co media
                """if bool(re.search('.[Zz][Ii][Pp]$', name)):
                   have_quiz_zip = True
                   """
        z.close()
    except Exception as ex:
        errors = list()
        errors.append("Error: " + str(ex))
        if z:
            z.close()
        return errors#False
    #     print "have_E_pdf " + str(have_E_pdf)
    #     print "have_cover " + str(have_cover)
    #     print "have_config " + str(have_config)
    #     print "have_zip " + str(have_zip)

    if osFileServerCP:
        osFileServerCP.close()
    if (product_type == 'Book') and (not have_E_pdf or not have_cover or not have_config or not have_zip or have_pdf):
        errors = list()
        errors.append(" have_E_pdf = " + str(have_E_pdf) + " | ")
        errors.append(" have_cover = " + str(have_cover) + " | ")
        errors.append(" have_config = " + str(have_config) + " | ")
        errors.append(" have_zip = " + str(have_zip) + " | ")
        errors.append(" have_pdf = " + str(have_pdf) + ", There is pdf file not encrypted!| ")
        return errors
    elif (product_type == 'Application') and (not have_cover or not have_apk):
        errors = list()
        errors.append(" have_cover = " + str(have_cover) + " | ")
        errors.append(" have_apk = " + str(have_apk) + " | ")
        return errors
    # PhuongNH : 15/8/2013 tam thoi comment check file zip vi nhieu de thi khong co media
    #elif (product_type == 'Exam' or product_type == 'Exercise') and (not have_qz or not have_quiz_zip):
    elif (product_type == 'Exam' or product_type == 'Exercise') and (not have_qz ):
        errors = list()
        errors.append(" have_qz = " + str(have_qz) + " | ")
        # PhuongNH : 15/8/2013 tam thoi comment check file zip vi nhieu de thi khong co media
        #errors.append(" have_quiz_zip = " + str(have_quiz_zip) + " | ")
        return errors
    else:
        return "OK"


def extract_product_data(code, product_type):
    osFileServerCP = OSFS(settings.home_dir+settings.cp_dir+code[:-14]+"/review/")
    zip_file = search_zip_file(code)
    if zip_file is None:
        return "Error: Cannot find zip file."

    result = validate_data(code, product_type)
    if "OK" not in result:
        return result

    zip_path = fs.path.pathjoin(code, zip_file)[:-3] + "zip"

    z = None
    zout = None
    result = "OK"
    try:
        osFileServerCP.makedir(code, True, True)
        if product_type == 'Book' or product_type == 'Application':
            z = zipfile.ZipFile(osFileServerCP.open(zip_file, 'rb'))
            zout = zipfile.ZipFile(osFileServerCP.open(zip_path, 'wb+'), mode="w")
            for name in z.namelist():
                if name.endswith('.E.pdf'):
                    osFileServerCP.setcontents(fs.path.pathjoin(code, fs.path.basename(name)), z.read(name))
                    pdf_path = fs.path.pathjoin(code, code + ".E.pdf")
                    if not isEncrypted(code, pdf_path):
                        result = "Error: pdf file isn\'t encrypted!"
                        osFileServerCP.removedir(fs.path.pathjoin(code), True, True)
                        raise Exception(result)
                else:
                    buffer_data = z.read(name)
                    zout.writestr(name, buffer_data)
                    if name.find('cover.clsbi') >= 0:
                        osFileServerCP.setcontents(fs.path.pathjoin(code, "cover.clsbi"), buffer_data)
                        #osFileServerCP.setcontents(fs.path.pathjoin(code, name.split('/')[-1]), z.read(name))
                        #             if name.endswith('.qz'):
                        #                 osFileServerCP.setcontents(fs.path.pathjoin(code, fs.path.basename(name)), z.read(name))
                        #             if (product_type == 'Exam' or product_type == 'Exercise') and bool(re.search('.[Zz][Ii][Pp]$', name)):
                        #                 osFileServerCP.setcontents(fs.path.pathjoin(code, fs.path.basename(name)), z.read(name))
            zout.close()
            z.close()
            makethumb(code)
            osFileServerCP.move(zip_file, zip_path + ".bk", True)
        else:
            osFileServerCP.move(zip_file, zip_path, True)
    except Exception as ex:
        if z:
            z.close()
        if zout:
            zout.close()
        result = "Extrac Error:" + str(ex.message) + " on line" + str(sys.exc_traceback.tb_lineno)
    if osFileServerCP:
        osFileServerCP.close()
    return result

################################## END CODE Encrypted ########################

@auth.requires_login()
def init_cp_path():
    response.title = "CP Product Manager"
    return "CP"+str(usercp.user_get_info(auth.user.id, db))
user_cp_path = init_cp_path()


def index():
    return dict(form=None)


@auth.requires_authorize()
def pending():
    # check_is_root()
    if session.auth:
        form = SQLFORM.grid(
            db.clsb20_product_cp.product_status.like("Submit"),
            showbuttontext=False,
            editable=False,
            deletable=False,
            create=False,
        )
        if request.url.find('/view/clsb20_product_cp') >= 0:
            return view_product()
        return dict(form=form)
    else:
        response.flash = "Bạn không có quyền truy cập"
        return dict(form="")


@auth.requires_signature()
def view_product():
    # check_is_root()
    id = request.args[2]
    data = db(db.clsb20_product_cp.id==id).select()
    relation = db(db.clsb20_product_relation_cp.product_cp_id==id).select()
    images = db(db.clsb20_product_image.product_code==data[0].product_code).select()

    path_cp = ""
    category = db(db.clsb_category.id == data[0].product_category)\
            (db.clsb_product_type.id == db.clsb_category.category_type).select()[0]
    if category['clsb_product_type']['type_name'].upper() == "BOOK":
        path_cp = data[0]['product_code'][:-17]
    if category['clsb_product_type']['type_name'].upper() == "APPLICATION":
        path_cp = data[0]['product_code'].split(".")[0][:-3]
    if category['clsb_product_type']['type_name'].upper() == "EXERCISE":
        path_cp = (data[0]['product_code'][:-17])[4:]

    if request.vars.reject:
        if request.vars.reply != "":
            db.clsb20_review_comment.insert(user_id=auth.user.id, product_code=data[0].product_code, comment_time=datetime.now(), review_comment=request.vars.reject)
            db.clsb20_review_history.insert(reviewed_by=auth.user.id, product_code=data[0].product_code, reviewed_time=datetime.now(), status="Reject")
            db(db.clsb20_product_cp.product_code == data[0].product_code).update(product_status="Reject")

    cmtdb = db(db.clsb20_review_comment.product_code == data[0].product_code)\
            (db.auth_user.id == db.clsb20_review_comment.user_id).select(db.clsb20_review_comment.ALL, db.auth_user.ALL)
    reject = TR(
        TD(
            LABEL(B("Thông tin phản hồi"), _class="clsb_label_product"),
            DIV(
                DIV(
                    SPAN("Không có phản hồi" if len(cmtdb) <= 0 else ""),
                    *[DIV(
                        DIV(cmtdb[i]['auth_user']['last_name']+" "+cmtdb[i]['auth_user']['first_name']+" - "+str(cmtdb[i]['clsb20_review_comment']['comment_time']), _class="user"),
                        DIV(cmtdb[i]['clsb20_review_comment']['review_comment'], _class="content"),
                        _class='left' if cmtdb[i]['auth_user']['id'] == auth.user.id else 'right'
                    ) for i in range(len(cmtdb))],
                    _class="border_msg"
                ),
                FORM(
                    INPUT(_name="reject", _style="margin-top: 10px;"),
                    INPUT(_type="submit", _value="Trả lời"),
                    _style="float: right; margin-bottom: 0px;"
                ),
                DIV(_class="clr"),
                _class="clsb20_review_comment"
            ),
            _colspan="2"
        )
    )

    form = TABLE(
        TR(
            TD(
                A(
                    DIV(
                        SPAN(_class="icon leftarrow icon-arrow-left"),
                        " Products", _class="btn"
                    ),
                    _href=URL()
                )
            ),
        ),
        TR(
            TD(
                TABLE(
                    TR(
                        TD(LABEL("Mã sản phẩm: ",_class="clsb_label_product")),
                        TD(LABEL(data[0].product_code,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Tiêu đề sản phẩm: ",_class="clsb_label_product")),
                        TD(LABEL(data[0].product_title,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Chuyên mục: ",_class="clsb_label_product")),
                        TD(LABEL(db(db.clsb_category.id==data[0].product_category).select()[0].category_name,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Giá sách: ",_class="clsb_label_product")),
                        TD(LABEL(db(db.clsb_device_shelf.id==data[0].device_shelf_code).select()[0].device_shelf_name,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Tác giả: ",_class="clsb_label_product")),
                        TD(LABEL(db(db.clsb20_dic_creator_cp.id==data[0].product_creator).select()[0].creator_name,_class="clsb_label_product"))
                    )
                    ,
                    TR(
                        TD(LABEL("Nhà cung cấp/Nhà xuất bản: ",_class="clsb_label_product")),
                        TD(LABEL(db(db.clsb_dic_publisher.id==data[0].product_publisher).select()[0].publisher_name,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Mô tả chi tiết: ",_class="clsb_label_product")),
                        TD(LABEL(data[0].product_description,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Giá tiền: ",_class="clsb_label_product")),
                        TD(LABEL(str(data[0].product_price)+" VNĐ", _class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("ZIP file: ",_class="clsb_label_product")),
                        TD(A(SPAN("Tải về: "+data[0].product_code+".ZIP",_class="btn"), _href=URL(a='cpa', c='download', f='file', args=[path_cp, "upload", data[0].product_code, data[0].product_code+".zip"])))
                    ),
                    reject
                    #TR(
                    #    TD(LABEL("Thao tác: ",_class="clsb_label_product")),
                    #    TD(A(BUTTON(SPAN(_class="icon leftarrow icon-arrow-left",_style="background-position: -96px -120px;")," Kích hoạt review sách",_class="btn"),_href=URL('topending',args=[id],user_signature=True)))
                    #),
                    # TR(
                    #     TD(LABEL("Phản hồi: ",_class="clsb_label_product")),
                    #     TD(
                    #         FORM(
                    #             INPUT(_placeholder="Lý do không được public", _type="text", _name="comment"),
                    #             XML("<br/>"),
                    #             INPUT(_value="Gửi Reject", _type="submit", _class="btn"),
                    #             _action=URL('reject',args=[id])
                    #         )
                    #     )
                    # ),
                    #TR(
                    #    TD(LABEL("Thao tác: ",_class="clsb_label_product")),
                    #    TD(BUTTON("Published",_class="btn")," ",BUTTON("Reject",_class="btn"))
                    #)
                )
            ),
            TD(
                TABLE(
                    TR(
                        TD(
                            LABEL("Ảnh: ", _class="clsb_label_product")
                        ),
                        TD(
                            TABLE(
                                TR(
                                    TH("bìa cỡ lớn (200x282)px"),
                                    TH("Cỡ nhỏ (100x141)px")
                                ),
                                TR(
                                    TD(IMG(_src=URL(a='cpa', c='download', f='cover', args=[path_cp, 'upload', data[0].product_code, 'cover.clsbi']), _class="clsb_image cover", _style="padding-top: 0px;")),
                                    TD(IMG(_src=URL(a='cpa', c='download', f='cover', args=[path_cp, 'upload', data[0].product_code,'thumb.png']), _class="clsb_image cover", _style="padding-top: 0px; width: 75px; height: 101px;"))
                                )
                            )
                        )
                    ),
                    TR(
                        TD(LABEL("Features Images: ",_class="clsb_label_product")),
                        TD(
                            DIV(
                                *[IMG(_src=URL(a='cpa', c='download', f='image', args=[path_cp, 'upload', images[i].image])) for i in range(len(images))],
                                _class="border_imglist_large"
                            )
                        )
                    ),
                    TR(
                        TD(LABEL("Sách liên quan: ",_class="clsb_label_product")),
                        TD(
                            TABLE(
                                    THEAD(
                                        TR(
                                            TH("ID",_style="background-color: #EAEAEA;", _class="col1"),
                                            TH("Tên sách",_style="background-color: #EAEAEA;", _class="col2")
                                        )
                                    ),
                                    TBODY(
                                        *[TR(TD(relation[i].relation_id), TD(db(db.clsb_product.id==relation[i].relation_id).select()[0].product_title)) for i in range(len(relation))]
                                    ),
                                    _class="clsb_table_product"
                                )
                        )
                    )
                )
            )
        ),
        _class="clsb_table_product"
    )
    return dict(form=form)

# @auth.requires_signature()
# @auth.requires_authorize()
# def topending():
#     try:
#         id = request.args[0]
#         data = db(db.clsb20_product_cp.id==id)
#         try:
#             code = data.select()[0]['product_code']
#         except:
#             session.flash = "Product not found"
#             return redirect(URL("index"))
#         copyanything(settings.home_dir+settings.cp_dir+code[:-14]+"/upload/"+code+"/"+code+".zip", settings.home_dir+settings.cp_dir+code[:-14]+"/review/"+code+".zip", True)
#
#         result = extract_product_data(code, "Book")
#
#         if "OK" not in result:
#             session.flash = result
#         else:
#             try:
#                 copyanything(settings.home_dir+settings.cp_dir+code[:-14]+"/upload/"+code+"/cover.clsbi",settings.home_dir+settings.cp_dir+code[:-14]+"/review/"+code+"/cover.clsbi", True)
#                 copyanything(settings.home_dir+settings.cp_dir+code[:-14]+"/upload/"+code+"/thumb.png",settings.home_dir+settings.cp_dir+code[:-14]+"/review/"+code+"/thumb.png", True)
#             except:
#                 nothing = True
#             now = datetime.now()
#             data.update(product_status = "Pending", product_pending = now)
#             session.flash = "Success"
#     except Exception as e:
#         if e.errno == 2:
#             session.flash = "Thiếu file ZIP"
#         else:
#             session.flash = e
#     return redirect(URL("pending", args=['view','clsb20_product_cp',id],user_signature=True))
#

#########################

def copyanything(src, dst, ovewrite=False):
    try:
        if ovewrite & os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

# @auth.requires_login()
# @auth.requires_authorize()
# def reject():
#     try:
#         check_is_root()
#         id = request.args[0]
#         cmt = request.vars.comment
#         session.flash = "Success: "+cmt
#         dbproduct = db(db.clsb20_product_cp.id==id).select()[0]
#         data = db(db.clsb_comment.product_code == dbproduct.product_code and db.clsb_comment.status.like('reject'))
#
#         if len(data.select()) == 0:
#             db.clsb_comment.insert(comment_content = cmt, product_code = dbproduct.product_code, email = auth.user.email, status = "REJECT")
#         else:
#             data.update(comment_content = cmt)
#         db(db.clsb20_product_cp.id==id).update(product_status="Reject")
#     except:
#         session.flash = "Có lỗi xảy ra"
#     return redirect(URL("pending", args=['view','clsb20_product_cp',id],user_signature=True))