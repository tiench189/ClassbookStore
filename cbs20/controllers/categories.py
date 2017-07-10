from applications.cba.modules import clsbUltils

"""
    Get all categories that root is given in parameter.
"""
def get_categories(root, show_on):
    db_query = db(db.clsb_category.category_type == db.clsb_product_type.id)
    db_query = db_query(db.clsb_category.category_parent == root['category_id'])
    children = list()

    rows = db_query.select(db.clsb_category.id,
                                db.clsb_category.category_name,
                                db.clsb_category.category_code,
                                db.clsb_product_type.type_name,
                                db.clsb_category.category_parent,
                                db.clsb_category.category_order,
                                orderby = db.clsb_category.category_order)
    lenR = len(rows)
    for i in range(0,lenR-1):
        for j in range(i+1, lenR):
            if int(rows[i].clsb_category.category_order)>int(rows[j].clsb_category.category_order):
                tmp = rows[i]
                rows[i] = rows[j]
                rows[j] = tmp

    for child in rows:
        if show_on == "":
            check_empty = db(db.clsb_product.product_category == child.clsb_category.id).select(db.clsb_product.id)
        else:
            check_empty = db(db.clsb_product.product_category == child.clsb_category.id)\
                    (db.clsb_product.show_on.like("%" + show_on + "%")).select(db.clsb_product.id)
        if len(check_empty) > 0:
            temp = dict()
            temp['category_id'] = child.clsb_category.id
            temp['category_name'] = child.clsb_category.category_name
            temp['category_code'] = child.clsb_category.category_code
            temp['category_parent'] = child.clsb_category.category_parent
            temp['category_type'] = child.clsb_product_type.type_name
            temp['category_order'] = child.clsb_category.category_order
            temp = get_categories(temp, show_on)
            children.append(temp)
    root['children'] = children
    return root

"""

"""
def getall():
    try:
        categories = list()
        rows = db(db.clsb_category.category_type == db.clsb_product_type.id)\
                (db.clsb_category.category_parent == None).select(db.clsb_category.id, 
                                                                            db.clsb_category.category_name, 
                                                                            db.clsb_category.category_code,
                                                                            db.clsb_product_type.type_name,
                                                                            db.clsb_category.category_order,
                                                                            orderby = db.clsb_category.category_order)
        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i].clsb_category.category_order)>int(rows[j].clsb_category.category_order):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp

        for row in rows:
            temp = dict()
            temp['category_id'] = row.clsb_category.id
            temp['category_name'] = row.clsb_category.category_name
            temp['category_code'] = row.clsb_category.category_code
            temp['category_type'] = row.clsb_product_type.type_name
            temp['category_order'] = row.clsb_category.category_order
            categories.append(temp)
        return dict(categories=categories)
    except Exception as e:
       redirect(clsbUltils.get_error_link('cba', 'default', 'error', e, request.is_local))

def get():
    try:
        root = list()
        db_query = db(db.clsb_category.category_type == db.clsb_product_type.id)
        if request.args:
            root_id = None
            if request.args[0] != '0':
                root_id = request.args[0]
                
            if len(request.args) == 1:
                db_query = db_query(db.clsb_category.category_parent == root_id)
            else:
                db_query = db_query((db.clsb_category.category_type == request.args[1])
                                 & (db.clsb_category.category_parent == root_id))
        else:
            db_query = db_query(db.clsb_category.category_parent == None)
        rows = db_query.select(db.clsb_category.id,
                                db.clsb_category.category_name,
                                db.clsb_category.category_code,
                                db.clsb_product_type.type_name,
                                db.clsb_category.category_order,
                                orderby = db.clsb_category.category_order)

        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i].clsb_category.category_order)>int(rows[j].clsb_category.category_order):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp

        for row in rows:
            temp = dict()
            temp['category_id'] = row.clsb_category.id
            temp['category_name'] = row.clsb_category.category_name
            temp['category_code'] = row.clsb_category.category_code
            temp['category_type'] = row.clsb_product_type.type_name
            temp['category_order'] = row.clsb_category.category_order
            root.append(temp)
        return dict(categories = root)
    except Exception as ex: 
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))

def get_category_name():
    try:
        db_query = db(db.clsb_category.id == request.args[0]).select(db.clsb_category.category_name).first()
        return db_query.category_name
    except Exception as ex:
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))

def get_tree():
    try:
        except_id = []
        show_on = ""
        if request.vars and "version" in request.vars:
            show_on = request.vars.version
            #if "ANDROID_APP" in request.vars.version:
            #    isWindow = True
            #    except_id = [86, 83, 3]
        isWindow = False
        if request.vars and "app_version" in request.vars:
            if "WINDOWAPP" in request.vars.app_version:
                isWindow = True
                except_id = [86, 83, 3]
        root = list()
        db_query = db(db.clsb_category.category_type == db.clsb_product_type.id)
        if request.args:
            root_id = request.args[0]
            db_query = db_query(db.clsb_category.id == root_id)
        else:
            db_query = db_query(db.clsb_category.category_parent == None)
        rows = db_query.select(db.clsb_category.id,
                                db.clsb_category.category_name,
                                db.clsb_category.category_order,
                                db.clsb_category.category_code,
                                db.clsb_category.category_parent,
                                db.clsb_product_type.type_name,
                                orderby = db.clsb_category.category_order)
        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i].clsb_category.category_order)>int(rows[j].clsb_category.category_order):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp

        for row in rows:
            temp = dict()
            if not int(row.clsb_category.id) in except_id:
                temp['category_id'] = row.clsb_category.id
                temp['category_name'] = row.clsb_category.category_name
                temp['category_order'] = row.clsb_category.category_order
                temp['category_parent'] = row.clsb_category.category_parent if row.clsb_category.category_parent else 0
                temp['category_code'] = row.clsb_category.category_code
                temp['category_type'] = row.clsb_product_type.type_name
                temp = get_categories(temp, show_on)
                root.append(temp)
        return dict(categories = root)
    except Exception as ex:
        print(ex)
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))

def search():
    try:
        root = list()
        page = 0
        items_per_page = settings.items_per_page
        if request.args:
            root_key = request.args[0]
            
            #Pagination
            try:
                if len(request.args) > 1: page = int(request.args[1])
                if len(request.args) > 2: items_per_page = int(request.args[2])
            except (TypeError, ValueError): pass
            limitby = (page * items_per_page, (page + 1) * items_per_page)
            
            root = db((db.clsb_category.category_code == root_key) | (db.clsb_category.category_name.like('%' + root_key + '%'))).select(db.clsb_category.id,
                                                                                                                                         db.clsb_category.category_name, 
                                                                                                                                         db.clsb_category.category_code, 
                                                                                                                                         limitby = limitby,
                                                                                                                                         orderby = db.clsb_category.category_order).as_list()
        return dict(page = page, items_per_page = items_per_page, categories = root)
    except Exception as ex: 
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))