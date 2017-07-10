# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Name:        db_wizard
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
from datetime import datetime

db.define_table('clsb_collection',
                Field('collection_name', type='string', unique=True, notnull=True,
                      label=T('Collection Name')),
                Field('collection_description', type='text',
                      label=T('Collection Description')),
                auth.signature,
                format='%(collection_name)s')
db.clsb_collection._singular = 'Collection'
db.clsb_collection._plural = 'Collections'

########################################
db.define_table('clsb_dic_metadata',
                Field('metadata_name', type='string', notnull=True, unique=True,
                      label=T('Loại thông tin')),
                Field('metadata_label', type='string', notnull=True, unique=True,
                      label=T('Nhãn thông tin')),
                Field('metadata_description', type='text',
                      label=T('Thông tin bổ sung')),
                auth.signature,
                format='%(metadata_name)s')
db.clsb_dic_metadata._singular = 'Metadata'
db.clsb_dic_metadata._plural = 'Metadatas'

########################################
db.define_table('clsb_dic_creator',
                Field('creator_name', type='string', notnull=True, unique=True,
                      label=T('Creator Name')),
                Field('creator_image', type='upload', uploadfs=osFileServer, requires=IS_IMAGE(), notnull=True,
                      autodelete=True,
                      label=T('Creator Image')),
                Field('creator_birthday', type='date',
                      label=T('Creator Birthday')),
                Field('creator_description', type='text',
                      label=T('Creator Description')),
                auth.signature,
                format='%(creator_name)s')
db.clsb_dic_creator._singular = 'Creator'
db.clsb_dic_creator._plural = 'Creator'

########################################
db.define_table('clsb_dic_publisher',
                Field('publisher_name', type='string', notnull=True, unique=True,
                      label=T('Publisher Name')),
                Field('publisher_description', type='text',
                      label=T('Publisher Description')),
                auth.signature,
                format='%(publisher_name)s')
db.clsb_dic_publisher._singular = 'Publisher'
db.clsb_dic_publisher._plural = 'Publishers'

########################################
db.define_table('clsb_product_type',
                Field('type_name', type='string', notnull=True, unique=True,
                      label=T('Product Type Name')),
                Field('type_description', type='text',
                      label=T('Product Type Description')),
                auth.signature,
                format='%(type_name)s')
db.clsb_product_type._singular = 'Product Type'
db.clsb_product_type._plural = 'Product Types'

########################################
db.define_table('clsb_category',
                Field('category_name', type='string', notnull=True,
                      label=T('Catagory Name')),
                Field('category_code', type='string', notnull=True, unique=True,
                      label=T('Category Code')),
                Field('category_type', type='reference clsb_product_type', notnull=True, default=1,
                      label=T('Category Type')),
                Field('category_order', type='integer', notnull=True, default=9999,
                      label=T('Order')),
                Field('category_parent', type='reference clsb_category', label='Category Parent',
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb_category.id', '%(category_name)s'))),
                auth.signature,
                format='%(category_name)s')
db.clsb_category._singular = 'Category'
db.clsb_category._plural = 'Categories'

#########################################
db.define_table('clsb_device_shelf',
                Field('device_shelf_name', type='string', notnull=True, unique=True,
                      label=T('Device_shelf name')),
                Field('device_shelf_code', type='string', notnull=True, unique=True,
                      #           requires = IS_IN_SET(['SK', 'SGK1', 'SGK2', 'SGK3', 'SGK4', 'SGK5', 'SGK6', 'SGK7', 'SGK8', 'SGK9', 'SGK10', 'SGK11', 'SGK12', 'SGV'], zero = None),
                      label=T('Device_shelf code')),
                Field('shelf_order', type='integer', default=0, notnull=True, label='Device Shelf Order'),
                Field('device_shelf_type', type='string', notnull=True,
                      requires=IS_IN_SET(['BOOK', 'APP', 'QUIZ'], zero=None),
                      label=T('Device_shelf type')),
                Field('description', type='string',
                      label=T('Description')),
                auth.signature,
                format='%(device_shelf_code)s')

########################################
db.define_table('clsb_class',
                Field('class_name', type='string', notnull=True,
                      label=T('Class Name')),
                Field('class_code', type='string', notnull=True, unique=True,
                      label=T('Class Code')),
                Field('class_order', type='string', notnull=True, default=9999,
                      label=T('Class order')),
                Field('class_sequent', type='string', notnull=True,
                      label=T('Class sequent')),
                Field('class_description', type='string',
                      label=T('Class Description')),
                auth.signature,
                format='%(class_name)s')

########################################
db.define_table('clsb_subject',
                Field('subject_name', type='string', notnull=True,
                      label=T('Subject Name')),
                Field('subject_code', type='string', notnull=True, unique=True,
                      label=T('Subject Code')),
                Field('subject_order', type='string', notnull=True, default=9999,
                      label=T('Subject order')),
                Field('subject_description', type='string',
                      label=T('Subject Description')),
                auth.signature,
                format='%(subject_name)s')

########################################
db.define_table('clsb_subject_class',
                Field('subject_id', type='reference clsb_subject', notnull=True,
                      label=T('Subject Id')),
                Field('class_id', type='reference clsb_class', notnull=True,
                      label=T('Class Id')),
                auth.signature,
                format='%(subject_id)s - %(class_id)s')

########################################
db.define_table('clsb_product',
                Field('product_category', type='reference clsb_category', notnull=True,
                      label=T('Category')),
                Field('device_shelf_code', type='reference clsb_device_shelf', notnull=True, default=1,
                      label=T('Device_shelf code')),
                Field('product_collection', type='reference clsb_collection', notnull=False,
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb_collection.id', '%(collection_name)s')),
                      label=T('Product Collection')),
                Field('product_creator', type='reference clsb_dic_creator', notnull=True,
                      label=T('Product Creator')),
                Field('product_publisher', type='reference clsb_dic_publisher', notnull=True,
                      label=T('Product Publisher')),
                Field('subject_class', type='reference clsb_subject_class',
                      label=T('Subject Class')),
                Field('product_title', type='string', notnull=True,
                      label=T('Product Title')),
                Field('product_description', type='text',
                      label=T('Product description')),
                Field('product_code', type='string', notnull=True, unique=True,
                      label=T('Product Code')),
                Field('product_status', type='string', notnull=True, default='Pending',
                      requires=IS_IN_SET(['Pending', 'Approved', 'Denied', 'Disable'], zero='Choose status:'),
                      label=T('Product Status')),
                Field('total_download', type='integer', default=0,
                      label=T('Total Download')),
                Field('product_cover', type='string', writable=False,
                      label=T('Cover Image')),
                Field('product_data', type='string', writable=False,
                      label=T('Product Data')),
                Field('product_pdf', type='string', writable=False,
                      label=T('Product PDF')),
                Field('product_price', type='integer', default=0,
                      label=T('Product price')),
                Field('product_rating', type='integer', default=0,
                      label=T('Product Rating')),
                Field('rating_count', type='integer', default=0,
                      label=T('Rating Count')),
                Field('created_on', type='datetime', writable=False, default=datetime.now(),
                      label=T('Created On')),
                Field('show_on', type='string', default='ANDROID_APP/IOS_APP/CBM/STORE_WEB/STORE_APP',
                      label=T('Show On')),
                Field('data_type', type='string', default='pdf',
                      label=T('Data Type')),
                auth.signature,
                format='%(product_title)s')
db.clsb_product._singular = 'Product'
db.clsb_product._plural = 'Products'

########################################
db.define_table('clsb_product_metadata',
                Field('product_id', type='reference clsb_product', notnull=True,
                      label=T('Product')),
                Field('metadata_id', type='reference clsb_dic_metadata', notnull=True,
                      label=T('Metadata')),
                Field('metadata_value', type='text', notnull=True,
                      label=T('Metadata Value')),
                auth.signature,
                format='%(id)s')
db.clsb_product_metadata._singular = 'Product Metadata'
db.clsb_product_metadata._plural = 'Product Metadatas'

########################################
db.define_table('clsb_product_relation',
                Field('product_id', type='reference clsb_product', notnull=True,
                      label=T('Product')),
                Field('relation_id', type='reference clsb_product', notnull=True,
                      label=T('Product Relation')),
                auth.signature)
db.clsb_product_relation._singular = 'Product Relation'
db.clsb_product_relation._plural = 'Product Relations'

import sys
########################################
db.define_table('clsb_user',
                Field('username', type='string', length=50, unique=True, notnull=True,
                      label=T('User Name')),
                Field('district', type='reference clsb_district', notnull=False, label=T('District')),
                Field('password', type='string', length=50, notnull=True,
                      label=T('Password')),
                Field('status', type='boolean', default=True,
                      label=T('Account Status')),
                Field('lastLoginTime', type='datetime', notnull=True, default=datetime.now(),
                      label=T('Last Login Time')),
                Field('firstName', type='string', length=100, notnull=True,
                      label=T('First Name')),
                Field('lastName', type='string', length=100, notnull=True,
                      label=T('Last Name')),
                Field('email', type='string', length=100, notnull=True, unique=True, requires=IS_EMAIL(),
                      label=T('Email')),
                Field('phoneNumber', type='string', length=50,
                      label=T('Phone Number')),
                Field('address', type='string', default="ND",
                      label=T('Address')),
                Field('user_token', type='string',
                      label=T('User token')),
                Field('valid_time', type='integer', default=0, notnull=True, requires=IS_INT_IN_RANGE(0, 6),
                      label=T('Valid time')),
                Field('fund', type='integer', default=0, # requires=IS_INT_IN_RANGE(0, sys.maxint),
                      label=T('Fund')),
                Field('data_sum', type='string', default="", notnull=True, readable=False, writable=False,
                      label=T('Data Sum')),
                Field('token_reset_pwd', type='string', default="", notnull=True, readable=False, writable=False,
                      label=T('Token reset password')),
                Field('reset_pwd_time', type='datetime', label=T('Last Login Time')),
                Field('test_user', type='integer', default=0, notnull=True, label=T('Test User')),
                Field('type_user', type='string', default="normal", notnull=True, label=T('Type User')),
                Field('register_from', type='string', label=T('Register from')),
                auth.signature,
                format='%(username)s')
db.clsb_user._singular = 'User'
db.clsb_user._plural = 'Users'


########################################
db.define_table('clsb_device',
                Field('user_id', type='reference clsb_user', notnull=True,
                      label=T('User')),
                Field('device_serial', type='string', notnull=True, unique=True,
                      label=T('Device Serial')),
                Field('status', type='boolean', default=True,  # True == active, False == disable
                      label=T('Device Status')),
                Field('in_use', type='boolean', default=False,  # True == in use, False == not in use
                      label=T('Device in use')),
                Field('device_firmware', type='string',  # notnull = True,
                      label=T('Device Firmware')),
                Field('device_release', type='date',
                      label=T('Device Release Date')),
                Field('device_registration', type='datetime', default=datetime.now(),
                      label=T('Device Registration Date')),
                Field('last_uid', type='integer',
                      label=T('Last user ID')),
                Field('device_type', type='string', default='CLASSBOOK',  # default : CLASSBOOK, if not : OTHER
                      label=T('Device type')),
                Field('device_name', type='string', default='CLASSBOOK',
                      label=T('Device name')),
                auth.signature,
                format='%(device_serial)s')
db.clsb_device._singular = 'Device'
db.clsb_device._plural = 'Devices'

########################################
db.define_table('clsb_download_archieve',
    Field('user_id', type='reference clsb_user', notnull=True,
          label=T('User id')),
    Field('product_id', type='reference clsb_product', notnull=True,
          label=T('Product')),
    Field('download_time', type='datetime', notnull=True, default=datetime.now(),
          label=T('Download time')),
    Field('price', type='integer', notnull=True,
          label=T('Price')),
    Field('purchase_type', type='string', #TANBM: add purchase_type
          label=T('Purchase type')),
    Field('rom_version', type='string', notnull=True, #add rom_version
          label=T('ROM version')),
    Field('device_serial', type='string', notnull=True,
          label=T('Device serial')),
    Field('status', type='string', notnull=True,
          label=T('Status')),
    auth.signature,
    format='%(product_id.product_code)s')
db.clsb_download_archieve._singular = 'Download Archieve'
db.clsb_download_archieve._plural = 'Download Archieves'

########################################
db.define_table('clsb_user_log',
                Field('user_id', type='reference clsb_user', notnull=True,
                      label=T('User id')),
                Field('user_action', type='string', length=50, notnull=True,
                      requires=IS_IN_SET(['Search', 'View', 'Download'], zero=T('choose one')),
                      label=T('Action')),
                Field('date_created', type='datetime', default=datetime.now(),
                      label=T('Date created')),
                Field('search_text', type='string',
                      label=T('Search Text')),
                Field('product_code', type='string',
                      label=T('Product code')),
                Field('ip_address', type='string',
                      label=T('ip address')),
                Field('from_system', type='string',
                      label=T('from system')),
                Field('created_on', type='datetime', writable=False, default=datetime.now(),
                      label=T('Created On')),
                auth.signature,
                format='%(user_action)s')
db.clsb_user_log._singular = 'User Log'
db.clsb_user_log._plural = 'User Logs'

########################################
db.define_table('clsb_attention_type',
                Field('type_name', type='string', notnull=True,
                      label=T('Type Name')),
                auth.signature,
                format='%(user_action)s')
db.clsb_attention_type._singular = 'Attention Type'
db.clsb_attention_type._plural = 'Attention Types'

########################################
db.define_table('clsb_attention',
                Field('product_id', type='reference clsb_product', notnull=True,
                      label=T('Product Id')),
                Field('attention_type', type='string', notnull=True,
                      label=T('Attention type')),
                Field('valid_date', type='string',
                      label=T('Valid date')),
                auth.signature)
db.clsb_attention._singular = 'Attention'
db.clsb_attention._plural = 'Attentions'

########################################
db.define_table('clsb_home_topic',
                Field('topic_name', type='string', notnull=True, unique=True,
                      label=T('Topic name')),
                Field('topic_order', type='integer',
                      label=T('Topic Order')),
                Field('category_id', type='reference clsb_category', notnull=True,
                      label=T('Category Id')),
                Field('used_for', type='string', default='Choose status:',
                      requires=IS_IN_SET(['All', 'Classbook_manager', 'ClassbookVN'], zero='Choose status:'),
                      label=T('Used for')),
                auth.signature,
                format='%(topic_name)s')
db.clsb_home_topic._singular = 'Home Topic'
db.clsb_home_topic._plural = 'Home Topics'

########################################
db.define_table('clsb_home_topic_item',
                Field('topic_id', type='reference clsb_home_topic', notnull=True,
                      label=T('Topic ID')),
                Field('product_id', type='reference clsb_product', notnull=True,
                      label=T('Product Id')),
                Field('product_type', type='string',
                      requires=IS_IN_SET(['APP', 'BOOK', 'Image'], zero='Choose type:'),
                      label=T('Product type')),
                Field('topic_item_order', type='integer', notnull=True,
                      label=T('Topic Item Order')),
                Field('item_path', type='upload',
                      label=T('Item path')),
                auth.signature,
                format='%(id)s')
db.clsb_home_topic_item._singular = 'Home Topic Item'
db.clsb_home_topic_item._plural = 'Home Topic Items'

########################################
db.define_table('clsb_contact_category',
                Field('category_name', type='string', notnull=True,
                      label=T('Category name')),
                Field('category_description', type='text',
                      label=T('Category description')),
                auth.signature,
                format='%(category_name)s')
db.clsb_contact_category._singular = 'Contact Category'
db.clsb_contact_category._plural = 'Contact Categories'

########################################
db.define_table('clsb_contact',
                Field('email', type='string', notnull=True, requires=IS_EMAIL(),
                      label=T('email')),
                Field('name', type='string',
                      label=T('name')),
                Field('phone', type='string',
                      label=T('phone')),
                Field('contact_category_id', type='reference clsb_contact_category', notnull=True,
                      label=T('Category')),
                Field('contact_content', type='text', notnull=True,
                      label=T('Content')),
                Field('contact_subject', type='string', notnull=True,
                      label=T('Subject')),
                Field('create_date', type='datetime', default=datetime.now,
                      label=T('Create date')),
                Field('status', type='string',
                      label=T('Status')),
                Field('processed_by', type='string',
                      label=T('Processed by')),
                Field('confirm_date', type='datetime',
                      label=T('Confirm date')),
                Field('finished_date', type='datetime',
                      label=T('Finished date')),
                Field('reply_content', type='text',
                      label=T('Reply content')),
                auth.signature,
                format='%(id)s')
db.clsb_contact._singular = 'Contact'
db.clsb_contact._plural = 'Contacts'

########################################
db.define_table('clsb_version',
                Field('software', type='string', notnull=True,
                      label=T('Software')),
                Field('lastest_version', type='string', notnull=True,
                      label=T('Lastest version')),
                Field('release_date', type='datetime', notnull=True,
                      label=T('Release date')),
                Field('description', type='string',
                      label=T('Description')),
                auth.signature,
                format='%(software)s')

#########################################
db.define_table('clsb_warranty_device',
                Field('device_serial', type='string', notnull=True, unique=True,
                      label=T('Device serial')),
                Field('full_name', type='string', notnull=True,
                      label=T('Full name')),
                Field('phone', type='string',
                      label=T('Phone')),
                Field('email', type='string', notnull=True, requires=IS_EMAIL(),
                      label=T('Email')),
                Field('purchase_date', type='datetime', notnull=True,
                      label=T('Purchase date')),
                Field('register_date', type='datetime', default=datetime.now(),
                      label=T('Register date')),
                Field('address', type='text',
                      label=T('address')),
                auth.signature,
                format='%(device_serial)s')

#########################################
db.define_table('clsb_released_serial',
                Field('released_serial', type='string', notnull=True, unique=True,
                      label=T('Released serial')),
                auth.signature,
                format='%(released_serial)s')

#########################################
db.define_table('clsb_warranty_history',
                Field('first_name', type='string',
                      label=T('First name')),
                Field('last_name', type='string',
                      label=T('Last name')),
                Field('address', type='text',
                      label=T('Address')),
                Field('phone', type='string', notnull=True,
                      label=T('Phone')),
                Field('cover_serial', type='string', notnull=True,
                      label=T('Cover serial')),
                Field('device_serial', type='string',
                      label=T('Device serial')),
                Field('service_order', type='string',
                      label=T('Service order')),
                Field('warranty_date', type='datetime', notnull=True,
                      label=T('Warranty date')),
                Field('accessory', type='string',
                      label=T('Accessory')),
                Field('warranty_time', type='integer', default=0,
                      label=T('Warranty time')),
                Field('error_description', type='text',
                      label=T('Error description')),
                Field('email', type='string', notnull=True, requires=IS_EMAIL(),
                      label=T('Email')),
                Field('receive_date', type='datetime', notnull=True, default=datetime.now(),
                      label=T('Receive date')),
                Field('return_date', type='datetime',
                      label=T('Return date')),
                Field('solution', type='text',
                      label=T('Solution')),
                Field('status', type='string',
                      label=T('Status')),
                Field('category', type='string',
                      label=T('Category')),
                auth.signature,
                format='%(device_serial)s')

#########################################
db.define_table('clsb_image',
                Field('image_code', type='string', notnull=True, unique=True,
                      label=T('Image code')),
                Field('image_title', type='string', notnull=True,
                      label=T('Title')),
                Field('description', type='text',
                      label=T('Description')),
                #    Field('item_path', type = 'upload', notnull = True,
                #          label = T('Item path')),
                auth.signature,
                format='%(image_code)s')

#########################################
db.define_table('clsb_comment',
                Field('email', type='string', requires=IS_EMAIL(),
                      label=T('Email')),
                Field('comment_content', type='text',
                      label=T('Comment')),
                Field('comment_date', type='datetime', notnull=True, default=datetime.now(),
                      label=T('Date')),
                Field('product_code', type='string', notnull=True,
                      label=T('Product code')),
                Field('status', type='string', notnull=True, default='NEW',
                      requires=IS_IN_SET(['APPROVED', 'PENDING', 'NEW'], zero=None),
                      label=T('Status')),
                auth.signature,
                format='%(email)s')

#########################################
db.define_table('clsb_country',
                Field('country_name', type='string', notnull=True, default="Viet Nam",
                      label=T('Country name')),
                Field('country_code', type='string', default="84", unique=True, notnull=True,
                      label=T('Country code')),
                Field('description', type='text',
                      label=T('Description')),
                auth.signature,
                format='%(country_name)s')

#########################################
db.define_table('clsb_province',
                Field('province_name', type='string', notnull=True,
                      label=T('Province name')),
                Field('country_id', type='reference clsb_country', notnull=True,
                      label=T('Country id')),
                Field('province_code', type='string', unique=True, notnull=True,
                      label=T('Province code')),
                Field('description', type='text',
                      label=T('Description')),
                auth.signature,
                format='%(province_name)s')

#########################################
db.define_table('clsb_district',
                Field('district_name', type='string', notnull=True,
                      label=T('District name')),
                Field('province_id', type='reference clsb_province', notnull=True,
                      label=T('Province id')),
                Field('district_code', type='string', unique=True, notnull=True,
                      label=T('District code')),
                Field('description', type='text',
                      label=T('Description')),
                auth.signature,
                format='%(district_name)s')

#########################################
db.define_table('clsb_order',
                Field('customer_name', type='string', notnull=True,
                      label=T('Customer name')),
                Field('email', type='string', notnull=True, requires=IS_EMAIL(),
                      label=T('Email')),
                Field('phone', type='string', notnull=True,
                      label=T('Phone')),
                Field('address', type='text', notnull=True,
                      label=T('Address')),
                Field('country', type='reference clsb_country',
                      #notnull = True, but we have old order, that dont have those fields. Then we let its null
                      label=T('Country')),
                Field('province', type='reference clsb_province',  #notnull = True,
                      label=T('Province')),
                Field('district', type='reference clsb_district',  #notnull = True,
                      label=T('District')),
                Field('number_devices', type='integer', notnull=True,
                      label=T('Number of device')),
                Field('order_date', type='datetime', notnull=True, default=datetime.now(),
                      label=T('Order date')),
                Field('payment_type', type='string',
                      label=T('Payement type')),
                Field('note', type='text',
                      label=T('Note')),
                Field('unit_price', type='integer', notnull=True,
                      label=T('Unit price')),
                Field('total_price', type='integer', notnull=True,
                      label=T('Total price')),
                auth.signature,
                format='%(customer_name)s')

from datetime import datetime
#########################################
db.define_table('clsb_transaction',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User Id')),
                Field('merchant_id', type='string', label=T('Merchant Id')),
                Field('merchant_account', type='string', label=T('Merchant Account')),
                Field('status', type='string', notnull=True, default='INIT', label=T('Status')),
                Field('amount', type='integer', default=0, notnull=True, label=T('Amount')),
                Field('payment_type', type='string', label=T('Payment Type')),
                Field('order_code', type='string', label=T('Order Code')),
                Field('description', type='string', label=T('Description')),
                Field('nl_version', type='string', notnull=True, label=T('NL Version')),  # ng?n lu?ng
                Field('nl_function', type='string', notnull=True, label=T('NL Function')),  # ng?n lu?ng function
                Field('card_serial', type='string', label=T('Card Serial')),  # s? serial c?a th? c?o
                Field('card_pin', type='string', label=T('Card Pin')),  # pin card c?a th?
                Field('card_amount', type='integer', label=T('Card Amount')),  # gi? tr? ti?n c?a th? c?o khi n?p = th?
                Field('token', type='string', label=T('Token')),
                Field('bank_code', type='string', label=T('Bank Code')),
                Field('created_on', type='datetime', notnull=True, writable=False,
                      default=datetime.now(), label=T('Created On')),
                auth.signature,
                format='%(id)s')

##########################################
db.define_table('clsb_rating',
                Field('user_id', type='reference clsb_user', notnull=True, label=T('User Id')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product Id')),
                Field('star', type='integer', notnull=True, default=3, label=T('Star')),
                auth.signature,
                format='%(id)s')  # , primarykey=['user_id', 'product_id'])

##########################################
db.define_table('clsb_gcm',
                Field('gcm_id', type='string', notnull=True, label=T('GCM Id')),
                Field('serial', type='string', notnull=True, unique=True, label=T('Serial')),
                Field('created', type='datetime', notnull=False, default=datetime.now(), label=T('Created On')),
                auth.signature,
                format='%(serial)s')
db.clsb_gcm._singular = 'GCM Device'
db.clsb_gcm._plural = 'GCM Devices'

##########################################
db.define_table('clsb_ota_version',
                Field('software', type='string', notnull=True, label=T('Software')),
                Field('lastest_version', type='string', notnull=True,
                      label=T('Lastest version')),
                Field('release_date', type='datetime', notnull=True,
                      label=T('Release date')),
                Field('description', type='string',
                      label=T('Description')),
                Field('MD5', type='string',
                      label=T('MD5')),
                auth.signature,
                format='%(software)s')

#########################################
db.define_table(auth.settings.table_permission_name,
                Field('group_id', type='reference ' + auth.settings.table_group_name, notnull=True,
                      label='Group ID'),
                Field('table_name', type='string', notnull=True, default='clsb_category', writable=False,
                      readable=False,
                      label='Table'),
                Field('name', type='string', notnull=True, default='Read',
                      requires=IS_IN_SET(['Approve', 'Create', 'Delete', 'List', 'Read', 'Update'],
                                         zero='Choose one below:'),
                      label='Name'),
                Field('record_id', type='reference clsb_category', notnull=True,
                      label='Category'),
                auth.signature,
                format='%(id)s')
db.define_table(auth.settings.table_group_name,
                Field('role', length=512, default='', label='Role',
                      requires=IS_NOT_IN_DB(db, '%s.role' % auth.settings.table_group_name)),
                Field('description', 'text', label='Description'),
                auth.signature, format='(%(id)s) %(role)s')

auth.define_tables(username=True, migrate=settings.migrate, signature=True)
db.auth_user._singular = 'Admin User'
db.auth_user._plural = 'Admin Users'
db.auth_group._singular = 'Admin Group'
db.auth_group._plural = 'Admin Groups'
db.auth_membership._singular = 'Admin Membership'
db.auth_membership._plural = 'Admin Memberships'
db.auth_permission._singular = 'Admin Permission'
db.auth_permission._plural = 'Admin Permissions'
