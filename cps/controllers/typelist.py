# -*- coding: utf-8 -*-
__author__ = 'tanbm'

def get():
    id = None
    if len(request.args) > 0:
        id = request.args[0]
    db_query = db(db.clsb20_product_type.parent_type == id).select()

    root = list()
    for row in db_query:
        temp = dict()
        temp['id'] = row.id
        temp['parent_type'] = row.parent_type
        temp['type_name'] = row.type_name
        temp['type_code'] = row.type_code
        temp['type_description'] = row.type_description
        root.append(temp)
    return dict(types=root)

def get_tree():
    try:
        if len(request.args)>0:
            id = int(request.args[0])
            db_query = db(db.clsb20_product_type.id == id).select()
        else:
            db_query = db(db.clsb20_product_type).select()
        root = list()
        if len(db_query) > 0:
            for row in db_query:
                temp = dict()
                temp['id'] = row.id
                temp['parent_type'] = row.parent_type
                temp['type_name'] = row.type_name
                temp['type_code'] = row.type_code
                temp['type_description'] = row.type_description
                get_child(temp)
                root.append(temp)

        return dict(types=root)
    except Exception as ex:
        return dict(error=ex.message)

def get_child(root):
    db_query = db((db.clsb20_product_type.parent_type == root['id'])&(db.clsb20_product_type.id != root['id'])).select()
    children = list()
    if len(db_query) > 0:
        for child in db_query:
            temp = dict()
            temp['id'] = child.id
            temp['parent_type'] = child.parent_type
            temp['type_name'] = child.type_name
            temp['type_code'] = child.type_code
            temp['type_description'] = child.type_description
            temp = get_child(temp)
            children.append(temp)
        root['children'] = children
    return root