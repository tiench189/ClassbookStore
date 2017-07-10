"""
    Category controler: Manage categories
"""
import sys


def delete(ids, table):
    try:
        to_delete = db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/category/delete(ids, table) " + str(e)


def category_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')


def category_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')


def category_on_delete(table, record_id):
    db(db.clsb20_category_class_mapping.category_id == record_id).delete()
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')


# @auth.requires_login()
@auth.requires_authorize()
def index():
    # check_is_root()
    current_table = "clsb_category"
    if request.url.find('/clsb_category/clsb_product.') >= 0:
        current_table = "clsb_product"
    if request.url.find('/clsb_category/clsb_category.') >= 0:
        current_table = "clsb_category"
    if request.url.find('/clsb_category/clsb_home_topic.') >= 0:
        current_table = "clsb_home_topic"
    if request.url.find('clsb_category/new/clsb_category') >= 0:
        if len(request.args) > 3:
            parent_id = request.args[3]
            print(parent_id)
            return add_category(parent_id=parent_id)
        return add_category()
    if request.url.find('clsb_category/edit/clsb_category') >= 0:
        return edit_category()
    if current_table == "clsb_product" and isinstance(request.args[len(request.args) - 1], int):
        print request.args[len(request.args) - 1]
        selectable = (lambda ids: delete(ids, current_table)) if auth.has_permission('Delete', db.clsb_category,
                                                                                     request.args[len(
                                                                                         request.args) - 1]) else None
    else:
        selectable = None
    db.clsb_product.product_category.writable = False

    # in index page, to group all linked_tables into the selectbox and display only the fields listed
    if request.url.find('clsb_product.product_category') >= 0:
        fields = (db.clsb_product.product_category,
                  db.clsb_product.product_publisher,
                  db.clsb_product.product_creator,
                  db.clsb_product.product_title,
                  db.clsb_product.device_shelf_code)
        linked_tables = []
        grid = smartgrid(db.clsb_category, showbuttontext=False, selectable=selectable,
                         fields=fields, linked_tables=linked_tables,
                         create=False, deletable=True, details=False, editable=False)
    else:
        linked_tables = []
        if len(request.args) == 0 or request.args[len(request.args) - 1] == 'clsb_category':
            linked_tables = ['clsb_product']
        grid = smartgrid(db.clsb_category,
                         oncreate=category_on_create,
                         onupdate=category_on_update,
                         ondelete=category_on_delete,
                         showbuttontext=False, selectable=selectable, linked_tables=linked_tables)

    if grid.element('.web2py_table input[type=submit]'):
        grid.element('.web2py_table input[type=submit]')['_value'] = T('Delete')
        grid.element('.web2py_table input[type=submit]')['_onclick'] = \
            "return confirm('" + CONFIRM_DELETE + "');"
    return dict(grid=grid)


def add_category(parent_id=0):
    type = db(db.clsb_product_type).select()
    cat = db(db.clsb_category).select().as_list()
    root_cate = dict()
    root_cate['id'] = 0
    root_cate['category_name'] = 'Category gốc'
    root_cate['category_code'] = 'ROOT'
    cat.insert(0, root_cate)
    cls = db(db.clsb_class).select()
    p_id = None if int(parent_id) == 0 else parent_id
    max = db.clsb_category.category_order.max()
    try:
        max_order = db(db.clsb_category.category_parent == p_id).select(max).first()[max] + 1
    except Exception as err:
        max_order = 1
    grid = FORM(
        TABLE(
            TR(
                TD("Catagory Name:"),
                TD(INPUT(_name='name', _class='string', _placeholder='Category name'))
            ),
            TR(
                TD("Category Code:"),
                TD(INPUT(_name='code', _class='string', _placeholder='Category code'))
            ),
            TR(
                TD("Category Type:"),
                TD(SELECT(
                    *[OPTION(item['type_name'], _value=item['id']) for item in type],
                    _name='type', _class='string', _placeholder='Category type'))
            ),
            TR(
                TD("Order:"),
                TD(INPUT(_name='order', _class='string', _placeholder='Order', _value=max_order))
            ),
            TR(
                TD("Category Parent:"),
                TD(SELECT(
                    *[OPTION(item['category_name'], _value=item['id'],
                             _selected=True if item['id'] == int(parent_id) else False) for item in cat],
                    _name='parent', _class='string', _placeholder='Category Parent'))
            )
            ,
            TR(
                TD("Mapping Class:"),
                TD(SELECT(
                    *[OPTION(item['class_name'], _selected=True if item['class_code'].upper() == "NONE" else False,
                             _value=item['id']) for item in cls],
                    _name='class_id', _class='string', _placeholder='Mapping class'))
            ),
            TR(
                TD(),
                TD(INPUT(_type='submit', _value='Submit'))
            )
        ),
        _class='web2py_form'
    )
    if grid.accepts(request, session):
        try:
            if request.vars.parent == '0':
                parent = None
            else:
                parent = request.vars.parent
            data = db.clsb_category.insert(
                category_name=request.vars.name,
                category_code=request.vars.code,
                category_type=request.vars.type,
                category_order=request.vars.order,
                category_parent=parent
            )
            db.clsb20_category_class_mapping.insert(
                category_id=data.id,
                class_id=request.vars.class_id
            )
            auth.log_event(description='Create id ' + str(data.id) + ' in ' + 'clsb_category', origin='data')
            response.flash = 'Success'
        except Exception as err:
            print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
            response.flash = 'Error: ' + str(err) + " on line: " + str(sys.exc_traceback.tb_lineno)
    elif grid.errors:
        response.flash = 'Validate data'
    else:
        response.flash = 'Complete form'
    return dict(grid=grid)


def edit_category():
    type = db(db.clsb_product_type).select()
    cat = db(db.clsb_category).select().as_list()
    root_cate = dict()
    root_cate['id'] = 0
    root_cate['category_name'] = 'Category gốc'
    root_cate['category_code'] = 'ROOT'
    cat.insert(0, root_cate)
    print(cat)
    cls = db(db.clsb_class).select()
    dataOld = db(db.clsb_category.id == request.args[3]).select().first()
    class_map = db(db.clsb20_category_class_mapping.category_id == dataOld.id).select()
    if len(class_map) > 0:
        class_map = class_map.first().class_id
    else:
        class_map = "NONE"
    print class_map
    grid = FORM(
        TABLE(
            TR(
                TD("Catagory Name:"),
                TD(INPUT(_name='name', _class='string', _value=dataOld.category_name, _placeholder='Category name'))
            ),
            TR(
                TD("Category Code:"),
                TD(INPUT(_name='code', _class='string', _value=dataOld.category_code, _placeholder='Category code'))
            ),
            TR(
                TD("Category Type:"),
                TD(SELECT(
                    *[OPTION(item['type_name'], _value=item['id'],
                             _selected=True if dataOld.category_type == item['id'] else False) for item in type],
                    _name='type', _class='string', _placeholder='Category type'))
            ),
            TR(
                TD("Order:"),
                TD(INPUT(_name='order', _class='string', _placeholder='Order', _value='0'))
            ),
            TR(
                TD("Category Parent:"),
                TD(SELECT(
                    *[OPTION(item['category_name'], _value=item['id'],
                             _selected=True if dataOld.category_parent == item['id'] else False) for item in cat],
                    _name='parent', _class='string', _placeholder='Category Parent'))
            )
            ,
            TR(
                TD("Mapping Class:"),
                TD(SELECT(
                    *[OPTION(item['class_name'], _selected=True if (class_map == item['id']) | (
                        item['class_code'].upper() == str(class_map)) else False, _value=item['id']) for item in cls],
                    _name='class_id', _class='string', _placeholder='Mapping class'))
            ),
            TR(
                TD(),
                TD(INPUT(_type='submit', _value='Update'))
            )
        ),
        _class='web2py_form'
    )
    if grid.accepts(request, session):
        try:
            if request.vars.parent == '0':
                parent = None
            else:
                parent = request.vars.parent
            print(parent)
            data = db(db.clsb_category.id == dataOld.id).update(
                category_name=request.vars.name,
                category_code=request.vars.code,
                category_type=request.vars.type,
                category_order=request.vars.order,
                category_parent=parent
            )
            db(db.clsb20_category_class_mapping.category_id == dataOld.id).delete()
            db.clsb20_category_class_mapping.insert(
                category_id=dataOld.id,
                class_id=request.vars.class_id
            )
            auth.log_event(description='Update id ' + str(dataOld.id) + ' in ' + 'clsb_category', origin='data')
            session.flash = 'Success'
            redirect(URL(a='cba', c='category', f='index', user_signature=True))
        except Exception as err:
            print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
            response.flash = 'Error: ' + str(err) + " on line: " + str(sys.exc_traceback.tb_lineno)
    elif grid.errors:
        response.flash = 'Validate data'
    else:
        response.flash = 'Complete form'
    return dict(grid=grid)


def order_category():
    try:
        order_by_parent(None)
        # root_parent
        return
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def order_by_parent(parent):
    try:
        select_category = db(db.clsb_category.category_parent == parent).select(orderby=db.clsb_category.category_order)
        max_order = len(select_category)
        for cate in select_category:
            print(cate['category_name'])
            print(max_order)
            db(db.clsb_category.id == cate['id']).update(category_order=max_order)
            max_order -= 1
            order_by_parent(cate['id'])
        return
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


# @auth.requires_authorize()
def tree():
    try:
        mcategories = []
        db_query = db(db.clsb_category.category_parent == None)
        rows = db_query.select(db.clsb_category.id,
                               db.clsb_category.category_name,
                               db.clsb_category.category_order,
                               orderby=~db.clsb_category.category_order)
        for row in rows:
            temp = dict()
            temp['category_id'] = row['id']
            temp['category_name'] = row['category_name']
            temp['order'] = row['category_order']
            temp = get_categories(temp)
            mcategories.append(temp)
        expands = []
        # for cate in mcategories:
        #     get_expand_cate(expands, cate)
        return dict(mcategories=mcategories, expands=expands)
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def delete_category_by_id():
    try:
        category_id = request.args[len(request.args) - 1]
        auth.log_event(description='Delete id ' + str(category_id) + ' in clsb_category', origin='data')
        db(db.clsb_category.id == category_id).delete()
        print category_id
        return dict(result=True)
    except Exception as err:
        print(err)
        return dict(result=False, mess="Lỗi: " + str(err))


def get_categories(root):
    try:
        db_query = db(db.clsb_category.category_parent == root['category_id'])
        children = list()
        rows = db_query.select(db.clsb_category.id,
                               db.clsb_category.category_name,
                               db.clsb_category.category_order,
                               orderby=~db.clsb_category.category_order)
        for child in rows:
            temp = dict()
            temp['category_id'] = child['id']
            temp['category_name'] = child['category_name']
            temp['order'] = child['category_order']
            temp = get_categories(temp)
            children.append(temp)
        root['children'] = children
        return root
    except Exception as ex:
        import sys
        print(ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def up_order():
    try:
        cate_id = int(request.args[0])
        select_cate = db(db.clsb_category.id == cate_id).select().first()
        select_all = db(db.clsb_category.category_parent == select_cate['category_parent']).select(db.clsb_category.id,
                                                                                                   db.clsb_category.category_order,
                                                                                                   orderby=~db.clsb_category.category_order).as_list()
        for i in range(1, len(select_all)):
            if select_all[i]['id'] == cate_id:
                db(db.clsb_category.id == select_all[i]['id']).update(
                    category_order=select_all[i - 1]['category_order'])
                db(db.clsb_category.id == select_all[i - 1]['id']).update(
                    category_order=select_all[i]['category_order'])
                return dict(result=True)
        return dict(result=False)
    except Exception as ex:
        import sys
        print(ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(result=False, mess=ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def down_order():
    try:
        cate_id = int(request.args[0])
        select_cate = db(db.clsb_category.id == cate_id).select().first()
        select_all = db(db.clsb_category.category_parent == select_cate['category_parent']).select(db.clsb_category.id,
                                                                                                   db.clsb_category.category_order,
                                                                                                   orderby=~db.clsb_category.category_order).as_list()
        for i in range(0, len(select_all) - 1):
            if select_all[i]['id'] == cate_id:
                db(db.clsb_category.id == select_all[i]['id']).update(
                    category_order=select_all[i + 1]['category_order'])
                db(db.clsb_category.id == select_all[i + 1]['id']).update(
                    category_order=select_all[i]['category_order'])
                return dict(result=True)
        return dict(result=False)
    except Exception as ex:
        import sys
        print(ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(result=False, mess=ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))
