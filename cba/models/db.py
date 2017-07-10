# coding=utf-8
# force set language to English
T.force('en-en')

db = DAL(settings.database_uri, pool_size=1, check_reserved=['all'],
         decode_credentials=True, migrate_enabled=settings.migrate)
#db config to fix db error
# db = DAL(settings.database_uri, pool_size=1, check_reserved=['all'],
#          decode_credentials=True, migrate_enabled=settings.migrate, fake_migrate_all=True)

response.generic_patterns = ['*']

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate, Mail
from datetime import datetime
from fs.osfs import OSFS

auth = Auth(db, hmac_key=settings.security_key)
service, plugins = Service(), PluginManager()

## create all tables needed by auth if not custom tables
auth.settings.extra_fields['auth_user'] = [
    #Field('category_permission', type='reference category',
    # requires=IS_EMPTY_OR(IS_IN_DB(db, 'category.id', '%(category_name)s')), writable=False),
    Field('is_root', type='boolean', writable=False, readable=False),
    Field('token', type='string', readable=False),
    Field('last_login', type='datetime', readable=False),
    Field('bank_acc', type='string'),
    Field('bank_number', type='string'),
    Field('phone', type='string'),
    Field('country', type='reference clsb_country'),
    Field('province', type='reference clsb_province'),
    Field('address', type='string'),
    Field('deny_functions', type='list:reference auth20_function', label=T('Deny Functions'))
]

## configure email
mail = Mail()
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

## configure auth policy
auth.settings.controller = 'default'
auth.settings.mailer = mail
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = False
auth.settings.actions_disabled.append('register')

osFileServer = OSFS(settings.home_dir)
if not osFileServer.exists(settings.creator_dir):
    osFileServer.makedir(settings.creator_dir)
if not osFileServer.exists(settings.product_image_dir):
    osFileServer.makedir(settings.product_image_dir)

## Google Api Key
GOOGLE_API_KEY = "AIzaSyBFA3zO-fDW6iVg11fMqf6MANE4AwB1xRU"
GCM_SEND_HOST = "android.googleapis.com"
GCM_SEND_URL = "/gcm/send"

db.define_table('clsb_config',
                Field('config_key', type='string', unique=True, notnull=True),
                Field('config_value', type='text'))
db.define_table('clsb20_encrypt_product',
                Field('product_code', type='string', unique=True, notnull=True),
                Field('product_path', type='string', notnull=True),
                Field('status', type='string', notnull=True, default='PENDING',
                      requires=IS_IN_SET(['PENDING', 'ENCRYPTING'], zero=None)))
