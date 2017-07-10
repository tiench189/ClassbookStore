# -*- coding: utf-8 -*-
""" Định nghĩa databases cho chương trình bán subscription video """
__author__ = 'Tien'

#Databases luu tru thong tin 1 video
db.define_table('cb_video',
                Field('video_title', type='string', notnull=True, label=T('Video Title')),
                Field('video_duration', type='string', label=T('Video Duration')),
                Field('video_description', type='string', label=T('Video Description')),
                Field('video_author', type='string', label=T('Video Author')),
                auth.signature,
                format='%(video_title)s')

db.cb_video._singular = 'CB Video'
db.cb_video._plural = 'CB Video'

#Database luu tru thong tin 1 goi video
db.define_table('cb_package',
                Field('package_name', type='string', notnull=True, label=T('Package Title')),
                Field('package_description', type='string', label=T('Package Description')),
                auth.signature,
                format='%(package_name)s')

db.cb_package._singular = 'CB Package'
db.cb_package._plural = 'CB Package'

#Database quan he giua video - goi video
db.define_table('cb_video_package',
                Field('video_id', type='reference cb_video', notnull=True, label=T('Video')),
                Field('package_id', type='reference cb_package', notnull=True, label=T('Package')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.cb_video_package._singular = 'CB Video Package'
db.cb_video_package._plural = 'CB Video Package'

#Database dinh nghia cac goi thoi gian
db.define_table('cb_subscription_level',
                Field('level_name', type='string', notnull=True, label=T('Name')),
                Field('times', type='integer', notnull=True, label=T('Times')),
                Field('description', type='string', label=T('Description')),
                auth.signature,
                format='%(level_name)s')

db.cb_subscription_level._singular = 'CB Subscription Level'
db.cb_subscription_level._plural = 'CB Subscription Level'

#Database dinh nghia price cho cac goi
db.define_table('cb_package_price',
                Field('package_id', type='reference cb_package', notnull=True, label=T('Package')),
                Field('level_id', type='reference cb_subscription_level', notnull=True, label=T('Level')),
                Field('price', type='integer', notnull=True, label=T('Price')),
                auth.signature)

db.cb_package_price._singular = 'CB Package Price'
db.cb_package_price._plural = 'CB Package Price'

#Database luu trang thai active
db.define_table('cb_user_subscription',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('package_id', type='reference cb_package', notnull=True, label=T('Package')),
                Field('time_active', type='datetime', notnull=True, label=T('Times Active')),
                Field('time_end', type='datetime', notnull=True, label=T('Times End')),
                auth.signature)

db.cb_user_subscription._singular = 'CB User Subscription'
db.cb_user_subscription._plural = 'CB User Subscription'

#Database Log buy subcription
db.define_table('cb_log_subscription',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User')),
                Field('package_price_id', type='reference cb_package_price', notnull=True, label=T('Pakage price')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.cb_log_subscription._singular = 'CB Log Subscription'
db.cb_log_subscription._plural = 'CB Log Subscription'