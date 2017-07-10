def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/creator/delete(ids, table) " + str(e)

def creator_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')

def creator_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')

def creator_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


# @auth.requires_login()
@auth.requires_authorize()
def index():
    # check_is_root()

    current_table = "clsb_dic_creator"
    if request.url.find('/clsb_dic_creator/clsb_product.') >= 0:
        current_table = "clsb_product"
#     print current_table
    selectable = lambda ids: delete(ids, current_table)

    form = smartgrid(db.clsb_dic_creator, 
                             oncreate = creator_on_create,
                             onupdate = creator_on_update,
                             ondelete = creator_on_delete,
                             showbuttontext = False, selectable=selectable, linked_tables = [])
    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
        "return confirm('"+ CONFIRM_DELETE +"');"
    return dict(form = form)
