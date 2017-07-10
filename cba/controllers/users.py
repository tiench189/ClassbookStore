#@author: hant 27-02-2013

################ Admin's functions ##################
#import cbMsg
SUCCESS = CB_0000#cbMsg.CB_0000
LACK_ARGS = CB_0002#cbMsg.CB_0002
DB_RQ_FAILD = CB_0003#cbMsg.CB_0003
import usercp
myTable = db.clsb_user

def index():
    pageName = "Users Management page."
    resultat = ""
    if request.vars.search:
        users_tbl = selectUserByUsername()
        if not users_tbl:
            users_tbl = getAllUsersSortByUsername()
    elif request.vars.delete:
        deleteMultipleRow()
        response.flash = SUCCESS
        users_tbl = getAllUsersSortByUsername()
    else:
        users_tbl = getAllUsersSortByUsername()
    
    return dict(message=pageName, users = users_tbl, resultat=resultat)

def deleteMultipleRow(): # by username
    if request.vars and len(request.vars)>1:
        rows = request.vars.pop("delete")
        for user in request.vars:
            db(myTable.username == request.vars[user]).delete()
        return SUCCESS
    else:
        return LACK_ARGS
      
def getAllUsersSortByUsername():
    users_tbl = db().select(myTable.ALL, orderby=myTable.username)
    #return dict(users = users_tbl)
    return users_tbl

  
def deleteRow(): # by username
    if request.vars.selectedRow:
        db(myTable.username == request.vars.selectedRow).delete()
        response.flash = SUCCESS
    else:
        response.flash = LACK_ARGS

    
def selectByUsername():
    if request.vars and len(request.vars) == 1:
        userSeleted = db(myTable.username.like(request.vars.search)).select() 
        return userSeleted
    else:
        return userSeleted


@auth.requires_authorize()
def discount_value():
    if request.url.find('discount_value/new') >= 0:
        users = db(db.auth_user.id == db.auth_membership.user_id)\
                (~db.auth_user.id.belongs(db(db.clsb20_discount_cp)._select(db.clsb20_discount_cp.user_id)))\
                (db.auth_group.role.like("CPAdmin"))\
                (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)
        form = FORM(
            A("Quay lại", _href=URL(), _class="btn"),
            TABLE(
                TR(
                    TD(B("Chọn CP Admin")),
                    TD(SELECT(*[OPTION(use['auth_user']['username'], _value=use['auth_user']['id']) for use in users], _name="cp_admin", _class="selectpicker", _title="Lựa chọn", requires=IS_NOT_EMPTY()))
                ),
                TR(
                    TD(B("Giá trị chiết khấu")),
                    TD(INPUT(_placeholder="Chiết khấu", _name="value_discount", _value="30"))
                ),
                TR(
                    TD(),
                    TD(INPUT(_value="Thêm mới", _type="submit", _class="btn"))
                )
            ),
            SCRIPT('$(".selectpicker").attr("data-live-search", true);$(".selectpicker").selectpicker()')
        )
        if form.accepts(request, session):
            try:
                cp_admin = request.vars['cp_admin']
                value_discount = request.vars['value_discount']
                db.clsb20_discount_cp.insert(user_id=cp_admin, value_discount=value_discount)
                session.flash = "Thành công!!!"
                return redirect(URL(a='cba', c='users', f='discount_value'))
            except Exception as e:
                response.flash = "Lỗi !!!"
        if form.errors:
            response.flash = "Lỗi !!!"
        return dict(form=form)
    elif request.url.find('discount_value/edit') >= 0:
        data = db(db.clsb20_discount_cp.id == int(request.args[1]))(db.clsb20_discount_cp.user_id == db.auth_user.id).select().first()
        form = FORM(
            A("Quay lại", _href=URL(), _class="btn"),
            TABLE(
                TR(
                    TD(B("CP Admin")),
                    TD(INPUT(_value=data['auth_user']['username'], _disabled=True))
                ),
                TR(
                    TD(B("Giá trị chiết khấu")),
                    TD(INPUT(_placeholder="Chiết khấu", _name="value_discount", _value=data['clsb20_discount_cp']['value_discount']))
                ),
                TR(
                    TD(),
                    TD(INPUT(_value="Thay đổi", _type="submit", _class="btn"))
                )
            ),
        )
        if form.accepts(request, session):
            try:
                value_discount = request.vars['value_discount']
                db(db.clsb20_discount_cp.id == int(request.args[1])).update(value_discount=value_discount)
                session.flash = "Thành công!!!"
                return redirect(URL(a='cba', c='users', f='discount_value'))
            except Exception as e:
                response.flash = "Lỗi !!!"
        if form.errors:
            response.flash = "Lỗi !!!"
        return dict(form=form)
    elif request.url.find('discount_value/delete') >= 0:
        print request.args[1]
        db(db.clsb20_discount_cp.id == int(request.args[1])).delete()
        session.flash = "Thành công"
        return "OK"
    data = db(db.clsb20_discount_cp.user_id == db.auth_user.id)(db.auth_user.is_active == True)(db.auth_user.id == db.auth_membership.user_id)\
        (db.auth_group.role.like("CPAdmin"))(db.auth_membership.group_id == db.auth_group.id).select()
    form = DIV(
        A("Thêm mới", _class="btn", _href=URL(a='cba', c='users', f='discount_value', args=['new'])),
        TABLE(
            THEAD(
                TR(
                    TH("Tài khoản CP Admin"),
                    TH("Chiết khấu"),
                    TH("Doanh thu"),
                    TH("Quản lý")
                )
            ),
            *[TR(
                TD(tmp['auth_user']['username']),
                TD(str(tmp['clsb20_discount_cp']['value_discount'])+"%"),
                TD(A("Xem chi tiết", _href=URL(a='cba', c='reports', f='index', vars=dict(select=tmp['auth_user']['id'])))),
                TD(A("Sửa", _href=URL(a='cba', c='users', f='discount_value', args=['edit', tmp['clsb20_discount_cp']['id']])), A("Xóa", _style="margin-left: 10px;", _href="",_onclick="javascript:submit_c('Bạn có muốn xóa với CP này?','"+URL(a='cba', c='users', f='discount_value', args=['delete', tmp['clsb20_discount_cp']['id']])+"')"))
            ) for tmp in data],
            _class="tablesorter web2py_grid"
        )
    )
    return dict(form=form)


@auth.requires_authorize()
def moveproduct():
    try:
        if 'u1' in request.vars and 'u2' in request.vars:
            user1 = db(db.clsb_user.username == request.vars.u1).select()
            if len(user1) == 0:
                return dict(result=False, mess="Tài khoản '" + request.vars.u1 + "' không tồn tại")
            uid1 = user1.first()['id']
            user2 = db(db.clsb_user.username == request.vars.u2).select()
            if len(user2) == 0:
                return dict(result=False, mess="Tài khoản '" + request.vars.u2 + "' không tồn tại")
            uid2 = user2.first()['id']
            db(db.clsb_download_archieve.user_id == uid1).update(user_id=uid2)
            db(db.clsb30_product_history.user_id == uid1).update(user_id=uid2)
            db(db.clsb30_media_history.user_id == uid1).update(user_id=uid2)
            return dict(result=True, mess="Thành công!")
        return dict(result=True, mess="")
    except Exception as ex:
        return dict(mess=str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno), result=False)