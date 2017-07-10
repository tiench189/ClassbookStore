# -*- coding: utf-8 -*-
__author__ = 'tanbm'
import zipfile
import re
import os,sys
import shutil
import usercp
import scripts
import products
from time import gmtime, strftime

@auth.requires_login()
def init_cp_path():
    response.title = "CP Product Manager"
    return "CP"+str(usercp.user_get_id_cp(auth.user.id, db))
user_cp_path = init_cp_path()


@auth.requires_authorize()
def index():
    if request.url.find('/new/clsb20_product_cp') >= 0:
        return create_product()
    if request.url.find('/edit/clsb20_product_cp') >= 0:
        return update_product()
    if request.url.find('/view/clsb20_product_cp') >= 0:
        return view_product()
    if request.url.find('/delete/clsb20_product_cp') >= 0:
        return remove_product()
    user_info = usercp.user_get_info(auth.user.id, db)
    query = None
    query_status = ~db.clsb20_product_cp.product_status.like("%delete%")
    if request.vars.product_status:
        if request.vars.product_status != "0":
            query_status = db.clsb20_product_cp.product_status.like(request.vars.product_status)
    if user_info['user_info']['is_admin'] == True:
        query = db(query_status)\
                    ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Application")))\
                    ((db.clsb_category.id == db.clsb20_product_cp.product_category) & (((db.auth_user.created_by == auth.user.id) & (db.auth_user.id == db.clsb20_product_cp.created_by)) | (db.clsb20_product_cp.created_by == auth.user.id)))
    else:
        query = db((query_status) & (db.clsb20_product_cp.created_by == auth.user.id))\
                    ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Application")))\
                    (db.clsb_category.id == db.clsb20_product_cp.product_category)
    if request.vars.keyword:
        keyword = request.vars.keyword
        search = ((db.clsb20_product_cp.product_code == keyword)\
                    | (db.clsb20_product_cp.product_title.like('%' + keyword + '%')))
                    # | (db.clsb20_dic_creator_cp.creator_name.like('%' + keyword + '%'))\
                    # | (db.clsb_dic_publisher.publisher_name.like('%' + keyword + '%')))
        query = query(search)
    product_list = list()
    # categories = db(db.clsb_category.category_parent != None).select()
    product_list.extend(query.select(groupby=db.clsb20_product_cp.id, orderby=~db.clsb20_product_cp.created_on).as_list())
    return dict(
        product_list=product_list,
        user_cp_path=user_cp_path
    )


def get_form(media=False):
    category = db((db.clsb_category.category_type == db.clsb_product_type.id) & ~(db.clsb_category.category_parent == None))(db.clsb_product_type.type_name.like("Application")).select()
    payment = db(~db.clsb20_purchase_type.name.like("Subscriptions")).select()
    subscriptions = db(db.clsb20_purchase_item.purchase_type == db(db.clsb20_purchase_type.name.like("Subscriptions")).select()[0].id).select()
    class_list = db().select(db.clsb_class.ALL, orderby="id DESC").as_list()
    subject_list = db().select(db.clsb_subject.ALL, orderby="id DESC").as_list()
    media_tag = "";
    if media == True:
        media_tag = (TR(
            TD(LABEL(XML("Dữ liệu đa phương tiện <br/>(ZIP file): "), _class="clsb_label_product"), _class="rows-left"),
            TD(
                INPUT(_name="data_media", _class="clsb_input_product", _accept=".zip", _type="file", _style="display: none;"),
                DIV(XML("<b>+</b> Chọn tệp tin ZIP"), _class="btn", _onclick="opendata('data_media', event)")
            )
        ),
        TR(
            TD(LABEL("Thư mục chứa dữ liệu: ", _class="clsb_label_product"), _class="rows-left"),
            TD(
                INPUT(_name="dic_media", _class="clsb_input_product", style=""),
                DIV(I("Ví dụ: '/sdcard/app_data', Tất cả dữ liệu trong file ZIP sẽ được đưa vào thư mục này khi cài đặt"), _style="font-size: 12px; color: rgb(0, 130, 250); font-weight: bold;")
            )
        ))

    form = FORM(
        DIV(
            TABLE(
                TR(
                    TD(
                        A(
                            DIV(
                                SPAN(_class="icon leftarrow icon-arrow-left"),
                                " Quản lý ứng dụng", _class="btn"
                            ),
                            _href=URL(user_signature=True)
                        ),
                    ),
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Tên ứng dụng: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_style="width: 100%;", _name="title",_class="clsb_input_product", requires=IS_NOT_EMPTY()),
                                )
                            ),
                            TR(
                                TD(LABEL("Package: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_style="margin-top: 10px; width: 60%;", _placeholder="com.tvb.example", _name="package", _idvalue=auth.user.id, _link=URL(a='cps',c='products',f='check_package.json'), _class="clsb_input_product", requires=IS_NOT_EMPTY()),
                                    SPAN("Check Validation", _class="btn", _onclick="check_package()")
                                )
                            ),
                            TR(
                                TD(LABEL("Thể loại ứng dụng: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(SELECT(*[OPTION(category[i]['clsb_category']['category_name'], _value=str(category[i]['clsb_category']['id'])) for i in range(len(category))], _style="margin-top: 5px;",_class="clsb_input_product", _name="category"))
                            ),
                            TR(
                                TD(LABEL("Lớp: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(SELECT(*[OPTION(class_list[i]['class_name'], _value=str(class_list[i]['id'])) for i in range(len(class_list))], _style="margin-top: 5px;",_class="clsb_input_product", _name="class"))
                            ),
                            TR(
                                TD(LABEL("Môn: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(SELECT(*[OPTION(subject_list[i]['subject_name'], _value=str(subject_list[i]['id'])) for i in range(len(subject_list))], _style="margin-top: 5px;",_class="clsb_input_product", _name="subject"))
                            ),
                            TR(
                                TD(LABEL("Mô tả chi tiết: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(TEXTAREA(_name="content",_class="clsb_input_product"))
                            ),
                            _style="width: 100%;"
                        ),
                        _class="clsb_upload_border"
                    )
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Cung cấp theo: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(SELECT(
                                    OPTION("Cá nhân", _value=0),
                                    OPTION("Doanh nghiệp", _value=1),
                                    name='select_publisher',
                                    _id='published_type'
                                ))
                            ),
                            TR(
                                TD(),
                                TD(TABLE(
                                    TR(
                                        TD(INPUT(_style="margin-top: 10px;", _class="clsb_input_product", _placeholder="Tác giả", _id="clsb_creator_list", _name="creator", _linkSearch=URL(a='cps', c='creators', f='search')),
                                            SPAN(XML("Tìm kiếm"), _class="btn", _onclick="javascript:searchcreator()"),
                                            DIV("Các tác giả phân cách nhau bằng dấu ';'"),
                                            _id='creator_select',
                                            _style="padding: 0px;"),
                                    ),
                                    TR(
                                        TD(INPUT(_style="margin-top: 10px;",_class="clsb_input_product", _placeholder="Nhà cung cấp", _id="clsb_publisher_list", _name="publisher", _linkSearch=URL(a='cps', c='publishers', f='search')),
                                            SPAN(XML("Tìm kiếm"), _class="btn", _onclick="javascript:searchpublisher()"),
                                            _id="publisher_select",
                                            _style="padding: 0px; display: none;"),
                                    ),
                                    _style="padding: 0px;"
                                ))
                            ),
                            _style="width: 100%;"
                        ),
                        _class="clsb_upload_border"
                    ),
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(
                                    TABLE(
                                        TR(
                                            # TD(
                                            #     SPAN(XML("Ảnh bìa cỡ nhỏ<br/>(100x100)px")),
                                            #     XML("<br/>"),
                                            #     INPUT(_name="thumbnail",_class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;"),
                                            #     DIV(XML("+<br/>Add<br/>Thumbnail"), _class="clsb_image thumbnail_cp app", _onclick="openimage('thumbnail',event,true)"),
                                            # ),
                                            TD(
                                                SPAN("Ảnh bìa (150x150, 200x200, 300x300, ...)px"),
                                                XML("<br/>"),
                                                INPUT(_name="cover", _class="clsb_input_product", _accept="image/*", _type="file", _style="display: none;", requires=IS_NOT_EMPTY()),
                                                DIV(XML("+<br/>Add Cover"), _class="clsb_image cover app", _onclick="openimage('cover',event,true)"),
                                            ),
                                        ),
                                    ),
                                    TABLE(
                                        TR(
                                            TD(
                                                SPAN("Ảnh minh họa khác (Tối đa 5 ảnh - kích cỡ < 1MB)"),
                                                DIV(
                                                    INPUT(_name="feature_images_1", _id="feature_images_1", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    INPUT(_name="feature_images_2", _id="feature_images_2", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    INPUT(_name="feature_images_3", _id="feature_images_3", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    INPUT(_name="feature_images_4", _id="feature_images_4", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    INPUT(_name="feature_images_5", _id="feature_images_5", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    DIV(XML("<b>+</b> Thêm ảnh"), _class="btn", _onclick="addimagesborder('#imglist')"),
                                                    XML("<br/>"),
                                                    DIV(_id="imglist",_class="border_imglist")
                                                ),
                                                _style="overflow: auto;"
                                            )
                                        )
                                    )
                                )
                            ),
                            _style="width: 100%;"
                        ),
                        _class="clsb_upload_border"
                    )
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Dữ liệu ứng dụng (APK file): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_name="data",_class="clsb_input_product", _accept=".apk", _type="file", _style="display: none;"),
                                    DIV(XML("<b>+</b> Chọn tệp tin APK"), _class="btn", _onclick="opendata('data', event)")
                                )
                            ),
                            media_tag,
                            TR(
                                TD(),
                                TD(XML("<b>Chú ý:</b> Mỗi phương thức thu tiền sẽ có hình thức thu phí khi tải về là khác nhau. <br/> <i>Hình thức miễn phí</i>: mặc định giá cho sản phẩm sẽ là 0 VNĐ, khách hàng sẽ không phải trả tiền cho sản phẩm khi chọn hình thức này.<br/> <i>Hình thức thanh toán cho lần tải đầu tiên</i>: Khác hàng sẽ chỉ phải trả phí cho lần đầu tiên tải sản phẩm, các lần sau sẽ không bị thu phí. <br/> <i>Hình thức thanh toán cho mỗi lượt tải</i>: Khách hàng sẽ phải trả phí cho mỗi lần tải sản phẩm về"), _style="color: #999;")
                            ),
                            TR(
                                TD(LABEL("Phương thức thu tiền: ",_class="clsb_label_product", _style="font-weight: bold;"), _class="rows-left"),
                                TD(
                                    SELECT(*[OPTION(payment[i].description, _value=str(payment[i].name)) for i in range(len(payment))], _id="payment",_style="margin-top: 5px;", _class="clsb_input_product", _name="payment"),
                                    DIV(INPUT(_name="price", _placeholder="Giá tiền", _class="clsb_input_product", _value=0, _style="color: rgb(255, 112, 0);  font-weight: bold;"), "VNĐ", _id="price"),
                                ),
                            ),
                            _style="width: 100%;"
                        ),
                        _class="clsb_upload_border"
                    )
                ),
                INPUT(_type="submit", _class="clsb_submit_upload", _value="Hoàn thành"),
                _class="clsb_table_product"
            ),
            #_class="clsb_upload_border"
        ),
        _class="clsb_form_upload"
    )
    return form


@auth.requires_signature()
def create_product(media=False):
    form = get_form(media)
    if form.accepts(request, session):
        try:
            publisher_char = "Doanh nghiệp mới"
            if request.vars.select_publisher == "0":
                publisher_char = "Cá nhân"
            elif request.vars.publisher:
                publisher_char = request.vars.publisher
            publisher = db(db.clsb_dic_publisher.publisher_name.like("%"+publisher_char+"%")).select()
            if len(publisher) <= 0:
                publisher = db.clsb_dic_publisher.insert(publisher_name=publisher_char)
            else:
                publisher = publisher[0]
            # code = user_cp_path+db(db.clsb20_product_type.type_name.like("Application")).select()[0].type_code+"."+request.vars.package
            code = request.vars.package
            data_check = db((db.clsb20_product_cp.product_code == code) & (~db.clsb20_product_cp.product_status.like("%delete%"))).select()
            data_check_out = db((db.clsb20_product_cp.product_code.like(request.vars.package)) & ~(db.clsb20_product_cp.created_by == auth.user.id)).select()
            data_check_store = db((db.clsb_product.product_code.like(request.vars.package)) & ~(db.clsb_product.product_code == code)).select()
            #if len(request.vars.package.split(".")) < 3:
            #    response.flash = "Sai package name"
            if (len(data_check_store) > 0) or (len(data_check_out) > 0) or (len(data_check) > 0):
                response.flash = "Package name đã tồn tại"
            else:

                creator_list = ["Tác giả mới"]
                if request.vars.select_publisher == "1":
                    creator_list = ["Doanh nghiệp"]
                elif request.vars.creator:
                    creator_list = re.split(r"[,;]", request.vars.creator)
                creator = dict()
                add_creator = ""
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("co_author")).select()[0]['id']
                for creat in creator_list:
                    if creat != "":
                        if add_creator == "" :
                            creator = db(db.clsb20_dic_creator_cp.creator_name == creat).select()
                            add_creator = creat
                        else:
                            db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=code, metadata_value=creat)

                if len(creator) <= 0:
                    creator = db.clsb20_dic_creator_cp.insert(creator_name=add_creator)
                else:
                    creator = creator[0]

                create_dir(user_cp_path+"/upload/"+code)
                if request.vars.cover != "":
                    if request.vars.cover.file:
                        save_file(request.vars.cover.file, code+"/cover.clsbi")
                if request.vars.data != "":
                    if request.vars.data.file:
                        create_dir(user_cp_path+"/upload/"+code+"/"+code)
                        create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code)
                        save_file(request.vars.data.file, code+"/"+code+"/"+code+"/"+code+".apk")
                        if media == True:
                            if bool(request.vars.data_media.file) & bool(request.vars.dic_media):
                                if request.vars.dic_media != "":
                                    save_file(request.vars.data_media.file, code+"/"+code+"/"+code+"/"+code+"_media.zip")
                                    with zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+"_media.zip", "r") as z:
                                        z.extractall(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code)
                                        z.close()
                                    os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+"_media.zip")
                                    f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/config.cfg", "w")
                                    f.writelines("des="+request.vars.dic_media+"\n")
                                    f.writelines("type=Normal")
                                    f.flush()
                                    f.close()
                                else:
                                    shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                                    session.flash = "Chưa định dạng đường dẫn cho dữ liệu mở rộng"
                                    return dict(form=form)
                        products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/cover.clsbi")
                        z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "w")
                        zipdir(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code, z)
                        z.close()
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code)
                    #     result = save_data(request.vars.data, code+"/"+code+".zip", code)
                    # if result != "OK":
                    #     response.flash = result
                shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/thumb.png")
                type_image = db(db.clsb20_image_type.name.like("Features")).select()
                if len(type_image) <= 0:
                    type_image = db.clsb20_image_type.insert(name="Features", description="Features Images")
                else:
                    type_image = type_image[0]
                for i in range(1, 6):
                    if request.vars['feature_images_'+str(i)] != "":
                        try:
                            file = request.vars['feature_images_'+str(i)]
                            save_file(file.file, "clsb20_product_cp."+code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                            db.clsb20_product_image.insert(type_id=type_image['id'], product_code=code,description=file.filename,image="clsb20_product_cp."+code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                        except:
                            continue
                device_shelf_code = db(db.clsb_device_shelf.id == db.clsb20_category_shelf_mapping.device_shelf_id)(db.clsb20_category_shelf_mapping.category_id == request.vars.category).select()
                # tiench match class, subject
                class_id = request.vars['class']
                subject_id = request.vars['subject']

                subject_class = db((db.clsb_subject_class.subject_id == subject_id) & (db.clsb_subject_class.class_id == class_id)).select()
                if len(subject_class) > 0:
                    subject_class = subject_class.first()
                else:
                    subject_class = db.clsb_subject_class.insert(subject_id=subject_id, class_id=class_id)
                # end tiench
                if len(db(db.clsb20_product_cp.product_code == code).select()) > 0:
                    newdata = db(db.clsb20_product_cp.product_code == code).select().first()
                    db(db.clsb20_product_cp.product_code == code).update(product_title=request.vars.title,
                                                      product_status="Init",
                                                      product_code=code,
                                                      product_description=request.vars.content,
                                                      product_publisher=publisher.id,
                                                      product_creator=creator.id,
                                                      device_shelf_code=device_shelf_code.first()['clsb_device_shelf']['id'],
                                                      product_category=request.vars.category,
                                                      product_price=request.vars.price,
                                                      subject_class=subject_class['id'])
                else:
                    newdata = db.clsb20_product_cp.insert(product_title=request.vars.title,
                                                      product_code=code,
                                                      product_description=request.vars.content,
                                                      product_publisher=publisher.id,
                                                      product_creator=creator.id,
                                                      device_shelf_code=device_shelf_code.first()['clsb_device_shelf']['id'],
                                                      product_category=request.vars.category,
                                                      product_price=request.vars.price,
                                                      subject_class=subject_class['id'])

                if request.vars.payment != "":
                    if request.vars.payment.upper() == "SUBSCRIPTIONS":
                        purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
                    else:
                        purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.payment)).select()[0].id
                        purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id

                    db.clsb20_product_purchase_item.insert(product_code=newdata.product_code, purchase_item=purchase_item)

                response.flash = 'Tải lên thành công'
        except Exception as ex:
            response.flash = 'Quá trình tải lên bị lỗi' + ex.message +str(sys.exc_traceback.tb_lineno)
    elif form.errors:
        response.flash = 'Lỗi: Thông tin không đúng'
    else:
        response.flash = 'Xin mời điền thông tin'
    return dict(form=form)


def save_file(file, filename):
    f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+filename, 'w+')
    for chunk in products.fbuffer(file):
        f.write(chunk)
    f.close()


def save_data(file, filename, code=""):
    try:
        old_filename = file.filename
        msg = ""
        if bool(re.search(".[Zz][Ii][Pp]$", old_filename)):
            if os.path.exists(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code):
                products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code, settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"_Backup", True)
            try:
                f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+old_filename, 'w+')
                for chunk in products.fbuffer(file.file):
                    f.write(chunk)
                f.close()
                z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+old_filename, "r")
                zip = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+filename, 'w')
                for name in z.namelist():
                    buffer_data = z.read(name)
                    if name.find(old_filename[:-4]) >= 0:
                        zip.writestr(name.replace(old_filename[:-4], code), buffer_data)
                    else:
                        zip.writestr(name, buffer_data)
                zip.close()
                z.close()
                os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+old_filename)
                msg = "OK"
            except Exception as ex:
                shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                try:
                    products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"_Backup", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                except:
                    create_dir(user_cp_path+"/upload/"+code)
                msg = "Fail: "+ex.message
        return msg
    except Exception as ex:
        return ex.message


def update_product(media=False):
    id = request.args[2]
    data = db(db.clsb20_product_cp.id==id)
    # if (data.select()[0].product_status.upper() != "INIT") & (data.select()[0].product_status.upper() != "CANCEL") & (data.select()[0].product_status.upper() != "REJECT") & (data.select()[0].product_status.upper() != "DEVELOPER"):
    if data.select()[0].product_status.upper() == "SUBMIT" or data.select()[0].product_status.upper() == "PENDING":
        session.flash = "Cần hủy chờ duyệt trước"
        if media == True:
            return redirect(URL('multi_media', user_signature=True))
        else:
            return redirect(URL('index', user_signature=True))
    data = data.select()
    category = db((db.clsb_category.category_type == db.clsb_product_type.id) & ~(db.clsb_category.category_parent == None))(db.clsb_product_type.type_name.like("Application")).select()
    creator = db(db.clsb20_dic_creator_cp.id==data[0].product_creator).select()
    creator_list =  db(db.clsb20_product_metadata_cp.product_code == data[0].product_code)\
            (db.clsb_dic_metadata.id == db.clsb20_product_metadata_cp.metadata_id)\
            (db.clsb_dic_metadata.metadata_name.like("co_author")).select()
    creator_name = creator[0]['creator_name']
    for creat in creator_list:
        creator_name += ";"+creat['clsb20_product_metadata_cp']['metadata_value']
    media_tag = "";
    if media == True:
        media_tag = (TR(
            TD(LABEL(XML("Dữ liệu đa phương tiện <br/>(ZIP file): "), _class="clsb_label_product"), _class="rows-left"),
            TD(
                INPUT(_name="data_media", _class="clsb_input_product", _accept=".zip", _type="file", _style="display: none;"),
                DIV(XML("<b>+</b> Chọn tệp tin ZIP"), _class="btn", _onclick="opendata('data_media', event)")
            )
        ),
        TR(
            TD(LABEL("Thư mục chứa dữ liệu: ", _class="clsb_label_product"), _class="rows-left"),
            TD(
                INPUT(_name="dic_media", _class="clsb_input_product", style=""),
                DIV(I("Ví dụ: '/sdcard/app_data', Tất cả dữ liệu trong file ZIP sẽ được đưa vào thư mục này khi cài đặt"), _style="font-size: 12px; color: rgb(0, 130, 250); font-weight: bold;")
            )
        ))
    publisher = db(db.clsb_dic_publisher.id==data[0].product_publisher).select()
    images = db(db.clsb20_product_image.product_code == data[0].product_code).select()
    form = FORM(
        DIV(
            TABLE(
                TR(
                    TD(
                        A(
                            DIV(
                                SPAN(_class="icon leftarrow icon-arrow-left"),
                                " Quản lý ứng dụng", _class="btn"
                            ),
                            _href=URL(user_signature=True)
                        ),
                    ),
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Tên ứng dụng: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_style="width: 100%;", _name="title", _value=data[0].product_title,_class="clsb_input_product", requires=IS_NOT_EMPTY()),
                                )
                            ),
                            TR(
                                TD(LABEL("Package: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_style="margin-top: 10px; width: 60%;", _idvalue=data[0].id, _value=data[0].product_code, _placeholder="com.tvb.example", _name="package", _link=URL(a='cps', c='products', f='check_package.json'), _class="clsb_input_product", _disabled=True),
                                    #SPAN("Check Validation", _class="btn", _onclick="check_package()")
                                )
                            ),
                            TR(
                                TD(LABEL("Thể loại ứng dụng: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(SELECT(*[OPTION(i['clsb_category']['category_name'], _value=str(i['clsb_category']['id']), _selected=True if i['clsb_category']['id'] == data[0].product_category else False) for i in category], _style="margin-top: 5px;",_class="clsb_input_product",_name="category"))
                            ),
                            TR(
                                TD(LABEL("Mô tả chi tiết: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(TEXTAREA(data[0].product_description, _name="content", _class="clsb_input_product"))
                            ),
                            _style="width: 100%;"
                        ),
                        _class="clsb_upload_border"
                    )
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(
                                    TABLE(
                                        TR(
                                            # TD(
                                            #     SPAN(XML("Ảnh bìa cỡ<br/>(100x100)px")),
                                            #     XML("<br/>"),
                                            #     INPUT(_name="thumbnail", _class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;"),
                                            #     DIV(_style="background-image: url("+URL(a='cpa',c='download', f='cover',args=[user_cp_path, 'upload', data[0].product_code, 'thumb.png'])+")", _class="clsb_image thumbnail_cp app", _onclick="openimage('thumbnail',event,true)"),
                                            # ),
                                            TD(
                                                SPAN("Ảnh bìa (150x150, 200x200, 300x300,...)px"),
                                                XML("<br/>"),
                                                INPUT(_name="cover",_class="clsb_input_product", _accept="image/*", _type="file", _style="display: none;"),
                                                DIV(_style="background-image: url("+URL(a='cpa',c='download', f='cover',args=[user_cp_path, 'upload', data[0].product_code, 'cover.clsbi'])+")", _class="clsb_image cover app", _onclick="openimage('cover',event,true)"),
                                            ),
                                        )
                                    ),
                                    TABLE(
                                        TR(
                                            TD(
                                                SPAN("Ảnh mô tả (Tối đa 5 ảnh - kích cỡ < 1MB)"),
                                                DIV(
                                                    INPUT(_name="removefimages", _id="feature_images", _class="clsb_input_product", _type="text", _style="display: none;", _multiple=True),
                                                    INPUT(_name="feature_images_1", _id="feature_images_1", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    INPUT(_name="feature_images_2", _id="feature_images_2", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    INPUT(_name="feature_images_3", _id="feature_images_3", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    INPUT(_name="feature_images_4", _id="feature_images_4", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    INPUT(_name="feature_images_5", _id="feature_images_5", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
                                                    DIV(XML("Xóa dữ liệu ảnh cũ"), _class="btn", _onclick="removeimages('removefimages','#imglist')"),
                                                    DIV(XML("Thêm ảnh"), _class="btn", _onclick="addimagesborder('#imglist')"),
                                                    XML("<br/>"),
                                                    DIV(
                                                        *[XML("<img src="+URL(a='cpa',c='download', f='image',args=[user_cp_path, 'upload', images[i].image])+"  class='clsb_image fimages'  style='padding-top: 0px;'/>") for i in range(len(images))],
                                                        _id="imglist",
                                                        _class="border_imglist"
                                                    ),
                                                    _style="overflow: auto;"
                                                )

                                            )
                                        )
                                    )
                                )
                            ),
                            _style="width: 100%;"
                        ),
                        _class="clsb_upload_border"
                    )
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Dữ liệu ứng dụng (APK file): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_name="data",_class="clsb_input_product", _accept=".apk", _type="file", _style="display: none;"),
                                    DIV(XML("<b>+</b> Chọn tệp tin APK Thay thế"), _class="btn", _onclick="opendata('data', event)"),
                                    XML("<br/>"),
                                    A(SPAN("Tải về: "+data[0].product_code+".ZIP",_class="btn"), _href="/cpa/download/file/"+user_cp_path+"/upload/"+data[0].product_code+"/"+data[0].product_code+".zip")
                                )
                            ),
                            media_tag,
                            _style="width: 100%;"
                        ),
                        _class="clsb_upload_border"
                    )
                ),
                INPUT(_type="submit", _class="clsb_submit_upload", _value="Hoàn thành"),
                _class="clsb_table_product"
            ),
        ),
        _class="clsb_form_upload"
    )
    if form.accepts(request, session):
        code = data[0].product_code
        products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code, settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"_Backup", True)
        device_shelf_code = db(db.clsb_device_shelf.id == db.clsb20_category_shelf_mapping.device_shelf_id)(db.clsb20_category_shelf_mapping.category_id == request.vars.category).select()
        db(db.clsb20_product_cp.id == id).update(
            product_title=request.vars.title,
            product_description=request.vars.content,
            product_category=request.vars.category,
            device_shelf_code=device_shelf_code.first()['clsb_device_shelf']['id'],
            product_status="Init",
        )
        if request.vars.cover != "":
            if request.vars.cover.file:
                try:
                    save_file(request.vars.cover.file, data[0].product_code+"/cover.clsbi")
                    zip_file = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "r")
                    zip_out = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"_new.zip", "w")
                    file_cover = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/cover.clsbi")
                    for item in zip_file.infolist():
                        buffer = zip_file.read(item.filename)
                        if item.filename.find('cover.clsbi') >= 0:
                            zip_out.writestr(item, file_cover.read())
                        else:
                            zip_out.writestr(item, buffer)
                    file_cover.close()
                    zip_out.close()
                    os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip")
                    os.rename(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"_new.zip", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip")
                    zip_file.close()
                except Exception as e:
                    print e
        if request.vars.data != "":
            if request.vars.data.file:
                try:
                    os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip")
                except Exception as e:
                    print e
                create_dir(user_cp_path+"/upload/"+code+"/"+code)
                create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code)
                save_file(request.vars.data.file, code+"/"+code+"/"+code+"/"+code+".apk")
                try:
                    products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/cover.clsbi")
                except:
                    response.flash = "Thiếu cover"
                    return dict(form=form)
                if media == True:
                    if bool(request.vars.data_media.file) & bool(request.vars.dic_media):
                        if request.vars.dic_media != "":
                            save_file(request.vars.data_media.file, code+"/"+code+"/"+code+"/"+code+"_media.zip")
                            with zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+"_media.zip", "r") as z:
                                z.extractall(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code)
                                z.close()
                            os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+"_media.zip")
                            f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/config.cfg", "w")
                            f.writelines("des="+request.vars.dic_media+"\n")
                            f.writelines("type=Normal")
                            f.flush()
                            f.close()
                        else:
                            shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                            products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"_Backup", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code, True)
                            session.flash = "Chưa định dạng đường dẫn cho dữ liệu mở rộng"
                            return dict(form=form)
                z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "w")
                zipdir(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code, z)
                z.close()
                shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code)

        shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/thumb.png")

        if request.vars.removefimages != "":
            imagedelete = db(db.clsb20_product_image.product_code == data[0].product_code).select()
            for i in imagedelete:
                try:
                    os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"
                                                     ""+i.image)
                except:
                    continue

                db(db.clsb20_product_image.product_code==data[0].product_code).delete()

        type_image = db(db.clsb20_image_type.name.like("Features")).select()
        if len(type_image) <= 0:
            type_image = db.clsb20_image_type.insert(name="Features", description="Features Images")
        else:
            type_image = type_image[0]
        for i in range(1, 6):
            if request.vars['feature_images_'+str(i)] != "":
                try:
                    file = request.vars['feature_images_'+str(i)]
                    save_file(file.file, "clsb20_product_cp."+data[0].product_code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                    db.clsb20_product_image.insert(type_id=type_image['id'], product_code=data[0].product_code,description=file.filename,image="clsb20_product_cp."+data[0].product_code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                except:
                    continue
        session.flash = 'Cập nhật thành công'
        return redirect(URL('index' if media != True else 'multi_media',args=['view','clsb20_product_cp', id], user_signature=True))
    elif form.errors:
        response.flash = 'Lỗi: Thông tin không đúng'
    else:
        response.flash = 'Xin mời điền thông tin'

    return dict(form=form)


@auth.requires_signature()
def view_product(media=False):
    id = request.args[2]
    data = db(db.clsb20_product_cp.id == id).select()
    relation = db(db.clsb20_product_relation_cp.product_cp_id == id).select()
    images = db(db.clsb20_product_image.product_code == data[0].product_code).select()
    metadata = db(db.clsb20_product_metadata_cp.product_code == data[0].product_code).select()
    payment_type = db(~db.clsb20_purchase_type.name.like("Subscriptions")).select()
    subscriptions = db(db.clsb20_purchase_item.purchase_type == db(db.clsb20_purchase_type.name.like("Subscriptions")).select()[0].id).select()

    payment = db(db.clsb20_product_purchase_item.product_code.like(data[0].product_code)).select()
    purchase_type = db(db.clsb20_purchase_item.id == payment[0].purchase_item).select()
    if request.vars.request_data:
        if request.vars.request_data.upper() == "SUBSCRIPTIONS":
                purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
        else:
            purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.request_data)).select()[0].id
            purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id
        price = data[0].product_price
        if request.vars.request_data.upper() == "FREE":
            price = 0
            db(db.clsb20_product_cp.product_code == data[0].product_code).update(product_price=price)
            db(db.clsb_product.product_code == data[0].product_code).update(product_price=price)
        data = db(db.clsb20_product_cp.id == id).select()
        db(db.clsb20_product_purchase_item.id == payment[0]['purchase_item']).update(purchase_item=purchase_item)
        db.clsb20_product_price_history.insert(product_id=id, purchase_item=purchase_item, price=price, changing_time=datetime.now())
        session.flash = "Thành công"
        return "OK"


    purchase_dict_type = db(db.clsb20_purchase_type.id == purchase_type[0].purchase_type).select()
    btnchangeprice = purchase_type[0].description

    if (purchase_dict_type[0]['name'].upper() != "SUBSCRIPTIONS") | (data[0].product_status.upper() != "PUBLISHED"):
        btnchangeprice = FORM(
            SELECT(*[OPTION(payment_type[i].description, _value=str(payment_type[i].name), _selected=True if payment_type[i].id == purchase_dict_type[0].id else False) for i in range(len(payment_type))], _id="payment", _style="width:250px; margin-top: 5px", _class="clsb_input_product", _name="payment"),
            # SELECT(*[OPTION(subscriptions[i].description, _value=str(subscriptions[i].id), _selected=True if subscriptions[i].id == purchase_type[0].id else False) for i in range(len(subscriptions))], _style="width:250px; margin-top: 5px; display: none;", _class="clsb_input_product", _name="payment_more",_id="payment_more"),
            # DIV(B("* Chú ý: "), XML("Khi chọn phương thức <b>Thanh toán theo thời gian</b> sẽ không thể đổi sang hình thức thanh toán khác khi đã được duyệt"), _style="width:250px;"),
            DIV(INPUT(_type="submit", _class="btn", _value="Đổi hình thức thu phí")),
            _action="javascript:submit_c('Bạn có muốn đổi hình thức thu phí?','"+URL(a='cpa', c='products', f='index' if media != True else 'multi_media', args=request.args)+"','payment')"
            # _style="white-space: normal; text-align: justify;"
        )

    if request.vars.reply:
        if request.vars.reply != "":
            db.clsb20_review_comment.insert(user_id=auth.user.id, product_code=data[0].product_code, comment_time=datetime.now(), review_comment=request.vars.reply)

    cmtdb = db(db.clsb20_review_comment.product_code == data[0].product_code)\
            (db.auth_user.id == db.clsb20_review_comment.user_id).select(db.clsb20_review_comment.ALL, db.auth_user.ALL)
    reject = TR(
        TD(
            LABEL(B("Thông tin phản hồi"), _class="clsb_label_product"),
            DIV(
                DIV(
                    SPAN("Không có phản hồi" if len(cmtdb) <= 0 else ""),
                    DIV(
                        *[DIV(
                            DIV(cmtdb[i]['auth_user']['last_name']+" "+cmtdb[i]['auth_user']['first_name']+" - "+str(cmtdb[i]['clsb20_review_comment']['comment_time']), _class="user"),
                            DIV(cmtdb[i]['clsb20_review_comment']['review_comment'], _class="content"),
                            _class='left' if (cmtdb[i]['auth_user']['id'] == auth.user.id) | (cmtdb[i]['auth_user']['id'] == usercp.user_get_id_cp(auth.user.id, db)) else 'right'
                        ) for i in range(len(cmtdb))]
                    ),
                    DIV(_class="clr"),
                    _class="border_msg"
                ),
                FORM(
                    INPUT(_name="reply", _style="margin-top: 10px;"),
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
                        " Quản lý ứng dụng", _class="btn"
                    ),
                    _href=URL()
                ),
                SPAN(" "),
                A(
                    DIV(
                        SPAN(_class="icon pen icon-pencil"),
                        " Cập nhật thông tin", _class="btn"
                    ),
                    _href=URL('index' if media != True else 'multi_media',args=['edit','clsb20_product_cp',id], user_signature=True),
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
                        TD(LABEL("Tiêu đề sách: ",_class="clsb_label_product")),
                        TD(LABEL(data[0].product_title,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Chuyên mục: ",_class="clsb_label_product")),
                        TD(LABEL(db(db.clsb_category.id==data[0].product_category).select()[0].category_name,_class="clsb_label_product"))
                    ),
                    # TR(
                    #     TD(LABEL("Giá sách: ",_class="clsb_label_product")),
                    #     TD(LABEL(db(db.clsb_device_shelf.id==data[0].device_shelf_code).select()[0].device_shelf_name,_class="clsb_label_product"))
                    # ),
                    TR(
                        TD(LABEL("Tác giả: ",_class="clsb_label_product")),
                        TD(LABEL(db(db.clsb20_dic_creator_cp.id==data[0].product_creator).select()[0].creator_name,_class="clsb_label_product"))
                    )
                    ,
                    TR(
                        TD(LABEL("Nhà cung cấp: ",_class="clsb_label_product")),
                        TD(LABEL(db(db.clsb_dic_publisher.id==data[0].product_publisher).select()[0].publisher_name,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Mô tả chi tiết: ",_class="clsb_label_product")),
                        TD(LABEL(data[0].product_description, _class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Thông tin mở rộng: ",_class="clsb_label_product")),
                        TD(
                            SPAN("Thông tin metadata", _class="btn", _onclick="showmetadata()"),XML(" "),A(SPAN("Sửa", _class="btn"),_href=URL(a='cpa',c='products',f='metadata',args=[data[0].product_code], user_signature=True)),
                            DIV(
                                TABLE(
                                    *[TR(TD(db(db.clsb_dic_metadata.id==metadata[i].metadata_id).select()[0].metadata_label+": "), TD(metadata[i].metadata_value)) for i in range(len(metadata))]
                                ),
                                _class="clsb_metadataview", _id="clsb_metadataview"
                            )
                        )
                    ),
                    TR(
                        TD(LABEL("Giá tiền: ",_class="clsb_label_product", _style="font-weight: bold;")),
                        TD(
                            A(BUTTON("Lịch sử đổi giá", _class="btn"), _href=URL(a='cpa', c='price', f='history', vars=dict(product_id=data[0].id), user_signature=True)),
                            FORM(INPUT(_value=str(data[0].product_price), _id="price_change", _style="text-align: right;min-width: 10px; width: 150px; margin-top: 10px; color: rgb(255, 112, 0); font-weight: bold;", _class="clsb_input_product")+"₫ ", INPUT(_type="submit", _value="Đổi giá", _style="width: 80px;", _class="btn"), _action="javascript:submit_c('Bạn có muốn thay đổi giá tiền?', '"+URL('change_price', args=[data[0].id])+"','price_change')", _method="GET", _style="color: rgb(255, 112, 0);"),
                        )
                    ),
                    TR(
                        TD(LABEL("Cách thức thu phí: ", _class="clsb_label_product")),
                        TD(DIV(btnchangeprice))
                    ),
                    TR(
                        TD(LABEL("ZIP file: ",_class="clsb_label_product")),
                        TD(A(SPAN("Tải về: "+data[0].product_code+".ZIP", _class="btn", _style="max-width: 200px; display: inline-block; text-overflow: "), _href="/cpa/download/file/"+user_cp_path+"/upload/"+data[0].product_code+"/"+data[0].product_code+".zip"))
                    )
                ),
                _class="clsb_upload_border"
            ),
            TD(
                TABLE(
                    TR(
                        TD(LABEL("Ảnh minh họa: ",_class="clsb_label_product")),
                        TD(
                            DIV(
                                *[IMG(_src="/cpa/download/image/"+user_cp_path+"/upload/"+images[i].image) for i in range(len(images))],
                                _class="border_imglist_large"
                            )
                        )
                    ),
                    TR(
                        TD(LABEL("Sản phẩm liên quan: ",_class="clsb_label_product")),
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
                    ),
                    reject
                ),
                _class="clsb_upload_border"
            )
        ),
        _class="clsb_table_product"
    )
    return dict(form=form)

@auth.requires_signature()
def metadata():
    links = [{
                'header': 'Tên thông tin',
                'body': lambda row: [
                    db(db.clsb_dic_metadata.id == row.metadata_id).select()[0].metadata_label
                ]
        }]

    if request.url.find('/metadata/view/') >= 0:
        links = []
    elif request.url.find('/metadata/edit/') >= 0:
        links = []
    elif request.url.find('/metadata/new/') >= 0:
        return newmetadata(session['product_code'])
    else:
        session['product_code'] = request.args[0]
    copy_metadata(session['product_code'])
    form = SQLFORM.grid(
        db.clsb20_product_metadata_cp.product_code == request.args[0],
        links=links
    )
    return dict(form=form)

def copy_relation(code):
    try:
        product_public = db(db.clsb_product.product_code == code)
        product = db(db.clsb20_product_cp.product_code==code).select()[0]
        if len(product_public.select()) > 0:
            id = product_public.select()[0].id
            db(db.clsb_product_relation.product_id==id).delete()
            relation = db(db.clsb20_product_relation_cp.product_cp_id==product.id).select()
            for item in relation:
                db.clsb_product_relation.insert(product_id = id, relation_id = item.relation_id)
        return "OK"
    except Exception as ex:
        return 'Error: '+ex.message

def copy_metadata(code):
    try:
        product_public = db(db.clsb_product.product_code == code)
        product = db(db.clsb20_product_cp.product_code==code).select()[0]
        if len(product_public.select()) > 0:
            id = product_public.select()[0].id
            db(db.clsb_product_metadata.product_id==id).delete()
            relation = db(db.clsb20_product_metadata_cp.product_code==product.product_code).select()
            for item in relation:
                db.clsb_product_metadata.insert(product_id = id, metadata_id = item.metadata_id, metadata_value=item.metadata_value)
        return "OK"
    except Exception as ex:
        return 'Error: '+ex.message

def newmetadata(code):
    metadata = db(db.clsb_dic_metadata).select()
    form = FORM(
        TABLE(
            TR(
              TD(
                  A(SPAN("Quay lại",_class="btn"),_href=URL('metadata', args=[code], user_signature=True)),XML("<br/>")
              ),
              TD()
            ),
            TR(
                TD(LABEL("Product Code:")),
                TD(INPUT(_value=code, _disabled=True))
            ),
            TR(
                TD(LABEL("Tên:")),
                TD(SELECT(*[OPTION(metadata[i].metadata_label, _value=metadata[i].id) for i in range(len(metadata))], _name="metadata_id"))
            ),
            TR(
                TD(LABEL("Giá trị:")),
                TD(TEXTAREA(_name="metadata_value"))
            ),
            TR(
                TD(),
                TD(INPUT(_type="Submit"))
            )
        )
    )
    if form.accepts(request, session):
        db.clsb20_product_metadata_cp.insert(product_code=code, metadata_id=request.vars.metadata_id, metadata_value=request.vars.metadata_value)
        result = copy_metadata(code)
        if result == "OK":
            response.flash = "Thành công"
        else:
            response.flash = result
    if form.errors:
        response.flash = "Lỗi"
    return dict(form=form)


def change_price():
    try:
        id = request.args[0]
        price = request.vars.request_data
        dbproduct = db(db.clsb20_product_cp.id == id)
        product = dbproduct.select()[0]

        product_public = db(db.clsb_product.product_code == product.product_code)
        purchase_item = db(db.clsb20_product_purchase_item.product_code.like(product.product_code)).select()[0]
        if db(db.clsb20_purchase_item.id == purchase_item['purchase_item']).select()[0]['name'].upper() == "FREE":
            price = 0
        dbproduct.update(product_price=int(price))
        db.clsb20_product_price_history.insert(product_id=id, purchase_item=purchase_item['purchase_item'], price=price, changing_time=datetime.now())
        if len(product_public.select()) > 0:
            product_public.update(product_price=int(price))
        session.flash = "Thành công"
        return "OK"
    except Exception as ex:
        session.flash = "Error: "+ex.message
    return "OK"
    # return redirect(URL('index', args=['view', 'clsb20_product_cp', product.id], user_signature=True))


@auth.requires_signature()
def topending():
    id = request.args[0]
    media = 0
    if len(request.args) > 1:
        media = int(request.args[1])
    data = db(db.clsb20_product_cp.id == id)
    if data.select()[0].product_status == "Pending":
        session.flash = "Ứng dụng đang được kiểm duyệt"
    else:
        result = products.validate_zip(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data.select()[0].product_code+"/"+data.select()[0].product_code+".zip", "Application")
        if result == "OK":
            data.update(
                product_status='Submit'
            )
            list_report = db(db.auth_user.id == db.clsb20_user_report_list.user_id)\
                    (db.clsb20_user_report_list.report_type == db.clsb20_user_report_type.id)\
                    (db.clsb20_user_report_type.code.like("REVIEW")).select(groupby=db.auth_user.id)
            for user in list_report:
                send_mail_report_to_review(id, user['auth_user']['email'])
            session.flash = 'Thành công'
        else:
            session.flash = result
    if media == 1:
        return redirect(URL('multi_media', user_signature=True))
    else:
        return redirect(URL('index', user_signature=True))


def send_mail_report_to_review(product_id, email):

    try:
        product_info = db(db.clsb20_product_cp.id == product_id).select().first()
        product_category = db(db.clsb_category.id == product_info['product_category']).select().first()

        message = '<html>'
        message += 'Thông tin chi tiết <br>'
        message += 'Tiêu đề sản phẩm : ' + str(product_info['product_title']) + '.<br>'
        message += 'Mã sản phẩm : ' + str(product_info['product_code']) + '.<br>'
        message += 'Loại : ' + str(product_category['category_name']) + '<br>'
        message += 'Giá : ' + str(product_info['product_price']) + ' VNĐ<br>'
        message += 'Thời gian: ' + str(strftime("%Y-%m-%d %H:%M:%S", gmtime())) + ' <br>'
        message += '</html>'
        subject = 'Thông báo sách mới đệ trình'

        try:
            mail.send(to=[email], subject=subject, message=message)
            return "OK"
        except Exception as e:
            print str(e)
            return dict(error="Lỗi gửi email")
    except Exception as e:
        raise HTTP(200, "Send Mail Error: "+e.message+" on line: "+str(sys.exc_traceback.tb_lineno))


@auth.requires_signature()
def disablepending():
    id = request.args[0]
    data = db(db.clsb20_product_cp.id==id)
    dbproduct = data.select()[0]
    if dbproduct.product_status == "Pending":
        session.flash = "Ứng dụng đang được kiểm duyệt"
    else:
        try:
            db(db.clsb_product.product_code.like(dbproduct.product_code)).update(product_status="Pending")
            shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/review/"+dbproduct.product_code)
            # shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/published/"+dbproduct.product_code)
        except:
            pass
        data.update(
            product_status='Cancel'
        )
        session.flash = 'Thành công'
    return "OK"
    # return redirect(URL('index', user_signature=True))


@auth.requires_signature()
def remove_product(media=False):
    id = request.args[2]
    #data = db(db.clsb20_product_cp.id==id)
    #if data.select()[0].product_status == "Pending":
    #    session.flash = "Sách ?ang ???c ki?m duy?t"
    #    return redirect(URL('index', user_signature=True))
    data = db(db.clsb20_product_cp.id==id).select()
    imagedelete = db(db.clsb20_product_image.product_code==data[0].product_code).select()
    for i in imagedelete:
        try:
            os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+i.image)
        except:
            continue

    db(db.clsb20_product_image.product_code == data[0].product_code).delete()
    db(db.clsb20_product_cp.product_code == data[0].product_code).update(product_status="CPDelete")
    db(db.clsb_product.product_code == data[0].product_code).update(product_status="CPDelete")
    try:
        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code)
        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"_Backup")
        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/review/"+data[0].product_code)
        # shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/published/"+data[0].product_code)
        session.flash = 'Xóa Thành công'
    except Exception as e:
        session.flash = "Không tồn tại thư mục"
    if media == True:
        redirect(URL("multi_media", user_signature=True))
    else:
        redirect(URL("index", user_signature=True))


def create_dir(directory):
    if URL().find('create_dir') >= 0:
        raise HTTP(404)
    if not os.path.exists(settings.home_dir+settings.cp_dir+directory):
        os.makedirs(settings.home_dir+settings.cp_dir+directory)


def zipdir(path, zip):
    rootlen = len(path) + 1
    for base, dirs, files in os.walk(path):
        for file in files:
            fn = os.path.join(base, file)
            zip.write(fn, fn[rootlen:])


@auth.requires_authorize()
def developers():
    if request.url.find('/new/clsb20_product_cp') >= 0:
            return create_app()
    if request.url.find('/view/clsb20_product_cp') >= 0:
            return view_app()
    if request.url.find('/delete/clsb20_product_cp') >= 0:
            return remove_product()
    try:
        query = None
        user_info = usercp.user_get_info(auth.user.id, db)
        if user_info['user_info']['is_admin'] == True:
            query = db(~db.clsb20_product_cp.product_status.like("%delete%"))\
                        ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Application")))\
                        ((db.clsb_category.id == db.clsb20_product_cp.product_category) & (((db.auth_user.created_by == auth.user.id) & (db.auth_user.id == db.clsb20_product_cp.created_by)) | (db.clsb20_product_cp.created_by == auth.user.id)))
        else:
            query = db((~db.clsb20_product_cp.product_status.like("%delete%")) & (db.clsb20_product_cp.created_by == auth.user.id))\
                        ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Application")))\
                        (db.clsb_category.id == db.clsb20_product_cp.product_category)

        if request.vars.keyword:
            keyword = request.vars.keyword
            search = ((db.clsb20_product_cp.product_code == keyword)\
                        | (db.clsb20_product_cp.product_title.like('%' + keyword + '%'))\
                        | (db.clsb20_dic_creator_cp.creator_name.like('%' + keyword + '%'))\
                        | (db.clsb_dic_publisher.publisher_name.like('%' + keyword + '%')))

            query = query(search)

        product_list = query.select(groupby=db.clsb20_product_cp.id, orderby=~db.clsb20_product_cp.created_on)
        return dict(user_cp_path=user_cp_path, product_list=product_list)
    except Exception as e:
        print e
        pass


def view_app():
    id = request.args[2]
    purchase_item = db(db.clsb20_purchase_item.purchase_type == db.clsb20_purchase_type.id)\
                    (db.clsb20_purchase_type.name.like("Subscriptions")).select()
    data = db(db.clsb20_product_cp.id == id).select()
    subscriptions = db(db.clsb20_purchase_item.purchase_type == db(db.clsb20_purchase_type.name.like("Subscriptions")).select()[0].id).select()
    query = db(db.clsb20_product_purchase_item.product_code.like(data[0].product_code))\
                (db.clsb20_product_purchase_item.purchase_item == db.clsb20_purchase_item.id)\
                (db.clsb20_purchase_item.purchase_type == db.clsb20_purchase_type.id)\
                (db.clsb20_purchase_type.name.like("Subscriptions"))
    if request.vars.purchase_type:
        if request.vars.purchase_type != "":
            print db(db.clsb20_product_purchase_item.id == query.select()[0]['clsb20_product_purchase_item']['id']).update(purchase_item=int(request.vars.purchase_type))

    payment = query.select()
    if request.vars.purchase_yes:
        try:
            tmp = list()
            for item in payment:
                tmp.append(item['clsb20_product_purchase_item']['id'])
            db(db.clsb20_product_purchase_item.id.belongs(tmp)).delete()

            if request.vars.purchase_yes == "1":
                list_purchase = list()
                list_price = list()
                for i in range(0, len(purchase_item)):
                    if request.vars['purchase_'+str(i)]:
                        list_purchase.append(request.vars['purchase_'+str(i)])
                        list_price.append(request.vars['price_'+str(i)])
                _flag = False
                for i in range(0, len(list_purchase)-1):
                    for j in range(i+1, len(list_purchase)):
                        if list_purchase[i] == list_purchase[j]:
                            _flag = True
                            response.flash = 'Upload Fail: Có nhiều hơn hoặc bằng 2 kiểu thanh toán giống nhau'
                        # d1 = db(db.clsb20_purchase_item.id == list_purchase[i]).select()[0]['duration']
                        # d2 = db(db.clsb20_purchase_item.id == list_purchase[j]).select()[0]['duration']
                        # p = 1
                        # if d1 > d2:
                        #     p = d1/d2
                        # else:
                        #     p = d2/d1
                        # if ((d2 > d1) & (int(list_price[j]) > (int(list_price[i])*p))) or ((d2 < d1) & ((p*int(list_price[j])) < int(list_price[i]))):
                        #     _flag = True
                        #     response.flash = 'Upload Fail: Số tiền trả cho thời gian dài hơn phải ít hơn'
                if not _flag:
                    for i in range(0, len(list_purchase)):
                        db.clsb20_product_purchase_item.insert(product_code=data[0].product_code, purchase_item=list_purchase[i], price=int(list_price[i]))
                    response.flash = "Thành công"
                else:
                    pass
            else:
                response.flash = "Thành công"

        except Exception as ex:
            response.flash = 'Lỗi: Thông tin không đúng'
    payment = query.select()
    form = FORM(
        A(" Quay lại", _href=URL(user_signature=True), _class="btn"), XML("<br/><br/>"),
        TABLE(
            TR(
                TD(LABEL("Tên ứng dụng: ")),
                TD(data[0]['product_title'])
            ),
            TR(
                TD(LABEL("Mã ứng dụng: ")),
                TD(data[0]['product_code'])
            ),
            TR(
                TD("Hình thức thanh toán nội dung số: "),
                TD(
                    SELECT(
                        OPTION("Không", _selected=True if len(payment) <= 0 else False, _value="0"),
                        OPTION("Có",  _selected=True if len(payment) > 0 else False, _value="1"),
                        _style="margin-top: 10px; width: 60%;",
                        _id='purchase_yes',
                        _name='purchase_yes'
                    )
                )
            ),
            TR(
                TD(),
                TD(
                    *[DIV(
                        DIV(
                            SELECT(
                                *[OPTION(item['clsb20_purchase_item']['description'], _value=item['clsb20_purchase_item']['id'], _selected=True if payment[i]['clsb20_product_purchase_item']['purchase_item'] == item['clsb20_purchase_item']['id'] else False) for item in purchase_item],
                                _name='purchase_'+str(i),
                                _style="margin-top: 10px; width: 60%;"
                            ),XML('<br/>'),
                            INPUT(_name="price_"+str(i), _placeholder="Số tiền", _value="0" if not payment[i] else payment[i]['clsb20_product_purchase_item']['price'], _style="font-weight: bold; color: rgb(255, 112, 0);"),
                            XML('<br/>'),DIV("Thêm", _class="btn", _style="margin-top: -10px;", _onclick="show_more_purchase("+str(i+1)+")") if i < (len(purchase_item)-1) else "",
                            _id='purchase_'+str(i)
                        ),
                    ) for i in range(0, len(payment))],
                    _class="id_purchase"
                )
            ),
            TR(
                TD(),
                TD(
                    *[DIV(
                        DIV(
                            SELECT(
                                *[OPTION(item['clsb20_purchase_item']['description'], _value=item['clsb20_purchase_item']['id']) for item in purchase_item],
                                    _name='purchase_'+str(i),
                                    _style="margin-top: 10px; width: 60%;",
                                    _disabled=True if i > 0 else False
                            ),XML('<br/>'),
                            INPUT(_name="price_"+str(i), _placeholder="Số tiền", _style="font-weight: bold; color: rgb(255, 112, 0);"),
                            XML('<br/>'),DIV("Thêm", _class="btn", _style="margin-top: -10px;", _onclick="show_more_purchase("+str(i+1)+")") if i < (len(purchase_item)-1) else "",
                            _style="display: none;"  if i > 0 else "",
                            _id='purchase_'+str(i)
                        )
                    ) for i in range(len(payment), len(purchase_item))],
                    _class="id_purchase"
                )
            ),
            TR(
                TD(),
                TD(INPUT(_value="Cập nhật", _type="submit", _class="btn"))
            ),
            _class="clsb_upload_border",
            _style="padding: 10px;"
        ),
        _class="clsb_table_product",
        _style="width: 60%; margin: 5px auto;"
    )
    return dict(form=form)


def create_app():
    purchase_item = db(db.clsb20_purchase_item.purchase_type == db.clsb20_purchase_type.id)\
                    (db.clsb20_purchase_type.name.like("Subscriptions")).select()
    form = FORM(
        DIV(
            TABLE(
                TR(
                    TD(
                        A(
                            DIV(
                                SPAN(_class="icon leftarrow icon-arrow-left"),
                                " Quản lý ứng dụng", _class="btn"
                            ),
                            _href=URL(user_signature=True)
                        ),
                    ),
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Tên ứng dụng: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_style="width: 100%;", _name="title", _class="clsb_input_product", requires=IS_NOT_EMPTY()),
                                )
                            ),
                            TR(
                                TD(LABEL("Tên package: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_style="margin-top: 10px; width: 60%;", _placeholder="com.tvb.example", _name="package", _idvalue=auth.user.id, _link=URL(a='cps',c='products',f='check_package.json'), _class="clsb_input_product", requires=IS_NOT_EMPTY()),
                                    SPAN("Check Validation", _class="btn", _onclick="check_package()")
                                )
                            ),
                            TR(
                                TD(LABEL("Bán kèm nội dung số: ", _class="clsb_label_product", _style="font-weight: bold;"), _class="rows-left"),
                                TD(
                                    SELECT(
                                        OPTION("Không", _value="0"),
                                        OPTION("Có", _value="1"),
                                        _style="margin-top: 10px; width: 60%;",
                                        _id='purchase_yes',
                                        _name='purchase_yes'
                                    )
                                )
                            ),
                            TR(
                                TD(),
                                TD(
                                    *[DIV(
                                        DIV(
                                            SELECT(
                                                *[OPTION(item['clsb20_purchase_item']['description'], _value=item['clsb20_purchase_item']['id']) for item in purchase_item],
                                                _name='purchase_'+str(i),
                                                _style="margin-top: 10px; width: 60%;",
                                                _disabled=True if i > 0 else False
                                            ), XML("<br/>"),
                                            INPUT(_name="price_"+str(i), _placeholder="Số tiền", _style="font-weight: bold; color: rgb(255, 112, 0);"), "VNĐ", XML("<br/>"),
                                            DIV("Thêm", _class="btn", _style="margin-top: -10px;", _onclick="show_more_purchase("+str(i+1)+")") if i < (len(purchase_item)-1) else "",
                                            _style="display: none;" if i > 0 else "",
                                            _id='purchase_'+str(i)
                                        )
                                    ) for i in range(0, len(purchase_item))],
                                    _class="id_purchase"
                                )
                            )
                        ),
                        _class="clsb_upload_border"
                    )
                ),
                TR(
                    TD(
                        INPUT(_type="submit", _value="Submit", _class='clsb_submit_upload')
                    )
                ),
                _class="clsb_table_product"
            )
        )
    )
    if form.accepts(request, session):
        try:
            if request.vars.purchase_yes == "1":
                list_purchase = list()
                list_price = list()
                for i in range(0, len(purchase_item)):
                    if request.vars['purchase_'+str(i)]:
                        list_purchase.append(request.vars['purchase_'+str(i)])
                        list_price.append(request.vars['price_'+str(i)])
                _flag = False
                for i in range(0, len(list_purchase)-1):
                    for j in range(i+1, len(list_purchase)):
                        if list_purchase[i] == list_purchase[j]:
                            _flag = True
                            response.flash = 'Upload Fail: Có nhiều hơn hoặc bằng 2 kiểu thanh toán giống nhau'
                        # d1 = db(db.clsb20_purchase_item.id == list_purchase[i]).select()[0]['duration']
                        # d2 = db(db.clsb20_purchase_item.id == list_purchase[j]).select()[0]['duration']
                        # p = 1
                        # if d1 > d2:
                        #     p = d1/d2
                        # else:
                        #     p = d2/d1
                        # if ((d2 > d1) & (int(list_price[j]) > (int(list_price[i])*p))) or ((d2 < d1) & ((p*int(list_price[j])) < int(list_price[i]))):
                        #     _flag = True
                        #     response.flash = 'Xảy ra lỗi: Số tiền trả cho thời gian dài hơn phải ít hơn'
                if not _flag:
                    newdata = start_add_app(request, session)
                    for i in range(0, len(list_purchase)):
                        db.clsb20_product_purchase_item.insert(product_code=newdata.product_code, purchase_item=list_purchase[i], price=int(list_price[i]))
                    response.flash = "Tải lên thành công"
                else:
                    pass
            else:
                start_add_app(request, session)
                response.flash = "Tải lên thành công"

        except Exception as ex:
            response.flash = "Lỗi khai báo thông tin"
    elif form.errors:
        response.flash = 'Lỗi khai báo thông tin'
    else:
        response.flash = 'Hãy điền vào form dưới'
    return dict(form=form)


def start_add_app(request, session):
    publisher_char = "Developers"
    # code = user_cp_path+db(db.clsb20_product_type.type_name.like("Application")).select()[0].type_code+"."+request.vars.package
    code = request.vars.package
    data_check = db((db.clsb20_product_cp.product_code == code) & ~(db.clsb20_product_cp.product_status.like("%delete%"))).select()
    publisher = db(db.clsb_dic_publisher.publisher_name.like(publisher_char)).select()
    data_check_out = db((db.clsb20_product_cp.product_code.like(request.vars.package)) & ~(db.clsb20_product_cp.created_by == auth.user.id)).select()
    data_check_store = db((db.clsb_product.product_code.like(request.vars.package)) & ~(db.clsb_product.product_code == code)).select()
    if len(publisher) <= 0:
        publisher = db.clsb_dic_publisher.insert(publisher_name=publisher_char)
    else:
        publisher = publisher[0]
    if len(request.vars.package.split(".")) < 3:
        response.flash = "Sai package name"
    elif (len(data_check_store) > 0) or (len(data_check_out) > 0) or (len(data_check) > 0):
        response.flash = "Package name đã tồn tại"
    else:
        creator_list = ["Developers"]
        creator = dict()
        add_creator = ""
        metadata_id = db(db.clsb_dic_metadata.metadata_name.like("co_author")).select()[0]['id']
        for creat in creator_list:
            if creat != "":
                if add_creator == "":
                    creator = db(db.clsb20_dic_creator_cp.creator_name == creat).select()
                    add_creator = creat
                else:
                    db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=code, metadata_value=creat)

        if len(creator) <= 0:
            creator = db.clsb20_dic_creator_cp.insert(creator_name=add_creator)
        else:
            creator = creator[0]

        create_dir(user_cp_path+"/upload/"+code)
        cat = db(db.clsb_category)(db.clsb_category.category_type == db.clsb_product_type.id)(db.clsb_product_type.type_name.like("Application")).select()
        category = db(db.clsb_device_shelf.device_shelf_type.like("APP")).select()
        if len(db(db.clsb20_product_cp.product_code == code).select()) > 0:
            newdata = db(db.clsb20_product_cp.product_code == code).select().first()
            db(db.clsb20_product_cp.product_code == code).update(product_title=request.vars.title,
                                                    product_code=code,
                                                    product_publisher=publisher.id,
                                                    product_creator=creator.id,
                                                    device_shelf_code=category[-1]['id'],
                                                    product_category=cat[0].clsb_category.id,
                                                    product_status='developer')
        else:
            newdata = db.clsb20_product_cp.insert(product_title=request.vars.title,
                                                    product_code=code,
                                                    product_publisher=publisher.id,
                                                    product_creator=creator.id,
                                                    device_shelf_code=category[-1]['id'],
                                                    product_category=cat[0].clsb_category.id,
                                                    product_status='developer')
        purchase_id = db(db.clsb20_purchase_type.name.like("Free")).select()[0].id
        purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id
        db.clsb20_product_purchase_item.insert(product_code=newdata.product_code, purchase_item=purchase_item)
        return newdata


@auth.requires_signature()
def tocancel():
    id = request.args[0]
    data = db(db.clsb20_product_cp.id == id)
    dbproduct = data.select()[0]
    try:
        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/review/"+dbproduct.product_code)
    except:
        pass
    data.update(
        product_status='Cancel'
    )
    session.flash = 'Thành công'
    return "OK"
    # return redirect(URL('index', user_signature=True))


# @auth.requires_authorize()
def multi_media():
    if request.url.find('/new/clsb20_product_cp') >= 0:
        return create_product(media=True)
    if request.url.find('/edit/clsb20_product_cp') >= 0:
        return update_product(media=True)
    if request.url.find('/view/clsb20_product_cp') >= 0:
        return view_product(media=True)
    if request.url.find('/delete/clsb20_product_cp') >= 0:
        return remove_product(media=True)
    user_info = usercp.user_get_info(auth.user.id, db)
    query = None
    query_status = ~db.clsb20_product_cp.product_status.like("%delete%")
    if request.vars.product_status:
        if request.vars.product_status != "0":
            query_status = db.clsb20_product_cp.product_status.like(request.vars.product_status)
    if user_info['user_info']['is_admin'] == True:
        query = db(query_status)\
                    ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Application")))\
                    ((db.clsb_category.id == db.clsb20_product_cp.product_category) & (((db.auth_user.created_by == auth.user.id) & (db.auth_user.id == db.clsb20_product_cp.created_by)) | (db.clsb20_product_cp.created_by == auth.user.id)))
    else:
        query = db((query_status) & (db.clsb20_product_cp.created_by == auth.user.id))\
                    ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Application")))\
                    (db.clsb_category.id == db.clsb20_product_cp.product_category)
    if request.vars.keyword:
        keyword = request.vars.keyword
        search = ((db.clsb20_product_cp.product_code == keyword)\
                    | (db.clsb20_product_cp.product_title.like('%' + keyword + '%'))\
                    | (db.clsb20_dic_creator_cp.creator_name.like('%' + keyword + '%'))\
                    | (db.clsb_dic_publisher.publisher_name.like('%' + keyword + '%')))
        query = query(search)

    product_list = query.select(groupby=db.clsb20_product_cp.id, orderby=~db.clsb20_product_cp.created_on)
    return dict(
        product_list=product_list,
        user_cp_path=user_cp_path
    )
