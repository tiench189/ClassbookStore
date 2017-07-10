#@author: hant
import sys
import fs.path
import json
import myredis

SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_subject'
def get():
    check_cache = myredis.get_cache(SUBJECT)
    if check_cache['result'] and check_cache['data'] is not None:
        data = json.loads(check_cache['data'])
        data['cache'] = True
        return data
    if not table in db.tables(): NOT_EXIST
    try:
        rows =  db().select(db.clsb_subject.ALL).as_list()
        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i]['subject_order'])>int(rows[j]['subject_order']):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp

        l = list()
        for row in rows:
            temp = dict()
            temp['id'] = row['id']
            temp['subject_name'] = row['subject_name']
            temp['subject_code'] = row['subject_code']
            temp['subject_order'] = row['subject_order']
            temp['subject_description'] = row['subject_description']

            l.append(temp)
        data = dict(items=l)
        myredis.write_cache(SUBJECT, str(json.dumps(data)), DEFAULT_TIME)
        data['cache'] = False
        return data
    except Exception as e:
        return dict(error = str(e))


def getbcatid():#args: cat_id
    if not table in db.tables(): NOT_EXIST
    try:
        cat_id = request.args(0)
        rows =  db(db.clsb_subject.subject_category == cat_id).select(db.clsb_subject.ALL)
        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i]['subject_order'])>int(rows[j]['subject_order']):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp
        l = list()
        for row in rows:
            temp = dict()
            temp['id'] = row['id']
            temp['subject_name'] = row['subject_name']
            temp['subject_code'] = row['subject_code']
            temp['subject_order'] = row['subject_order']
            temp['subject_description'] = row['subject_description']

            l.append(temp)
        return dict(items=l)
    except Exception as e:
        return dict(error = str(e))

def classes(): #args: subj_id
    try:
        subject_id = request.args(0)
        check_cache = myredis.get_cache(CLASSES + subject_id)
        if check_cache['result'] and check_cache['data'] is not None:
            data = json.loads(check_cache['data'])
            data['cache'] = True
            return data
#         subject_id =  db(db.clsb_subject.subject_code == subject_code).select(db.clsb_subject.id).as_list()[0]['id']
#         print subject_id
        
        rows =  db(db.clsb_class.id == db.clsb_subject_class.class_id)\
                    (db.clsb_subject_class.subject_id == subject_id).select(db.clsb_class.ALL, db.clsb_subject_class.id).as_list()
        
#         return dict(d= rows)
        lenR = len(rows)
        for i in range(0,lenR-1):
            for j in range(i+1, lenR):
                if int(rows[i]['clsb_class']['class_order'])>int(rows[j]['clsb_class']['class_order']):
                    tmp = rows[i]
                    rows[i] = rows[j]
                    rows[j] = tmp
        l = list()
        for row in rows:
            temp = dict()
            temp['class_id'] = row['clsb_class']['id']
            temp['class_name'] = row['clsb_class']['class_name']
            temp['class_code'] = row['clsb_class']['class_code']
            temp['class_order'] = row['clsb_class']['class_order']
            temp['class_description'] = row['clsb_class']['class_description']
            temp['subject_class_id'] = row['clsb_subject_class']['id']
            l.append(temp)
        data = dict(items=l)
        myredis.write_cache(CLASSES + subject_id, str(json.dumps(data)), DEFAULT_TIME)
        data['cache'] = False
        return data
    except Exception as e:
        return dict(error = str(e))