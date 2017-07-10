def index():
    response.view = 'generic.json'
    return dict(error="Trang này không tồn tại!")

@request.restful()
def api():
    response.view = 'generic.json'
    def GET(*args, **vars):
        return dict(error="Trang này không tồn tại!")
    def POST(*args, **vars):
        if len(args) != 1:
            return dict(error="Đối số không hợp lệ!")
        elif args[0] == 'register' and 'serial' in vars and 'gcmId' in vars:
            serial = vars["serial"]
            gcmId = vars["gcmId"]
            import pdf2dev
            if pdf2dev.isValidSerial(serial) is None:
                return dict(error=CB_0016, serial=serial)

            import urllib2
            try:
                import json
            except ImportError:
                import simplejson as json
                
            url = 'https://android.googleapis.com/gcm/send'
            values = {"data": {"register": "ok"}, "registration_ids": [gcmId]}
            headers = {'Authorization': 'key=' + GOOGLE_API_KEY, 'Content-Type': 'application/json'}

            try:
                # data = urllib.urlencode(values)
                data = json.dumps(values)
                req = urllib2.Request(url, data, headers)
                response = urllib2.urlopen(req)
                the_page = response.read()
                result = json.loads(the_page)
                if 'error' in result["results"][0]:
                    return dict(error=result["results"][0]['error'])
                device = db(db.clsb_gcm.serial == serial).select()
                if len(device) == 0:
                    result = db.clsb_gcm.update_or_insert(serial=serial, gcm_id=gcmId, created=datetime.now())
                else:
                    db(db.clsb_gcm.serial == serial).update(gcm_id=gcmId, created=datetime.now())
                    result = "SUCCESS"
                return dict(result=str(result))
            except Exception as ex:
                return dict(error=str(ex))
        elif args[0] == 'unregister' and 'serial' in vars:
            serial = vars["serial"]
            try:
                db(db.clsb_gcm.serial == serial).delete()
                return dict(result="ok")
            except Exception as ex:
                return dict(error=str(ex))
        else:
            return dict(error="Đối số không hợp lệ!")
    return locals()
