# -*- coding: utf-8 -*-
import os
import zipfile
import sys
import shutil
from time import gmtime, strftime

""" Products
    Quản lý sản phẩm, upload, chỉnh sửa thông tin, đệ trình review, xóa...
"""
import re
import usercp
import scripts
import products

__author__ = 'manhtd'
response.title = "CP Product Manager"


@auth.requires_login()
def init_cp_path():
    response.title = "CP Product Manager"
    return "CP"+str(usercp.user_get_id_cp(auth.user.id, db))
user_cp_path = init_cp_path()


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
        btnchangeprice = SELECT(*[OPTION(payment_type[i].description, _value=str(payment_type[i].name), _selected=True if payment_type[i].id == purchase_dict_type[0].id else False) for i in range(len(payment_type))], _id="payment", _style="width:250px; margin-top: 5px", _class="clsb_input_product", _name="payment")\
                #,
            # SELECT(*[OPTION(subscriptions[i].description, _value=str(subscriptions[i].id), _selected=True if subscriptions[i].id == purchase_type[0].id else False) for i in range(len(subscriptions))], _style="width:250px; margin-top: 5px; display: none;", _class="clsb_input_product", _name="payment_more",_id="payment_more"),
            # DIV(B("* Chú ý: "), XML("Khi ch?n ph??ng th?c <b>Thanh toán theo th?i gian</b> s? không th? ??i sang hình th?c thanh toán khác khi ?ã ???c duy?t"), _style="width:250px;"),
            #DIV(INPUT(_type="submit", _class="btn", _value="Đổi hình thức thu phí")),
            #_action="javascript:submit_c('Bạn có muốn đổi hình thức thu phí?','"+URL(a='cpa', c='products', f='index', args=request.args)+"','payment')"
            # _style="white-space: normal; text-align: justify;"
        #)

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
    if request.vars.payment != "":
        pass

    form = FORM(TABLE(
        TR(
            TD(
                A(
                    DIV(
                        SPAN(_class="icon leftarrow icon-arrow-left"),
                        " Quản lý sách", _class="btn"
                    ),
                    _href=URL()
                ),
                SPAN(" "),
                A(
                    DIV(
                        SPAN(_class="icon pen icon-pencil"),
                        " Cập nhật sách", _class="btn"
                    ),
                    _href=URL('index',args=['edit','clsb20_product_cp',id], user_signature=True),
                )
            ),
        ),
        TR(
            TD(
                TABLE(
                    TR(
                        TD(LABEL("Mã sách: ",_class="clsb_label_product")),
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
                        TD(LABEL("Nhà xuất bản: ",_class="clsb_label_product")),
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
                        TD(LABEL("Giá tiền: ", _class="clsb_label_product", _style=" font-weight: bold;")),
                        TD(
                            A(BUTTON("Lịch sử đổi giá", _class="btn"), _href=URL(a='cpa', c='price', f='history', vars=dict(product_id=data[0].id), user_signature=True)),
                            #FORM(INPUT(_value=str(data[0].product_price), _id="price_change", _style="text-align: right;min-width: 10px; width: 150px; margin-top: 10px; color: rgb(255, 112, 0);  font-weight: bold;", _class="clsb_input_product")+"₫ ", INPUT(_type="submit", _value="Đổi giá", _style="width: 80px;", _class="btn"), _action="javascript:submit_c('Bạn có muốn thay đổi giá tiền?', '"+URL('change_price', args=[data[0].id])+"','price_change')", _method="GET", _style="color: rgb(255, 112, 0);"),
                            INPUT(_value=str(data[0].product_price), _id="price_change", _style="text-align: right;min-width: 10px; width: 150px; margin-top: 10px; color: rgb(255, 112, 0);  font-weight: bold;", _class="clsb_input_product")+"₫ "

                        )
                    ),
                    TR(
                        TD(LABEL("Cách thức thu phí: ", _class="clsb_label_product")),
                        TD(
                            DIV(btnchangeprice),
                        )
                    ),
                    TR(
                        TD(),
                        TD(INPUT(_type="submit", _value="Lưu thay đổi", _style="width: 150;", _class="btn"), _action="javascript:submit_c('Bạn có muốn lưu thay đổi không?', '"+URL('change_price', args=[data[0].id])+"','price_change')", _method="GET", _style="color: rgb(255, 112, 0);"),
                        #TD(A(SPAN("Tải về: "+data[0].product_code+".ZIP",_class="btn"), _href=URL(a="cpa", c="download", f="file", args=[user_cp_path, "upload", data[0].product_code, data[0].product_code+".zip"])))
                    ),
                    TR(
                        TD(LABEL("ZIP file: ",_class="clsb_label_product")),
                        TD(A(SPAN("Tải về: "+data[0].product_code+".ZIP",_class="btn"), _href=URL(a="cpa", c="download", f="file", args=[user_cp_path, "upload", data[0].product_code, data[0].product_code+".zip"])))
                    )
                ),
                _class="clsb_upload_border"
            ),
            TD(
                TABLE(
                    TR(
                        TD(LABEL("Features Images: ",_class="clsb_label_product")),
                        TD(
                            DIV(
                                *[IMG(_src=URL(a="cpa", c="download", f="image", args=[user_cp_path, "upload", images[i].image])) for i in range(len(images))],
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
                    ),
                    reject
                ),
                _class="clsb_upload_border"
            )
        ),
        _class="clsb_table_product"
    ), _action="javascript:submit_c_p('Bạn có muốn lưu các thay đổi?', '" + URL('change_price', args=[data[0].id])+"','price_change', 'payment')", _method="GET"
    )
    return dict(form=form)


@auth.requires_signature()
def update_product():
    id = request.args[2]
    data = db(db.clsb20_product_cp.id == id)
    update_file = data.select()[0].update_file
    # if (data.select()[0].product_status.upper() != "INIT") & (data.select()[0].product_status.upper() != "CANCEL") & (data.select()[0].product_status.upper() != "REJECT"):
    if data.select()[0].product_status.upper() == "SUBMIT" or data.select()[0].product_status.upper() == "PENDING":
        session.flash = "Cần hủy chờ duyệt trước"
        return redirect(URL('index', user_signature=True))

    data = db(db.clsb20_product_cp.id == id).select()
    session.cat_id = data[0].product_category
    creator = db(db.clsb20_dic_creator_cp.id == data[0].product_creator).select()
    publisher = db(db.clsb_dic_publisher.id == data[0].product_publisher).select()

    images = db(db.clsb20_product_image.product_code == data[0].product_code).select()
    category_parent_id = db(db.clsb_category.id == data[0].product_category).select().first()['category_parent']
    category_parent = db(db.clsb_category.category_parent == None)\
                (db.clsb_category.category_type == db.clsb_product_type.id)\
                (db.clsb_product_type.type_name.like("Book")).select()
    category = db(db.clsb_category.category_parent == category_parent_id).select()


    subject_class = db(db.clsb_subject_class.id == data[0].subject_class).select()
    num_page = db(db.clsb20_product_metadata_cp.product_code == data[0].product_code)\
            (db.clsb_dic_metadata.id == db.clsb20_product_metadata_cp.metadata_id)\
            (db.clsb_dic_metadata.metadata_name.like("page_number")).select()
    if len(num_page) > 0:
        num_page = num_page.first()['clsb20_product_metadata_cp']['metadata_value']
    else:
        num_page = 0

    select_format = db(db.clsb20_product_metadata_cp.product_code == data[0].product_code)\
            (db.clsb_dic_metadata.id == db.clsb20_product_metadata_cp.metadata_id)\
            (db.clsb_dic_metadata.metadata_name.like("format")).select()
    if len(select_format) > 0:
        size_cover = select_format.first()['clsb20_product_metadata_cp']['metadata_value']
    else:
        size_cover = ""

    select_pub_year = db(db.clsb20_product_metadata_cp.product_code == data[0].product_code)\
            (db.clsb_dic_metadata.id == db.clsb20_product_metadata_cp.metadata_id)\
            (db.clsb_dic_metadata.metadata_name.like("pub_year")).select()
    if len(select_pub_year) > 0:
        pub_year = select_pub_year.first()['clsb20_product_metadata_cp']['metadata_value']
    else:
        pub_year = ""

    creator_list = db(db.clsb20_product_metadata_cp.product_code == data[0].product_code)\
            (db.clsb_dic_metadata.id == db.clsb20_product_metadata_cp.metadata_id)\
            (db.clsb_dic_metadata.metadata_name.like("co_author")).select()
    creator_name = creator[0]['creator_name']
    for creat in creator_list:
        creator_name += ";"+creat['clsb20_product_metadata_cp']['metadata_value']


    if len(subject_class)>0:
        subject_class = subject_class[0]
    else:
        subject_class = dict()
        subject_class['subject_id'] = '0'
        subject_class['class_id'] = '0'

    classes = db(db.clsb_class.id == db.clsb_subject_class.class_id)\
                (db.clsb_subject_class.subject_id == subject_class['subject_id']).select()
    subjects = db(db.clsb_subject).select()

    form = FORM(
        DIV(
            TABLE(
                TR(
                    TD(
                        A(
                            DIV(
                                SPAN(_class="icon leftarrow icon-arrow-left"),
                                " Quản lý sách", _class="btn"
                            ),
                            _href=URL(user_signature=True)
                        ),
                        SPAN(" "),
                        A(
                            DIV(
                                SPAN(_class="icon pen icon-zoom-in"),
                                " Chi tiết", _class="btn"
                            ),
                            _href=URL('index',args=['view','clsb20_product_cp',id], user_signature=True),
                        ),
                    )
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Tiêu đề sách: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_name="title",_class="clsb_input_product",_style="width: 100%;", _value=data[0].product_title, requires=IS_NOT_EMPTY()))
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
                            # TR(
                            #     TD(LABEL("Thể loại: ",_class="clsb_label_product"), _class="rows-left"),
                            #     TD(
                            #         SELECT(*[OPTION(category_parent[i]['clsb_category']['category_name'], _value=str(category_parent[i]['clsb_category']['id']), _selected=True if category_parent[i]['clsb_category']['id'] == category_parent_id else False) for i in range(len(category_parent))], _class="clsb_input_product", _id="category_parent"),
                            #     ),
                            # ),
                            TR(
                                TD(LABEL("Danh mục: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    SELECT(*[OPTION(category[i].category_name, _value=str(category[i].id), _selected=True if category[i].id==data[0].product_category else False) for i in range(len(category))], _class="clsb_input_product", _name="category",  _id="category"),
                                ),
                            ),
                            TR(
                                TD(LABEL("Môn học: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    SELECT(
                                        *[OPTION(subjects[i].subject_name, _value=subjects[i].id, _selected=True if subjects[i].id == subject_class['subject_id'] else False) for i in range(len(subjects))],
                                        _class="clsb_input_product", _name="subjects", _id="subject", requires=IS_NOT_EMPTY()
                                    ),
                                    # TABLE(
                                    #     TR(
                                    #         TD(
                                    #             SPAN("Môn học: ", _style="vertical-align: super;"),
                                    #             SELECT(
                                    #                 *[OPTION(subjects[i].subject_name, _value=subjects[i].id, _selected=True if subjects[i].id == subject_class['subject_id'] else False) for i in range(len(subjects))],
                                    #                 _class="clsb_input_product", _style="min-width: 120px; width: 200px;", _name="subjects", _id="subject", requires=IS_NOT_EMPTY()
                                    #             ), _style="padding: 0px;"
                                    #         ),
                                    #         TD(
                                    #             SPAN("Lớp: ", _style="vertical-align: super;"),
                                    #             SELECT(
                                    #                 *[OPTION(classes[i]['clsb_class']['class_name'], _value=classes[i]['clsb_class']['id'], _selected=True if classes[i]['clsb_class']['id'] == subject_class['class_id'] else False) for i in range(len(classes))],
                                    #                 _class="clsb_input_product", _style="min-width: 120px; width: 150px;", _name="classes", _id="classes", requires=IS_NOT_EMPTY()
                                    #             ), _style="padding: 0px;"
                                    #         )
                                    #     ),
                                    #     _style="width: 100%;"
                                    # )
                                )
                            ),
                            TR(
                                TD(LABEL("Tác giả: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_value = creator_name, _class="clsb_input_product",_id="clsb_creator_list", _name="creator", _linkSearch=URL(a='cps',c='creators',f='search'), requires=IS_NOT_EMPTY()),
                                   SPAN(XML("Tìm kiếm"), _class="btn", _onclick="javascript:searchcreator()",_style="margin-top: -10px;"),
                                   DIV("Các tác giả phân cách nhau bằng dấu ';'")),
                            ),
                            TR(
                                TD(LABEL("Nhà xuất bản: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_value = publisher[0].publisher_name, _class="clsb_input_product",_id="clsb_publisher_list", _name="publisher", _linkSearch=URL(a='cps',c='publishers',f='search'), requires=IS_NOT_EMPTY()),
                                   SPAN(XML("Tìm kiếm"), _class="btn", _onclick="javascript:searchpublisher()", _style="margin-top: -10px;")),
                            ),
                            #TR(
                            #    TD(LABEL("Số trang: ", _class="clsb_label_product"), _class="rows-left"),
                            #    TD(INPUT(_name="num_page", _value=num_page, _class="clsb_input_product", _placeholder="Số trang trên Ebook", requires=IS_NOT_EMPTY()))
                            #),
                            #TR(
                            #    TD(LABEL("Khổ cỡ: ", _class="clsb_label_product"), _class="rows-left"),
                            #    TD(INPUT(_name="size_cover", _value=size_cover, _class="clsb_input_product", _placeholder="Kích thước trang"))
                            #),
                            #TR(
                            #    TD(LABEL("Năm xuất bản: ", _class="clsb_label_product"), _class="rows-left"),
                            #    TD(INPUT(_name="pub_year", _value=pub_year, _class="clsb_input_product", _placeholder="Năm xuất bản"))
                            #),
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
                                    SPAN("Ảnh minh họa khác (Tối đa 5 ảnh - kích cỡ < 1MB)"),
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
                                            *[XML("<img src="+URL(a='cpa',c='download', f='image',args=[user_cp_path, 'upload', images[i].image])+" class='clsb_image fimages'  style='padding-top: 0px;'/>") for i in range(len(images))],
                                            _id="imglist",
                                            _class="border_imglist"
                                        ),
                                        _style="overflow: auto;"
                                    )

                                )
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
                                TD(LABEL("Dữ liệu sách đang dùng: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    A(SPAN("Tải về: "+data[0].product_code+".ZIP",_class="btn"), _href=URL(a='cpa',c='download', f='file', args=[user_cp_path,"upload",data[0].product_code,data[0].product_code+".zip"]))
                                )
                            ),
                            TR(
                                TD(LABEL("Dữ liệu sách (ZIP file): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_name="data", _id="data", _class="clsb_input_product", _accept=".zip", _type="file", _style="display: none;"),
                                    DIV(XML("<b>+</b> Chọn tệp tin ZIP Thay thế"), _id="btn_data", _class="btn", _onclick="opendata('data', event)"),
                                    XML("<br/>"), SPAN(" Được đóng gói từ ứng dụng CBEditor")
                                )
                            ),
                            TR(
                                TD(LABEL("Dữ liệu sách (PDF file): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_name="data_pdf", _id="data_pdf", _class="clsb_input_product", _accept=".pdf", _type="file", _style="display: none;"),
                                    DIV(XML("<b>+</b> Chọn tệp tin PDF Thay thế"), _id="btn_data_pdf", _class="btn", _onclick="opendata('data_pdf', event)"),
                                )
                            ),
                            TR(
                                TD(),
                                TD(
                                    DIV(
                                        SPAN("Ảnh bìa (200x282, 400x564,...)px"),
                                        XML("<br/>"),
                                        INPUT(_name="cover", _class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;"),
                                        DIV(_style="background-image: url("+URL(a='cpa',c='download', f='cover',args=[user_cp_path, 'upload', data[0].product_code, 'cover.clsbi'])+")", _class="clsb_image cover", _onclick="openimage('cover',event)"),
                                        _style="margin-left: 20px; display: inline-block; vertical-align: top;"
                                    ),
                                ),
                                _id="cover_id",
                                _style="display: none;"
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
    try:
        if form.accepts(request, session):
            try:
                class_id = db(db.clsb_class.class_code.like("None")).select()
                subject_class = None
                cat_id = request.vars.category
                session.cat_id = cat_id
                if len(class_id) > 0:
                    class_id = class_id.first().id
                else:
                    class_id = db.clsb_class.insert(
                        class_name="Khác",
                        class_code="None",
                        class_order="9999",
                    )
                    class_id = class_id.id
                if request.vars.category == "0":
                    cat_id = db(db.clsb_category.category_code.like("None")).select()
                    if len(cat_id) <= 0:
                        cat_id = db.clsb_category.insert(
                            category_name="Danh mục khác",
                            category_code="None",
                            category_order="9999"
                        )
                        cat_id = db.clsb_category.insert(
                            category_name="Khác",
                            category_code="None",
                            category_order="9999",
                            category_parent=cat_id.id
                        )
                        cat_id = cat_id.id
                        device_shelf_check = db(db.clsb20_category_shelf_mapping.category_id == cat_id).select()
                        if len(device_shelf_check) <= 0:
                            db.clsb20_category_shelf_mapping.insert(
                                category_id=cat_id,
                                device_shelf_id=db(db.clsb_device_shelf.device_shelf_code.like("STK")).select().first()['id']
                            )
                    else:
                        cat_id = cat_id.first().id

                    subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == class_id)).select()
                    if len(subject_class) > 0:
                        subject_class = subject_class.first()
                    else:
                        subject_class = db.clsb_subject_class.insert(
                            subject_id=request.vars.subjects,
                            class_id=class_id
                        )
                else:
                    map = db(db.clsb20_category_class_mapping.category_id == request.vars.category).select()
                    if len(map) > 0:
                        class_id = map.first().class_id
                    subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == class_id)).select()[0]
            except Exception as e:
                response.flash = "Có lỗi xảy ra: lựa chọn danh mục sách không tương ứng với môn học: "+str(e)+" - on line "+str(sys.exc_traceback.tb_lineno)
                return dict(form=form)
            result_str = ""
            if request.vars.data != "":
                if request.vars.data.file:
                    try:
                        update_file = 1
                        result_str = save_data(request.vars.data, data[0].product_code+"/"+data[0].product_code+".zip", data[0].product_code)
                        zip_file = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/"+data[0].product_code+".zip", "r")
                        for name in zip_file.namelist():
                            if bool(re.search('cover.[Pp][Nn][Gg]$', name)) or bool(re.search('cover.[Jj][Pp][Gg]$', name)):
                                f = zip_file.open(name)
                                print "Name "+ name
                                save_file(f, data[0].product_code+"/cover.clsbi")
                                f.close()
                                break
                        zip_file.close()

                    except Exception as e:
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code)
                        try:
                            products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"_Backup", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code)
                        except:
                            create_dir(user_cp_path+"/upload/"+data[0].product_code)
                        response.flash = "File zip không đúng quy định"
                        return dict(form=form)
            if request.vars.data_pdf != "":
                update_file = 1
                if request.vars.cover != "":
                    save_file(request.vars.cover.file, data[0].product_code+"/cover.clsbi")
                update_product_pdf(request, data[0].product_code)
            try:
                resize_thumb(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/")
                #shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"/thumb.png")
            except Exception as e:
                response.flash = "Dữ liệu tải lên thiếu ảnh bìa"
                shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code)
                try:
                    products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"_Backup", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code)
                except:
                    create_dir(user_cp_path+"/upload/"+data[0].product_code)
                return dict(form=form)
            publisher = db(db.clsb_dic_publisher.publisher_name.like("%"+request.vars.publisher+"%")).select()
            creator_list = re.split(r"[,;]", request.vars.creator)
            creator = dict()
            add_creator = ""
            metadata_id = db(db.clsb_dic_metadata.metadata_name.like("co_author")).select()[0]['id']
            db((db.clsb20_product_metadata_cp.product_code == data[0].product_code) & (db.clsb20_product_metadata_cp.metadata_id == metadata_id)).delete()
            for creat in creator_list:
                if creat != "":
                    if add_creator == "":
                        creator = db(db.clsb20_dic_creator_cp.creator_name == creat).select()
                        add_creator = creat
                    else:
                        db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=data[0].product_code,metadata_value=creat)
            copy_metadata(data[0].product_code)
            if len(creator) <= 0:
                creator = db.clsb20_dic_creator_cp.insert(creator_name=add_creator)
            else:
                creator = creator[0]

            if len(publisher) <= 0:
                publisher = db.clsb_dic_publisher.insert(publisher_name=request.vars.publisher)
            else:
                publisher = publisher[0]
            try:
                device_shelf = db(db.clsb20_category_shelf_mapping.category_id == cat_id).select()[0]['device_shelf_id']
            except Exception as err:
                device_shelf = 27
            db(db.clsb20_product_cp.id == id).update(
                product_title=request.vars.title,
                product_description=request.vars.content,
                product_category=cat_id,
                subject_class=subject_class.id,
                device_shelf_code=device_shelf,
                product_creator=creator.id,
                product_publisher=publisher.id,
                product_status="Init",
                update_file=update_file
                # product_price = request.vars.price
            )


            # if request.vars.thumbnail != "":
            #     if request.vars.thumbnail.file:
            #             save_file(request.vars.thumbnail.file, data[0].product_code+"/thumb.png")
            if request.vars.size_cover is not None and request.vars.size_cover != "":
                metadata = db(db.clsb_dic_metadata.metadata_name.like("format")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="format", metadata_label="Kích cỡ")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("format")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=data[0].product_code,metadata_value=request.vars.size_cover)

            if request.vars.num_page is not None and request.vars.num_page != "":
                metadata = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="page_number", metadata_label="Số trang")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=data[0].product_code,metadata_value=request.vars.num_page)

            if request.vars.pub_year is not None and  request.vars.pub_year != "":
                metadata = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="pub_year", metadata_label="Năm xuất bản")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=data[0].product_code,metadata_value=request.vars.pub_year)

            if request.vars.removefimages != "":
                imagedelete = db(db.clsb20_product_image.product_code == data[0].product_code).select()
                for i in imagedelete:
                    try:
                        os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+i.image)
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

                        db.clsb20_product_image.insert(type_id=type_image['id'], product_code=data[0].product_code, description=file.filename, image="clsb20_product_cp."+data[0].product_code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                    except:
                        continue
                #try:
                #    file = request.vars.imageslist.file
                #    save_file(file.file, "clsb20_product_cp."+data[0].product_code+"."+computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                #    db.clsb20_product_image.insert(product_code=data[0].product_code,description=file.filename,image="clsb20_product_cp."+data[0].product_code+"."+computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                #except:
                #    for file in request.vars.imageslist:
                #        save_file(file.file, "clsb20_product_cp."+data[0].product_code+"."+computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                #        db.clsb20_product_image.insert(product_code=data[0].product_code,description=file.filename,image="clsb20_product_cp."+data[0].product_code+"."+computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
            response.flash = 'Cập nhật thành công'
            return redirect(URL('index',args=['view','clsb20_product_cp', id], user_signature=True))
        elif form.errors:
            response.flash = 'Lỗi: Thông tin không đúng'
        else:
            response.flash = 'Xin mời điền thông tin'
    except Exception as e:
        print e
        response.flash = 'Lỗi: Thông tin không đúng ' + str(e) +" - on line "+str(sys.exc_traceback.tb_lineno)
    #get category_tree
    categories = []
    db_query = db(db.clsb_category.category_parent==None)
    rows = db_query.select(db.clsb_category.id,
                                db.clsb_category.category_name,
                                db.clsb_category.category_order,
                                orderby = ~db.clsb_category.category_order)
    for row in rows:
        print row
        temp = dict()
        temp['category_id'] = row['id']
        temp['category_name'] = row['category_name']
        temp = get_categories(temp)
        categories.append(temp)
    expands=[]
    for cate in categories:
        get_expand_cate(expands, cate)
    return dict(form=form, mcategories=categories, expands=expands)


# @auth.requires_signature()
def update_product_pdf(request, code):
    if request.vars.data_pdf.file:
        try:
            products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code, settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"_Backup", True)
            try:
                os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip")
            except Exception as e:
                print e
            create_dir(user_cp_path+"/upload/"+code+"/"+code)
            create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code)
            create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config")
            f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/.nomedia", "w+")
            f.flush()
            f.close()
            f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/config.xml", "w+")
            f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                        '<configs>'
                        '<bookId>'+code+'</bookId>'
                        '<bookName>'+request.vars.title+'</bookName>'
                        '<firstPageIndex>1</firstPageIndex>'
                        '<contentPageIndex>1</contentPageIndex>'
                        '<pageCountIndex>'+str(request.vars.num_page)+'</pageCountIndex>'
                        '<publisher></publisher>'
                        '<cover-normal>'
                        '<cover>cover.jpg</cover>'
                        '<cover-width>482</cover-width>'
                        '<cover-height>680</cover-height>'
                        '</cover-normal>'
                    '</configs>')
            f.flush()
            f.close()
            products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/cover.clsbi21")
            save_file(request.vars.data_pdf.file, code+"/"+code+"/"+code+"/"+code+".pdf")

            # os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".pdf")
            # os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+".W.pdf")

            shutil.copy("/home/libs/zipfileforpdf.zip", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+".zip")
            #create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code+"_json")


            z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "w")
            zipdir(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code, z)
            z.close()
            shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code)
            print "OK"
        except Exception as ex:
            products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"_Backup", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code, True)
            print "Loi upload " + str(ex)+" - on line "+str(sys.exc_traceback.tb_lineno)

def get_form(action = False):
    if not session.cat_id:
        session.cat_id=54
    #book = db(db.clsb_product).select()
    #creator = db(db.clsb20_dic_creator_cp).select()
    #publisher = db(db.clsb_dic_publisher).select()
    category_parent = db(db.clsb_category.category_parent == None)\
                (db.clsb_category.category_type == db.clsb_product_type.id)\
                (db.clsb_product_type.type_name.like("Book")).select()
    category = db(db.clsb_category.category_parent != None).select()
    subjects = db(db.clsb_subject).select()
    payment = db(~db.clsb20_purchase_type.name.like("Subscriptions")).select()
    classes = db(db.clsb_class).select()
    form = FORM(
        DIV(
            TABLE(
                TR(
                    TD(
                        A(
                            DIV(
                                SPAN(_class="icon leftarrow icon-arrow-left"),
                                " Quản lý sách", _class="btn",
                            ),
                            _href=URL(user_signature=True)
                        ),
                    ),
                ),
                TR(
                    TD(
                        SPAN(INPUT(_type="checkbox", _name="save_cache", _id="save_cache", _value="save_cache", _checked=True)),
                        SPAN("Save to continue"),
                    ),
                ),
                # TR(
                #     TD(
                #         TABLE(
                #             TR(
                #                 TD(LABEL("File Info: ", _class="clsb_label_product"), _class="rows-left"),
                #                 TD(
                #                     INPUT(_name="f_info", _id="f_info", _class="clsb_input_product", _accept=".xlsx", _type="file", _style="")
                #                 )
                #             ),
                #             _style="width: 100%;"
                #         ),
                #         _class="clsb_upload_border"
                #     )
                # ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Tiêu đề sách: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_name="title",_class="clsb_input_product",_style="width: 100%;", requires=IS_NOT_EMPTY()))
                            ),
                            TR(
                                TD(LABEL("Mô tả chi tiết: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(TEXTAREA(_name="content",_class="clsb_input_product",_value=session.description))
                            ),
                            _style="width: 100%;"
                        ),
                        _class="clsb_upload_border"
                    )
                ),
                TR(
                    TD(
                        TABLE(
                            # TR(
                            #     TD(LABEL("Thể loại: ",_class="clsb_label_product"), _class="rows-left"),
                            #     TD(
                            #         SELECT(*[OPTION(category_parent[i]['clsb_category']['category_name'], _value=str(category_parent[i]['clsb_category']['id'])) for i in range(len(category_parent))], _class="clsb_input_product", _id="category_parent"),
                            #     )
                            # ),
                            TR(
                                TD(LABEL("Danh mục: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    SELECT(*[OPTION(category[i].category_name, _value=str(category[i].id)) for i in range(len(category))], _class="clsb_input_product", _name="category",  _id="category"),
                                ),
                            ),
                            TR(
                                TD(LABEL("Môn học: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    SELECT(
                                        *[OPTION(subjects[i].subject_name,_value=subjects[i].id, _selected=True if subjects[i].id == int(session.subjects) else False) for i in range(len(subjects))],
                                        _class="clsb_input_product", _name="subjects", _id="subject", requires=IS_NOT_EMPTY()
                                    ),
                                ),
                                # TD(
                                #     TABLE(
                                #         TR(
                                #             TD(
                                #                 SPAN("Môn học: ", _style="vertical-align: super;"),
                                #                 SELECT(
                                #                     *[OPTION(subjects[i].subject_name,_value=subjects[i].id) for i in range(len(subjects))],
                                #                     _class="clsb_input_product", _style="min-width: 120px; width: 200px", _name="subjects", _id="subject", requires=IS_NOT_EMPTY()
                                #                 ), _style="padding: 0px;"
                                #             ),
                                #             # TD(
                                #             #     SPAN("Lớp: ", _style="vertical-align: super;"),
                                #             #     SELECT(
                                #             #         *[OPTION(classes[i].class_name,_value=classes[i].id) for i in range(len(classes))],
                                #             #         _class="clsb_input_product", _style="min-width: 120px; width: 150px", _name="classes", _id="classes", requires=IS_NOT_EMPTY()
                                #             #     ), _style="padding: 0px;"
                                #             # )
                                #         ),
                                #         _style="width: 100%;"
                                #     )
                                # )
                            ),
                            TR(
                                TD(LABEL("Tác giả: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_style="margin-top: 10px;",_value=session.creator,_class="clsb_input_product",_id="clsb_creator_list", _name="creator", _linkSearch=URL(a='cps',c='creators',f='search'), requires=IS_NOT_EMPTY()),
                                   SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchcreator()"),
                                   DIV("Các tác giả phân cách nhau bằng dấu ';'")),
                            ),
                            TR(
                                TD(LABEL("Nhà xuất bản: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_style="margin-top: 10px;",_value=session.publisher,_class="clsb_input_product",_id="clsb_publisher_list", _name="publisher", _linkSearch=URL(a='cps',c='publishers',f='search'), requires=IS_NOT_EMPTY()),
                                   SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchpublisher()")),
                            ),
                            TR(
                                TD(LABEL("Sách liên quan: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    TABLE(
                                        THEAD(
                                            TR(
                                                TH("ID",_style="background-color: #08c; color: #fff; width: 30%;"),
                                                TH("Tên sách",_style="background-color: #08c; color: #fff; width: 69%;")
                                            )
                                        ),
                                        _id="clsb_list_product_show",
                                        _style="margin-top: 0px; width: 100%;"
                                    ),
                                    INPUT(_name="title_relation",_class="clsb_input_product",_id="clsb_relation_product", _style="display: none;"),
                                    SPAN(INPUT(_style="margin-top: 10px; display: none;", _class="clsb_input_product", _id="clsb_list_product", _linkSearch=URL(a='cbs',c='products',f='search'))),
                                    SPAN(XML("<b>+</b> Thêm sách"),_class="btn",_onclick="javascript:searchrelation()"),
                                    )
                            ),
                            # TR(
                            #     TD(LABEL("Đồng tác giả: ", _class="clsb_label_product"), _class="rows-left"),
                            #     TD(INPUT(_style="width: 100%;", _class="clsb_input_product",_id="clsb_creator_list", _name="creator_more"))
                            # ),
                            TR(
                                TD(LABEL("Năm xuất bản: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_class="clsb_input_product", _name="year_created", _value=session.year_created))
                            ),
                            TR(
                                TD(LABEL("Kích cỡ (cm): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_class="clsb_input_product", _name="size_cover", _value=session.size_cover), SPAN(" (rộng x dài)"))
                            ),
                            TR(
                                TD(LABEL("Số trang: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_class="clsb_input_product", _name="num_page", _value=session.num_page), requires=IS_NOT_EMPTY())
                            ),
                            TR(
                                TD(LABEL("Giá bìa: ", _class="clsb_label_product", _style="font-weight: bold;"), _class="rows-left"),
                                TD(INPUT(_class="clsb_input_product", _name="cover_price", _value=session.cover_price, _style="color: rgb(255, 112, 0);  font-weight: bold;"), "VNĐ")
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
                                            TD(
                                                SPAN("Ảnh minh họa khác(Tối đa 5 ảnh - kích cỡ < 1MB)"),
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
                                TD(),
                                TD(XML("<b>Chú ý:</b> Khi đưa sách PDF, chỉ chọn một trong hai loại dữ liệu ZIP hoặc PDF để tải lên"), _style="color: red;")
                            ),
                            TR(
                                TD(LABEL("Kiểu dữ liệu: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    SELECT(
                                        OPTION('PDF', _value='pdf'),
                                        OPTION('EPUB', _value='epub'),
                                        OPTION('HTML', _value='html'),
                                        _class="clsb_input_product", _id="data_type", _name='data_type'
                                    ),
                                )
                            ),
                            TR(
                                TD(LABEL("Dữ liệu sách (ZIP file): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_name="data", _id="data", _class="clsb_input_product", _accept=".zip", _type="file", _style="display: none;"),
                                    DIV(XML("<b>+</b> Chọn tệp tin ZIP"), _class="btn", _onclick="opendata('data', event)", _id="btn_data"),
                                    SPAN(" Được đóng gói từ ứng dụng CBEditor")
                                )
                            ),
                            TR(
                                TD(LABEL("Dữ liệu sách (file): ", _class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    INPUT(_name="data_pdf", _id="data_pdf", _class="clsb_input_product", _accept=".pdf", _type="file", _style="display: none;"),
                                    DIV(XML("<b>+</b> Chọn tệp tin"), _class="btn", _id="btn_data_pdf", _onclick="opendata('data_pdf', event)")
                                )
                            ),
                            TR(
                                TD(),
                                TD(
                                    # DIV(
                                    #     SPAN(XML("Ảnh bìa cỡ nhỏ<br/>(100x141)px")),
                                    #     XML("<br/>"),
                                    #     INPUT(_name="thumbnail",_class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;"),
                                    #     DIV(XML("+<br/>Add<br/>Thumbnail"), _class="clsb_image thumbnail_cp", _onclick="openimage('thumbnail',event)"),
                                    #     _style="display: inline-block; vertical-align: top;"
                                    # ),
                                    DIV(
                                        SPAN("Ảnh bìa (200x282, 400x564,...)px"),
                                        XML("<br/>"),
                                        INPUT(_name="cover", _class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;"),
                                        DIV(XML("+<br/>Add Cover"), _class="clsb_image cover", _onclick="openimage('cover',event)"),
                                        _style="margin-left: 20px; display: inline-block; vertical-align: top;"
                                    ),
                                ),
                                _id="cover_id",
                                _style="display: none;"
                            ),
                            TR(
                                TD(),
                                TD(XML("<b>Chú ý:</b> Mỗi phương thức thu tiền sẽ có hình thức thu phí khi tải về là khác nhau. <br/> <i>Hình thức miễn phí</i>: mặc định giá cho sản phẩm sẽ là 0 VNĐ, khách hàng sẽ không phải trả tiền cho sản phẩm khi chọn hình thức này.<br/> <i>Hình thức thanh toán cho lần tải đầu tiên</i>: Khác hàng sẽ chỉ phải trả phí cho lần đầu tiên tải sản phẩm, các lần sau sẽ không bị thu phí. <br/> <i>Hình thức thanh toán cho mỗi lượt tải</i>: Khách hàng sẽ phải trả phí cho mỗi lần tải sản phẩm về"), _style="color: #999;")
                            ),
                            TR(
                                TD(LABEL("Phương thức thu tiền: ", _class="clsb_label_product", _style="font-weight:bold;"), _class="rows-left"),
                                TD(
                                    SELECT(*[OPTION(payment[i].description, _value=str(payment[i].name)) for i in range(len(payment))], _id="payment",_style="margin-top: 5px;", _class="clsb_input_product", _name="payment"),
                                    # SELECT(*[OPTION(subscriptions[i].description, _value=str(subscriptions[i].id)) for i in range(len(subscriptions))],_style="margin-top: 5px; display: none;", _class="clsb_input_product", _name="payment_more",_id="payment_more"),
                                    DIV(INPUT(_name="price", _placeholder="Giá tiền", _class="clsb_input_product", _value=0, _style="color: rgb(255, 112, 0); font-weight: bold;"), "VNĐ", _id="price"),
                                    # DIV(B("* Chú ý: "),  XML("Khi chọn phương thức <b>Thanh toán theo thời gian</b> sẽ không thể đổi sang hình thức thanh toán khác khi sản phẩm đã được duyệt"), _style="white-space: normal; text-align: justify;")
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


# @auth.requires_signature()
def create_product():
    if not session.description:
        session.description = ""
    if not session.subjects:
        session.subjects = 1
    if not session.creator:
        session.creator = ""
    if not session.publisher:
        session.publisher = ""
    if not session.year_created:
        session.year_created = ""
    if not session.size_cover:
        session.size_cover = ""
    if not session.num_page:
        session.num_page = ""
    if not session.cover_price:
        session.cover_price = ""
    if not session.save_cache:
        session.save_cache = False
    form = get_form()
    print(session.save_cache)
    if form.accepts(request, session):
        try:
            try:
                # if request.vars.f_info != "":
                #     osFileServer = OSFS("/home/CBSData/")
                #     osFileServer.setcontents("product_info.xlsx", request.vars.f_info)
                #     response.flash = request.vars.f_info
                #     return dict(form=form)
                if request.vars.save_cache is None:
                    session.save_cache = False
                else:
                    session.save_cache = True
                class_id = db(db.clsb_class.class_code.like("None")).select()
                subject_class = None
                cat_id = request.vars.category
                session.cat_id = cat_id
                if len(class_id) > 0:
                    class_id = class_id.first().id
                else:
                    class_id = db.clsb_class.insert(
                        class_name="Khác",
                        class_code="None",
                        class_order="9999",
                    )
                    class_id = class_id.id
                if request.vars.category == "0":
                    cat_id = db(db.clsb_category.category_code.like("None")).select()
                    if len(cat_id) <= 0:
                        cat_id = db.clsb_category.insert(
                            category_name="Danh mục khác",
                            category_code="None",
                            category_order="9999"
                        )
                        cat_id = db.clsb_category.insert(
                            category_name="Khác",
                            category_code="None",
                            category_order="9999",
                            category_parent=cat_id.id
                        )
                        cat_id = cat_id.id
                        device_shelf_check = db(db.clsb20_category_shelf_mapping.category_id == cat_id).select()
                        if len(device_shelf_check) <= 0:
                            db.clsb20_category_shelf_mapping.insert(
                                category_id=cat_id,
                                device_shelf_id=db(db.clsb_device_shelf.device_shelf_code.like("STK")).select().first()['id']
                            )
                    else:
                        cat_id = cat_id.first().id

                    subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == class_id)).select()
                    if len(subject_class) > 0:
                        subject_class = subject_class.first()
                    else:
                        subject_class = db.clsb_subject_class.insert(
                            subject_id=request.vars.subjects,
                            class_id=class_id
                        )
                    session.subjects = request.vars.subjects
                else:
                    map = db(db.clsb20_category_class_mapping.category_id == request.vars.category).select()
                    if len(map) > 0:
                        class_id = map.first().class_id
                    subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == class_id)).select()[0]
            except Exception as e:
                # print("Có lỗi xảy ra: lựa chọn danh mục sách không tương ứng với môn học: "+str(e)+" - on line "+str(sys.exc_traceback.tb_lineno))
                response.flash = "Có lỗi xảy ra: lựa chọn danh mục sách không tương ứng với môn học: "+str(e)+" - on line "+str(sys.exc_traceback.tb_lineno)
                return dict(form=form)
            code = usercp.user_gen_product_code(user_cp_path, db(db.clsb20_product_type.type_name.like("Book")).select()[0].type_code)
            result_str = ""
            create_dir(user_cp_path+"/upload/"+code)
            if request.vars.data != "":
                if request.vars.data.file:
                    if not bool(re.search(".[Zz][Ii][Pp]$", request.vars.data.filename)):
                        response.flash = "Tệp tin ZIP không đúng"
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                        return dict(form=form)
                    if request.vars.data_type == 'pdf':
                        save_data(request.vars.data, code+"/"+code+".zip", code)
                        try:
                            zip_file = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "r")
                            for name in zip_file.namelist():
                                if bool(re.search('cover.[Pp][Nn][Gg]$', name)) or bool(re.search('cover.[Jj][Pp][Gg]$', name)):
                                    f = zip_file.open(name)
                                    print "Name "+ name
                                    save_file(f, code+"/cover.clsbi")
                                    f.close()
                                    break

                            zip_file.close()
                        except Exception as e:
                            response.flash = "Cấu trúc tệp tin ZIP không đúng"
                            shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                            return dict(form=form)

                # if request.vars.cover != "":
                #     if request.vars.cover.file:
                #             save_file(request.vars.cover.file, code+"/cover.clsbi")

            if request.vars.data_pdf != "":
                if request.vars.cover != "":
                    if not bool(re.search(".[Pp][Dd][Ff]$", request.vars.data_pdf.filename)) and request.vars.data_type == 'pdf':
                        response.flash = "Tệp tin PDF không đúng"
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                        return dict(form=form)
                    if not bool(re.search(".[Ee][Pp][Uu][Bb]$", request.vars.data_pdf.filename)) and request.vars.data_type == 'epub':
                        response.flash = "Tệp tin Epub không đúng"
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                        return dict(form=form)
                    if not bool(re.search(".[Hh][Tt][Mm][Ll]$", request.vars.data_pdf.filename)) and request.vars.data_type == 'html':
                        response.flash = "Tệp tin Html không đúng"
                        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                        return dict(form=form)
                    create_product_pdf(request, code)
                else:
                    response.flash = "Dữ liệu tải lên thiếu ảnh bìa"
                    shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                    return dict(form=form)
            try:
                resize_thumb(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/")
                #shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/thumb.png")
            except Exception as e:
                response.flash = "Dữ liệu tải lên thiếu ảnh bìa"
                shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
                return dict(form=form)
            # if request.vars.thumbnail != "":
            #     if request.vars.thumbnail.file:
            #             save_file(request.vars.thumbnail.file, code+"/thumb.png")
            session.creator = request.vars.creator
            # print(session.creator)
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

            publisher = db(db.clsb_dic_publisher.publisher_name == request.vars.publisher).select()

            if len(publisher) <= 0:
                publisher = db.clsb_dic_publisher.insert(publisher_name = request.vars.publisher)
            else:
                publisher = publisher[0]

            session.publisher = request.vars.publisher
            # print(session.publisher)
            try:
                device_shelf = db(db.clsb20_category_shelf_mapping.category_id == cat_id).select()[0]['device_shelf_id']
            except Exception as err:
                device_shelf = 27

            newdata = db.clsb20_product_cp.insert(product_title=request.vars.title,
                                                  product_code=code,
                                                  product_description=request.vars.content,
                                                  subject_class=subject_class.id,
                                                  product_publisher=publisher.id,
                                                  product_creator=creator.id,
                                                  device_shelf_code=device_shelf,
                                                  product_category=cat_id,
                                                  product_price=request.vars.price,
                                                  data_type=request.vars.data_type)

            session.description = request.vars.content

            if request.vars.title_relation != "":
                list = request.vars.title_relation.split(";")
                sum = 0
                for one in list:
                    if (sum>0):
                        db.clsb20_product_relation_cp.insert(product_cp_id=newdata.id, relation_id=one)
                    sum = sum+1


            # if request.vars.creator_more != "":
            #     list_creator = re.split(r"[,;]",request.vars.creator_more)
            #     metadata_id = db(db.clsb_dic_metadata.metadata_name.like("co_author")).select()[0]['id']
            #     for one in list_creator:
            #         db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=one)

            if request.vars.year_created != "":
                session.year_created = request.vars.year_created
                metadata = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="pub_year", metadata_label="Năm xuất bản")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.year_created)

            price_cover = request.vars.price
            if request.vars.cover_price != "":
                session.cover_price = request.vars.cover_price
                price_cover = request.vars.cover_price
            metadata = db(db.clsb_dic_metadata.metadata_name.like("cover_price")).select()
            if len(metadata) <= 0:
                db.clsb_dic_metadata.insert(metadata_name="cover_price", metadata_label="Giá bìa")
            metadata_id = db(db.clsb_dic_metadata.metadata_name.like("cover_price")).select()[0]['id']
            db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=price_cover)


            if request.vars.size_cover != "":
                session.size_cover = request.vars.size_cover
                metadata = db(db.clsb_dic_metadata.metadata_name.like("format")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="format", metadata_label="Kích cỡ")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("format")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.size_cover)

            if request.vars.num_page != "":
                session.num_page = request.vars.num_page
                metadata = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()
                if len(metadata) <= 0:
                    db.clsb_dic_metadata.insert(metadata_name="page_number", metadata_label="Số trang")
                metadata_id = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()[0]['id']
                db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.num_page)

            if request.vars.payment != "":
                if request.vars.payment.upper() == "SUBSCRIPTIONS":
                    purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
                else:
                    purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.payment)).select()[0].id
                    purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id

                db.clsb20_product_purchase_item.insert(product_code=newdata.product_code, purchase_item=purchase_item)

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
                        db.clsb20_product_image.insert(type_id=type_image['id'], product_code=code, description=file.filename, image="clsb20_product_cp."+code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                    except:
                        continue
            if not session.save_cache:
                print "clear cache"
                session.description = ""
                session.subjects = 1
                session.creator = ""
                session.publisher = ""
                session.year_created = ""
                session.size_cover = ""
                session.num_page = ""
                session.cover_price = ""
            response.flash = 'Thành công'
        except Exception as e:
            print e
            response.flash = 'Xảy ra lỗi trong quá trình tải lên ' + str(e) + " on line: "+str(sys.exc_traceback.tb_lineno)
    elif form.errors:
        response.flash = 'Thông tin không đúng'
    else:
        response.flash = 'Xin mời điền vào form'
    #get category_tree
    categories = []
    db_query = db(db.clsb_category.category_parent==None)
    rows = db_query.select(db.clsb_category.id,
                                db.clsb_category.category_name,
                                db.clsb_category.category_order,
                                orderby = ~db.clsb_category.category_order)
    for row in rows:
        # print row
        temp = dict()
        temp['category_id'] = row['id']
        temp['category_name'] = row['category_name']
        temp = get_categories(temp)
        categories.append(temp)
    expands=[]
    for cate in categories:
        get_expand_cate(expands, cate)
    return dict(form=form, mcategories=categories, expands=expands)


def get_expand_cate(expands, cate):
    for child in cate['children']:
        if child['category_id'] == int(session.cat_id):
            expands.append(cate['category_id'])
        get_expand_cate(expands, child)
    return


def get_categories(root):
    try:
        db_query = db(db.clsb_category.category_parent == root['category_id'])
        children = list()
        rows = db_query.select(db.clsb_category.id,
                                    db.clsb_category.category_name,
                                    db.clsb_category.category_order,
                                    orderby=~db.clsb_category.category_order)
        for child in rows:
            temp = dict()
            temp['category_id'] = child['id']
            temp['category_name'] = child['category_name']
            temp = get_categories(temp)
            children.append(temp)
        root['children'] = children
        return root
    except Exception as ex:
        import sys
        print(ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))

# @auth.requires_signature()
def create_product_pdf(request, code):

    create_dir(user_cp_path+"/upload/"+code+"/"+code)
    create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code)
    create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config")
    f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/.nomedia", "w+")
    f.flush()
    f.close()
    f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/config.xml", "w+")
    f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                '<configs>'
                    '<bookId>'+code+'</bookId>'
                    '<bookName>'+request.vars.title+'</bookName>'
                    '<firstPageIndex>1</firstPageIndex>'
                    '<contentPageIndex>1</contentPageIndex>'
                    '<pageCountIndex>'+request.vars.num_page+'</pageCountIndex>'
                    '<publisher></publisher>'
                    '<cover-normal>'
                        '<cover>cover.jpg</cover>'
                        '<cover-width>482</cover-width>'
                        '<cover-height>680</cover-height>'
                    '</cover-normal>'
                '</configs>')
    f.flush()
    f.close()

    book_config_str = '{"id":"' + code + '","contentPageIndex":' + str(request.vars.num_page) + ',"pageCountIndex":' + str(request.vars.num_page) + ',"numberPages":' + str(request.vars.num_page) + ',"publisher":null,"bookName":"' + request.vars.title + '"}'
    if request.vars.cover.file:
        save_file(request.vars.cover.file, code+"/"+code+"/"+code+"/book_config/cover.clsbi21")
        shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/cover.clsbi21", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi")
    if request.vars.data_pdf.file:
        if request.vars.data_type == 'epub':
            save_file(request.vars.data_pdf.file, code+"/"+code+"."+str(request.vars.data_type))
        elif request.vars.data_type == 'html':
            #create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/" + request.vars.data.filename)
            save_file(request.vars.data_pdf.file, code+"/"+code+"."+str(request.vars.data_type))
            save_file(request.vars.data.file, code+"/"+request.vars.data.filename)
            with zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+request.vars.data.filename, "r") as z:
                z.extractall(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code)
                z.close()
            os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+request.vars.data.filename)
        else:
            save_file(request.vars.data_pdf.file, code+"/"+code+"/"+code+"/"+code+".pdf")
        shutil.copy("/home/libs/zipfileforpdf.zip", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+".zip")
        try:
            create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json")
            target = open_file(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json" + "/" + "bookconfig.txt" )
            target.write(book_config_str)
            target.close()

            target = open_file(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json" + "/" + "addtional.txt")
            target.write("{}")
            target.close()

            target = open_file(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json" + "/" + "clickable.txt")
            target.write("{}")
            target.close()


            target = open_file(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json" + "/" + "metadata.txt")
            target.write("[]")
            target.close()

            z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "w")
            zipdir(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code, z)
            z.close()
        except Exception as e:
            print str(e)
        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code)

    # old form
    # category = db((~db.clsb_category.category_code.like("UDHT")) & (~db.clsb_category.category_code.like("APP"))).select()
    # device = db((~db.clsb_device_shelf.device_shelf_code.like("APP")) & (~db.clsb_device_shelf.device_shelf_code.like("UDHT")) & (~db.clsb_device_shelf.device_shelf_code.like("EDUGAME"))).select(orderby=db.clsb_device_shelf.shelf_order)
    # subjects = db(db.clsb_subject).select()
    # payment = db(db.clsb20_purchase_type).select()
    # subscriptions = db(db.clsb20_purchase_item.purchase_type == db(db.clsb20_purchase_type.name.like("Subscriptions")).select()[0].id).select()
    # classes = db(db.clsb_class).select()
    # form = FORM(
    #     DIV(
    #         TABLE(
    #             TR(
    #                 TD(
    #                     A(
    #                         DIV(
    #                             SPAN(_class="icon leftarrow icon-arrow-left"),
    #                             " Products", _class="btn"
    #                         ),
    #                         SPAN(" "),
    #                         A(
    #                             DIV(
    #                                 "Upload ZIP", _class="btn"
    #                             ),
    #                             _href=URL(args=["new", "clsb20_product_cp"], user_signature=True)
    #                         ),
    #                         _href=URL(user_signature=True)
    #                     ),
    #                 ),
    #             ),
    #             TR(
    #                 TD(
    #                     TABLE(
    #                         TR(
    #                             TD(LABEL("Tiêu đề sách: ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(INPUT(_name="title",_class="clsb_input_product",_style="width: 100%;", requires=IS_NOT_EMPTY()))
    #                         ),
    #                         TR(
    #                             TD(LABEL("Mô tả chi tiết: ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(TEXTAREA(_name="content",_class="clsb_input_product"))
    #                         ),
    #                         _style="width: 100%;"
    #                     ),
    #                     _class="clsb_upload_border"
    #                 )
    #             ),
    #             TR(
    #                 TD(
    #                     TABLE(
    #                         TR(
    #                             TD(LABEL("Category: ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(SELECT(*[OPTION(category[i].category_name, _value=str(category[i].id)) for i in range(len(category))], _style="margin-top: 5px;",_class="clsb_input_product", _name="category"))
    #                         ),
    #                         TR(
    #                             TD(),
    #                             TD(
    #                                 TABLE(
    #                                     TR(
    #                                         TD(
    #                                             SELECT(
    #                                                 *[OPTION(subjects[i].subject_name,_value=subjects[i].id) for i in range(len(subjects))],
    #                                                 _class="clsb_input_product", _style="min-width: 150px", _name="subjects", requires=IS_NOT_EMPTY()
    #                                             ), _style="padding: 0px;"
    #                                         ),
    #                                         TD(
    #                                             SELECT(
    #                                                 *[OPTION(classes[i].class_name,_value=classes[i].id) for i in range(len(classes))],
    #                                                 _class="clsb_input_product", _style="min-width: 150px", _name="classes", requires=IS_NOT_EMPTY()
    #                                             ), _style="padding: 0px;"
    #                                         )
    #                                     )
    #                                 )
    #                             )
    #                         ),
    #                         TR(
    #                             TD(LABEL("Tác giả: ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(INPUT(_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_creator_list", _name="creator", _linkSearch=URL(a='cps',c='creators',f='search.json'), requires=IS_NOT_EMPTY()),
    #                                SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchcreator()")),
    #                         ),
    #                         TR(
    #                             TD(LABEL("Bản quyền: ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(INPUT(_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_publisher_list", _name="publisher", _linkSearch=URL(a='cps',c='publishers',f='search.json'), requires=IS_NOT_EMPTY()),
    #                                SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchpublisher()")),
    #                         ),
    #                         TR(
    #                             TD(LABEL("Sách liên quan: ", _class="clsb_label_product"), _class="rows-left"),
    #                             TD(
    #                                 TABLE(
    #                                     THEAD(
    #                                         TR(
    #                                             TH("ID",_style="background-color: #08c; color: #fff; width: 30%;"),
    #                                             TH("Tên sách",_style="background-color: #08c; color: #fff; width: 69%;")
    #                                         )
    #                                     ),
    #                                     _id="clsb_list_product_show",
    #                                     _style="margin-top: 0px; width: 100%;"
    #                                 ),
    #                                 INPUT(_name="title_relation",_class="clsb_input_product",_id="clsb_relation_product", _style="display: none;"),
    #                                 SPAN(INPUT(_style="margin-top: 10px;", _class="clsb_input_product", _id="clsb_list_product", _linkSearch=URL(a='cbs',c='products',f='search.json',args=['0','10','Book']))),
    #                                 SPAN(XML("<b>+</b> Thêm sách"),_class="btn",_onclick="javascript:searchrelation()"),
    #                             )
    #                         ),
    #                         _style="width: 100%;"
    #                     ),
    #                     _class="clsb_upload_border"
    #                 )
    #             ),
    #             TR(
    #                 TD(
    #                     TABLE(
    #                         TR(
    #                             TD(LABEL("Đồng tác giả: ", _class="clsb_label_product"), _class="rows-left"),
    #                             TD(INPUT(_style="width: 100%;", _class="clsb_input_product",_id="clsb_creator_list", _name="creator_more"))
    #                         ),
    #                         TR(
    #                             TD(LABEL("Năm xuất bản: ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(INPUT(_class="clsb_input_product", _name="year_created"))
    #                         ),
    #                         TR(
    #                             TD(LABEL("Kích cỡ (cm): ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(INPUT(_class="clsb_input_product", _name="size_cover"))
    #                         ),
    #                         TR(
    #                             TD(LABEL("Số trang: ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(INPUT(_class="clsb_input_product", _name="num_page", requires=IS_NOT_EMPTY()))
    #                         ),
    #                         _style="width: 100%;"
    #                     ),
    #                     _class="clsb_upload_border"
    #                 )
    #             ),
    #             TR(
    #                 TD(
    #                     TABLE(
    #                         TR(
    #                             TD(
    #                                 TABLE(
    #                                     TR(
    #                                         TD(
    #                                             SPAN("Ảnh Thumbnail"),
    #                                             XML("<br/>"),
    #                                             INPUT(_name="thumbnail",_class="clsb_input_product",_accept="image/*", _type="file", _style="display: none;"),
    #                                             DIV(XML("+<br/>Add Thumbnail"), _class="clsb_image thumbnail_cp", _onclick="openimage('thumbnail',event)"),
    #                                         ),
    #                                         TD(
    #                                             SPAN("Ảnh Cover"),
    #                                             XML("<br/>"),
    #                                             INPUT(_name="cover", _class="clsb_input_product", _accept="image/*", _type="file", _style="display: none;", requires=IS_NOT_EMPTY()),
    #                                             DIV(XML("+<br/>Add Cover"), _class="clsb_image cover", _onclick="openimage('cover',event)"),
    #                                         ),
    #                                         TD(
    #                                             SPAN("Features Image (Tối đa 5 ảnh - kích cỡ < 1MB)"),
    #                                             DIV(
    #                                                 INPUT(_name="feature_images_1", _id="feature_images_1", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
    #                                                 INPUT(_name="feature_images_2", _id="feature_images_2", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
    #                                                 INPUT(_name="feature_images_3", _id="feature_images_3", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
    #                                                 INPUT(_name="feature_images_4", _id="feature_images_4", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
    #                                                 INPUT(_name="feature_images_5", _id="feature_images_5", _class="clsb_input_product", _type="file",_accept="image/*", _style="display: none;"),
    #                                                 DIV(XML("<b>+</b> Thêm ảnh"), _class="btn", _onclick="addimagesborder('#imglist')"),
    #                                                 XML("<br/>"),
    #                                                 DIV(_id="imglist",_class="border_imglist")
    #                                             ),
    #                                             _style="overflow: auto;"
    #                                         )
    #                                     )
    #                                 )
    #                             )
    #                         ),
    #                         _style="width: 100%;"
    #                     ),
    #                     _class="clsb_upload_border"
    #                 )
    #             ),
    #             TR(
    #                 TD(
    #                     TABLE(
    #                         TR(
    #                             TD(LABEL("Dữ liệu sách (PDF file): ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(
    #                                 INPUT(_name="data",_class="clsb_input_product", _accept=".pdf", _type="file", _style="display: none;", requires=IS_NOT_EMPTY()),
    #                                 DIV(XML("<b>+</b> Chọn tệp tin PDF"), _class="btn", _onclick="opendata('data')")
    #                             )
    #                         ),
    #                         TR(
    #                             TD(LABEL("Phương thức thu tiền: ",_class="clsb_label_product"), _class="rows-left"),
    #                             TD(
    #                                 SELECT(*[OPTION(payment[i].description, _value=str(payment[i].name)) for i in range(len(payment))], _id="payment",_style="margin-top: 5px", _class="clsb_input_product", _name="payment"),
    #                                 SELECT(*[OPTION(subscriptions[i].description, _value=str(subscriptions[i].id)) for i in range(len(subscriptions))], _style="margin-top: 5px; display: none;", _class="clsb_input_product", _name="payment_more",_id="payment_more"),
    #                                 DIV(INPUT(_name="price", _placeholder="Giá tiền", _class="clsb_input_product", _value=0), "VNĐ", _id="price"),
    #                                 DIV(B("* Chú ý: "),  XML("Khi chọn phương thức <b>Thanh toán theo thời gian</b> sẽ không thể đổi sang hình thức thanh toán khác"), _style="white-space: normal; text-align: justify;")
    #                             )
    #                         ),
    #                         _style="width: 100%;"
    #                     ),
    #                     _class="clsb_upload_border"
    #                 )
    #             ),
    #             INPUT(_type="submit", _class="clsb_submit_upload", _value="Hoàn thành"),
    #             _class="clsb_table_product"
    #         ),
    #         #_class="clsb_upload_border"
    #     ),
    #     _class="clsb_form_upload"
    # )
    # if form.accepts(request, session):
    #     try:
    #         code = usercp.user_gen_product_code(user_cp_path, db(db.clsb20_product_type.type_name.like("Book")).select()[0].type_code)
    #         create_dir(user_cp_path+"/upload/"+code)
    #         create_dir(user_cp_path+"/upload/"+code+"/"+code)
    #         create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code)
    #         create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config")
    #         f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/.nomedia", "w+")
    #         f.close()
    #         f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/config.xml", "w+")
    #         f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    #                     '<configs>'
    #                         '<bookId>'+code+'</bookId>'
    #                         '<bookName>'+request.vars.title+'</bookName>'
    #                         '<firstPageIndex>1</firstPageIndex>'
    #                         '<contentPageIndex>1</contentPageIndex>'
    #                         '<pageCountIndex>'+request.vars.num_page+'</pageCountIndex>'
    #                         '<publisher></publisher>'
    #                         '<cover-normal>'
    #                             '<cover>cover.jpg</cover>'
    #                             '<cover-width>482</cover-width>'
    #                             '<cover-height>680</cover-height>'
    #                         '</cover-normal>'
    #                     '</configs>')
    #         f.close()
    #         if request.vars.cover.file:
    #             save_file(request.vars.cover.file, code+"/"+code+"/"+code+"/book_config/cover.clsbi")
    #             shutil.copy(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/cover.clsbi", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi")
    #         if request.vars.data.file:
    #             save_file(request.vars.data.file, code+"/"+code+"/"+code+"/"+code+".pdf")
    #             shutil.copy(settings.home_dir+settings.cp_dir+"zipfileforpdf.zip", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+".zip")
    #
    #             z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "w")
    #             zipdir(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code, z)
    #             z.close()
    #             shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code)
    #
    #             creator = db(db.clsb20_dic_creator_cp.creator_name == request.vars.creator).select()
    #             publisher = db(db.clsb_dic_publisher.publisher_name == request.vars.publisher).select()
    #             if(len(creator)<=0):
    #                 creator = db.clsb20_dic_creator_cp.insert(creator_name = request.vars.creator)
    #             else:
    #                 creator = creator[0]
    #             if(len(publisher)<=0):
    #                 publisher = db.clsb_dic_publisher.insert(publisher_name = request.vars.publisher)
    #             else:
    #                 publisher = publisher[0]
    #             subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == request.vars.classes)).select()[0]
    #             device_shelf = db(db.clsb20_category_shelf_mapping.category_id == request.vars.category).select()[0]['device_shelf_id']
    #             newdata = db.clsb20_product_cp.insert(product_title=request.vars.title,
    #                                                     product_code=code,
    #                                                     product_description=request.vars.content,
    #                                                     subject_class=subject_class.id,
    #                                                     product_publisher=publisher.id,
    #                                                     product_creator=creator.id,
    #                                                     device_shelf_code=device_shelf,
    #                                                     product_category=request.vars.category,
    #                                                     product_price=request.vars.price);
    #
    #             if(request.vars.title_relation!=""):
    #                 list = request.vars.title_relation.split(";")
    #                 sum = 0
    #                 for one in list:
    #                     if (sum>0):
    #                         db.clsb20_product_relation_cp.insert(product_cp_id=newdata.id, relation_id=one)
    #                     sum = sum+1
    #
    #             if request.vars.creator_more != "":
    #                 list_creator = re.split(r"[,;]",request.vars.creator_more)
    #                 metadata_id = db(db.clsb_dic_metadata.metadata_name.like("co_author")).select()[0]['id']
    #                 for one in list_creator:
    #                     db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=one)
    #
    #             if request.vars.year_created != "":
    #                 metadata_id = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()[0]['id']
    #                 db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.year_created)
    #
    #             if request.vars.size_cover != "":
    #                 metadata_id = db(db.clsb_dic_metadata.metadata_name.like("format")).select()[0]['id']
    #                 db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.size_cover)
    #
    #             if request.vars.num_page != "":
    #                 metadata_id = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()[0]['id']
    #                 db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.num_page)
    #
    #
    #             if request.vars.thumbnail != "":
    #                 if request.vars.thumbnail.file:
    #                     save_file(request.vars.thumbnail.file, code+"/thumb.png")
    #
    #             if request.vars.payment != "":
    #                 if request.vars.payment.upper() == "SUBSCRIPTIONS":
    #                     purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
    #                 else:
    #                     purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.payment)).select()[0].id
    #                     purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id
    #
    #                 db.clsb20_product_purchase_item.insert(product_code=newdata.product_code, purchase_item=purchase_item)
    #
    #             type_image = db(db.clsb20_image_type.name.like("Features")).select()
    #             if len(type_image) <= 0:
    #                 type_image = db.clsb20_image_type.insert(name="Features", description="Features Images")
    #             else:
    #                 type_image = type_image[0]
    #             for i in range(1, 6):
    #                 if request.vars['feature_images_'+str(i)] != "":
    #                     try:
    #                         file = request.vars['feature_images_'+str(i)]
    #                         save_file(file.file, "clsb20_product_cp."+code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
    #                         db.clsb20_product_image.insert(type_id=type_image['id'], product_code=code,description=file.filename,image="clsb20_product_cp."+code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
    #                     except:
    #                         continue
    #
    #                 response.flash = 'Upload Success'
    #     except Exception as e:
    #         response.flash = "Error: "+e.message +" - on line "+str(sys.exc_traceback.tb_lineno)
    # elif form.errors:
    #     response.flash = 'Form has errors'
    # else:
    #     response.flash = 'Please fill the form'
    #
    # return dict(form=form)


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
        # shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/published/"+data[0].product_code+"_Backup")
        session.flash = 'Xóa thành công'
    except Exception as e:
        response.flash = "Không tồn tại thư mục"
    redirect(URL("index", user_signature=True))


@auth.requires_signature()
def topending():
    id = request.args[0]
    data = db(db.clsb20_product_cp.id==id)
    if data.select()[0].product_status == "Pending":
        session.flash = "Sách đang được kiểm duyệt"
    else:
        result = products.validate_zip(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data.select()[0].product_code+"/"+data.select()[0].product_code+".zip", "Book")
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


@auth.requires_signature()
def disablepending():
    id = request.args[0]
    data = db(db.clsb20_product_cp.id == id)
    dbproduct = data.select()[0]
    if dbproduct.product_status == "Pending":
        session.flash = "Sách đang đượcc kiểm duyệt"
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
    # return redirect(URL(a="cpa", c="products", f="index", args=[str(id)], user_signature=True))


def save_file(file, filename):
    try:
        f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+filename, 'w+')
        for chunk in products.fbuffer(file):
            f.write(chunk)
        f.close()
    except Exception as e:
        print e


def save_data(file, filename, code=""):
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
            #with zipfile.ZipFile(settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+old_filename, "r") as z:
            #    z.extractall(settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code)
            #    z.close()
            #os.rename(settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code+"/"+old_filename[:-4], settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code+"/"+code)
            #os.rename(settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code+"/"+code+"/"+old_filename, settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code+"/"+code+"/"+code+".zip")
            #try:
            #    os.rename(settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code+"/"+code+"/"+old_filename[:-4]+".E.pdf", settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code+"/"+code+"/"+code+".E.pdf")
            #except:
            #    os.rename(settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code+"/"+code+"/"+old_filename[:-4]+".pdf", settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code+"/"+code+"/"+code+".E.pdf")
            z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+old_filename, "r")
            zip = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+filename, 'w')
            #zipdir(settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code, zip)
            for name in z.namelist():
                buffer_data = z.read(name)
                if name.find(old_filename[:-4]) >= 0:
                    zip.writestr(name.replace(old_filename[:-4], code), buffer_data)
                else:
                    zip.writestr(name, buffer_data)
            zip.close()
            z.close()
            #shutil.rmtree(settings.home_dir+settings.cp_dir+path+"/upload/"+code+"/"+code)
            os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+old_filename)
            msg = "OK"
        except Exception as ex:
            shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
            try:
                products.copyanything(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"_Backup", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code)
            except:
                create_dir(user_cp_path+"/upload/"+code)
            msg = "Faile: "+ex.message
    return msg


def zipdir(path, zip):
    for base, dirs, files in os.walk(path):
        for d in files:
            zip_name = os.path.join(base, d).replace("%s%s" % (path, os.path.sep), '')
            read_file = open(os.path.join(base, d), "rb")
            zip.writestr(zip_name, read_file.read())
            read_file.close()
        for d in dirs:
            zip_name = os.path.join(base, d).replace("%s%s" % (path, os.path.sep), '')
            zip.writestr(zip_name + "/", '')


# @auth.requires_authorize()
def index():
    try:
        if request.url.find('/new/clsb20_product_cp') >= 0:
            return create_product()
        if request.url.find('/edit/clsb20_product_cp') >= 0:
            return update_product()
        if request.url.find('/view/clsb20_product_cp') >= 0:
            return view_product()
        if request.url.find('/delete/clsb20_product_cp') >= 0:
            return remove_product()
        if request.url.find('/edit/clsb20_product_from_editor') >= 0:
            return update_from_editor()
        if request.url.find('/delete/clsb20_product_from_editor') >= 0:
            return remove_from_editor()
        user_info = usercp.user_get_info(auth.user.id, db)
        query = None
        query_status = ~db.clsb20_product_cp.product_status.like("%delete%")
        if request.vars.product_status:
            if request.vars.product_status != "0":
                query_status = db.clsb20_product_cp.product_status.like(request.vars.product_status)
        if user_info['user_info']['is_admin'] == True:
            query = db(query_status)\
                        ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Book")))\
                        ((db.clsb_category.id == db.clsb20_product_cp.product_category) & (((db.auth_user.created_by == auth.user.id) & (db.auth_user.id == db.clsb20_product_cp.created_by)) | (db.clsb20_product_cp.created_by == auth.user.id)))
        else:
            query = db((query_status) & (db.clsb20_product_cp.created_by == auth.user.id))\
                        ((db.clsb_product_type.id == db.clsb_category.category_type) & (db.clsb_product_type.type_name.like("Book")))\
                        (db.clsb_category.id == db.clsb20_product_cp.product_category)

        if request.vars.keyword:
            keyword = request.vars.keyword
            search = ((db.clsb20_product_cp.product_code == keyword)\
                        | (db.clsb20_product_cp.product_title.like('%' + keyword + '%')))
                        # | (db.clsb20_dic_creator_cp.creator_name.like('%' + keyword + '%'))\
                        # | (db.clsb_dic_publisher.publisher_name.like('%' + keyword + '%')))
            query = query(search)
        if request.vars.category_searh:
            cat = int(request.vars.category_searh)
            if cat != 0:
                cat = (db.clsb_category.id == cat)
                query = query(cat)

        print query
        categories = db(db.clsb_category.category_parent != None)\
                        (db.clsb_category.category_type == db.clsb_product_type.id)\
                        (db.clsb_product_type.type_name.like("Book")).select()
        product_list = query.select(groupby=db.clsb20_product_cp.id, orderby=~db.clsb20_product_cp.created_on)

        form_editor = db(((db.auth_user.created_by == auth.user.id) & (db.clsb20_product_from_editor.created_by == db.auth_user.id)) | (db.clsb20_product_from_editor.created_by == auth.user.id)).select(groupby=db.clsb20_product_from_editor.id, orderby=~db.clsb20_product_from_editor.created_on)
        return dict(product_list=product_list, user_cp_path=user_cp_path, categories=categories, form_editor=form_editor)
    except Exception as e:
        print e
        pass


@auth.requires_signature()
def metadata():
    links = [{
                'header': 'Loại thông tin',
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
        product = db(db.clsb20_product_cp.product_code == code).select()[0]
        if len(product_public.select()) > 0:
            id = product_public.select()[0].id
            db(db.clsb_product_metadata.product_id == id).delete()
            relation = db(db.clsb20_product_metadata_cp.product_code == product.product_code).select()
            for item in relation:
                db.clsb_product_metadata.insert(product_id=id, metadata_id=item.metadata_id, metadata_value=item.metadata_value)
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
                TD(LABEL("Mã sách:")),
                TD(INPUT(_value=code, _disabled=True))
            ),
            TR(
                TD(LABEL("Kiểu thông tin:")),
                TD(SELECT(*[OPTION(metadata[i].metadata_label, _value=metadata[i].id) for i in range(len(metadata))], _name="metadata_id"))
            ),
            TR(
                TD(LABEL("Giá trị:")),
                TD(TEXTAREA(_name="metadata_value"))
            ),
            TR(
                TD(),
                TD(INPUT(_type="submit", _value="Chấp nhận"))
            )
        )
    )
    if form.accepts(request, session):
        db.clsb20_product_metadata_cp.insert(product_code=code, metadata_id=request.vars.metadata_id, metadata_value=request.vars.metadata_value)
        result =  copy_metadata(code)
        if result=="OK":
            response.flash = "Thành công!!!"
        else:
            response.flash = result
    if form.errors:
        response.flash = "Lỗi !!!"
    return dict(form=form)


def change_price():
    try:
        print request.vars
        print request.args
        id = request.args[0]
        price = request.vars.request_data1
        payment_type_id = request.vars.request_data2
        dbproduct = db(db.clsb20_product_cp.id == id)
        product = dbproduct.select()[0]
        data = db(db.clsb20_product_cp.id == id).select()
        product_public = db(db.clsb_product.product_code == product.product_code)
        purchase_item = db(db.clsb20_product_purchase_item.product_code.like(product.product_code)).select()[0]

        #if db(db.clsb20_purchase_item.id == purchase_item['purchase_item']).select()[0]['name'].upper() == "FREE":
        #    print 'free'
        #    price = 0
        result = dbproduct.update(product_price=int(price))
        db.clsb20_product_price_history.insert(product_id=id, purchase_item=purchase_item['purchase_item'], price=price, changing_time=datetime.now())
        if len(product_public.select()) > 0:
            product_public.update(product_price=int(price))

        if request.vars.request_data2.upper() == "SUBSCRIPTIONS":
                purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
        else:
            purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.request_data2)).select()[0].id
            purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id

        #price = data[0].product_price

        if request.vars.request_data2.upper() == "FREE":
            price = 0
            db(db.clsb20_product_cp.product_code == data[0].product_code).update(product_price=price)
            db(db.clsb_product.product_code == data[0].product_code).update(product_price=price)
            data = db(db.clsb20_product_cp.id == id).select()
        db(db.clsb20_product_purchase_item.product_code.like(data[0].product_code)).update(purchase_item=purchase_item)

        print 'price'+ str(price)
        result1 = db.clsb20_product_price_history.insert(product_id=id, purchase_item=purchase_item, price=price, changing_time=datetime.now())
        print 'kq:' + str(result1)
        #print db.
        
        session.flash = "Thành công"
        return "OK"
    except Exception as ex:
        session.flash = "Error: "+ex.message
    return "OK"
    # return redirect(URL('index', args=['view', 'clsb20_product_cp', product.id], user_signature=True))


def search():
    try:
        products = list()
        page = 0
        category_type = None
        items_per_page = settings.items_per_page
        total_items = 0
        total_pages = 0
        if request.vars:
            keyword = request.vars["store_search"]

            #Pagination
            try:
                if len(request.args) > 0: page = int(request.args[0])
                if len(request.args) > 1: items_per_page = int(request.args[1])
                #PhuongNH : request.args[2] : category_type
                if len(request.args) > 2: category_type = request.args[2]
                print category_type
            except (TypeError, ValueError): pass
            limitby = (page * items_per_page, (page + 1) * items_per_page)
            # if request containt category_type
            if category_type != None :
                category_id = db(db.clsb_product_type.type_name.like('%' + category_type + '%')).select(db.clsb_product_type.id)
                query = db((db.clsb20_product_cp.created_by == db.auth_user.id)&((db.clsb20_product_cp.product_code == keyword)\
                                | (db.clsb20_product_cp.product_title.like('%' + keyword + '%'))\
                                | (db.clsb20_dic_creator_cp.creator_name.like('%' + keyword + '%'))\
                                | (db.clsb_dic_publisher.publisher_name.like('%' + keyword + '%'))) & (~db.clsb20_product_cp.product_status.like("%delete%")) & (db.clsb_category.category_type == int(category_id[0].id)))\
                (db.clsb20_product_cp.product_creator == db.clsb20_dic_creator_cp.id)\
                (db.clsb20_product_cp.product_publisher == db.clsb_dic_publisher.id)\
                (db.clsb_category.category_type == db.clsb_product_type.id)\
                (db.clsb20_product_cp.product_category == db.clsb_category.id)\
                ((db.auth_user.id==usercp.user_get_id_cp(session.auth.user.id,db))|(db.auth_user.id==auth.user.id)|(db.auth_user.created_by==usercp.user_get_id_cp(session.auth.user.id,db)))

                total_items = query.count()

                total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

                db_product = query.select(db.clsb20_product_cp.id,
                                          db.clsb_category.ALL,
                                          db.clsb_product_type.type_name,
                                          db.clsb20_dic_creator_cp.creator_name,
                                          db.clsb_dic_publisher.publisher_name,
                                          db.clsb20_product_cp.product_title,
                                          db.clsb20_product_cp.product_price,
                                          db.clsb20_product_cp.product_code, limitby = limitby, groupby=db.clsb20_product_cp.id).as_list()
            else:
                query = db(((db.clsb20_product_cp.created_by == auth.user.id) & (db.clsb20_product_cp.product_code == keyword) & (~db.clsb20_product_cp.product_status.like("%delete%")))\
                            | (db.clsb20_product_cp.product_title.like('%' + keyword + '%'))\
                            | (db.clsb20_dic_creator_cp.creator_name.like('%' + keyword + '%'))\
                            | (db.clsb_dic_publisher.publisher_name.like('%' + keyword + '%')))\
                            (db.clsb20_product_cp.product_creator == db.clsb20_dic_creator_cp.id)\
                            (db.clsb20_product_cp.product_publisher == db.clsb_dic_publisher.id)\
                            (db.clsb_category.category_type == db.clsb_product_type.id)\
                            (db.clsb20_product_cp.product_category == db.clsb_category.id)
                total_items = query.count()

                total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

                db_product = query.select(db.clsb20_product_cp.id,
                                          db.clsb_category.ALL,
                                          db.clsb_product_type.type_name,
                                          db.clsb20_dic_creator_cp.creator_name,
                                          db.clsb_dic_publisher.publisher_name,
                                          db.clsb20_product_cp.product_title,
                                          db.clsb20_product_cp.product_price,
                                          db.clsb20_product_cp.product_code, limitby = limitby).as_list()

            if db_product:
                for row in db_product:
                    temp = dict()
                    temp['id'] = row['clsb20_product_cp']['id']
                    temp['category_id'] = row['clsb_category']['id']
                    temp['category_name'] = row['clsb_category']['category_name']
                    temp['category_code'] = row['clsb_category']['category_code']
                    temp['category_type'] = row['clsb_product_type']['type_name']
                    temp['creator_name'] = row['clsb20_dic_creator_cp']['creator_name']
                    temp['publisher_name'] = row['clsb_dic_publisher']['publisher_name']
                    temp['product_title'] = row['clsb20_product_cp']['product_title']
                    temp['product_code'] = row['clsb20_product_cp']['product_code']
                    temp['product_price'] = row['clsb20_product_cp']['product_price']
#                    temp['product_description'] = row['clsb_product']['product_description']
                    products.append(temp)
        return dict(page = page, total_items = total_items, total_pages = total_pages, items_per_page = items_per_page, products = products)
    except Exception as ex:
        return dict(error = ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def create_dir(directory):
    if URL().find('create_dir') >= 0:
        raise HTTP(404)
    if not os.path.exists(settings.home_dir+settings.cp_dir+directory):
        os.makedirs(settings.home_dir+settings.cp_dir+directory, 0770)

def open_file(file):
    return open(settings.home_dir+settings.cp_dir + file, 'w')


@auth.requires_signature()
def update_from_editor():
    if len(request.args) < 1:
        return dict(error="Không tồn tại truy vấn")
    id = int(request.args[2])
    data = db(db.clsb20_product_from_editor.id == id)
    data = data.select()
    if len(data) <= 0:
        session.flash = "Không tồn tại sản phẩm"
        return dict()
    category_parent = db(db.clsb_category.category_parent == None)\
                (db.clsb_category.category_type == db.clsb_product_type.id)\
                (db.clsb_product_type.type_name.like("Book")).select()
    category = db(db.clsb_category.category_parent == category_parent.first()['clsb_category']['id']).select()
    subjects = db(db.clsb_subject).select()
    payment = db(~db.clsb20_purchase_type.name.like("Subscriptions")).select()
    classes = db(db.clsb_class).select()
    form = FORM(
        DIV(
            TABLE(
                TR(
                    TD(
                        A(
                            DIV(
                                SPAN(_class="icon leftarrow icon-arrow-left"),
                                " Quản lý sách", _class="btn"
                            ),
                            _href=URL(user_signature=True)
                        ),
                    ),
                ),
                TR(
                    TD(
                        TABLE(
                            TR(
                                TD(LABEL("Tiêu đề sách: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_name="title", _value=data[0].product_title, _class="clsb_input_product",_style="width: 100%;", requires=IS_NOT_EMPTY()))
                            ),
                            TR(
                                TD(LABEL("Mô tả chi tiết: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(TEXTAREA(_name="content", _class="clsb_input_product"))
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
                                TD(LABEL("Thể loại: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    SELECT(*[OPTION(category_parent[i]['clsb_category']['category_name'], _value=str(category_parent[i]['clsb_category']['id'])) for i in range(len(category_parent))], _class="clsb_input_product", _id="category_parent"),
                                    # TABLE(
                                    #     TR(
                                    #         TD(
                                    #             SELECT(*[OPTION(category_parent[i]['clsb_category']['category_name'], _value=str(category_parent[i]['clsb_category']['id'])) for i in range(len(category_parent))], _class="clsb_input_product", _id="category_parent"),
                                    #             _style="padding: 0px;"
                                    #         ),
                                    #         TD(
                                    #             SELECT(*[OPTION(category[i].category_name, _value=str(category[i].id)) for i in range(len(category))], _class="clsb_input_product", _name="category",  _id="category"),
                                    #             _style="padding: 0px;"
                                    #         ),
                                    #     )
                                    # )
                                )
                            ),
                            TR(
                                TD(LABEL("Danh mục: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    SELECT(*[OPTION(category[i].category_name, _value=str(category[i].id)) for i in range(len(category))], _class="clsb_input_product", _name="category",  _id="category"),
                                )
                            ),
                            TR(
                                TD(LABEL("Môn học: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    SELECT(
                                        *[OPTION(subjects[i].subject_name,_value=subjects[i].id) for i in range(len(subjects))],
                                        _class="clsb_input_product", _style="min-width: 120px; width: 150px;",_name="subjects", _id="subject", requires=IS_NOT_EMPTY()
                                    ),
                                    # TABLE(
                                    #     TR(
                                    #         TD(
                                    #             SPAN("Môn học: ", _style="vertical-align: super;"),
                                    #             SELECT(
                                    #                 *[OPTION(subjects[i].subject_name,_value=subjects[i].id) for i in range(len(subjects))],
                                    #                 _class="clsb_input_product", _style="min-width: 120px; width: 150px;",_name="subjects", _id="subject", requires=IS_NOT_EMPTY()
                                    #             ), _style="padding: 0px;"
                                    #         ),
                                    #         TD(
                                    #             SPAN("Lớp: ", _style="vertical-align: super;"),
                                    #             SELECT(
                                    #                 *[OPTION(classes[i].class_name,_value=classes[i].id) for i in range(len(classes))],
                                    #                 _class="clsb_input_product", _style="min-width: 120px; width: 120px;",_name="classes", _id="classes", requires=IS_NOT_EMPTY()
                                    #             ), _style="padding: 0px;"
                                    #         )
                                    #     ),
                                    #     _style="width: 100%;"
                                    # )
                                )
                            ),
                            TR(
                                TD(LABEL("Tác giả: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_creator_list", _name="creator", _linkSearch=URL(a='cps',c='creators',f='search'), requires=IS_NOT_EMPTY()),
                                   SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchcreator()"),
                                   DIV("Các tác giả phân cách nhau bằng dấu ';'")),
                            ),
                            TR(
                                TD(LABEL("Nhà xuất bản: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_style="margin-top: 10px;",_class="clsb_input_product",_id="clsb_publisher_list", _name="publisher", _linkSearch=URL(a='cps',c='publishers',f='search'), requires=IS_NOT_EMPTY()),
                                   SPAN(XML("Tìm kiếm"),_class="btn",_onclick="javascript:searchpublisher()")),
                            ),
                            TR(
                                TD(LABEL("Sách liên quan: ", _class="clsb_label_product"), _class="rows-left"),
                                TD(
                                    TABLE(
                                        THEAD(
                                            TR(
                                                TH("ID",_style="background-color: #08c; color: #fff; width: 30%;"),
                                                TH("Tên sách",_style="background-color: #08c; color: #fff; width: 69%;")
                                            )
                                        ),
                                        _id="clsb_list_product_show",
                                        _style="margin-top: 0px; width: 100%;"
                                    ),
                                    INPUT(_name="title_relation",_class="clsb_input_product",_id="clsb_relation_product", _style="display: none;"),
                                    SPAN(INPUT(_style="margin-top: 10px; display: none;", _class="clsb_input_product", _id="clsb_list_product", _linkSearch=URL(a='cbs',c='products',f='search'))),
                                    SPAN(XML("<b>+</b> Thêm sách"),_class="btn",_onclick="javascript:searchrelation()"),
                                    )
                            ),
                            TR(
                                TD(LABEL("Năm xuất bản: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_class="clsb_input_product", _name="year_created"))
                            ),
                            TR(
                                TD(LABEL("Kích cỡ (cm): ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_class="clsb_input_product", _name="size_cover"), SPAN(" (rộng x dài)"))
                            ),
                            TR(
                                TD(LABEL("Số trang: ",_class="clsb_label_product"), _class="rows-left"),
                                TD(INPUT(_class="clsb_input_product", _name="num_page"), requires=IS_NOT_EMPTY())
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
                                            TD(
                                                SPAN("Ảnh minh họa khác(Tối đa 5 ảnh - kích cỡ < 1MB)"),
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
                                TD(LABEL("Phương thức thu tiền: ", _class="clsb_label_product", _style="font-weight: bold;"), _class="rows-left"),
                                TD(
                                    SELECT(*[OPTION(payment[i].description, _value=str(payment[i].name)) for i in range(len(payment))], _id="payment",_style="margin-top: 5px;", _class="clsb_input_product", _name="payment"),
                                    DIV(INPUT(_name="price", _placeholder="Giá tiền", _class="clsb_input_product", _value=0, _style="color: rgb(255, 112, 0); font-weight: bold;"), "VNĐ", _id="price"),
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
        ),
        _class="clsb_form_upload"
    )
    if form.accepts(request, session):
        try:
            class_id = db(db.clsb_class.class_code.like("None")).select()
            subject_class = None
            cat_id = request.vars.category
            if len(class_id) > 0:
                class_id = class_id.first().id
            else:
                class_id = db.clsb_class.insert(
                    class_name="Khác",
                    class_code="None",
                    class_order="9999",
                )
                class_id = class_id.id
            if request.vars.category == "0":
                cat_id = db(db.clsb_category.category_code.like("None")).select()
                if len(cat_id) <= 0:
                    cat_id = db.clsb_category.insert(
                        category_name="Danh mục khác",
                        category_code="None",
                        category_order="9999"
                    )
                    cat_id = db.clsb_category.insert(
                        category_name="Khác",
                        category_code="None",
                        category_order="9999",
                        category_parent=cat_id.id
                    )
                    cat_id = cat_id.id
                    device_shelf_check = db(db.clsb20_category_shelf_mapping.category_id == cat_id).select()
                    if len(device_shelf_check) <= 0:
                        db.clsb20_category_shelf_mapping.insert(
                            category_id=cat_id,
                            device_shelf_id=db(db.clsb_device_shelf.device_shelf_code.like("STK")).select().first()['id']
                        )
                else:
                    cat_id = cat_id.first().id

                subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == class_id)).select()
                if len(subject_class) > 0:
                    subject_class = subject_class.first()
                else:
                    subject_class = db.clsb_subject_class.insert(
                        subject_id=request.vars.subjects,
                        class_id=class_id
                    )
            else:
                map = db(db.clsb20_category_class_mapping.category_id == request.vars.category).select()
                if len(map) > 0:
                    class_id = map.first().class_id
                subject_class = db((db.clsb_subject_class.subject_id == request.vars.subjects) & (db.clsb_subject_class.class_id == class_id)).select()[0]
        except Exception as e:
            response.flash = "Có lỗi xảy ra: lựa chọn danh mục sách không tương ứng với môn học"
            return dict(form=form)
        code = data[0].product_code
        result_str = ""
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

        publisher = db(db.clsb_dic_publisher.publisher_name == request.vars.publisher).select()

        if len(publisher) <= 0:
            publisher = db.clsb_dic_publisher.insert(publisher_name = request.vars.publisher)
        else:
            publisher = publisher[0]

        device_shelf = db(db.clsb20_category_shelf_mapping.category_id == cat_id).select()[0]['device_shelf_id']

        newdata = db.clsb20_product_cp.insert(product_title=request.vars.title,
                                              product_code=code,
                                              product_description=request.vars.content,
                                              subject_class=subject_class.id,
                                              product_publisher=publisher.id,
                                              product_creator=creator.id,
                                              device_shelf_code=device_shelf,
                                              product_category=cat_id,
                                              product_price=request.vars.price)
        db(db.clsb20_product_from_editor.id == id).delete()

        if request.vars.title_relation != "":
            list = request.vars.title_relation.split(";")
            sum = 0
            for one in list:
                if (sum>0):
                    db.clsb20_product_relation_cp.insert(product_cp_id=newdata.id, relation_id=one)
                sum = sum+1

        if request.vars.year_created != "":
            metadata = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()
            if len(metadata) <= 0:
                db.clsb_dic_metadata.insert(metadata_name="pub_year", metadata_label="Năm xuất bản")
            metadata_id = db(db.clsb_dic_metadata.metadata_name.like("pub_year")).select()[0]['id']
            db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.year_created)

        if request.vars.size_cover != "":
            metadata = db(db.clsb_dic_metadata.metadata_name.like("format")).select()
            if len(metadata) <= 0:
                db.clsb_dic_metadata.insert(metadata_name="format", metadata_label="Kích cỡ")
            metadata_id = db(db.clsb_dic_metadata.metadata_name.like("format")).select()[0]['id']
            db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.size_cover)

        if request.vars.num_page != "":
            metadata = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()
            if len(metadata) <= 0:
                db.clsb_dic_metadata.insert(metadata_name="page_number", metadata_label="Số trang")
            metadata_id = db(db.clsb_dic_metadata.metadata_name.like("page_number")).select()[0]['id']
            db.clsb20_product_metadata_cp.insert(metadata_id=metadata_id, product_code=newdata['product_code'],metadata_value=request.vars.num_page)

        if request.vars.payment != "":
            if request.vars.payment.upper() == "SUBSCRIPTIONS":
                purchase_item = db(db.clsb20_purchase_item.id == request.vars.payment_more).select()[0].id
            else:
                purchase_id = db(db.clsb20_purchase_type.name.like(request.vars.payment)).select()[0].id
                purchase_item = db(db.clsb20_purchase_item.purchase_type == purchase_id).select()[0].id

            db.clsb20_product_purchase_item.insert(product_code=newdata.product_code, purchase_item=purchase_item)

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
                    db.clsb20_product_image.insert(type_id=type_image['id'], product_code=code, description=file.filename, image="clsb20_product_cp."+code+"."+scripts.computeMD5hash(file.filename)+"."+file.filename.split(".")[-1])
                except:
                    continue
        session.flash = 'Thành công'
        redirect(URL(a='cpa', c='products', f='index', user_signature=True))
    elif form.errors:
        response.flash = 'Thông tin không đúng quy định'
    else:
        response.flash = 'Hãy điền vào form dưới'
    return dict(form=form)


def remove_from_editor():
    id = request.args[2]
    data = db(db.clsb20_product_from_editor.id == id).delete()
    try:
        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code)
        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+data[0].product_code+"_Backup")
        session.flash = 'Xóa thành công'
    except Exception as e:
        response.flash = "Không tồn tại thư mục"
    redirect(URL("index", user_signature=True))

def create_product_from_file():
    import os
    upload_dir = "/home/CBSData/upload/"
    try:
        if request.vars and len(request.vars) > 0:
            print(request.vars)
            for pdf_file in request.vars.files:
                create_product_upload(pdf_file + ".pdf")
        list_file = list()
        for directory in os.listdir(upload_dir):
            if os.path.isdir(upload_dir + directory):
                dir = dict()
                dir['category'] = directory
                dir['files'] = list()
                for file_pdf in os.listdir(upload_dir + directory):
                    if file_pdf.endswith(".pdf"):
                        code = os.path.splitext(str(file_pdf))[0]
                        if not check_exist_code(code):
                            dir['files'].append(code)
                list_file.append(dir)
        return dict(list_file=list_file)
    except Exception as e:
        print(str(e) + " - on line "+str(sys.exc_traceback.tb_lineno))
        response.flash = "Xay ra loi: " + str(e)

def check_exist_code(code):
    check_product = db(db.clsb_product.product_code == code).select()
    check_cp = db(db.clsb20_product_cp.product_code == code).select()
    if len(check_product) == 0 and len(check_cp) == 0:
        return False
    return True

def create_product_upload(pdf_file):
    upload_dir = "/home/CBSData/upload/"
    metadata = read_metadata(upload_dir + pdf_file)
    number_page = '0'
    dir = os.path.splitext(pdf_file)[0]
    code = dir.split("/")[1]
    category_code = dir.split("/")[0]
    print(check_valid_code(code))
    if not check_valid_code(code):
        db.clsb30_log_upload.insert(product_code=code,
                                    product_category=category_code,
                                    upload_status='FAIL',
                                    description='Invalid product code')
        return
    print(code)
    print(category_code)
    try:
        if 'error' not in metadata:
            creator_list = re.split(r"[,;]", metadata['/Author'])
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

            #publisher = db(db.clsb_dic_publisher.publisher_name == metadata['/publisher']).select()
            #
            #if len(publisher) <= 0:
            #    publisher = db.clsb_dic_publisher.insert(publisher_name=metadata['/publisher'])
            #else:
            #    publisher = publisher[0]
            device_shelf = 31

            category_id = 87
            category = db(db.clsb_category.category_code == category_code).select()
            if len(category) > 0:
                category_id = category.first()['id']

            newdata = db.clsb20_product_cp.insert(product_title=metadata['/Title'],
                                                  product_code=code,
                                                  product_description=metadata['/Subject'],
                                                  subject_class=299,
                                                  product_publisher=13,
                                                  product_creator=creator.id,
                                                  device_shelf_code=device_shelf,
                                                  product_category=category_id,
                                                  product_price=0,
                                                  data_type='pdf')
        else:
            db.clsb30_log_upload.insert(product_code=code,
                                    product_category=category_code,
                                    upload_status='FAIL',
                                    description=metadata['error'])
            return

        print("code: " + code)
        create_dir(user_cp_path+"/upload/"+code+"/"+code)
        create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code)
        create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config")
        f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/.nomedia", "w+")
        print(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/.nomedia")
        f.flush()
        f.close()
        f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/book_config/config.xml", "w+")
        f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
                    '<configs>'
                        '<bookId>'+code+'</bookId>'
                        '<bookName></bookName>'
                        '<firstPageIndex>1</firstPageIndex>'
                        '<contentPageIndex>1</contentPageIndex>'
                        '<pageCountIndex>0</pageCountIndex>'
                        '<publisher></publisher>'
                        '<cover-normal>'
                            '<cover>cover.jpg</cover>'
                            '<cover-width>482</cover-width>'
                            '<cover-height>680</cover-height>'
                        '</cover-normal>'
                    '</configs>')
        f.flush()
        f.close()

        book_config_str = '{"id":"' + code + '","contentPageIndex":0,"pageCountIndex":0,"numberPages":0,"publisher":null,"bookName":"}'
        #shutil.copy(upload_dir + "cover.clsbi21", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi")
        shutil.copy(upload_dir + pdf_file, settings.home_dir+settings.cp_dir+user_cp_path+"/upload/" +code+"/"+code+"/"+code+"/"+code+".pdf")
        from pyPdf import PdfFileWriter, PdfFileReader
        inputpdf = PdfFileReader(open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/" +code+"/"+code+"/"+code+"/"+code+".pdf", "rb"))
        output = PdfFileWriter()
        output.addPage(inputpdf.getPage(0))
        with open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/first-page.pdf", "wb") as outputStream:
            output.write(outputStream)
        import PythonMagick
        img = PythonMagick.Image()
        img.density("100")
        img.read(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/first-page.pdf")
        img.write(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/cover.clsbi")
        os.remove(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/first-page.pdf")
        shutil.copy("/home/libs/zipfileforpdf.zip", settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+"/"+code+"/"+code+".zip")
        try:
            create_dir(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json")
            target = open_file(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json" + "/" + "bookconfig.txt" )
            target.write(book_config_str)
            target.close()

            target = open_file(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json" + "/" + "addtional.txt")
            target.write("{}")
            target.close()

            target = open_file(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json" + "/" + "clickable.txt")
            target.write("{}")
            target.close()


            target = open_file(user_cp_path+"/upload/"+code+"/"+code+"/"+code + "_json" + "/" + "metadata.txt")
            target.write("[]")
            target.close()

            z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code+".zip", "w")
            zipdir(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code, z)
            z.close()
        except Exception as e:
            print str(e)
            db.clsb30_log_upload.insert(product_code=code,
                                    product_category=category_code,
                                    upload_status='FAIL',
                                    description=str(e) +" - on line "+str(sys.exc_traceback.tb_lineno))
            return
        shutil.rmtree(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+code+"/"+code)
        os.remove(upload_dir + pdf_file)
        db.clsb30_log_upload.insert(product_code=code,
                                    product_category=category_code,
                                    upload_status='SUCCESS')
        return
    except Exception as err:
        print(str(err) +" - on line "+str(sys.exc_traceback.tb_lineno))
        db.clsb30_log_upload.insert(product_code=code,
                                    product_category=category_code,
                                    upload_status='FAIL',
                                    description=str(err) +" - on line "+str(sys.exc_traceback.tb_lineno))
        return


def read_metadata(file):
    try:
        from pyPdf import PdfFileReader
        print(file)
        pdf_toread = PdfFileReader(open(file, "rb"))
        pdf_info = pdf_toread.getDocumentInfo()
        print(pdf_info)
        return pdf_info
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def check_valid_code(code):
    try:
        if re.match("^[A-Za-z0-9]*$", code):
            return True
        return False
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def resize_thumb(path):
    try:
        import os
        import PIL
        from PIL import Image
        basewidth = 200
        print(path)
        thumb = Image.open(path + 'cover.clsbi')
        wper = (basewidth / float(thumb.size[0]))
        hsize = int(float(thumb.size[1]) * float(wper))
        new_thumb = thumb.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        new_thumb.save(path + 'thumb.png')
        return "success"
    except Exception as err:
        print str(err) + path
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def overview():
    try:
        products = list()
        select_product = db(((db.clsb20_product_cp.created_by == db.auth_user.created_by) & (db.auth_user.id == auth.user.id)) | (db.clsb20_product_cp.created_by == auth.user.id)).select(db.clsb20_product_cp.ALL)
        for p in select_product:
            temp = dict()
            temp['id'] = p[db.clsb20_product_cp.id]
            temp['product_code'] = p[db.clsb20_product_cp.product_code]
            temp['product_title'] = p[db.clsb20_product_cp.product_title]
            temp['product_price'] = p[db.clsb20_product_cp.product_price]
            temp['product_status'] = p[db.clsb20_product_cp.product_status]
            temp['created_on'] = p[db.clsb20_product_cp.created_on]
            products.append(temp)
        return dict(products=products)
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))