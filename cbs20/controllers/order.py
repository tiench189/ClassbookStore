#@author: hant 

from gluon.tools import Auth
from datetime import datetime

# email_seller = "nhunt@tinhvan.com"
#email_seller = "hant@tinhvan.com"
email_seller = "order@edcom.vn"

"""
    Get all order in database.
"""
def get():# software
    try:
        rows = db().select(db.clsb_order.ALL, orderby = db.clsb_order.release_date).as_list()
        d = list()
        for row in rows:
            temp = dict()
            temp['customer_name'] = row['customer_name'] #notnull
            temp['email'] = row['email'] #notnull
            temp['phone'] = row['phone'] #notnull
            temp['address'] = row['address'] #notnull
            temp['number_devices'] = row['number_devices'] #notnull
            temp['order_date'] = str(row['order_date'])
            temp['note'] = row['note']
            temp['payment_type'] = str(row['payment_type'])
            
            d.append(temp)
        return dict(items=d)
    except Exception as e:
        return dict(error =  CB_0003 + str(e)) #DB_RQ_FAILD

"""
    Return cb price (found in /cbs/models/cb_constants.py).
"""    
def cb_price():
    return dict(cb_price=CB_PRICE)
    
"""
    Send email to EDC and client.
"""    
def send(): #vars: customer_name, email, phone, address, number_devices
    subject = "Xác nhận đơn đặt hàng ClassBook"
 #   print "-------------------------------------"
 #   print request.vars
#     customer_name = request.vars['customer_name']
#     phone = request.vars['phone']
#     note = request.vars['note'];
#     if request.vars['email']:
#         email = request.vars['email']
#     else:
#         email = ""
#     if request.vars['address']:
#         address = request.vars['address']
#     else:
#         address = ""
    number_devices = request.vars['number_devices']
#     date = str(datetime.now())
#    print number_devices
    try:
        if request.vars['unit_price']:
            request.vars.pop(unit_price)
        if request.vars['total_price']:
            request.vars.pop(total_price)
        
        request.vars.update({'unit_price':CB_PRICE})
        request.vars.update({'total_price':CB_PRICE*int(number_devices)})
        
#        print request.vars

        buyer_id = db.clsb_order.insert(**request.vars)

        buyer = db(db.clsb_order.id == buyer_id).select(db.clsb_order.ALL).as_list()
        number_devices = buyer[0]['number_devices']
        total = CB_PRICE * number_devices
        province = db(db.clsb_province.id == buyer[0]['province']).select(db.clsb_province.province_name).as_list()
        if province:
            province = province[0]['province_name']
        else:
            #print "province null"
        district = db(db.clsb_district.id == buyer[0]['district']).select(db.clsb_district.district_name).as_list()
#        print district
        if district:
            district = district[0]['district_name']
        else:
            #print "district null"
        
        context = dict(buyer=buyer, total = total, unit_price = CB_PRICE, province=province, district=district)
        message = response.render('template_bill.html', context)
 #       mail.send(to=[email_seller],
 #                 subject=subject,
 #                 message=message)
        
        #send email to confirm to buyer
        if request.vars.email :
            mail.send(to=[request.vars.email],
                  bcc=[email_seller],
                  subject=subject,
                  message=message)
            
        return dict(item=CB_0000)#SUCCESS
    except Exception as e:
        print e
        return dict(error =  CB_0003 + str(e)) #DB_RQ_FAILD
