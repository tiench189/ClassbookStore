# -*- coding: utf-8 -*-
""" Định nghĩa databases cho store 3.0 """
__author__ = 'manhtd'

#########################################
db.define_table('clsb30_product_history',
                Field('product_title', type='string', notnull=True, label=T('Product Title')),
                Field('product_price', type='integer', default=0, label=T('Product Price')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product')),
                Field('category_id', type='reference clsb_category', notnull=True, label=T('Category')),
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                auth.signature, format='%(product_title)s')
db.clsb20_dic_creator_cp._singular = 'Product History'
db.clsb20_dic_creator_cp._plural = 'Product Histories'


#########################################
db.define_table('clsb30_category_classbook_device',
                Field('product_category', type='reference clsb_category', notnull=True, label=T('Product category')),
                Field('per_value', type='integer', default=0, label=T('Per for free')),
                Field('description', type='string', label=T('Description')),
                auth.signature, format='%(product_category)s')
db.clsb20_dic_creator_cp._singular = 'Product Category Free'
db.clsb20_dic_creator_cp._plural = 'Product Categories Free'


db.define_table('clsb30_set_purchase',
                Field('set_code', type='string', label=T('Set code'), notnull=True),
                Field('set_name', type='string', label=T('Set name'), notnull=True),
                Field('description', type='string', label=T('Description')),
                auth.signature, format='%(set_name)s')
db.clsb30_set_purchase._singular = "Set purchase"
db.clsb30_set_purchase._plural = "Sets purchase"

db.define_table('clsb30_set_purchase_product',
                Field('set_purchase_id', type='reference clsb30_set_purchase',notnull=True, label=T('Set purchase id')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product id')),
                auth.signature, format='%(id)s'
                )
db.clsb30_set_purchase_product._singular = "Set purchase product"
db.clsb30_set_purchase_product._plural = "Sets purchase product"


db.define_table('clsb30_set_product',
                Field('set_purchase_id', type='reference clsb30_set_purchase',notnull=True, label=T('Set purchase id')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product id')),
                auth.signature, format='%(id)s'
                )
db.clsb30_set_product._singular = "Set product"
db.clsb30_set_product._plural = "Sets product"

#####################################################################
db.define_table('clsb30_media_history',
                Field('product_title', type='string', notnull=True, label=T('Product Title')),
                Field('product_price', type='integer', default=0, label=T('Product Price')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product')),
                Field('category_id', type='reference clsb_category', notnull=True, label=T('Category')),
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                auth.signature, format='%(product_title)s')
db.clsb20_dic_creator_cp._singular = 'Product History'
db.clsb20_dic_creator_cp._plural = 'Product Histories'

################## apns ###############################
db.define_table('clsb30_apns',
                Field('user_email', type='string', notnull=True, label=T('User Email')),
                Field('apns_token', type='string', notnull=True, label=T('APNS Token')),
                Field('date_created', type='datetime', notnull=True, label=T('Date Created')),
                Field('date_modify', type='datetime', notnull=True, label=T('Date Modify')),
                Field('description', type='string', default="", label=T('Description')),
                auth.signature)
################## apns ###############################
db.define_table('clsb30_direct',
                Field('product_code', type='string', notnull=True, label=T('Code')),
                Field('download_time', type='datetime', notnull=True, label=T('Download Time')),
                Field('des', type='string', notnull=False, label=T('Description')),
                auth.signature)

db.define_table('clsb30_data_extend',
                Field('name', type='string', notnull=True, label=T('Name')),
                Field('data_type', type='string', notnull=False, label=T('Type')),
                Field('description', type='string', notnull=False, label=T('Description')),
                auth.signature)

db.define_table('clsb30_product_extend',
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product')),
                Field('extend_id', type='reference clsb30_data_extend', notnull=True, label=T('Extend')),
                Field('price', type='integer', default=0, label=T('Data Price')),
                Field('description', type='string', notnull=False, label=T('Description')),
                auth.signature)

db.define_table('clsb30_ios_identifier',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('unique_id', type='string', notnull=True, label=T('Account')),
                Field('ios_id', type='string', notnull=True, label=T('iOS Identifier')),
                Field('requested_time', type='integer', notnull=False, label=T('Request times')),
                Field('date_created', type='datetime', notnull=True, label=T('Date Created')),
                Field('des', type='string', notnull=False, label=T('Description')),
                auth.signature)

db.define_table('clsb30_fake_ios',
                Field('fake_name', type='string', label=T('Name')),
                Field('fake_value', type='integer', label=T('value')))

####################SYNC##################################
db.define_table('clsb30_sync_log',
                Field('record_id', type='string', label=T('Record ID')),
                Field('table_name', type='string', label=T('Table Name')),
                Field('data_source', type='string', label=T('Source')),
                Field('status', type='string', label=T('Status')),
                Field('key_unique', type='string', label=T('Unique Key')),
                Field('description', type='string', label=T('Description')),
                auth.signature)
db.clsb30_sync_log._singular = 'Log Sync'
db.clsb30_sync_log._plural = 'Logs Sync'

db.define_table('clsb30_sync_temp',
                Field('record_id', type='string', label=T('Record ID')),
                Field('table_name', type='string', label=T('Table Name')),
                Field('status', type='string', label=T('Status')),
                Field('key_unique', type='string', label=T('Unique Key')),
                Field('description', type='string', label=T('Description')),
                auth.signature)
db.clsb30_sync_temp._singular = 'Temp Sync'
db.clsb30_sync_temp._plural = 'Temp Sync'

################GIFT CODE LOG ###############################
db.define_table('clsb30_gift_code_log',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('gift_code', type='string', notnull=True, label=T('Gift Code')),
                Field('project_code', type='string', notnull=True, default="01", label=T('Project Code')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_gift_code_log._singular = 'Gift Code'
db.clsb30_gift_code_log._plural = 'Gift Code'
###############New pay log##############################
db.define_table('clsb30_payment_log',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product')),
                Field('product_type', type='string', label=T('Type')),
                Field('pay', type='integer', notnull=True, default=0, label=T('Pay')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_payment_log._singular = 'Payment Log'
db.clsb30_payment_log._plural = 'Payment Log'
###############khuyen mai#########################
db.define_table('clsb30_samsung_promotion',
                Field('device_serial', type='string', notnull=True, label=T('Device Serial')),
                Field('description', type='string', label=T('Description')),
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                auth.signature)

db.clsb30_samsung_promotion._singular = 'Promotion Log'
db.clsb30_samsung_promotion._plural = 'Promotion Log'

################ interactive ###############################
db.define_table('clsb30_interactive',
                Field('interactive_title', type='string', notnull=True, label=T('Title')),
                Field('interactive_code', type='string', notnull=True, label=T('Code')),
                Field('interactive_data', type='text', notnull=True, label=T('Data')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_interactive._singular = 'Interactive'
db.clsb30_interactive._plural = 'Interactive'