__author__ = 'Windows 10 Gamer'

import redis
import sys

HOST_CACHE_MASTER = '192.168.95.229'
HOST_CACHE_SLAVE = '127.0.0.1'
PORT = 6379
DB = 0
PASSWORD = 'chaoemcogailamhong!'


def write_cache(key, data, time_expire=0):
    try:
        r = redis.Redis(host=HOST_CACHE_MASTER, port=PORT, db=DB, password=PASSWORD)
        r.set(key, data)
        if time_expire > 0:
            r.expire(key, time_expire)
        return dict(result=True)
    except Exception as ex:
        return dict(result=False, error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def write_dict(key, data, time_expire=0):
    try:
        r = redis.Redis(host=HOST_CACHE_MASTER, port=PORT, db=DB, password=PASSWORD)
        r.hmset(key, data)
        if time_expire > 0:
            r.expire(key, time_expire)
        return dict(result=True)
    except Exception as ex:
        return dict(result=False, error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def get_cache(key):
    try:
        r = redis.Redis(host=HOST_CACHE_SLAVE, port=PORT, db=DB)
        data = r.get(key)
        return dict(result=True, data=data)
    except Exception as ex:
        return dict(result=False, error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def get_cache_dict(key):
    try:
        r = redis.Redis(host=HOST_CACHE_SLAVE, port=PORT, db=DB)
        data = r.hgetall(key)
        return dict(result=True, data=data)
    except Exception as ex:
        return dict(result=False, error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))
