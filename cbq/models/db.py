db = DAL(settings.database_uri, pool_size=1, check_reserved=['all'], migrate=settings.migrate, fake_migrate_all=False,
         decode_credentials=True)

response.generic_patterns = ['*'] #if request.is_local else []

## configure email
from gluon.tools import Auth, Mail

auth = Auth(db, hmac_key=settings.security_key)
auth.define_tables(username=True, migrate=settings.migrate, fake_migrate=False)

mail = Mail()
mail.settings.server = settings.email_server
mail.settings.sender = settings.email_sender
mail.settings.login = settings.email_login

from datetime import datetime
from fs.osfs import OSFS

osFileServer = OSFS(settings.home_dir)

osFileServer = OSFS(settings.home_dir)

osStaticFolder = OSFS(settings.static_folder)
