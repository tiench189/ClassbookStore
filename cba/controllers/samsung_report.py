# -*- coding: utf-8 -*-
""" Reports
    Theo dõi thống kê dữ liệu, doanh thu, lượt tải...
"""

__author__ = 'tiench'
import scripts
import usercp
samsung_query = (db.clsb_user.id == db.clsb30_gift_code_log.user_id)

@auth.requires_authorize()
def index():
    try:
        import math
        import calendar
        by_year = False
        by_day = False
        by_month = False
        if request.vars.getbyyear:
            if request.vars.getbyyear == "1":
                by_year = True
            elif request.vars.getbyyear == "2":
                by_month = True
            elif request.vars.getbyyear == "3":
                by_day = True
            else:
                by_month = True
        else:
            by_month = True


        start = datetime.strptime(str(datetime.now().year), "%Y")
        if by_day:
            start = datetime.strptime(str(datetime.now().month) + "-" + str(datetime.now().year), "%m-%Y")
        end = datetime.now()
        if request.vars.start:
            if by_year:
                start = datetime.strptime(request.vars.start, "%Y")
            elif by_month:
                start = datetime.strptime(request.vars.start, "%m-%Y")
            elif by_day:
                start = datetime.strptime(request.vars.start, "%d-%m-%Y")

        if request.vars.end:
            if by_year:
                end = datetime.strptime("31-12-" + str(request.vars.end), "%d-%m-%Y")
            elif by_month:
                end = datetime.strptime(request.vars.end, "%m-%Y")
                end = datetime.strptime(str(calendar.monthrange(end.year, end.month)[1]) + "-" + request.vars.end, "%d-%m-%Y")
            elif by_day:
                end = datetime.strptime(request.vars.end, "%d-%m-%Y")

        maxMonth = datetime.now().month
        maxYear = datetime.now().year

        data = list()
        percent = list()
        if end.year < maxYear:
            maxYear = end.year
            maxMonth = 12
        if end.month != maxMonth:
            maxMonth = end.month
        for y in range(start.year, maxYear+1):
            max = maxMonth
            min = 1
            if y == start.year:
                min = start.month
            if y < maxYear:
                max = 12
            if by_year:
                temp = list()
                temp.append(str(y))
                timeStart = datetime.strptime(str(y), "%Y")
                timeEnd = datetime.strptime(str(y+1), "%Y")
                query = (db.clsb_user.id == db.clsb30_gift_code_log.user_id) & \
                                (db.clsb30_gift_code_log.created_on > timeStart) & \
                                (db.clsb30_gift_code_log.created_on < timeEnd)
                all_user = len(db(query).select())
                temp.append(all_user)
                select_buy = db(query)\
                        (db.clsb_user.id == db.clsb30_product_history.user_id).select(db.clsb_user.id, distinct=True)
                temp.append(len(select_buy))
                select_transaction = db(query)\
                        (db.clsb_user.id == db.clsb_transaction.user_id).select(db.clsb_user.id, distinct=True)
                temp.append(len(select_transaction))
                data.append(temp)
                tmp_percent = dict()
                if all_user == 0:
                    tmp_percent['buy'] = "0%"
                    tmp_percent['transaction'] = "0%"
                else:
                    tmp_percent['buy'] = str(len(select_buy) * 100 / all_user) + "%"
                    tmp_percent['transaction'] = str(len(select_transaction) * 100 / all_user) + "%"
                percent.append(tmp_percent)
            elif by_month:
                for i in range(min, max+1):
                    temp = list()
                    temp.append(str(i)+"/"+str(y))
                    timeStart = datetime.strptime(str(y)+"-"+str(i), "%Y-%m")
                    timeEnd = None
                    if i == 12:
                        timeEnd = datetime.strptime(str(y+1)+"-"+str(1), "%Y-%m")
                    else:
                        timeEnd = datetime.strptime(str(y)+"-"+str(i+1), "%Y-%m")
                    query = (db.clsb_user.id == db.clsb30_gift_code_log.user_id) & \
                                (db.clsb30_gift_code_log.created_on > timeStart) & \
                                (db.clsb30_gift_code_log.created_on < timeEnd)
                    all_user = len(db(query).select())
                    temp.append(all_user)
                    select_buy = db(query)\
                            (db.clsb_user.id == db.clsb30_product_history.user_id).select(db.clsb_user.id, distinct=True)
                    temp.append(len(select_buy))
                    select_transaction = db(query)\
                            (db.clsb_user.id == db.clsb_transaction.user_id).select(db.clsb_user.id, distinct=True)
                    temp.append(len(select_transaction))
                    data.append(temp)
                    tmp_percent = dict()
                    if all_user == 0:
                        tmp_percent['buy'] = "0%"
                        tmp_percent['transaction'] = "0%"
                    else:
                        tmp_percent['buy'] = str(len(select_buy) * 100 / all_user) + "%"
                        tmp_percent['transaction'] = str(len(select_transaction) * 100 / all_user) + "%"
                    percent.append(tmp_percent)
            elif by_day:
                for i in range(min, max+1):
                    max_day = calendar.monthrange(y, i)[1]
                    if (y == maxYear) and (i == maxMonth):
                        max_day = end.day
                    day_min = 1
                    if (y == start.year) & (i == start.month):
                        day_min = start.day
                    for d in range(day_min, max_day+1):
                        temp = list()
                        temp.append(str(d)+"/"+str(i)+"/"+str(y))
                        timeStart = datetime.strptime(str(y)+"-"+str(i)+"-"+str(d), "%Y-%m-%d")
                        timeEnd = None
                        if i == 12:
                            if d == calendar.monthrange(y, i)[1]:
                                timeEnd = datetime.strptime(str(y+1)+"-"+str(1)+"-"+str(1), "%Y-%m-%d")
                            else:
                                timeEnd = datetime.strptime(str(y)+"-"+str(i)+"-"+str(d+1), "%Y-%m-%d")
                        else:
                            if d == calendar.monthrange(y, i)[1]:
                                timeEnd = datetime.strptime(str(y)+"-"+str(i+1)+"-"+str(1), "%Y-%m-%d")
                            else:
                                timeEnd = datetime.strptime(str(y)+"-"+str(i)+"-"+str(d+1), "%Y-%m-%d")
                        query = (db.clsb_user.id == db.clsb30_gift_code_log.user_id) & \
                                (db.clsb30_gift_code_log.created_on > timeStart) & \
                                (db.clsb30_gift_code_log.created_on < timeEnd)
                        all_user = len(db(query).select())
                        temp.append(all_user)
                        select_buy = db(query)\
                                (db.clsb_user.id == db.clsb30_product_history.user_id).select(db.clsb_user.id, distinct=True)
                        temp.append(len(select_buy))
                        select_transaction = db(query)\
                                (db.clsb_user.id == db.clsb_transaction.user_id).select(db.clsb_user.id, distinct=True)
                        temp.append(len(select_transaction))
                        data.append(temp)
                        tmp_percent = dict()
                        if all_user == 0:
                            tmp_percent['buy'] = "0%"
                            tmp_percent['transaction'] = "0%"
                        else:
                            tmp_percent['buy'] = str(len(select_buy) * 100 / all_user) + "%"
                            tmp_percent['transaction'] = str(len(select_transaction) * 100 / all_user) + "%"
                        percent.append(tmp_percent)
        return dict(data=data, percent=percent, start=str(start), end=str(end))
    except Exception as err:
        import sys
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))

@auth.requires_authorize()
def downloaded():
    users = db(db.auth_user.id == db.auth_membership.user_id)\
        (db.auth_group.role.like("CPAdmin"))\
        (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)
    cp_admin = None
    select = "none"
    type = 'none'
    if request.vars.select:
        select = request.vars.select
        if request.vars.select == "all":
            pass
        elif request.vars.select == "all_cp":
            cp_admin = (db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (db.clsb20_product_cp.created_by == db.auth_user.id)
        elif request.vars.select == "not_cp":
            cp_admin = ((~db.clsb_product.product_code.belongs(db(db.clsb20_product_cp)._select(db.clsb20_product_cp.product_code))) & (db.clsb_product.created_by == db.auth_user.id))
        else:
            cp_id = int(request.vars.select)
            cp_admin = ((db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (((db.auth_user.created_by == cp_id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | ((db.clsb20_product_cp.created_by == cp_id) & (db.auth_user.id == cp_id))))
    query = cp_admin

    if request.vars.type:
        type = request.vars.type
        if request.vars.type == "all":
            pass
        elif request.vars.type == 'book':
            query_type = (db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name == "Book")
            if cp_admin is not None:
                query = cp_admin & query_type
            else:
                query = query_type
        elif request.vars.type == 'app':
            query_type = (db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name == "Application")
            if cp_admin is not None:
                query = cp_admin & query_type
            else:
                query = query_type
    import calendar
    by_year = False
    by_day = False
    by_month = False
    if request.vars.getbyyear:
        if request.vars.getbyyear == "1":
            by_year = True
        elif request.vars.getbyyear == "2":
            by_month = True
        elif request.vars.getbyyear == "3":
            by_day = True
        else:
            by_month = True
    else:
        by_month = True


    start = datetime.strptime(str(datetime.now().year), "%Y")
    if by_day:
        start = datetime.strptime(str(datetime.now().month) + "-" + str(datetime.now().year), "%m-%Y")
    end = datetime.now()
    if request.vars.start:
        if by_year:
            start = datetime.strptime(request.vars.start, "%Y")
        elif by_month:
            start = datetime.strptime(request.vars.start, "%m-%Y")
        elif by_day:
            start = datetime.strptime(request.vars.start, "%d-%m-%Y")

    if request.vars.end:
        if by_year:
            end = datetime.strptime("31-12-" + str(request.vars.end), "%d-%m-%Y")
        elif by_month:
            end = datetime.strptime(request.vars.end, "%m-%Y")
            end = datetime.strptime(str(calendar.monthrange(end.year, end.month)[1]) + "-" + request.vars.end, "%d-%m-%Y")
        elif by_day:
            end = datetime.strptime(request.vars.end, "%d-%m-%Y")

    maxMonth = datetime.now().month
    maxYear = datetime.now().year

    if end.year < maxYear:
        maxYear = end.year
        maxMonth = 12
    if end.month != maxMonth:
        maxMonth = end.month

    data = list()
    list_total = list()
    totalAll = 0
    print(start)
    print(end)
    time_type = 'by_month'

    if by_year:
        time_type = 'by_year'
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        if query is not None:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY_BK"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (query)(samsung_query).select(count,
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY_BK"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (samsung_query).select(count,
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.year()))
        print(count_by_time)
        time_data = list()
        for index_time in count_by_time:
            time_data.append(str(index_time[db.clsb_download_archieve.download_time.year()]))
        for y in range(start.year, maxYear+1):
            str_time = str(y)
            temp = list()
            tempTotal = list()
            tempTotal.append(str_time)
            temp.append(str_time)
            if str_time in time_data:
                index = time_data.index(str_time)
                len_down = count_by_time[index][count]
                rows = dict()
                rows['download_time'] = str_time
                rows['downloaded'] = len_down
                rows['start'] = '01-01-' + str_time
                rows['end'] = '31-12-' + str_time
                list_total.append(rows)
                temp.append(len_down)
                totalAll += len_down
                data.append(temp)
            else:
                rows = dict()
                rows['download_time'] = str_time
                rows['downloaded'] = 0
                rows['start'] = '01-01-' + str_time
                rows['end'] = '31-12-' + str_time
                list_total.append(rows)
                temp.append(0)
                data.append(temp)
    elif by_month:
        time_type = 'by_month'
        # count = db.clsb_download_archieve.id.count()
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        if query is not None:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY_BK"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (query)(samsung_query).select(count,
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY_BK"))\
                        ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                        (samsung_query).select(count,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
        print(count_by_time)
        time_data = list()
        for index_time in count_by_time:
            time_data.append(str(index_time[db.clsb_download_archieve.download_time.month()])
                                  + "-"
                                    + str(index_time[db.clsb_download_archieve.download_time.year()]))
        for y in range(start.year, maxYear+1):
            for m in range(1,13):
                time = datetime.strptime(str(y)+"-"+str(m), "%Y-%m")
                if time <= end and time >= start:
                    str_time = str(m) + "-" + str(y)
                    temp = list()
                    tempTotal = list()
                    tempTotal.append(str_time)
                    temp.append(str_time)
                    if str_time in time_data:
                        index = time_data.index(str_time)
                        len_down = count_by_time[index][count]
                        rows = dict()
                        rows['download_time'] = str_time
                        rows['downloaded'] = len_down
                        rows['start'] = '01-' + str_time
                        rows['end'] = str(calendar.monthrange(y, m)[1]) + "-" + str_time
                        list_total.append(rows)
                        temp.append(len_down)
                        totalAll += len_down
                        data.append(temp)
                    else:
                        rows = dict()
                        rows['download_time'] = str_time
                        rows['downloaded'] = 0
                        rows['start'] = '01-' + str_time
                        rows['end'] = str(calendar.monthrange(y, m)[1]) + "-" + str_time
                        list_total.append(rows)
                        temp.append(0)
                        data.append(temp)
    elif by_day:
        time_type='by_day'
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        if query is not None:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY_BK"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (query)(samsung_query).select(count,
                                                    db.clsb_download_archieve.download_time.day(),
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.day(),
                                                            db.clsb_download_archieve.download_time.month(),
                                                            db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY_BK"))\
                        ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                        (samsung_query).select(count,
                                                db.clsb_download_archieve.download_time.day(),
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.day(),
                                                        db.clsb_download_archieve.download_time.month(),
                                                        db.clsb_download_archieve.download_time.year()))
        # print(count_by_time)
        time_data = list()
        for index_time in count_by_time:
            time_data.append(str(index_time[db.clsb_download_archieve.download_time.day()])
                                + "-" + str(index_time[db.clsb_download_archieve.download_time.month()])
                                  + "-"
                                    + str(index_time[db.clsb_download_archieve.download_time.year()]))
        for y in range(start.year, maxYear+1):
            for m in range(1,13):
                max_day = calendar.monthrange(y, m)[1]
                for d in range(1, max_day + 1):
                    time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                    if time <= end and time >= start:
                        str_time = str(d) + "-" +str(m) + "-" + str(y)
                        temp = list()
                        tempTotal = list()
                        tempTotal.append(str_time)
                        temp.append(str_time)
                        if str_time in time_data:
                            index = time_data.index(str_time)
                            len_down = count_by_time[index][count]
                            rows = dict()
                            rows['download_time'] = str_time
                            rows['downloaded'] = len_down
                            rows['start'] = str_time
                            rows['end'] = str_time
                            list_total.append(rows)
                            temp.append(len_down)
                            totalAll += len_down
                            data.append(temp)
                        else:
                            rows = dict()
                            rows['download_time'] = str_time
                            rows['downloaded'] = 0
                            rows['start'] = str_time
                            rows['end'] = str_time
                            list_total.append(rows)
                            temp.append(0)
                            data.append(temp)
    print(list_total)

    return dict(users=users, data=data, totalAll=totalAll, listDownloadTotal=list_total, time=time_type, select=select, type = type)

def downloaded_details():
    if request.args and len(request) > 4:
        time_type = request.args[0]
        time_start = request.args[1]
        time_end = request.args[2]
        select = request.args[3]
        type = request.args[4]

        users = db(db.auth_user.id == db.auth_membership.user_id)\
            (db.auth_group.role.like("CPAdmin"))\
            (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)
        cp_admin = None
        str_cp = ""
        if select != 'none':
            if select == "all":
                pass
            elif select == "all_cp":
                str_cp = ' c?a t?t c? CP'
                cp_admin = (db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (db.clsb20_product_cp.created_by == db.auth_user.id)
            elif select == "not_cp":
                str_cp = ' c?a Phòng n?i dung Version 1.0'
                cp_admin = ((~db.clsb_product.product_code.belongs(db(db.clsb20_product_cp)._select(db.clsb20_product_cp.product_code))) & (db.clsb_product.created_by == db.auth_user.id))
            else:
                str_cp = ' c?a ' + str(users['auth_user']['last_name']) + ' ' + str(users['auth_user']['first_name'])
                cp_id = int(request.vars.select)
                cp_admin = ((db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (((db.auth_user.created_by == cp_id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | ((db.clsb20_product_cp.created_by == cp_id) & (db.auth_user.id == cp_id))))
        query = cp_admin
        str_type = ''
        if type != 'none':
            if type == "all":
                pass
            elif type == 'book':
                str_type = ' Sách'
                query_type = (db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name == "Book")
                if cp_admin is not None:
                    query = cp_admin & query_type
                else:
                    query = query_type
            elif type == 'app':
                str_type = ' ?ng d?ng'
                query_type = (db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name == "Application")
                if cp_admin is not None:
                    query = cp_admin & query_type
                else:
                    query = query_type
        import calendar
        str_time = ''
        if time_type == 'by_year':
            start = datetime.strptime(time_start, '%d-%m-%Y')
            end = datetime.strptime(time_end, '%d-%m-%Y')
            str_time = 'n?m ' + str(start.year)
        elif time_type == 'by_month':
            start = datetime.strptime(time_start, '%d-%m-%Y')
            end = datetime.strptime(time_end, '%d-%m-%Y')
            str_time = 'tháng ' + str(start.month) + "/" + str(start.year)
        else:
            start = datetime.strptime(time_start + " 00:00", '%d-%m-%Y %H:%M')
            end = datetime.strptime(time_end + " 23:59", '%d-%m-%Y %H:%M')
            str_time = 'ngày ' + str(start.day) + "/" + str(start.month) + "/" + str(start.year)
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        if query is not None:
            count_by_product = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY_BK"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_product.product_category == db.clsb_category.id)\
                    (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                    (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (query)(samsung_query).select(count,
                                                   db.clsb_download_archieve.product_id,
                                                   db.clsb_product.product_code,
                                                   db.clsb_product.product_title,
                                                   db.clsb_category.category_name,
                                                   db.clsb_class.class_name,
                                                   groupby=(db.clsb_download_archieve.product_id),
                                                   orderby=count)
        else:
            count_by_product = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY_BK"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_product.product_category == db.clsb_category.id)\
                    (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                    (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (samsung_query).select(count,
                                                   db.clsb_download_archieve.product_id,
                                                   db.clsb_product.product_code,
                                                   db.clsb_product.product_title,
                                                   db.clsb_category.category_name,
                                                   db.clsb_class.class_name,
                                                   groupby=(db.clsb_download_archieve.product_id),
                                                   orderby=count)
        list_total = list()
        total = 0
        for count_product in count_by_product:
            product = dict()
            product['id'] = count_product[db.clsb_download_archieve.product_id]
            product['product_code'] = count_product[db.clsb_product.product_code]
            product['product_title'] = count_product[db.clsb_product.product_title]
            product['download_time'] = count_product[count]
            product['category'] = count_product[db.clsb_category.category_name]
            product['class'] = count_product[db.clsb_class.class_name]
            list_total.append(product)
            total += int(count_product[count])
        list_total.reverse()
        print(str_cp)
        return dict(list_total=list_total, users=users, str_time=str_time, total=total, str_cp = str_cp, str_type=str_type)
    else:
        return "Không thể thống kê vì không đủ tham số"