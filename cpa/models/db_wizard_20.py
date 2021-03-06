# -*- coding: utf-8 -*-
""" Định nghĩa databases cho store 2.0 """
__author__ = 'manhtd'

#########################################
db.define_table('clsb20_dic_creator_cp',
                Field('creator_name', type='string', notnull=True, unique=True, label=T('Creator Name')),
                Field('creator_image', type='upload', uploadfs=osFileServer.opendir(settings.creator_dir),
                      requires=IS_IMAGE(), notnull=True, autodelete=True, label=T('Creator Image')),
                Field('creator_birthday', type='date', label=T('Creator Birthday')),
                Field('creator_description', type='text', label=T('Creator Description')),
                auth.signature, format='%(creator_name)s')
db.clsb20_dic_creator_cp._singular = 'CP Creator'
db.clsb20_dic_creator_cp._plural = 'CP Creators'

#########################################
db.define_table('clsb20_collection_cp',
                Field('collection_name', type='string', unique=True, notnull=True, label=T('Collection Name')),
                Field('collection_description', type='text', label=T('Collection Description')),
                auth.signature, format='%(collection_name)s')
db.clsb20_collection_cp._singular = 'CP Collection'
db.clsb20_collection_cp._plural = 'CP Collections'

#########################################
db.define_table('clsb20_image_type',
                Field('name', type='string', unique=True, notnull=True, label=T('Type Name')),
                Field('description', type='text', label=T('Type Description')),
                auth.signature, format='%(name)s')
db.clsb20_image_type._singular = 'Image Type'
db.clsb20_image_type._plural = 'Image Types'

#########################################
db.define_table('clsb20_product_image',
                Field('product_code', type='string', notnull=True, label=T('Product Code')),
                Field('type_id', type='reference clsb20_image_type', notnull=True),
                Field('image', type='upload', uploadfs=osFileServer.opendir(settings.product_image_dir),
                      requires=IS_IMAGE(), notnull=True, autodelete=True, label=T('Image')),
                Field('description', type='text', label=T('Image Description')),
                auth.signature)
db.clsb20_product_image._singular = 'Product Image'
db.clsb20_product_image._plural = 'Product Images'

########################################
# Get type_code for gen product code
db.define_table('clsb20_product_type',
                Field('type_name', type='string', notnull=True, unique=True, label=T('Product Type Name')),
                Field('type_code', type='string', notnull=True, unique=True, label=T('Product Type Code')),
                Field('parent_type', type="reference clsb20_product_type", label=T('Parent Type'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb20_product_type.id', '%(type_name)s'))),
                Field('type_description', type='text', label=T('Product Type Description')),
                auth.signature, format='%(type_name)s')
db.clsb20_product_type._singular = 'CP Product Type'
db.clsb20_product_type._plural = 'CP Product Types'

#########################################
db.define_table('clsb20_product_cp',
                Field('product_category', type='reference clsb_category', notnull=True, label=T('Category')),
                Field('device_shelf_code', type='reference clsb_device_shelf', notnull=True, default=1,
                      label=T('Device_shelf code')),
                Field('product_collection', type='reference clsb20_collection_cp', notnull=False,
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb20_collection_cp.id', '%(collection_name)s')),
                      label=T('Product Collection')),
                Field('product_creator', type='reference clsb20_dic_creator_cp', notnull=True,
                      label=T('Product Creator')),
                Field('product_publisher', type='reference clsb_dic_publisher', notnull=True,
                      label=T('Product Publisher')),
                Field('subject_class', type='reference clsb_subject_class', label=T('Subject Class')),
                Field('product_title', type='string', notnull=True, label=T('Product Title')),
                Field('product_description', type='text', label=T('Product description')),
                Field('product_code', type='string', notnull=True, unique=True, label=T('Product Code')),
                Field('product_status', type='string', notnull=True, default='Init',
                      requires=IS_IN_SET(['Init', 'Submit', 'Published', 'Cancel', 'Reject', 'CPDelete'],
                                         zero='Choose status:'), label=T('Product Status')),
                # Delete rows for product_status change
                # Field('product_pending', type='datetime', label=T('Product Pending Time')),
                # Field('product_published', type='datetime', label=T('Product Published Time')),
                # Field('product_auth_pending', type='reference auth_user', label=T('Product Pending User')),
                # Field('product_auth_published', type='reference auth_user', label=T('Product Published User')),
                Field('product_price', type='integer', default=0, label=T('Product price')),
                Field('update_file', type='integer', default=1, label=T('Update File')),
                Field('data_type', type='string', default='pdf',
                      label=T('Data Type')),
                auth.signature, format='%(product_title)s')
db.clsb20_product_cp._singular = 'CP Product'
db.clsb20_product_cp._plural = 'CP Products'

#########################################
db.define_table('clsb20_product_metadata_cp',
                Field('product_code', type='string', notnull=True, label=T('Product Code')),
                Field('metadata_id', type='reference clsb_dic_metadata', notnull=True, label=T('Metadata')),
                Field('metadata_value', type='text', notnull=True, label=T('Metadata Value')),
                auth.signature)
db.clsb20_product_metadata_cp._singular = 'CP Product Metadata'
db.clsb20_product_metadata_cp._plural = 'CP Product Metadatas'

#########################################
db.define_table('clsb20_product_relation_cp',
                Field('product_cp_id', type='reference clsb20_product_cp', notnull=True, label=T('Product Code')),
                Field('relation_id', type='reference clsb_product', notnull=True, label=T('Product Relation')),
                auth.signature)
db.clsb20_product_relation_cp._singular = 'CP Product Relation'
db.clsb20_product_relation_cp._plural = 'CP Product Relations'

#########################################
db.define_table('clsb20_review_history',
                Field('product_code', type='string', notnull=True, label=T('Product Code')),
                Field('reviewed_by', type='reference auth_user', label=T('Reviewed User')),
                Field('reviewed_time', type='datetime', notnull=True, label=T('Reviewed Time')),
                Field('status', type='string', notnull=True),
                auth.signature)
db.clsb20_review_history._singular = 'Review History'
db.clsb20_review_history._plural = 'Review Histories'

#########################################
db.define_table('clsb20_review_comment',
                Field('product_code', type='string', notnull=True, label=T('Product Code')),
                Field('user_id', type='reference auth_user', label=T('Comment User')),
                Field('comment_time', type='datetime', notnull=True, label=T('Comment Time')),
                Field('review_comment', type='text', notnull=True),
                auth.signature)
db.clsb20_review_comment._singular = 'Review Comment'
db.clsb20_review_comment._plural = 'Review Comments'
#########################################
db.define_table('clsb20_purchase_type',
                Field('name', type='string', notnull=True, label=T('Type Name')),
                Field('description', type='text', label=T('Description')),
                auth.signature, format="%(name)s")
db.clsb20_purchase_type._singular = 'Purchase Type'
db.clsb20_purchase_type._plural = 'Purchase Types'

#########################################
db.define_table('clsb20_purchase_item',
                Field('name', type='string', notnull=True, label=T('Name')),
                Field('purchase_type', type='reference clsb20_purchase_type', label=T('Purchase Type')),
                Field('duration', type='integer', default=0, label=T('Duration')),
                Field('description', type='text', label=T('Description')),
                auth.signature, format="%(name)s")
db.clsb20_purchase_item._singular = 'Purchase Item'
db.clsb20_purchase_item._plural = 'Purchase Items'

#########################################
db.define_table('clsb20_product_purchase_item',
                Field('product_code', type='string', notnull=True, label=T('Product Code')),
                Field('purchase_item', type='reference clsb20_purchase_item', label=T('Purchase Item')),
                Field('price', type='integer', default=0, label=T('Price')),
                auth.signature)
db.clsb20_product_purchase_item._singular = 'Product Purchase Item'
db.clsb20_product_purchase_item._plural = 'Product  Purchase Items'

#########################################
db.define_table('clsb20_user_purchase_item',
                Field('user_id', type='reference clsb_user', label=T('Customer')),
                Field('purchase_id', type='reference clsb20_product_purchase_item', label=T('Product Purchase')),
                Field('day_end', type='datetime', label=T('Day End')),
                auth.signature)
db.clsb20_user_purchase_item._singular = 'User Purchase Item'
db.clsb20_user_purchase_item._plural = 'User  Purchase Items'

#########################################
db.define_table('clsb20_purchase_renew_history',
                Field('user_id', type='reference clsb_user', label=T('Customer')),
                Field('product_id', type='reference clsb_product', notnull=True, label=T('Product')),
                Field('purchase_id', type='reference clsb20_product_purchase_item', label=T('Product Purchase')),
                Field('date_do_renew', type='datetime', label=T('Renew Day')),
                auth.signature)
db.clsb20_purchase_renew_history._singular = 'Purchase Renew History'
db.clsb20_purchase_renew_history._plural = 'Purchase Renew Histories'

## Tan BM Adding two table 26/12/2013
########################################
db.define_table('clsb20_category_shelf_mapping',
                Field('device_shelf_id', type='reference clsb_device_shelf', notnull=True, label=T('Device Shelf')),
                Field('category_id', type='reference clsb_category', notnull=True, label=T('Category')),
                Field('description', type='text', label=T('Description')),
                auth.signature)
db.clsb20_category_shelf_mapping._singular = 'Category Shelf Mapping'
db.clsb20_category_shelf_mapping._plural = 'Categories Shelf Mappings'

########################################
db.define_table('clsb20_product_price_history',
                Field('product_id', type='reference clsb20_product_cp', notnull=True, label=T('Product')),
                Field('purchase_item', type='reference clsb20_purchase_item', notnull=True, label=T('Purchase Item')),
                Field('price', type='integer', default=0, label=T('Price')),
                Field('changing_time', type='datetime', notnull=True, label=T('Changing Time')),
                Field('description', type='text', label=T('Description')),
                auth.signature)
db.clsb20_product_price_history._singular = 'Product price history'
db.clsb20_product_price_history._plural = 'Product price histories'

#Add product_upload_from_editor TanBM
########################################
db.define_table('clsb20_product_from_editor',
                Field('product_title', type='string', notnull=True, label=T('Product Title')),
                Field('product_code', type='string', notnull=True, unique=True, label=T('Product Code')),
                auth.signature)
db.clsb20_product_from_editor._singular = 'Product from editor'
db.clsb20_product_from_editor._plural = 'Products from editor'

#PhuongNH: add 2 table : clsb20_device_change_history, clsb20_device_exception
# device change history
##########################################
db.define_table('clsb20_device_change_history',
                Field('device_serial', type='string', notnull=True, label=T('Device serial')),
                Field('user_id_move', type='reference clsb_user', notnull=False, label=T('User id move')),
                Field('user_id_move_to', type='reference clsb_user', notnull=False, label=T('User id move to')),
                auth.signature)
db.clsb20_device_change_history._singular = 'Device change history'
db.clsb20_device_change_history._plural = 'Device change history'

#device exception
########################################
db.define_table('clsb20_device_exception',
                Field('device_serial', type='string', notnull=True, label=T('Device serial')),
                Field('status', type='boolean', notnull=True, label=T('Status')),
                Field('history_change', type='reference clsb20_device_change_history', notnull=True, label=T('History change')),
                auth.signature)
db.clsb20_device_exception._singular = 'Device exception'
db.clsb20_device_exception._plural = 'Devices exception'


#type report to user
########################################
db.define_table('clsb20_user_report_type',
                Field('code', type='string', notnull=True, label=T('Code')),
                Field('name', type='string', notnull=True, label=T('Name')),
                Field('description', type='string', notnull=True, label=T('Description')),
                auth.signature,
                format='%(name)s')
db.clsb20_user_report_type._singular = 'User report type'
db.clsb20_user_report_type._plural = 'User report type'

#list report to user
########################################
db.define_table('clsb20_user_report_list',
                Field('report_type', type='reference clsb20_user_report_type', notnull=True, label=T('Report Type')),
                Field('user_id', type='reference auth_user', notnull=True, label=T('User')),
                auth.signature)
db.clsb20_user_report_list._singular = 'User report list'
db.clsb20_user_report_list._plural = 'User report list'

#mapping for category - class
########################################
db.define_table('clsb20_category_class_mapping',
                Field('category_id', type='reference clsb_category', notnull=True, label=T('Categories')),
                Field('class_id', type='reference clsb_class', notnull=True, label=T('Class')),
                auth.signature)
db.clsb20_category_class_mapping._singular = 'Category and class mapping'
db.clsb20_category_class_mapping._plural = 'Categories and classes mapping'

#Add discount table for CP admin
db.define_table('clsb20_discount_cp',
                Field('user_id', type='reference auth_user', notnull=True, label=T('CP Admin')),
                Field('value_discount', type='integer', default="30", label=T('Value Discount')),
                auth.signature)
db.clsb20_discount_cp._singular = 'Discount for CP Admin'
db.clsb20_discount_cp._plural = 'Discounts for CP Admin'

#log err
db.define_table('clsb20_encript_error',
                Field('product_code', type='string', notnull=True, label=T('Product Code')),
                Field('log_error', type='text', label=T('Log Error')),
                Field('created_on', type='datetime', label=T('Created')),
                auth.signature)
db.clsb20_encript_error._singular = 'clsb20_encript_error'
db.clsb20_encript_error._plural = 'clsb20_encript_error'