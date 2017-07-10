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


##########################################
db.define_table('clsb30_set_purchase',
                Field('set_code', type='string', label=T('Set code'), notnull=True),
                Field('set_name', type='string', label=T('Set name'), notnull=True),
                Field('description', type='string', label=T('Description')),
                auth.signature, format='%(set_name)s')
db.clsb30_set_purchase._singular = "Set purchase"
db.clsb30_set_purchase._plural = "Sets purchase"

############################################
db.define_table('clsb30_set_purchase_product',
                Field('set_purchase_id', type='reference clsb30_set_purchase', notnull=True,
                      label=T('Set purchase id')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product id')),
                auth.signature, format='%(id)s'
                )
db.clsb30_set_purchase_product._singular = "Set purchase product"
db.clsb30_set_purchase_product._plural = "Sets purchase product"

db.define_table('clsb30_set_product',
                Field('set_purchase_id', type='reference clsb30_set_purchase', notnull=True,
                      label=T('Set purchase id')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product id')),
                auth.signature, format='%(id)s'
                )
db.clsb30_set_product._singular = "Set product"
db.clsb30_set_product._plural = "Sets product"

###################################################
db.define_table('clsb30_media_history',
                Field('product_title', type='string', notnull=True, label=T('Product Title')),
                Field('product_price', type='integer', default=0, label=T('Product Price')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product')),
                Field('category_id', type='reference clsb_category', notnull=True, label=T('Category')),
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                auth.signature, format='%(product_title)s')
db.clsb20_dic_creator_cp._singular = 'Product History'
db.clsb20_dic_creator_cp._plural = 'Product Histories'

###################3A-project##########################
db.define_table('clsb30_3a_register',
                Field('device_serial', type='string', notnull=True, label=T('Device Serial')),
                Field('user_id', type='string', notnull=True, label=T('User')),
                Field('insert_time', type='datetime', notnull=True, label=T('Time')),
                Field('desctiption', type='string', default="", label=T('Description')),
                auth.signature)
###################3A-project##########################

################## apns ###############################
db.define_table('clsb30_apns',
                Field('user_email', type='string', notnull=True, label=T('User Email')),
                Field('apns_token', type='string', notnull=True, label=T('APNS Token')),
                Field('date_created', type='datetime', notnull=True, label=T('Date Created')),
                Field('date_modify', type='datetime', notnull=True, label=T('Date Modify')),
                Field('description', type='string', default="", label=T('Description')),
                auth.signature)
################## apsn ###############################

db.define_table('clsb30_ios_identifier',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('unique_id', type='string', notnull=True, label=T('Account')),
                Field('ios_id', type='string', notnull=True, label=T('iOS Identifier')),
                Field('requested_time', type='integer', notnull=False, label=T('Request times')),
                Field('date_created', type='datetime', notnull=True, label=T('Date Created')),
                Field('des', type='string', notnull=False, label=T('Description')),
                auth.signature)

####################direct download##########################
db.define_table('clsb30_direct',
                Field('product_code', type='string', notnull=True, label=T('Code')),
                Field('download_time', type='datetime', notnull=True, label=T('Download Time')),
                Field('des', type='string', notnull=False, label=T('Description')),
                auth.signature)

############### Dinh nghia du lieu mo rong ####################
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
                Field('code_suffix', type='string', label=T('Suffix')),
                Field('code_value', type='integer', label=T('Code Value')),
                Field('project_code', type='string', notnull=True, default="01", label=T('Project Code')),
                Field('created_on', type='datetime', notnull=False, label=T('Created On')),
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

################ Log register device #####################
db.define_table('clsb30_device_log',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('device_serial', type='string', notnull=True, label=T('Device Serial')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_device_log._singular = 'Device Log'
db.clsb30_device_log._plural = 'Device Log'

################ interactive ###############################
db.define_table('clsb30_interactive',
                Field('interactive_title', type='string', notnull=True, label=T('Title')),
                Field('interactive_code', type='string', notnull=True, label=T('Code')),
                Field('interactive_data', type='text', notnull=True, label=T('Data')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_interactive._singular = 'Interactive'
db.clsb30_interactive._plural = 'Interactive'

################GIFT CODE LOG ###############################
db.define_table('clsb30_gift_code_test',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('gift_code', type='string', notnull=True, label=T('Gift Code')),
                Field('project_code', type='string', notnull=True, default="01", label=T('Project Code')),
                Field('created_on', type='datetime', notnull=False, label=T('Created On')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_gift_code_test._singular = 'Gift Code'
db.clsb30_gift_code_test._plural = 'Gift Code'

##############LOG UPLOAD#########################
db.define_table('clsb30_log_upload',
                Field('product_code', type='string', notnull=True, label=T('Product Code')),
                Field('product_category', type='string', notnull=True, label=T('Product Category')),
                Field('upload_status', type='string', notnull=True, default="FAIL", label=T('Status')),
                Field('created_on', type='datetime', notnull=False, label=T('Created On')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_log_upload._singular = 'Log Upload'
db.clsb30_log_upload._plural = 'Log Upload'

#############Hen gio push gcm#################
db.define_table('clsb30_gcm_timer',
                Field('group_type', type='string', notnull=True,
                      requires=IS_IN_SET(['ANDROID_APP', 'CB_DEVICE']),
                      label=T('Group Type')),
                Field('gcm_timer', type='datetime', notnull=True, label=T('Timer')),
                Field('gcm_message', type='text', notnull=True, label=T('Message')),
                Field('gcm_link', type='string', label=T('Link')),
                auth.signature)

db.clsb30_gcm_timer._singular = 'clsb30_gcm_timer'
db.clsb30_gcm_timer._plural = 'clsb30_gcm_timer'

#############Update solr#################
db.define_table('clsb30_update_product_log',
                Field('record_id', type='integer', notnull=True, label=T('Record ID')),
                Field('table_name', type='string', notnull=True, label=T('Table')),
                Field('update_action', type='string', notnull=True, label=T('Action')),
                Field('update_status', type='string', notnull=True, default="FAIL", label=T('Status')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_gcm_timer._singular = 'Log Update Product'
db.clsb30_gcm_timer._plural = 'Log Update Product'

#############Dang ki email#################
db.define_table('clsb30_support_email',
                Field('email', type='string', notnull=True, label=T('Email')),
                Field("from_site", type='string', label=T('Site')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_support_email._singular = 'Support Email'
db.clsb30_support_email._plural = 'Support Email'


#############Back up price#################
db.define_table('clsb30_backup_price',
                Field('product_id', type='integer', notnull=True, label=T('Product id')),
                Field('product_price', type='integer', notnull=True, label=T('Product Price')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.clsb30_backup_price._singular = 'clsb30_backup_price'
db.clsb30_backup_price._plural = 'clsb30_backup_price'


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
                Field('created_on', type='datetime', notnull=False, label=T('Created On')),
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

db.clsb30_third_party_log._singular = 'clsb30_third_party_log'
db.clsb30_third_party_log._plural = 'clsb30_third_party_log'

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
db.define_table('clsb30_tqg_log_tranfer',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('fund', type='integer', notnull=True, label=T('Fund')),
                Field('status', type='string', notnull=True, label=T('Status')),
                Field('created_on', type='string', notnull=True, label=T('Created On')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tqg_log_tranfer._singular = 'clsb30_tqg_log_tranfer'
db.clsb30_tqg_log_tranfer._plural = 'clsb30_tqg_log_tranfer'


############## Define thi quoc gia card ############################
db.define_table('clsb30_tqg_card',
                Field('hash_code', type='string', notnull=True, unique=True, label=T('Hash Code')),
                Field('card_serial', type='string', notnull=True, label=T('Card Serial')),
                Field('card_value', type='string', notnull=True, label=T('Card value')),
                Field('serial_activate', type='integer', notnull=True, default=0, label=T('Serial Activate')),
                Field('time_valid', type='datetime', notnull=False, label=T('Time valid')),
                Field('actived_by', type='reference auth_user', notnull=False, label=T('Actived By')),
                Field('actived_on', type='datetime', notnull=False, label=T('Activated On')),
                Field('card_gift', type='integer', notnull=True, default=0, label=T('Gift')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tqg_log_tranfer._singular = 'clsb30_tqg_card'
db.clsb30_tqg_log_tranfer._plural = 'clsb30_tqg_card'


db.define_table('clsb30_tqg_card_log',
                Field('user_id', type='integer', notnull=True, label=T('User')),
                Field('card_serial', type='string', notnull=True, label=T('Card Serial')),
                Field('card_pin', type='string', notnull=True, label=T('Card Pin')),
                Field('card_value', type='integer', notnull=True, label=T('Card Value')),
                Field('created_on', type='string', notnull=True, label=T('Created On')),
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
                Field('promotion_code', type='string', notnull=True, label=T('Code')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_tvt_code._singular = 'clsb30_tvt_code'
db.clsb30_tvt_code._plural = 'clsb30_tvt_code'
###################################################

####################Thi thu##################
db.define_table('clsb30_ki_thi_thu',
                Field('exam_name', type='string', notnull=True, label=T('Name')),
                Field('exam_index', type='integer', notnull=True, label=T('Index')),
                Field('start_date', type='datetime', notnull=True, label=T('Start')),
                Field('end_date', type='datetime', notnull=True, label=T('End')),
                Field('exam_time', type='integer', notnull=True, default=90, label=T('Time')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.clsb30_ki_thi_thu._singular = 'clsb30_ki_thi_thu'
db.clsb30_ki_thi_thu._plural = 'clsb30_ki_thi_thu'

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
                Field('created_on', type='datetime', notnull=False, label=T('Created On')),
                Field('description', type='text', label=T('Description')),
                auth.signature)

db.cbcode_log._singular = 'cbcode_log'
db.cbcode_log._plural = 'cbcode_log'


##Vstep atempts


db.define_table('vstep_attempts',
                Field('id', type='integer', notnull=True, label=T('ID')),
                Field('user_id', type='integer', notnull=True, label=T('User')),
                Field('subject', type='string', label=T('Subject')),
                Field('grade', type='double', label=T('Grade')),
                Field('timestart', type='integer', label=T('Time Start')),
                Field('timefinish', type='integer', label=T('Time Finish')),
                Field('duration', type='integer', label=T('Duration')),
                Field('exam_id', type='integer', label=T('Exam')),
                Field('vstep_format', type='string', label=T('Format')))

db.vstep_attempts._singular = 'vstep_attempts'
db.vstep_attempts._plural = 'vstep_attempts'

