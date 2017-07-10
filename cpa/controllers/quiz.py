# -*- coding: utf-8 -*-
__author__ = 'tanbm'
from time import gmtime, strftime
import zipfile
import re
import os,sys
import shutil
import usercp, scripts, products


@auth.requires_login()
def init_cp_path():
    response.title = "CP Product Manager"
    return "CP"+str(usercp.user_get_id_cp(auth.user.id, db))
user_cp_path = init_cp_path()


def index():
    return dict()


@auth.requires_authorize()
def exercises():
    try:
        if request.url.find('/new/clsb20_product_cp') >= 0:
            return create_product()
        if request.url.find('/edit/clsb20_product_cp') >= 0:
            return update_product()
        if request.url.find('/view/clsb20_product_cp') >= 0:
            return view_product()
        if request.url.find('/delete/clsb20_product_cp') >= 0:
            return remove_product()
        user_info = usercp.user_get_info(auth.user.id, db)
        query_status = ~db.clsb20_product_cp.product_status.like("%delete%")
        if request.vars.product_status:
            if request.vars.product_status != "0":
                query_status = db.clsb20_product_cp.product_status.like(request.vars.product_status)
        if user_info['user_info']['is_admin'] == True:
            query = db(query_status)\
                        ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Exercise")))\
                        ((db.clsb_category.id == db.clsb20_product_cp.product_category) & (((db.auth_user.created_by == auth.user.id) & (db.auth_user.id == db.clsb20_product_cp.created_by)) | (db.clsb20_product_cp.created_by == auth.user.id)))
        else:
            query = db((query_status) & (db.clsb20_product_cp.created_by == auth.user.id))\
                        ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Exercise")))\
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
    except Exception as e:
        print e
        pass


@auth.requires_signature()
def view_product():
    id = request.args[2]
    data = db(db.clsb20_product_cp.id == id).select()
    relation = db(db.clsb20_product_relation_cp.product_cp_id == id).select()
    images = db(db.clsb20_product_image.product_code == data[0].product_code).select()
    metadata = db(db.clsb20_product_metadata_cp.product_code == data[0].product_code).select()
    payment_type = db(~db.clsb20_purchase_type.name.like("Subscriptions")).select()
    subscriptions = db(db.clsb20_purchase_item.purchase_type == db(db.clsb20_purchase_type.name.like("Subscriptions")).select()[0].id).select()

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
        db(db.clsb20_product_purchase_item.product_code.like(data[0].product_code)).update(purchase_item=purchase_item)
        db.clsb20_product_price_history.insert(product_id=id, purchase_item=purchase_item, price=price, changing_time=datetime.now())

        session.flash = "Thành công"
        return "OK"

    payment = db(db.clsb20_product_purchase_item.product_code.like(data[0].product_code)).select()
    purchase_type = db(db.clsb20_purchase_item.id == payment[0].purchase_item).select()

    purchase_dict_type = db(db.clsb20_purchase_type.id == purchase_type[0].purchase_type).select()
    btnchangeprice = purchase_type[0].description

    if (purchase_dict_type[0]['name'].upper() != "SUBSCRIPTIONS") | (data[0].product_status.upper() != "PUBLISHED"):
        btnchangeprice = FORM(
            SELECT(*[OPTION(payment_type[i].description, _value=str(payment_type[i].name), _selected=True if payment_type[i].id == purchase_dict_type[0].id else False) for i in range(len(payment_type))], _id="payment", _style="width:250px; margin-top: 5px", _class="clsb_input_product", _name="payment"),
            # SELECT(*[OPTION(subscriptions[i].description, _value=str(subscriptions[i].id), _selected=True if subscriptions[i].id == purchase_type[0].id else False) for i in range(len(subscriptions))], _style="width:250px; margin-top: 5px; display: none;", _class="clsb_input_product", _name="payment_more",_id="payment_more"),
            # DIV(B("* Chú ý: "), XML("Khi chọn phương thức <b>Thanh toán theo thời gian</b> sẽ không thể đổi sang hình thức thanh toán khác khi đã được duyệt"), _style="width:250px;"),
            DIV(INPUT(_type="submit", _class="btn", _value="Đổi hình thức thu phí")),
            _action="javascript:submit_c('Bạn có muốn đổi hình thức thu phí?','"+URL(a='cpa', c='products', f='index', args=request.args)+"','payment')",
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
                        " Quản lý trắc nghiệm", _class="btn"
                    ),
                    _href=URL()
                ),
                SPAN(" "),
                A(
                    DIV(
                        SPAN(_class="icon pen icon-pencil"),
                        " Cập nhật dữ liệu", _class="btn"
                    ),
                    _href=URL('exercises',args=['edit','clsb20_product_cp',id], user_signature=True),
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
                        TD(LABEL(data[0].product_description,_class="clsb_label_product"))
                    ),
                    TR(
                        TD(LABEL("Metadata: ",_class="clsb_label_product")),
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
                        TD(LABEL("Giá tiền: ",_class="clsb_label_product", _style=" font-weight: bold;")),
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
                        TD(A(SPAN("Tải về: "+data[0].product_code+".ZIP",_class="btn"), _href="/cpa/download/file/"+user_cp_path+"/upload/"+data[0].product_code+"/"+data[0].product_code+".zip"))
                    )
                )
            ),
            TD(
                TABLE(
                    TR(
                        TD(LABEL("Features Images: ",_class="clsb_label_product")),
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
                        ),
                        reject
                    )
                )
            )
        ),
        _class="clsb_table_product"
    )
    return dict(form=form)


@auth.requires_signature()
def create_product():
    form = get_form()
    if form.accepts(request, session):
        try:
            publisher = db(db.clsb_dic_publisher.publisher_name.like("%"+request.vars.publisher+"%")).select()
            if len(publisher) <= 0:
                publisher = db.clsb_dic_publisher.insert(publisher_name = request.vars.publisher)
            else:
                publisher = publisher[0]
            product = db(db.clsb20_product_cp.id==request.vars.book).select()
            if len(product)>0:
                product = product[0]
                code = "Exer"+product.product_code

                creator_list = re.split(r"[,;]", request.vars.creator)
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
                exer = db(db.clsb20_product_cp.product_code.like(code)).select()
                check_valid = False
                check_delete = False
                if len(exer) > 0:
                    exer_d = db(db.clsb20_product_cp.product_code.like(code) & db.clsb20_product_cp.product_status.like("%delete%")).select()
                    if len(exer_d) > 0:
                        check_delete = True
                    else:
                        check_valid = True
                if check_valid:
                    response.flash = 'Đã tồn tại trắc nghiệm'
                else:
                    if request.vars.data != "":
                        if request.vars.data.file:
                            result = save_data(request.vars.data, code+"/"+code+".zip", code)
                            if result != "OK":
                                response.flash = result
                    if request.vars.cover != "":
                        if request.vars.cover.file:
                            save_file(request.vars.cover.file, code+"/cover.clsbi")
                    if request.vars.thumbnail != "":
                        if request.vars.thumbnail.file:
                            save_file(request.vars.thumbnail.file, code+"/thumb.png")
                        else:
                            shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/thumb.png")
                    else:
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

                    cat = db(db.clsb_category)(db.clsb_category.category_type==db.clsb_product_type.id)(db.clsb_product_type.type_name.like("Exercise")).select()

                    if check_delete:
                        db(db.clsb20_product_cp.product_code.like(code)).update(
                            product_title=product.product_title,
                            product_description=request.vars.content,
                            subject_class=product.subject_class,
                            device_shelf_code=product.device_shelf_code,
                            product_creator=creator.id,
                            product_publisher=publisher.id,
                            product_category=cat[0].clsb_category.id,
                            product_price=request.vars.price,
                            product_status="Init",
                        )
                        if request.vars.payment != "":
                            if request.vars.payment.upper() == "SUBSCRIPTIONS":
                                purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
                            else:
                                purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.payment)).select()[0].id
                                purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id

                            db(db.clsb20_product_purchase_item.product_code.like(code)).update(purchase_item=purchase_item)
                    else:
                        newdata = db.clsb20_product_cp.insert(product_title="Trắc nghiệm "+product.product_title,
                                                              product_code=code,
                                                              product_description=request.vars.content,
                                                              subject_class=product.subject_class,
                                                              product_publisher=publisher.id,
                                                              product_creator=creator.id,
                                                              device_shelf_code=product.device_shelf_code,
                                                              product_category=cat[0].clsb_category.id,
                                                              product_price=request.vars.price)
                        if request.vars.payment != "":
                            if request.vars.payment.upper() == "SUBSCRIPTIONS":
                                purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
                            else:
                                purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.payment)).select()[0].id
                                purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id

                            db.clsb20_product_purchase_item.insert(product_code=newdata.product_code, purchase_item=purchase_item)


                    response.flash = 'Tải lên thành công'

            else:
                response.flash = "Không tồn tại sách"

        except Exception as ex:
            response.flash = 'Quá trình tải : '+ex.message+' on line: '+str(sys.exc_traceback.tb_lineno)
    elif form.errors:
        response.flash = 'Thông tin không đúng'
    else:
        response.flash = 'Xin mời điền thông tin'
    return dict(form=form)


def get_form():
    payment = db(~db.clsb20_purchase_type.name.like("Subscriptions")).select()
    subscriptions = db(db.clsb20_purchase_item.purchase_type == db(db.clsb20_purchase_type.name.like("Subscriptions")).select()[0].id).select()
    form = FORM(
        DIV(
            TABLE(
                TR(
                    TD(
                        A(
                            DIV(
                                SPAN(_class="icon leftarrow icon-arrow-left"),
                                " Quản lý trắc nghiệm", _class="btn"
                            ),
                            _href=URL(user_signature=True)
                        ),
                    ),
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Sách: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_style="display: none;", _name="book", _id="clsb_book_list_value"),
                                    INPUT(_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_book_list", _linkSearch=URL(a='cpa', c='products', f='search'), requires=IS_NOT_EMPTY()),
                                    SPAN(XML("Chọn sách"),_class="btn",_onclick="javascript:searchproductquiz()"))
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
                                TD(LABEL("Tác giả: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_creator_list", _name="creator", _linkSearch=URL(a='cps',c='creators',f='search'), requires=IS_NOT_EMPTY()),
                                    SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchcreator()"),
                                    DIV("Các tác giả phân cách nhau bằng dấu ';'")),
                            ),
                            TR(
                                TD(LABEL("Nhà cung cấp: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_publisher_list", _name="publisher", _linkSearch=URL(a='cps',c='publishers',f='search'), requires=IS_NOT_EMPTY()),
                                    SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchpublisher()")),
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
                                            TD(
                                                SPAN(XML("Ảnh bìa cỡ nhỏ<br/>(100x141)px")),
                                                XML("<br/>"),
                                                INPUT(_name="thumbnail",_class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;"),
                                                DIV(XML("+<br/>Add<br/>Thumbnail"), _class="clsb_image thumbnail_cp", _onclick="openimage('thumbnail',event)"),
                                            ),
                                            TD(
                                                SPAN("Ảnh bìa cỡ lớn(200x282)px"),
                                                XML("<br/>"),
                                                INPUT(_name="cover", _class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;", requires=IS_NOT_EMPTY()),
                                                DIV(XML("+<br/>Add Cover"), _class="clsb_image cover", _onclick="openimage('cover',event)"),
                                            ),
                                        )
                                    ),
                                    TABLE(
                                        TR(
                                            TD(
                                                SPAN("Ảnh minh họa chi tiết (Tối đa 5 ảnh - kích cỡ < 1MB)"),
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
                                TD(LABEL("Dữ liệu trắc nghiệm (ZIP file): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_name="data",_class="clsb_input_product", _accept=".zip", _type="file", _style="display: none;"),
                                    DIV(XML("<b>+</b> Chọn tệp tin ZIP"), _class="btn", _onclick="opendata('data', event)"),
                                    XML("<br/>"), SPAN(" Được đóng gói từ ứng dụng CBQUIZEditor")
                                )
                            ),
                            TR(
                                TD(),
                                TD(XML("<b>Chú ý:</b> Mỗi phương thức thu tiền sẽ có hình thức thu phí khi tải về là khác nhau. <br/> <i>Hình thức miễn phí</i>: mặc định giá cho sản phẩm sẽ là 0 VNĐ, khách hàng sẽ không phải trả tiền cho sản phẩm khi chọn hình thức này.<br/> <i>Hình thức thanh toán cho lần tải đầu tiên</i>: Khác hàng sẽ chỉ phải trả phí cho lần đầu tiên tải sản phẩm, các lần sau sẽ không bị thu phí. <br/> <i>Hình thức thanh toán cho mỗi lượt tải</i>: Khách hàng sẽ phải trả phí cho mỗi lần tải sản phẩm về"), _style="color: #999;")
                            ),
                            TR(
                                TD(LABEL("Phương thức thu tiền: ",_class="clsb_label_product", _style="font-weight: bold;"), _class="rows-left"),
                                TD(
                                    SELECT(*[OPTION(payment[i].description, _value=str(payment[i].name)) for i in range(len(payment))], _id="payment",_style="margin-top: 5px;", _class="clsb_input_product", _name="payment"),
                                    # SELECT(*[OPTION(subscriptions[i].description, _value=str(subscriptions[i].id)) for i in range(len(subscriptions))],_style="margin-top: 5px; display: none;", _class="clsb_input_product", _name="payment_more",_id="payment_more"),
                                    DIV(INPUT(_name="price", _placeholder="Giá tiền", _class="clsb_input_product", _value=0, _style="color: rgb(255, 112, 0);  font-weight: bold;"), "VNĐ", _id="price"),
                                    # DIV(B("* Chú ý: "),  XML("Khi chọn phương thức <b>Thanh toán theo thời gian</b> sẽ không thể đổi sang hình thức thanh toán khác khi đã được duyệt"), _style="white-space: normal; text-align: justify;")
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
                        if name.find(".qz"):
                            zip.writestr((name.replace(old_filename[:-4], code)).replace(code+".qz",code.replace("Exer","")+".qz"), buffer_data)
                        else:
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


@auth.requires_signature()
def topending():
    id = request.args[0]
    data = db(db.clsb20_product_cp.id==id)
    if data.select()[0].product_status == "Pending":
        session.flash = "Trắc nghiệm đang được kiểm duyệt"
    else:
        result = products.validate_zip(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data.select()[0].product_code+"/"+data.select()[0].product_code+".zip", "Exercise")
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
    return redirect(URL('exercises', user_signature=True))


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
        session.flash = "Trắc nghiệm đang được kiểm duyệt"
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
    # return redirect(URL('exercises', user_signature=True))


@auth.requires_signature()
def metadata():
    links = [{
                'header': 'Metadata Name',
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
        session['product_code']=request.args[0]
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
                  A(SPAN("Back",_class="btn"),_href=URL('metadata', args=[code], user_signature=True)),XML("<br/>")
              ),
              TD()
            ),
            TR(
                TD(LABEL("Product Code:")),
                TD(INPUT(_value=code, _disabled=True))
            ),
            TR(
                TD(LABEL("Metadata:")),
                TD(SELECT(*[OPTION(metadata[i].metadata_label, _value=metadata[i].id) for i in range(len(metadata))], _name="metadata_id"))
            ),
            TR(
                TD(LABEL("Metadata Value:")),
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
        result =  copy_metadata(code)
        if result=="OK":
            response.flash = "Success!!!"
        else:
            response.flash = result
    if form.errors:
        response.flash = "Error!!!"
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
def update_product():
    id = request.args[2]
    data = db(db.clsb20_product_cp.id==id)
    #if (data.select()[0].product_status.upper() != "INIT") & (data.select()[0].product_status.upper() != "CANCEL") & (data.select()[0].product_status.upper() != "REJECT"):
    if data.select()[0].product_status.upper() == "SUBMIT" or data.select()[0].product_status.upper() == "PENDING":
        session.flash = "Cần hủy chờ duyệt trước"
        return redirect(URL('exercises', user_signature=True))
    #if data.select()[0].product_status == "Published":
    #    session.flash = "Sách ?ã ???c public, b?n c?n ng?ng public tr??c khi s?a ??i"
    #    return redirect(URL('index', user_signature=True))
    data = db(db.clsb20_product_cp.id==id).select()
    creator = db(db.clsb20_dic_creator_cp.id==data[0].product_creator).select()
    publisher = db(db.clsb_dic_publisher.id==data[0].product_publisher).select()

    creator_list =  db(db.clsb20_product_metadata_cp.product_code == data[0].product_code)\
            (db.clsb_dic_metadata.id == db.clsb20_product_metadata_cp.metadata_id)\
            (db.clsb_dic_metadata.metadata_name.like("co_author")).select()
    creator_name = creator[0]['creator_name']
    for creat in creator_list:
        creator_name += ";"+creat['clsb20_product_metadata_cp']['metadata_value']

    images = db(db.clsb20_product_image.product_code == data[0].product_code).select()
    subject_class = db(db.clsb_subject_class.id==data[0].subject_class).select()
    if len(subject_class)>0:
        subject_class = subject_class[0]
    else:
        subject_class = dict()
        subject_class['subject_id'] = '0'
        subject_class['class_id'] = '0'

    form = FORM(
        DIV(
            TABLE(
                TR(
                    TD(
                        A(
                            DIV(
                                SPAN(_class="icon leftarrow icon-arrow-left"),
                                " Quản lý trắc nghiệm", _class="btn"
                            ),
                            _href=URL(user_signature=True)
                        ),
                        SPAN(" "),
                        A(
                            DIV(
                                SPAN(_class="icon pen icon-zoom-in"),
                                " Xem chi tiết", _class="btn"
                            ),
                            _href=URL('exercises',args=['view','clsb20_product_cp',id], user_signature=True),
                        )
                    )
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Sách: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    #INPUT(_style="display: none;", _name="book", _id="clsb_book_list_value", _value=db(db.clsb20_product_cp.product_code.like(data[0].product_code[4:])).select()[0].id),
                                    INPUT(_style="margin-top: 10px;",_class="clsb_input_product", _value=data[0].product_title,_id="clsb_book_list", _linkSearch=URL(a='cpa',c='products',f='search',args=['0','10','Book']), _disabled=True, requires=IS_NOT_EMPTY()),
                                    #SPAN(XML("Chọn sách"),_class="btn",_onclick="javascript:searchproductquiz()")
                                )
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
                                TD(LABEL("Tác giả: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_value = creator_name,_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_creator_list", _name="creator", _linkSearch=URL(a='cps',c='creators',f='search'), requires=IS_NOT_EMPTY()),
                                   SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchcreator()"),
                                   DIV("Các tác giả phân cách nhau bằng dấu ';'")),
                            ),
                            TR(
                                TD(LABEL("Nhà cung cấp: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_value = publisher[0].publisher_name ,_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_publisher_list", _name="publisher", _linkSearch=URL(a='cps',c='publishers',f='search'), requires=IS_NOT_EMPTY()),
                                   SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchpublisher()")),
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
                                    SPAN(XML("Ảnh bìa cỡ nhỏ<br/>(100x141)px")),
                                    XML("<br/>"),
                                    INPUT(_name="thumbnail", _class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;"),
                                    DIV(_style="background-image: url("+URL(a='cpa',c='download', f='cover',args=[user_cp_path, 'upload', data[0].product_code, 'thumb.png'])+")", _class="clsb_image thumbnail_cp", _onclick="openimage('thumbnail',event)"),
                                ),
                                TD(
                                    SPAN("Ảnh bìa cỡ lớn(200x281)px"),
                                    XML("<br/>"),
                                    INPUT(_name="cover",_class="clsb_input_product", _accept="image/*", _type="file", _style="display: none;"),
                                    DIV(_style="background-image: url("+URL(a='cpa',c='download', f='cover',args=[user_cp_path, 'upload', data[0].product_code, 'cover.clsbi'])+")", _class="clsb_image cover", _onclick="openimage('cover',event)"),
                                ),
                            ),
                            _style="width: 100%;"
                        ),
                        TABLE(
                            TR(
                                TD(
                                    SPAN("Ảnh minh họa chi tiết (Tối đa 5 ảnh - kích cỡ < 1MB)"),
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
                                            *[XML("<img src="+URL(a='cpa',c='download', f='image',args=[user_cp_path, 'upload', images[i].image])+"  class='clsb_image fimages' style='padding-top: 0px;'/>") for i in range(len(images))],
                                            _id="imglist",
                                            _class="border_imglist"
                                        ),
                                        _style="overflow: auto;"
                                    )

                                )
                            )
                        ),
                        _class="clsb_upload_border"
                    ),
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Dữ liệu trắc nghiệm (ZIP file): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_name="data",_class="clsb_input_product", _accept=".zip", _type="file", _style="display: none;"),
                                    DIV(XML("<b>+</b> Chọn tệp tin ZIP Thay thế"), _class="btn", _onclick="opendata('data', event)"),
                                    XML("<br/>"), SPAN(" Được đóng gói từ ứng dụng CBQUIZEditor"), XML("<br/>"),
                                    A(SPAN("Tải về: "+data[0].product_code+".ZIP",_class="btn"), _href="/cpa/download/file/"+user_cp_path+"/upload/"+data[0].product_code+"/"+data[0].product_code+".zip")
                                )
                            ),
                            # TR(
                            #     TD(LABEL("Giá tiền: ",_class="clsb_label_product"), _class="rows-left"),
                            #     TD(INPUT(_name="price", _class="clsb_input_product", _value=data[0].product_price), "VNĐ")
                            # ),
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
    if form.accepts(request, session):
        publisher = db(db.clsb_dic_publisher.publisher_name.like("%"+request.vars.publisher+"%")).select()
        creator_list = re.split(r"[,;]", request.vars.creator)
        creator = dict()
        add_creator = ""
        metadata_id = db(db.clsb_dic_metadata.metadata_name.like("co_author")).select()[0]['id']
        db((db.clsb20_product_metadata_cp.product_code == data[0].product_code) & (db.clsb20_product_metadata_cp.metadata_id == metadata_id)).delete()
        for creat in creator_list:
            if creat != "":
                if add_creator == "" :
                    creator = db(db.clsb20_dic_creator_cp.creator_name == creat).select()
                    add_creator = creat
                else:
                    db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=data[0].product_code, metadata_value=creat)

        if len(creator) <= 0:
            creator = db.clsb20_dic_creator_cp.insert(creator_name=add_creator)
        else:
            creator = creator[0]
        if len(publisher) <= 0:
            publisher = db.clsb_dic_publisher.insert(publisher_name = request.vars.publisher)
        else:
            publisher = publisher[0]

        product = db(db.clsb20_product_cp.id==db(db.clsb20_product_cp.product_code.like(data[0].product_code[4:])).select()[0].id).select()
        if len(product)>0:
            product = product[0]
            db(db.clsb20_product_cp.id == id).update(
                product_title=product.product_title,
                product_description=request.vars.content,
                subject_class=product.subject_class,
                device_shelf_code=product.device_shelf_code,
                product_creator=creator.id,
                product_publisher=publisher.id,
                product_status="Init",
                # product_price = request.vars.price
            )
            if request.vars.data != "":
                if request.vars.data.file:
                     save_data(request.vars.data, data[0].product_code+"/"+data[0].product_code+".zip", data[0].product_code)
            if request.vars.cover != "":
                if request.vars.cover.file:
                    save_file(request.vars.cover.file, data[0].product_code+"/cover.clsbi")
            if request.vars.thumbnail != "":
                if request.vars.thumbnail.file:
                            save_file(request.vars.thumbnail.file, data[0].product_code+"/thumb.png")
                else:
                    shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/thumb.png")
            else:
                shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/thumb.png")
            if request.vars.removefimages != "":
                imagedelete = db(db.clsb20_product_image.product_code==data[0].product_code).select()
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
        else:
            session.flash = 'Có lỗi xảy ra'
        return redirect(URL('exercises', args=['view', 'clsb20_product_cp', id], user_signature=True))
    elif form.errors:
        response.flash = 'Thông tin không đúng'
    else:
        response.flash = 'Xin mời nhập thông tin'

    return dict(form=form)


@auth.requires_signature()
def remove_product():
    id = request.args[2]
    #data = db(db.clsb20_product_cp.id==id)
    #if data.select()[0].product_status == "Pending":
    #    session.flash = "Sách ?ang ???c ki?m duy?t"
    #    return redirect(URL('index', user_signature=True))
    data = db(db.clsb20_product_cp.id == id).select()
    imagedelete = db(db.clsb20_product_image.product_code == data[0].product_code).select()
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
        session.flash = 'Xóa thành công'
    except Exception as e:
        response.flash = "Không tồn tại thư mục"
    redirect(URL("exercises", user_signature=True))

def create_dir(directory):
    if URL().find('create_dir') >= 0:
        raise HTTP(404)
    if not os.path.exists(settings.home_dir+settings.cp_dir+directory):
        os.makedirs(settings.home_dir+settings.cp_dir+directory)


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
    # return redirect(URL('exercises', user_signature=True))