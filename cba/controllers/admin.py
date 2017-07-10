# coding=utf-8
def call():
    session.forget()
    return service()


@auth.requires_login()
@auth.requires_authorize()
def index():
    def get_role(user):
        user_id = user.id
        roles = db(db.auth_membership.user_id == user_id)
        roles = roles(db.auth_group.id == db.auth_membership.group_id)
        roles = roles.select(db.auth_group.role)
        return ', '.join([x.role for x in roles])
    query = db(db.auth_group.role.startswith('CP'))
    query = query(db.auth_membership.group_id == db.auth_group.id)
    query = query(db.auth_user.id == db.auth_membership.user_id)
    filter_users = query.select(db.auth_user.id, groupby=db.auth_user.id)
    filter_users = [x.id for x in filter_users]

    constraints = {str(db.auth_user): (~db.auth_user.id.belongs(filter_users))}
    links = [{'header': A('Membership', _href=URL(c='membership', f='index')),
              'body': lambda row_data: SPAN(get_role(row_data))}]
    grid = SQLFORM.smartgrid(db.auth_user, constraints=constraints, oncreate=admin_on_create,
                             onupdate=admin_on_update, ondelete=admin_on_delete,
                             showbuttontext=False, linked_tables=[], links=links)
    return dict(grid=grid)


def admin_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')


def admin_on_update(form):
    table = request.args[-2]
    record_id = form.vars.id
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')


def admin_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


@service.jsonrpc
@auth.requires_token(3, 4)
def check_permission(a, c, f, user_id):
    permissions = list()
    query = db(db.auth_membership.user_id == user_id)
    groups = query.select(db.auth_membership.group_id)
    for group in groups:
        query = db(db.auth20_permission.group_id == group.group_id)
        query = query(db.auth20_permission.functions.contains(db.auth20_function.id))
        query = query(db.auth20_function.aname == a)
        query = query(db.auth20_function.cname == c)
        query = query(db.auth20_function.fname == f)
        query = query(db.auth20_permission.actions.contains(db.auth20_action.id))
        roles = query(db.auth20_action.name == 'View').select(db.auth20_permission.actions,
                                                              db.auth20_permission.data_id)
        for role in roles:
            actions = db(db.auth20_action.id.belongs(role.actions)).select(db.auth20_action.name).as_list()
            data = db(db.auth20_data.id == role.data_id).select(db.auth20_data.table_name,
                                                                db.auth20_data.data_condition).as_list()
            permissions.append(dict(actions=actions, data=data))
    if len(permissions) > 0:
        return dict(result=True, permissions=permissions)
    return dict(result=False, reason=2, message="You don't have permission to access!")


@service.jsonrpc
def authorize(username, password):
    username = username.encode('utf-8')
    password = password.encode('utf-8')
    user = auth.login_bare(username, password)
    if not user:
        return dict(error=dict(code=401, message='Authorize failed!'))
    else:
        import os
        from gluon.contrib import pbkdf2
        from datetime import datetime

        str_regenration = os.urandom(10)
        token = pbkdf2.pbkdf2_hex(username, str_regenration)
        try:
            db(db[auth.table_user()].username == username).update(token=token, last_login=datetime.today())
        except:
            import traceback
            traceback.print_exc()
            return dict(error=dict(code=500, message='Database error!'))
        return dict(token=token)


@service.jsonrpc
def get_cp_roles(application):
    query = db(db.auth_group.role.like("CPUser_%"))
    groups = query.select(db.auth_group.id, db.auth_group.role).as_list()
    for group in groups:
        query = db(db.auth20_permission.group_id == group["id"])
        query = query(db.auth20_permission.functions.contains(db.auth20_function.id))
        query = query(db.auth20_function.aname == application)
        query = query(db.auth20_permission.actions.contains(db.auth20_action.id))
        query = query(db.auth20_action.name == "View")
        functions = query.select(db.auth20_permission.functions)
        function = list()
        for f in functions:
            function.extend(f.functions)
        group["functions"] = list(set(function))

    permissions = list()
    query = db(db.auth20_permission.group_id == auth.id_group("CPAdmin"))
    query = query(db.auth20_permission.actions.contains(db.auth20_action.id))
    roles = query(db.auth20_action.name == 'View').select(db.auth20_permission.functions)
    for role in roles:
        permissions.extend(role.functions)
    permissions = set(permissions)

    query = db(db.auth20_function.id.belongs(permissions))
    query = query(db.auth20_function.aname == application)
    query = query(db.auth20_function_category.id == db.auth20_function.category)
    res = query.select(db.auth20_function.id, db.auth20_function.name,
                       db.auth20_function_category.name, orderby=db.auth20_function_category.name)
    functions = [{"id": x["auth20_function"]["id"],
                  "name": x["auth20_function"]["name"],
                  "category": x["auth20_function_category"]["name"]} for x in res]
    return dict(result=dict(groups=groups, functions=functions))
