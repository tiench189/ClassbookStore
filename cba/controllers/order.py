def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/order/delete(ids, table) " + str(e)

def device_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')

def device_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')

def device_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


@auth.requires_authorize()
def index():
    #check_is_root()

    current_table = "clsb_order"
    selectable = lambda ids: delete(ids, current_table)
    
    if check_root():
        form = smartgrid(db.clsb_order, 
                                 oncreate = device_on_create,
                                 onupdate = device_on_update,
                                 ondelete = device_on_delete,
                                 showbuttontext = False,
                                 exportclasses=dict(xml=False, html=False, csv_with_hidden_cols=False, csv=False, tsv_with_hidden_cols=False, tsv=False, json=False), fields=[db.clsb_order.id, db.clsb_order.customer_name, db.clsb_order.email, db.clsb_order.phone, db.clsb_order.address, db.clsb_order.number_devices, db.clsb_order.order_date])
    else:
        form = smartgrid(db.clsb_order, showbuttontext = False, deletable=False, editable=False, create=False,
                                 exportclasses=dict(xml=False, html=False, csv_with_hidden_cols=False, csv=False, tsv_with_hidden_cols=False, tsv=False, json=False), fields=[db.clsb_order.id, db.clsb_order.customer_name, db.clsb_order.email, db.clsb_order.phone, db.clsb_order.address, db.clsb_order.number_devices, db.clsb_order.order_date])
    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
        "return confirm('"+ CONFIRM_DELETE +"');"
    return dict(grid = form)