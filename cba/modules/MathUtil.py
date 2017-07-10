__author__ = 'PhuongNH'

from random import randint
import hashlib


def random_in_range(min, max):
    value = min + randint(0, max)

    return value


def gen_md5_of_string(str):

    return hashlib.md5(str).hexdigest()
