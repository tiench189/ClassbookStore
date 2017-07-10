from gluon.storage import Storage
settings = Storage()

settings.migrate = True
settings.title = 'Classbook Admin'
settings.subtitle = 'powered by TVB'
settings.author = 'TVB'
settings.author_email = 'admin@classbook.vn'
settings.keywords = ''
settings.description = ''

# settings.database_uri = 'mysql://dev:DEV2013%21%40%23@127.0.0.1:3306/tvb20'
settings.database_uri = 'mysql://dev:DEV2013%21%40%23@127.0.0.1:3306/manhtd_cbs'

settings.security_key = '315ac07f-778c-4b3c-a36c-1762f18e6886'
settings.email_server = '123.30.179.202:25'
settings.email_sender = 'classbook-noreply@classbook.vn'
settings.email_login = 'classbook-noreply@classbook.vn:Tinhvan20!$'

# settings.home_dir = '/home/CBSData/'
settings.home_dir = '/home/CBSData/'
settings.default_show = 'ANDROID_APP/IOS_APP/CBM/STORE_WEB/STORE_APP'

settings.cp_dir = 'CPData/'
settings.creator_dir = 'CreatorImages/'
settings.product_image_dir = 'ProductImages/'
settings.discount_value = 30
