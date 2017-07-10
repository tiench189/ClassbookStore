#@author: hant
import sys
import fs.path

SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_class'
"""
    Get all classes by subject_code.
"""


def get(): # args: subject_code
    if not table in db.tables(): NOT_EXIST
    try:
        if request.args:
            subject_code = request.args(0)
            
            subject_id =  db(db.clsb_subject.subject_code == subject_code).select(db.clsb_subject.id).as_list()[0]['id']
            
            rows =  db(db.clsb_class.id == db.clsb_subject_class.class_id)\
                        (db.clsb_subject_class.subject_id == subject_id).select(db.clsb_class.ALL).as_list()
        else:
            rows =  db().select(db.clsb_class.ALL).as_list()

        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i]['class_order'])>int(rows[j]['class_order']):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp
        l = list()
        for row in rows:
            temp = dict()
            temp['id'] = row['id']
            temp['class_name'] = row['class_name']
            temp['class_code'] = row['class_code']
            temp['class_order'] = row['class_order']
            temp['class_description'] = row['class_description']
            l.append(temp)
        return dict(items=l)
    except Exception as e:
        return dict(error = str(e))


def subjects(): #args: class_id
    try:
        class_id = request.args(0)

        rows = db(db.clsb_subject.id == db.clsb_subject_class.subject_id)\
                    (db.clsb_subject_class.class_id == class_id).select(db.clsb_subject.ALL, db.clsb_subject_class.id).as_list()

#         return dict(d= rows)
        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i]['clsb_subject']['subject_order'])>int(rows[j]['clsb_subject']['subject_order']):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp
        l = list()
        for row in rows:
            temp = dict()
            temp['subject_id'] = row['clsb_subject']['id']
            temp['subject_name'] = row['clsb_subject']['subject_name']
            temp['subject_code'] = row['clsb_subject']['subject_code']
            temp['subject_order'] = row['clsb_subject']['subject_order']
            temp['subject_description'] = row['clsb_subject']['subject_description']
            temp['subject_class_id'] = row['clsb_subject_class']['id']
            l.append(temp)
        return dict(items=l)
    except Exception as e:
        return dict(error = str(e))


def subjects_from_category(): #args: category_id
    try:
        category_id = request.args(0)
        class_id = db(db.clsb20_category_class_mapping.category_id == category_id).select()
        if len(class_id) > 0:
            class_id = class_id.first().class_id
        else:
            return dict(items=[])
        rows = db(db.clsb_subject.id == db.clsb_subject_class.subject_id)\
                    (db.clsb_subject_class.class_id == class_id).select(db.clsb_subject.ALL, db.clsb_subject_class.id).as_list()

#         return dict(d= rows)
        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i]['clsb_subject']['subject_order'])>int(rows[j]['clsb_subject']['subject_order']):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp
        l = list()
        for row in rows:
            temp = dict()
            temp['subject_id'] = row['clsb_subject']['id']
            temp['subject_name'] = row['clsb_subject']['subject_name']
            temp['subject_code'] = row['clsb_subject']['subject_code']
            temp['subject_order'] = row['clsb_subject']['subject_order']
            temp['subject_description'] = row['clsb_subject']['subject_description']
            temp['subject_class_id'] = row['clsb_subject_class']['id']
            l.append(temp)
        return dict(items=l)
    except Exception as e:
        return dict(error = str(e))

# def getbid(): # args: subject_id
#     if not table in db.tables(): NOT_EXIST
#     try:
#         subject_id = request.args(0)
#         
# #         subject_id =  db(db.clsb_subject.subject_code == subject_code).select(db.clsb_subject.id).as_list()[0]['id']
# #         print subject_id
#         
#         rows =  db(db.clsb_class.id == db.clsb_subject_class.class_id)\
#                     (db.clsb_subject_class.subject_id == subject_id).select(db.clsb_class.ALL)
#         
# #         return dict(d= rows)
#         
#         l = list()
#         for row in rows:
#             temp = dict()
#             temp['id'] = row['id']
#             temp['class_name'] = row['class_name']
#             temp['class_code'] = row['class_code']
#             temp['class_order'] = row['class_order']
#             temp['class_description'] = row['class_description']
#             l.append(temp)
#         return dict(items=l)
#     except Exception as e:
#         return dict(error = str(e))