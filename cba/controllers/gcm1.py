# @auth.requires_login()
#@auth.requires_authorize()
def index():
    # check_is_root()
    form = smartgrid(db.clsb_gcm, showbuttontext = False, selectable = lambda ids: select_for_send(ids))
    return dict(form=form)

def select_for_send(ids):
    redirect(URL('cba','gcm1', 'send1', args=ids))
    return


# @auth.requires_login()
@auth.requires_authorize()
def send1():
    # check_is_root()
    if "message" not in request.vars:
        list_device_serial = list()
        list_gcm_id = list()
        for s in request.args:
            device_serial = db(db.clsb_gcm.id == int(s)).select().first()
            list_device_serial.append(device_serial['serial'])
            list_gcm_id.append(device_serial['gcm_id'])
        session.list_device_serial = list_device_serial
        session.list_gcm_id = list_gcm_id
    if "message" in request.vars:
        message = request.vars.message
        list_gcm_id = list()
        list_gcm_id = session.list_gcm_id
#         devices = db(db.clsb_gcm.serial in list_device).select(db.clsb_gcm.gcm_id)
#         
#         dev_ids = list()
#         for dev in devices:
#             dev_ids.append(dev['gcm_id'])
#             print 'Id cua device : ' + dev['gcm_id']
#         
        import urllib2
        
        try:
            import json
        except ImportError:
            import simplejson as json
        for dev_ids in list_gcm_id :
            print 'dev_ids : ' +str(dev_ids)
            print message
            url = 'https://android.googleapis.com/gcm/send'
            values = {"data": {"message": message}, "registration_ids": dev_ids}
            headers = {'Authorization': 'key=' + GOOGLE_API_KEY,'Content-Type': 'application/json'}
                       
            try:
                data = json.dumps(values)
                req = urllib2.Request(url, data, headers)
                response = urllib2.urlopen(req)
                the_page = response.read()
                result = json.loads(the_page)
                print 'da gui xong'
                return result
            except Exception as ex:
                print str(ex)
                return dict(error=str(ex))
    return dict()