from gluon.storage import Storage
settings = Storage()


settings.migrate = False
settings.title = 'Class Book Service'
settings.subtitle = 'powered by TVB'
settings.author = 'TVB'
settings.author_email = 'admin@classbook.vn'
settings.keywords = ''
settings.description = ''
settings.layout_theme = 'default'
settings.database_uri = 'mysql://quiz_bank:QUIZ2013%21%40%23@127.0.0.1:3306/quiz_bank'
#settings.database_uri = 'mysql://dev:DEV2013%21%40%23@127.0.0.1:3306/phuongnh_cbs'
settings.security_key = '315ac07f-778c-4b3c-a36c-1762f18e6886'
settings.email_server = '123.30.179.202:25'
settings.email_sender = 'order@classbook.vn'
settings.email_login = 'order@classbook.vn:Redro16)&!#'
settings.login_method = 'local'
settings.login_config = ''
settings.plugins = []
settings.items_per_page = 20
settings.home_dir = '/home/CBSData/'
settings.static_folder = '/home/developers/phuongnh/web2py/applications/cbq/static'
