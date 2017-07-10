def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/released_serial/delete(ids, table) " + str(e)

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


# @auth.requires_login()
@auth.requires_authorize()
def index():
    # check_is_root()

    current_table = "clsb_released_serial"
#     if request.url.find('/clsb_released_serial/clsb_product.') >= 0:
#         current_table = "clsb_product"
    selectable = lambda ids: delete(ids, current_table)
    
    form = smartgrid(db.clsb_released_serial, 
                             oncreate = device_on_create,
                             onupdate = device_on_update,
                             ondelete = device_on_delete,
                             showbuttontext = False, selectable=selectable )
    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
        "return confirm('"+ CONFIRM_DELETE +"');"
    return dict(grid = form)

"""
    The script to insert released serial in range of 121200001-121201015. 
"""
def insert():
    error = list()
    for serial in range(121200001, 121201016):
        try:
            db.clsb_released_serial.insert(released_serial=serial)
        except Exception as e:
            error.append(str(serial) + " " + str(e)) 
    return dict(error=error)     