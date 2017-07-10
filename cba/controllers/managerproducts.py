    # -*- coding: utf-8 -*-
__author__ = 'tanbm'
import shutil, errno
import subprocess
import usercp
import thread

STATIC_FILE = "/home/www-data/web2py/applications/cbw/static/covers/"


def index():
    return dict(form=None)


# @auth.requires_signature()
@auth.requires_authorize()
def pending():
    form = SQLFORM.grid(
        (db.clsb20_product_cp.product_status.like("Submit")) | (db.clsb20_product_cp.product_status.like("Pending")),
        showbuttontext=False,
        editable=False,
        fields=(
            db.clsb20_product_cp.id,
            db.clsb20_product_cp.product_title,
            db.clsb20_product_cp.product_code,
            db.clsb20_product_cp.product_category,
            db.clsb20_product_cp.product_status,
        ),
        links=[
            {
                "header": "Encrypt status",
                "body": lambda row: check_status(row['product_code'])
            },
            {
                "header": "Extra",
                "body": lambda row: A("Approved", _href=URL("topublished", args=[row['id'], row['product_code']], user_signature=True), _class="btn") if check_status(row['product_code']) != "PENDING" else A("Đang mã hóa (Hủy)", _href=URL("undopublish", args=[row['id'], row['product_code']], user_signature=True), _class="btn")
            }
        ],
        deletable=False,
        create=False,
    )
    if request.url.find('/view/clsb20_product_cp') >= 0:
        return view_product()
    return dict(form=form)


def check_status(code):
    tmp = db(db.clsb20_encrypt_product.product_code.like(code)).select()
    if len(tmp) > 0:
        return tmp.first()['status']
    else:
        return "None"


@auth.requires_signature()
def view_product():
    # check_is_root()
    id = request.args[2]
    data = db(db.clsb20_product_cp.id == id).select()
    relation = db(db.clsb20_product_relation_cp.product_cp_id==id).select()
    images = db(db.clsb20_product_image.product_code==data[0].product_code).select()

    path_cp = ""
    category = db(db.clsb_category.id == data[0].product_category)\
            (db.clsb_product_type.id == db.clsb_category.category_type).select()[0]
    if category['clsb_product_type']['type_name'].upper() == "BOOK":
        path_cp = data[0]['product_code'][:-17]
    if category['clsb_product_type']['type_name'].upper() == "APPLICATION":
        created_by = data[0]['created_by']
        path_cp = "CP"+str(usercp.user_get_id_cp(created_by, db))
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
                        TD(A(SPAN("Tải về: "+data[0].product_code+".ZIP", _class="btn"), _href=URL(a='cpa', c='download', f='file', args=[path_cp, "upload", data[0].product_code, data[0].product_code+".zip"]), _style="width: 300px;"))
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
                ),
                _class="clsb_upload_border"
            ),
            TD(
                TABLE(
                    TR(
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
                    TR(TD(LABEL("Features Images: ",_class="clsb_label_product"))),
                    TR(
                        TD(
                            DIV(
                                *[IMG(_src=URL(a='cpa', c='download', f='image', args=[path_cp, 'upload', images[i].image])) for i in range(len(images))],
                                _class="border_imglist_large"
                            )
                        )
                    ),
                    TR(TD(LABEL("Sách liên quan: ",_class="clsb_label_product"))),
                    TR(
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
                ),
                _class="clsb_upload_border"
            )
        ),
        _class="clsb_table_product"
    )
    return dict(form=form)


@auth.requires_signature()
def topending(code):
    try:
        data = db((db.clsb20_product_cp.product_code == code) & ((db.clsb20_product_cp.product_status.like("submit")) | (db.clsb20_product_cp.product_status.like("pending"))))
        if len(data.select()) <= 0:
            return "Product not found"

        type_name = db(db.clsb_product_type.id == db.clsb_category.category_type)(db.clsb_category.id == data.select()[0].product_category).select()[0]['clsb_product_type']['type_name']

        cp_path = ""
        check_cp = db(db.clsb20_product_cp.product_code.like(code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
        cp_path = "CP"+str(cpid)
        path = os.path.join(settings.home_dir+settings.cp_dir, cp_path)
        if not os.path.exists(path):
            os.makedirs(path)
        print 'path cp_Dir' + str(path)
        review_path = os.path.join(path, 'review')
        if not os.path.exists(review_path):
            os.makedirs(review_path)
        encrypt = True
        if type_name == "Book":

            z = zipfile.ZipFile(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + code + "/" + code + ".zip", "r")
            for name in z.namelist():
                if name.find('.sqlite') >= 0:
                    encrypt = False
            if encrypt == False:
                print subprocess.call(['java', '-jar', '/home/libs/PdfTool/IcePdf.jar', settings.home_dir + settings.cp_dir + cp_path + "/upload/" + code + "/" + code + ".zip", code, settings.home_dir + settings.cp_dir + cp_path + "/review/"+code])
                shutil.rmtree(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + code + "/" + code)
                z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+cp_path+"/review/"+code+".zip", "w")
                zipdir(settings.home_dir+settings.cp_dir+cp_path+"/review/"+code, z)
                z.close()
                shutil.rmtree(settings.home_dir+settings.cp_dir+cp_path+"/review/"+code)



        if encrypt:
            copyanything(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + code + "/" + code + ".zip",
                         settings.home_dir + settings.cp_dir + cp_path + "/review/" + code + ".zip", True)

        result = extract_product_data(code, type_name)
        if "OK" not in result:
            error = result
            return error

        try:
            copyanything(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + code + "/cover.clsbi",
                             settings.home_dir + settings.cp_dir + cp_path + "/review/" + code + "/cover.clsbi", True)
            copyanything(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + code + "/thumb.png",
                             settings.home_dir + settings.cp_dir + cp_path + "/review/" + code + "/thumb.png", True)
        except:
            pass
        db.clsb20_review_history.insert(reviewed_by=auth.user.id, product_code=data.select()[0].product_code, reviewed_time=datetime.now(), status="Pending")
        data.update(product_status="Pending")
        return "OK"
    except OSError as e:
        if e.errno == 2:
            return "Thiếu file ZIP - " +str(e)+ "- on line" + str(sys.exc_traceback.tb_lineno)
        else:
            return str(e)+ "- on line" + str(sys.exc_traceback.tb_lineno)


    #########################
def published_other(code):
    try:
        data = db((db.clsb20_product_cp.product_code == code) & ((db.clsb20_product_cp.product_status.like("pending")) | (db.clsb20_product_cp.product_status.like("published")))).select()
        if len(data) <= 0:
            print "Product not found"
            return "Product not found"
        cat = data[0].product_category
        type_name = db(db.clsb_product_type.id == db.clsb_category.category_type)(db.clsb_category.id == cat).select()[0]['clsb_product_type']['type_name']

        cp_path = ""
        check_cp = db(db.clsb20_product_cp.product_code.like(code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
        cp_path = "CP"+str(cpid)

        path = os.path.join(settings.home_dir+settings.cp_dir, cp_path)
        if not os.path.exists(path):
            os.makedirs(path)
        print 'path cp_Dir' + str(path)
        review_path = os.path.join(path, 'published')
        if not os.path.exists(review_path):
            os.makedirs(review_path)

        try:
            # check if product already exits on store
            dbproduct = db(db.clsb20_product_cp.product_code == code).select()[0]
            data = db(db.clsb_product.product_code == dbproduct.product_code)\
                    (db.clsb_category.id == db.clsb_product.product_category)\
                    (db.clsb_product_type.id == db.clsb_category.category_type).select()
            product_is_exits = True
            if len(data) == 0:
                product_is_exits = False
            creator = db(db.clsb_dic_creator.creator_name.like(db(db.clsb20_dic_creator_cp.id == dbproduct.product_creator).select()[0].creator_name)).select()
            if len(creator) <= 0:
                creator = db.clsb_dic_creator.insert(creator_name=db(db.clsb20_dic_creator_cp.id == dbproduct.product_creator).select()[0].creator_name)
            else:
                creator = creator[0]
            if product_is_exits:
                try:
                    copyanything(settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code,
                             settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code+"_Backup", True)
                except Exception as e:
                    pass
            data = db(db.clsb20_product_cp.product_code == code).select()
            if data.first()['data_type'] == 'epub' or data.first()['data_type'] == 'html':
                copyanything(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + dbproduct.product_code,
                        settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code, True)
        except Exception as e:
            print "ERROR"
            print e
        newdata = list()
        if not product_is_exits:
            newdata = db.clsb_product.insert(
                    product_code=dbproduct.product_code,
                    product_title=dbproduct.product_title,
                    product_description=dbproduct.product_description,
                    subject_class=dbproduct.subject_class,
                    product_category=dbproduct.product_category,
                    product_creator=creator.id,
                    product_publisher=dbproduct.product_publisher,
                    product_price=dbproduct.product_price,
                    product_status="Approved",
                    device_shelf_code=dbproduct.device_shelf_code,
                    product_cover=URL(a='cps', c='file', f='cover', args=dbproduct.product_code, host=True),
                    product_data=URL(a='cps', c='file', f='data', args=dbproduct.product_code, host=True),
                    product_pdf=URL(a='cps', c='file', f='product', args=dbproduct.product_code, host=True),
                    data_type=dbproduct.data_type
                )
        else:
            newdata = db(db.clsb_product.product_code==dbproduct.product_code).select()[0]
            db(db.clsb_product.product_code==dbproduct.product_code).update(
                    product_title=dbproduct.product_title,
                    subject_class = dbproduct.subject_class,
                    product_description=dbproduct.product_description,
                    product_category=dbproduct.product_category,
                    product_creator=creator.id,
                    product_publisher=dbproduct.product_publisher,
                    product_price=dbproduct.product_price,
                    product_status="Approved",
                    device_shelf_code=dbproduct.device_shelf_code,
                    product_cover=URL(a='cps', c='file', f='cover', args=dbproduct.product_code, host=True),
                    product_data=URL(a='cps', c='file', f='data', args=dbproduct.product_code, host=True),
                    product_pdf=URL(a='cps', c='file', f='product', args=dbproduct.product_code, host=True),
                    data_type=dbproduct.data_type
                )

        copy_relation(code)
        copy_metadata(code)
        db(db.clsb20_product_cp.product_code == code).update(product_status="Published")
        return "OK"
    except Exception as ex:
        print ex.message+" on line: "+str(sys.exc_traceback.tb_lineno)
        return "Lỗi: " + str(ex) +" on line: "+str(sys.exc_traceback.tb_lineno)

@auth.requires_signature()
def published(code):
    print "Start: "+code
    try:
        data = db((db.clsb20_product_cp.product_code == code) & ((db.clsb20_product_cp.product_status.like("pending")) | (db.clsb20_product_cp.product_status.like("published")))).select()
        if len(data) <= 0:
            print "Product not found"
            return "Product not found"
        cat = data[0].product_category
        type_name = db(db.clsb_product_type.id == db.clsb_category.category_type)(db.clsb_category.id == cat).select()[0]['clsb_product_type']['type_name']

        cp_path = ""
        check_cp = db(db.clsb20_product_cp.product_code.like(code)).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
        cp_path = "CP"+str(cpid)

        path = os.path.join(settings.home_dir+settings.cp_dir, cp_path)
        if not os.path.exists(path):
            os.makedirs(path)
        print 'path cp_Dir' + str(path)
        review_path = os.path.join(path, 'published')
        if not os.path.exists(review_path):
            os.makedirs(review_path)

        try:
            # check if product already exits on store
            dbproduct = db(db.clsb20_product_cp.product_code == code).select()[0]
            data = db(db.clsb_product.product_code == dbproduct.product_code)\
                    (db.clsb_category.id == db.clsb_product.product_category)\
                    (db.clsb_product_type.id == db.clsb_category.category_type).select()
            product_is_exits = False
            if len(data) > 0:
                product_is_exits = True
            creator = db(db.clsb_dic_creator.creator_name.like(db(db.clsb20_dic_creator_cp.id == dbproduct.product_creator).select()[0].creator_name)).select()
            if len(creator) <= 0:
                creator = db.clsb_dic_creator.insert(creator_name=db(db.clsb20_dic_creator_cp.id == dbproduct.product_creator).select()[0].creator_name)
            else:
                creator = creator[0]
            if product_is_exits:
                try:
                    # if product already exits on store then backup old data -> product_codeBackup folder
                    copyanything(settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code,
                             settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code+"_Backup", True)
                except Exception as e:
                    pass
            if type_name.upper() == "APPLICATION":
                # if product is an application, coppy all data from upload folder to published folder
                copyanything(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + dbproduct.product_code,
                         settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code, True)
            else:
                # if product is not an application, coppy all data from review folder to published folder
                copyanything(settings.home_dir + settings.cp_dir + cp_path + "/review/" + dbproduct.product_code,
                         settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code, True)
        except Exception as e:
            print "ERROR"
            print e
        if type_name.upper() == "BOOK":
            # if product is a book, check product encrypt status in table clsb20_encrypt_product
            check = db(db.clsb20_encrypt_product.product_code.like(dbproduct.product_code)).select()
            if len(check) > 0:
                # if product status is peding or encrypting
                if (check.first()['status'].upper() == "PENDING") | (check.first()['status'].upper() == "ENCRYPTING"):
                    return "?ang mã hóa"
                else:
                    db(db.clsb20_encrypt_product.product_code == dbproduct.product_code).update(
                        status="PENDING",
                    )
            else:
                db.clsb20_encrypt_product.insert(
                    product_code=dbproduct.product_code,
                    product_path=settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code,
                )
            # encript_now(code, dbproduct, cp_path, product_is_exits)
            # thread.start_new_thread(encript_now, (code, dbproduct, cp_path, product_is_exits, ))
            # from gluon.contrib.simplejsonrpc import ServerProxy
            # url = settings.rpc_server+"/cba/tools/call/jsonrpc"
            # service = ServerProxy(url)
            # result_pdf = service.encrypt_pdf(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".pdf", settings.home_dir+settings.cp_dir+cp_path+"/published/"+code)
            # if result_pdf['result'] != True:
            #     shutil.rmtree(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code)
            #     if product_is_exits:
            #         copyanything(settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code+"_Backup",
            #                  settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code, True)
            #     print "Encript False"
            #     return
            # else:
            #     os.remove(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".pdf")
            #     os.remove(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".W.pdf")
        if type_name.upper() == "APPLICATION":
            import subprocess
            sh_location = '/home/CBSData/SignUpdate/convert2ota.sh'
            proc = subprocess.Popen('sh %s %s %s "%s" %s %s "%s" %s' % (sh_location,
                                                    settings.home_dir+settings.cp_dir+cp_path+'/published/'+code+'/'+code+'.zip',
                                                    code, '127.0.0.1:3306', 'dev', settings.database_uri.split('/')[-1],
                                                    'DEV2013!@#', settings.home_dir+'OTAUPDATE/'+code+'.zip'),
                                                shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            proc.wait()
            std_err = proc.stderr.readlines()
            if len(std_err) > 0:
                print "ERROR ON OTA: " + str(std_err)
                return RuntimeError(str(std_err))
            # sh_location = '/home/CBSData/SignUpdate/convert2ota_new.sh'
            # proc = subprocess.Popen('sh %s %s %s "%s" %s %s "%s" %s' % (sh_location,
            #                                         settings.home_dir+settings.cp_dir+cp_path+'/published/'+code+'/'+code+'.zip',
            #                                         code, '127.0.0.1:3306', 'dev', settings.database_uri.split('/')[-1],
            #                                         'DEV2013!@#', settings.home_dir+'CB02OTA/'+code+'.zip'),
            #                                     shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
            # proc.wait()
            # std_err = proc.stderr.readlines()
            # if len(std_err) > 0:
            #     print "ERROR ON OTA: " + str(std_err)
            #     return RuntimeError(str(std_err))
        if type_name.upper() == "EXERCISES":
            pass

        if type_name.upper() == "BOOK":
            pass
            # db(db.clsb20_product_cp.product_code == code).update(product_status="ENCRYPTING")
        else:
            newdata = list()
            if not product_is_exits:
                newdata = db.clsb_product.insert(
                    product_code=dbproduct.product_code,
                    product_title=dbproduct.product_title,
                    product_description=dbproduct.product_description,
                    subject_class=dbproduct.subject_class,
                    product_category=dbproduct.product_category,
                    product_creator=creator.id,
                    product_publisher=dbproduct.product_publisher,
                    product_price=dbproduct.product_price,
                    product_status="Approved",
                    device_shelf_code=dbproduct.device_shelf_code,
                    product_cover=URL(a='cps', c='file', f='cover', args=dbproduct.product_code, host=True),
                    product_data=URL(a='cps', c='file', f='data', args=dbproduct.product_code, host=True),
                    product_pdf=URL(a='cps', c='file', f='product', args=dbproduct.product_code, host=True)
                )
            else:
                newdata = db(db.clsb_product.product_code==dbproduct.product_code).select()[0]
                db(db.clsb_product.product_code==dbproduct.product_code).update(
                    product_title=dbproduct.product_title,
                    subject_class = dbproduct.subject_class,
                    product_description=dbproduct.product_description,
                    product_category=dbproduct.product_category,
                    product_creator=creator.id,
                    product_publisher=dbproduct.product_publisher,
                    product_price=dbproduct.product_price,
                    product_status="Approved",
                    device_shelf_code=dbproduct.device_shelf_code,
                    product_cover=URL(a='cps', c='file', f='cover', args=dbproduct.product_code, host=True),
                    product_data=URL(a='cps', c='file', f='data', args=dbproduct.product_code, host=True),
                    product_pdf=URL(a='cps', c='file', f='product', args=dbproduct.product_code, host=True)
                )

            copy_relation(code)
            copy_metadata(code)
            db(db.clsb20_product_cp.product_code == code).update(product_status="Published")
        db.clsb20_review_history.insert(reviewed_by=auth.user.id, product_code=dbproduct.product_code, reviewed_time=datetime.now(), status="Published")
        print "OK"
        return "OK"
    except Exception as ex:
        print ex.message+" on line: "+str(sys.exc_traceback.tb_lineno)
        return "L?i"


def encrypt_success(): #code
    code = request.args[0]
    dbproduct = db(db.clsb20_product_cp.product_code == code).select()[0]
    db(db.clsb20_product_cp.product_code == code).update(update_file=0)
    cp_path = (code[:-17])
    os.remove(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".pdf")
    directory = STATIC_FILE + code
    if not os.path.exists(directory):
        os.makedirs(directory)
    copyanything(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/cover.clsbi", STATIC_FILE + code + "/cover.clsbi")
    copyanything(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/thumb.png", STATIC_FILE + code + "/thumb.png")
    # os.remove(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".W.pdf")
    import subprocess
    subprocess.call(["python", "/home/pylibs/create_preview.py",
                     settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".E.pdf",
                     settings.home_dir+settings.cp_dir+cp_path+"/published/"+code + "_PREVIEW/"])
    newdata = list()
    data = db(db.clsb_product.product_code == dbproduct.product_code)\
            (db.clsb_category.id == db.clsb_product.product_category)\
            (db.clsb_product_type.id == db.clsb_category.category_type).select()
    product_is_exits = False
    if len(data) > 0:
        product_is_exits = True
    creator = db(db.clsb_dic_creator.creator_name.like(db(db.clsb20_dic_creator_cp.id == dbproduct.product_creator).select()[0].creator_name)).select()
    if len(creator) <= 0:
        creator = db.clsb_dic_creator.insert(creator_name=db(db.clsb20_dic_creator_cp.id == dbproduct.product_creator).select()[0].creator_name)
    else:
        creator = creator[0]

    if not product_is_exits:
        newdata = db.clsb_product.insert(
            product_code=dbproduct.product_code,
            product_title=dbproduct.product_title,
            product_description=dbproduct.product_description,
            subject_class=dbproduct.subject_class,
            product_category=dbproduct.product_category,
            product_creator=creator.id,
            product_publisher=dbproduct.product_publisher,
            product_price=dbproduct.product_price,
            product_status="Approved",
            device_shelf_code=dbproduct.device_shelf_code,
            product_cover=URL(a='cps', c='file', f='cover', args=dbproduct.product_code, host=True),
            product_data=URL(a='cps', c='file', f='data', args=dbproduct.product_code, host=True),
            product_pdf=URL(a='cps', c='file', f='product', args=dbproduct.product_code, host=True)
        )
    else:
        newdata = db(db.clsb_product.product_code==dbproduct.product_code).select()[0]
        db(db.clsb_product.product_code==dbproduct.product_code).update(
            product_title=dbproduct.product_title,
            subject_class = dbproduct.subject_class,
            product_description=dbproduct.product_description,
            product_category=dbproduct.product_category,
            product_creator=creator.id,
            product_publisher=dbproduct.product_publisher,
            product_price=dbproduct.product_price,
            product_status="Approved",
            device_shelf_code=dbproduct.device_shelf_code,
            product_cover=URL(a='cps', c='file', f='cover', args=dbproduct.product_code, host=True),
            product_data=URL(a='cps', c='file', f='data', args=dbproduct.product_code, host=True),
            product_pdf=URL(a='cps', c='file', f='product', args=dbproduct.product_code, host=True)
        )
    copy_relation(code)
    copy_metadata(code)
    #subprocess.call(['java', '-jar', '/home/libs/ToolConvertSerialable/ToolConvertSerialable.jar', settings.home_dir+settings.cp_dir+cp_path+"/published/", code])
    db(db.clsb20_product_cp.product_code == code).update(product_status="Published")


def encrypt_error(): #code
    code = request.args[0]
    list_report = db(db.auth_user.id == db.clsb20_user_report_list.user_id)\
        (db.clsb20_user_report_list.report_type == db.clsb20_user_report_type.id)\
        (db.clsb20_user_report_type.code.like("ENCRYPT")).select(groupby=db.auth_user.id)
    for user in list_report:
        send_mail_report_to_encrypt_false(code, user['auth_user']['email'])

    dbproduct = db(db.clsb20_product_cp.product_code == code).select()[0]
    cp_path = (code[:-17])
    data = db(db.clsb_product.product_code == dbproduct.product_code)\
            (db.clsb_category.id == db.clsb_product.product_category)\
            (db.clsb_product_type.id == db.clsb_category.category_type).select()
    product_is_exits = False
    if len(data) > 0:
        product_is_exits = True
    shutil.rmtree(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code)
    if product_is_exits:
        copyanything(settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code+"_Backup",
            settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code, True)
    # db(db.clsb20_product_cp.product_code == code).update(product_status="Pending")
    print "Encript False"


def send_mail_report_to_encrypt_false(code, email):
    try:
        from time import strftime, gmtime
        product_info = db(db.clsb20_product_cp.product_code == code).select().first()
        product_category = db(db.clsb_category.id == product_info['product_category']).select().first()

        message = '<html>'
        message += 'Thông tin chi tiết <br>'
        message += 'Tiêu đề sản phẩm : ' + str(product_info['product_title']) + '.<br>'
        message += 'Mã sản phẩm : ' + str(product_info['product_code']) + '.<br>'
        message += 'Loại : ' + str(product_category['category_name']) + '<br>'
        message += 'Giá : ' + str(product_info['product_price']) + ' VNĐ<br>'
        message += 'Thời gian: ' + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + ' <br>'
        message += 'Mã hóa không thành công'
        message += '</html>'
        subject = 'Thông báo mã hóa sách không thành công'

        try:
            mail.send(to=[email], subject=subject, message=message)
            return "OK"
        except Exception as e:
            print str(e)
            return dict(error="Lỗi gửi email")
    except Exception as e:
        raise HTTP(200, "Send Mail Error: "+e.message+" on line: "+str(sys.exc_traceback.tb_lineno))


def encript_now(code, dbproduct, cp_path, product_is_exits):
    try:
        import urllib2
        print URL(a='cbe', c='default', f='start_encrypt', args=[code], host=True)
        res = urllib2.urlopen(URL(a='cbe', c='default', f='start_encrypt', args=[code], host=True))
        data = res.read()
    except Exception as e:
        print e
    # from gluon.contrib.simplejsonrpc import ServerProxy
    # url = settings.rpc_server+"/cba/tools/call/jsonrpc"
    # service = ServerProxy(url)
    # result_pdf = service.encrypt_pdf(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".pdf", settings.home_dir+settings.cp_dir+cp_path+"/published/"+code)
    # if result_pdf['result'] != True:
    #     shutil.rmtree(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code)
    #     if product_is_exits:
    #         copyanything(settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code+"_Backup",
    #                 settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code, True)
    #         print "Encript False"
    #         return
    #     else:
    #         os.remove(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".pdf")
    #         os.remove(settings.home_dir+settings.cp_dir+cp_path+"/published/"+code+"/"+code+".W.pdf")
    # print "Finish"
    return


def copy_relation(code):
    try:
        product_public = db(db.clsb_product.product_code == code)
        product = db(db.clsb20_product_cp.product_code == code).select()[0]
        if len(product_public.select()) > 0:
            id = product_public.select()[0].id
            db(db.clsb_product_relation.product_id == id).delete()
            relation = db(db.clsb20_product_relation_cp.product_cp_id == product.id).select()
            for item in relation:
                db.clsb_product_relation.insert(product_id=id, relation_id=item.relation_id)
        return "OK"
    except Exception as ex:
        return 'Error: '+ex.message


def copy_metadata(code):
    try:
        product_public = db(db.clsb_product.product_code == code)
        product = db(db.clsb20_product_cp.product_code == code).select()[0]
        if len(product_public.select()) > 0:
            id=product_public.select()[0].id
            db(db.clsb_product_metadata.product_id == id).delete()
            relation = db(db.clsb20_product_metadata_cp.product_code == product.product_code).select()
            for item in relation:
                db.clsb_product_metadata.insert(product_id=id, metadata_id=item.metadata_id, metadata_value=item.metadata_value)
        return "OK"
    except Exception as ex:
        return 'Error: '+ex.message


def copyanything(src, dst, ovewrite=False):
    try:
        if ovewrite & os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

################################## Encrypted Copyright CBA

import zipfile
import fs.path

import os
import re
from PIL import Image

THUMB_X = 100
THUMB_Y = 143


def makethumb(product_code, product_type):#product_code, example: VHNT01
#    product_code = request.args(0)
    cp_path = ""
    check_cp = db(db.clsb20_product_cp.product_code.like(product_code)).select()
    if len(check_cp) > 0:
        cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
    cp_path = "CP"+str(cpid)

    size = (THUMB_X, THUMB_Y)
    osFileServerCP = OSFS(settings.home_dir + settings.cp_dir + cp_path + "/review/")
    path = os.path.join(settings.home_dir + settings.cp_dir + cp_path + "/review/", product_code)
    cover = os.path.join(settings.home_dir + settings.cp_dir + cp_path + "/review/",
                         fs.path.pathjoin(product_code, 'cover.clsbi'))
    try:
        im = Image.open(cover)
        thumb = im.copy()
        thumb.thumbnail(size, Image.ANTIALIAS)
        thumb.save(os.path.join(path, 'thumb.png'))
    except:
        osFileServerCP.copy(fs.path.pathjoin(product_code, 'cover.clsbi'),
                            fs.path.pathjoin(product_code, 'thumb.png'), True)
    return path


def search_zip_file(code, product_type):
    cp_path = ""
    check_cp = db(db.clsb20_product_cp.product_code.like(code)).select()
    if len(check_cp) > 0:
        cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
    cp_path = "CP"+str(cpid)
    osFileServerCP = OSFS(settings.home_dir + settings.cp_dir + cp_path + "/review/")
    files = osFileServerCP.listdir(wildcard=code + ".[Zz][Ii][Pp]", files_only=True)
    if len(files) == 0:
        return None
    return files[0]

import sys


def validate_data(code, product_type):
    cp_path = ""
    check_cp = db(db.clsb20_product_cp.product_code.like(code)).select()
    if len(check_cp) > 0:
        cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
    cp_path = "CP"+str(cpid)
    osFileServerCP = OSFS(settings.home_dir + settings.cp_dir + cp_path + "/review/")
    have_pdf = False
    #have_E_pdf = False
    have_cover = False
    have_config = False
    have_zip = True

    have_apk = False

    have_qz = False
    have_quiz_zip = False

    zip_file = search_zip_file(code, product_type)
    if zip_file == None:
        return "Error: cannot find zip file."#False

    z = None
    try:
        z = zipfile.ZipFile(osFileServerCP.open(zip_file, 'rb'))

        for name in z.namelist():
            if product_type == 'Book':
                if name.endswith('.pdf'):
                    #if name.endswith('.E.pdf'):
                    #    have_E_pdf = True
                    #else:
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
    #if (product_type == 'Book') and (not have_E_pdf or not have_cover or not have_config or not have_zip or not have_pdf):
    if (product_type == 'Book') and (not have_cover or not have_config or not have_zip or not have_pdf):
        errors = list()
        #errors.append(" have_E_pdf = " + str(have_E_pdf) + " | ")
        errors.append(" have_cover = " + str(have_cover) + " | ")
        errors.append(" have_config = " + str(have_config) + " | ")
        errors.append(" have_zip = " + str(have_zip) + " | ")
        errors.append(" have_pdf = " + str(have_pdf) + " | ")
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
    '''
        - validate zip file
        - extract pdf and cover.clsbi to folder : review/productcode
    '''
    cp_path = ""
    check_cp = db(db.clsb20_product_cp.product_code.like(code)).select()
    if len(check_cp) > 0:
        cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
    cp_path = "CP"+str(cpid)
    osFileServerCP = OSFS(settings.home_dir + settings.cp_dir + cp_path + "/review/")
    zip_file = search_zip_file(code, product_type)
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
                if name.endswith('.E.pdf') | name.endswith('.pdf'):
                    osFileServerCP.setcontents(fs.path.pathjoin(code, code+".pdf"), z.read(name))
                    #osFileServerCP.setcontents(fs.path.pathjoin(code, fs.path.basename(name)), z.read(name))
                    #pdf_path = fs.path.pathjoin(code, code + ".E.pdf")
                    #if not isEncrypted(code, pdf_path):
                    #    result = "Error: pdf file isn\'t encrypted!"
                    #    osFileServerCP.removedir(fs.path.pathjoin(code), True, True)
                    #    raise Exception(result)
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
            makethumb(code, product_type)
            osFileServerCP.move(zip_file, zip_path + ".bk", True)
        else:
            osFileServerCP.move(zip_file, zip_path, True)
    except Exception as ex:
        if z:
            z.close()
        if zout:
            zout.close()
        result = "Extra Error:" + str(ex.message) + " on line" + str(sys.exc_traceback.tb_lineno)
    if osFileServerCP:
        osFileServerCP.close()
    return result

################################## END CODE Encrypted ########################


def zipdir(path, zip):
    rootlen = len(path) + 1
    for base, dirs, files in os.walk(path):
        for file in files:
            fn = os.path.join(base, file)
            zip.write(fn, fn[rootlen:])

def undopublish():
    id = request.args[0]
    code = request.args[1]
    tmp = db(db.clsb20_encrypt_product.product_code.like(code)).select()
    if len(tmp) <= 0:
        session.flash = "Không tồn tại sản phẩm"
    else:
        db(db.clsb20_encrypt_product.product_code.like(code)).delete()
        session.flash = "OK"
    redirect(URL("pending", user_signature=True))

def topublished():
    id = request.args[0]
    code = request.args[1]
    dbproduct = db(db.clsb20_product_cp.product_code == code).select()[0]
    cp_path = (code[:-17])

    data = db(db.clsb20_product_cp.id == id).select()
    if len(data) <= 0:
        session.flash = "Không tồn tại sản phẩm"
    else:
        code = data.first()['product_code']
        if data.first()['data_type'] == 'epub' or data.first()['data_type'] == 'html':
            db(db.clsb20_product_cp.product_code == code).update(product_status='pending')
            result = published_other(code)
        else:
            if data.first()['update_file'] and data.first()['update_file'] == 1:
                result = topending(code)
                if result == "OK":
                    result = published(code)
                    subprocess.call(['java', '-jar', '/home/libs/ToolConvertSerialable/ToolConvertSerialable.jar', settings.home_dir+settings.cp_dir+cp_path+"/published/", code])
            else:
                db(db.clsb20_product_cp.product_code == code).update(product_status='pending')
                result = published_other(code)
        session.flash = result
    redirect(URL("pending", user_signature=True))

def testApproved():
    cp_path = request.args[0]
    code = request.args[1]
    try:
        subprocess.call(['java', '-jar', '/home/libs/ToolConvertSerialable/ToolConvertSerialable.jar', settings.home_dir+settings.cp_dir+cp_path+"/published/", code])
        return True
    except Exception as err:
        print(err)
        return False


def test_copy():
    try:
        code = request.args[0]
        directory = STATIC_FILE + code
        if not os.path.exists(directory):
            os.makedirs(directory)
        copyanything(settings.home_dir+code+"/cover.clsbi", STATIC_FILE + code + "/cover.clsbi21")
        copyanything(settings.home_dir+code+"/thumb.png", STATIC_FILE + code + "/thumb.png")
        return True
    except Exception as err:
        print(err)
        return False
