# -*- coding: utf-8 -*-
__author__ = 'tanbm'
import shutil, errno
import subprocess
import products
import usercp
import products

DEVICE_NOT_EXIST = CB_0013
ID_NOT_EXIST = CB_0014
PRODUCT_CODE_NOT_EXIST = CB_0015
SUCCES = CB_0000
DB_RQ_FAILD = CB_0003
ERROR_DATA = CB_0007


def index():
    return dict()


# def check_admin(token):
#     if usercp.check_is_root(token, db):
#         return
#     else:
#         redirect(URL(a='cps', c='users', f='error_time_out.json'))
#         return

@auth.requires_authorize()
def get(): #args = [status, type, page, item_per_page, token]
    try:
        # token = request.args[-1]
        # check_admin(token)
        products = list()
        p_type = "Book"
        page = 0
        status = "Submit"
        items_per_page = settings.items_per_page
        try:
            if len(request.args) >= 1:
                status = request.args[0]
            if len(request.args) >= 2:
                p_type = request.args[1]
            if len(request.args) >= 3:
                page = int(request.args[2])
            if len(request.args) >= 4:
                items_per_page = int(request.args[3])
        except (TypeError, ValueError):
            return dict(error="Params sytax error")

        product_query = db(db.clsb20_product_cp.product_status.like(status))
        # product_query = db(db.clsb20_product_cp.id > 0)
        limitby = (page * items_per_page, (page + 1) * items_per_page)

        total_items = product_query.count()
        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

        db_product = product_query(db.clsb20_product_cp.product_category == db.clsb_category.id)\
            (db.clsb_category.category_type == db.clsb_product_type.id)(db.clsb_product_type.type_name.like(p_type)).select(orderby=~db.clsb20_product_cp.created_on, limitby=limitby).as_list()

        if db_product:
            for row in db_product:
                temp = dict()
                temp['id'] = row['clsb20_product_cp']['id']
                temp['product_title'] = row['clsb20_product_cp']['product_title']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_id'] = row['clsb_category']['id']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_type'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_type']
                temp['creator_name'] = db(db.clsb20_dic_creator_cp.id == row['clsb20_product_cp']['product_creator']).select()[0][
                    'creator_name']
                temp['device_shelf_code'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_code']
                temp['device_shelf_name'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_name']
                temp['publisher_name'] = db(db.clsb_dic_publisher.id == row['clsb20_product_cp']['product_publisher']).select()[0][
                    'publisher_name']
                temp['product_code'] = row['clsb20_product_cp']['product_code']
                temp['product_description'] = row['clsb20_product_cp']['product_description']
                temp['product_price'] = row['clsb20_product_cp']['product_price']
                temp['created_on'] = row['clsb20_product_cp']['created_on']
                path_cp = ""
                if temp['category_type'].upper() == "BOOK":
                    path_cp = row['clsb20_product_cp']['product_code'][:-17]
                if temp['category_type'].upper() == "APPLICATION":
                    created_by = row['clsb20_product_cp']['created_by']
                    path_cp = "CP"+str(usercp.user_get_id_cp(created_by, db))
                if temp['category_type'].upper() == "EXERCISE":
                    path_cp = (row['clsb20_product_cp']['product_code'][:-17])[4:]

                temp['product_thumb'] = URL(a='cpa', c='download', f='cover',
                                            args=[path_cp + "/upload/" + row['clsb20_product_cp']['product_code'] + "/thumb.png"],
                                            host=True)
                if (row['clsb20_product_cp']['product_status'] == "Pending")|(row['clsb20_product_cp']['product_status'] == "Published"):
                    temp['product_thumb'] = URL(a='cps', c='download', f='thumb', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_cover'] = URL(a='cps', c='download', f='cover', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_data'] = URL(a='cps', c='download', f='data', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_pdf'] = URL(a='cps', c='download', f='product', args=[row['clsb20_product_cp']['product_code']], host=True)
                products.append(temp)
        return dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
                    products=products)
    except Exception as ex:
        return dict(error="Request error: "+ex.message+ "on line: " + str(sys.exc_traceback.tb_lineno))


@auth.requires_authorize()
def get_info_by_code():#args = [code, token]
    try:
        # token = request.args[-1]
        # check_admin(token)
        code = ""
        try:
            if len(request.args) > 0:
                code = request.args[0]
        except (TypeError, ValueError):
            pass
        products = list()
        db_product = db(db.clsb20_product_cp.product_code == code)(db.clsb20_product_cp.product_category == db.clsb_category.id)\
            (db.clsb_category.category_type == db.clsb_product_type.id).select()
        if db_product:
            for row in db_product:
                temp = dict()
                temp['id'] = row['clsb20_product_cp']['id']
                temp['product_title'] = row['clsb20_product_cp']['product_title']
                temp['category_id'] = row['clsb20_product_cp']['product_category']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['device_self_code'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_code']
                temp['device_shelf_name'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_name']
                temp['creator_name'] = db(db.clsb20_dic_creator_cp.id == row['clsb20_product_cp']['product_creator']).select()[0]['creator_name']
                temp['publisher_name'] = db(db.clsb_dic_publisher.id == row['clsb20_product_cp']['product_publisher']).select()[0][
                    'publisher_name']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_type'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_type']
                if row['clsb20_product_cp']['subject_class']:
                    subject_classes = db(db.clsb_subject_class.id == row['clsb20_product_cp']['subject_class']).select()[0]
                    temp['class_name'] = db(db.clsb_class.id == subject_classes.class_id).select()[0].class_name
                    temp['subject_name'] = db(db.clsb_subject.id == subject_classes.subject_id).select()[0].subject_name
                temp['product_code'] = row['clsb20_product_cp']['product_code']
                temp['product_price'] = row['clsb20_product_cp']['product_price']
                temp['product_description'] = row['clsb20_product_cp']['product_description']
                if (row['clsb20_product_cp']['product_status'] == "Pending")|(row['clsb20_product_cp']['product_status'] == "Published"):
                    temp['product_thumb'] = URL(a='cps', c='download', f='thumb', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_cover'] = URL(a='cps', c='download', f='cover', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_data'] = URL(a='cps', c='download', f='data', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_pdf'] = URL(a='cps', c='download', f='product', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['is_pending'] = True
                else:
                    path_cp = ""
                    if temp['category_type'].upper() == "BOOK":
                        path_cp = row['product_code'][:-17]
                    if temp['category_type'].upper() == "APPLICATION":
                        created_by = row['clsb20_product_cp']['created_by']
                        path_cp = "CP"+str(usercp.user_get_id_cp(created_by, db))
                    if temp['category_type'].upper() == "EXERCISE":
                        path_cp = (row['product_code'][:-17])[4:]
                    temp['is_pending'] = False
                    temp['product_thumb'] = URL(a='cpa', c='download', f='cover', args=[
                        path_cp + "/upload/" + row['clsb20_product_cp']['product_code'] + "/thumb.png"], host=True)
                    temp['product_cover'] = URL(a='cpa', c='download', f='cover', args=[
                        path_cp + "/upload/" + row['clsb20_product_cp']['product_code'] + "/cover.clsbi"], host=True)
                    temp['product_zip'] = URL(a='cpa', c='download', f='file', args=[
                        path_cp + "/upload/" + row['clsb20_product_cp']['product_code'] + "/" + row['clsb20_product_cp']['product_code'] + ".zip"], host=True)
                products.append(temp)

        return dict(products=products)
    except Exception as ex:
        return dict(error=ex.message + "on line: " + str(sys.exc_traceback.tb_lineno))


@auth.requires_authorize()
def getinfo():#args = [id, token]
    try:
        # token = request.args[-1]
        # check_admin(token)
        id = 0
        try:
            if len(request.args) > 0:
                id = int(request.args[0])
        except (TypeError, ValueError):
            pass
        products = list()
        db_product = db(db.clsb20_product_cp.id == id)(db.clsb20_product_cp.product_category == db.clsb_category.id)\
            (db.clsb_category.category_type == db.clsb_product_type.id).select()

        if db_product:
            for row in db_product:
                temp = dict()
                temp['id'] = row['clsb20_product_cp']['id']
                temp['product_title'] = row['clsb20_product_cp']['product_title']
                temp['category_id'] = row['clsb20_product_cp']['product_category']
                temp['category_code'] = row['clsb_category']['category_code']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['device_self_code'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_code']
                temp['device_shelf_name'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_name']
                temp['creator_name'] = db(db.clsb20_dic_creator_cp.id == row['clsb20_product_cp']['product_creator']).select()[0]['creator_name']
                temp['publisher_name'] = db(db.clsb_dic_publisher.id == row['clsb20_product_cp']['product_publisher']).select()[0][
                    'publisher_name']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['device_self_type'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_type']
                if row['clsb20_product_cp']['subject_class']:
                    subject_classes = db(db.clsb_subject_class.id==row['clsb20_product_cp']['subject_class']).select()[0]
                    temp['class_name'] = db(db.clsb_class.id==subject_classes.class_id).select()[0].class_name
                    temp['subject_name'] = db(db.clsb_subject.id==subject_classes.subject_id).select()[0].subject_name
                temp['product_code'] = row['clsb20_product_cp']['product_code']
                temp['product_price'] = row['clsb20_product_cp']['product_price']
                temp['product_description'] = row['clsb20_product_cp']['product_description']
                if (row['clsb20_product_cp']['product_status'] == "Pending")|(row['clsb20_product_cp']['product_status'] == "Published"):
                    temp['product_thumb'] = URL(a='cps', c='download', f='thumb', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_cover'] = URL(a='cps', c='download', f='cover', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_data'] = URL(a='cps', c='download', f='data', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_pdf'] = URL(a='cps', c='download', f='product', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['is_pending'] = True
                else:
                    path_cp = ""
                    if temp['category_type'].upper() == "BOOK":
                        path_cp = row['clsb20_product_cp']['product_code'][:-17]
                    if temp['category_type'].upper() == "APPLICATION":
                        created_by = row['clsb20_product_cp']['created_by']
                        path_cp = "CP"+str(usercp.user_get_id_cp(created_by, db))
                    if temp['category_type'].upper() == "EXERCISE":
                        path_cp = (row['clsb20_product_cp']['product_code'][:-17])[4:]
                    temp['is_pending'] = False
                    temp['product_thumb'] = URL(a='cpa', c='download', f='cover', args=[
                        path_cp + "/upload/" + row['clsb20_product_cp']['product_code'] + "/thumb.png"], host=True)
                    temp['product_cover'] = URL(a='cpa', c='download', f='cover', args=[
                        path_cp + "/upload/" + row['clsb20_product_cp']['product_code'] + "/cover.clsbi"], host=True)
                    temp['product_zip'] = URL(a='cpa', c='download', f='file', args=[
                        path_cp + "/upload/" + row['clsb20_product_cp']['product_code'] + "/" + row['clsb20_product_cp']['product_code'] + ".zip"], host=True)
                products.append(temp)

        return dict(products=products)
    except Exception as ex:
        return ex.message + "on line: " + str(sys.exc_traceback.tb_lineno)


@auth.requires_authorize()
def reject():#args [product_code, token], vars comment
    result = dict()
    try:
        token = request.args[-1]
        # check_admin(token)
        code = request.args[0]
        cmt = request.vars.comment
        dbproduct = db(db.clsb20_product_cp.product_code == code).select()[0]
        user_id = db(db.auth_user.token.like(token)).select()[0].id
        db.clsb20_review_comment.insert(user_id=user_id, product_code=dbproduct.product_code, comment_time=datetime.now(), review_comment=request.vars.comment)
        db.clsb20_review_history.insert(reviewed_by=user_id, product_code=dbproduct.product_code, reviewed_time=datetime.now(), status="Reject")
        db(db.clsb20_product_cp.product_code == dbproduct.product_code).update(product_status="Reject")
        result['status'] = "OK"
        result['msg'] = cmt
    except Exception as ex:
        return dict(error=ex.message)
    return dict(result=result)


@auth.requires_authorize()
def published():#args = [code, token]
    result = dict()
    try:
        token = request.args[-1]
        # check_admin(token)
        code = request.args[0]
        data = db((db.clsb20_product_cp.product_code == code) & ((db.clsb20_product_cp.product_status.like("pending")) | (db.clsb20_product_cp.product_status.like("published"))))

        if len(data.select()) <= 0:
            return dict(error="Product not found")

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
        review_path = os.path.join(path, 'published')
        if not os.path.exists(review_path):
            os.makedirs(review_path)

        try:
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
                    copyanything(settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code,
                             settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code+"_Backup", True)
                except Exception as e:
                    pass
            if type_name.upper() == "APPLICATION":
                copyanything(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + dbproduct.product_code,
                         settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code, True)
            else:
                copyanything(settings.home_dir + settings.cp_dir + cp_path + "/review/" + dbproduct.product_code,
                         settings.home_dir + settings.cp_dir + cp_path + "/published/" + dbproduct.product_code, True)
        except Exception as e:
            print "ERROR"
            print e
        if type_name.upper() == "BOOK":
            check = db(db.clsb20_encrypt_product.product_code.like(dbproduct.product_code)).select()
            if len(check) > 0:
                if (check.first()['status'].upper() == "PENDING") | (check.first()['status'].upper() == "ENCRYPTING"):
                    return "Đang mã hóa"
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
        result['status'] = "OK"
    except Exception as ex:
        return dict(error=ex.message+" on line: "+str(sys.exc_traceback.tb_lineno))
    return dict(result=result)


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
        else:
            raise

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
    have_zip = False

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


@auth.requires_authorize()
def topending():#args = [product_code, token]
    try:
        token = request.args[-1]
        # check_admin(token)
        code = request.args[0]
        data = db((db.clsb20_product_cp.product_code == code) & (db.clsb20_product_cp.product_status.like("submit")))
        if len(data.select()) <= 0:
            return dict(error="Product not found")

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
            return dict(error=error)

        try:
            copyanything(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + code + "/cover.clsbi",
                             settings.home_dir + settings.cp_dir + cp_path + "/review/" + code + "/cover.clsbi", True)
            copyanything(settings.home_dir + settings.cp_dir + cp_path + "/upload/" + code + "/thumb.png",
                             settings.home_dir + settings.cp_dir + cp_path + "/review/" + code + "/thumb.png", True)
        except:
            pass
        user_id = db(db.auth_user.token.like(token)).select()[0].id
        db.clsb20_review_history.insert(reviewed_by=user_id, product_code=data.select()[0].product_code, reviewed_time=datetime.now(), status="Pending")
        data.update(product_status="Pending")
        return dict(result=CB_0000)
    except OSError as e:
        if e.errno == 2:
            error = "Thiếu file ZIP - " +str(e)+ "- on line" + str(sys.exc_traceback.tb_lineno)
        else:
            error = e
    return dict(error=error)


    #########################


@auth.requires_authorize()
def get_by_type():#args = [status, type, page, item_per_page, token]
    try:
        # token = request.args[-1]
        # check_admin(token)
        products = list()
        page = 0
        items_per_page = settings.items_per_page
        status = "submit"
        type = 0
        try:
            if len(request.args) > 0:
                status = request.args[0]
            if len(request.args) > 1:
                type = int(request.args[1])
            if len(request.args) > 2:
                page = int(request.args[2])
            if len(request.args) > 3:
                items_per_page = int(request.args[3])
        except (TypeError, ValueError):
            pass

        type_name = db(db.clsb20_product_type.id == type).select()
        if len(type_name)>0:
            type_name = type_name[0].type_name

        product_query = db(db.clsb20_product_cp.product_status.like(status))

        limitby = (page * items_per_page, (page + 1) * items_per_page)

        total_items = product_query(db.clsb20_product_cp.product_category == db.clsb_category.id)\
            (db.clsb_category.category_type == db.clsb_product_type.id)\
            (db.clsb20_product_type.type_name == db.clsb_product_type.type_name)\
            (db.clsb20_product_type.id == type).count()

        total_pages = total_items / items_per_page + 1 if total_items % items_per_page > 0 else total_items / items_per_page

        db_product = product_query(db.clsb20_product_cp.product_category == db.clsb_category.id)\
            (db.clsb_category.category_type == db.clsb_product_type.id)\
            (db.clsb20_product_type.type_name == db.clsb_product_type.type_name)\
            (db.clsb20_product_type.id == type).select(
                db.clsb20_product_cp.ALL,
                db.clsb_category.ALL,
                db.clsb_product_type.ALL,
                orderby=db.clsb20_product_cp.created_on, limitby=limitby).as_list()

        if db_product:
            for row in db_product:
                temp = dict()
                temp['id'] = row['clsb20_product_cp']['id']
                temp['product_title'] = row['clsb20_product_cp']['product_title']
                temp['category_name'] = row['clsb_category']['category_name']
                temp['category_id'] = row['clsb20_product_cp']['product_category']
                temp['category_type'] = row['clsb_product_type']['type_name']
                temp['creator_name'] = db(db.clsb20_dic_creator_cp.id == row['clsb20_product_cp']['product_creator']).select()[0][
                    'creator_name']
                temp['device_shelf_code'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_code']
                temp['device_shelf_name'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_name']
                temp['publisher_name'] = db(db.clsb_dic_publisher.id == row['clsb20_product_cp']['product_publisher']).select()[0][
                    'publisher_name']
                temp['device_self_type'] = db(db.clsb_device_shelf.id == row['clsb20_product_cp']['device_shelf_code']).select()[0][
                    'device_shelf_type']
                temp['product_code'] = row['clsb20_product_cp']['product_code']
                temp['product_description'] = row['clsb20_product_cp']['product_description']
                temp['product_price'] = row['clsb20_product_cp']['product_price']
                path_cp = ""
                if temp['category_type'].upper() == "BOOK":
                    path_cp = row['product_code'][:-17]
                if temp['category_type'].upper() == "APPLICATION":
                    created_by = row['clsb20_product_cp']['created_by']
                    path_cp = "CP"+str(usercp.user_get_id_cp(created_by, db))
                if temp['category_type'].upper() == "EXERCISE":
                    path_cp = (row['product_code'][:-17])[4:]
                temp['product_thumb'] = URL(a='cpa', c='download', f='cover',
                                            args=[path_cp + "/upload/" + row['clsb20_product_cp']['product_code'] + "/thumb.png"],
                                            host=True)
                if (row['clsb20_product_cp']['product_status'] == "Pending")|(row['clsb20_product_cp']['product_status'] == "Published"):
                    temp['product_thumb'] = URL(a='cps', c='download', f='thumb', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_cover'] = URL(a='cps', c='download', f='cover', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_data'] = URL(a='cps', c='download', f='data', args=[row['clsb20_product_cp']['product_code']], host=True)
                    temp['product_pdf'] = URL(a='cps', c='download', f='product', args=[row['clsb20_product_cp']['product_code']], host=True)
                products.append(temp)
        return dict(page=page, items_per_page=items_per_page, total_items=total_items, total_pages=total_pages,
                    products=products)
    except Exception as ex:
        return ex.message + " on line: " + str(sys.exc_traceback.tb_lineno)


def check_package():#args code,user_id
    try:
        if len(request.args)<1:
            return dict(error="Chưa nhập tên package")
        code = request.args[0]
        #if len(code.split("."))<3:
        #    return dict(error="Tên package không đúng")
        try:
            user_id = int(request.args[1])

            data_20 = db(db.clsb20_product_cp.product_code.like(code) & db.clsb20_product_cp.product_status.like("%delete%") & db.clsb20_product_cp.created_by == user_id).select()
            if len(data_20) > 0:
                return dict(result="OK")
            data_10 = db(db.clsb_product.product_code.like(code)).select()
            data_20 = db(db.clsb20_product_cp.product_code.like(code)).select()
        except:
            data_10 = db(db.clsb_product.product_code.like(code)).select()
            data_20 = db(db.clsb20_product_cp.product_code.like(code)).select()
        if (len(data_10) > 0) | (len(data_20) > 0):
            return dict(error="Đã tồn tại package")
        else:
            return dict(result="OK")
    except:
        return dict(error=CB_0003)


def upload():
    try:
        if len(request.vars) < 3:
            return dict(mess=CB_0002)

        if 'data' in request.vars:
            try:
                filename = request.vars.data.filename
                token = request.vars['token']
                user_name = request.vars['user_name']

                # get user name by token
                user_info = usercp.info_by_token(user_name, token, db)



                # co can tao thu muc CP neu chua co khong?
                cp_dir = 'CP' + str(usercp.user_get_id_cp(user_info['result']['user_info']['id'], db))
                path = os.path.join(settings.home_dir+settings.cp_dir, cp_dir)
                if not os.path.exists(path):
                    os.makedirs(path)
                print 'path cp_Dir' + str(path)
                upload_path = os.path.join(path, 'upload')
                if not os.path.exists(upload_path):
                    os.makedirs(upload_path)

                index_ = filename.rfind("\\") + 1
                filename = filename[index_:]

                product_type = db(db.clsb20_product_type.type_name.like("Book")).select()[0].type_code
                product_gen_code = usercp.user_gen_product_code(cp_dir, product_type)

                #product_code = filename[:index_dot]
                path = fs.path.join(upload_path, product_gen_code)
                #make folder named by product code if not exits:
                if not os.path.exists(path):
                    os.makedirs(path)
                result = save_data(request.vars.data, product_gen_code + "/" + product_gen_code+".zip", cp_dir, product_gen_code)

                z = zipfile.ZipFile(settings.home_dir+settings.cp_dir+cp_dir+"/upload/"+product_gen_code+"/"+product_gen_code + '.zip', 'r')
                for name in z.namelist():
                    if bool(re.search('cover.[Pp][Nn][Gg]$', name)) or bool(re.search('cover.[Jj][Pp][Gg]$', name)):
                        f = z.open(name)
                        print "Name "+ name
                        save_file(f, product_gen_code+"/cover.clsbi", cp_dir)
                        f.close()
                        break
                z.close()
                kq = db.clsb20_product_from_editor.insert(product_title=request.vars.title, product_code=product_gen_code, created_by=user_info['result']['user_info']['id'])
            except Exception as e:
                print str(e)
                return dict(mess=CB_0003)
        return dict(mess=CB_0000)
    except Exception as e:
        print e
        return dict(mess=CB_0003)


def save_data(file, filename, user_cp_path, code=""):
    old_filename = re.split("\\\\", file.filename)[-1]
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
            except Exception as e:
                print str(e)
            msg = "Faile: "+ex.message
    return msg


def save_file(file, filename, user_cp_path):
    try:
        f = open(settings.home_dir+settings.cp_dir+user_cp_path+"/upload/"+filename, 'w+')
        for chunk in products.fbuffer(file):
            f.write(chunk)
        f.close()
    except Exception as e:
        print e


def zipdir(path, zip):
    rootlen = len(path) + 1
    for base, dirs, files in os.walk(path):
        for file in files:
            fn = os.path.join(base, file)
            zip.write(fn, fn[rootlen:])


@auth.requires_authorize()
def get_reject(): #product_code, token
    token = request.args[1]
    code = request.args[0]
    user_id = db(db.auth_user.token.like(token)).select()[0].id
    cmtdb = db(db.clsb20_review_comment.product_code == code)\
        (db.auth_user.id == db.clsb20_review_comment.user_id).select(db.clsb20_review_comment.ALL, db.auth_user.ALL)
    cp = db(db.clsb20_product_cp.product_code == code).select(db.clsb20_product_cp.created_by)
    cp_id = cp.first()['created_by']
    cp_admin = usercp.user_get_id_cp(cp_id, db)
    items_comment = list()
    for cmt in cmtdb:
        temp = dict()
        temp['user'] = cmt['auth_user']['username']
        if (cp_id == cmt['auth_user']['id']) or (cp_admin == cmt['auth_user']['id']):
            temp['cp_cm'] = True
        temp['comment'] = cmt['clsb20_review_comment']['review_comment']
        temp['time'] = cmt['clsb20_review_comment']['comment_time']
        items_comment.append(temp)
    return dict(comments=items_comment)