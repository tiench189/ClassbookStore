# -*- coding: utf-8 -*-
""" Định nghĩa databases cho classbook phien ban windows """
__author__ = 'vuongtm'


db.define_table('cbapp_windows_activated_key',
                Field('license_key', type='string', notnull=True,  unique=True, label=T('License Key')),
                Field('device_serial', type='string', notnull=True, label=T('Device Serial')),
                Field('user_name', type='string', notnull=False, default="None", label=T('User name')),
                Field('company', type='string', notnull=False, default="None", label=T('Email')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.cbapp_windows_activated_key._singular = 'CBApp Windows Activated Key'
db.cbapp_windows_activated_key._plural = 'CBApp Windows Activated Keys'


db.define_table('cbapp_windows_key_available',
                Field('license_key', type='string', notnull=True,  unique=True, label=T('License Key')),
                Field('gender', type='integer', notnull=True, default=0, label=T('Gender')),
                Field('description', type='string', label=T('Description')),
                auth.signature)

db.cbapp_windows_key_available._singular = 'CBApp Windows Available Key'
db.cbapp_windows_key_available._plural   = 'CBApp Windows Available Keys'