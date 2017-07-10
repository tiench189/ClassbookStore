# -*- coding: utf-8 -*-
""" Reports
    Theo dõi thống kê dữ liệu, doanh thu, lượt tải...
"""

__author__ = 'manhtd'
import scripts
import usercp
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import sys


@auth.requires_authorize()
def index_old():
    users = db(db.auth_user.id == db.auth_membership.user_id)\
        (db.auth_group.role.like("CPAdmin"))\
        (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)

    cp_admin = (((db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | ((~db.clsb_product.product_code.belongs(db(db.clsb20_product_cp)._select(db.clsb20_product_cp.product_code))) & (db.clsb_product.created_by == db.auth_user.id)))
    if request.vars.select:
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
            end = datetime.strptime(request.vars.end, "%Y")
        elif by_month:
            end = datetime.strptime(request.vars.end, "%m-%Y")
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
    totalAll = dict()
    totalAll['price'] = 0
    totalAll['discount'] = 0

    import calendar
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

            downloads = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.price > 0))\
                        ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                        (query).select(groupby=db.clsb_download_archieve.id)
            price = 0
            discount = 0
            for download in downloads:
                price += download['clsb_download_archieve']['price']
                tmp = download['clsb_download_archieve']['price']*usercp.get_discount_value(download['auth_user']['id'], db)/100
                discount += tmp
                totalAll['discount'] += tmp
                totalAll['price'] += download['clsb_download_archieve']['price']
            rows = dict()
            rows['download_time'] = str(y)
            rows['discount'] = str(discount)
            rows['price'] = str(price)
            list_total.append(rows)
            temp.append(price)
            data.append(temp)
        elif by_month:
            for i in range(min, max+1):
                temp = list()
                tempTotal = list()
                tempTotal.append(str(i)+"/"+str(y))
                temp.append(str(i)+"/"+str(y))
                timeStart = datetime.strptime(str(y)+"-"+str(i), "%Y-%m")
                timeEnd = None
                if i == 12:
                    timeEnd = datetime.strptime(str(y+1)+"-"+str(1), "%Y-%m")
                else:
                    timeEnd = datetime.strptime(str(y)+"-"+str(i+1), "%Y-%m")

                downloads = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.price > 0))\
                        ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                        (query).select(groupby=db.clsb_download_archieve.id)
                price = 0
                discount = 0
                for download in downloads:
                    print download['clsb_product']['product_code'] +" - "+ str(usercp.get_discount_value(download['auth_user']['id'], db))
                    price += download['clsb_download_archieve']['price']
                    tmp = download['clsb_download_archieve']['price']*usercp.get_discount_value(download['auth_user']['id'], db)/100
                    discount += tmp
                    totalAll['discount'] += tmp
                    totalAll['price'] += download['clsb_download_archieve']['price']
                rows = dict()
                rows['download_time'] = str(i)+"/"+str(y)
                rows['discount'] = str(discount)
                rows['price'] = str(price)
                list_total.append(rows)
                temp.append(price)
                data.append(temp)
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
                    downloads = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.price > 0))\
                            ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                            (query).select(groupby=db.clsb_download_archieve.id)
                    price = 0
                    discount = 0
                    for download in downloads:
                        price += download['clsb_download_archieve']['price']
                        tmp = download['clsb_download_archieve']['price']*usercp.get_discount_value(download['auth_user']['id'], db)/100
                        discount += tmp
                        totalAll['discount'] += tmp
                        totalAll['price'] += download['clsb_download_archieve']['price']
                    rows = dict()
                    rows['download_time'] = str(d)+"/"+str(i)+"/"+str(y)
                    rows['discount'] = str(discount)
                    rows['price'] = str(price)
                    list_total.append(rows)
                    temp.append(price)
                    data.append(temp)

    return dict(users=users, data=data, totalAll=totalAll, listDownloadTotal=list_total)

@auth.requires_authorize()
def index():
    users = db(db.auth_user.id == db.auth_membership.user_id)\
        (db.auth_group.role.like("CPAdmin"))\
        (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)
    cp_admin = None
    #cp_admin = (((db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | ((~db.clsb_product.product_code.belongs(db(db.clsb20_product_cp)._select(db.clsb20_product_cp.product_code))) & (db.clsb_product.created_by == db.auth_user.id)))
    if request.vars.select:
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
        by_day = True


    start = datetime.strptime(str(datetime.now().year), "%Y")
    if by_day:
        start = datetime.now() - timedelta(days=7)
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
            end = datetime.strptime(request.vars.end, "%Y")
        elif by_month:
            end = datetime.strptime(request.vars.end, "%m-%Y")
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
    totalAll = dict()
    totalAll['price'] = 0
    totalAll['discount'] = 0
    list_id = list()
    print(query)
    if query is not None:
        products_list = db((db.clsb_download_archieve.price > 0) & (db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                                   & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                                ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                                (query).select(db.clsb_download_archieve.id, distinct=True)
    else:
        products_list = db((db.clsb_download_archieve.price > 0) & (db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                                   & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            .select(db.clsb_download_archieve.id, distinct=True)
    print(products_list)
    import calendar
    sum = "SUM(clsb_download_archieve.price)"
    sum_discount = "SUM(clsb_download_archieve.pay_provider)"
    sum_cp = "SUM(clsb_download_archieve.pay_cp)"
    if by_year:
        for pd in products_list:
            list_id.append(pd[db.clsb_download_archieve.id])
        count_by_time = db(db.clsb_download_archieve.id.belongs(list_id)).select(sum, sum_discount, sum_cp,
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.year()))
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
                sum_price = count_by_time[index][sum]
                discount = count_by_time[index][sum_discount]
                rows = dict()
                rows['download_time'] = str_time
                rows['discount'] = discount
                price_cp = count_by_time[index][sum_cp]
                rows['cp'] = price_cp
                rows['price'] = sum_price
                rows['start'] = '01-01-' + str_time
                rows['end'] = '31-12-' + str_time
                list_total.append(rows)
                temp.append(sum_price)
                totalAll['discount'] += discount
                totalAll['price'] += sum_price
                data.append(temp)
            else:
                rows = dict()
                rows['download_time'] = str_time
                rows['discount'] = 0
                rows['cp'] = 0
                rows['price'] = 0
                rows['start'] = '01-01-' + str_time
                rows['end'] = '31-12-' + str_time
                list_total.append(rows)
                temp.append(0)
                data.append(temp)
    elif by_month:
        for pd in products_list:
            list_id.append(pd[db.clsb_download_archieve.id])
        count_by_time = db(db.clsb_download_archieve.id.belongs(list_id)).select(sum, sum_discount, sum_cp,
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.month(),
                                                            db.clsb_download_archieve.download_time.year()))
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
                        sum_price = count_by_time[index][sum]
                        discount = count_by_time[index][sum_discount]
                        rows = dict()
                        rows['download_time'] = str_time
                        rows['discount'] = discount
                        price_cp = count_by_time[index][sum_cp]
                        rows['cp'] = price_cp
                        rows['price'] = sum_price
                        rows['start'] = '01-' + str_time
                        rows['end'] = str_time
                        list_total.append(rows)
                        temp.append(sum_price)
                        totalAll['discount'] += discount
                        totalAll['price'] += sum_price
                        data.append(temp)
                    else:
                        rows = dict()
                        rows['download_time'] = str_time
                        rows['discount'] = 0
                        rows['cp'] = 0
                        rows['price'] = 0
                        rows['start'] = str_time
                        rows['end'] = str_time
                        list_total.append(rows)
                        temp.append(0)
                        data.append(temp)
    elif by_day:
        for pd in products_list:
            list_id.append(pd[db.clsb_download_archieve.id])
        count_by_time = db(db.clsb_download_archieve.id.belongs(list_id)).select(sum, sum_discount, sum_cp,
                                                                                 db.clsb_download_archieve.download_time.day(),
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.day(),
                                                            db.clsb_download_archieve.download_time.month(),
                                                            db.clsb_download_archieve.download_time.year()))
        time_data = list()
        for index_time in count_by_time:
            time_data.append(str(index_time[db.clsb_download_archieve.download_time.day()])
                                    + "-" + str(index_time[db.clsb_download_archieve.download_time.month()])
                                      + "-"
                                        + str(index_time[db.clsb_download_archieve.download_time.year()]))
        for y in range(start.year, maxYear+1):
            for m in range(1, 13):
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
                            sum_price = int(count_by_time[index][sum])
                            discount = int(count_by_time[index][sum_discount])
                            rows = dict()
                            rows['download_time'] = str_time
                            rows['discount'] = discount
                            price_cp = count_by_time[index][sum_cp]
                            rows['cp'] = price_cp
                            rows['price'] = sum_price
                            rows['start'] = str_time
                            rows['end'] = str_time
                            list_total.append(rows)
                            temp.append(sum_price)
                            totalAll['discount'] += discount
                            totalAll['price'] += sum_price
                            data.append(temp)
                        else:
                            rows = dict()
                            rows['download_time'] = str_time
                            rows['discount'] = 0
                            rows['cp'] = 0
                            rows['price'] = 0
                            rows['start'] = str_time
                            rows['end'] = str_time
                            list_total.append(rows)
                            temp.append(0)
                            data.append(temp)
    return dict(users=users, data=data, totalAll=totalAll, listDownloadTotal=list_total)


@auth.requires_login()
def get_payment_cp_admin(cp_admin_id):
    query = db(db.clsb_download_archieve)\
        ((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.status.like('Completed')))\
        (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
        (((db.auth_user.created_by == cp_admin_id) & (db.clsb20_product_cp.created_by == cp_admin_id)) | (db.clsb20_product_cp.created_by == cp_admin_id))\

    total_payment = 0
    downloads = query.select(groupby=db.clsb_download_archieve.id)
    for download in downloads:
        total_payment += download['clsb_download_archieve']['price']
    return total_payment


@auth.requires_authorize()
def report_mail_type():
    form = SQLFORM.smartgrid(db.clsb20_user_report_type)
    return dict(form=form)


@auth.requires_authorize()
def report_mail_list():
    form = SQLFORM.smartgrid(db.clsb20_user_report_list)
    return dict(form=form)


# @auth.requires_authorize()
def downloaded_old():
    users = db(db.auth_user.id == db.auth_membership.user_id)\
        (db.auth_group.role.like("CPAdmin"))\
        (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)

    cp_admin = (((db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | ((~db.clsb_product.product_code.belongs(db(db.clsb20_product_cp)._select(db.clsb20_product_cp.product_code))) & (db.clsb_product.created_by == db.auth_user.id)))
    if request.vars.select:
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
            end = datetime.strptime(request.vars.end, "%Y")
        elif by_month:
            end = datetime.strptime(request.vars.end, "%m-%Y")
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

    import calendar
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

            downloads = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.status.like('Completed')))\
                        ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                        (query).select(groupby=db.clsb_download_archieve.id)
            rows = dict()
            rows['download_time'] = str(y)
            rows['downloaded'] = str(len(downloads))
            list_total.append(rows)
            temp.append(len(downloads))
            totalAll += len(downloads)
            data.append(temp)
        elif by_month:
            for i in range(min, max+1):
                temp = list()
                tempTotal = list()
                tempTotal.append(str(i)+"/"+str(y))
                temp.append(str(i)+"/"+str(y))
                timeStart = datetime.strptime(str(y)+"-"+str(i), "%Y-%m")
                timeEnd = None
                if i == 12:
                    timeEnd = datetime.strptime(str(y+1)+"-"+str(1), "%Y-%m")
                else:
                    timeEnd = datetime.strptime(str(y)+"-"+str(i+1), "%Y-%m")

                downloads = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.status.like('Completed')))\
                        ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                        (query).select(groupby=db.clsb_download_archieve.id)
                rows = dict()
                rows['download_time'] = str(i)+"/"+str(y)
                rows['downloaded'] = str(len(downloads))
                list_total.append(rows)
                temp.append(len(downloads))
                totalAll += len(downloads)
                data.append(temp)
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
                    downloads = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.status.like('Completed')))\
                            ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                            (query).select(groupby=db.clsb_download_archieve.id)
                    rows = dict()
                    rows['download_time'] = str(d)+"/"+str(i)+"/"+str(y)
                    rows['downloaded'] = str(len(downloads))
                    list_total.append(rows)
                    temp.append(len(downloads))
                    totalAll += len(downloads)
                    data.append(temp)

    return dict(users=users, data=data, totalAll=totalAll, listDownloadTotal=list_total)

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
    filter_type = ["Book", "Application"]
    query_type = (db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name.belongs(filter_type))
    if cp_admin is not None:
        query = cp_admin & query_type
    else:
        query = query_type
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
        by_day = True


    start = datetime.strptime(str(datetime.now().year), "%Y")
    if by_day:
        start = datetime.now() - timedelta(days=7)
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
            end = datetime.strptime(request.vars.end, "%m-%Y") + relativedelta(months=1)
            #end = datetime.strptime(str(calendar.monthrange(end.year, end.month)[1]) + "-" + request.vars.end, "%d-%m-%Y")
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
    #print(start)
    #print(end)
    time_type = 'by_month'
    print("All: " + str(query))
    if by_year:
        time_type = 'by_year'
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        if query is not None:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (query).select(count,
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            .select(count,
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
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_product.product_category == db.clsb_category.id)\
                            (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                            (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (query).select(count,
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY"))\
                        ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                        .select(count,
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
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_product.product_category == db.clsb_category.id)\
                            (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                            (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (query).select(count,
                                                    db.clsb_download_archieve.download_time.day(),
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.day(),
                                                            db.clsb_download_archieve.download_time.month(),
                                                            db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY"))\
                        ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                        .select(count,
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
    #print(list_total)

    return dict(users=users, data=data, totalAll=totalAll, listDownloadTotal=list_total, time=time_type, select=select, type = type)
# @auth.requires_authorize()
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
                str_cp = ' của tất cả CP'
                cp_admin = (db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (db.clsb20_product_cp.created_by == db.auth_user.id)
            elif select == "not_cp":
                str_cp = ' của Phòng nội dung Version 1.0'
                cp_admin = ((~db.clsb_product.product_code.belongs(db(db.clsb20_product_cp)._select(db.clsb20_product_cp.product_code))) & (db.clsb_product.created_by == db.auth_user.id))
            else:
                # str_cp = ' của ' + str(users['auth_user']['last_name']) + ' ' + str(users['auth_user']['first_name'])
                cp_id = int(select)
                cp_admin = ((db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (((db.auth_user.created_by == cp_id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | ((db.clsb20_product_cp.created_by == cp_id) & (db.auth_user.id == cp_id))))
        query = cp_admin
        str_type = ''
        filter_type = ["Book", "Application"]
        query_type = (db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name.belongs(filter_type))
        if cp_admin is not None:
            query = cp_admin & query_type
        else:
            query = query_type
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
                str_type = ' Ứng dụng'
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
            str_time = 'năm ' + str(start.year)
        elif time_type == 'by_month':
            start = datetime.strptime(time_start + " 00:00", '%d-%m-%Y %H:%M')
            end = datetime.strptime(time_end + " 00:00", '%d-%m-%Y %H:%M') + timedelta(days=1)
            str_time = 'tháng ' + str(start.month) + "/" + str(start.year)
        else:
            start = datetime.strptime(time_start + " 00:00", '%d-%m-%Y %H:%M')
            end = datetime.strptime(time_end + " 00:00", '%d-%m-%Y %H:%M') + timedelta(days=1)
            str_time = 'ngày ' + str(start.day) + "/" + str(start.month) + "/" + str(start.year)
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        print("detail" + str(query))
        if query is not None:
            count_by_product = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_product.product_category == db.clsb_category.id)\
                    (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                    (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (query).select(count,
                                                   db.clsb_download_archieve.product_id,
                                                   db.clsb_product.product_code,
                                                   db.clsb_product.product_title,
                                                   db.clsb_category.category_name,
                                                   db.clsb_class.class_name,
                                                   groupby=(db.clsb_download_archieve.product_id),
                                                   orderby=count)
        else:
            count_by_product = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0) & (db.clsb_download_archieve.purchase_type != "WEB_PAY"))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_product.product_category == db.clsb_category.id)\
                    (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                    (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            .select(count,
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

# remove test user
@auth.requires_authorize()
def remove_test_user():
    try:
        key = request.args[0]
        db(db.clsb_user.username.like('%' + key + '%')).update(test_user=1)
        return dict(result='SUCCESS')
    except Exception as err:
        return dict(error=str(err))

@auth.requires_authorize()
def samsung_gift_code():
    if "start" in request.vars:
        start1 = request.vars.start
        time_start = datetime.strptime(start1 + " 00:00:00", "%Y-%m-%d  %H:%M:%S")
    else:
        time_start = str(datetime.now().strftime("%Y-%m-%d")) + " 00:00:00"
        time_start = datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")

    if "end" in request.vars:
        end1 = request.vars.end
        time_end = datetime.strptime(end1 + " 23:59:59", "%Y-%m-%d  %H:%M:%S")
    else:
        time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        time_end = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S")
    print(time_start)
    print(time_end)
    query = (db.clsb_user.id == db.clsb30_gift_code_log.user_id) & \
            (db.clsb30_gift_code_log.created_on > time_start) & \
            (db.clsb30_gift_code_log.created_on < time_end)
    print(query)
    return dict(start=time_start.strftime("%Y-%m-%d"),
                end=time_end.strftime("%Y-%m-%d"),
                grid=SQLFORM.grid(query, fields=(db.clsb_user.username,
                                                db.clsb30_gift_code_log.gift_code,
                                                db.clsb30_gift_code_log.created_on),
                                    deletable=False,
                                    editable=False,
                                    details=True,
                                    selectable=None,
                                    create=False))
@auth.requires_authorize()
def account_gift_code():
    try:
        if "start" in request.vars:
            start1 = request.vars.start
            time_start = datetime.strptime(start1 + " 00:00:00", "%Y-%m-%d  %H:%M:%S")
        else:
            time_start = "2015-03-03 00:00:00"
            time_start = datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")

        if "end" in request.vars:
            end1 = request.vars.end
            time_end = datetime.strptime(end1 + " 23:59:59", "%Y-%m-%d  %H:%M:%S")
        else:
            time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_end = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S")

        query = (db.clsb_user.id == db.clsb30_gift_code_log.user_id) & \
                (db.clsb30_gift_code_log.created_on > time_start) & \
                (db.clsb30_gift_code_log.created_on < time_end) & \
                (db.clsb_user.phoneNumber != '0987654321') & \
                (db.clsb_user.phoneNumber != '')
        users = db(query).select()
        list_user = list()
        for user in users:
            temp = dict()
            temp['user_id'] = user[db.clsb_user.id]
            temp['email'] = user[db.clsb_user.username]
            temp['first_name'] = user[db.clsb_user.firstName]
            temp['last_name'] = user[db.clsb_user.lastName]
            temp['phone'] = user[db.clsb_user.phoneNumber]
            temp['created_on'] = str(user[db.clsb30_gift_code_log.created_on])
            list_user.append(temp)
        return dict(users=list_user)
    except Exception as err:
        import sys
        return dict(error=err.message + " on line: "+ str(sys.exc_traceback.tb_lineno))

def samsung_count_download():
    try:
        fh = open("/var/log/apache2/access.log", "r")
        mdata = fh.readlines()
        return dict(read=mdata)
    except Exception as err:
        import sys
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))

def trend_gift_code():
    try:
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
                end = datetime.strptime(request.vars.end, "%Y")
            elif by_month:
                end = datetime.strptime(request.vars.end, "%m-%Y")
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
        if by_year:
            time_type = 'by_year'
            count = "COUNT(DISTINCT clsb30_gift_code_log.id)"
            count_by_time = db(db.clsb30_gift_code_log.created_on > start)\
                    (db.clsb30_gift_code_log.created_on <= end).select(count,
                                                   db.clsb30_gift_code_log.created_on.year(),
                                                   groupby=(db.clsb30_gift_code_log.created_on.year()))
            time_data = list()
            for index_time in count_by_time:
                time_data.append(str(index_time[db.clsb30_gift_code_log.created_on.year()]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                tempTotal = list()
                tempTotal.append(str_time)
                temp.append(str_time)
                if str_time in time_data:
                    index = time_data.index(str_time)
                    len_gift = count_by_time[index][count]
                    rows = dict()
                    rows['time'] = str_time
                    rows['count'] = len_gift
                    list_total.append(rows)
                    temp.append(len_gift)
                    totalAll += len_gift
                    data.append(temp)
                else:
                    rows = dict()
                    rows['time'] = str_time
                    rows['count'] = 0
                    list_total.append(rows)
                    temp.append(0)
                    data.append(temp)
        if by_month:
            time_type = 'by_month'
            count = "COUNT(DISTINCT clsb30_gift_code_log.id)"
            count_by_time = db(db.clsb30_gift_code_log.created_on > start)\
                    (db.clsb30_gift_code_log.created_on <= end).select(count,
                                                   db.clsb30_gift_code_log.created_on.month(),
                                                   db.clsb30_gift_code_log.created_on.year(),
                                                   groupby=(db.clsb30_gift_code_log.created_on.month(),
                                                            db.clsb30_gift_code_log.created_on.year()))
            time_data = list()
            for index_time in count_by_time:
                time_data.append(str(index_time[db.clsb30_gift_code_log.created_on.month()])
                                      + "-"
                                        + str(index_time[db.clsb30_gift_code_log.created_on.year()]))
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
                            len_gift = count_by_time[index][count]
                            rows = dict()
                            rows['time'] = str_time
                            rows['count'] = len_gift
                            list_total.append(rows)
                            temp.append(len_gift)
                            totalAll += len_gift
                            data.append(temp)
                        else:
                            rows = dict()
                            rows['time'] = str_time
                            rows['count'] = 0
                            list_total.append(rows)
                            temp.append(0)
                            data.append(temp)
        if by_day:
            time_type = 'by_month'
            count = "COUNT(DISTINCT clsb30_gift_code_log.id)"
            count_by_time = db(db.clsb30_gift_code_log.created_on > start)\
                    (db.clsb30_gift_code_log.created_on <= end).select(count,
                                                    db.clsb30_gift_code_log.created_on.day(),
                                                    db.clsb30_gift_code_log.created_on.month(),
                                                    db.clsb30_gift_code_log.created_on.year(),
                                                    groupby=(db.clsb30_gift_code_log.created_on.day(),
                                                            db.clsb30_gift_code_log.created_on.month(),
                                                            db.clsb30_gift_code_log.created_on.year()))
            time_data = list()
            for index_time in count_by_time:
                time_data.append(str(index_time[db.clsb30_gift_code_log.created_on.day()])
                                    + "-" + str(index_time[db.clsb30_gift_code_log.created_on.month()])
                                      + "-"
                                        + str(index_time[db.clsb30_gift_code_log.created_on.year()]))
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
                                len_gift = count_by_time[index][count]
                                rows = dict()
                                rows['time'] = str_time
                                rows['count'] = len_gift
                                list_total.append(rows)
                                temp.append(len_gift)
                                totalAll += len_gift
                                data.append(temp)
                            else:
                                rows = dict()
                                rows['time'] = str_time
                                rows['count'] = 0
                                list_total.append(rows)
                                temp.append(0)
                                data.append(temp)
        return dict(data=data, totalAll=totalAll, listTotal=list_total, time=time_type)
    except Exception as err:
        import sys
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))

#@auth.requires_authorize()
def nganluong_old():
    try:
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
                end = datetime.strptime(request.vars.end, "%Y")
            elif by_month:
                end = datetime.strptime(request.vars.end, "%m-%Y")
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
        total_face = 0
        total_real = 0
        if by_year:
            time_type = 'by_year'
            sum_face = "SUM(clsb_transaction.face_value)"
            sum_real = "SUM(clsb_transaction.real_value)"
            sum_by_time = db(db.clsb_transaction.created_on > start)\
                    (db.clsb_transaction.created_on <= end)\
                    (db.clsb_transaction.status == "COMPLETE").select(sum_face, sum_real,
                                                   db.clsb_transaction.created_on.year(),
                                                   groupby=(db.clsb_transaction.created_on.year()))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb_transaction.created_on.year()]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                tempTotal = list()
                tempTotal.append(str_time)
                temp.append(str_time)
                if str_time in time_data:
                    index = time_data.index(str_time)
                    face = sum_by_time[index][sum_face]
                    real = sum_by_time[index][sum_real]
                    rows = dict()
                    rows['time'] = str_time
                    rows['face'] = face
                    rows['real'] = real
                    list_total.append(rows)
                    temp.append(real)
                    total_face += face
                    total_real += real
                    data.append(temp)
                else:
                    rows = dict()
                    rows['face'] = 0
                    rows['real'] = 0
                    list_total.append(rows)
                    temp.append(0)
                    data.append(temp)
        if by_month:
            time_type = 'by_month'
            sum_face = "SUM(clsb_transaction.face_value)"
            sum_real = "SUM(clsb_transaction.real_value)"
            sum_by_time = db(db.clsb_transaction.created_on > start)\
                    (db.clsb_transaction.created_on <= end)\
                    (db.clsb_transaction.status == "COMPLETE").select(sum_face, sum_real,
                                                   db.clsb_transaction.created_on.month(),
                                                   db.clsb_transaction.created_on.year(),
                                                   groupby=(db.clsb_transaction.created_on.month(),
                                                            db.clsb_transaction.created_on.year()))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb_transaction.created_on.month()])
                                      + "-"
                                        + str(index_time[db.clsb_transaction.created_on.year()]))
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
                            print("index: " + str(index))
                            face = sum_by_time[index][sum_face]
                            real = sum_by_time[index][sum_real]
                            rows = dict()
                            rows['time'] = str_time
                            rows['face'] = face
                            rows['real'] = real
                            list_total.append(rows)
                            temp.append(real)
                            total_face += face
                            total_real += real
                            data.append(temp)
                        else:
                            rows = dict()
                            rows['time'] = str_time
                            rows['face'] = 0
                            rows['real'] = 0
                            list_total.append(rows)
                            temp.append(0)
                            data.append(temp)
        if by_day:
            time_type = 'by_month'
            sum_face = "SUM(clsb_transaction.face_value)"
            sum_real = "SUM(clsb_transaction.real_value)"
            sum_by_time = db(db.clsb_transaction.created_on > start)\
                    (db.clsb_transaction.created_on <= end)\
                    (db.clsb_transaction.status == "COMPLETE").select(sum_face, sum_real,
                                                    db.clsb_transaction.created_on.day(),
                                                    db.clsb_transaction.created_on.month(),
                                                    db.clsb_transaction.created_on.year(),
                                                    groupby=(db.clsb_transaction.created_on.day(),
                                                            db.clsb_transaction.created_on.month(),
                                                            db.clsb_transaction.created_on.year()))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb_transaction.created_on.day()])
                                    + "-" + str(index_time[db.clsb_transaction.created_on.month()])
                                      + "-"
                                        + str(index_time[db.clsb_transaction.created_on.year()]))
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
                                face = sum_by_time[index][sum_face]
                                real = sum_by_time[index][sum_real]
                                rows = dict()
                                rows['time'] = str_time
                                rows['face'] = face
                                rows['real'] = real
                                list_total.append(rows)
                                temp.append(real)
                                total_face += face
                                total_real += real
                                data.append(temp)
                            else:
                                rows = dict()
                                rows['time'] = str_time
                                rows['face'] = 0
                                rows['real'] = 0
                                list_total.append(rows)
                                temp.append(0)
                                data.append(temp)
        print(list_total)
        return dict(data=data, total_face=total_face, total_real=total_real, listTotal=list_total, time=time_type)
    except Exception as err:
        import sys
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))

@auth.requires_authorize()
def nganluong():
    try:
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
                end = datetime.strptime(request.vars.end, "%Y")
            elif by_month:
                end = datetime.strptime(request.vars.end, "%m-%Y")
            elif by_day:
                end = datetime.strptime(request.vars.end, "%d-%m-%Y")

        maxMonth = datetime.now().month
        maxYear = datetime.now().year

        if end.year < maxYear:
            maxYear = end.year
            maxMonth = 12
        if end.month != maxMonth:
            maxMonth = end.month
        list_type = ["VIETTEL", "VMS", "VNP", "NL", "VISA", "ATM_ONLINE"]
        total_type = dict()
        for type in list_type:
            total_type[type + "face"] = 0
            total_type[type + "real"] = 0
        data = list()
        list_total = list()
        total_face = 0
        total_real = 0
        if by_year:
            time_type = 'by_year'
            sum_face = "SUM(clsb_transaction.face_value)"
            sum_real = "SUM(clsb_transaction.real_value)"
            sum_by_time = db(db.clsb_transaction.created_on > start)\
                    (db.clsb_transaction.created_on <= end)\
                    (db.clsb_transaction.status == "COMPLETE").select(sum_face, sum_real,
                                                   db.clsb_transaction.created_on.year(),
                                                   db.clsb_transaction.payment_type,
                                                   groupby=(db.clsb_transaction.created_on.year(),
                                                   db.clsb_transaction.payment_type))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb_transaction.created_on.year()]) + "-" +
                                        str(index_time[db.clsb_transaction.payment_type]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp_face = 0
                temp_real = 0
                temp = list()
                tempTotal = list()
                tempTotal.append(str_time)
                temp.append(str_time)
                rows = dict()
                rows['time'] = str_time
                for type in list_type:
                    time_type = str_time + "-" + type
                    if time_type in time_data:
                        index = time_data.index(time_type)
                        face = sum_by_time[index][sum_face]
                        real = sum_by_time[index][sum_real]
                        temp_face += face
                        temp_real += real
                        total_face += face
                        total_real += real
                        rows[type + "real"] = real
                        rows[type + "face"] = face
                        total_type[type + "real"] = total_type[type + "real"] + real
                        total_type[type + "face"] = total_type[type + "face"] + face
                    else:
                        rows[type + "real"] = 0
                        rows[type + "face"] = 0
                rows['face'] = temp_face
                rows['real'] = temp_real
                list_total.append(rows)
                temp.append(temp_real)
                data.append(temp)
        if by_month:
            time_type = 'by_month'
            sum_face = "SUM(clsb_transaction.face_value)"
            sum_real = "SUM(clsb_transaction.real_value)"
            sum_by_time = db(db.clsb_transaction.created_on > start)\
                    (db.clsb_transaction.created_on <= end)\
                    (db.clsb_transaction.status == "COMPLETE").select(sum_face, sum_real,
                                                   db.clsb_transaction.created_on.month(),
                                                   db.clsb_transaction.created_on.year(),
                                                   db.clsb_transaction.payment_type,
                                                   groupby=(db.clsb_transaction.created_on.month(),
                                                            db.clsb_transaction.created_on.year(),
                                                            db.clsb_transaction.payment_type))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb_transaction.created_on.month()])
                                      + "-"
                                        + str(index_time[db.clsb_transaction.created_on.year()]) + "-" +
                                        str(index_time[db.clsb_transaction.payment_type]))
            #print(time_data)
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    time = datetime.strptime(str(y)+"-"+str(m), "%Y-%m")
                    if time <= end and time >= start:
                        str_time = str(m) + "-" + str(y)
                        temp_face = 0
                        temp_real = 0
                        temp = list()
                        tempTotal = list()
                        tempTotal.append(str_time)
                        temp.append(str_time)
                        rows = dict()
                        rows['time'] = str_time
                        #print(list_type)
                        for type in list_type:
                            time_type = str_time + "-" + type
                            if time_type in time_data:
                                index = time_data.index(time_type)
                                face = sum_by_time[index][sum_face]
                                real = sum_by_time[index][sum_real]
                                temp_face += face
                                temp_real += real
                                total_face += face
                                total_real += real
                                rows[type + "real"] = real
                                rows[type + "face"] = face
                                total_type[type + "real"] = total_type[type + "real"] + real
                                total_type[type + "face"] = total_type[type + "face"] + face
                            else:
                                rows[type + "real"] = 0
                                rows[type + "face"] = 0
                        rows['face'] = temp_face
                        rows['real'] = temp_real
                        list_total.append(rows)
                        temp.append(temp_real)
                        data.append(temp)
        if by_day:
            time_type = 'by_month'
            sum_face = "SUM(clsb_transaction.face_value)"
            sum_real = "SUM(clsb_transaction.real_value)"
            sum_by_time = db(db.clsb_transaction.created_on > start)\
                    (db.clsb_transaction.created_on <= end)\
                    (db.clsb_transaction.status == "COMPLETE").select(sum_face, sum_real,
                                                    db.clsb_transaction.created_on.day(),
                                                    db.clsb_transaction.created_on.month(),
                                                    db.clsb_transaction.created_on.year(),
                                                    db.clsb_transaction.payment_type,
                                                    groupby=(db.clsb_transaction.created_on.day(),
                                                            db.clsb_transaction.created_on.month(),
                                                            db.clsb_transaction.created_on.year(),
                                                    db.clsb_transaction.payment_type))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb_transaction.created_on.day()])
                                    + "-" + str(index_time[db.clsb_transaction.created_on.month()])
                                      + "-"
                                        + str(index_time[db.clsb_transaction.created_on.year()])+ "-" +
                                        str(index_time[db.clsb_transaction.payment_type]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    max_day = calendar.monthrange(y, m)[1]
                    for d in range(1, max_day + 1):
                        time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                        if time <= end and time >= start:
                            str_time = str(d) + "-" +str(m) + "-" + str(y)
                            temp_face = 0
                            temp_real = 0
                            temp = list()
                            tempTotal = list()
                            tempTotal.append(str_time)
                            temp.append(str_time)
                            rows = dict()
                            rows['time'] = str_time
                            #print(list_type)
                            for type in list_type:
                                time_type = str_time + "-" + type
                                if time_type in time_data:
                                    index = time_data.index(time_type)
                                    face = sum_by_time[index][sum_face]
                                    real = sum_by_time[index][sum_real]
                                    temp_face += face
                                    temp_real += real
                                    total_face += face
                                    total_real += real
                                    rows[type + "real"] = real
                                    rows[type + "face"] = face
                                    total_type[type + "real"] = total_type[type + "real"] + real
                                    total_type[type + "face"] = total_type[type + "face"] + face
                                else:
                                    rows[type + "real"] = 0
                                    rows[type + "face"] = 0
                            rows['face'] = temp_face
                            rows['real'] = temp_real
                            list_total.append(rows)
                            temp.append(temp_real)
                            data.append(temp)
        print(total_type)
        return dict(data=data, total_face=total_face, total_real=total_real, listTotal=list_total,
                    time=time_type, total_type=total_type, list_type=list_type)
    except Exception as err:
        import sys
        print(err.message + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))

def report_custom_download():
    try:
        list_product = list()
        limit = 1
        if request.vars and "limit" in request.vars:
            limit = int(request.vars.limit)
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        count_by_product =  db(db.clsb_download_archieve.product_id == db.clsb_product.id)\
                (db.clsb_download_archieve.user_id == db.clsb_user.id)\
                (db.clsb_download_archieve.status.like('Completed'))\
                (db.clsb_user.test_user == 0)\
                (db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_download_archieve.price > 0)\
                (db.clsb_category.category_type == 1)\
                (~db.clsb_category.category_code.like('%SGK%'))\
                (~db.clsb_category.category_code.like('%SGV%'))\
                (~db.clsb_category.category_code.like('%TTDT%')).select(count,
                                                                              db.clsb_product.id,
                                                                              db.clsb_product.product_code,
                                                                              db.clsb_product.product_title,
                                                                              groupby=db.clsb_download_archieve.product_id)
        for product in count_by_product:
            if int(product[count]) >= limit:
                temp = dict()
                temp['id'] = product[db.clsb_product.id]
                temp['product_code'] = product[db.clsb_product.product_code]
                temp['count'] = product[count]
                temp['product_title'] = product[db.clsb_product.product_title]
                list_product.append(temp)
        return dict(products=list_product)
    except Exception as err:
        import sys
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))

@auth.requires_authorize()
def count_user_paid():
    try:
        if "start" in request.vars:
            start1 = request.vars.start
            time_start = datetime.strptime(start1 + " 00:00:00", "%Y-%m-%d  %H:%M:%S")
        else:
            time_start = str((datetime.now() - relativedelta(months=1)).strftime("%Y-%m-%d")) + " 00:00:00"
            time_start = datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S")

        if "end" in request.vars:
            end1 = request.vars.end
            time_end = datetime.strptime(end1 + " 23:59:59", "%Y-%m-%d  %H:%M:%S")
        else:
            time_end = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            time_end = datetime.strptime(time_end, "%Y-%m-%d %H:%M:%S")
        print(str(time_start) + " / " + str(time_end))
        count = "COUNT(DISTINCT clsb_download_archieve.user_id)"
        data = db(db.clsb_download_archieve.price > 0)\
                (db.clsb_download_archieve.download_time >= time_start)\
                (db.clsb_download_archieve.download_time <= time_end).select(count)
        print(data.first()[count])
        return dict(count=data.first()[count], start=time_start,
                 end=time_end)
    except Exception as err:
        import sys
        print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


@auth.requires_authorize()
def paid():
    users = db(db.auth_user.id == db.auth_membership.user_id)\
        (db.auth_group.role.like("CPAdmin"))\
        (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)
    cate_parent_id = db(db.clsb_category.id > 0).select(db.clsb_category.category_parent, distinct=True)
    list_parent = list()
    for parent in cate_parent_id:
        list_parent.append(parent[db.clsb_category.category_parent])
    category_list = db(db.clsb_category.id.belongs(list_parent)).select()
    category = list()
    for cate in category_list:
        temp = dict()
        temp['id'] = cate['id']
        temp['category_name'] = cate['category_name']
        category.append(temp)
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
    filter_type = ["Book", "Application"]
    query_type = (db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name.belongs(filter_type))
    if cp_admin is not None:
        query = cp_admin & query_type
    else:
        query = query_type
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
    choose_cate = "all"
    if request.vars.category:
        choose_cate = request.vars.category
        if choose_cate == "all":
            pass
        else:
            query_cate = (db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_parent==choose_cate)
            if query is not None:

                query = query & query_cate
            else:
                query = query_cate
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
        by_day = True


    start = datetime.strptime(str(datetime.now().year), "%Y")
    if by_day:
        start = datetime.now() - timedelta(days=7)
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
            end = datetime.strptime(request.vars.end, "%m-%Y") + relativedelta(months=1)
            #end = datetime.strptime(str(calendar.monthrange(end.year, end.month)[1]) + "-" + request.vars.end, "%d-%m-%Y")
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
    #print(start)
    #print(end)
    time_type = 'by_month'
    print("All: " + str(query))
    if by_year:
        time_type = 'by_year'
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        if query is not None:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_download_archieve.price > 0)\
                            (query).select(count,
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_download_archieve.price > 0).select(count,
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
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_download_archieve.price > 0)\
                            (query).select(count,
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                        ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                        (db.clsb_download_archieve.price > 0).select(count,
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
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_download_archieve.price > 0)\
                            (db.clsb_product.product_category == db.clsb_category.id)\
                            (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                            (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (query).select(count,
                                                    db.clsb_download_archieve.download_time.day(),
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.day(),
                                                            db.clsb_download_archieve.download_time.month(),
                                                            db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                        ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                        (db.clsb_download_archieve.price > 0).select(count,
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
    return dict(users=users, data=data, totalAll=totalAll, listDownloadTotal=list_total, time=time_type, select=select, type = type, category=category, choose_cate=choose_cate)

def paid_details():
    if request.args and len(request) > 4:
        time_type = request.args[0]
        time_start = request.args[1]
        time_end = request.args[2]
        select = request.args[3]
        type = request.args[4]
        choose_cate = request.args[5]

        users = db(db.auth_user.id == db.auth_membership.user_id)\
            (db.auth_group.role.like("CPAdmin"))\
            (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)
        cp_admin = None
        str_cp = ""
        if select != 'none':
            if select == "all":
                pass
            elif select == "all_cp":
                str_cp = ' của tất cả CP'
                cp_admin = (db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (db.clsb20_product_cp.created_by == db.auth_user.id)
            elif select == "not_cp":
                str_cp = ' của Phòng nội dung Version 1.0'
                cp_admin = ((~db.clsb_product.product_code.belongs(db(db.clsb20_product_cp)._select(db.clsb20_product_cp.product_code))) & (db.clsb_product.created_by == db.auth_user.id))
            else:
                str_cp = ''
                cp_id = int(select)
                cp_admin = ((db.clsb_product.product_code == db.clsb20_product_cp.product_code) & (((db.auth_user.created_by == cp_id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | ((db.clsb20_product_cp.created_by == cp_id) & (db.auth_user.id == cp_id))))
        query = cp_admin
        str_type = ''
        filter_type = ["Book", "Application"]
        query_type = (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name.belongs(filter_type))
        if cp_admin is not None:
            query = cp_admin & query_type
        else:
            query = query_type
        if type != 'none':
            if type == "all":
                pass
            elif type == 'book':
                str_type = ' Sách'
                query_type = (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name == "Book")
                if cp_admin is not None:
                    query = cp_admin & query_type
                else:
                    query = query_type
            elif type == 'app':
                str_type = ' Ứng dụng'
                query_type = (db.clsb_category.category_type == db.clsb_product_type.id) & (db.clsb_product_type.type_name == "Application")
                if cp_admin is not None:
                    query = cp_admin & query_type
                else:
                    query = query_type
        if choose_cate == "all":
            pass
        else:
            query_cate = (db.clsb_category.category_parent == choose_cate)
            if query is not None:
                query = query & query_cate
            else:
                query = query_cate
        import calendar
        str_time = ''
        if time_type == 'by_year':
            start = datetime.strptime(time_start, '%d-%m-%Y')
            end = datetime.strptime(time_end, '%d-%m-%Y')
            str_time = 'n?m ' + str(start.year)
        elif time_type == 'by_month':
            start = datetime.strptime(time_start + " 00:00", '%d-%m-%Y %H:%M')
            end = datetime.strptime(time_end + " 00:00", '%d-%m-%Y %H:%M') + timedelta(days=1)
            str_time = 'tháng ' + str(start.month) + "/" + str(start.year)
        else:
            start = datetime.strptime(time_start + " 00:00", '%d-%m-%Y %H:%M')
            end = datetime.strptime(time_end + " 00:00", '%d-%m-%Y %H:%M') + timedelta(days=1)
            str_time = 'ngày ' + str(start.day) + "/" + str(start.month) + "/" + str(start.year)
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        print("detail" + str(query))
        if query is not None:
            count_by_product = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_download_archieve.price > 0)\
                    (db.clsb_product.product_category == db.clsb_category.id)\
                    (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                    (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (query).select(count,
                                                   db.clsb_download_archieve.product_id,
                                                   db.clsb_product.product_code,
                                                   db.clsb_product.product_title,
                                                   db.clsb_category.category_name,
                                                   db.clsb_class.class_name,
                                                   groupby=(db.clsb_download_archieve.product_id),
                                                   orderby=count)
        else:
            count_by_product = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_download_archieve.price > 0)\
                    (db.clsb_product.product_category == db.clsb_category.id)\
                    (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                    (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            .select(count,
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
        return dict(list_total=list_total, users=users, str_time=str_time, total=total, str_cp = str_cp, str_type=str_type, query=str(query))
    else:
        return "Không thể thống kê vì không đủ tham số"


def update_pay():
    try:
        select_download = db(db.clsb_download_archieve.price > 0)\
                (db.clsb_download_archieve.product_id == db.clsb_product.id)\
                (db.clsb_product.product_category == db.clsb_category.id).select()
        for down in select_download:
            discount = 98
            #select_cate = db(db.clsb_product.product_code == down['clsb_product']['product_code'])\
            #        (db.clsb_product.product_category == db.clsb_category.id)\
            #        (~db.clsb_category.category_parent.belongs([1, 26])).select()
            #if len(select_cate) > 0:
            #    print(down['clsb_product']['product_code'] + ": " + select_cate.first()['clsb_category']['category_code'])
            #    discount = 30
            select_cp = db(db.clsb20_product_cp.product_code == down['clsb_product']['product_code']).select()
            if len(select_cp) > 0:
                discount = usercp.get_discount_value(select_cp.first()['created_by'], db)
            elif down['clsb_category']['category_parent'] is not None and int(down['clsb_category']['category_parent']) not in [1, 26]:
                discount = 30
                print(down['clsb_product']['product_code'] + ": " + down['clsb_category']['category_code'])
            price = int(down['clsb_download_archieve']['price'])
            pay_provider = price * discount / 100
            pay_cp = price - pay_provider
            db(db.clsb_download_archieve.id == down['clsb_download_archieve']['id']).update(pay_provider=pay_provider, pay_cp=pay_cp)
        return "SUCCESS"
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def update_pay_2014():
    try:
        select_download = db(db.clsb_download_archieve_2014.price > 0)\
                (db.clsb_download_archieve_2014.product_id == db.clsb_product.id)\
                (db.clsb_product.product_category == db.clsb_category.id).select()
        for down in select_download:
            discount = 98
            #select_cate = db(db.clsb_product.product_code == down['clsb_product']['product_code'])\
            #        (db.clsb_product.product_category == db.clsb_category.id)\
            #        (~db.clsb_category.category_parent.belongs([1, 26])).select()
            #if len(select_cate) > 0:
            #    print(down['clsb_product']['product_code'] + ": " + select_cate.first()['clsb_category']['category_code'])
            #    discount = 30
            select_cp = db(db.clsb20_product_cp.product_code == down['clsb_product']['product_code']).select()
            if len(select_cp) > 0:
                discount = usercp.get_discount_value(select_cp.first()['created_by'], db)
            elif down['clsb_category']['category_parent'] is not None and int(down['clsb_category']['category_parent']) not in [1, 26]:
                discount = 30
                print(down['clsb_product']['product_code'] + ": " + down['clsb_category']['category_code'])
            price = int(down['clsb_download_archieve_2014']['price'])
            pay_provider = price * discount / 100
            pay_cp = price - pay_provider
            db(db.clsb_download_archieve_2014.id == down['clsb_download_archieve_2014']['id']).update(pay_provider=pay_provider, pay_cp=pay_cp)
        return "SUCCESS"
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def import_buy():
    try:
        select_buy = db(db.clsb30_product_history.created_on >= "2015-10-20 00:00:00")\
                (db.clsb30_product_history.created_on <= "2015-10-26 10:00:00")\
                (db.clsb30_product_history.product_id == db.clsb_product.id)\
                (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
                (db.clsb30_product_history.product_price > 0).select()
        histories = list()
        for buy in select_buy:
            temp = dict()
            temp['user_id'] = buy['clsb30_product_history']['user_id']
            temp['product_id'] = buy['clsb30_product_history']['product_id']
            temp['download_time'] = buy['clsb30_product_history']['created_on']
            temp['price'] = buy['clsb30_product_history']['product_price']
            temp['pay_provider'] = 0
            temp['pay_cp'] = 0
            temp['purchase_type'] = 'WEB_PAY'
            temp['rom_version'] = ""
            temp['device_serial'] = ""
            temp['status'] = 'Completed'
            histories.append(temp)
        #return dict(data=histories)
        db.clsb_download_archieve.bulk_insert(histories)
        return "SUCCESS"
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def export_data():
    try:
        start = int(request.args[0])
        end = int(request.args[1])
        data = list()
        select_product = db(~db.clsb_product.product_code.like("%.%"))\
                (db.clsb_product.product_category == db.clsb_category.id)\
                (~db.clsb_category.category_code.like("%SGK%"))\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.ALL,
                                                                                   db.clsb_dic_creator.creator_name,
                                                                                   orderby=db.clsb_product.product_title,
                                                                                   groupby=db.clsb_product.id,
                                                                                    limitby=(start, end))
        for product in select_product:
            temp = dict()
            temp['product_id'] = product['clsb_product']['id']
            temp['product_code'] = product['clsb_product']['product_code']
            temp['product_title'] = product['clsb_product']['product_title']
            temp['product_price'] = product['clsb_product']['product_price']
            temp['product_description'] = product['clsb_product']['product_description']
            temp['product_status'] = product['clsb_product']['product_status']
            temp['product_creator'] = product['clsb_dic_creator']['creator_name']
            #cover_price
            select_cover_price = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 2).select(db.clsb_product_metadata.metadata_value)
            if len(select_cover_price) > 0:
                temp['cover_price'] = select_cover_price.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['cover_price'] = 0
            #format
            select_format = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 6).select(db.clsb_product_metadata.metadata_value)
            if len(select_format) > 0:
                temp['format'] = select_format.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['format'] = ""
            #page_number
            select_page_number = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 9).select(db.clsb_product_metadata.metadata_value)
            if len(select_page_number) > 0:
                temp['page_number'] = select_page_number.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['page_number'] = ""
            #pub_year
            select_pub_year = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 3).select(db.clsb_product_metadata.metadata_value)
            if len(select_pub_year) > 0:
                temp['pub_year'] = select_pub_year.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['pub_year'] = ""
            #co_author
            select_co_author = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 1).select(db.clsb_product_metadata.metadata_value)
            if len(select_co_author) > 0:
                temp['co_author'] = select_co_author.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['co_author'] = ""
            data.append(temp)
        return dict(datas=data, count=len(select_product))
    except Exception as err:
        import sys
        print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))



def export_data_sgk():
    try:
        start = int(request.args[0])
        end = int(request.args[1])
        data = list()
        select_product = db(~db.clsb_product.product_code.like("%.%"))\
                (db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_category.category_code.like("%SGK%"))\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.ALL,
                                                                                   db.clsb_dic_creator.creator_name,
                                                                                   orderby=db.clsb_product.product_title,
                                                                                   groupby=db.clsb_product.id,
                                                                                    limitby=(start, end))
        for product in select_product:
            temp = dict()
            temp['product_id'] = product['clsb_product']['id']
            temp['product_code'] = product['clsb_product']['product_code']
            temp['product_title'] = product['clsb_product']['product_title']
            temp['product_price'] = product['clsb_product']['product_price']
            temp['product_description'] = product['clsb_product']['product_description']
            temp['product_status'] = product['clsb_product']['product_status']
            temp['product_creator'] = product['clsb_dic_creator']['creator_name']
            #cover_price
            select_cover_price = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 2).select(db.clsb_product_metadata.metadata_value)
            if len(select_cover_price) > 0:
                temp['cover_price'] = select_cover_price.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['cover_price'] = 0
            #format
            select_format = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 6).select(db.clsb_product_metadata.metadata_value)
            if len(select_format) > 0:
                temp['format'] = select_format.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['format'] = ""
            #page_number
            select_page_number = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 9).select(db.clsb_product_metadata.metadata_value)
            if len(select_page_number) > 0:
                temp['page_number'] = select_page_number.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['page_number'] = ""
            #pub_year
            select_pub_year = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 3).select(db.clsb_product_metadata.metadata_value)
            if len(select_pub_year) > 0:
                temp['pub_year'] = select_pub_year.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['pub_year'] = ""
            #co_author
            select_co_author = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 1).select(db.clsb_product_metadata.metadata_value)
            if len(select_co_author) > 0:
                temp['co_author'] = select_co_author.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['co_author'] = ""
            data.append(temp)
        return dict(datas=data, count=len(select_product))
    except Exception as err:
        import sys
        print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def export_data_by_cate():
    try:
        start = int(request.args[0])
        end = int(request.args[1])
        category_id = int(request.args[2])
        print(request.args)
        data = list()
        select_product = db(~db.clsb_product.product_code.like("%.%"))\
                (db.clsb_product.product_status.like("Approved"))\
                (db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_category.category_parent == category_id)\
                (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                (db.clsb_subject_class.class_id == db.clsb_class.id)\
                (db.clsb_subject_class.subject_id == db.clsb_subject.id)\
                (db.clsb_product.device_shelf_code == db.clsb_device_shelf.id)\
                (db.clsb_product.product_creator == db.clsb_dic_creator.id).select(db.clsb_product.ALL,
                                                                                   db.clsb_category.category_name,
                                                                                   db.clsb_device_shelf.device_shelf_code,
                                                                                   db.clsb_class.class_name,
                                                                                   db.clsb_subject.subject_name,
                                                                                   db.clsb_dic_creator.creator_name,
                                                                                   orderby=db.clsb_product.product_title,
                                                                                   groupby=db.clsb_product.id,
                                                                                    limitby=(start, end))
        for product in select_product:
            temp = dict()
            temp['product_id'] = product['clsb_product']['id']
            temp['product_category'] = product['clsb_category']['category_name']
            temp['device_shelf_code'] = product['clsb_device_shelf']['device_shelf_code']
            temp['product_class'] = product['clsb_class']['class_name']
            temp['product_subject'] = product['clsb_subject']['subject_name']
            temp['product_code'] = product['clsb_product']['product_code']
            temp['product_title'] = product['clsb_product']['product_title']
            temp['product_price'] = product['clsb_product']['product_price']
            temp['product_description'] = product['clsb_product']['product_description']
            temp['product_status'] = product['clsb_product']['product_status']
            temp['product_creator'] = product['clsb_dic_creator']['creator_name']
            #cover_price
            select_cover_price = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 2).select(db.clsb_product_metadata.metadata_value)
            if len(select_cover_price) > 0:
                temp['cover_price'] = select_cover_price.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['cover_price'] = 0
            #format
            select_format = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 6).select(db.clsb_product_metadata.metadata_value)
            if len(select_format) > 0:
                temp['format'] = select_format.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['format'] = ""
            #page_number
            select_page_number = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 9).select(db.clsb_product_metadata.metadata_value)
            if len(select_page_number) > 0:
                temp['page_number'] = select_page_number.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['page_number'] = ""
            #pub_year
            select_pub_year = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 3).select(db.clsb_product_metadata.metadata_value)
            if len(select_pub_year) > 0:
                temp['pub_year'] = select_pub_year.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['pub_year'] = ""
            #co_author
            select_co_author = db(db.clsb_product_metadata.product_id == product['clsb_product']['id'])\
                        (db.clsb_product_metadata.metadata_id == 1).select(db.clsb_product_metadata.metadata_value)
            if len(select_co_author) > 0:
                temp['co_author'] = select_co_author.first()[db.clsb_product_metadata.metadata_value]
            else:
                temp['co_author'] = ""
            data.append(temp)
        return dict(datas=data, count=len(select_product))
    except Exception as err:
        import sys
        print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def top_user_naptien():
    try:
        datas = list()
        sum = db.clsb_transaction.amount.sum()
        start = datetime.strptime(str(datetime.now().year), "%Y")
        select_top = db(db.clsb_transaction.status.like("COMPLETE"))\
            (db.clsb_transaction.created_on >= start)\
            (db.clsb_transaction.user_id == db.clsb_user.id).select(sum,
                                                                  db.clsb_user.username,
                                                                  db.clsb_user.firstName,
                                                                  db.clsb_user.lastName,
                                                                  db.clsb_user.phoneNumber,
                                                                groupby=db.clsb_transaction.user_id,
                                                                  orderby=~sum,
                                                                  limitby=(0, 50))
        for user in select_top:
            temp = dict()
            temp['amount'] = user[sum]
            temp['username'] = user[db.clsb_user.username]
            temp['firstName'] = user[db.clsb_user.firstName]
            temp['lastName'] = user[db.clsb_user.lastName]
            temp['phoneNumber'] = user[db.clsb_user.phoneNumber]
            datas.append(temp)
        return dict(datas=datas)
    except Exception as err:
        import sys
        print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def top_user_mua_sach():
    try:
        datas = list()
        count = db.clsb_download_archieve.id.count()
        start = datetime.strptime(str(datetime.now().year), "%Y")
        select_top = db(db.clsb_download_archieve.status.like("Completed"))\
            (db.clsb_download_archieve.created_on >= start)\
            (db.clsb_download_archieve.price > 0)\
            (db.clsb_download_archieve.user_id == db.clsb_user.id)\
            (db.clsb_user.test_user != 1).select(count,
                                                                  db.clsb_user.username,
                                                                  db.clsb_user.firstName,
                                                                  db.clsb_user.lastName,
                                                                  db.clsb_user.phoneNumber,
                                                                groupby=db.clsb_download_archieve.user_id,
                                                                  orderby=~count,
                                                                  limitby=(0, 50))
        for user in select_top:
            temp = dict()
            temp['count'] = user[count]
            temp['username'] = user[db.clsb_user.username]
            temp['firstName'] = user[db.clsb_user.firstName]
            temp['lastName'] = user[db.clsb_user.lastName]
            temp['phoneNumber'] = user[db.clsb_user.phoneNumber]
            datas.append(temp)
        return dict(datas=datas)
    except Exception as err:
        import sys
        print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def export_product_by_cp():
    try:
        products = list()
        select_product = db(~db.clsb20_product_cp.product_code.like("CP%"))\
                (~db.clsb20_product_cp.product_code.like("%.%"))\
                (~db.clsb20_product_cp.product_code.like("Exer%")).select()

        for product in select_product:
            temp = dict()
            temp['product_title'] = product[db.clsb20_product_cp.product_title]
            temp['product_code'] = product[db.clsb20_product_cp.product_code]
            temp['created_by'] = product[db.clsb20_product_cp.created_by]
            products.append(temp)
        return dict(products=products)
    except Exception as err:
        import sys
        print(str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


@auth.requires_authorize()
def cbcode():
    form = SQLFORM.smartgrid(db.cbcode_log, args=request.args[:1],
                             showbuttontext=False,
    )
    return dict(args=True, grid=form)


def paynxb():
    query = ((db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_parent.belongs([1, 26])))
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
        by_day = True


    start = datetime.strptime(str(datetime.now().year), "%Y")
    if by_day:
        start = datetime.now() - timedelta(days=7)
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
            end = datetime.strptime(str(int(request.vars.end) + 1), "%Y")
        elif by_month:
            end = datetime.strptime(request.vars.end, "%m-%Y")
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
    totalAll = dict()
    totalAll['price'] = 0
    totalAll['discount'] = 0
    list_id = list()
    products_list = db((db.clsb_download_archieve.price > 0) & (db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                                   & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                                ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                                (query).select(db.clsb_download_archieve.id, distinct=True)
    import calendar
    if by_year:
        sum = "SUM(clsb_product.product_price)"
        for pd in products_list:
            list_id.append(pd[db.clsb_download_archieve.id])
        count_by_time = db(db.clsb_download_archieve.id.belongs(list_id))\
                (db.clsb_download_archieve.product_id == db.clsb_product.id).select(sum,
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.year()))
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
                sum_price = count_by_time[index][sum]
                discount = sum_price * 14 / 15
                rows = dict()
                rows['download_time'] = str_time
                rows['discount'] = discount
                rows['price'] = sum_price
                rows['start'] = '01-01-' + str_time
                rows['end'] = '31-12-' + str_time
                list_total.append(rows)
                temp.append(sum_price)
                totalAll['discount'] += discount
                totalAll['price'] += sum_price
                data.append(temp)
            else:
                rows = dict()
                rows['download_time'] = str_time
                rows['discount'] = 0
                rows['price'] = 0
                rows['start'] = '01-01-' + str_time
                rows['end'] = '31-12-' + str_time
                list_total.append(rows)
                temp.append(0)
                data.append(temp)
    elif by_month:
        sum = "SUM(clsb_product.product_price)"
        for pd in products_list:
            list_id.append(pd[db.clsb_download_archieve.id])
        count_by_time = db(db.clsb_download_archieve.id.belongs(list_id))\
                (db.clsb_download_archieve.product_id == db.clsb_product.id).select(sum,
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.month(),
                                                            db.clsb_download_archieve.download_time.year()))
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
                        sum_price = count_by_time[index][sum]
                        discount = sum_price * 14 / 15
                        rows = dict()
                        rows['download_time'] = str_time
                        rows['discount'] = discount
                        rows['price'] = sum_price
                        rows['start'] = '01-' + str_time
                        rows['end'] = str_time
                        list_total.append(rows)
                        temp.append(sum_price)
                        totalAll['discount'] += discount
                        totalAll['price'] += sum_price
                        data.append(temp)
                    else:
                        rows = dict()
                        rows['download_time'] = str_time
                        rows['discount'] = 0
                        rows['price'] = 0
                        rows['start'] = str_time
                        rows['end'] = str_time
                        list_total.append(rows)
                        temp.append(0)
                        data.append(temp)
    elif by_day:
        sum = "SUM(clsb_product.product_price)"
        for pd in products_list:
            list_id.append(pd[db.clsb_download_archieve.id])
        count_by_time = db(db.clsb_download_archieve.id.belongs(list_id))\
                (db.clsb_download_archieve.product_id == db.clsb_product.id).select(sum, db.clsb_download_archieve.download_time.day(),
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.day(),
                                                            db.clsb_download_archieve.download_time.month(),
                                                            db.clsb_download_archieve.download_time.year()))
        time_data = list()
        for index_time in count_by_time:
            time_data.append(str(index_time[db.clsb_download_archieve.download_time.day()])
                                    + "-" + str(index_time[db.clsb_download_archieve.download_time.month()])
                                      + "-"
                                        + str(index_time[db.clsb_download_archieve.download_time.year()]))
        for y in range(start.year, maxYear+1):
            for m in range(1, 13):
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
                            sum_price = int(count_by_time[index][sum])
                            discount = sum_price * 14 / 15
                            rows = dict()
                            rows['download_time'] = str_time
                            rows['discount'] = discount
                            rows['price'] = sum_price
                            rows['start'] = str_time
                            rows['end'] = str_time
                            list_total.append(rows)
                            temp.append(sum_price)
                            totalAll['discount'] += discount
                            totalAll['price'] += sum_price
                            data.append(temp)
                        else:
                            rows = dict()
                            rows['download_time'] = str_time
                            rows['discount'] = 0
                            rows['price'] = 0
                            rows['start'] = str_time
                            rows['end'] = str_time
                            list_total.append(rows)
                            temp.append(0)
                            data.append(temp)
    return dict(data=data, totalAll=totalAll, listDownloadTotal=list_total)


def paidnxb():
    query = ((db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_parent.belongs([1, 26])))
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
        by_day = True
    start = datetime.strptime(str(datetime.now().year), "%Y")
    if by_day:
        start = datetime.now() - timedelta(days=7)
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
            end = datetime.strptime("31-12-" + str(request.vars.end) + " 23:59:59", "%d-%m-%Y %H:%M:%S")
        elif by_month:
            end = datetime.strptime(request.vars.end, "%m-%Y") + relativedelta(months=1)
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
    time_type = 'by_month'
    print("All: " + str(query))
    if by_year:
        time_type = 'by_year'
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_download_archieve.price > 0)\
                            (query).select(count,
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
                rows['end'] = '01-01-' + str(y+1)
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
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_download_archieve.price > 0)\
                            (query).select(count,
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                        ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                        (db.clsb_download_archieve.price > 0).select(count,
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
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                            (db.clsb_download_archieve.price > 0)\
                            (db.clsb_product.product_category == db.clsb_category.id)\
                            (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                            (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (query).select(count,
                                                    db.clsb_download_archieve.download_time.day(),
                                                   db.clsb_download_archieve.download_time.month(),
                                                   db.clsb_download_archieve.download_time.year(),
                                                   groupby=(db.clsb_download_archieve.download_time.day(),
                                                            db.clsb_download_archieve.download_time.month(),
                                                            db.clsb_download_archieve.download_time.year()))
        else:
            count_by_time = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                        ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                        (db.clsb_download_archieve.price > 0).select(count,
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
    return dict(data=data, totalAll=totalAll, listDownloadTotal=list_total, time=time_type,
                start=start.strftime("%d-%m-%Y"), end=end.strftime("%d-%m-%Y"))


def paidnxb_details():
    if request.args and len(request) > 2:
        time_type = request.args[0]
        time_start = request.args[1]
        time_end = request.args[2]

        query = ((db.clsb_product.product_category == db.clsb_category.id) & (db.clsb_category.category_parent.belongs([1, 26])))
        import calendar
        str_time = ''
        if time_type == 'by_year':
            start = datetime.strptime(time_start, '%d-%m-%Y')
            end = datetime.strptime(time_end, '%d-%m-%Y')
            str_time = 'năm ' + str(start.year)
        elif time_type == 'by_month':
            start = datetime.strptime(time_start + " 00:00", '%d-%m-%Y %H:%M')
            end = datetime.strptime(time_end + " 00:00", '%d-%m-%Y %H:%M') + timedelta(days=1)
            str_time = 'tháng ' + str(start.month) + "/" + str(start.year)
        else:
            start = datetime.strptime(time_start + " 00:00", '%d-%m-%Y %H:%M')
            end = datetime.strptime(time_end + " 00:00", '%d-%m-%Y %H:%M') + timedelta(days=1)
            str_time = 'ngày ' + str(start.day) + "/" + str(start.month) + "/" + str(start.year)
        count = "COUNT(DISTINCT clsb_download_archieve.id)"
        print("detail" + str(query))
        count_by_product = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.user_id == db.clsb_user.id)
                               & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_user.test_user == 0))\
                            ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_download_archieve.price > 0)\
                    (db.clsb_product.product_category == db.clsb_category.id)\
                    (db.clsb_product.subject_class == db.clsb_subject_class.id)\
                    (db.clsb_subject_class.class_id == db.clsb_class.id)\
                            (query).select(count,
                                                   db.clsb_download_archieve.product_id,
                                                   db.clsb_product.product_code,
                                                    db.clsb_product.product_price,
                                                   db.clsb_product.product_title,
                                                   db.clsb_category.category_name,
                                                   db.clsb_class.class_name,
                                                   groupby=(db.clsb_download_archieve.product_id),
                                                   orderby=count)
        list_total = list()
        total = 0
        total_price = 0
        for count_product in count_by_product:
            product = dict()
            product['id'] = count_product[db.clsb_download_archieve.product_id]
            product['product_code'] = count_product[db.clsb_product.product_code]
            product['product_price'] = count_product[db.clsb_product.product_price]
            product['product_title'] = count_product[db.clsb_product.product_title]
            product['download_time'] = count_product[count]
            product['category'] = count_product[db.clsb_category.category_name]
            product['class'] = count_product[db.clsb_class.class_name]
            product['paid'] = int(count_product[count]) * int(product['product_price'])
            list_total.append(product)
            total += int(count_product[count])
            total_price += product['paid']
        list_total.reverse()
        return dict(list_total=list_total, str_time=str_time, total=total, query=str(query), total_price=total_price)
    else:
        return "Không thể thống kê vì không đủ tham số"
