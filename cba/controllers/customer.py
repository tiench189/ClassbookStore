from contrib.pbkdf2 import *
P_2_D_KEY = 'c-p3d*b'


def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/customer/delete(ids, table) " + str(e)


def user_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')


def user_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')


def user_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


def get_devices_data(user_id):
    data = db(db.clsb_device.user_id == user_id).select().as_list()
    tmp = ""
    for data_one in data:
        tmp += "<b>"+data_one['device_serial']+"</b>"+"/"+data_one['device_registration']+"<br/>"
    return tmp


@auth.requires_authorize()
def index():
    # check_is_root()

    if request.vars.export and len(request.args) <= 1:
        query = db(db.clsb_user)
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
        num = 0
        for data_one in data_list:
            num += 1
            tbody_data += "<tr style='font-size: 18px;'>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;'>"+str(data_one['id'])+"</td>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;'>"+str(data_one['username'])+"</td>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;'>"+str(data_one['firstName'])+"</td>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;; vertical-align:middle;'>"+str(data_one['lastName'])+"</td>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;; vertical-align:middle;'>"+str(data_one['email'])+"</td>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;'>"+str(data_one['phoneNumber'])+"</td>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;'>"+str(data_one['address'])+"</td>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;'>"+str(data_one['lastLoginTime'])+"</td>" \
                          "<td style='"+("background: #F5F5F5;" if num % 2 == 0 else "")+" border:1px solid #999; vertical-align:middle;'>"+get_devices_data(data_one['id'])+"</td>" \
                          "</tr>"
        table_data = "<thead>" \
                     "<tr style='height: 50px; font-size: 20px;'>" \
                     "<th style='background: #ccc; border:1px solid #999;'>ID</th>" \
                     "<th style='background: #ccc; border:1px solid #999;'>Username</th>" \
                     "<th style='background: #ccc; border:1px solid #999;'>First name</th>" \
                     "<th style='background: #ccc; border:1px solid #999;'>Last name</th>" \
                     "<th style='background: #ccc; border:1px solid #999;'>Email</th>" \
                     "<th style='background: #ccc; border:1px solid #999;'>Phone number</th>" \
                     "<th style='background: #ccc; border:1px solid #999;'>Address</th>" \
                     "<th style='background: #ccc; border:1px solid #999;'>Last login</th>" \
                     "<th style='background: #ccc; border:1px solid #999;'>Devices Serial/Devices Registration</th>" \
                     "</tr>" \
                     "</thead>"\
                     "<tbody>"+tbody_data+"</tbody>"

        return list_to_excel(table_data, 'Customers')



    current_table = "clsb_user"
    if request.url.find("/clsb_user/edit/clsb_user") >= 0:
        return edit_user()
    # fields = [db.clsb_user.username, db.clsb_user.firstName, db.clsb_user.lastName, db.clsb_user.fund, db.clsb_user.valid_time, db.clsb_user.lastLoginTime]
    # if request.url.find('/clsb_user/clsb_device.') >= 0:
    #     fields = [db.clsb_device.user_id, db.clsb_device.device_serial, db.clsb_device.status, db.clsb_device.in_use, db.clsb_device.device_firmware, db.clsb_device.device_release]
    #     current_table = "clsb_device"
    # if request.url.find('/clsb_user/clsb_download_archieve.') >= 0:
    #     fields = [db.clsb_download_archieve.user_id, db.clsb_download_archieve.product_id, db.clsb_download_archieve.download_time, db.clsb_download_archieve.price, db.clsb_download_archieve.purchase_type, db.clsb_download_archieve.device_serial]
    #     current_table = "clsb_download_archieve"
    # if request.url.find('/clsb_user/clsb_user_log.') >= 0:
    #     fields = [db.clsb_user_log.user_id, db.clsb_user_log.user_action, db.clsb_user_log.date_created, db.clsb_user_log.search_text, db.clsb_user_log.product_code, db.clsb_user_log.ip_address]
    #     current_table = "clsb_user_log"
    selectable = lambda ids: delete(ids, current_table)

    form = smartgrid(db.clsb_user,
                             oncreate = user_on_create,
                             onupdate = user_on_update,
                             ondelete = user_on_delete,
                             # fields = fields,
                             create=False,
                             showbuttontext = False,
                             linked_tables=['clsb_user_log', 'clsb_download_archieve', 'clsb_device' ],
                             selectable=selectable,
                             exportclasses=dict(
                                 csv_with_hidden_cols=False,
                                 csv=False,
                                 xml=False,
                                 html=False,
                                 tsv_with_hidden_cols=False,
                                 tsv=False,
                                 json=False
                             )
    )
    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
        "return confirm('"+ CONFIRM_DELETE +"');"
    page = 1
    if request.vars.page:
        page = int(request.vars.page)
    if len(request.args) <= 1:
        form.append(DIV(A("Export page to excel", _class="btn", _href=URL(a=request.application, c=request.controller, f=request.function, vars=dict(export=True, all=True, start=(page-1)*20, total=20))),
                        A("Export all to excel", _class="btn", _style="margin-left: 20px;",_href=URL(a=request.application, c=request.controller, f=request.function, vars=dict(export=True)))))
#    form = SQLFORM(db.clsb_user, showbuttontext = False, selectable=selectable, submit_button = 'Delete')

#    my_extra_element = TR(LABEL('I agree to the terms and conditions'), \
#                      INPUT(_name='agree',value=True,_type='checkbox'))
#    form[0].insert(1,my_extra_element)
    return dict(grid=form)


def edit_user():
    id = request.args[3]
    data = db(db.clsb_user.id == id).select().first()
    form = FORM(
        TABLE(
            TR(
                TD(A("Back to users", _class="btn", _href=URL()), _style="padding: 0; height: 50px;"),
                TD()
            ),
            TR(
                TD('Username:'),
                TD(INPUT(_value=data.username, _disabled=True))
            ),
            TR(
                TD('Password:'),
                TD(INPUT(_value='', _name='password', _type='password'))
            ),
            TR(
                TD('Fund:'),
                TD(INPUT(_value=data.fund, _name='fund'))
            ),
            TR(
                TD('Valid time:'),
                TD(INPUT(_value=data.valid_time, _name='valid_time'))
            ),
            TR(
                TD('Test User:'),
                TD(INPUT(_value=data.test_user, _name='test_user'))
            ),
            TR(
                TD(),
                TD(INPUT(_type="Submit", _value="Submit"))
            )
        )
    )
    if form.accepts(request):
        pwd = data.password
        if request.vars.password != "":
            pwd = pbkdf2_hex(P_2_D_KEY, request.vars.password)
        db(db.clsb_user.id == id).update(
            password=pwd,
            fund=request.vars.fund,
            valid_time=request.vars.valid_time,
            test_user=request.vars.test_user
        )
        session.flash = "OK"
        redirect(URL(args=['clsb_user', 'edit', 'clsb_user', id], user_signature=True))
    if form.errors:
        response.flash = "Xảy ra lỗi"
    return dict(grid = form)