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


#########################################
db.define_table('clsb30_link_download_app',
                Field('title', type='string', notnull=True, label=T('Title')),
                Field('description', type='string', label=T('Description')),
                Field('code', type='string', label=T('Code')),
                Field('creator_name', type='string', label=T('Creator name')),
                Field('link', type='string', label=T('Link')),
                auth.signature, format='%(title)s')
db.clsb30_link_download_app._singular = 'Download app'
db.clsb30_link_download_app._plural = 'Download apps'

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

############################################################Tiench
db.define_table('clsb_free_product',
                Field('username', type='string', notnull=True, label='User Name'),
                Field('product_code', type='string', notnull=True, label='Product Code'),
                Field('is_download', type='integer', notnull=True, default=0, label='Is Download'))

###################3A-project##########################
db.define_table('clsb30_3a_register',
                Field('device_serial', type='string', notnull=True, label=T('Device Serial')),
                Field('user_id', type='string', notnull=True, label=T('User')),
                Field('insert_time', type='datetime', notnull=True, label=T('Time')),
                Field('desctiption', type='string', default="", label=T('Description')),
                auth.signature)
###################3A-project##########################

db.define_table('clsb30_ios_identifier',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('unique_id', type='string', notnull=True, label=T('Account')),
                Field('ios_id', type='string', notnull=True, label=T('iOS Identifier')),
                Field('requested_time', type='integer', notnull=False, label=T('Request times')),
                Field('date_created', type='datetime', notnull=True, label=T('Date Created')),
                Field('des', type='string', notnull=False, label=T('Description')),
                auth.signature)

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

################ Log register device #####################
db.define_table('clsb30_device_log',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('device_serial', type='string', notnull=True, label=T('Device Serial')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_device_log._singular = 'Device Log'
db.clsb30_device_log._plural = 'Device Log'


db.define_table('clsb30_elearning_transaction',
                Field('user_id', type='integer', notnull=True, label=T('User')),
                Field('package_code', type='string', label=T('Package')),
                Field('purchase_type', type='string', label=T('Purchase Type')),
                Field('email_receiver', type='string', label=T('Email Receiver')),
                Field('pack_type', type='string', label=T('Package Type')),
                Field('transaction_id', type='integer', label=T('Transaction')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_elearning_transaction._singular = 'clsb30_elearning_transaction'
db.clsb30_elearning_transaction._plural = 'clsb30_elearning_transaction'


db.define_table('clsb30_tqg_log_tranfer',
                Field('user_id', type='reference clsb_user', notnull=True, unique=True, label=T('User')),
                Field('fund', type='integer', notnull=True, label=T('Fund')),
                Field('status', type='string', notnull=True, label=T('Status')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tqg_log_tranfer._singular = 'clsb30_tqg_log_tranfer'
db.clsb30_tqg_log_tranfer._plural = 'clsb30_tqg_log_tranfer'

############tvt promotion code#####################
db.define_table('clsb30_tvt_promotion_code',
                Field('user_id', type='integer', label=T('User')),
                Field('promotion_code', type='string', notnull=True, label=T('Card Serial')),
                Field('action_type', type='string', label=T('Action Type')),
                Field('before_discount', type='integer', label=T('Before')),
                Field('after_discount', type='integer', label=T('After')),
                Field('time_used', type='datetime', label=T('Time Used')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tvt_promotion_code._singular = 'clsb30_tvt_promotion_code'
db.clsb30_tvt_promotion_code._plural = 'clsb30_tvt_promotion_code'


db.define_table('clsb30_tvt_log',
                Field('user_id', type='integer', label=T('User')),
                Field('discount_code', type='string', notnull=True, label=T('Promotion Code')),
                Field('action_type', type='string', label=T('Action Type')),
                Field('before_discount', type='integer', label=T('Before')),
                Field('after_discount', type='integer', label=T('After')),
                Field('time_used', type='datetime', label=T('Time Used')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tvt_log._singular = 'clsb30_tvt_log'
db.clsb30_tvt_log._plural = 'clsb30_tvt_log'


db.define_table('clsb30_tvt_code',
                Field('promotion_code', type='string', notnull=True, label=T('Card Serial')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tvt_code._singular = 'clsb30_tvt_code'
db.clsb30_tvt_code._plural = 'clsb30_tvt_code'
###################################################


db.define_table('clsb30_tqg_card_log',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('card_serial', type='string', notnull=True, label=T('Card Serial')),
                Field('card_pin', type='string', notnull=True, label=T('Card Pin')),
                Field('card_value', type='integer', notnull=True, label=T('Card Value')),
                Field('created_on', type='string', notnull=True, label=T('Created On')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tqg_card_log._singular = 'clsb30_tqg_card_log'
db.clsb30_tqg_card_log._plural = 'clsb30_tqg_card_log'
