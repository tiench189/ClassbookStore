#@author: hant 08-03-2013

from gluon.tools import Auth
#import cbMsg
SUCCESS = CB_0000#cbMsg.CB_0000
LACK_ARGS = CB_0002#cbMsg.CB_0002
DB_RQ_FAILD = CB_0003#cbMsg.CB_0003

def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/home_topic/delete(ids, table) " + str(e)

def home_topic_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')

def home_topic_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')

def home_topic_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


# @auth.requires_login()
@auth.requires_authorize()
def index():
    # check_is_root()

    current_table = "clsb_home_topic"
    if request.url.find('/clsb_home_topic/clsb_home_topic_item.') >= 0:
        current_table = "clsb_home_topic_item"
    selectable = lambda ids: delete(ids, current_table)

    try:
        table = 'clsb_home_topic'
        if not table in db.tables(): redirect(URL('error'))
        form = smartgrid(db[table], 
                                 oncreate = home_topic_on_create,
                                 onupdate = home_topic_on_update,
                                 ondelete = home_topic_on_delete,
                                 linked_tables=['clsb_home_topic_item'],
                                 showbuttontext = False,
                                 user_signature = False,
                                 create=True, editable=True, details=True, 
                            #links=links,
                                selectable=selectable )
        if form.element('.web2py_table input[type=submit]'):
            form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
            form.element('.web2py_table input[type=submit]')['_onclick'] = \
            "return confirm('"+ CONFIRM_DELETE +"');"
        #return locals()
        return dict(form = form)
    except Exception as ex: 
        if request.is_local: 
            return ex 
        else: 
            raise HTTP(400)
