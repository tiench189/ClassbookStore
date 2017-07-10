def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/comments/delete(ids, table) " + str(e)


def device_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')


def device_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')


def device_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


@auth.requires_authorize()
def index():
    # check_is_root()
    if request.vars.export:
        query = db(db.clsb_comment)(db.clsb_product.product_code.like(db.clsb_comment.product_code))
        if request.vars.all is not None:
            start = 0
            total = request.vars.total
            if request.vars.start is not None:
                start = int(request.vars.start)
            if request.vars.total is not None:
                total = int(request.vars.total)
            data_list = query.select(limitby=(start, start+total)).as_list()
        else:
            data_list = query.select().as_list()

        tbody_data = ""
        for data_one in data_list:
            tbody_data += "<tr style='font-size: 18px;'>" \
                     "<td>"+str(data_one['clsb_comment']['id'])+"</td>" \
                     "<td>"+str(data_one['clsb_comment']['email'])+"</td>" \
                     "<td>"+str(data_one['clsb_comment']['comment_content'])+"</td>" \
                     "<td>"+str(data_one['clsb_comment']['comment_date'])+"</td>" \
                     "<td>"+str(data_one['clsb_product']['product_title'])+"</td>" \
                     "<td>"+str(data_one['clsb_comment']['status'])+"</td>" \
                     "</tr>"
        table_data = "<thead>" \
                "<tr style='height: 50px; font-size: 20px;'>" \
                "<th style='background: #ccc;'>ID</th>" \
                "<th style='background: #ccc;'>Email</th>" \
                "<th style='background: #ccc;'>Comment</th>" \
                "<th style='background: #ccc;'>Date</th>" \
                "<th style='background: #ccc;'>Product</th>" \
                "<th style='background: #ccc;'>Status</th>" \
                "</tr>" \
                "</thead>"\
                "<tbody>"+tbody_data+"</tbody>"

        return list_to_excel(table_data, 'comments')

    current_table = "clsb_comment"
#     if request.url.find('/clsb_device/clsb_product.') >= 0:
#         current_table = "clsb_product"
    selectable = lambda ids: delete(ids, current_table)
    
    form = smartgrid(db.clsb_comment, 
                             oncreate = device_on_create,
                             onupdate = device_on_update,
                             ondelete = device_on_delete,
                             showbuttontext = False, selectable=selectable,
                             exportclasses = dict(

                             )
    )

    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
        "return confirm('"+ CONFIRM_DELETE +"');"

    page = 1
    if request.vars.page:
        page = int(request.vars.page)
    form.append(DIV(A("Export page to excel", _class="btn", _href=URL(a=request.application, c=request.controller, f=request.function, vars=dict(export=True, all=True, start=(page-1)*20, total=20))),
                    A("Export all to excel", _class="btn", _style="margin-left: 20px;",_href=URL(a=request.application, c=request.controller, f=request.function, vars=dict(export=True)))))

    return dict(grid = form)