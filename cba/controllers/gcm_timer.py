__author__ = 'Tien'

import sys
import urllib2
import datetime


@auth.requires_authorize()
def index():
    form = SQLFORM.smartgrid(db.clsb30_gcm_timer,showbuttontext=False)
    return dict(form=form)


def check_timer():
    try:
        select_timer = db(db.clsb30_gcm_timer.gcm_timer < datetime.datetime.now()).select()
        if len(select_timer) == 0:
            return
        for timer in select_timer:
            send(timer['id'])
    except Exception as err:
        return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))


def send(timer_id):
    try:
        select_gcm = db(db.clsb30_gcm_timer.id == timer_id).select()
        if len(select_gcm) == 0:
            return
        gcm = select_gcm.first()
        db(db.clsb30_gcm_timer.id == timer_id).delete()
        list_gcm_id = list()
        if gcm['group_type'] == 'ANDROID_APP':
            select_device = db(db.clsb_gcm.serial.like("CA%")).select(db.clsb_gcm.gcm_id, distinct=True)
            for device in select_device:
                list_gcm_id.append(device['gcm_id'])
        else:
            select_device = db(~db.clsb_gcm.serial.like("CA%")).select(db.clsb_gcm.gcm_id, distinct=True)
            for device in select_device:
                list_gcm_id.append(device['gcm_id'])
        #list_gcm_id = ['APA91bEmvN2ZW2l04B1q34d7vsZF36vZmN7DFsvT05I_whMO8pbdGBwHYoAgEwpGHKKhAgMRJtXzxejM4K_Qpk_De-zZ6DdfNjhR7wnomR9VH2-JvkEBOT4den98w1K0VXoK9O6iji-H']
        action_send(list_gcm_id, gcm['gcm_message'], gcm['gcm_link'])
        return dict(list_gcm_id=list_gcm_id)
    except Exception as err:
        return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))


def action_send(list_gcm_id, message, link):
    try:
        size = 500
        split_gcm = [list_gcm_id[i:i+size] for i in range(0, len(list_gcm_id), size)]
        try:
            import json
        except ImportError:
            import simplejson as json
        #         for dev_ids in list_gcm_id :
        print message
        for list_split in split_gcm:
            url = 'https://android.googleapis.com/gcm/send'
            values = {"data": {"message": message, "link": link}, "registration_ids": list_split}
            headers = {'Authorization': 'key=' + GOOGLE_API_KEY, 'Content-Type': 'application/json'}
            try:
                data = json.dumps(values)
                req = urllib2.Request(url, data, headers)
                response = urllib2.urlopen(req)
                the_page = response.read()
                result = json.loads(the_page)
                #return result
            except Exception as ex:
                return dict(error=str(ex))
    except Exception as err:
        return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
