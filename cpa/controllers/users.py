# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Name:        Users
#
# Purpose:     Quản lý thông tin tài khoản và các tài khoản dưới quyền
#
# Version:     1.1
#
# Author:      manhtd
#
# Created:     11/02/2013
# Updated:     11/26/2013
#
# Copyright:   (c) Tinh Vân Books
#
# Todo:
#-----------------------------------------------------------------------------
"""


@auth.requires_login()
@auth.requires_authorize()
def member_register():
    links = None
    db.auth_user.id.readable = False
    # db.auth_user.first_name.writable = False
    # db.auth_user.last_name.writable = False
    # db.auth_user.first_name.readable = False
    # db.auth_user.last_name.readable = False
    db.auth_user.password.readable = False
    db.auth_user.username.readable = False
    db.auth_user.username.writable = False
    db.auth_user.province.readable = False
    db.auth_user.province.writable = False
    db.auth_user.address.readable = False
    db.auth_user.address.writable = False
    db.auth_user.country.readable = False
    db.auth_user.country.writable = False
    db.auth_user.bank_number.readable = False
    db.auth_user.bank_number.writable = False
    db.auth_user.bank_acc.readable = False
    db.auth_user.bank_acc.writable = False
    db.auth_user.phone.readable = False
    db.auth_user.phone.writable = False
    if not "new" in request.args:
        db.auth_user.email.writable = False
    db.auth_user.password.writable = False
    grid = SQLFORM.smartgrid(table=db.auth_user, showbuttontext=False, linked_tables=[], csv=False, links=links,
                             constraints={str(auth.table_user()): (db.auth_user.created_by == auth.user_id)},
                             oncreate=member_register_oncreate, onupdate=member_register_onupdate,
                             ondelete=member_register_ondelete)

    if grid.create_form or grid.update_form or grid.view_form:
        functions = list()
        roles = list()
        try:
            from gluon.contrib.simplejsonrpc import ServerProxy
            url = settings.rpc_server + "/cba/admin/call/jsonrpc"
            service = ServerProxy(url)
            if grid.create_form:
                res = service.get_cp_roles(request.application)
            else:
                res = service.get_cp_roles(request.application)
            if "result" in res and res["result"]:
                functions.extend(res["result"]["functions"])
                roles.extend(res["result"]["groups"])
        except:
            import traceback
            traceback.print_exc()
            pass

        groups = list()
        if grid.view_form or grid.update_form:
            groups = db(db.auth_membership.user_id == request.args[-1]).select(db.auth_membership.group_id)
            groups = [x.group_id for x in groups]

        div_permission = TABLE(_border=1, _style="border: 1px solid #C8CDD5;color: #45535e;")
        header = TR(TD(), _style="background: #ACB5C5 -webkit-gradient(linear, left top,"
                                 " left bottom, from(#D0D8E1), to(#ACB5C5));")
        for role in roles:
            header.append(TD(LABEL(str.replace(role["role"].encode("utf-8"), "CPUser_", ""), _for=role["role"],
                                   _style="font-weight:bold;padding: 5px 5px 0 5px;"
                                          "margin-bottom:-7px;text-align: center;"),
                             INPUT(_type="checkbox", _id=role["role"], _name="roles", _value=role["id"],
                                   _checked='' if role["id"] in groups else None,
                                   _disabled='' if grid.view_form else None),
                             _style="text-align: center;width: 80px;"))
        div_permission.append(header)
        old_cat = None
        bg_odd = "background-color: #eff1f4;"
        bg_even = ""
        bg = bg_odd
        for function in functions:
            cat_tr = TR(TD(function["category"], _style="font-weight:bold;padding: 5px 5px 5px;"))
            if old_cat != function["category"]:
                bg = bg_odd if bg == bg_even else bg_even
                div_permission.append(cat_tr)
                old_cat = function["category"]
            cat_tr.attributes["_style"] = "%s" % bg
            cat_tr.append(TD(_colspan=len(roles)))

            tr = TR(TD(SPAN(function["name"], _style="margin-left: 20px;"),
                       _style="padding: 5px 5px 5px;"), _style="%s" % bg)
            for role in roles:
                if function["id"] in role["functions"]:
                    tr.append(TD(IMG(_src=URL('static', 'images/check_green.png')),
                                 _style="text-align:center;min-width: 50px;padding: 5px 0 5px;"))
                else:
                    tr.append(TD(IMG(_src=URL('static', 'images/check_grey.png')),
                                 _style="text-align:center;min-width: 50px;padding: 5px 0 5px;"))
            div_permission.append(tr)
        div_permission = TR(TD("Phân Quyền:"), TD(div_permission))

        if grid.view_form:
            grid.view_form.element('table').insert(len(grid.view_form.element('table')), div_permission)
        if grid.update_form:
            grid.update_form.element('table').insert(-2, div_permission)
        if grid.create_form:
            grid.create_form.element('table').insert(-1, div_permission)
    js = SCRIPT("""
        //alert('test');
        //alert('test');
    """)

    return dict(grid=grid+js)


def member_register_oncreate(user_form):
    roles = list()
    if request.vars["roles"]:
        if isinstance(request.vars["roles"], list):
            roles.extend(request.vars["roles"])
        else:
            roles.append(request.vars["roles"])
    for role in roles:
        auth.add_membership(role, user_form.vars.id)
    auth.add_membership(user_id=user_form.vars.id, role='CPUser')
    password = auth.random_password()
    crypt_pass = db.auth_user[auth.settings.password_field].validate(password)[0]
    db(db.auth_user.id == user_form.vars.id).update(password=crypt_pass, username=user_form.vars.email)
    message = """
    <html>
    <body>
        Chúc mừng %s đã trở thành CP member tại hệ thống classbook.<br>
        Bạn đã được đăng ký là thành viên dưới sự quản lý của tài khoản: %s<br>
        Bạn có thể đăng nhập với tài khoản:<br>
        Username: %s <br>
        Password: %s <br>
    </body>
    </html>
    """ % (user_form.vars.email, auth.user.username, user_form.vars.email, password)
    mail.send(user_form.vars.email, 'Đăng ký tài khoản CP member thành công!', message)


def member_register_onupdate(user_form):
    if user_form.vars.delete_this_record is None:
        roles = list()
        if request.vars["roles"]:
            if isinstance(request.vars["roles"], list):
                roles.extend(request.vars["roles"])
            else:
                roles.append(request.vars["roles"])
        groups = db(db.auth_membership.user_id == request.args[-1]).select(db.auth_membership.group_id)
        groups = [x.group_id for x in groups]
        for group in groups:
            if not group in roles:
                auth.del_membership(group, user_form.vars.id)
            else:
                roles.remove(group)
        for role in roles:
            auth.add_membership(role, user_form.vars.id)


# noinspection PyUnusedLocal
def member_register_ondelete(table, id):
    pass


def register_onaccept(form):
    from datetime import datetime
    db(db['auth_user'].id == form.vars.id).update(created_on=datetime.today(), username=form.vars.email)
    session.flash = "Chúng tôi đã gửi link xác thực vào địa chỉ email đăng ký của bạn!"


def verify_email_onaccept(user_data):
    from datetime import datetime
    if (datetime.today() - user_data.created_on).seconds > 60*60*24:
        db(db['auth_user'].id == user_data.id).delete()
        session.flash = "Key invalidate!"
        redirect(URL('index'))
    auth.add_membership(user_id=user_data.id, role=settings.cpadmin_group)
    if not osFileServer.exists(settings.cp_dir):
        osFileServer.makedir(settings.cp_dir)
    cp = osFileServer.opendir(settings.cp_dir)
    cp.makedir("CP%d" % user_data.id)
    cp.makedir("CP%d/upload" % user_data.id)
    cp.makedir("CP%d/review" % user_data.id)
    cp.makedir("CP%d/published" % user_data.id)
    mail.send(to=settings.email_admin, subject="Thông báo hệ thống!",
              message="""<html>Hệ thống có tài khoản %s đăng ký CP admin đang chờ được cấp phép.
              <br>Bạn hãy truy cập vào hệ thống để cấp phép cho tài khoản trên.</html>
              """ % user_data.username, )


def login_onaccept(form):
    import os
    from gluon.contrib import pbkdf2
    from datetime import datetime

    str_regenration = os.urandom(10)
    token = pbkdf2.pbkdf2_hex(form.vars.username, str_regenration)
    last_login = datetime.today()
    try:
        db(db[auth.table_user()].username == form.vars.username).update(token=token, last_login=last_login)
        auth.user.token = token
        auth.user.last_login = last_login
    except:
        import traceback
        traceback.print_exc()


def register_onvalidation(form):
    if len(form.vars.country) == 0:
        form.errors.country = 'Không được bỏ trống quốc gia'
    if len(form.vars.province) == 0:
        form.errors.province = 'Không được bỏ trống thành phố'


def index():
    """
    exposes:
    http://..../[app]/users/index/login
    http://..../[app]/users/index/logout
    http://..../[app]/users/index/register
    http://..../[app]/users/index/profile
    http://..../[app]/users/index/retrieve_password
    http://..../[app]/users/index/change_password
    http://..../[app]/users/index/manage_users (requires membership in
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    if len(request.args) > 0 and request.args[0] == 'register':
        if len(request.vars) == 0 and not session.accept_term:
            redirect(URL('term'))
        session.accept_term = None
    if "profile" in request.args:
        db.auth_user.email.writable = False
    db.auth_user.username.readable = False
    db.auth_user.username.writable = False
    auth.settings.register_onaccept = register_onaccept
    auth.settings.register_onvalidation = register_onvalidation
    auth.settings.verify_email_onaccept = verify_email_onaccept
    auth.settings.login_onaccept = login_onaccept
    return dict(form=auth())


def term():
    if 'accept' in request.vars:
        session.accept_term = True
        redirect(URL('index', args='register'))
    form = DIV()
    form.append(H3("Điều khoản sử dụng classbook store:"))
    form.append(DIV(XML('<b style="color: red;">Bạn cần chấp nhận điều khoản của chúng tôi để có thể đăng ký tài khoản!</b> <br/>'
                        '<div style="margin: 10px auto; width: 100%; height: 500px; overflow-y: scroll; border-top: 1px #888 dashed; padding: 10px; box-sizing: border-box;">'
                        '<h4 style="text-align:center;">ĐIỀU  KHOẢN DỊCH VỤ CỦA CLASSBOOK</h4>'
                        '<h5 style="margin-left: 20px;">Điều 1: Đăng kí tài khoản và đặt tên nội dung số</h5>'
                        '<p style="text-indent: 20px;">'
                        'Khi đăng ký tài khoản của các thành viên phải đồng ý cung cấp các thông tin một cách trung thực, đầy đủ và sẽ cập nhật các thông tin này khi có sự thay đổi trong thực tế. Nghiêm cấm việc thành viên cố tình cung cấp thông tin không chính xác về cá nhân, nhóm hoặc công ty khi đăng ký. Người đại diện cho tài khoản Nhà cung cấp có thể là một cá nhân, một tổ chức hay một công ty. Người đại diện phải có trách nhiệm bảo vệ thông tin đăng nhập của tài khoản để tránh việc người khác sử dụng trái phép và thông báo kịp thời tới Classbook về bất kỳ việc sử dụng trái phép nào.'
                        '<br/>Các thành viên tham gia hệ thống của Classbook được đặt tên tài khoản hoặc tên nội dung số theo sở thích của mình, loại trừ các trường hợp sau:'
                        '<ul>'
                        '<li> Sử dụng các từ ngữ gây phản cảm, trái thuần phong mỹ tục Việt Nam và các nước khác</li> '
                        '<li> Sử dụng tên các danh nhân Việt Nam, các lãnh đạo của cơ quan nhà nước Việt Nam</li> '
                        '<li> Sử dụng các tên trái với quy định Pháp luật Việt Nam</li> '
                        '</ul>'
                        '</p>'
                        '<h5 style="margin-left: 20px;">Điều 2: Đăng tải nội dung số lên hệ thống Classbook.vn</h5>'
                        '<p style="text-indent: 20px;">'
                        'Quy định về đăng tải nội dung số của Classbook áp dụng cho bất kỳ nội dung số bao gồm nhưng không giới hạn: Sách, ứng dụng và trắc nghiệm.'
                        '<br/>Các thành viên phải tự chịu toàn bộ trách nhiệm về những nội dung số do chính mình đã đăng tải lên Classbook.vn. Các trách nhiệm trên bao gồm nhưng không giới hạn các điều sau:'
                        '<ul>'
                        '<li>Không đăng tải các nội dung số khiêu dâm, đồi trụy, bạo lực…</li>'
                        '<li>Không đăng tải các loại nội dung số liên quan đến các vấn đề chính trị, tôn giáo, chủng tộc, và các quy định khác của Pháp luật.</li>'
                        '<li>Không vi phạm các quyền sở hữu trí tuệ của người khác, bao gồm cả thương hiệu bằng sáng chế, bí mật thương mại, quyền tác giả, quyền sở hữu khác.</li>'
                        '<li>Không đăng tải các nội dung số có chứa virus, phần mềm độc hại, phần mềm gián điệp hoặc bất kỳ phần mềm nào khác mà có thể gây tổn hại cho các thiết bị người dùng hoặc dữ liệu cá nhân.</li>'
                        '<li>Không đăng tải các nội dung số có thể gây tổn hại đến người khác hoặc làm tổn hại đến việc kinh doanh của Classbook, làm mất uy tín của Classbook.</li>'
                        '<li>Không đăng tải nội dung số lặp đi lặp lại.</li>'
                        '<li>Không đăng các thông tin nội dung khác không liên quan đến nội dung Sách điện tử Classbook</li>'
                        '</ul>'
                        '</p>'
                        '<h5 style="margin-left: 20px;">Điều 3: Tính cá nhân và bảo mật thông tin đăng kí</h5>'
                        '<p style="text-indent: 20px;">'
                        '<ul>'
                        '<li>Classbook không chia sẻ hoặc cung cấp các thông tin cá nhân của thành viên cho bên thứ ba mà không được phép. Ngoại trừ trường hợp, khi toàn án, viện kiểm sát, cảnh sát, cơ quan thuế, trung tâm bảo vệ người tiêu dùng, các cơ quan chức năng có thẩm quyền tương đương yêu cầu Classbook cung cấp thông tin cá nhân. Classbook sẽ cung cấp thông tin cá nhân của các thành viên với mục đích bảo vệ quyền lợi, thương hiệu của Classbook.</li>'
                        '<li>Classbook có thể gửi thư điện tử với mục đích thông báo, tuyên truyền quảng cáo, cung cấp thông tin theo địa chỉ email các thành viên đã đăng ký. Nếu các thành viên không muốn nhận thư, có thể thông báo cho Classbook, Classbook sẽ ngừng cung cấp thông tin qua thư điện tử.</li>'
                        '</ul>'
                        '</p>'
                        '<h5 style="margin-left: 20px;">Điều 4: Thay đổi thông tin đăng ký</h5>'
                        '<p style="text-indent: 20px;">'
                        'Sau khi đăng ký tài khoản, thành viên có thể thay đổi thông tin đã đăng ký. Classbook cho phép thành viên sửa đổi các thông tin tài khoản bao gồm: Họ tên, mật khẩu, tài khoản ngân hàng, số điện thoại, địa chỉ (Người dùng không thể thay thế địa chỉ email đã đăng ký). Classbook không chịu bất kỳ trách nhiệm gì về những phát sinh liên quan đến việc thay đổi thông tin của thành viên.'
                        '</p>'
                        '<h5 style="margin-left: 20px;">Điều 5: Sử dụng dịch vụ</h5>'
                        '<p style="text-indent: 20px;">'
                        '<ul>'
                        '<li>Các thành viên khi sử dụng dịch vụ phải tuân thủ các quy định và các hướng dẫn của Classbook</li>'
                        '<li>Trong trường hợp Classbook tiến hành bảo trì, nâng cấp hệ thống để nâng cấp dịch vụ, tiến hành bảo mật thông tin, hệ thống bị quá tải, và những trường hợp khác mang tính khách quan gây ảnh hưởng đến hệ thống, Classbook có thể dừng một phần hoặc toàn bộ dịch vụ, và sẽ không chịu trách nhiệm về tổn thất phát sinh do việc dừng cung cấp với lý do trên gây ra.</li>'
                        '</ul>'
                        '</p>'
                        '<h5 style="margin-left: 20px;">Điều 6: Thay đổi quy định</h5>'
                        '<p style="text-indent: 20px;">'
                        'Classbook có thể thay đổi những quy định về Điều khoản dịch vụ mà không cần báo trước. Khi có thay đổi, Classbook sẽ đăng tải lên Classbook.vn, và sau khi đăng lên coi như quy định đó có hiệu lực. Sau khi quy định thay đổi, nếu thành viên sử dụng Classbook.vn thì Classbook coi thành viên đã chấp nhận tất cả các quy định mới. Bạn có trách nhiệm theo dõi thường xuyên các thông tin được Classbook cung cấp để cập nhật những thay đổi mới nhất.'
                        '</p>'
                        '<h5 style="margin-left: 20px;">Điều 7: Cấm, hủy bỏ tư cách sử dụng của thành viên</h5>'
                        '<p style="text-indent: 20px;">'
                        'Trong trường hợp Classbook xác nhận được thành viên vi phạm các khoản tại Điều 1 và Điều 2, Classbook có thể xóa nội dung số vi phạm hoặc ngừng, hủy bỏ tài khoản của thành viên đó, và Classbook không chịu trách nhiệm về những tổn hại phát sinh do việc ngừng hoặc hủy bỏ như trên gây ra. Trong trường hợp thành viên gây tổn hại đến lợi ích của Classbook hoặc người thứ ba thì thành viên vi phạm phải có trách nhiệm bồi thường những tổn hại đó.'
                        '</p>'
                        '<h5 style="margin-left: 20px;">Điều 8: Giải quyết tranh chấp, luật áp dụng</h5>'
                        '<p style="text-indent: 20px;">'
                        'Trong quá trình sử dụng nếu xảy ra tranh chấp giữa thành viên và Classbook, hai bên sẽ tiến hành đàm phán hòa giải với tinh thần hữu nghị. Trong trường hợp không giải quyết được bằng hòa giải sẽ đưa ra tòa án kinh tế Hà Nội hoặc những cơ quan có thẩm quyền giải quyết.'
                        '</p>'
                        '<br/>'
                        '<h5>Mọi ý kiến phản hồi liên quan đến Điều khoản dịch vụ, bạn vui lòng liên hệ:</h5>'
                        '<p>'
                        '<b>NHÀ XUẤT BẢN GIÁO DỤC VIỆT NAM – CÔNG TY CỔ PHẦN SÁCH ĐIỆN TỬ GIÁO DỤC EDC</b>'
                        '<br/>Trụ sở chính: 187B Giảng Võ, Đống Đa, Hà Nội'
                        '<br/>(+84) - 902138004'
                        '<br/>Fax: (+84-4)-35124007'
                        '<br/>Miền Nam: 210/8 Hồ Văn Huê, P.9, Q. Phú Nhuận, Hồ Chí Minh'
                        '<br/>Hotline: (+84-8)-38476284'
                        '<br/>Email: info@edcom.vn'
                        '</p>'
                        '</div>'),
                    _style='width:98%;border: gray 1px solid;padding: 10px 10px 10px 10px;margin-bottom:10px'))
    form.append(FORM(INPUT(_value='Hủy bỏ', _type='button', _onclick='window.location="%s"' % URL('index')),
                     INPUT(_name="accept", _type='hidden'),
                     INPUT(_value='Đồng ý', _type='submit'), _action=URL(),
                     _style='text-align:right'))
    form.append(BR())
    return dict(form=form)