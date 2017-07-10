# -*- coding: utf-8 -*-
import zipfile
import fs.path
import time
import shutil, errno
import subprocess

import os
import re
from PIL import Image
from time import gmtime, strftime
import usercp

THUMB_X = 200
THUMB_Y = 286

STATIC_FILE = "/home/www-data/web2py/applications/cbw/static/covers/"

def makethumb(product_code):#product_code, example: VHNT01 
#    product_code = request.args(0) 
    size = (THUMB_X, THUMB_Y)

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


from pyPdf import PdfFileReader
import sys


def isEncrypted(path):
#     return PdfFileReader(file(path, 'rb')).isEncrypted
    return PdfFileReader(osFileServer.open(path, 'rb')).isEncrypted


def validate_data(code, product_type):
    have_pdf = False
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
        z = zipfile.ZipFile(osFileServer.open(zip_file, 'rb'))

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

    if osFileServer:
        osFileServer.close()
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


def extract_product_data(code, product_type, product_title):
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
        osFileServer.makedir(code, True, True)
        if product_type == 'Book' or product_type == 'Application':
            z = zipfile.ZipFile(osFileServer.open(zip_file, 'rb'))
            zout = zipfile.ZipFile(osFileServer.open(zip_path, 'wb+'), mode="w")
            for name in z.namelist():
                if name.endswith('.E.pdf'):
                    osFileServer.setcontents(fs.path.pathjoin(code, fs.path.basename(name)), z.read(name))
                    pdf_path = fs.path.pathjoin(code, code + ".E.pdf")
                    if not isEncrypted(pdf_path):
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
        else:
            osFileServer.move(zip_file, zip_path, True)
    except:
        if z:
            z.close()
        if zout:
            zout.close()
        import traceback
        import StringIO

        output_err = StringIO.StringIO()
        traceback.print_exc(file=output_err)
        result = output_err.getvalue()
    if osFileServer:
        osFileServer.close()
    return result


def delete(ids, table):
    try:
        to_delete = db(db[table].id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/product/delete(ids, table) " + str(e)


@auth.requires_login()
def category():
    return dict(categories=get_list_category())


@auth.requires_login()
def index():
    current_table = "clsb_product"
    if 'category' in request.vars:
        session.catid = int(request.vars['category'])
    elif 'product_category' in request.vars:
        session.catid = int(request.vars['product_category'])
    else:
        session.catid = 0
    print("cat_id: " + str(session.catid))

    if session.product_id_list is None:
        session.product_id_list =''

    # To detect what page user is on, then delete into a correct table
    if request.url.find('/clsb_product/clsb_attention.') >= 0:
        current_table = "clsb_attention"
    if request.url.find('/clsb_product/clsb_product_metadata.') >= 0:
        current_table = "clsb_product_metadata"
    if request.url.find('/clsb_product/clsb_download_archieve.') >= 0:
        current_table = "clsb_download_archieve"
    if request.url.find('/clsb_product/clsb_home_topic_item.') >= 0:
        current_table = "clsb_home_topic_item"
    if request.url.find('/clsb_product/clsb_product_relation.') >= 0:
        current_table = "clsb_product_relation"
    db.clsb_product.product_code.readable = True

    #if current_table == "clsb_product":
    #    selectable = (lambda ids: delete(ids, current_table)) if auth.has_permission('Delete', "clsb_category",
    #                                                                                 session.catid) else None
    #else:
    selectable = (lambda ids: delete(ids, current_table))

    is_root = db(db[auth.settings.table_user_name].id == auth.user.id)(
        db[auth.settings.table_user_name].is_root == 'T').count()
    #if is_root == 0:
    #    db.clsb_product.product_category.writable = False
    #else:
    db.clsb_product.product_category.writable = True
    db.clsb_product.product_category.default = session.catid
    print(session.catid)
    if request.url.find('clsb_product/new/clsb_product') >= 0:
        db.clsb_product.subject_class.writable = False
        db.clsb_product.subject_class.readable = False
        max_id = db(db.clsb_subject_class).select(db.clsb_subject_class.id.max()).first()[
            db.clsb_subject_class.id.max()]
        db.clsb_product.subject_class.default = max_id

        zip_list = osFileServer.listdir(wildcard="*.[Zz][Ii][Pp]", files_only=True)
        zip_list.sort()
        ignore_items = -1
        for index in range(0, len(zip_list)):
            if zip_list[index].find('cbdriver') > -1:
                ignore_items = index
            else:
                zip_list[index] = fs.path.splitext(zip_list[index])[0]
        if ignore_items != -1:
            zip_list.pop(ignore_items)

        db.clsb_product.product_code.requires = IS_IN_SET(zip_list, zero='Choose one below:')
    if request.url.find('clsb_product/edit/clsb_product') >= 0:
        db.clsb_product.product_code.writable = True
        db.clsb_product.product_code.readable = True

        db.clsb_product.subject_class.writable = False
        db.clsb_product.subject_class.readable = False

    #in index page, to group all linked_tables into the selectbox and display only the fields listed
    if len(request.args) <= 2 or request.url.find('clsb_product/view/clsb_product') >= 0:
        fields = (db.clsb_product.id,
                  db.clsb_product.product_category,
                  db.clsb_product.product_code,
                  # db.clsb_product.product_publisher,
                  # db.clsb_product.product_creator,
                  db.clsb_product.product_title,
                  db.clsb_product.device_shelf_code,
                  db.clsb_product.product_price,
                  db.clsb_product.created_on,)
        links = [{'header': 'Linked Tables', 'body': lambda row: SELECT('Choose linked table', "Attentions",
                                                                        "Product metadata", "Download Archieves",
                                                                        "Home Topic Items", "Product Relations",
                                                                        _id="selectbox" + str(row.id),
                                                                        value='Choose linked table',
                                                                        _class="generic-widget",
                                                                        _onchange="changeFunc(" + str(row.id) + ");")},
                 {'header': 'Thumb', 'body': lambda row: A('Update', _href=URL(f='update_thumb', args=row.id))},
                 {'header': 'Size', 'body': lambda row: A('View', _href="javascript:caculateSize(" + str(row.id) + ");")},
                 {'header': 'Relation', 'body': lambda row: A('Insert', _href=URL(f='insert_relation', args=row.id))}]
    else:
        links = None
        if request.url.find('clsb_product/edit/clsb_product') >= 0:
            pid = request.args[len(request.args) - 1]
            product = db(db.clsb_product.id == pid).select(db.clsb_product.product_code).first()
            if not product is None:
                links = [{'header': 'Thumbnail',
                          'body': lambda row: DIV(IMG(_src=URL('cbs', 'download', 'thumb', args=product.product_code)),
                                                  A('Update Thumbnail', _href=URL(f='update_thumb', args=row.id)))}]
        fields = None

    form = smartgrid(db.clsb_product, fields=fields,
                     showbuttontext=False,
                     oncreate=product_on_create,
                     onupdate=product_on_update,
                     ondelete=product_on_delete,
                     onvalidation=product_on_validation,
                     selectable=selectable,
                     linked_tables=[''],
                     links=links)

    form[1].insert(-1, A('Send gcm', _href=URL('cba', 'gcm', 'send1')))
    if len(request.args) > 3:
        form[1].insert(-1, A("Send apns", _href="/cba/apns/send/" + request.args[3]))

    # If there is the update-form
    zip_product_code = None
    if request.url.find('clsb_product/edit/clsb_product') >= 0:

        # Verify if there is a new zip file to update.
        zip_list = osFileServer.listdir(wildcard='*.[Zz][Ii][Pp]', files_only=True)
        product_select = db(db.clsb_product.id == request.args(3)).select().as_list()[0]
        product_code = product_select['product_code']
        product_show_on = product_select['show_on'].split('/')
        product_show_all = settings.default_show.split('/')

        # PhuongNH: check product_code already in clsb20_product_cp
        check_cp_product = db(db.clsb20_product_cp.product_code == product_code).select().as_list()
        form[2].insert(-1, TR( TD(LABEL('Send gcm:', _id='send_gcm', _name='send_gcm')), TD(INPUT(_type="checkbox", _name="gcm_check", _id="gcm_check",  _value="gcm"))))
        dict_show = dict()
        dict_show['ANDROID_APP'] = "Classbook Android App"
        dict_show['IOS_APP'] = "Classbook IOS App"
        dict_show['CBM'] = "Trang cbm"
        dict_show['STORE_WEB'] = "Trang web classbook.vn/store"
        dict_show['STORE_APP'] = "App Classbook Store"
        for show_on in product_show_all:
            form[2].insert(0, DIV(INPUT(_type="checkbox", _name=show_on, _id=show_on,  _value=show_on, _checked=True if show_on in product_show_on else False), LABEL(dict_show[show_on], _style="margin-left: 30px; margin-top: -19px"), _style="margin-left: 40px"))
        form[2].insert(0,LABEL("Cho phép hiển thị trên: "))
        if len(check_cp_product) > 0:
            cpid = check_cp_product[0]['created_by']
            cpinfo = db(db.auth_user.id == cpid).select()
            if len(cpinfo) > 0:
                form[2].insert(-1, TR(TD(LABEL('CP')), TD(LABEL(cpinfo[0]['email']))))
        if len(check_cp_product) <= 0:

            old_zip_product_code = None
            product_files = osFileServer.listdir(path='./' + product_code, wildcard=product_code + ".[Zz][Ii][Pp]",
                                                 files_only=True)
            if len(product_files) > 0:
                old_zip_product_code = product_files[0]

            for name in zip_list:
                if re.match(product_code + r'.[Zz][Ii][Pp]', name, 0):
                    zip_product_code = name
                    #                old_zip_product_code = name
                    #             else:
                    #                 print 'KO'
                    #             if name.find(product_code + ".") >= 0:
                    #                 zip_product_code = product_code + '.zip'
                    #                 old_zip_product_code = product_code + '.zip'

            if zip_product_code and old_zip_product_code:
                path = settings.home_dir + product_code
                old_zip_time = time.ctime(os.path.getmtime(os.path.join(path, old_zip_product_code)))
                new_zip_time = time.ctime(os.path.getmtime(os.path.join(settings.home_dir, zip_product_code)))
                # Create a new element to insert into the form
                table = form.element('table')

                old_zip_line = TD("Last modified on " + old_zip_time, _class="w2p_fw")
                table[8].insert(2, old_zip_line)

                my_extra_select = SELECT('Choose file to update', product_code, value='Choose file to update',
                                         _id='clsb_product_new_zip_file', _name='new_zip_file', _class="generic-widget")
                my_extra_input = INPUT(_id='update_zip_file', _type='checkbox')
                my_extra_label = LABEL(B('Update product zip file?'), _for="clsb_product_new_product_code",
                                       _id="clsb_product_new_product_code__label")

                new_zip_line = TR(TD(my_extra_label, _class="w2p_f1"),
                                  TD(my_extra_select, _class="w2p_fw"),
                                  TD("Last modified on " + new_zip_time, _class="w2p_fw"),
                                  _id="clsb_product_new_product_code__row")

                table[9].insert(0, new_zip_line)

            else:
                print 'error: ' + product_code + ' file zip do not exist.'

    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
            "return confirm('" + CONFIRM_DELETE + "');"

    if request.url.find('clsb_product_metadata.product_id') >= 0:
        # check product_metadata, if user selects 'class' then we show the class select box required
        metadata_id = db(db.clsb_dic_metadata.metadata_name == "class").select(db.clsb_dic_metadata.ALL).as_list()

        if metadata_id:
            metadata_id = metadata_id[0]['id']

        # make the new metadata_value line (select box of class)
        classes = db().select(db.clsb_class.class_code, db.clsb_class.class_name)

        label = LABEL('Metadata Value:', _for="new_clsb_product_metadata_metadata_value",
                      _id="new_clsb_product_metadata_metadata_value__label")

        select = SELECT(_name='new_metadata_value',
                        *[OPTION(classes[i].class_name, _value=str(classes[i].class_code)) for i in
                          range(len(classes))])
        new_metadata_value_line = TR(TD(label, _class="w2p_f1"),
                                     TD(select, _class="w2p_fw"),
                                     _id="new_clsb_product_metadata_metadata_value__row")
        # and insert it to the form's table
        table = form.element('table')
        if metadata_id and form.element('tr', _id='clsb_product_metadata_metadata_id__row'):
            table[2].insert(2, new_metadata_value_line)

            # if Metadata 'class' is selected
            if form.element('option', _selected='selected', _value=str(metadata_id)):
                # if there has the metadata_value line (textarea)
                if form.element('tr', _id='clsb_product_metadata_metadata_value__row'):
                    # make its style to display:none
                    form.element('tr', _id='clsb_product_metadata_metadata_value__row')['_style'] = "display: none;"
            # else, Metadata 'class' isn't selected
            else:
                # if there has the new_metadata_value line (select box of class)
                if form.element('tr', _id='new_clsb_product_metadata_metadata_value__row'):
                    # make its style to display:none
                    form.element('tr', _id='new_clsb_product_metadata_metadata_value__row')['_style'] = "display: none;"

            # set onchange to the select box clsb_product_metadata_metadata_id
            if form.element('select', _id='clsb_product_metadata_metadata_id'):
                form.element('select', _id='clsb_product_metadata_metadata_id')[
                    '_onchange'] = "metadata_id_onchange(" + str(metadata_id) + ");"
            else:
                print "KO2"

    if request.url.find('clsb_product/new/clsb_product') >= 0 or request.url.find(
            'clsb_product/edit/clsb_product') >= 0:

        prod_subject_id = None
        prod_class_id = None

        subject = db().select(db.clsb_subject.ALL)
        classes = db().select(db.clsb_class.ALL)
        session.cat_id = 0
        if request.url.find('clsb_product/edit/clsb_product') >= 0:
            product_id = request.args(3)
            session.cat_id = db(db.clsb_product.id == product_id).select().first()['product_category']
            prod_subj_class = db(db.clsb_product.id == product_id).select(db.clsb_product.subject_class).as_list()

            if prod_subj_class and prod_subj_class[0]['subject_class']:
                prod_subj_class = prod_subj_class[0]['subject_class']

                # find current product's subject
                prod_subject_id = db(db.clsb_subject_class.id == prod_subj_class) \
                        (db.clsb_subject.id == db.clsb_subject_class.subject_id).select(db.clsb_subject.id)
                prod_subject_id = prod_subject_id[0]['id']

                # find current product's class
                prod_class_id = db(db.clsb_subject_class.id == prod_subj_class) \
                        (db.clsb_class.id == db.clsb_subject_class.class_id).select(db.clsb_class.id)
                prod_class_id = prod_class_id[0]['id']

        slabel = LABEL('Subject:', _for="clsb_product_subject_name", _id="clsb_product_subject_name__label")
        sselect = SELECT(_name='product_subject_name', _id="product_subject_name", value=prod_subject_id,
                         *[OPTION(subject[i].subject_name, _value=str(subject[i].id), _id=str(subject[i].id)) for i in
                           range(len(subject))]
            , _onchange="subject_name_onchange()")

        clabel = LABEL('Class:', _for="clsb_product_class_name", _id="clsb_product_class_name__label")
        cselect = SELECT(_name='product_class_name', _id="product_class_name", value=prod_class_id,
                         *[OPTION(classes[i].class_name, _value=str(classes[i].id), _id=str(classes[i].id)) for i in
                           range(len(classes))])

        product_subject_name_line = TR(TD(slabel, _class="w2p_f1"),
                                       TD(sselect, _class="w2p_fw"), TD(clabel, _class="w2p_f1"),
                                       TD(cselect, _class="w2p_fw"),
                                       _id="clsb_product_subject_name__row")
        # and insert it to the form's table
        table = form.element('table')
        if form.element('tr', _id='clsb_product_product_publisher__row'):
        #             print form.element('tr', _id='clsb_product_product_publisher__row')
            table[6].insert(0, product_subject_name_line)
            #             if form.element('select', _id='product_subject_name'):# = "subject_name_onchange("+ str(metadata_id) +");"
            #                 print 'OK'
            #                 print form.element('select', _id='product_subject_name')
            #                 print form.element('select', _id='product_subject_name')[1]['_value']
            #             else:
            #                 print 'KO'

    query = db(db.clsb_category.id == db.auth_permission.record_id)
    query = query(db.auth_permission.name == "List")
    groups = db(db.auth_membership.user_id == auth.user.id).select(db.auth_membership.group_id, distinct=True)
    for group in groups:
        query = query(db.auth_permission.group_id == group.group_id)
    categories = db(db.clsb_category.id >= 0).select(db.clsb_category.id, db.clsb_category.category_name, distinct=True).as_list()
    for index in range(len(categories)):
        categories.extend(db(db.clsb_category.category_parent == categories[index]['id']).select(db.clsb_category.id,
                                                                                                 db.clsb_category.category_name).as_list())
    #get category_tree
    mcategories = []
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
        mcategories.append(temp)
    expands=[]
    for cate in mcategories:
        get_expand_cate(expands, cate)
    return dict(form=form, categories=get_list_category(), zip_product_code=zip_product_code,
                mcategories=mcategories, expands=expands)

def get_expand_cate(expands, cate):
    if not session.cat_id:
        session.cat_id = 0
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

def product_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    exercise_name = form.vars.product_code
    pLinkDownload = None
    # print exercise_name
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')
    db.clsb30_update_product_log.insert(record_id=record_id, table_name=str(table), update_action="CREATE", update_status="INIT")
    if request.url.find('clsb_product/new/clsb_product') >= 0:
    #         extract_product_data(form.vars.product_code)
        pCover = URL(a='cbs', c='download', f='cover',
                     scheme=True, host=True, args=form.vars.product_code)
        pData = URL(a='cbs', c='download', f='data',
                    scheme=True, host=True, args=form.vars.product_code)
        pPDF = URL(a='cbs', c='download', f='product',
                   scheme=True, host=True, args=(form.vars.product_code))
        pLinkDownload = pPDF
        db(db.clsb_product.id == form.vars.id).update(product_cover=pCover, product_data=pData, product_pdf=pPDF)

        #-----------------
        # PhuongNH
        #insert product metadata value version = created date
        #-----------------

        # get current date
        currentDate = strftime("%Y%m%d", gmtime())
        # check metadata version exits
        metadata = db(db.clsb_dic_metadata.metadata_name == 'version').select(db.clsb_dic_metadata.ALL).as_list()
        if metadata:
            metadataId = metadata[0]['id']
            db.clsb_product_metadata.insert(product_id=record_id, \
                                            metadata_id=metadataId, \
                                            metadata_value=str(currentDate))
        else:
            metadata_name_value = 'version'
            db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, \
                                        metadata_label=metadata_name_value, \
                                        metadata_description=metadata_name_value)
            metadata = db(db.clsb_dic_metadata.metadata_name == 'version').select(db.clsb_dic_metadata.ALL).as_list()
            metadataId = metadata[0]['id']
            db.clsb_product_metadata.insert(product_id=record_id, \
                                            metadata_id=metadataId, \
                                            metadata_value=str(currentDate))
        try:
            subprocess.call(["python", "/home/pylibs/create_preview.py",
                             settings.home_dir + form.vars.product_code + "/" + form.vars.product_code + ".E.pdf",
                             settings.home_dir + form.vars.product_code + "_PREVIEW/"])
            directory = STATIC_FILE + form.vars.product_code
            if not os.path.exists(directory):
                os.makedirs(directory)
            copyanything(settings.home_dir + form.vars.product_code+"/cover.clsbi", STATIC_FILE + form.vars.product_code + "/cover.clsbi")
            copyanything(settings.home_dir + form.vars.product_code+"/thumb.png", STATIC_FILE + form.vars.product_code + "/thumb.png")
        except Exception as err:
            pass
    if request.url.find(
            'clsb_product_metadata.product_id') >= 0 and request.vars.new_metadata_value and request.vars.metadata_value:
        metadata_id = db(db.clsb_dic_metadata.metadata_name == "class").select(db.clsb_dic_metadata.ALL).as_list()
        if metadata_id:
            metadata_id = metadata_id[0]['id']
        if metadata_id and int(request.vars.metadata_id) == int(metadata_id):
            request.vars.pop('metadata_value')
            d = dict(metadata_value=request.vars.pop('new_metadata_value'))
            request.vars.update(d)
            try:
                # web2py log something then if we do just an insert the new value, there will have 2 records. Then we need to fake: let web2py insert first and update the last insert with our new value. 
                max_id = db(db.clsb_product_metadata).select(db.clsb_product_metadata.id.max()).first()[
                    db.clsb_product_metadata.id.max()]
                oldval = \
                    db(db.clsb_product_metadata.id == max_id).select(db.clsb_product_metadata.metadata_value).first()[
                        'metadata_value']
                if (oldval == '<br>'):
                    db(db.clsb_product_metadata._id == max_id).update(metadata_value=request.vars.metadata_value)
            except Exception as e:
                print 'loi khon glien qan ' + str(e)

    if request.url.find('clsb_product/new/clsb_product') >= 0 and request.vars['product_class_name'] and request.vars[
        'product_subject_name']:
        try:
            code = form.vars.product_code
            if session.catid == 0:
                product_type = db(db.clsb_category.id > 0)
            else:
                product_type = db(db.clsb_category.id == session.catid)
            product_type = product_type(db.clsb_product_type.id == db.clsb_category.category_type)
            product_type = product_type.select(db.clsb_product_type.type_name).first()
            product_type = product_type.type_name
            if product_type == 'Application':
                import subprocess

                sh_location = '/home/CBSData/SignUpdate/convert2ota.sh'
                proc = subprocess.Popen('sh %s %s %s "%s" %s %s "%s" %s' % (sh_location,
                                                                            '%s%s/%s.zip' % (
                                                                            settings.home_dir, code, code),
                                                                            code, '127.0.0.1:3306', 'dev',
                                                                            settings.database_uri.split('/')[-1],
                                                                            'DEV2013!@#', '%sOTAUPDATE/%s.zip' % (
                settings.home_dir, code)),
                                        shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                proc.wait()
                std_err = proc.stderr.readlines()
                if len(std_err) > 0:
                    print "ERROR ON OTA: " + str(std_err)
                    raise RuntimeError(str(std_err))
        except:
            import traceback
            import StringIO

            output_err = StringIO.StringIO()
            traceback.print_exc(file=output_err)
            session.flash = output_err.getvalue()

        subjclass = db(db.clsb_subject_class.class_id == request.vars['product_class_name']) \
                (db.clsb_subject_class.subject_id == request.vars['product_subject_name']).select(
            db.clsb_subject_class.id).as_list()
        if subjclass:
            subjclass = subjclass[0]['id']
        else:
            subjclass = db.clsb_subject_class.insert(subject_id=request.vars['product_subject_name'],
                                                     class_id=request.vars['product_class_name'])
            #print request.vars
        #         request.vars.pop('subject_class')
        #         d = dict(subject_class = subjclass)
        #         request.vars.update(d)
        try:
            # web2py log something then if we do just an insert the new value, there will have 2 records.
            #Then we need to fake: let web2py insert first and update the last insert with our new value.
            max_id = db(db.clsb_product).select(db.clsb_product.id.max()).first()[db.clsb_product.id.max()]
            db(db.clsb_product._id == max_id).update(subject_class=subjclass)
        except Exception as e:
            print 'Loi khong lien quan ' + str(e)
            # check if product has just update is a exercise
        # check product code : example exerGK08ENG008, 
        #   => perfix : exer, GK08ENG008 is a product_code already exits =>  product is a exercise 
        try:
            # get product without prefix
            exercise_code = exercise_name[4:]

            product_exits = db(db.clsb_product.product_code == exercise_code).select(db.clsb_product.id)

            # print product_exits
            if product_exits is not None:
                # get metadata_id has name = 'product_exercise'
                exercise_metadata = db(db.clsb_dic_metadata.metadata_name == 'product_exercise').select(
                    db.clsb_dic_metadata.id)
                # print 'id = ' + str(exercise_metadata)
                if exercise_metadata is not None:

                    try:
                        db.clsb_product_metadata.insert(product_id=product_exits[0], \
                                                        metadata_id=exercise_metadata[0], \
                                                        metadata_value=str(pLinkDownload))
                    #                         db.clsb_product_metadata.update_or_insert(product_id = product_exits[0], metadata_id = exercise_metadata[0], metadata_value = str(pLinkDownload))

                    except Exception as ex1:
                        print 'loi insert ' + str(ex1)
        except Exception as e:
            print 'Loi khong lien quan ' + str(e)


def product_on_update(form):
    try:
        # print(request.args)
        # print(request.vars)
        table = request.args[-2]
        record_id = request.args[-1]
        # print("update " + table + ": " + record_id)
        product_info = db(db.clsb_product.id == record_id).select(db.clsb_product.product_code, db.clsb_product.product_title, db.clsb_product.id).first()
        auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')
        db.clsb30_update_product_log.insert(record_id=record_id, table_name=str(table), update_action="UPDATE", update_status="INIT")
        #----------------
        # PhuongNH
        # update version = date modify (current date)
        #----------------
        if request.url.find('clsb_product/edit/clsb_product') >= 0:
        # get current date
            currentDate = strftime("%Y%m%d", gmtime())
            metadata = db(db.clsb_dic_metadata.metadata_name == "version").select(db.clsb_dic_metadata.ALL).as_list()
            # if metadata version already exits
            if metadata:
                metadata_id = metadata[0]['id']
                product_metadata = db(db.clsb_product_metadata.product_id == record_id)(
                    db.clsb_product_metadata.metadata_id == metadata_id).select().first()
                if product_metadata:
                    product_metadata.update_record(metadata_value=str(currentDate))
                else:
                    db.clsb_product_metadata.insert(product_id=record_id, metadata_id=metadata_id,
                                                    metadata_value=str(currentDate))
                    #         else :

        if request.url.find('clsb_product_metadata.product_id') >= 0 \
            and request.vars.new_metadata_value and request.vars.metadata_value:
            metadata_id = db(db.clsb_dic_metadata.metadata_name == "class").select(db.clsb_dic_metadata.ALL).as_list()
            if metadata_id:
                metadata_id = metadata_id[0]['id']

            if metadata_id and int(request.vars.metadata_id) == int(metadata_id):
                request.vars.pop('metadata_value')
                d = dict(metadata_value=request.vars.pop('new_metadata_value'))
                request.vars.update(d)
                try:
                    db[table].update_or_insert(db[table]._id == request.vars.id, metadata_value=request.vars.metadata_value)
                except Exception as e:
                    print e

        if request.url.find('clsb_product/edit/clsb_product') >= 0 and request.vars['product_class_name'] and request.vars[
            'product_subject_name']:
            subjclass = db(db.clsb_subject_class.class_id == request.vars['product_class_name']) \
                    (db.clsb_subject_class.subject_id == request.vars['product_subject_name']).select(
                db.clsb_subject_class.id).as_list()
            if subjclass:
                subjclass = subjclass[0]['id']
            else:
                subjclass = db.clsb_subject_class.insert(subject_id=request.vars['product_subject_name'],
                                                         class_id=request.vars['product_class_name'])
                #         print request.vars
            #         request.vars.pop('subject_class')
            #         d = dict(subject_class = subjclass)
            #         request.vars.update(d)
            try:
                db.clsb_product.update_or_insert(db.clsb_product._id == request.vars.id, subject_class=subjclass)
            except Exception as e:
                print e
            if request.vars.new_zip_file is not None and request.vars.new_zip_file != "Choose file to update":
                try:
                    code = db.clsb_product(id=form.vars.id).product_code
                    if session.catid == 0:
                        product_type = db(db.clsb_category.id > 0)
                    else:
                        product_type = db(db.clsb_category.id == session.catid)
                    product_type = product_type(db.clsb_product_type.id == db.clsb_category.category_type)
                    product_type = product_type.select(db.clsb_product_type.type_name).first()
                    product_type = product_type.type_name
                    if product_type == 'Application':
                        import subprocess

                        sh_location = '/home/CBSData/SignUpdate/convert2ota.sh'
                        proc = subprocess.Popen('sh %s %s %s "%s" %s %s "%s" %s' % (sh_location,
                                                                                    '%s%s/%s.zip' % (
                                                                                    settings.home_dir, code, code),
                                                                                    code, '127.0.0.1:3306', 'dev',
                                                                                    settings.database_uri.split('/')[-1],
                                                                                    'DEV2013!@#', '%sOTAUPDATE/%s.zip' % (
                        settings.home_dir, code)),
                                                shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                        proc.wait()
                        std_err = proc.stderr.readlines()
                        if len(std_err) > 0:
                            print "ERROR ON OTA: " + str(std_err)
                            raise RuntimeError(str(std_err))
                except:
                    import traceback
                    import StringIO

                    output_err = StringIO.StringIO()
                    traceback.print_exc(file=output_err)
                    session.flash = output_err.getvalue()

            if 'gcm_check' in request.vars:
                session.product_id_list = ''
                session.product_id_list += str(product_info['id'])
                session.product_id_list += ','
                redirect(URL('cba', 'gcm', 'send1'))
    except Exception as e:
        print str(e)


def product_on_delete(table, record_id):
    product = db(db.clsb_product.id == record_id).select()
    title = ""
    if len(product) > 0:
        title = product.first()['product_title']
    auth.log_event(description='Delete id ' + str(record_id) + " " + title + ' in ' + str(table), origin='data')


def product_on_validation(form):
    if request.url.find('clsb_product/new/clsb_product') >= 0:
        if search_zip_file(form.vars.product_code) is None:
            form.errors.product_code = 'Error: product zip file isn\'t exist on the server.'

        #         print 'Log category_type'
        if session.catid == 0:
            category_type = db(db.clsb_category.id > 0).select(db.clsb_category.category_type).as_list()
        else:
            category_type = db(db.clsb_category.id == session.catid).select(db.clsb_category.category_type).as_list()
        category_type = category_type[0]['category_type']
        #             print category_type
        #             print 'Log type_name'
        product_type = db(db.clsb_product_type.id == category_type).select(db.clsb_product_type.type_name).as_list()
        product_type = product_type[0]['type_name']

        #         if not extract_product_data(form.vars.product_code, product_type):
        #             form.errors.product_code = 'Error: product zip file isn\'t valid.'
        result = extract_product_data(form.vars.product_code, product_type, form.vars.product_title)
        if "OK" not in result:
            form.errors.product_code = result

        res = db(db.clsb_product.product_code == form.vars.product_code).select(db.clsb_product.product_code)
        if res:
            form.errors.product_code = 'Product code already in database.'
    if request.url.find('clsb_product/edit/clsb_product') >= 0:
    #       print 'Log category_type'
        if session.catid == 0:
            category_type = db(db.clsb_category.id > 0).select(db.clsb_category.category_type).as_list()
        else:
            category_type = db(db.clsb_category.id == session.catid).select(db.clsb_category.category_type).as_list()
        category_type = category_type[0]['category_type']
        #             print category_type
        #             print 'Log type_name'
        product_type = db(db.clsb_product_type.id == category_type).select(db.clsb_product_type.type_name).as_list()
        product_type = product_type[0]['type_name']

        if request.vars.new_zip_file != None and request.vars.new_zip_file != "Choose file to update":
        #             if not extract_product_data(request.vars.new_zip_file, product_type):
        #                    form.errors.product_status = 'Error: NEW product zip file isn\'t valid.'
            result = extract_product_data(request.vars.new_zip_file, product_type, form.vars.product_title)
            if "OK" not in result:
                form.errors.product_code = 'Error in NEW product zip file: ' + str(result)
                response.flash = 'Error in NEW product zip file: ' + str(result)
                #             extract_product_data(request.vars.new_zip_file, product_type)
                #             print request.vars.new_zip_file + " onsubmit"

        else:
            print 'zip file isn\'t update.'

#     if request.url.find('clsb_product_metadata.product_id') >= 0 and request.vars.new_metadata_value and request.vars.metadata_value:
#         print  request.vars
#         print  request.vars.metadata_value
#         print request.vars.new_metadata_value
#         request.vars.pop('metadata_value')
#         d = dict(metadata_value=request.vars.pop('new_metadata_value'))
#         request.vars.update(d)
#         print "-----------"
#         thisid = request.vars.id
#         print thisid
#         thisval = request.vars.metadata_value
#         print thisval
#         print table
#         try:
# #             db[table].update_or_insert(db[table]._id == request.vars.id, metadata_value=request.vars.metadata_value)
#             print db(db[table].id == thisid).update(metadata_value = str(thisval))
# #             db[table].update_or_insert(request.vars)
#         except Exception as e:
#             print e


# def set_device_shelf():
#     
#     try:
#         # update(clsb_product.device_shelf_code = clsb_product.product_category (category_code))
# #         rows = db().select(db.clsb_product.product_code)
#         rows = db(db.clsb_product.product_category == db.clsb_category.id).select(db.clsb_product.product_code,
#                                                                                  db.clsb_category.category_code,
#                                                                                  db.clsb_product.device_shelf_code)
# 
#         for row in rows:
# #             category_code = db()
#             print row['clsb_category']['category_code']
#             device_shelf = db(db.clsb_device_shelf.device_shelf_code == row['clsb_category']['category_code']).select(db.clsb_device_shelf.id,
#                                                                                                                    db.clsb_device_shelf.device_shelf_code).as_list()
#             print device_shelf[0]['device_shelf_code']
#             print device_shelf[0]['id']
#             db(db.clsb_product.product_code == row['clsb_product']['product_code']).update(device_shelf_code = device_shelf[0]['id'])
#             print row['clsb_product']['product_code']
#             s = db(db.clsb_product.product_code == row['clsb_product']['product_code']).select(db.clsb_product.device_shelf_code).as_list()[0]['device_shelf_code']
#             print str(s)
#             print "--------------------------------"
#         return dict(item = rows)
#     except Exception as e:
#         return e

#####
# def update_device_shelf():
#     try:
#         db(db.clsb_product).update(device_shelf_code = 1)
#         return True
#     except Exception as e:
#         return e

import unicodedata


def subject_class():
    try:
        categories = db((db.clsb_category.category_name == 'Sách Giáo Khoa - Bài Tập') |
                        (db.clsb_category.category_name == 'Sách Giáo Viên')).select(db.clsb_category.id).as_list()
        print categories[0]['id']
        products = db(db.clsb_product.product_category == db.clsb_category.id) \
                (db.clsb_category.category_type == db.clsb_product_type.id) \
                ((db.clsb_category.category_parent == categories[0]['id']) |
                 (db.clsb_category.category_parent == categories[1]['id'])).select(db.clsb_product.ALL,
                                                                                   db.clsb_category.category_name,
                                                                                   db.clsb_category.category_type,
                                                                                   db.clsb_category.category_parent,
                                                                                   db.clsb_product_type.type_name).as_list()

        for product in products:
        #         print product['clsb_category']['category_parent']
            print '------------- ' + product['clsb_product']['product_title']
            if bool(re.search(r'^[b,B]ài [t,T]ập', product['clsb_product']['product_title'])):
                subject = product['clsb_product']['product_title'][11:]
                index = re.search(r' \d+', subject)
                subject = subject[: index.start()]
                pclass = index.group()
            else:
                subject = product['clsb_product']['product_title']
                index = re.search(r' \d+', subject)
                subject = subject[: index.start()]
                pclass = index.group().strip()
            print '\'' + subject + '\''
            #             print '\'' + pclass + '\''

            subj_code = u'' + subject.strip()
            print subj_code
            subj_code = unicodedata.normalize('NFKD', subj_code).encode('ascii', 'ignore')
            print subj_code
            subj_code = subj_code.upper()
            subj_code = subj_code.replace(' ', '_')
            print subj_code
            #             subj_id = db.clsb_subject.update_or_insert(subject_name = subject, subject_code = subj_code)
            #             print subj_id
            #             cls_id = db.clsb_class.update_or_insert(class_name = 'Lớp '+pclass, class_code= 'LOP'+pclass)
            #
            #             subj_cls_id = db.clsb_subject_class.update_or_insert(subject_id = subj_id, class_id = cls_id)
            #             print subj_cls_id

    except Exception as e:
        return e

import os
from PIL import Image
def make_all_thumbnail():
    size=(THUMB_X,THUMB_Y)

    try:
        ff = osFileServer.listdir()
        dir_list = list()
        #for f in ff:
        #    #if not os.path.isdir("bob")
        #return dict(i=ff)
        for f in ff:
            try:

                path = settings.home_dir + f
                cover = settings.home_dir + fs.path.pathjoin(f, 'cover.clsbi')
                try:
                    im = Image.open(cover)
                except Exception as e:
                    continue
                thumb=im.copy()
                thumb.thumbnail(size, Image.ANTIALIAS)
                thumb.save(os.path.join(path, 'thumb.png'))
            except Exception as e:
                try:
                    osFileServer.copy(fs.path.pathjoin(path, 'cover.clsbi'),
                              fs.path.pathjoin(path, 'thumb.png'), True)
                except Exception as e1:
                    print e1
                print e
        return CB_0000#SUCCESS
    except Exception as e:
        return dict(error=str(e))

def promotion():
    try:
        products = db(db.clsb_product.id == db.clsb_product_metadata.product_id) \
                (db.clsb_product_metadata.metadata_id == db.clsb_dic_metadata.id) \
                (db.clsb_dic_metadata.metadata_name == 'cover_price').select(db.clsb_product.id,
                                                                             db.clsb_product.product_price,
                                                                             db.clsb_product_metadata.metadata_value,
                                                                             db.clsb_dic_metadata.metadata_name,
        ).as_list()

        error_cover_price = list()

        for product in products:
            price = product['clsb_product_metadata']['metadata_value']
            try:
                if price and int(price):
                    db.clsb_product.update_or_insert(db.clsb_product.id == product['clsb_product']['id'],
                                                     product_price=30 * int(price) / 100)
                error_id = None
            except Exception as e:
                temps = dict()
                db.clsb_product.update_or_insert(db.clsb_product.id == product['clsb_product']['id'],
                                                 product_price=0)
                temps['product_id'] = product['clsb_product']['id']
                temps['cover_price_error'] = product['clsb_product_metadata']['metadata_value']

                error_cover_price.append(temps)
                #             if error_id:
                #                 db(db.clsb_product_metadata.product_id==error_id).update(metadata_value = '0')

        return dict(Error=error_cover_price)
    except Exception as e:
        return e


def update_thumb():
    osFileServerCP = OSFS(settings.home_dir+settings.cp_dir)
    try:
        product = db(db.clsb_product.id == request.args[0]).select(db.clsb_product.product_title,
                                                                   db.clsb_product.product_code).first()
        if "thumb" in request.vars:
            product_code = product.product_code
            check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
            if len(check_cp) > 0:
                cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
                path_thumb = fs.path.pathjoin("CP%s" % cpid, 'published', product_code + "/thumb.png")
                path_cover = fs.path.pathjoin("CP%s" % cpid, 'published', product_code + "/cover.clsbi")
            else:
                path_thumb = product.product_code + "/thumb.png"
                path_cover = product.product_code + "/cover.clsbi"
            osFileServer.setcontents(path_thumb, request.vars.thumb.file)
            osFileServer.setcontents(path_cover, request.vars.thumb.file)
            directory = STATIC_FILE + product.product_code
            if not os.path.exists(directory):
                os.makedirs(directory)
            copyanything(settings.home_dir + path_cover, STATIC_FILE + product.product_code + "/cover.clsbi")
            copyanything(settings.home_dir + path_thumb, STATIC_FILE + product.product_code + "/thumb.png")
            redirect(URL(f='index', args=['clsb_product', 'edit', 'clsb_product', request.args[0]],
                         user_signature=True))
        thumb = URL('cbs', 'download', 'thumb', args=product.product_code)
        return dict(data=FORM(H4("Product: " + product.product_title),
                              A("Refresh", _href=URL(f='generate_thumb', args=[request.args[0]])),
                              H4("Thumbnail: ", _style="float:left;"),
                              IMG(_src=thumb), BR(_style="overflow: auto;"), BR(_style="overflow: auto;"),
                              H4("New Thumbnail: ", _style="float:left;"),
                              INPUT(_type="file", _name="thumb", _accept="image/*"),
                              BR(_style="overflow: auto;"), BR(_style="overflow: auto;"),
                              INPUT(_type="submit", value="Cập nhật", _style="margin-left: 100px;"),
                              _method='POST', _enctype='multipart/form-data', _action=""))
    except Exception as ex:
        return dict(error=str(ex) + str(osFileServerCP))


def generate_thumb():
    try:
        product = db(db.clsb_product.id == request.args[0]).select(db.clsb_product.product_title,
                                                                   db.clsb_product.product_code).first()
        product_code = product.product_code
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()

        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'published', product_code)
        else:
            path = product_code
        print path
        product_files = osFileServer.listdir(path=path, wildcard=product_code + ".[Zz][Ii][Pp]", files_only=True)
        if not check_media_in_zip(fs.path.pathjoin(settings.home_dir, path, product_files[0]), product_code):
            path = settings.home_dir + path
            if os.path.isfile(path + "/thumb_bk.png"):
                os.rename(path+'/thumb.png', path+'/thumb_media.png')
                os.rename(path+'/thumb_bk.png', path+'/thumb.png')
        else:
            path = settings.home_dir + path
            if os.path.isfile(path + "/thumb_bk.png"):
                thumb_img = path + "/thumb_bk.png"
                cover_img = path + "/cover_bk.clsbi"
            else:
                thumb_img = path + "/thumb.png"
                cover_img = path + "/cover.clsbi"
            import Image
            #thumb
            try:
                background_thumb = Image.open(thumb_img)
                foreground_thumb = Image.open("/home/CBSData/thumb.png")
                background_thumb.paste(foreground_thumb, (background_thumb.size[0]-foreground_thumb.size[0], background_thumb.size[1]-foreground_thumb.size[1]), foreground_thumb)
                background_thumb.save(path + "/thumb_media.png", "PNG")
                try:
                    if "thumb_bk" not in thumb_img:
                        os.rename(path+'/thumb.png', path+'/thumb_bk.png')
                except Exception as err:
                    pass
                os.rename(path+'/thumb_media.png', path+'/thumb.png')
            except Exception as err:
                pass
            #cover
            try:
                background_cover = Image.open(cover_img)
                foreground_cover = Image.open("/home/CBSData/cover.png")
                background_cover.paste(foreground_cover, (background_cover.size[0]-foreground_cover.size[0], background_cover.size[1]-foreground_cover.size[1]), foreground_cover)
                background_cover.save(path + "/cover_media.clsbi", "PNG")
                try:
                    if "cover_bk" not in cover_img:
                        os.rename(path+'/cover.clsbi', path+'/cover_bk.clsbi')
                except Exception as err:
                    pass
                os.rename(path+'/cover_media.clsbi', path+'/cover.clsbi')
            except Exception as err:
                pass
        copyanything(path+"/cover.clsbi", STATIC_FILE + product.product_code + "/cover.clsbi")
        copyanything(path+"/thumb.png", STATIC_FILE + product.product_code + "/thumb.png")
        redirect(URL(f='update_thumb', args=[request.args[0]],
                         user_signature=True))
    except Exception as ex:
        return dict(err=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def check_media_in_zip(path, product_code):
    try:
        import zipfile
        zip_file = zipfile.ZipFile(path, "r")
        for name in [member.filename for member in zip_file.infolist()]:
            if str.startswith(name, product_code.upper()+"/media/"):
                zip_file.close()
                return True
        else:
            zip_file.close()
        return False
    except Exception as err:
        print('tiench' + str(err))
        return False


def update_batch():
    import zipfile
    import fs.utils as Utils
    from datetime import datetime

    update_server = OSFS("/home/DataUpdate")
    files = update_server.listdir(files_only=True, wildcard="*.[Zz][Ii][Pp]")
    results = list()

    bk_dir_root = "bk %s" % (datetime.today())
    if len(files) > 0:
        update_server.makedir(bk_dir_root)
    else:
        return dict(result=u"Không tìm thấy bất kỳ dữ liệu update nào!")

    for file in files:
        code = file[:-4]
        result = u"%(file)s: Update thành công!" % dict(file=file)
        z = None
        zout = None
        zbk = None
        bk_dir = fs.path.pathjoin(bk_dir_root, code)

        try:
            if db(db.clsb_product.product_code == code).count() <= 0:
                raise ValueError(u"Không tìm thấy sản phẩm trong hệ thống!")

            if not osFileServer.exists(code):
                raise ValueError(u"Không tìm thấy thư mục dữ liệu cũ trong hệ thống!")

            # Backup old data
            update_server.makedir(bk_dir)
            for data_file in osFileServer.listdir(code, files_only=True):
                if data_file in ["cover.clsbi", "thumb.png", "%s.E.pdf" % code, "%s.zip" % code, "%s.zip.bk" % code]:
                    Utils.copyfile(osFileServer, fs.path.pathjoin(code, data_file),
                                   update_server, fs.path.pathjoin(bk_dir, data_file))

            # process new data
            zip_path = fs.path.pathjoin(code, file)[:-3] + "zip"
            z = zipfile.ZipFile(update_server.open(file, 'rb'))
            zout = zipfile.ZipFile(osFileServer.open(zip_path, 'wb+'), mode="w")

            Utils.copyfile(update_server, file, osFileServer, zip_path + ".bk", overwrite=True)
            for filename in z.namelist():
                buffer_data = z.read(filename)
                zinfo = z.getinfo(filename)
                if filename.endswith('.E.pdf'):
                    osFileServer.setcontents(fs.path.pathjoin(code, fs.path.basename(filename)), z.read(filename))
                    pdf_path = fs.path.pathjoin(code, "%s.E.pdf" % code)
                    if not isEncrypted(pdf_path):
                        if update_server.exists(fs.path.pathjoin(bk_dir, fs.path.basename(filename))):
                            Utils.copyfile(update_server, fs.path.pathjoin(bk_dir, fs.path.basename(filename)),
                                           osFileServer, fs.path.pathjoin(code, fs.path.basename(filename)))
                        raise ValueError(u"%s pdf không được mã hóa!" % filename)
                else:
                    if zinfo.external_attr == 16:
                        zout.writestr(filename, '')
                    else:
                        zout.writestr(filename, buffer_data)
                    if filename.find('cover.clsbi') >= 0:
                        osFileServer.setcontents(fs.path.pathjoin(code, "cover.clsbi"), buffer_data)
                        makethumb(code)
            zout.close()
            z.close()
            update_server.remove(file)
        except Exception as ex:
            if isinstance(ex, ValueError):
                result = u"%(file)s: %(error)s" % dict(file=file, error=ex)
            else:
                result = u"%(file)s - Lỗi: %(error)s!" % dict(file=file, error=ex)
            try:
                if update_server.exists(bk_dir):
                    for data_file in update_server.listdir(bk_dir, files_only=True):
                        Utils.copyfile(update_server, fs.path.pathjoin(bk_dir, data_file),
                                       osFileServer, fs.path.pathjoin(code, data_file), overwrite=True)
            except:
                pass
        finally:
            if z is not None:
                z.close()
            if zout is not None:
                zout.close()
        results.append(result)
    return dict(result=results)


def import_product():
    import xlrd

    excel_form = FORM(SPAN('Excel File: '), INPUT(_name='excel_file', _type='file'),
                      INPUT(_type='submit', _value='Upload'), BR(), _action=URL())
    if "excel_file" in request.vars and not isinstance(request.vars.excel_file, str):
        excel_file = request.vars.excel_file
        excel_table = DIV()
        if excel_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            message = H3('Excel Uploaded: %s' % request.vars.excel_file.filename)
            fields = ['product_category', 'device_shelf_code', 'product_collection', 'product_creator',
                      'product_publisher', 'subject', 'class', 'product_title', 'product_description',
                      'product_code', 'co_author', 'cover_price', 'pub_year', 'format', 'edition',
                      'key_word', 'page_number']
            try:
                excel_file = xlrd.open_workbook(file_contents=excel_file.value)
                worksheet = excel_file.sheet_by_name('Sheet1')
                num_rows = worksheet.nrows - 1
                num_cells = worksheet.ncols - 1
                curr_row = -1
                while curr_row < num_rows:
                    curr_row += 1
                    curr_cell = -1
                    if curr_row == 0:
                        while curr_cell < num_cells:
                            curr_cell += 1
                            cell_value = worksheet.cell_value(curr_row, curr_cell)
                            if cell_value != fields[curr_cell]:
                                message = H3("Định dạng file excel không hợp lệ!", _style='color:red;')
                                excel_form.insert(0, SPAN(message))
                                return dict(excel_form=excel_form)
                    else:
                        product = dict()
                        while curr_cell < num_cells:
                            curr_cell += 1
                            # Cell Types: 0=Empty, 1=Text, 2=Number, 3=Date, 4=Boolean, 5=Error, 6=Blank
                            # cell_type = worksheet.cell_type(curr_row, curr_cell)
                            product[fields[curr_cell]] = worksheet.cell_value(curr_row, curr_cell)
                        excel_table.append(process_insert(product))
            except Exception as ex:
                import traceback

                traceback.print_exc()
                message = H3("Error: %s" % str(ex), _style='color:red;')
                excel_form.insert(0, SPAN(message))
                return dict(excel_form=excel_form)
        else:
            message = H3('Uploaded file is not excel file!', _style='color:red;')
        excel_form.insert(0, SPAN(message))
        excel_form.append(excel_table)
        # excel_form = FORM(SPAN(message), BR(),
        #                   SPAN('Excel File: '), INPUT(_name='excel_file', _type='file'), BR(),
        #                   INPUT(_type='submit', _value='Upload'), BR(), excel_table, _action=URL())
    return dict(excel_form=excel_form)


def process_insert(product):
    import traceback
    import StringIO

    res = DIV("Process insert product: %s" % product['product_title'])
    try:
        rets = db(db.clsb_category.category_name == product['product_category']).select(db.clsb_category.id)
        if len(rets) == 0:
            res += DIV(u"Không tồn tại product category: %s" % product['product_category'])
            res += DIV("Insert Fail!")
            res += BR()
            return res
        product['product_category'] = rets.first().id
        res += DIV("product_category: %s" % product['product_category'])

        rets = db(db.clsb_device_shelf.device_shelf_code == product['device_shelf_code'])
        rets = rets.select(db.clsb_device_shelf.id)
        if len(rets) == 0:
            res += DIV(u"Không tồn tại device shelf code: %s" % product['device_shelf_code'])
            res += DIV("Insert Fail!")
            res += BR()
            return res
        product['device_shelf_code'] = rets.first().id
        res += DIV("device_shelf_code: %s" % product['device_shelf_code'])

        if len(product['product_collection']) == 0:
            product['product_collection'] = None
        else:
            rets = db(db.clsb__collection.collection_name == product['product_collection'])
            rets = rets.select(db.clsb_collection.id)
            if len(rets) == 0:
                res += DIV(u"Không tồn tại product collection: %s" % product['product_collection'])
                res += DIV("Insert Fail!")
                res += BR()
                return res
            product['product_collection'] = rets.first().id
            res += DIV("product_collection: %s" % product['product_collection'])

        rets = db(db.clsb_dic_creator.creator_name == product['product_creator']).select(db.clsb_dic_creator.id)
        if len(rets) == 0:
            res += DIV(u"Không tồn tại product creator: %s" % product['product_creator'])
            res += DIV("Insert Fail!")
            res += BR()
            return res
        product['product_creator'] = rets.first().id
        res += DIV("product_creator: %s" % product['product_creator'])

        rets = db(db.clsb_dic_publisher.publisher_name == product['product_publisher']).select(db.clsb_dic_publisher.id)
        if len(rets) == 0:
            res += DIV(u"Không tồn tại product publisher: %s" % product['product_publisher'])
            res += DIV("Insert Fail!")
            res += BR()
            return res
        product['product_publisher'] = rets.first().id
        res += DIV("product_publisher: %s" % product['product_publisher'])

        rets = db(db.clsb_subject.subject_name == product['subject']).select(db.clsb_subject.id)
        if len(rets) == 0:
            res += DIV(u"Không tồn tại product subject: %s" % product['subject'])
            res += DIV("Insert Fail!")
            res += BR()
            return res
        product['subject'] = rets.first().id
        res += DIV("subject: %s" % product['subject'])

        rets = db(db.clsb_class.class_name == product['class']).select(db.clsb_class.id)
        if len(rets) == 0:
            res += DIV(u"Không tồn tại product class: %s" % product['class'])
            res += DIV("Insert Fail!")
            res += BR()
            return res
        product['class'] = rets.first().id
        res += DIV("class: %s" % product['class'])

        rets = db(db.clsb_subject_class.subject_id == product['subject'])
        rets = rets(db.clsb_subject_class.class_id == product['class']).select(db.clsb_subject_class.id)
        if len(rets) == 0:
            product['subject_class'] = db.clsb_subject_class.insert(subject_id=product['subject'],
                                                                    class_id=product['class'])
        else:
            product['subject_class'] = rets.first().id
        res += DIV("subject_class: %s" % product['subject_class'])

        check_product = db(db.clsb_product.product_code == product['product_code']).count()
        if check_product > 0:
            res += DIV(u"Đã tồn tại mã sản phẩm trong hệ thống!")
            res += DIV("Insert Fail!")
            res += BR()
            return res

        query = db(db.clsb_category.id == product['product_category'])
        query = query(db.clsb_product_type.id == db.clsb_category.category_type).select(db.clsb_product_type.type_name)
        product_type = query.first().type_name
        extract_res = extract_product_data(product['product_code'], product_type, product['product_title'])
        if "OK" not in extract_res:
            res += DIV(u"Extract Error: %s" % extract_res)
            res += DIV("Insert Fail!")
            res += BR()
            return res
        try:
            code = product['product_code']
            if product_type == 'Application':
                import subprocess

                sh_location = '/home/CBSData/SignUpdate/convert2ota.sh'
                proc = subprocess.Popen('sh %s %s %s "%s" %s %s "%s" %s' % (sh_location,
                                                                            '%s%s/%s.zip' % (
                                                                            settings.home_dir, code, code),
                                                                            code, '127.0.0.1:3306', 'dev',
                                                                            settings.database_uri.split('/')[-1],
                                                                            'DEV2013!@#', '%sOTAUPDATE/%s.zip' % (
                settings.home_dir, code)),
                                        shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)
                proc.wait()
                std_err = proc.stderr.readlines()
                if len(std_err) > 0:
                    print "ERROR ON OTA: " + str(std_err)
                    raise RuntimeError(str(std_err))
        except:
            output_err = StringIO.StringIO()
            traceback.print_exc(file=output_err)
            session.flash = output_err.getvalue()
            response.flash = output_err.getvalue()

        p_cover = URL(a='cbs', c='download', f='cover', scheme=True, host=True, args=product['product_code'])
        p_data = URL(a='cbs', c='download', f='data', scheme=True, host=True, args=product['product_code'])
        p_pdf = URL(a='cbs', c='download', f='product', scheme=True, host=True, args=(product['product_code']))
        pid = db.clsb_product.insert(product_category=product['product_category'],
                                     device_shelf_code=product['device_shelf_code'],
                                     product_collection=product['product_collection'],
                                     product_creator=product['product_creator'],
                                     product_publisher=product['product_publisher'],
                                     subject_class=product['subject_class'],
                                     product_title=product['product_title'],
                                     product_description=product['product_description'],
                                     product_code=product['product_code'],
                                     product_cover=p_cover, product_data=p_data, product_pdf=p_pdf,
                                     product_status='Import')
        # get current date
        current_date = strftime("%Y%m%d", gmtime())
        # check metadata version exits
        metadata = db(db.clsb_dic_metadata.metadata_name == 'version').select(db.clsb_dic_metadata.id)
        if len(metadata) > 0:
            vid = metadata.first().id
        else:
            metadata_name_value = 'version'
            vid = db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, metadata_label=metadata_name_value,
                                              metadata_description=metadata_name_value)
        db.clsb_product_metadata.insert(product_id=pid, metadata_id=vid, metadata_value=str(current_date))
        res += DIV("metadata version: %s" % current_date)

        metadata = db(db.clsb_dic_metadata.metadata_name == 'co_author').select(db.clsb_dic_metadata.id)
        if len(metadata) > 0:
            vid = metadata.first().id
        else:
            metadata_name_value = 'co_author'
            vid = db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, metadata_label=metadata_name_value,
                                              metadata_description=metadata_name_value)
        db.clsb_product_metadata.insert(product_id=pid, metadata_id=vid, metadata_value=product['co_author'])
        res += DIV("metadata co_author: %s" % product['co_author'])

        metadata = db(db.clsb_dic_metadata.metadata_name == 'cover_price').select(db.clsb_dic_metadata.id)
        if len(metadata) > 0:
            vid = metadata.first().id
        else:
            metadata_name_value = 'cover_price'
            vid = db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, metadata_label=metadata_name_value,
                                              metadata_description=metadata_name_value)
        db.clsb_product_metadata.insert(product_id=pid, metadata_id=vid, metadata_value=product['cover_price'])
        res += DIV("metadata cover_price: %s" % product['cover_price'])

        metadata = db(db.clsb_dic_metadata.metadata_name == 'pub_year').select(db.clsb_dic_metadata.id)
        if len(metadata) > 0:
            vid = metadata.first().id
        else:
            metadata_name_value = 'pub_year'
            vid = db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, metadata_label=metadata_name_value,
                                              metadata_description=metadata_name_value)
        db.clsb_product_metadata.insert(product_id=pid, metadata_id=vid, metadata_value=product['pub_year'])
        res += DIV("metadata pub_year: %s" % product['pub_year'])

        metadata = db(db.clsb_dic_metadata.metadata_name == 'format').select(db.clsb_dic_metadata.id)
        if len(metadata) > 0:
            vid = metadata.first().id
        else:
            metadata_name_value = 'format'
            vid = db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, metadata_label=metadata_name_value,
                                              metadata_description=metadata_name_value)
        db.clsb_product_metadata.insert(product_id=pid, metadata_id=vid, metadata_value=product['format'])
        res += DIV("metadata format: %s" % product['format'])

        metadata = db(db.clsb_dic_metadata.metadata_name == 'edition').select(db.clsb_dic_metadata.id)
        if len(metadata) > 0:
            vid = metadata.first().id
        else:
            metadata_name_value = 'edition'
            vid = db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, metadata_label=metadata_name_value,
                                              metadata_description=metadata_name_value)
        db.clsb_product_metadata.insert(product_id=pid, metadata_id=vid, metadata_value=product['edition'])
        res += DIV("metadata edition: %s" % product['edition'])

        metadata = db(db.clsb_dic_metadata.metadata_name == 'key_word').select(db.clsb_dic_metadata.id)
        if len(metadata) > 0:
            vid = metadata.first().id
        else:
            metadata_name_value = 'key_word'
            vid = db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, metadata_label=metadata_name_value,
                                              metadata_description=metadata_name_value)
        db.clsb_product_metadata.insert(product_id=pid, metadata_id=vid, metadata_value=product['key_word'])
        res += DIV("metadata key_word: %s" % product['key_word'])

        metadata = db(db.clsb_dic_metadata.metadata_name == 'page_number').select(db.clsb_dic_metadata.id)
        if len(metadata) > 0:
            vid = metadata.first().id
        else:
            metadata_name_value = 'page_number'
            vid = db.clsb_dic_metadata.insert(metadata_name=metadata_name_value, metadata_label=metadata_name_value,
                                              metadata_description=metadata_name_value)
        db.clsb_product_metadata.insert(product_id=pid, metadata_id=vid, metadata_value=product['page_number'])
        res += DIV("metadata page_number: %s" % product['page_number'])
        res += DIV("Insert Done!")
        res += BR()
        print pid
    except:
        output_err = StringIO.StringIO()
        traceback.print_exc(file=output_err)
        session.flash = output_err.getvalue()
        response.flash = output_err.getvalue()
        res += DIV("Error: %s" % output_err.getvalue())
        res += DIV("Insert Fail!")
        res += BR()

    return res

def execute_product_id():
    try:
        tmp = ''
        product_id = request.vars['product_id']
        product_list = session.product_id_list

        if product_list == '':
            tmp += product_id
            tmp += ','
            session.product_id_list = tmp
            return

        product_arr = product_list.split(",")


        if product_id in product_arr:
            str_tmp = ''

            for product in product_arr:
                if product == '' or product == product_id:
                    continue
                str_tmp += product
                str_tmp += ','

            session.product_id_list = str_tmp
            return


        product_list += product_id

        product_list += ','
        print product_list
        session.product_id_list = product_list
    except Exception as e:
        print e

def show_all():
    try:
        db(db.clsb_product.id > 0).update(show_on='ANDROID_APP/IOS_APP/CBM/STORE_WEB/STORE_APP')
        return dict(result='SUCCESS')
    except Exception as err:
        return dict(error=str(err))
def show_hide():
    product_show_all = settings.default_show.split('/')

    product_type = db(db.clsb_product_type.id > 0).select().as_list()
    product_type.insert(0, dict(id=0, type_name='Tất cả'))

    author_cp = db(db.auth_user.id > 0).select().as_list()
    author_cp.insert(0, dict(id=0, email='Tất cả'))

    list_cate_parent = db(db.clsb_category.id > 0).select(db.clsb_category.category_parent, distinct=True).as_list()
    list_parent = list()
    for cate_parent in list_cate_parent:
        if cate_parent['category_parent']:
            list_parent.append(int(cate_parent['category_parent']))
    list_cate_child = db(~db.clsb_category.id.belongs(list_parent)).select().as_list()
    list_cate_child.insert(0, dict(id=0, category_name='Tất cả', category_code='ALL'))

    list_show = db(db.clsb_show_hide.product_type == 0)\
        (db.clsb_show_hide.auth_id == 0)\
        (db.clsb_show_hide.category == 0).select()
    if len(list_show) == 0:
        db.clsb_show_hide.insert(value_show=settings.default_show)
        current_status = product_show_all
    else:
        list_show = list_show.first();
        current_status = str(list_show['value_show']).split('/')
    dict_show = dict()
    dict_show['ANDROID_APP'] = "Classbook Android App"
    dict_show['IOS_APP'] = "Classbook IOS App"
    dict_show['CBM'] = "Trang cbm"
    dict_show['STORE_WEB'] = "Trang web classbook.vn/store"
    dict_show['STORE_APP'] = "App Classbook Store"
    vars = dict()
    if len(request.vars) > 0:
        current_status = list()
        show_val = ""
        for show_on in product_show_all:
            if show_on in request.vars:
                show_val = show_val + "/" + show_on
                current_status.append(show_on)
        try:
            query = db(db.clsb_product.id > 0)
            if request.vars.product_type != '0':
                query = query(db.clsb_product.product_category == db.clsb_category.id)\
                    (db.clsb_category.category_type == request.vars.product_type)
            if request.vars.auth != '0':
                query = query(db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
                    (db.clsb20_product_cp.created_by == request.vars.auth)
            if request.vars.category != '0':
                query = query(db.clsb_product.product_category == request.vars.category)
            select_product = query.select(db.clsb_product.id).as_list()
            list_id = list()
            for product in select_product:
                list_id.append(product['id'])
            print(list_id)
            db(db.clsb_product.id.belongs(list_id)).update(show_on=show_val)
            check_status_exist = db(db.clsb_show_hide.product_type == request.vars.product_type)\
                (db.clsb_show_hide.auth_id == request.vars.auth)\
                (db.clsb_show_hide.category == request.vars.category).select()
            if len(check_status_exist) == 0:
                db.clsb_show_hide.insert(value_show=show_val, product_type=request.vars.product_type,
                                                    auth_id=request.vars.auth, category=request.vars.category)
            else:
                db(db.clsb_show_hide.product_type == request.vars.product_type)\
                (db.clsb_show_hide.auth_id == request.vars.auth)\
                (db.clsb_show_hide.category == request.vars.category).update(value_show=show_val)
            vars['product_type'] = int(request.vars.product_type)
            vars['auth'] = int(request.vars.auth)
            vars['category'] = int(request.vars.category)
            response.flash = "THÀNH CÔNG"
        except Exception as err:
            response.flash = str(err) + " on line " + str(sys.exc_traceback.tb_lineno)
    else:
        vars['product_type'] = 0
        vars['auth'] = 0
        vars['category'] = 0
    print(request.vars)
    print(vars)
    return dict(list_show=product_show_all, current_status=current_status, dict_show=dict_show,
                product_type=product_type, author_cp=author_cp, list_cate_child=list_cate_child, vars=vars)

def get_list_show_hide():#params: product_type/auth_id/category
    response.generic_patterns = ['*']
    try:
        show_value = db(db.clsb_show_hide.product_type == request.args[0])\
            (db.clsb_show_hide.auth_id == request.args[1])\
            (db.clsb_show_hide.category == request.args[2]).select()
        if len(show_value) == 0:
            str_show = settings.default_show
        else:
            str_show = show_value.first()['value_show']
        print('value_show: ' + str_show)
        return dict(value_show=str_show)
    except Exception as err:
        return dict(err=str(err))

def show_metadata_product():# category_code
    try:
        cate = request.args[0]
        data = list()
        products = db(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_category.category_code.like("%" + cate + "%"))\
                (db.clsb_product.product_status == "Pending")\
                (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                (db.clsb_subject_class.subject_id == db.clsb_subject.id)\
                (db.clsb_subject_class.class_id == db.clsb_class.id).select(orderby=db.clsb_category.id)
        for product in products:
            temp = dict()
            temp['id'] = product[db.clsb_product.id]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['product_title'] = product[db.clsb_product.product_title]
            temp['device_shelf_code'] = product[db.clsb_product.device_shelf_code]
            #temp['product_description'] = product[db.clsb_product.product_description]
            temp['category'] = product[db.clsb_category.category_name]
            temp['subject'] = product[db.clsb_subject.subject_name]
            temp['class'] = product[db.clsb_class.class_name]
            temp['product_price'] = product[db.clsb_product.product_price]
            temp['product_publisher'] = product[db.clsb_product.product_publisher]
            temp['product_creator'] = product[db.clsb_product.product_creator]
            temp['product_collection'] = product[db.clsb_product.product_collection]
            data.append(temp)
        return dict(data=data)
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
def get_err_cover_price():
    try:
        data = list()
        products = db(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_category.category_type == 1)\
                (db.clsb_product.product_status == "Approved").select()
        for product in products:
            temp = dict()
            temp['product_id'] = product[db.clsb_product.id]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['product_price'] = product[db.clsb_product.product_price]
            cover_price = db(db.clsb_product_metadata.product_id == product[db.clsb_product.id])\
                    (db.clsb_product_metadata.metadata_id == 2).select(db.clsb_product_metadata.metadata_value)
            if len(cover_price) == 0:
                temp['cover_price'] = "Chưa nhập"
                data.append(temp)
            else:
                try:
                    price = int(product[db.clsb_product.product_price])
                    cover_price = int(cover_price.first()[db.clsb_product_metadata.metadata_value])
                    if (cover_price * 3) / 10 != price:
                        temp['cover_price'] = cover_price
                        data.append(temp)
                except Exception as e:
                    temp['cover_price'] = "ERROR: " + str(e)
                    data.append(temp)
        return dict(product=data)
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def get_none_description():
    try:
        data = list()
        products = db(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_category.category_parent == 2)\
                (db.clsb_product.product_status == "Approved").select()
        for product in products:
            if len(str(product[db.clsb_product.product_description])) < 20:
                temp = dict()
                temp['product_id'] = product[db.clsb_product.id]
                temp['product_code'] = product[db.clsb_product.product_code]
                temp['product_description'] = product[db.clsb_product.product_description]
                data.append(temp)
        return dict(product=data)
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def get_detail_product():
    try:
        categories = [1, 26]
        data = list()
        #products = db(db.clsb_product.product_category == db.clsb_category.id)\
        #        (db.clsb_category.category_parent.belongs(categories)).select()
        products = db(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product.created_on >= "2015-06-08 00:00:00")\
                (db.clsb_product.created_on <= "2015-06-13 23:59:59").select()
        for product in products:
            temp = dict()
            temp['product_id'] = product[db.clsb_product.id]
            temp['product_code'] = product[db.clsb_product.product_code]
            temp['product_title'] = product[db.clsb_product.product_title]
            temp['product_category'] = product[db.clsb_category.category_name]
            temp['product_price'] = product[db.clsb_product.product_price]
            temp['created_on'] = product[db.clsb_product.created_on]
            temp['product_status'] = product[db.clsb_product.product_status]
            data.append(temp)
        return dict(product=data)
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def insert_relation():
    try:
        if request.args:
            print(request.args)
            if len(request.args) == 1:
                product_id = request.args[0]
                return dict(product_id=product_id)
            elif len(request.args) == 2:
                product_id = request.args[0]
                relation_id = request.args[1]
                check_relation = db(db.clsb_product.id == relation_id).select()
                if len(check_relation) == 0:
                    return dict(result=False, mess="Sản phẩm không tồn tại")
                check1 = db(db.clsb_product_relation.product_id == product_id)\
                        (db.clsb_product_relation.relation_id == relation_id).select()
                check2 = db(db.clsb_product_relation.product_id == relation_id)\
                        (db.clsb_product_relation.relation_id == product_id).select()
                if len(check1) + len(check2) > 0:
                    return dict(result=False, mess="Đã tồn tại liên kết")
                else:
                    db.clsb_product_relation.insert(product_id=product_id, relation_id=relation_id)
                    db.clsb_product_relation.insert(product_id=relation_id, relation_id=product_id)
                    return dict(result=True, mess="Thành công")
    except Exception as err:
        print(str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(result=False, mess=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def caculate_size():
    try:
        product_id = request.args[0]
        product = db(db.clsb_product.id == product_id).select().first()
        product_code = product['product_code']
        check_cp = db(db.clsb_product.product_code.like(product_code))(db.clsb20_product_cp.product_code.like(product_code)).select()
        path = settings.home_dir + product_code
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['clsb20_product_cp']['created_by'], db)
            path = settings.home_dir + settings.cp_dir + "CP" + cpid + "/published/" + product_code
        size = get_folder_size(path)
        return dict(result=True, size=size)
    except Exception as err:
        print(str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
        return dict(result=False, mess=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def get_folder_size(folder):
    import os
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    total_size = int(total_size / 1024)
    if total_size == 0:
        str_size = "1K"
    elif total_size < 1024:
        str_size = str(total_size) + "K"
    else:
        str_size = str(int(total_size / 1024)) + "M"
    return str_size

def getFolderSize(folder):
    total_size = os.path.getsize(folder)
    for item in os.listdir(folder):
        itempath = os.path.join(folder, item)
        if os.path.isfile(itempath):
            total_size += os.path.getsize(itempath)
        elif os.path.isdir(itempath):
            total_size += getFolderSize(itempath)
    return total_size


def update_cover_price():
    try:
        select_product = db(~db.clsb_product.product_code.like("%.%")).select()
        for product in select_product:
            cover_price = 0
            select_cover_price = db(db.clsb_product_metadata.product_id == product['id'])\
                        (db.clsb_product_metadata.metadata_id == 2).select(db.clsb_product_metadata.metadata_value)
            if len(select_cover_price) > 0:
                cover_price = select_cover_price.first()[db.clsb_product_metadata.metadata_value]
            db(db.clsb_product.id == product['id']).update(cover_price=cover_price)
        return "SUCCESS"
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def resize_all_thumb():
    try:
        select_product = db(db.clsb_product.id > 0).select()
        for product in select_product:
            product_code = product['product_code']
            check_cp = db(db.clsb20_product_cp.product_code == product_code).select()
            path = settings.home_dir + product_code + "/"
            if len(check_cp) > 0:
                cp_id = check_cp.first()['created_by']
                path = settings.home_dir + settings.cp_dir + "CP" + str(cp_id) + "/published/" + product_code + "/"
            resize_thumb(path)
        return "SUCCESS"
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


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
        new_thumb.save(path + 'thumb_resize.png')
        os.remove(path + 'thumb.png')
        os.rename(path + 'thumb_resize.png', path + 'thumb.png')
    except Exception as err:
        print str(err) + path
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def copyanything(src, dst, ovewrite=False):
    try:
        if ovewrite & os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise


def test_preview():
    import subprocess
    subprocess.call(['python', '/home/pylibs/create_preview.py', '/home/CBSData/01GKTAPVIET01/01GKTAPVIET01.E.pdf', '/home/CBSData/01GKTAPVIET01_test_preview/'])