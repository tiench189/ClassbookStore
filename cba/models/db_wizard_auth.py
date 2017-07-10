# -*- coding: utf-8 -*-
""" Định nghĩa database phục vụ cho phân quyền """
__author__ = 'manhtd'

#########################################
db.define_table('auth20_function_category',
                Field('name', type='string', notnull=True, label=T('Category Name')),
                Field('category_order', type='integer', notnull=True, default=0, label=T('Category Order')),
                Field('description', type='text', label=T('Function Description')),
                auth.signature, format='%(name)s')

db.define_table('auth20_function',
                Field('name', type='string', notnull=True, label=T('Function Name')),
                Field('category', type='reference auth20_function_category', label=T('Function Category')),
                Field('aname', type='string', notnull=True, label=T('Application Name')),
                Field('cname', type='string', notnull=True, label=T('Controller Name')),
                Field('fname', type='string', notnull=True, default='index', label=T('Function Name')),
                Field('args', type='list:string', notnull=True, label=T('Function Agruments')),
                Field('vars', type='list:string', notnull=True, label=T('Function Variables')),
                Field('description', type='text', label=T('Function Description')),
                auth.signature, format='%(name)s')

#########################################
db.define_table('auth20_action',
                Field('name', type='string', notnull=True, unique=True, label=T('Action Name')),
                Field('description', type='text', label=T('Action Description')),
                auth.signature, format='%(name)s')

#########################################
db.define_table('auth20_data',
                Field('name', type='string', notnull=True, unique=True, label=T('Data Name')),
                Field('table_name', type='string', notnull=True, label=T('Table Data')),
                Field('data_condition', type='string', notnull=True, default='id>0', label=T('Data Condition')),
                auth.signature, format='%(name)s')

#########################################
db.define_table('auth20_permission',
                Field('group_id', type='reference auth_group', label=T('Auth Group')),
                Field('actions', type='list:reference auth20_action', label=T('Auth Actions'),
                      requires=IS_IN_DB(db, 'auth20_action.id', '%(name)s', multiple=(1, 10000), sort=True)),
                Field('functions', type='list:reference auth20_function', label=T('Auth Functions'),
                      requires=IS_IN_DB(db, 'auth20_function.id',
                                        lambda r: '%s > %s > %s' % (r.aname, r.category.name, r.name),
                                        multiple=(1, 10000), sort=True)),
                Field('data_id', type='reference auth20_data', label=T('Auth Data'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'auth20_data.id', '%(id)s'))),
                auth.signature)


def find_element_in_list(element, list_element):
    try:
        index_element = list_element.index(element)
        return index_element
    except ValueError:
        return -1


def __authorize(application=None, controller=None, function=None, action_mode=None):
#action_mode for new authorize permission and remove check with request.args
    if application is None:
        application = request.application
    if controller is None:
        controller = request.controller
    if function is None:
        function = request.function

    def decorate(action):
        def f(*a, **b):
            if auth.user:
                permissions = list()
                for group_id in auth.user_groups.keys():
                    query = db(db.auth20_permission.group_id == group_id)
                    query = query(db.auth20_permission.functions.contains(db.auth20_function.id))
                    query = query(db.auth20_function.aname == application)
                    query = query(db.auth20_function.cname == controller)
                    query = query(db.auth20_function.fname == function)
                    query = query(db.auth20_permission.actions.contains(db.auth20_action.id))
                    roles = query(db.auth20_action.name == 'View').select(db.auth20_permission.actions,
                                                                          db.auth20_permission.data_id)

                    #Group from database and action from request.args
                    write_group = ['edit', 'write', 'new', 'upload', 'publish', 'submit']
                    relation_group = ['relation']
                    read_group = ['read', 'view', 'review']
                    delete_group = ['delete']
                    write_action = ['edit', 'new']
                    read_action = ['view']
                    delete_action = ['delete']

                    if len(roles) > 0:
                        for role in roles:
                            actions = db(db.auth20_action.id.belongs(role.actions))
                            actions = actions.select(db.auth20_action.name).as_list()
                            data = db(db.auth20_data.id == role.data_id).select(db.auth20_data.table_name,
                                                                                db.auth20_data.data_condition).as_list()

                            #get request.args[0] or request.args[2] for action/ default and modify mode
                            check_action = list()
                            for action_one in actions:
                                if action_mode is not None:
                                    if action_one['name'] == action_mode:
                                        check_action.append(action_one)
                                elif (len(request.args) <= 0) and (action_one['name'] == "View")\
                                    or (len(request.args) == 1
                                        and find_element_in_list(request.args[0], write_action) == -1
                                        and find_element_in_list(request.args[0], read_action) == -1
                                        and find_element_in_list(request.args[0], delete_action) == -1)\
                                    or ((len(request.args) >= 1)
                                        and ((find_element_in_list(action_one['name'].lower(), write_group) != -1
                                              and find_element_in_list(request.args[0].lower(), write_action) != -1)
                                             or (find_element_in_list(action_one['name'].lower(), read_group) != -1
                                                 and find_element_in_list(request.args[0].lower(), read_action) != -1)
                                             or (find_element_in_list(action_one['name'].lower(), delete_group) != -1
                                                 and find_element_in_list(request.args[0].lower(), delete_action) != -1)
                                            )
                                        )\
                                    or ((len(request.args) >= 2)
                                        and ((find_element_in_list(action_one['name'].lower(), write_group) != -1
                                              and find_element_in_list(request.args[1].lower(), write_action) != -1)
                                             or (find_element_in_list(action_one['name'].lower(), read_group) != -1
                                                 and find_element_in_list(request.args[1].lower(), read_action) != -1)
                                             or (find_element_in_list(action_one['name'].lower(), delete_group) != -1
                                                 and find_element_in_list(request.args[1].lower(), write_action) != -1)
                                             or (find_element_in_list(action_one['name'].lower(), relation_group) != -1
                                                 and str.find(request.args[1].lower(), ".") > 0)
                                            )
                                        ):
                                        check_action.append(action_one)
                            if len(check_action) > 0:
                                permissions.append(dict(actions=actions, data=data))

                if len(permissions) > 0:
                    auth.user.permissions = permissions
                    return action(*a, **b)
            if request.is_restful:
                raise HTTP(401)
            else:
                session.flash = "You don't have permission to access!"
                redirect(URL(c='default', f='index'))
        f.__doc__ = action.__doc__
        f.__name__ = action.__name__
        f.__dict__.update(action.__dict__)
        return f
    return decorate
auth.requires_authorize = __authorize


def __authorize_token(pos=0, total=1):
    def decorate(action):
        def f(*a, **b):
            messages = Storage()
            messages.token_invalid = "Token is invalid!"
            messages.token_expired = "Token is expired!"
            messages.parameter_invalid = "Parameters are invalid!"
            messages.error = "Error occur!"

            if len(a) != total or pos >= total:
                return dict(result=False, reason=0, message=messages.parameter_invalid)

            from datetime import datetime
            cur_time = datetime.today()
            token = a[pos]
            try:
                query = db(db.auth_user.token == token)
                user = query.select(db.auth_user.last_login, db.auth_user.id)
                if len(user) == 0:
                    return dict(result=False, reason=1, message=messages.token_invalid)
                elif (cur_time - user.first().last_login).total_seconds() > auth.settings.expiration:
                    return dict(result=False, reason=2, message=messages.token_expired)
                a = [(x if not i == pos else user.first().id) for i, x in enumerate(a)]
                db(db.auth_user.token == token).update(last_login=cur_time)
            except:
                import traceback
                traceback.print_exc()
                return dict(result=False, reason=-1, message=messages.error)
            return action(*a, **b)
        f.__doc__ = action.__doc__
        f.__name__ = action.__name__
        f.__dict__.update(action.__dict__)
        return f
    return decorate
auth.requires_token = __authorize_token

#auth.enable_record_versioning(db)
