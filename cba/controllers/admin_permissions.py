# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Name:        roles
#
# Purpose:     manager roles of group
#
# Version:     1.1
#
# Author:      manhtd
#
# Created:     12/10/13
# Updated:     12/10/13
#
# Copyright:   (c) Tinh Vân Books
#
# Todo:        list, view, edit, delete role
#-----------------------------------------------------------------------------
"""
__table_permission__ = "auth20_permission"
__table_action__ = "auth20_action"
__table_function__ = "auth20_function"
__table_function_category__ = "auth20_function_category"


def get_list_function(row):
    query = db(db[__table_function__].id.belongs(row.functions))
    query = query(db[__table_function_category__].id == db[__table_function__].category)
    rows = query.select(db[__table_function__].aname, db[__table_function_category__].name,
                        db[__table_function__].name, orderby=(db[__table_function__].aname,
                                                              db[__table_function_category__].name,
                                                              db[__table_function__].name))

    res = DIV(_style='margin-left:10px;%s' % ('max-height:140px; overflow-y:auto;' if len(rows) > 7 else ''))
    for row in rows:
        res.append(DIV("%s > %s > %s" % (row[__table_function__].aname,
                                         row[__table_function_category__].name, row[__table_function__].name)))
    return res


def get_list_action(row):
    query = db(db[__table_action__].id.belongs(row.actions))
    rows = query.select(db[__table_action__].name, orderby=db[__table_action__].name)

    res = DIV(_style='margin-left:10px;%s' % ('max-height:140px; overflow-y:auto;' if len(rows) > 7 else ''))
    for row in rows:
        res.append(DIV(row.name))
    return res


@auth.requires_login()
@auth.requires_authorize()
def index():
    actions = Storage(list=0, view=1, edit=2, new=3)
    action = actions.list
    if len(request.args) > 1:
        if request.args[1] == 'edit':
            action = actions.edit
        elif request.args[1] == 'view':
            action = actions.view
        elif request.args[1] == 'new':
            action = actions.new
    fields = None
    links = None
    if action == actions.list:
        db[__table_permission__].functions.readable = False
        db[__table_permission__].actions.readable = False
        links = [{'header': A('Auth Actions', _href=URL(c='admin_actions')),
                  'body': lambda row_data: get_list_action(row_data)},
                 {'header': A('Auth Functions', _href=URL(c='admin_functions')),
                  'body': lambda row_data: get_list_function(row_data)}]
    elif action == actions.view:
        db[__table_permission__].functions.readable = False
        db[__table_permission__].actions.readable = False
    form = SQLFORM.smartgrid(db[__table_permission__], constraints=None, linked_tables=[],
                             links=links, links_in_grid=True, args=None, paginate=50,
                             csv=False, showbuttontext=False, fields=fields)
    if action == actions.view:
        query = db(db[__table_permission__].id == request.args[-1])
        row = query.select(db[__table_permission__].id, db[__table_permission__].functions,
                           db[__table_permission__].actions, db[__table_permission__].data_id).first()
        table = form.element("table")
        table.append(TR(TD("Auth Actions"), TD(get_list_action(row))))
        table.append(TR(TD("Auth Functions"), TD(get_list_function(row))))
    elif action == actions.edit or action == actions.new:
        select_tags = form.elements('select[name=functions],select[name=actions]')
        for select in select_tags:
            select.attributes['_size'] = 7
            select.attributes['_style'] = "width: auto;"
    return dict(form=(STYLE(".web2py_grid td { vertical-align: top !important;}") + form))