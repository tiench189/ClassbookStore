def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/product/delete(ids, table) " + str(e)

def relation_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')

def relation_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')

def relation_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


# @auth.requires_login()
@auth.requires_authorize()
def index():
    # check_is_root()

    current_table = "clsb_product_relation"
#     if request.url.find('/clsb_product_relation/clsb_attention.') >= 0:
#         current_table = "clsb_attention"
    selectable = lambda ids: delete(ids, current_table)

    form = smartgrid(db.clsb_product_relation, 
                             oncreate = relation_on_create,
                             onupdate = relation_on_update,
                             ondelete = relation_on_delete,
                             showbuttontext = False, selectable=selectable, linked_tables = [])
    if form.element('.web2py_table input[type=submit]'):
        form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
        form.element('.web2py_table input[type=submit]')['_onclick'] = \
        "return confirm('"+ CONFIRM_DELETE +"');"
    return dict(form = form)

#update metadata value page number : cut out 'tr'
def update_metadata_page_number_value():
    regex1 = 'tr'
    regex2 = 'tr.'
    metadata_name = 'page_number'
    
#    try:
    metadata_id =  db(db.clsb_dic_metadata.metadata_name == metadata_name).select(db.clsb_dic_metadata.id)
    metadata_id = metadata_id[0].id
    
    rows = db(db.clsb_product_metadata.metadata_id == metadata_id).select(db.clsb_product_metadata.product_id,
                                                                          db.clsb_product_metadata.metadata_id,
                                                                          db.clsb_product_metadata.metadata_value )
    for row in rows:
        metadata_value = row['metadata_value']
        
        if metadata_value.find(regex1) != -1:
            metadata_value = metadata_value.replace(regex1, '')
        if metadata_value.find(regex2) != -1:
            metadata_value = metadata_value.replace(regex2,'')
        
        product_metadata_id = db((db.clsb_product_metadata.metadata_id == row['metadata_id']) &
                                 (db.clsb_product_metadata.product_id == row['product_id'])).select(db.clsb_product_metadata.id)
        if len(product_metadata_id) > 0:
            db(db.clsb_product_metadata.id == product_metadata_id[0].id).update(metadata_value = metadata_value)
    return dict(item='OK')
#    except Exception as e:
#        return dict(error = str(e))        

#update metadata_label = Khổ cỡ of metadata_name format
def update_metadata_name():
    metadata_name = 'format'
    metadata_label = 'Khổ cỡ'
    
    try:
        row = db(db.clsb_dic_metadata.metadata_name == metadata_name).select(db.clsb_dic_metadata.id)
        
        if len(row) >0 :
            db(db.clsb_dic_metadata.id == row[0].id).update(metadata_label = metadata_label)
        return dict(item='OK')
    except Exception as e:
        return dict(error=str(e)) 

# format and update value in clsb_product_metadata where metadata_name = format ex : 17x24cm -> 17 x 24cm
def update_metadata_format_value():    
    metadata_name = 'format'
    try:
        metadata_id = db(db.clsb_dic_metadata.metadata_name == metadata_name).select(db.clsb_dic_metadata.id).as_list()
        metadata_id = metadata_id[0]['id']
        
        rows = db(db.clsb_product_metadata == metadata_id).select(db.clsb_product_metadata.metadata_value,
                                                                   db.clsb_product_metadata.product_id, 
                                                                    db.clsb_product_metadata.metadata_id )
        for row in rows:
            metadata_value = row['metadata_value']
            if metadata_value.find('x') == -1 :
                continue
            metadata_value_tmp = metadata_value.split('x')
            metadata_value = metadata_value_tmp[0].strip() + ' x ' + metadata_value_tmp[1].strip()
            product_metadata_id = db((db.clsb_product_metadata.product_id == row['product_id']) & 
                      (db.clsb_product_metadata.metadata_id == row['metadata_id'])).select(db.clsb_product_metadata.id)
            if len(product_metadata_id) > 0:
                db(db.clsb_product_metadata.id==product_metadata_id[0].id).update(metadata_value = metadata_value)
        return dict(item='OK')
    except Exception as e:
        return dict(error=str(e))
    
def auto_update(): # arg: metadata_name
    #metadata_id, product_id, metadata_value
    metadata_name = 'key_word' #request.args(0)
    try:
        metadata_id = db(db.clsb_dic_metadata.metadata_name == metadata_name).select(db.clsb_dic_metadata.id).as_list()
        metadata_id = metadata_id[0]['id']
        
        rows = db(db.clsb_product_metadata.metadata_id == metadata_id).select(db.clsb_product_metadata.metadata_value,
                                                                              db.clsb_product_metadata.product_id)
        for row in rows:
            product_relation = db(db.clsb_product_metadata.metadata_value == row['metadata_value']).select(db.clsb_product_metadata.product_id)
            for line in product_relation:
                if line['product_id'] != row['product_id']:
                    db.clsb_product_relation.update_or_insert(product_id = row['product_id'], relation_id = line['product_id'])
        return dict(item='OK')
    except Exception as e:
        return dict(error=str(e))
    