# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Name:        db_wizard_auth
#
# Purpose:     
#
# Version:     1.1
#
# Author:      manhtd
#
# Created:     1/14/14
# Updated:     1/14/14
#
# Copyright:   (c) Tinh Vân Books
#
# Todo: 
#-----------------------------------------------------------------------------
"""

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
#auth.enable_record_versioning(db)
