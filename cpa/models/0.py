# coding=utf-8
from gluon.storage import Storage
from gluon.tools import Auth, Mail, DAL
from fs.osfs import OSFS


T.force("vi-vn")

settings = Storage()
settings.title = 'Class Book Service'
settings.subtitle = 'powered by TVB'
settings.author = 'TVB'
settings.author_email = 'admin@classbook.vn'
settings.keywords = ''
settings.description = ''
settings.cpadmin_group = 'CPAdmin'
# settings.database_uri = 'mysql://classbook:CBS2013%21%40%23@127.0.0.1:3306/cbs_r_1_3'
# settings.database_uri = 'mysql://root:CBSadmin2013%21%40%23@127.0.0.1:3306/test_2.0'
#settings.database_uri = 'mysql://dev:DEV2013%21%40%23@127.0.0.1:3306/tvb20'
settings.database_uri = 'mysql://dev:DEV2013%21%40%23@127.0.0.1:3306/manhtd_cbs'
settings.security_key = '315ac07f-778c-4b3c-a36c-1762f18e6886'
settings.migrate = False
settings.item_per_page = 10

settings.email_server = '123.30.179.202:25'
settings.email_sender = 'classbook-noreply@classbook.vn'
settings.email_login = 'classbook-noreply@classbook.vn:Tinhvan20!$'
settings.email_admin = 'classbook.root@gmail.com'

settings.home_dir = '/home/CBSData/'
# settings.home_dir = '/home/developers/manhtd/CBSData/'
settings.cp_dir = 'CPData/'
settings.creator_dir = 'CreatorImages/'
settings.product_image_dir = 'ProductImages/'

settings.rpc_server = "http://127.0.0.1"
settings.discount_value = 30

response.generic_patterns = ['*']
from gluon.custom_import import track_changes
track_changes(True)

db = DAL(settings.database_uri, pool_size=1, check_reserved=['all'],
         migrate_enabled=False, decode_credentials=True)

## configure email
mail = Mail()
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

## configure auth policy
url_index = URL('default', 'index')
auth = Auth(db, hmac_key=settings.security_key, controller='users', function='index')

#########################################
db.define_table('clsb_country',
    Field('country_name', type = 'string', notnull = True, default = "Viet Nam",
          label = T('Country name')),
    Field('country_code', type = 'string', default = "84", unique = True, notnull = True,
          label = T('Country code')),
    Field('description', type = 'text',
          label = T('Description')),
    auth.signature,
    format='%(country_name)s')

#########################################
db.define_table('clsb_province',
    Field('province_name', type = 'string', notnull = True,
          label = T('Province name')),
    Field('country_id', type = 'reference clsb_country', notnull = True,
          label = T('Country id')),
    Field('province_code', type = 'string', unique = True, notnull = True,
          label = T('Province code')),
    Field('description', type = 'text',
          label = T('Description')),
    auth.signature,
    format='%(province_name)s')

#########################################
db.define_table('clsb_district',
    Field('district_name', type = 'string', notnull = True,
          label = T('District name')),
    Field('province_id', type = 'reference clsb_province', notnull = True,
          label = T('Province id')),
    Field('district_code', type = 'string', unique = True, notnull = True,
          label = T('District code')),
    Field('description', type = 'text',
          label = T('Description')),
    auth.signature,
    format='%(district_name)s')

auth.settings.extra_fields['auth_user'] = [
    Field('is_root', type='boolean', writable=False, readable=False),
    Field('token', type='string', readable=False, writable=False),
    Field('last_login', type='datetime', readable=False, writable=False),
    Field('bank_acc', type='string', label='Chủ tài khoản NH'),
    Field('bank_number', type='string', label='Số tài khoản NH'),
    Field('phone', type='string', label='Số điện thoại'),
    Field('country', type='reference clsb_country', default=1, label='Quốc gia'),
    Field('province', type='reference clsb_province', default=1, label='Thành phố'),
    Field('address', type='string', label='Địa chỉ')
]
auth.settings.mailer = mail
auth.settings.registration_requires_verification = True
auth.settings.registration_requires_approval = True
auth.settings.reset_password_requires_verification = True
auth.settings.login_after_registration = False
auth.settings.create_user_groups = False
auth.settings.login_next = url_index
auth.settings.logout_next = url_index
auth.settings.profile_next = url_index
auth.settings.register_next = url_index
auth.settings.retrieve_username_next = url_index
auth.settings.retrieve_password_next = url_index
auth.settings.reset_password_next = url_index
auth.settings.change_password_next = url_index
auth.settings.actions_disabled = ['retrieve_username']
auth.messages.update(dict(
    login_button='Đăng nhập',
    register_button='Đăng ký',
    password_reset_button='Yêu cầu cấp lại mật khẩu',
    password_change_button='Đổi mật khẩu',
    profile_save_button='Cập nhật thay đổi',
    submit_button='Submit',
    verify_password='Xác nhận mật khẩu',
    delete_label='Đánh dấu để xóa',
    function_disabled='Function disabled',
    access_denied='Không đủ quyền hạn',
    registration_verifying='Đăng ký chờ xác thực được gửi qua email',
    registration_pending='Đăng ký đang chờ cấp phép của quản trị',
    login_disabled='Login disabled by administrator',
    logged_in='Đã đăng nhập',
    email_sent='Email đã được gửi',
    unable_to_send_email='Hệ thống đang tạm thời bảo trì, quý khách vui lòng đăng ký lại sau!',
    #'Không thể gửi email',
    email_verified='Email đã được xác thực',
    logged_out='Đăng xuất',
    registration_successful='Đăng ký tài khoản thành công',
    invalid_email='Email không hợp lệ',
    unable_send_email='Hệ thống đang tạm thời bảo trì, quý khách vui lòng đăng ký lại sau!',
    #'Không thể gửi email',
    invalid_login='Đăng nhập thất bại',
    invalid_user='Tài khoản không hợp lệ',
    invalid_password='Mật khẩu không hợp lệ',
    is_empty="Không được bỏ trống",
    mismatched_password="Mật khẩu không khớp",
    verify_email="""
    <html>
    Bạn hoặc ai đó đã sử dụng email này để đăng kí tài khoản cung
    cấp nội dung trên <a href="http://classbook.vn">Classbook Store</a>.<br>
    Để đảm bảo, xin hãy nhấn vào link dưới đây để xác nhận với hệ thống.<br>
    <a href="%(link)s">%(link)s</a><br>
    Trong trường hợp bạn không xác thực, hệ thống sẽ tự động xóa yêu cầu đăng kí của bạn sau 24h.<br>
    (Tài khoản của bạn chỉ thực sự được kích hoạt sau khi chúng tôi hoàn thành việc kiểm tra xác nhận
    thông tin đăng kí  và gửi mail xác nhận tới bạn).<br>
    Đây là mail tự động, xin vui lòng không reply lại.<br>
    Trân trọng!
    </html>
    """,
    verify_email_subject='Xác thực tài khoản',
    username_sent='Your username was emailed to you',
    new_password_sent='A new password was emailed to you',
    password_changed='Password changed',
    retrieve_username='Your username is: %(username)s',
    retrieve_username_subject='Username retrieve',
    retrieve_password='Your password is: %(password)s',
    retrieve_password_subject='Password retrieve',
    reset_password='Click on the link %(link)s to reset your password',
    reset_password_subject='Password reset',
    invalid_reset_password='Invalid reset password',
    profile_updated='Profile updated',
    new_password='Mật khẩu mới',
    old_password='Mật khẩu cũ',
    group_description='Group uniquely assigned to user %(id)s',
    register_log='User %(id)s Registered',
    login_log='User %(id)s Logged-in',
    login_failed_log=None,
    logout_log='User %(id)s Logged-out',
    profile_log='User %(id)s Profile updated',
    verify_email_log='User %(id)s Verification email sent',
    retrieve_username_log='User %(id)s Username retrieved',
    retrieve_password_log='User %(id)s Password retrieved',
    reset_password_log='User %(id)s Password reset',
    change_password_log='User %(id)s Password changed',
    add_group_log='Group %(group_id)s created',
    del_group_log='Group %(group_id)s deleted',
    add_membership_log=None,
    del_membership_log=None,
    has_membership_log=None,
    add_permission_log=None,
    del_permission_log=None,
    has_permission_log=None,
    impersonate_log='User %(id)s is impersonating %(other_id)s',
    label_first_name='Họ',
    label_last_name='Tên',
    label_username='Email',
    label_email='E-mail',
    label_password='Mật khẩu',
    label_registration_key='Registration key',
    label_reset_password_key='Reset Password key',
    label_registration_id='Registration identifier',
    label_role='Role',
    label_description='Description',
    label_user_id='User ID',
    label_group_id='Group ID',
    label_name='Name',
    label_table_name='Object or table name',
    label_record_id='Record ID',
    label_time_stamp='Timestamp',
    label_client_ip='Client IP',
    label_origin='Origin',
    label_remember_me="Lưu tài khoản (trong 30 ngày)",
    verify_password_comment='nhập lại mật khẩu ở trên',
))

#########################################
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

osFileServer = OSFS(settings.home_dir)


def check_is_root():
    query = db(db[auth.settings.table_user_name].id == auth.user.id)
    query = query(db[auth.settings.table_user_name].is_root is True)
    num_root = query.count()
    if num_root == 0:
        session.flash = "You don't have permission!"
        redirect('index')
    return


def __authorize():
    def decorate(action):
        def f(*a, **b):
            if auth.user is not None:
                res = None
                try:
                    from gluon.contrib.simplejsonrpc import ServerProxy
                    url = settings.rpc_server + "/cba/admin/call/jsonrpc"
                    service = ServerProxy(url)
                    res = service.check_permission(request.application, request.controller,
                                                   request.function, auth.user.token)
                except:
                    # print auth.user.token
                    # import traceback
                    # traceback.print_exc()
                    pass
                finally:
                    if res and "result" in res and res["result"] is True:
                        auth.user.permissions = res["permissions"]
                        return action(*a, **b)
            if request.is_restful:
                raise HTTP(401)
            else:
                #session.flash = "Bạn không có quyền truy cập!" if not "message" in res else res["message"]
                redirect(URL(c='default', f='index'))
        f.__doc__ = action.__doc__
        f.__name__ = action.__name__
        f.__dict__.update(action.__dict__)
        return f
    return decorate
auth.requires_authorize = __authorize
