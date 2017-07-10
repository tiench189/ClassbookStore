# -*- coding: utf-8 -*-
""" Định nghĩa databases cho Classbook library"""
__author__ = 'Tien'


########################################
db.define_table('clsblib_category',
                Field('category_name', type='string', notnull=True,
                      label=T('Catagory Name')),
                Field('category_code', type='string', notnull=True, unique=True,
                      label=T('Category Code')),
                Field('category_type', type='reference clsb_product_type', notnull=True, default=1,
                      label=T('Category Type')),
                Field('category_order', type='integer', notnull=True, default=9999,
                      label=T('Order')),
                Field('category_parent', type='reference clsb_category', label='Category Parent',
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsblib_category.id', '%(category_name)s'))),
                auth.signature,
                format='%(category_name)s')
db.clsblib_category._singular = 'Category'
db.clsblib_category._plural = 'Categories'


db.define_table('clsblib_category_product',
                Field('category_code', type='string', notnull=True,
                      label=T('Catagory ID')),
                Field('product_id', type='integer', notnull=True,
                      label=T('Product ID')),
                Field('description', type='string',
                      label=T('Description')),
                auth.signature)
db.clsblib_category_product._singular = 'Product Category'
db.clsblib_category_product._plural = 'Product Categories'


db.define_table('clsblib_subscription_log',
                Field('user_id', type='integer', notnull=True,
                      label=T('User ID')),
                Field('start_time', type='datetime',
                      label=T('Start')),
                Field('end_time', type='datetime',
                      label=T('End')),
                Field('subscription_type', type='string',
                      label=T('Sub Type')),
                Field('description', type='string',
                      label=T('Description')),
                auth.signature)
db.clsblib_subscription_log._singular = 'clsblib_subscription_log'
db.clsblib_subscription_log._plural = 'clsblib_subscription_log'


db.define_table('clsblib_subscription_status',
                Field('user_id', type='integer', notnull=True,
                      label=T('User ID')),
                Field('start_time', type='datetime',
                      label=T('Start')),
                Field('end_time', type='datetime',
                      label=T('End')),
                Field('subscription_type', type='string',
                      label=T('Sub Type')),
                Field('description', type='string',
                      label=T('Description')),
                auth.signature)
db.clsblib_subscription_status._singular = 'clsblib_subscription_status'
db.clsblib_subscription_status._plural = 'clsblib_subscription_status'