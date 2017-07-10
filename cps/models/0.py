from gluon.storage import Storage
from gluon.tools import Auth, Mail, DAL, Service
from fs.osfs import OSFS


T.force("en-us")

settings = Storage()
settings.title = 'Class Book Service'
settings.subtitle = 'powered by TVB'
settings.author = 'TVB'
settings.author_email = 'admin@classbook.vn'
settings.keywords = ''
settings.description = ''

#settings.database_uri = 'mysql://classbook:CBS2013%21%40%23@127.0.0.1:3306/tvb20'
settings.database_uri = 'mysql://classbook:CBS2013%21%40%23@127.0.0.1:3306/tvb21'
settings.database_uri = 'mysql://dev:DEV2013%21%40%23@127.0.0.1:3306/phuongnh_cbs'
settings.security_key = '315ac07f-778c-4b3c-a36c-1762f18e6886'
settings.migrate = False

settings.email_server = '123.30.179.202:25'
settings.email_sender = 'classbook-noreply@classbook.vn'
settings.email_login = 'classbook-noreply@classbook.vn:Tinhvan20!$'

settings.home_dir = '/home/CBSData/'
#settings.home_dir = '/home/developers/manhtd/CBSData/'
settings.cp_dir = 'CPData/'
settings.creator_dir = 'CreatorImages/'
settings.product_image_dir = 'ProductImages/'

settings.rpc_server = "http://127.0.0.1:8001"

response.generic_patterns = ['*']
from gluon.custom_import import track_changes
track_changes(True)

db = DAL(settings.database_uri, pool_size=1, check_reserved=['all'],
         migrate_enabled=False, decode_credentials=True)

service = Service()

## configure email
mail = Mail()
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

## configure auth policy
url_index = URL('default', 'index')
auth = Auth(db, hmac_key=settings.security_key)
auth.settings.mailer = mail
auth.settings.extra_fields['auth_user'] = [
    Field('is_root', type='boolean', writable=False, readable=False),
    Field('token', type='string', readable=False, writable=False),
    Field('last_login', type='datetime', readable=False, writable=False)
]
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.create_user_groups = False
auth.settings.update(actions_disabled=['login', 'logout', 'register', 'verify_email', 'retrieve_username',
                                       'retrieve_password', 'reset_password', 'request_reset_password',
                                       'change_password', 'profile', 'groups', 'impersonate', 'not_authorized'])
auth.define_tables(username=True, migrate=settings.migrate, signature=True)

osFileServer = OSFS(settings.home_dir)


def check_login():
    if not auth.user:
        redirect(URL("users", "error"))
    return


def check_service_root():
    count = db(db[auth.settings.table_user_name].id == auth.user.id)
    count = count(db[auth.settings.table_user_name].is_root is True).count()
    if count == 0:
        redirect(URL("users", "error"))
    return


def check_local():
    if request.env.http_x_forwarded_for or request.is_https:
        session.secure()
    elif not request.client.startswith('192.168.56.'):
    #elif not request.is_local and not DEMO_MODE:
        raise HTTP(200, T('Admin is disabled because insecure channel'))
    return


def __authorize():
    def decorate(action):
        def f(*a, **b):
            if len(request.args) > 0:
                token = request.args[-1]
                res = None
                try:
                    from gluon.contrib.simplejsonrpc import ServerProxy
                    url = settings.rpc_server + "/cba/admin/call/jsonrpc"
                    server = ServerProxy(url)
                    res = server.check_permission(request.application, request.controller, request.function, token)
                except:
                    # print auth.user.token
                    # import traceback
                    # traceback.print_exc()
                    pass
                finally:
                    if "result" in res and res["result"] is True:
                        return action(*a, **b)
            if request.is_restful:
                raise HTTP(401)
            else:
                return dict(error="You don't have permission to access!")
                # session.flash = "You don't have permission to access!"
                # redirect(URL(c='default', f='index'))
        f.__doc__ = action.__doc__
        f.__name__ = action.__name__
        f.__dict__.update(action.__dict__)
        return f
    return decorate
auth.requires_authorize = __authorize


db.define_table('clsb_config',
                Field('config_key', type='string', unique=True, notnull=True),
                Field('config_value', type='text'))
db.define_table('clsb20_encrypt_product',
                Field('product_code', type='string', unique=True, notnull=True),
                Field('product_path', type='string', notnull=True),
                Field('status', type='string', notnull=True, default='PENDING',
                      requires=IS_IN_SET(['PENDING', 'ENCRYPTING'], zero = None)))
