
__author__ = 'PhuongNH'

import hashlib


def gen_md5_of_string(str):

    return hashlib.md5(str).hexdigest()


def gen_restore_code(serial, secret_code):
    try:
        secret_key = "LVDEQS"

        device_serial = serial

        key = device_serial + secret_code + secret_key

        key = key.upper()

        md5str = gen_md5_of_string(key)

        last6character = md5str[len(md5str) -6:]
    except Exception as e:
        print str(e)

    return last6character




