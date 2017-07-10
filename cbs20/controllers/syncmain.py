# -*- coding: utf-8 -*-

__author__ = 'Tien'

import urllib2
import json
import sys
import os.path

FILE_CHECK = settings.home_dir + "run_sync.txt"

def test():
    user = db(db.clsb_user.email == 'tien@tinhvan.com').select().first()
    for key in user.keys():
        print(key)
    return dict()

def run_sign_record(record_id, table_name, key_unique, data_source):
    url_get_data = URL(host=data_source, a='cbs20', c="syncmain", f="get_data_from_log.json",
                              vars=dict(record_id=record_id, table_name=table_name, key_unique=key_unique))
    print(url_get_data)
    get_data = urllib2.urlopen(url_get_data)
    str_json = str(get_data.read())
    print("str json: " + str_json)
    get_data = json.loads(str_json)
    get_data['table_name'] = table_name
    print("get_data: " + str(get_data))
    result = run_data_to_db(get_data)
    if result['error']:
        result['error'] = result['error'] + " " + url_get_data
    return result

def sign_record():#record_id, table_name, data_source, key_unique
    record_id = request.vars.record_id
    table_name = request.vars.table_name
    data_source = request.vars.data_source
    key_unique = request.vars.key_unique

    url_get_data = URL(host=data_source, a='cbs20', c="syncmain", f="get_data_from_log.json",
                              vars=dict(record_id=record_id, table_name=table_name, key_unique=key_unique))
    print(url_get_data)
    get_data = urllib2.urlopen(url_get_data)
    str_json = str(get_data.read())
    print("str json: " + str_json)
    get_data = json.loads(str_json)
    get_data['table_name'] = table_name
    print("get_data: " + str(get_data))
    result = run_data_to_db(get_data)
    if result['error']:
        result['error'] = result['error'] + " " + url_get_data
    return result

def insert_data_to_db():
    get_data = request.vars
    unique = get_data['unique']
    data = get_data['data']
    table_name = get_data['table_name']
    if 'username' in unique:
        user = db(db.clsb_user.username == unique['username']).select()
        if len(user) == 0:
            return dict(result=False, error=CB_0001)
        user = user.first()
        if 'user_id' in data:
            data['user_id'] = user['id']
            unique['user_id'] = user['id']
        if 'username' not in data:
            del unique['username']
        # return dict(data=data)
    query_unique = ""
    for key in unique.keys():
        if table_name != 'clsb_device' or key != 'user_id':
            if unique.keys().index(key) > 0:
                query_unique += " AND "
            query_unique += str(key) + "='" + str(unique[key]) + "'"
    check_exist = False
    if len(unique) > 0:
        check_data = db.executesql("SELECT * FROM " + table_name + " WHERE " + query_unique)
        if len(check_data) > 0:
            check_exist = True
    print(check_exist)
    if check_exist:
        query_data_update = "UPDATE " + table_name + " SET "
        for key in data.keys():
            if key not in unique:
                if data.keys().index(key) > 0:
                    query_data_update += ","
                if data[key] == None:
                    query_data_update += str(key) + "=null"
                else:
                    query_data_update += str(key) + "='" + str(data[key]) + "'"
        query_data_update += " WHERE " + query_unique
        print(query_data_update)
        try:
            db.executesql(query_data_update)
            return dict(result=True)
        except Exception as err:
            return dict(result=False, error=str(err))
    else:
        str_field = ""
        str_value = ""
        for key in data.keys():
            if data.keys().index(key) > 0:
                str_field += ","
                str_value += ","
            str_field += str(key)
            if data[key] == None:
                str_value += "null"
            else:
                str_value += "'" + str(data[key]) + "'"
        query_data_insert = "INSERT INTO " + table_name + "(" + str_field + ") VALUES (" + str_value + ")"
        print(query_data_insert)
        try:
            db.executesql(query_data_insert)
            return dict(result=True)
        except Exception as err:
            return dict(result=False, error=str(err))
    return dict()

def run_data_to_db(get_data):
    query_bug = ""
    try:
        unique_data = get_data['unique']
        data = get_data['data']
        table_name = get_data['table_name']
        if 'username' in unique_data:
            user = db(db.clsb_user.username == unique_data['username']).select()
            if len(user) == 0 and table_name != 'clsb_user':
                return dict(result=False, error=CB_0001)
            if len(user) > 0:
                user = user.first()
                if 'user_id' in data:
                    data['user_id'] = user['id']
                    unique_data['user_id'] = user['id']
                if 'username' not in data:
                    del unique_data['username']
            # return dict(data=data)
        query_unique = ""
        for key in unique_data.keys():
            if table_name != 'clsb_device' or key != 'user_id':
                if query_unique != "":
                    query_unique += " AND "
                query_unique += str(key) + "='" + str(unique_data[key]) + "'"
        check_exist = False
        query_bug = "SELECT * FROM " + table_name + " WHERE " + query_unique
        if len(unique_data) > 0:
            check_data = db.executesql("SELECT * FROM " + table_name + " WHERE " + query_unique)
            if len(check_data) > 0:
                check_exist = True
        print("exist: " + str(check_exist))
        if check_exist:
            query_data_update = "UPDATE " + table_name + " SET "
            data_update = ""
            for key in data.keys():
                if key not in unique_data:
                    print(key)
                    if data_update != "":
                        data_update += ","
                    if data[key] == None:
                        data_update += str(key) + "=null"
                    else:
                        try:
                            data_update += str(key) + "='" + data[key].encode('utf-8') + "'"
                        except Exception as err:
                            try:
                                data_update += str(key) + "='" + str(data[key]) + "'"
                            except Exception as e:
                                print("ERR: " + str(e))
                        print(data_update)
            query_data_update += data_update
            query_data_update += " WHERE " + query_unique
            print(query_data_update)
            query_bug = query_data_update
            try:
                db.executesql(query_data_update)
                return dict(result=True)
            except Exception as err:
                print('err sql: ' + str(err))
                return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
        else:
            str_field = ""
            str_value = ""
            for key in data.keys():
                if data.keys().index(key) > 0:
                    str_field += ","
                    str_value += ","
                str_field += str(key)
                print("data " + str(key) + ": ")
                if data[key] == None:
                    str_value += "null"
                else:
                    try:
                        str_value += "'" + data[str(key)].encode("utf-8") + "'"
                    except Exception as err:
                        print(err)
                        str_value += "'" + str(data[str(key)]) + "'"
            query_data_insert = "INSERT INTO " + table_name + "(" + str_field + ") VALUES (" + str_value + ")"
            print(query_data_insert)
            query_bug = query_data_insert
            try:
                db.executesql(query_data_insert)
                return dict(result=True)
            except Exception as err:
                return dict(result=False, error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
    except Exception as err:
        return dict(result=False, error=str(err) + " - " + query_bug + " on line: "+str(sys.exc_traceback.tb_lineno) + ":" + str(get_data))


def insert_to_log(): #record_id, table_name, data_source, key_unique
    if request.vars:
        record_id = request.vars.record_id
        table_name = request.vars.table_name
        data_source = request.vars.data_source
        key_unique = request.vars.key_unique
        try:
            check_log = db(db.clsb30_sync_log.record_id == record_id)\
                    (db.clsb30_sync_log.table_name == table_name)\
                    (db.clsb30_sync_log.data_source == data_source).select()
            if len(check_log) == 0:
                log_id = db.clsb30_sync_log.insert(record_id=record_id, table_name=table_name,
                                          data_source=data_source, status=INIT, key_unique=key_unique)
            #db(db.clsb30_sync_log.record_id == record_id)(db.clsb30_sync_log.table_name == table_name).update(description="test-" + log_id['id'])
            #url_sign = "http://127.0.0.1/cbs20/syncmain/run_sync_log_by_id/" + str(log_id['id'])
            #data_sign = urllib2.urlopen(url_sign)
            #try:
            #   db(db.clsb30_sync_log.record_id == record_id)(db.clsb30_sync_log.table_name == table_name).update(description=url_sign + ":" + data_sign.read())
            #except Exception as err:
            #    print(err)
            #data = sync_log_by_id(log_id['id'])
            return dict(result=True, id=log_id['id'])
        except Exception as err:
            return dict(result=False, err=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
    return dict(result=False, err="UNKNOWN")

def insert_to_temp(): #record_id, table_name, key_unique
    if request.vars:
        record_id = request.vars.record_id
        table_name = request.vars.table_name
        key_unique = request.vars.key_unique
        try:
            temp = db.clsb30_sync_temp.insert(record_id=record_id, table_name=table_name,
                                    status=INIT, key_unique=key_unique)
            sync_temp_by_id(temp['id'])
            return dict(result=True)
        except Exception as err:
            return dict(result=False, err=str(err))
    return dict(result=False, err="UNKNOWN")

def run_temp_by_id():
    try:
        temp_id = request.args[0]
        temp = db(db.clsb30_sync_temp.id == temp_id)\
                 (db.clsb30_sync_temp.status == INIT).select()
        if len(temp) == 0:
            return "no record"
        temp = temp.first()
        db(db.clsb30_sync_temp.id == temp['id']).update(status=PROCESS)

        url_import = URL(host=MAIN_SERVER, a='cbs20', c="syncmain", f="insert_to_log.json",
                                  vars=dict(record_id=temp['record_id'], table_name=temp['table_name'],
                                            data_source=CURRENT_SERVER, key_unique=temp['key_unique']))
        print(url_import)
        get_data = urllib2.urlopen(url_import)
        get_data = json.loads(get_data.read())
        if get_data['result'] == True:
            db(db.clsb30_sync_temp.id == temp['id']).delete()
        else:
            db(db.clsb30_sync_temp.id == temp['id']).update(status=INIT, description=get_data['error'])
        return True
    except Exception as err:
        print(err)
        db(db.clsb30_sync_temp.id == temp['id']).update(status=INIT, description=str(err))
        return dict(error=str(err))
def sync_temp_by_id(temp_id):
    try:
        temp = db(db.clsb30_sync_temp.id == temp_id)\
                 (db.clsb30_sync_temp.status == INIT).select()
        if len(temp) == 0:
            return "no record"
        temp = temp.first()
        db(db.clsb30_sync_temp.id == temp['id']).update(status=PROCESS)

        url_import = URL(host=MAIN_SERVER, a='cbs20', c="syncmain", f="insert_to_log.json",
                                  vars=dict(record_id=temp['record_id'], table_name=temp['table_name'],
                                            data_source=CURRENT_SERVER, key_unique=temp['key_unique']))
        print(url_import)
        get_data = urllib2.urlopen(url_import)
        get_data = json.loads(get_data.read())
        if get_data['result'] == True:
            db(db.clsb30_sync_temp.id == temp['id']).delete()
        else:
            db(db.clsb30_sync_temp.id == temp['id']).update(status=INIT, description=get_data['error'])
        return True
    except Exception as err:
        print(err)
        db(db.clsb30_sync_temp.id == temp['id']).update(status=INIT, description=str(err))
        return dict(error=str(err))

def import_temp_to_log():
    print("import temp")
    temp_list = db(db.clsb30_sync_temp.status == INIT).select(limitby=(0, 5))
    for temp in temp_list:
        db(db.clsb30_sync_temp.id == temp['id']).update(status=PROCESS)
        try:
            url_import = URL(host=MAIN_SERVER, a='cbs20', c="syncmain", f="insert_to_log.json",
                                  vars=dict(record_id=temp['record_id'], table_name=temp['table_name'],
                                            data_source=CURRENT_SERVER, key_unique=temp['key_unique']))
            print(url_import)
            get_data = urllib2.urlopen(url_import)
            get_data = json.loads(get_data.read())
            if get_data['result'] == True:
                db(db.clsb30_sync_temp.id == temp['id']).delete()
            else:
                db(db.clsb30_sync_temp.id == temp['id']).update(status=INIT, description=get_data['error'])
        except Exception as err:
            print(err)
            db(db.clsb30_sync_temp.id == temp['id']).update(status=INIT, description=str(err))
    return dict()

def run_sync_log_by_id():
    url_sign_record = ""
    try:
        log = db(db.clsb30_sync_log.id == request.args[0]).select()
        if len(log) == 0:
            return "No record"
        log = log.first()
        db(db.clsb30_sync_log.id == log['id']).update(status=PROCESS)
        server = ""
        if log['data_source'] == "classbook.vn":
            server = "127.0.0.1"
        elif log['data_source'] == "123.30.179.205":
            server = "classbook.vn"
        elif log['data_source'] == "app.classbook.vn":
            server = "classbook.vn"
        if server == "127.0.0.1":
            url_get_data = URL(host=log['data_source'], a='cbs20', c="syncmain", f="get_data_from_log.json",
                              vars=dict(record_id=log['record_id'], table_name=log['table_name'], key_unique=log['key_unique']))
            url_sign_record = url_get_data
            print(url_get_data)
            get_data = urllib2.urlopen(url_get_data)
            str_json = str(get_data.read())
            print("str json: " + str_json)
            get_data = json.loads(str_json)
            get_data['table_name'] = log['table_name']
            print("get_data: " + str(get_data))
            run = run_data_to_db(get_data)
        else:
            url_sign_record = URL(host=server, a='cbs20', c="syncmain", f="sign_record.json",
                        vars=dict(record_id=log['record_id'], table_name=log['table_name'], key_unique=log['key_unique'], data_source=log['data_source']))
            print url_sign_record
            run = json.loads(urllib2.urlopen(url_sign_record).read())
        print(run)
        if run['result']:
            db(db.clsb30_sync_log.id == log['id']).delete()
            # return dict(result=True)
        else:
            db(db.clsb30_sync_log.id == log['id']).update(status=INIT, description=run['error'])
            # return dict(result=True)
        return run
    except Exception as err:
        print("Error: " + str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
        db(db.clsb30_sync_log.id == log['id']).update(status=INIT,
                                                description=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno) + ":" + url_sign_record)
        return str(err) + " on line: " + str(sys.exc_traceback.tb_lineno) + ":" + url_sign_record
    #return True

def sync_log_by_id(id_log):
    url_sign_record = ""
    try:
        log = db(db.clsb30_sync_log.id == id_log).select()
        if len(log) == 0:
            return "No record"
        log = log.first()
        #db(db.clsb30_sync_log.id == log['id']).update(status=PROCESS)
        server = ""
        if log['data_source'] == "classbook.vn":
            server = "127.0.0.1"
        elif log['data_source'] == "123.30.179.205":
            server = "classbook.vn"
        elif log['data_source'] == "app.classbook.vn":
            server = "classbook.vn"
        if server == "127.0.0.1":
            url_get_data = URL(host=log['data_source'], a='cbs20', c="syncmain", f="get_data_from_log.json",
                              vars=dict(record_id=log['record_id'], table_name=log['table_name'], key_unique=log['key_unique']))
            url_sign_record = url_get_data
            print(url_get_data)
            get_data = urllib2.urlopen(url_get_data)
            str_json = str(get_data.read())
            print("str json: " + str_json)
            get_data = json.loads(str_json)
            get_data['table_name'] = log['table_name']
            print("get_data: " + str(get_data))
            run = run_data_to_db(get_data)
        else:
            url_sign_record = URL(host=server, a='cbs20', c="syncmain", f="sign_record.json",
                        vars=dict(record_id=log['record_id'], table_name=log['table_name'], key_unique=log['key_unique'], data_source=log['data_source']))
            print url_sign_record
            run = json.loads(urllib2.urlopen(url_sign_record).read())
        print(run)
        if run['result']:
            db(db.clsb30_sync_log.id == log['id']).delete()
            # return dict(result=True)
        else:
            db(db.clsb30_sync_log.id == log['id']).update(status=INIT, description=run['error'])
            # return dict(result=True)
        return run
    except Exception as err:
        print("Error: " + str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
        db(db.clsb30_sync_log.id == log['id']).update(status=INIT,
                                                description=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno) + ":" + url_sign_record)
        return str(err) + " on line: " + str(sys.exc_traceback.tb_lineno) + ":" + url_sign_record

def run_sync_log():
    #if check_sync_run():
    #    check_file = open(FILE_CHECK, "r")
    log_list = db(db.clsb30_sync_log.status == INIT).select(limitby=(0, 5))
    for log in log_list:
        sync_log_by_id(log['id'])
        #check_continue = db(db.clsb30_sync_log.status == INIT).select()
        #if len(check_continue) > 0:
        #    #run_sync_log()
        #    print "continue"
        #else:
        #    os.remove(FILE_CHECK)
        #    return dict(result=True)
    return dict(result=True)

def check_sync_run():
    if os.path.exists(FILE_CHECK):
        return True
    return False

def get_data_from_log(): #record_id, table_name, key_unique
    response.generic_patterns = ['*']
    if request.vars:
        record_id = request.vars.record_id
        table_name = request.vars.table_name
        key_unique = request.vars.key_unique
        try:
            data_result = db.executesql("SELECT * FROM " + table_name + " WHERE id =" + record_id, as_dict=True)
            if len(data_result) == 0:
                return dict(result=False, err="no record")
            print(data_result[0])
            data = data_result[0]
            del data['id']
            unique_dict = dict()
            for unique in key_unique.split('.'):
                if unique == 'user_id':
                    user = db(db.clsb_user.id == data['user_id']).select().first()
                    unique_dict['username'] = user['username']
                else:
                    unique_dict[unique] = data[unique]
            return dict(data=data, unique=unique_dict)
        except Exception as err:
            return dict(result=False, err=str(err))
    return dict(result=False, err="UNKNOWN")

def import_data():
    print(db.clsb_user)
    return dict()

def test_split():
    str_test = request.args[0]
    return dict(result=str_test.split('.'))

def test_update():
    res = db(db.clsb30_sync_temp.record_id == 13641).update(description='test')
    return dict(id=res)

def test_url():
    import urllib2
    try:
        get_data = urllib2.urlopen("https://127.0.0.1")
        return dict(data=get_data.read())
    except Exception as err:
        return dict(err=str(err))

def test_select_desc():
    print db(db.clsb_user.id > 0).select(limitby=(0, 5), orderby="id DESC")
    return True

def test_connect_db():
    try:
        db_sync = DAL(settings.database_sync,
                        pool_size=1, check_reserved=['all'],
                        migrate_enabled=settings.migrate, decode_credentials=True, db_codec='UTF-8')
        check = db_sync.executesql("SELECT * FROM clsb_user WHERE username like '%tien%'")
        return dict(result=len(check))
    except Exception as err:
        return dict(error=str(err))

def test_sleep():
    import time
    print("a")
    time.sleep(3)
    test_sleep()

def sync():
    while(True):

    return sync_a_record()


