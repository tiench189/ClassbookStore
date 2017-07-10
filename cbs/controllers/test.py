__author__ = 'Tien'

import sys
from applications.cbs.modules.transaction import encrypt
from gluon.contrib.redis_utils import RConn
from gluon.contrib.redis_cache import RedisCache
from gluon.contrib.redis_session import RedisSession

def set_redis_session():
    try:
        #from gluon.contrib.redis_utils import RConn
        rconn = RConn(host='192.168.95.229', port=6379, db=0, password='chaoemcogailamhong!')
        
        sessiondb = RedisSession(redis_conn=rconn, with_lock=True, session_expiry=False)
        session.connect(request, response, db=sessiondb)

        session.vuongtm = 'Chao em'
    except Exception as ex:
        return ex
	#dict(error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def get_redis_sesion():
    return session.vuongtm

def get_redis_cache():

    try:
        key = request.vars['key']

        #rconn = RConn(host='192.168.95.192', port=6379)
        #cache.redis = RedisCache(redis_conn=rconn, debug=True)
        #cache.redis = RedisCache(redis_conn=rconn, debug=True, with_lock=True)
        import redis
        r = redis.StrictRedis(host='127.0.0.1', port=6379, db=0)
        #r.set('foo', 'bar')
        return r.hgetall("test")

    except Exception as ex:
        return dict(error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def set_redis_cache():
    import pickle
    import redis
    import json
    try:
        r = redis.Redis(host='192.168.95.229', port=6379, db=0, password='chaoemcogailamhong!')
        testd = {'Name': 'Zara', 'Age': 7, 'Class': 'First'}
        #user = {}
        #user['username'] = 'vuongtm'
        #user['dept'] = "TVB"
        r.delete("test")
        r.hmset("test", testd)
        r.expire("test", 60)

        #p_mydict = pickle.dumps(testd)
        ##r.set('test', 'set from slave')
        #r.hmset ("test",p_mydict)
        rconn = RConn(host='192.168.95.229', port=6379, db=0, password='chaoemcogailamhong!')
        cache.redis = RedisCache(redis_conn=rconn, debug=True)
        #favorite_color = {"lion": "yellow", "kitty": "red"}
        cache.redis.delete("test")
        cache.redis.cache_it('test', testd, 180)
        #return cache.redis.stats()
    except Exception as ex:
        return dict(error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))


def test_transaction():
    buyer_id = 8289
    user_name = 'tiench@gmail.com'
    nl_token = "test"
    nl_data = dict()
    nl_data['total_amount'] = 2000
    nl_data["order_code"] = 8793
    nl_data["transaction_id"] = "20614912"
    if True:
        if True:
            if True:
                if True:
                    if True:
                        try:
                            old_fund = db(db.clsb_user.id == buyer_id).select(
                                db.clsb_user.fund)[0].fund
                            if isinstance(old_fund, (int, long)):
                                new_fund = int(old_fund)
                                new_fund += int(nl_data["total_amount"])
                                data_sum = encrypt(new_fund, user_name)
                                db(db.clsb_user.id == buyer_id).update(
                                    fund=new_fund, data_sum=data_sum)
                            else:
                                return dict(error="Error fund")
                            order_code = nl_data["order_code"]
                            q = db(db.clsb_transaction.id == order_code)
                            payment_type = q.select().first()['payment_type']
                            amount = int(nl_data["total_amount"])
                            face_value = amount
                            real_value = amount
                            if payment_type == "VISA":
                                face_value = amount
                                real_value = amount * 0.97 - 5000
                            elif payment_type == "ATM_ONLINE":
                                face_value = amount
                                real_value = amount * 0.985 - 500
                            q.update(status="COMPLETE",
                                     amount=nl_data["total_amount"],
                                     token=nl_token,
                                     face_value=face_value,
                                     real_value=real_value,
                                     order_code=nl_data["order_code"],
                                     merchant_id=nl_data["transaction_id"])
                            return nl_data["total_amount"]
                        except Exception as ex:
                            return dict(error=str(ex) + " on line " + str(sys.exc_traceback.tb_lineno))
