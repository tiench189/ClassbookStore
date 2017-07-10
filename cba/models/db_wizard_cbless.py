# -*- coding: utf-8 -*-
""" Định nghĩa databases cho chương trình bán subscription video """
__author__ = 'Tien'

#Database luu tru thong tin 1 goi video

db.define_table('cbless_package',
                Field('package_name', type='string', notnull=True, label=T('Package Title')),
                Field('parent_id', type='reference cbless_package', default=None, label=T('Package Parent')),
                Field('package_description', type='text', label=T('Package Description')),
                Field('package_order', type='integer', label=T('Order')),
                Field("deep_level", type='integer', label="Deep Level"),
                Field('video_overview', type='string', label=T('Video Overview')),
                auth.signature,
                format='%(package_name)s')

db.cbless_package._singular = 'CBless less Package'
db.cbless_package._plural = 'CBless less Packages'
#Databases luu tru thong tin 1 video
db.define_table('cbless_item',
                Field('title', type='string', notnull=True, label=T('Title')),
                Field('package_id', type='reference cbless_package', default=None, label=T('Package')),
                Field('description', type='text', label=T('Description')),
                Field('item_path', type='string', label=T('Path')),
                Field('item_type', type='string', label=T('Type')),
                Field('item_order', type='integer', label=T('Order')),
                Field('presenter', type='string', label=T('Author')),
                Field('creator', type='string', label=T('Cretor')),
                Field('publisher', type='string', label=T('publisher')),
                auth.signature,
                format='%(title)s')
db.cbless_item._singular = 'CBless less'
db.cbless_item._plural = 'CBless lesss'


#Databases luu tru thong tin 1 resource
db.define_table('cbless_item_resource',
                Field('title', type='string', notnull=True, label=T('Title')),
                Field('item_id', type='reference cbless_item', default=None, label=T('Item')),
                Field('description', type='text', label=T('Description')),
                Field('item_path', type='string', label=T('Path')),
                Field('item_type', type='string', label=T('Type')),
                Field('item_order', type='integer', label=T('Order')),
                auth.signature,
                format='%(title)s')
db.cbless_item_resource._singular = 'CBless resource'
db.cbless_item_resource._plural = 'CBless resource'

#Quan he n-n item vs package tables
db.define_table('cbless_item_package',
                Field('item_id', type='reference cbless_item', notnull=True, label=T('Item')),
                Field('package_id', type='reference cbless_package', notnull=True, label=T('Package')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.cbless_item_package._singular = 'CBless Package-Item'
db.cbless_item_package._plural = 'CBless Package-Items'

#Database dinh nghia cac goi thoi gian
db.define_table('cbless_subscription_level',
                Field('level_name', type='string', unique=True, notnull=True, label=T('Name')),
                Field('duration', type='integer', notnull=True, label=T('Times')), #days
                Field('description', type='string', label=T('Description')),
                auth.signature,
                format='%(level_name)s')

db.cbless_subscription_level._singular = 'CBless Subscription Level'
db.cbless_subscription_level._plural = 'CBless Subscription Levels'

#Database dinh nghia price cho cac goi
db.define_table('cbless_package_price',
                Field('package_id', type='reference cbless_package', notnull=True, label=T('Package')),
                Field('level_id', type='reference cbless_subscription_level', notnull=True, label=T('Level')),
                Field('price', type='integer', notnull=True, label=T('Price')),
                auth.signature)

db.cbless_package_price._singular = 'CBless Package Price'
db.cbless_package_price._plural = 'CBless Package Price'

#Database luu cac goi KH da mua
db.define_table('cbless_purcharsing',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('package_id', type='reference cbless_package', notnull=True, label=T('Package')),
                Field('subscription_level_id', type='reference cbless_subscription_level', notnull=True, label=T('Package')),
                Field('time_active', type='datetime', notnull=True, label=T('Times Active')),
                Field('time_end', type='datetime', notnull=True, label=T('Times End')),
                Field('auto_renew', type='boolean', notnull=True, default=True, label=T('Auto Renew')),
                auth.signature)

db.cbless_purcharsing._singular = 'CBless Purchasing'
db.cbless_purcharsing._plural = 'CBlessPurchasings'

#Database Log buy subcription
db.define_table('cbless_purcharsing_log',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('package_id', type='reference cbless_package', notnull=True, label=T('Package')),
                Field('subscription_level_id', type='reference cbless_subscription_level', notnull=True, label=T('Package')),
                Field('time_active', type='datetime', notnull=True, label=T('Times Active')),
                Field('time_end', type='datetime', notnull=True, label=T('Times End')),
                Field('auto_renew', type='boolean', notnull=True, default=True, label=T('Auto Renew')),
                auth.signature)

db.cbless_purcharsing_log._singular = 'CBless Log of Purchasing'
db.cbless_purcharsing_log._plural = 'CBless Log of Purchasings'

#Database seek note
db.define_table('cbless_item_seek_point',
                Field('item_id', type='reference cbless_item', notnull=True, label=T('Video')),
                Field('seek_point', type='integer', notnull=True, label=T('Position')),
                Field('seek_point_label', type='string', notnull=True, label=T('Note Label')),
                Field('seek_point_order', type='integer', notnull=True, label=T('Note Order')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.cbless_item_seek_point._singular = 'CBless Seek Point'
db.cbless_item_seek_point._plural = 'CBless Seek Points'

#relation book
db.define_table('cbless_relation_book',
                Field('package_id', type='reference cbless_package', notnull=True, label=T('Package')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Book')),
                Field('relation_type', type='string', label=T('Type')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

#teacher
db.define_table('cbless_teacher',
                Field('teacher_name', type='string', notnull=True, label=T('Name')),
                Field('university', type='string', notnull=True, label=T('University')),
                Field('description', type='text', label=T('Description')),
                auth.signature,
                format='%(teacher_name)s')
db.define_table('cbless_teacher_package',
                Field('package_id', type='reference cbless_package', notnull=True, label=T('Package')),
                Field('teacher_id', type='reference cbless_teacher', notnull=True, label=T('Teacher')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.define_table('a0tech_sms_pay_code',
                Field('package_id', type='reference cbless_package', notnull=True, label=T('Package')), #mon hoc
                Field('paycode', type='string', notnull=True, label=T('Pay Code')),
                Field('send_number', type='string', notnull=True, label=T('Send Number')), # So dien thoai KH gui tin nhan
                Field('service_number', type='string', notnull=True, label=T('Service Number')), # So dien thoai KH gui tin nhan
                Field('message_id', type='string', notnull=True, label=T('Message ID')), #MessageID cua tin nhan KH gui den
                Field('duration', type='integer', notnull=True, label=T('Duration')), #days
                auth.signature)

db.define_table('a0tech_sms_pay_log',
                Field('device_serial', type='string', notnull=True, label=T('Device Serial')),
                Field('package_id', type='reference cbless_package', notnull=True, label=T('Package')),
                Field('paycode', type='string', notnull=True, label=T('Pay Code')),
                Field('amount', type='integer', notnull=True, label=T('Amount')),
                Field('time_active', type='datetime', notnull=True, label=T('Times Active')),
                Field('time_end', type='datetime', notnull=True, label=T('Times End')),
                auth.signature)