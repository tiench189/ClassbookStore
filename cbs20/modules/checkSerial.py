def hex2byte(s):
    b = ''
    while len(s) >= 2:
        t, s = s[:2], s[2:]
        try:
            b += chr(int('0x' + t, 16))
        except: pass
    return b

Signature = 'Classbook'

import re
import hashlib
def isValidSerial(serial):
    m = re.match(r'(\w\w)(\w\w\w\w)-(\d{9}$)', serial)
    if m:
        version, checksum, id = m.groups()
        version, checksum = hex2byte(version), hex2byte(checksum)
        md5 = hashlib.md5()
        md5.update(Signature + version + id)
        if checksum == md5.digest()[-2:]:
            return True
    return False
