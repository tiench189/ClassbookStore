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
                Field('code_suffix', type='string', label=T('suffix')),
                Field('code_value', type='integer', label=T('Code Value')),
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

#############Dang ki email#################
db.define_table('clsb30_support_email',
                Field('email', type='string', notnull=True, label=T('Email')),
                Field("from_site", type='string', label=T('Site')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_support_email._singular = 'Support Email'
db.clsb30_support_email._plural = 'Support Email'


##############mua bo sach#########################
db.define_table('clsb30_set_of_product',
                Field('set_name', type='string', notnull=True, label=T('Name')),
                Field('set_code', type='string', unique=True, notnull=True, label=T('Code')),
                Field('set_status', type='string', notnull=True, default='show',
                      requires=IS_IN_SET(['show', 'hide']),
                      label=T('Code')),
                Field('description', type='string', label=T('Description')),
                auth.signature,
                format='%(set_name)s')

db.clsb30_set_of_product._singular = 'clsb30_set_of_product'
db.clsb30_set_of_product._plural = 'clsb30_set_of_product'


##############mua bo sach#########################
db.define_table('clsb30_product_in_set',
                Field('product_id', type='integer', notnull=True, label=T('Product')),
                Field('set_id', type='reference clsb30_set_of_product', notnull=True, label=T('set')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_product_in_set._singular = 'clsb30_product_in_set'
db.clsb30_product_in_set._plural = 'clsb30_product_in_set'


##############Log Preview#########################
db.define_table('clsb30_preview_log',
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product')),
                Field('client_type', type='string', notnull=True, default="ANDROID", label=T('Client Type')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_preview_log._singular = 'clsb30_preview_log'
db.clsb30_preview_log._plural = 'clsb30_preview_log'


###################Event khuyen mai###################
db.define_table('clsb30_event_promotion',
                Field('product_id', type='integer', notnull=True, label=T('Product')),
                Field('user_id', type='integer', notnull=True, label=T('User')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_event_promotion._singular = 'eventpromotion'
db.clsb30_event_promotion._plural = 'event promotion'


db.define_table('clsb30_user_get_promotion',
                Field('product_id', type='integer', notnull=True, label=T('Product')),
                Field('user_id', type='integer', notnull=True, label=T('User')),
                Field('time_get', type='datetime', notnull=True, label=T('Time')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_user_get_promotion._singular = 'clsb30_user_get_promotion'
db.clsb30_user_get_promotion._plural = 'clsb30_user_get_promotion'


#Third party
db.define_table('clsb30_third_party_log',
                Field('username', type='string', notnull=True, label=T('User')),
                Field('time_set', type='datetime', notnull=True, label=T('Time')),
                Field('party_code', type='string', label=T('Code')),
                Field('party_name', type='string', label=T('Name')),
                Field('party_type', type='string', label=T('Type')),
                Field('price', type='integer', label=T('Price')),
                Field('from_system', type='string', label=T('System')),
                Field('description', type='text', label=T('Description')),
                auth.signature)


db.define_table('clsb30_tqg_log_tranfer',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('fund', type='integer', notnull=True, label=T('Fund')),
                Field('status', type='string', notnull=True, label=T('Status')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tqg_log_tranfer._singular = 'clsb30_tqg_log_tranfer'
db.clsb30_tqg_log_tranfer._plural = 'clsb30_tqg_log_tranfer'

## Bo de thi#
db.define_table('clsb30_chuyen_de',
                Field('cate_code', type='string', label=T('Code')),
                Field('cate_title', type='string', notnull=True, label=T('Title')),
                Field('cate_parent', type='reference clsb30_chuyen_de', label=T('Parent')),
                Field('show_status', type='integer', notnull=True, default=1, label=T('Show Status')),
                Field('description', type='text', label=T('Description')),
                auth.signature, format='%(cate_title)s')

db.clsb30_chuyen_de._singular = 'clsb30_chuyen_de'
db.clsb30_chuyen_de._plural = 'clsb30_chuyen_de'

db.define_table('clsb30_bt_chuyen_de',
                Field('exer_code', type='string', notnull=True, unique=True, label=T('Code')),
                Field('exer_title', type='string', notnull=True, label=T('Title')),
                Field('chuyen_de', type='reference clsb30_chuyen_de', notnull=True, label=T('Chuyen de')),
                Field('show_status', type='integer', notnull=True, default=1, label=T('Show Status')),
                Field('description', type='text', label=T('Description')),
                auth.signature, format='%(exer_title)s')

db.clsb30_bt_chuyen_de._singular = 'clsb30_bt_chuyen_de'
db.clsb30_bt_chuyen_de._plural = 'clsb30_bt_chuyen_de'

#################

db.define_table('clsb30_tqg_card',
                Field('hash_code', type='string', notnull=True, unique=True, label=T('Hash Code')),
                Field('card_serial', type='string', notnull=True, label=T('Card Serial')),
                Field('card_value', type='string', notnull=True, label=T('Card value')),
                Field('serial_activate', type='integer', notnull=True, default=0, label=T('Serial Activate')),
                Field('time_valid', type='datetime', notnull=False, label=T('Time valid')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tqg_log_tranfer._singular = 'clsb30_tqg_card'
db.clsb30_tqg_log_tranfer._plural = 'clsb30_tqg_card'


db.define_table('clsb30_tqg_card_log',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('card_serial', type='string', notnull=True, label=T('Card Serial')),
                Field('card_pin', type='string', notnull=True, label=T('Card Pin')),
                Field('card_value', type='integer', notnull=True, label=T('Card Value')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tqg_card_log._singular = 'clsb30_tqg_card_log'
db.clsb30_tqg_card_log._plural = 'clsb30_tqg_card_log'

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

################Banner home page#########################
db.define_table('clsb30_banner',
                Field('banner_title', type='string', label=T('Title')),
                Field('banner_url', type='string', notnull=True, label=T('URL')),
                Field('active_status', type='integer', notnull=True, default=1, label=T('Status')),
                Field('action_type', type='string', notnull=True, label=T('Action Type')),
                Field('action_data', type='string', label=T('Action Data')),
                Field('banner_order', type='integer', notnull=True, default=0, label=T('Order')),
                Field('banner_site', type='string', label=T('Site')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_banner._singular = 'clsb30_banner'
db.clsb30_banner._plural = 'clsb30_banner'


##################Dinh nghia bo sach de tai#################################
db.define_table('clsb30_bo_sach',
                Field('bs_name', type='string', notnull=True, label=T('Name')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_bo_sach._singular = 'clsb30_bo_sach'
db.clsb30_bo_sach._plural = 'clsb30_bo_sach'


db.define_table('clsb30_sach_trong_bo',
                Field('bs_id', type='reference clsb30_bo_sach', notnull=True, label=T('Bo sach')),
                Field('product_id', type='integer', notnull=True, label=T('Sach')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_sach_trong_bo._singular = 'clsb30_sach_trong_bo'
db.clsb30_sach_trong_bo._plural = 'clsb30_sach_trong_bo'


'''
DB phuv vu du an ban the mua cac goi lop cap 1
'''
db.define_table('cbcode_collection',
                Field('collection_name', type='string', notnull=True, label=T('Name')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.cbcode_collection._singular = 'cbcode_collection'
db.cbcode_collection._plural = 'cbcode_collection'

db.define_table('cbcode_product_collection',
                Field('collection_id', type='reference cbcode_collection', notnull=True, label=T('Collection')),
                Field('product_id', type='integer', notnull=True, label=T('Product')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.cbcode_product_collection._singular = 'cbcode_product_collection'
db.cbcode_product_collection._plural = 'cbcode_product_collection'

db.define_table('cbcode_log',
                Field('user_id', type='integer', notnull=True, label=T('User')),
                Field('collection_id', type='integer', notnull=True, label=T('Collection')),
                Field('pin_code', type='string', label=T('Code')),
                Field('serial', type='string', label=T('Serial')),
                Field('code_value', type='integer', label=T('Value')),
                Field('project', type='string', label=T('Value')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.cbcode_log._singular = 'cbcode_log'
db.cbcode_log._plural = 'cbcode_log'