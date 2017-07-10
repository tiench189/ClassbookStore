# -*- coding: utf-8 -*-
__author__ = 'Tien'
import sys
from datetime import datetime, timedelta

def index():
    try:
        time_now = datetime.now()
        if request.vars and 'time' in request.vars:
            time_now = request.vars.time
            time_now = datetime.strptime(str(time_now), "%Y-%m-%d")
        time = datetime.strptime(str(time_now.year) + " " + str(time_now.month) + " " + str(time_now.day), "%Y %m %d")
        select_promotion = db(db.clsb30_event_promotion.created_on > time)\
                (db.clsb30_event_promotion.created_on < time + timedelta(days=1))\
                (db.clsb30_event_promotion.user_id == db.clsb_user.id)\
                (db.clsb30_event_promotion.product_id == db.clsb_product.id).select()
        promotions = list()
        for pr in select_promotion:
            temp = dict()
            temp['id'] = pr['clsb30_event_promotion']['id']
            temp['user'] = pr['clsb_user']['email']
            if pr['clsb_user']['type_user'] == "facebook":
                temp['user'] = pr['clsb_user']['lastName'] + " " + pr['clsb_user']['firstName']
            temp['type_user'] = pr['clsb_user']['type_user']
            temp['product'] = pr['clsb_product']['product_title']
            temp['created_on'] = pr['clsb30_event_promotion']['created_on']
            promotions.append(temp)
        return dict(promotions=promotions, time=time)
    except Exception as ex:
        return dict(result=False, error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def pick_user():
    try:
        list_id = list()
        if isinstance(request.vars.pick, list):
            list_id = request.vars.pick
        else:
            list_id.append(request.vars.pick)
        print(list_id)
        time = datetime.strptime(str(request.vars.time), "%Y-%m-%d")
        select_promotion = db(db.clsb30_event_promotion.id.belongs(list_id))\
                (db.clsb30_event_promotion.created_on > time)\
                (db.clsb30_event_promotion.created_on < time + timedelta(days=1))\
                (db.clsb30_event_promotion.user_id == db.clsb_user.id)\
                (db.clsb30_event_promotion.product_id == db.clsb_product.id).select()
        promotions = list()
        for pr in select_promotion:
            temp = dict()
            temp['id'] = pr['clsb30_event_promotion']['id']
            temp['user'] = pr['clsb_user']['email']
            if pr['clsb_user']['type_user'] == "facebook":
                temp['user'] = pr['clsb_user']['lastName'] + " " + pr['clsb_user']['firstName']
            temp['type_user'] = pr['clsb_user']['type_user']
            temp['product'] = pr['clsb_product']['product_title']
            temp['user_id'] = pr['clsb_user']['id']
            promotions.append(temp)
            try:
                db.clsb30_user_get_promotion.insert(product_id=pr['clsb_product']['id'],
                                                    user_id=pr['clsb_user']['id'],
                                                    time_get=time)
                db.clsb30_product_history.insert(product_title=pr['clsb_product']['product_title'],
                                                 product_price=0,
                                                 product_id=pr['clsb_product']['id'],
                                                 category_id=pr['clsb_product']['product_category'],
                                                 user_id=pr['clsb_user']['id'])
            except Exception as e:
                print(e)
        return dict(promotions=promotions)
    except Exception as ex:
        return dict(result=False, error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))


def send_noti():
    try:
        list_id = list()
        if isinstance(request.vars.user_id, list):
            list_id = request.vars.user_id
        else:
            list_id.append(request.vars.user_id)
        print(list_id)
        message = request.vars.message
        link = request.vars.link
        list_gcm_id = list()
        select_gcm = db(db.clsb_device.user_id.belongs(list_id))\
            (db.clsb_gcm.serial == db.clsb_device.device_serial).select()
        for gcm in select_gcm:
            list_gcm_id.append(gcm['clsb_gcm']['gcm_id'])

        import urllib2
        try:
            import json
        except ImportError:
            import simplejson as json
        url = 'https://android.googleapis.com/gcm/send'
        values = {"data": {"message": message, "link": link}, "registration_ids": list_gcm_id}
        headers = {'Authorization': 'key=' + GOOGLE_API_KEY, 'Content-Type': 'application/json'}
        try:
            data = json.dumps(values)
            req = urllib2.Request(url, data, headers)
            response = urllib2.urlopen(req)
            the_page = response.read()
            result = json.loads(the_page)
        except Exception as ex:
            print str(ex)
            response.flash = "error"
    except Exception as ex:
        return dict(result=False, error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))