# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Name:        admin_functions
#
# Purpose:     
#
# Version:     1.1
#
# Author:      manhtd
#
# Created:     12/13/13
# Updated:     12/13/13
#
# Copyright:   (c) Tinh Vân Books
#
# Todo: 
#-----------------------------------------------------------------------------
"""
__table__ = "auth20_function"


@auth.requires_login()
@auth.requires_authorize()
def index():
    # actions = Storage(list=0, view=1, edit=2)
    # action = actions.list
    # if len(request.args) > 1:
    #     if request.args[1] == 'edit':
    #         action = actions.edit
    #     elif request.args[1] == 'view':
    #         action = actions.view
    fields = None
    links = None
    form = SQLFORM.smartgrid(db[__table__], constraints=None, linked_tables=[],
                             links=links, links_in_grid=True, args=None, paginate=50,
                             csv=False, showbuttontext=False, fields=fields)
    return dict(form=form)
