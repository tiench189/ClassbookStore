#@author: hant

SUCCESS = CB_0000#cbMsg.CB_0000
EXISTENT = CB_0005#cbMsg.CB_0005
LACK_ARGS = CB_0002#cbMsg.CB_0002

myTable= db.clsb_warranty_device

def registed():
    if len(request.args) == 1:
        serial = request.args(0)
        realesed_device = db(db.clsb_warranty_device.device_serial == serial).select(db.clsb_warranty_device.ALL)
        if realesed_device:
            return dict(item=True)
        else:
            return dict(item=False)

def register():
    #the minimum required args
    nbargsrequired = 4

    #request = ../a/c/f/device_serial/full_name/email/purchase_date/phone/address
    if request.vars and not request.args:
        try:
            myTable.insert(**request.vars)
            return dict(item=SUCCESS)
        except Exception as e:
            if 'Duplicate entry' in str(e) and 'device_serial' in str(e):
                return dict(error=CB_0018)#DEVICE_EXISTED
            else:
                return dict(error=DB_RQ_FAILD)
    elif request.args and len(request.args) >= nbargsrequired and not request.vars:
        if db(myTable.device_serial.like(request.args(0))).select():
            return dict(error=EXISTENT)
        else:
            myTable.update_or_insert(
                                     device_serial=request.args(0), full_name=request.args(1), 
                                     register_date=request.now, email=request.args(2),
                                     purchase_date=request.args(3), phone=request.args(4),
                                     address=request.args(5) or "ND")
            return dict(item=SUCCESS)
    else:
        return dict(error=LACK_ARGS)