def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/product_metadata/delete(ids, table) " + str(e)

def product_metadata_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')
    db.clsb30_update_product_log.insert(record_id=record_id, table_name=str(table), update_action="CREATE", update_status="INIT")


def product_metadata_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')
    db.clsb30_update_product_log.insert(record_id=record_id, table_name=str(table), update_action="UPDATE", update_status="INIT")

def product_metadata_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


# @auth.requires_login()
@auth.requires_authorize()
def index():
    # check_is_root()

    current_table = "clsb_product_metadata"
#     if request.url.find('/clsb_product_metadata/clsb_product.') >= 0:
#         current_table = "clsb_product"
#     print current_table
    selectable = lambda ids: delete(ids, current_table)
    
    form = smartgrid(db.clsb_product_metadata, 
                             showbuttontext = False, selectable = selectable,
                             onupdate = on_update,
                             oncreate = on_create,
                             orderby = db.clsb_product_metadata.created_on )
    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
        "return confirm('"+ CONFIRM_DELETE +"');"
    
    if request.url.find('clsb_product_metadata/new/clsb_product_metadata') >= 0 or request.url.find('clsb_product_metadata/edit/clsb_product_metadata') >= 0:

        # check product_metadata, if user selects 'classes' then we show the classes select box required
        metadata_id = db(db.clsb_dic_metadata.metadata_name == "classes").select(db.clsb_dic_metadata.ALL).as_list()[0]['id']
        
        # make the new metadata_value line (select box of classes)
        classes = db().select(db.clsb_class.class_code, db.clsb_class.class_name)
        
        label = LABEL( 'Metadata Value:', _for="clsb_product_metadata_metadata_value", _id="new_clsb_product_metadata_metadata_value__label")
    
        select = SELECT(_name='new_metadata_value', 
                        *[OPTION(classes[i].class_name, _value=str(classes[i].class_code)) for i in range(len(classes))])
        new_metadata_value_line = TR(TD(label, _class="w2p_f1"),
                          TD(select, _class="w2p_fw"),
                   _id="new_clsb_product_metadata_metadata_value__row")
        # and insert it to the form's table
        table = form.element('table')
        if form.element('tr', _id='clsb_product_metadata_metadata_id__row'):
            table[2].insert(2,new_metadata_value_line)
        
            # if Metadata 'classes' is selected 
            if form.element('option', _selected='selected', _value=str(metadata_id)):
                # if there has the metadata_value line (textarea)
                if form.element('tr', _id='clsb_product_metadata_metadata_value__row'):
                    # make its style to display:none 
                    form.element('tr', _id='clsb_product_metadata_metadata_value__row')['_style'] = "display: none;"
            # else, Metadata 'classes' isn't selected       
            else:
                # if there has the new_metadata_value line (select box of classes)
                if form.element('tr', _id='new_clsb_product_metadata_metadata_value__row'):
                    # make its style to display:none 
                    form.element('tr', _id='new_clsb_product_metadata_metadata_value__row')['_style'] = "display: none;"
            
            # set onchange to the select box clsb_product_metadata_metadata_id       
            if form.element('select', _id='clsb_product_metadata_metadata_id'):
                form.element('select', _id='clsb_product_metadata_metadata_id')['_onchange'] = "metadata_id_onchange("+ str(metadata_id) +");"
            else:
                print "KO2"
    
    return dict(grid = form)

def on_update(form):
    if request.url.find('clsb_product_metadata') >= 0 and request.vars.new_metadata_value and request.vars.metadata_value:
        db.clsb30_update_product_log.insert(record_id=request.vars.id, table_name="clsb_product_metadata", update_action="UPDATE", update_status="INIT")
        metadata_id = db(db.clsb_dic_metadata.metadata_name == "classes").select(db.clsb_dic_metadata.ALL).as_list()[0]['id']
        if int(request.vars.metadata_id) == int(metadata_id):
            request.vars.pop('metadata_value')
            d = dict(metadata_value=request.vars.pop('new_metadata_value'))
            request.vars.update(d)
            try:
                db.clsb_product_metadata.update_or_insert(db.clsb_product_metadata._id == request.vars.id, metadata_value=request.vars.metadata_value)
            except Exception as e:
                print e

def on_create(form):
    if request.url.find('clsb_product_metadata') >= 0 and request.vars.new_metadata_value and request.vars.metadata_value:
        metadata_id = db(db.clsb_dic_metadata.metadata_name == "classes").select(db.clsb_dic_metadata.ALL).as_list()[0]['id']
        if int(request.vars.metadata_id) == int(metadata_id):
            request.vars.pop('metadata_value')
            d = dict(metadata_value=request.vars.pop('new_metadata_value'))
            request.vars.update(d)
            try:
                # web2py log something then if we do just an insert the new value, there will have 2 records. Then we need to fake: let web2py insert first and update the last insert with our new value. 
                max_id = db(db.clsb_product_metadata).select(db.clsb_product_metadata.id.max()).first()[db.clsb_product_metadata.id.max()]
                oldval = db(db.clsb_product_metadata.id==max_id).select(db.clsb_product_metadata.metadata_value).first()['metadata_value']
                db.clsb30_update_product_log.insert(record_id=request.vars.max_id, table_name="clsb_product_metadata", update_action="CREATE", update_status="INIT")
                if(oldval == '<br>'):
                    db(db.clsb_product_metadata._id == max_id).update(metadata_value = request.vars.metadata_value)
            except Exception as e:
                print e