# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import usercp


def check_staff(user):
    # data = db(db.auth_user.id == user)(~db.auth_group.role.like("CPAdmin"))((db.auth_membership.user_id == user) & (db.auth_membership.group_id == db.auth_group.id)).select()
    # if len(data) > 0:
    #     return True
    return False
@auth.requires_login()
def index():
    return dict()

@auth.requires_login()
def old_index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    start = datetime.strptime(str(datetime.now().year), "%Y")
    end = datetime.now()
    if request.vars.start:
        if request.vars.start != "":
            start = datetime.strptime(request.vars.start, "%Y-%m")
    if request.vars.end:
        if request.vars.end != "":
            end = datetime.strptime(request.vars.end, "%Y-%m")

    listType = ["Book", "Application", "Exercise"]
    dataList = list()
    for i in range(len(listType)):
        dataList.append(db(db.clsb20_product_cp)\
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (db.clsb_category.id == db.clsb20_product_cp.product_category)\
            (db.clsb_category.category_type == db.clsb_product_type.id)\
            (db.clsb_product_type.type_name.like(listType[i]))\
            (((db.auth_user.created_by == auth.user.id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))\
            (db.clsb20_product_purchase_item.product_code.like(db.clsb20_product_cp.product_code))\
            (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
            (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type).select(groupby=db.clsb20_product_cp.id))

    data = list()
    data.append(["Tháng", "Sách", "Ứng dụng", "Trắc nghiệm"])
    totalPrice = 0
    paymentYear = 0
    for i in range(start.month, end.month+1):
        timeStart = datetime.strptime(str(start.year)+"-"+str(i), "%Y-%m")
        timeEnd = None
        if i == 12:
            timeEnd = datetime.strptime(str(start.year+1)+"-"+str(1), "%Y-%m")
        else:
            timeEnd = datetime.strptime(str(start.year)+"-"+str(i+1), "%Y-%m")

        temp = list()
        temp.append(str(i)+"/"+str(start.year))
        for item in dataList:
            total = 0
            for product in item:
                price = 0
                downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')))\
                        ((db.clsb_download_archieve.download_time >= timeStart) & (db.clsb_download_archieve.download_time < timeEnd)).select(groupby=db.clsb_download_archieve.id)

                for download in downloads:
                    price += download['price']
                totalPrice += price
                total += price
                price = price - price*usercp.get_discount_value(auth.user.id, db)/100
                paymentYear += price
            temp.append(total)
        data.append(temp)

    query = db((db.clsb20_product_cp.created_by == auth.user.id) | ((db.auth_user.created_by == auth.user.id) & (db.clsb20_product_cp.created_by == db.auth_user.id)))\
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (db.clsb_product.id == db.clsb_download_archieve.product_id)((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time < end) & (db.clsb_download_archieve.status.like("Completed")))
    downloadTotal = len(query.select(groupby=db.clsb_download_archieve.id))
    customerTotal = len(query.select(groupby=db.clsb_download_archieve.user_id))

    query = db(~db.clsb20_product_cp.product_status.like("%delete%"))\
            (((db.auth_user.created_by == auth.user.id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))
    productTotal = len(query.select(groupby=db.clsb20_product_cp.id))
    productPublished = len(query((db.clsb_product.product_code == db.clsb20_product_cp.product_code) & ((db.clsb_product.product_status.like("Approved")))).select(groupby=db.clsb20_product_cp.id))
    productPending = productTotal-productPublished

    response.title = None

    submits = db(db.clsb20_product_cp.product_status.like("submit"))(db.clsb_category.id == db.clsb20_product_cp.product_category)\
        (db.clsb_category.category_type == db.clsb_product_type.id).select(groupby=db.clsb20_product_cp.id)
    totalSubmit = len(submits)
    bookSubmit = 0
    quizSubmit = 0
    appSubmit = 0
    for submit in submits:
        if submit['clsb_product_type']['type_name'].upper() == "BOOK":
            bookSubmit += 1
        if submit['clsb_product_type']['type_name'].upper() == "EXERCISES":
            quizSubmit += 1
        if submit['clsb_product_type']['type_name'].upper() == "APPLICATION":
            appSubmit += 1

    return dict(
        productPublished=productPublished, productPending=productPending, data=data, paymentYear=paymentYear, downloadTotal=downloadTotal, customerTotal=customerTotal, productTotal=productTotal,
        check_staff=check_staff(auth.user.id),
        totalSubmit=totalSubmit,
        bookSubmit=bookSubmit,
        quizSubmit=quizSubmit,
        appSubmit=appSubmit,
        total=totalPrice
        )


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


def error():
    """
    handle error pages
    """
    response.generic_patterns = ['*']
    response.title = "Thông báo lỗi"
    if "code" in request.vars and request.vars.request_url != request.url:
        code = request.vars.code
        response.status = int(code)

        # show custom error message and view
        if not session.error is None:
            if "view" in session.error:
                response.view = session.error['view']
            message = session.error['message']
            del session.error
            if not message is None:
                return dict(request.vars, message=message)

        # default error handle
        if code == "500":
            if 'ticket' in request.vars:
                if str.startswith(request.client, '10.0.'):
                    url_ticket = URL(a="admin", c="default", f="ticket", args=request.vars["ticket"])
                    message = TAG("Server error! Check more info <a href='%s' target='_blank'>here</a>." % url_ticket)
                    return dict(message=message)
        elif code == "401":
            return dict(message=TAG("Bạn không có quyền truy cập! Quay trở về <a href='%s'>trang chủ</a>"
                                    % URL('index')))
        elif code == "404" or code == "400":
            return dict(message=TAG("Đường dẫn không tồn tại(%s)! Quay trở về <a href='%s'>trang chủ</a>"
                                    % (code, URL('index'))))

        return dict(message=TAG("Chức năng đang bảo trì(%s). Bạn có thể quay về <a href='%s'>trang chủ</a> hoặc "
                                "<a href='%s'>thông báo</a> với quản trị viên!"
                                % (code, URL('index'), URL('support_form'))))
    redirect(URL('index'))
