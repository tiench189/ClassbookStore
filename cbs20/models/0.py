from gluon.storage import Storage
settings = Storage()
settings.title = 'Class Book Service'
settings.subtitle = 'powered by TVB'
settings.author = 'TVB'
settings.author_email = 'admin@classbook.vn'
settings.keywords = ''
settings.description = ''


# settings.database_uri = 'mysql://classbook:CBS2013%21%40%23@127.0.0.1:3306/tvb21'
settings.database_uri = 'mysql://sync:CBSadmin2014%21%40%23@123.30.179.205:3306/tvb20'
settings.database_sync = 'mysql://sync:CBSadmin2014%21%40%23@classbook.vn:3306/tvb20'

settings.security_key = '315ac07f-778c-4b3c-a36c-1762f18e6886'
settings.migrate = False

settings.email_server = '123.30.179.202:25'
settings.email_sender = 'classbook-noreply@classbook.vn'
settings.email_login = 'classbook-noreply@classbook.vn:Tinhvan20!$'

# settings.home_dir = '/home/CBSData/'
settings.home_dir = '/home/CBSData/'
settings.cp_dir = 'CPData/'
settings.creator_dir = 'CreatorImages/'
settings.product_image_dir = 'ProductImages/'
settings.items_per_page = 20
settings.server_ver = 'server_mp'
settings.fake_fund_media = 0
settings.fake_fund_quiz = 5000
settings.device_support = "tablet"
settings.current_server = "classbook.vn"
settings.main_server = "123.30.179.205"

#settings.aes_key = b"#+Renajeva=URe6eV94EWu66asW-T?uB"

# the block size for the cipher object; must be 16, 24, or 32 for AES
#settings.aes_blocksize = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
#settings.aes_padding = '{'
