__author__ = 'Tien'

import urllib2

CURRENT_SERVER = "127.0.0.1"

url_sync = 'http://' + CURRENT_SERVER + "/cbs20/syncmain/import_temp_to_log.json"
print(url_sync)
urllib2.urlopen(url_sync)
