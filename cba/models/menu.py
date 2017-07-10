# -*- coding: utf-8 -*-
def render_menu():
    menu = list()
    menu.append(['Homepage', URL('default', 'index') == URL(), URL('default', 'index')])
    if not auth.user:
        return menu

    categories = db(db.auth20_function_category.id > 0).select(db.auth20_function_category.id,
                                                               db.auth20_function_category.name,
                                                               orderby=db.auth20_function_category.category_order)
    query = db(db.auth_membership.user_id == auth.user.id)
    query = query(db.auth20_permission.group_id == db.auth_membership.group_id)
    query = query.select(db.auth20_permission.functions)
    permissions = list()
    for q in query:
        permissions.extend(q.functions)
    for category in categories:
        functions = db(db.auth20_function.category == category.id)
        functions = functions(db.auth20_function.id.belongs(permissions))
        functions = functions(db.auth20_function.aname == request.application)
        functions = functions.select(db.auth20_function.name, db.auth20_function.aname,
                                     db.auth20_function.cname, db.auth20_function.fname,
                                     orderby=db.auth20_function.name)
        if len(functions) > 0:
            sub_menu = list()
            for function in functions:
                url = URL(a=function.aname, c=function.cname, f=function.fname)
                sub_menu.append([function.name, url == URL(), url])
            menu.append([category.name, False, None, sub_menu])
    return menu

response.title = settings.title
response.subtitle = settings.subtitle
response.meta.author = '%(author)s <%(author_email)s>' % settings
response.meta.keywords = settings.keywords
response.meta.description = settings.description
response.menu = render_menu()
