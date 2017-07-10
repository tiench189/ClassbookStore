db = DAL(settings.database_uri, pool_size=1, check_reserved=['all'],
         migrate_enabled=settings.migrate, decode_credentials=True, db_codec='UTF-8')


response.generic_patterns = ['*']

from gluon.tools import Auth, Mail
auth = Auth(db, hmac_key = settings.security_key)

mail = Mail()
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

from datetime import datetime
from fs.osfs import OSFS
osFileServer = OSFS(settings.home_dir)

## Google Api Key 
GOOGLE_API_KEY = "AIzaSyBFA3zO-fDW6iVg11fMqf6MANE4AwB1xRU"
GCM_SEND_HOST = "android.googleapis.com"
GCM_SEND_URL = "/gcm/send"