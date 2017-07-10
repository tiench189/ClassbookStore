#@author: hant 27-02-2013

"""
    Device_self (the name shelf was an error here) is a self to display products on devices.
    This service get the list of all device_self.
"""
def get():# software
#     software = request.args(0)
    
    try:
        rows = db().select(db.clsb_device_shelf.ALL, orderby=db.clsb_device_shelf.shelf_order).as_list()
        d = list()
        for row in rows:
            temp = dict()
            temp['device_self_name'] = row['device_shelf_name']
            temp['device_self_code'] = row['device_shelf_code']
            temp['device_self_type'] = row['device_shelf_type']
            temp['shelf_order'] = row['shelf_order']
            temp['description'] = row['description']

            d.append(temp)
        return dict(items=d)
    except Exception as e:
        return dict(error =  CB_0003 + str(e)) #DB_RQ_FAILD