# -*- coding: utf-8 -*-
__author__ = 'tanbm'
import usercp
from dateutil.relativedelta import relativedelta
from datetime import date, timedelta

def index():
    return dict()


# @auth.requires_authorize()
def downloaded_old():
    query = db(db.clsb20_product_cp)\
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (((db.clsb20_product_cp.created_by == db.auth_user.id) & (db.auth_user.created_by == auth.user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))
    # query = db(db.clsb20_product_cp)\
    #         ((db.clsb20_product_cp.created_by == db.auth_user.id) | (db.clsb20_product_cp.created_by == auth.user.id))\
    #         (db.auth_user.created_by == auth.user.id)

    query_location = None
    district = None
    province = db(db.clsb_province).select()
    province_select = province
    if request.vars.province:
        if (int(request.vars.province) != 0) & (int(request.vars.province) != -1):
            # if not request.vars.district or int(request.vars.district) == 0:
            query_location = (db.clsb_province.id == int(request.vars.province))
            # else:
            #     query_location = (db.clsb_user.district == int(request.vars.district))
        elif int(request.vars.province) == -1:
            query_locationB = None
            if request.vars.select_province:
                if type(request.vars.select_province) == type(list()):
                    query_locationB = (db.clsb_province.id.belongs(request.vars.select_province))
                    # for i in range(1, len(request.vars.select_province)):
                    #     query_locationB = query_locationB | (db.clsb_province.id == request.vars.select_province[i])
                else:
                    query_locationB = (db.clsb_province.id == request.vars.select_province)
                print query_locationB
            query_location = query_locationB
        province_select = db(query_location).select(groupby=db.clsb_province.id)
        print db(query_location)
    if query_location != None:
        query_location = query_location & (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    else:
        query_location = (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)

    query_device = (db.clsb_download_archieve.rom_version.like("%%"))
    if request.vars.device:
        if int(request.vars.device) == 1:
            query_device = (db.clsb_download_archieve.rom_version.like("CB.%"))
        if int(request.vars.device) == 2:
            query_device = (db.clsb_download_archieve.rom_version.like("CBT.%"))

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



    products = query.select(groupby=db.clsb20_product_cp.product_code)
    queryB = None
    if request.vars.select:
        if request.vars.select != "select" and request.vars.select != "all":
            query = query(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product_type.id == db.clsb_category.category_type)\
                (db.clsb_product_type.type_name.like(request.vars.select))
        if request.vars.select == "select":
            if type(request.vars.selectProduct) == type(list()):
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct[0])
                for i in range(1, len(request.vars.selectProduct)):
                    queryB = queryB | (db.clsb20_product_cp.id == request.vars.selectProduct[i])
            else:
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct)

            # productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


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

    print start, end
    maxMonth = datetime.now().month
    maxYear = datetime.now().year

    if end.year < maxYear:
        maxYear = end.year
        maxMonth = 12
    if end.month != maxMonth:
        maxMonth = end.month

    data = list()
    totalData = list()

    downloads = list()

    listDownload = list()
    listDownloadTotal = list()
    listProvince = list()
    list_product = list()
    dataProvince = list()
    for item in productsList:
        list_product.append(item['clsb_product']['id'])

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
            tempTotal = list()
            tempTotal.append(str(y))
            temp.append(str(y))
            total_all = 0
            timeStart = datetime.strptime(str(y), "%Y")
            timeEnd = datetime.strptime(str(y+1), "%Y")

            prov_one = list()
            prov_one.append(str(y))
            for prov in province_select:
                try:
                    id = prov.id
                except:
                    id = prov['clsb_province']['id']
                downloads = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed') & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id == id).select(groupby=db.clsb_download_archieve.id)
                rows = dict()
                rows['download_time'] = str(y)
                rows['province'] = db(db.clsb_province.id == id).select()[0]['province_name']
                rows['total_download'] = len(downloads)

                prov_one.append(len(downloads))
                listProvince.append(rows)
            dataProvince.append(prov_one)
            for product in productsList:
                downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                    ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                    (query_location).select(groupby=db.clsb_download_archieve.id)
                # downloads = db(db.clsb_download_archieve)\
                #     ((db.clsb_download_archieve.download_time >= timeStart) & (db.clsb_download_archieve.download_time < timeEnd)).select()

                total_one = len(downloads)
                total_all += len(downloads)
                rows = dict()
                rows['start'] = str(timeStart.day)+"-"+str(timeStart.month)+"-"+str(timeStart.year)
                rows['end'] = str(timeEnd.day)+"-"+str(timeEnd.month)+"-"+str(timeEnd.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = str(y)
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['total_download'] = total_one
                listDownload.append(rows)
                temp.append(total_one)
            tempTotal.append(total_all)
            data.append(temp)
            totalData.append(tempTotal)
        elif by_month:
            for i in range(min, max+1):
                temp = list()
                tempTotal = list()
                tempTotal.append(str(i)+"/"+str(y))
                temp.append(str(i)+"/"+str(y))
                total_all = 0
                timeStart = datetime.strptime(str(y)+"-"+str(i), "%Y-%m")
                timeEnd = None
                if i == 12:
                    timeEnd = datetime.strptime(str(y+1)+"-"+str(1), "%Y-%m")
                else:
                    timeEnd = datetime.strptime(str(y)+"-"+str(i+1), "%Y-%m")
                prov_one = list()
                prov_one.append(str(i)+"/"+str(y))
                for prov in province_select:
                    try:
                        id = prov.id
                    except:
                        id = prov['clsb_province']['id']
                    downloads = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                        (db.clsb_download_archieve.product_id.belongs(list_product))\
                        ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                        (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id == id).select(groupby=db.clsb_download_archieve.id)
                    rows = dict()
                    rows['download_time'] = str(i)+"/"+str(y)
                    rows['province'] = db(db.clsb_province.id == id).select()[0]['province_name']
                    rows['total_download'] = len(downloads)
                    prov_one.append(len(downloads))
                    listProvince.append(rows)
                dataProvince.append(prov_one)

                for product in productsList:
                    downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                        ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                        (query_location).select(groupby=db.clsb_download_archieve.id)
                    # downloads = db(db.clsb_download_archieve)\
                    #     ((db.clsb_download_archieve.download_time >= timeStart) & (db.clsb_download_archieve.download_time < timeEnd)).select()

                    total_one = len(downloads)
                    total_all += len(downloads)
                    rows = dict()
                    rows['start'] = str(timeStart.day)+"-"+str(timeStart.month)+"-"+str(timeStart.year)
                    rows['end'] = str(timeEnd.day)+"-"+str(timeEnd.month)+"-"+str(timeEnd.year)
                    rows['product_id'] = product['clsb20_product_cp']['id']
                    rows['product_code'] = product['clsb20_product_cp']['product_code']
                    rows['download_time'] = str(i)+"/"+str(y)
                    rows['product_title'] = product['clsb20_product_cp']['product_title']
                    rows['product_id'] = product['clsb20_product_cp']['id']
                    rows['product_id'] = product['clsb20_product_cp']['id']
                    rows['product_status'] = product['clsb20_product_cp']['product_status']
                    rows['total_download'] = total_one
                    listDownload.append(rows)
                    temp.append(total_one)
                tempTotal.append(total_all)
                data.append(temp)
                totalData.append(tempTotal)
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
                    tempTotal = list()
                    tempTotal.append(str(d)+"/"+str(i)+"/"+str(y))
                    temp.append(str(d)+"/"+str(i)+"/"+str(y))
                    total_all = 0
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
                    prov_one = list()
                    prov_one.append(str(d)+"/"+str(i)+"/"+str(y))
                    for prov in province_select:
                        try:
                            id = prov.id
                        except:
                            id = prov['clsb_province']['id']
                        downloads = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                            (db.clsb_download_archieve.product_id.belongs(list_product))\
                            ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                            (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id == id).select(groupby=db.clsb_download_archieve.id)
                        rows = dict()
                        rows['download_time'] = str(d)+"/"+str(i)+"/"+str(y)
                        rows['province'] = db(db.clsb_province.id == id).select()[0]['province_name']
                        rows['total_download'] = len(downloads)
                        prov_one.append(len(downloads))
                        listProvince.append(rows)
                    dataProvince.append(prov_one)

                    for product in productsList:
                        downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                            ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                            (query_location).select(groupby=db.clsb_download_archieve.id)
                        # downloads = db(db.clsb_download_archieve)\
                        #     ((db.clsb_download_archieve.download_time >= timeStart) & (db.clsb_download_archieve.download_time < timeEnd)).select()

                        total_one = len(downloads)
                        total_all += len(downloads)
                        rows = dict()
                        rows['start'] = str(timeStart.day)+"-"+str(timeStart.month)+"-"+str(timeStart.year)
                        rows['end'] = str(timeEnd.day)+"-"+str(timeEnd.month)+"-"+str(timeEnd.year)
                        rows['product_id'] = product['clsb20_product_cp']['id']
                        rows['product_code'] = product['clsb20_product_cp']['product_code']
                        rows['download_time'] = str(d)+"/"+str(i)+"/"+str(y)
                        rows['product_title'] = product['clsb20_product_cp']['product_title']
                        rows['product_id'] = product['clsb20_product_cp']['id']
                        rows['product_id'] = product['clsb20_product_cp']['id']
                        rows['product_status'] = product['clsb20_product_cp']['product_status']
                        rows['total_download'] = total_one
                        listDownload.append(rows)
                        temp.append(total_one)
                    data.append(temp)
                    tempTotal.append(total_all)
                    totalData.append(tempTotal)

    total_download = 0
    for product in productsList:
        timeStart = start
        timeEnd = end
        if by_year:
            timeStart = datetime.strptime(str(start.year), "%Y")
            timeEnd = datetime.strptime(str(end.year+1), "%Y")
        elif by_month:
            timeStart = datetime.strptime(str(start.year)+"-"+str(start.month), "%Y-%m")
            timeEnd = datetime.strptime(str(end.year)+"-"+str(end.month+1), "%Y-%m")


        downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
            ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
            (query_location).select(groupby=db.clsb_download_archieve.id)
        # downloads = db(db.clsb_download_archieve)\
        #             ((db.clsb_download_archieve.download_time >= start) & (db.clsb_download_archieve.download_time <= end)).select()
        rows = dict()
        rows['start'] = str(timeStart.day)+"-"+str(timeStart.month)+"-"+str(timeStart.year)
        rows['end'] = str(timeEnd.day)+"-"+str(timeEnd.month)+"-"+str(timeEnd.year)
        rows['product_id'] = product['clsb20_product_cp']['id']
        rows['product_code'] = product['clsb20_product_cp']['product_code']
        rows['download_time'] = str(start.month)+"/"+str(start.year)+"-"+str(end.month)+"/"+str(end.year)
        rows['product_title'] = product['clsb20_product_cp']['product_title']
        rows['product_id'] = product['clsb20_product_cp']['id']
        rows['product_status'] = product['clsb20_product_cp']['product_status']
        rows['total_download'] = len(downloads)
        total_download += len(downloads)
        listDownloadTotal.append(rows)

    print data
    # print totalData
    return dict(data=data, listDownloadTotal=listDownloadTotal, total_download=total_download,
                listDownload=listDownload,
                productsList=productsList, totalData=totalData, products=products,
                province=province,
                province_select=province_select,
                listProvince=listProvince,
                dataProvince=dataProvince)


@auth.requires_authorize()
def payment_old():
    query = db(db.clsb20_product_cp)\
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (((db.auth_user.created_by == auth.user.id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))\
            (db.clsb20_product_purchase_item.product_code.like(db.clsb20_product_cp.product_code))\
            (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
            (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type)

    query_location = None
    district = None
    discount_value = usercp.get_discount_value(auth.user.id,db)
    province = db(db.clsb_province).select()
    province_select = province
    if request.vars.province:
        if (int(request.vars.province) != 0) & (int(request.vars.province) != -1):
            # if not request.vars.district or int(request.vars.district) == 0:
            query_location = (db.clsb_province.id == int(request.vars.province))
            # else:
            #     query_location = (db.clsb_user.district == int(request.vars.district))
        elif int(request.vars.province) == -1:
            query_locationB = None
            if request.vars.select_province:
                if type(request.vars.select_province) == type(list()):
                    query_locationB = (db.clsb_province.id.belongs(request.vars.select_province))
                    # for i in range(1, len(request.vars.select_province)):
                    #     query_locationB = query_locationB | (db.clsb_province.id == request.vars.select_province[i])
                else:
                    query_locationB = (db.clsb_province.id == request.vars.select_province)
                print query_locationB
            query_location = query_locationB
        province_select = db(query_location).select(groupby=db.clsb_province.id)
        print db(query_location)
    if query_location != None:
        query_location = query_location & (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    else:
        query_location = (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)

    query_device = (db.clsb_download_archieve.rom_version.like("%%"))
    if request.vars.device:
        if int(request.vars.device) == 1:
            query_device = (db.clsb_download_archieve.rom_version.like("CB.%"))
        if int(request.vars.device) == 2:
            query_device = (db.clsb_download_archieve.rom_version.like("CBT.%"))

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

    products = query.select(groupby=db.clsb20_product_cp.product_code)
    queryB = None
    if request.vars.select:
        if request.vars.select != "select" and request.vars.select != "all":
            query = query(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product_type.id == db.clsb_category.category_type)\
                (db.clsb_product_type.type_name.like(request.vars.select))
        if request.vars.select == "select":
            if type(request.vars.selectProduct) == type(list()):
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct[0])
                for i in range(1,len(request.vars.selectProduct)):
                    queryB = queryB | (db.clsb20_product_cp.id == request.vars.selectProduct[i])
            else:
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct)

            # productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


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

    print start, end
    maxMonth = datetime.now().month
    maxYear = datetime.now().year

    if end.year < maxYear:
        maxYear = end.year
        maxMonth = 12
    if end.month != maxMonth:
        maxMonth = end.month

    tableList = list()
    totalData = list()
    data = list()
    dataAll = list()
    list_product = list()
    listProvince = list()
    dataProvince = list()
    for item in productsList:
        list_product.append(item['clsb_product']['id'])

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
            tempTotal = list()
            tempTotal.append(str(y))
            timeStart = datetime.strptime(str(y), "%Y")
            timeEnd = datetime.strptime(str(y+1), "%Y")
            total_all = 0
            prov_one = list()
            prov_one.append(str(y))
            for prov in province_select:
                try:
                    id = prov.id
                except:
                    id = prov['clsb_province']['id']
                downloads = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id == id).select(groupby=db.clsb_download_archieve.id)
                price = 0
                for download in downloads:
                    price += download['clsb_download_archieve']['price']
                rows = dict()
                rows['download_time'] = str(y)
                rows['province'] = db(db.clsb_province.id == id).select()[0]['province_name']
                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                prov_one.append(rows['total_payment'])
                listProvince.append(rows)
            dataProvince.append(prov_one)
            for product in productsList:
                rows = dict()
                rows['start'] = str(timeStart.day)+"-"+str(timeStart.month)+"-"+str(timeStart.year)
                rows['end'] = str(timeEnd.day)+"-"+str(timeEnd.month)+"-"+str(timeEnd.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = str(y)
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = product['clsb20_purchase_item']['description']

                price = 0
                downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                    ((db.clsb_download_archieve.download_time >= timeStart) & (db.clsb_download_archieve.download_time < timeEnd))\
                    (query_location).select(groupby=db.clsb_download_archieve.id)
                for download in downloads:
                    try:
                        price += download['clsb_download_archieve']['price']
                    except Exception as e:
                        price += download['price']

                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                temp.append(rows['total_payment'])
                total_all += rows['total_price']
                tableList.append(rows)
            data.append(temp)
            tempTotal.append(total_all)
            dataAll.append(tempTotal)

        elif by_month:
            for i in range(min, max+1):
                timeStart = datetime.strptime(str(y)+"-"+str(i), "%Y-%m")
                timeEnd = None
                if i == 12:
                    timeEnd = datetime.strptime(str(y+1)+"-"+str(1), "%Y-%m")
                else:
                    timeEnd = datetime.strptime(str(y)+"-"+str(i+1), "%Y-%m")

                temp = list()
                temp.append(str(i)+"/"+str(y))
                tempTotal = list()
                tempTotal.append(str(i)+"/"+str(y))
                total_all = 0
                prov_one = list()
                prov_one.append(str(i)+"/"+str(y))
                for prov in province_select:
                    try:
                        id = prov.id
                    except:
                        id = prov['clsb_province']['id']
                    downloads = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                        (db.clsb_download_archieve.product_id.belongs(list_product))\
                        ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                        (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id == id).select(groupby=db.clsb_download_archieve.id)
                    price = 0
                    for download in downloads:
                        price += download['clsb_download_archieve']['price']
                    rows = dict()
                    rows['download_time'] = str(i)+"/"+str(y)
                    rows['province'] = db(db.clsb_province.id == id).select()[0]['province_name']
                    rows['total_price'] = price
                    rows['total_discount'] = price*discount_value/100
                    rows['total_payment'] = price - price*discount_value/100
                    prov_one.append(rows['total_payment'])
                    listProvince.append(rows)
                dataProvince.append(prov_one)

                for product in productsList:
                    rows = dict()
                    rows['start'] = str(timeStart.day)+"-"+str(timeStart.month)+"-"+str(timeStart.year)
                    rows['end'] = str(timeEnd.day)+"-"+str(timeEnd.month)+"-"+str(timeEnd.year)
                    rows['product_id'] = product['clsb20_product_cp']['id']
                    rows['product_code'] = product['clsb20_product_cp']['product_code']
                    rows['download_time'] = str(i)+"/"+str(y)
                    rows['product_title'] = product['clsb20_product_cp']['product_title']
                    rows['product_status'] = product['clsb20_product_cp']['product_status']
                    rows['purchase_type'] = product['clsb20_purchase_item']['description']

                    price = 0
                    downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                        ((db.clsb_download_archieve.download_time >= timeStart) & (db.clsb_download_archieve.download_time < timeEnd))\
                        (query_location).select(groupby=db.clsb_download_archieve.id)
                    for download in downloads:
                        try:
                            price += download['clsb_download_archieve']['price']
                        except Exception as e:
                            price += download['price']

                    rows['total_price'] = price
                    rows['total_discount'] = price*discount_value/100
                    rows['total_payment'] = price - price*discount_value/100
                    total_all += rows['total_price']
                    temp.append(rows['total_payment'])

                    tableList.append(rows)
                data.append(temp)
                tempTotal.append(total_all)
                dataAll.append(tempTotal)
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
                    tempTotal = list()
                    tempTotal.append(str(d)+"/"+str(i)+"/"+str(y))
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
                    total_all = 0

                    prov_one = list()
                    prov_one.append(str(d)+"/"+str(i)+"/"+str(y))
                    for prov in province_select:
                        try:
                            id = prov.id
                        except:
                            id = prov['clsb_province']['id']

                        downloads = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                            (db.clsb_download_archieve.product_id.belongs(list_product))\
                            ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time <= timeEnd))\
                            (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id == id).select(groupby=db.clsb_download_archieve.id)
                        price = 0
                        for download in downloads:
                            price += download['clsb_download_archieve']['price']
                        rows = dict()
                        rows['download_time'] = str(d)+"/"+str(i)+"/"+str(y)
                        rows['province'] = db(db.clsb_province.id == id).select()[0]['province_name']
                        rows['total_price'] = price
                        rows['total_discount'] = price*discount_value/100
                        rows['total_payment'] = price - price*discount_value/100
                        prov_one.append(rows['total_payment'])
                        listProvince.append(rows)
                    dataProvince.append(prov_one)
                    for product in productsList:
                        rows = dict()
                        rows['start'] = str(timeStart.day)+"-"+str(timeStart.month)+"-"+str(timeStart.year)
                        rows['end'] = str(timeEnd.day)+"-"+str(timeEnd.month)+"-"+str(timeEnd.year)
                        rows['product_id'] = product['clsb20_product_cp']['id']
                        rows['product_code'] = product['clsb20_product_cp']['product_code']
                        rows['download_time'] = str(d)+"/"+str(i)+"/"+str(y)
                        rows['product_title'] = product['clsb20_product_cp']['product_title']
                        rows['product_status'] = product['clsb20_product_cp']['product_status']
                        rows['purchase_type'] = product['clsb20_purchase_item']['description']

                        price = 0
                        downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
                            ((db.clsb_download_archieve.download_time >= timeStart) & (db.clsb_download_archieve.download_time < timeEnd))\
                            (query_location).select(groupby=db.clsb_download_archieve.id)
                        for download in downloads:
                            try:
                                price += download['clsb_download_archieve']['price']
                            except Exception as e:
                                price += download['price']

                        rows['total_price'] = price
                        rows['total_discount'] = price*discount_value/100
                        rows['total_payment'] = price - price*discount_value/100
                        total_all += rows['total_price']
                        temp.append(rows['total_payment'])

                        tableList.append(rows)
                    data.append(temp)
                    tempTotal.append(total_all)
                    dataAll.append(tempTotal)
    total_price = 0
    total_discount = 0
    total_payment = 0

    for product in productsList:
        timeStart = start
        timeEnd = end
        if by_year:
            timeStart = datetime.strptime(str(start.year), "%Y")
            timeEnd = datetime.strptime(str(end.year+1), "%Y")
        elif by_month:
            timeStart = datetime.strptime(str(start.year)+"-"+str(start.month), "%Y-%m")
            timeEnd = datetime.strptime(str(end.year)+"-"+str(end.month+1), "%Y-%m")
        rows = dict()
        rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
        rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
        rows['product_id'] = product['clsb20_product_cp']['id']
        rows['product_code'] = product['clsb20_product_cp']['product_code']
        rows['download_time'] = str(start.day)+"/"+str(start.month)+"/"+str(start.year)+"-"+str(end.day)+"/"+str(end.month)+"/"+str(end.year)
        rows['product_title'] = product['clsb20_product_cp']['product_title']
        rows['purchase_type'] = product['clsb20_purchase_item']['description']
        rows['product_status'] = product['clsb20_product_cp']['product_status']
        price = 0
        downloads = db((db.clsb_download_archieve.product_id == product['clsb_product']['id']) & (db.clsb_download_archieve.status.like('Completed')) & query_device)\
            ((db.clsb_download_archieve.download_time > timeStart) & (db.clsb_download_archieve.download_time < timeEnd))\
            (query_location).select(groupby=db.clsb_download_archieve.id)
        for download in downloads:
            try:
                price += download['clsb_download_archieve']['price']
            except Exception as e:
                price += download['price']

        rows['total_price'] = price
        total_price += price
        rows['total_discount'] = price*discount_value/100
        total_discount += price*discount_value/100
        rows['total_payment'] = price - price*discount_value/100
        total_payment += price - price*discount_value/100
        totalData.append(rows)
    province = db(db.clsb_province).select()
    return dict(
        tableList=tableList, totalData=totalData, data=data, dataAll=dataAll, products=products, productsList=productsList,
        total_price=total_price,
        total_payment=total_payment,
        total_discount=total_discount,
        province=province,
        listProvince=listProvince,
        dataProvince=dataProvince,
        province_select=province_select
    )


@auth.requires_signature()
def viewlogs():
    product_id = request.args[0]
    query_location = None
    query_device = (db.clsb_download_archieve.rom_version.like("%%"))
    if request.vars.device:
        if int(request.vars.device) == 1:
            query_device = (db.clsb_download_archieve.rom_version.like("CB.%"))
        if int(request.vars.device) == 2:
            query_device = (db.clsb_download_archieve.rom_version.like("CBT.%"))
    if request.vars.province:
        if (int(request.vars.province) != 0) & (int(request.vars.province) != -1):
            # if not request.vars.district or int(request.vars.district) == 0:
            query_location = (db.clsb_province.id == int(request.vars.province))
            # else:
            #     query_location = (db.clsb_user.district == int(request.vars.district))
        elif int(request.vars.province) == -1:
            query_locationB = None
            if request.vars.select_province:
                if type(request.vars.select_province) == type(list()):
                    query_locationB = (db.clsb_province.id.belongs(request.vars.select_province))
                    # for i in range(1, len(request.vars.select_province)):
                    #     query_locationB = query_locationB | (db.clsb_province.id == request.vars.select_province[i])
                else:
                    query_locationB = (db.clsb_province.id == request.vars.select_province)
            query_location = query_locationB
        print db(query_location)
    if query_location != None:
        query_location = query_location & (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    else:
        query_location = (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    start = datetime.strptime(str(datetime.now().year), "%Y")
    end = datetime.now()
    if request.args[1]:
        start = datetime.strptime(request.args[1], "%d-%m-%Y")
    if request.args[2]:
        end = datetime.strptime(request.args[2], "%d-%m-%Y")

    query = db(db.clsb_download_archieve)\
        ((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.status.like('Completed')) & (db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time < end) & query_device)\
                    (query_location)\
                    (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
                    (db.clsb20_product_cp.id == product_id)
    product = db(db.clsb20_product_cp.id == product_id).select().first()
    downloads = query.select(groupby=db.clsb_download_archieve.id)
    total_price = 0
    for down in downloads:
        total_price += down['clsb_download_archieve']['price']
    return dict(list=downloads, product=product, total_price=total_price)

#Tiench test
# @auth.requires_authorize()
def downloaded():
    # query (chưa run) điều kiện đầu vào get các product thuộc quyền quản lý của tài khoản này và nhóm CP này.
    query = db(db.clsb20_product_cp)\
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (((db.clsb20_product_cp.created_by == db.auth_user.id) & (db.auth_user.created_by == auth.user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))
    # query = db(db.clsb20_product_cp)\
    #         ((db.clsb20_product_cp.created_by == db.auth_user.id) | (db.clsb20_product_cp.created_by == auth.user.id))\
    #         (db.auth_user.created_by == auth.user.id)
    # print(query)
    """
    # query_location tạo thêm diều kiện query với tuỳ chọn theo tỉnh thành nếu có request với province
    # district tạm thời chưa giải quyết với district
    # province
    # sử dụng dữ liệu địa chỉ của người dùng tải về
    """
    query_location = None
    district = None
    province = db(db.clsb_province).select()
    province_select = province
    if request.vars.province:
        if (int(request.vars.province) != 0) & (int(request.vars.province) != -1):
            # if not request.vars.district or int(request.vars.district) == 0:
            query_location = (db.clsb_province.id == int(request.vars.province))
            # else:
            #     query_location = (db.clsb_user.district == int(request.vars.district))
        elif int(request.vars.province) == -1:
            query_locationB = None
            if request.vars.select_province:
                if type(request.vars.select_province) == type(list()):
                    query_locationB = (db.clsb_province.id.belongs(request.vars.select_province))
                    # for i in range(1, len(request.vars.select_province)):
                    #     query_locationB = query_locationB | (db.clsb_province.id == request.vars.select_province[i])
                else:
                    query_locationB = (db.clsb_province.id == request.vars.select_province)
                # print query_locationB
            query_location = query_locationB
        province_select = db(query_location).select(groupby=db.clsb_province.id)
        # print db(query_location)
    if query_location != None:
        query_location = query_location & (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    else:
        query_location = (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    """
    # query_device lấy điều kiện query cho phiên bản ROM tải về. Mặc định accept tất.
        Khi có tuỳ chọn theo thiết bị thì thay đổi theo bản giáo viên or học sinh
    """
    query_device = (db.clsb_download_archieve.rom_version.like("%%"))
    if request.vars.device:
        if int(request.vars.device) == 1:
            query_device = (db.clsb_download_archieve.rom_version.like("CB.%"))
        if int(request.vars.device) == 2:
            query_device = (db.clsb_download_archieve.rom_version.like("CBT.%"))


    """
    # by_year, day, month check dữ liệu yêu cầu trả về là theo ngày, tháng hay năm
    """
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




    """
    # products query lấy tất cả danh sách products user có thể xem theo điều kiện biến query ở trên
    """

    products = query.select(groupby=db.clsb20_product_cp.product_code)
    """
    # queryB mặc định là none
    # khi có điều kiện select all hoặc từng product hay category product queryB sẽ được tạo điều kiện query
    """
    queryB = None
    if request.vars.select:
        if request.vars.select != "select" and request.vars.select != "all":
            query = query(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product_type.id == db.clsb_category.category_type)\
                (db.clsb_product_type.type_name.like(request.vars.select))
        if request.vars.select == "select":
            if type(request.vars.selectProduct) == type(list()):
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct[0])
                for i in range(1, len(request.vars.selectProduct)):
                    queryB = queryB | (db.clsb20_product_cp.id == request.vars.selectProduct[i])
            else:
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct)

            # productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    """
    lấy dữ liệu products cần thống kê với kết hợp giữa biến query và queryB
    """
    productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    """
    start, end là thời gian bắt đầu đến kết thúc của request yêu cầu thống kê
    mặc định là bắt đầu vào đầu năm, hiện tại và kết thúc tại thời điểm hiện tại (ngày yêu cầu thống kê)
    Khi có request về thời gian bắt đầu và kết thúc + điều kiện thống kê theo tháng, năm hay ngày thì bắt đầu gán giá trị cho start, end
    """
    import calendar
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
            end = datetime.strptime(request.vars.end + "-12-31", "%Y-%m-%d")
        elif by_month:
            end1 = datetime.strptime(request.vars.end, "%m-%Y")
            end = datetime.strptime(str(calendar.monthrange(end1.year, end1.month)[1]) + "-" + request.vars.end, "%d-%m-%Y")
        elif by_day:
            end1 = datetime.strptime(request.vars.end, "%d-%m-%Y")
            month = int(end1.month)
            day = int(end1.day)
            if end1.day < calendar.monthrange(end1.year, end1.month)[1]:
                day += 1
            else:
                day = 1
                month += 1
            end = datetime.strptime(str(day) + "-" + str(month) + "-" + str(end1.year), "%d-%m-%Y")

    print start, end


    """
    thời gian tối đa có thể xem với tháng và năm lấy theo thời điểm hiện tại
    """
    maxMonth = datetime.now().month
    maxYear = datetime.now().year

    if end.year < maxYear:
        maxYear = end.year
        maxMonth = 12
    if end.month != maxMonth:
        maxMonth = end.month


    """
    # data là dữ liệu tải về cho từng sản phẩm theo từng năm
    # totalData là dữ liệu tải về tổng các sản phẩm theo từng năm
    """
    data = list()
    totalData = list()

    # Dữ liệu tải về sau khi được query theo các điều kiện lập ở trên
    downloads = list()

    """
    listDownload, listDownloadTotal mang thông tin từng dòng dữ liệu vs tên sản phẩm + số lượt tải
    listProvince mang thông tin tỉnh thành khi có thống kê theo tỉnh thành
    """
    listDownload = list()
    listDownloadTotal = list()
    listProvince = list()
    list_product = list()
    dataProvince = list()

    """
    List products là thông tin chứa id các products được thống kê
    """
    for item in productsList:
        list_product.append(item['clsb_product']['id'])

    list_province = list()
    try:
        for prov in province_select:
            list_province.append(prov['id'])
    except Exception as err:
        print(err)

    total_download = 0

    print(start)
    print(end)

    if by_year:
        try:
            count = db.clsb_download_archieve.id.count()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(count,
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.year()))
            # print(len(count_by_time))
            # print(count_by_time)



            # Tinh theo product

            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                & (db.clsb_download_archieve.status.like('Completed'))
                                & (db.clsb_user.test_user == 0)
                                & (db.clsb_download_archieve.product_id.belongs(list_product))
                                & (db.clsb_download_archieve.download_time > start)
                                & (db.clsb_download_archieve.download_time < end)
                                & query_device).select(count,
                                                       db.clsb_download_archieve.product_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_download_archieve.product_id,
                                                       db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            product_dict = dict()
            # print(count_by_product)
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]

                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = item_product[db.clsb_download_archieve.download_time.year()]
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['total_download'] = item_product[count]
                listDownload.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = int(item_product[count])

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(count,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_province[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                rows['total_download'] = int(item_province[count])
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = int(item_province[count])

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                temp.append(str_time)
                temp_prov = list()
                temp_prov.append(str_time)
                if str_time in time_data:
                    index = time_data.index(str_time)
                    total_data=[]
                    total_data.append(str(count_by_time[index][db.clsb_download_archieve.download_time.year()]))
                    total_data.append(int(count_by_time[index][count]))
                    total_download += int(count_by_time[index][count])
                    totalData.append(total_data)
                else:
                    total_data=[]
                    total_data.append(str_time)
                    total_data.append(0)
                    totalData.append(total_data)

                for product_id in list_product:
                    if product_dict.has_key(str_time + "-" + str(product_id)):
                        temp.append(product_dict.get(str_time + "-" + str(product_id)))
                    else:
                        temp.append(0)
                data.append(temp)

                for prov_id in list_province:
                    if prov_dict.has_key(str_time + "-" + str(prov_id)):
                        temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                    else:
                        temp_prov.append(0)
                dataProvince.append(temp_prov)

        except Exception as err:
            print(err)
    elif by_month:
        try:
            #Tinh theo thoi gian
            count = db.clsb_download_archieve.id.count()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time < end)
                        & query_device & query_location).select(count,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
            # print(len(test))
            # print(test)

            # Tinh theo product

            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                & (db.clsb_download_archieve.status.like('Completed'))
                                & (db.clsb_user.test_user == 0)
                                & (db.clsb_download_archieve.product_id.belongs(list_product))
                                & (db.clsb_download_archieve.download_time > start)
                                & (db.clsb_download_archieve.download_time < end)
                                & query_device).select(count,
                                                       db.clsb_download_archieve.product_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       db.clsb_download_archieve.download_time.month(),
                                                       groupby=(db.clsb_download_archieve.product_id,
                                                                db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            # print(count_by_product)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" +str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['total_download'] = item_product[count]
                listDownload.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = int(item_product[count])

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(count,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       db.clsb_download_archieve.download_time.month(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.month(),
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_province[db.clsb_download_archieve.download_time.month()]) + "/" +str(item_province[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                rows['total_download'] = int(item_province[count])
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = int(item_province[count])

            #Tong hop du lieu

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.month()])
                                  + "/"
                                    + str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    time = datetime.strptime(str(y)+"-"+str(m), "%Y-%m")
                    if time <= end and time >= start:

                        str_time = str(m) + "/" + str(y)
                        temp = list()
                        temp.append(str_time)
                        temp_prov = list()
                        temp_prov.append(str_time)
                        if str_time in time_data:
                            index = time_data.index(str_time)
                            total_data=[]
                            total_data.append(str(count_by_time[index][db.clsb_download_archieve.download_time.month()])
                                              + "/"
                                                + str(count_by_time[index][db.clsb_download_archieve.download_time.year()]))
                            total_data.append(int(count_by_time[index][count]))
                            total_download += int(count_by_time[index][count])
                            totalData.append(total_data)
                        else:
                            total_data=[]
                            total_data.append(str_time)
                            total_data.append(0)
                            totalData.append(total_data)
                        for product_id in list_product:
                            if product_dict.has_key(str_time + "-" + str(product_id)):
                                temp.append(product_dict.get(str_time + "-" + str(product_id)))
                            else:
                                temp.append(0)
                        data.append(temp)
                        for prov_id in list_province:
                            if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                            else:
                                temp_prov.append(0)
                        dataProvince.append(temp_prov)
            print("province" + str(dataProvince))
        except Exception as err:
            print(err)
    elif by_day:
        try:
            count = db.clsb_download_archieve.id.count()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(count,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               db.clsb_download_archieve.download_time.day(),
                                               groupby=(db.clsb_download_archieve.download_time.month(),
                                                        db.clsb_download_archieve.download_time.year(),
                                                        db.clsb_download_archieve.download_time.day()))

            # Tinh theo product

            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                & (db.clsb_download_archieve.status.like('Completed'))
                                & (db.clsb_user.test_user == 0)
                                & (db.clsb_download_archieve.product_id.belongs(list_product))
                                & (db.clsb_download_archieve.download_time > start)
                                & (db.clsb_download_archieve.download_time <= end)
                                & query_device).select(count,
                                                       db.clsb_download_archieve.product_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.day(),
                                                       groupby=(db.clsb_download_archieve.product_id,
                                                                db.clsb_download_archieve.download_time.day(),
                                                                db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            product_dict = dict()
            # print(count_by_product)
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" +str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['total_download'] = item_product[count]
                listDownload.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = int(item_product[count])

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed') & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(count,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.day(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.day(),
                                                                db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" +str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                rows['total_download'] = int(item_province[count])
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = int(item_province[count])

            #Tong hop du lieu

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.day()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve.download_time.month()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    max_day = calendar.monthrange(y, m)[1]
                    for d in range(1, max_day + 1):
                        time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                        if time <= end and time >= start:
                            str_time = str(d) + "/" + str(m) + "/" + str(y)
                            temp = list()
                            temp.append(str_time)
                            temp_prov = list()
                            temp_prov.append(str_time)
                            if str_time in time_data:
                                index = time_data.index(str_time)
                                total_data=[]
                                total_data.append(str_time)
                                total_data.append(int(count_by_time[index][count]))
                                total_download += int(count_by_time[index][count])
                                totalData.append(total_data)
                            else:
                                total_data=[]
                                total_data.append(str_time)
                                total_data.append(0)
                                totalData.append(total_data)

                            for product_id in list_product:
                                if product_dict.has_key(str_time + "-" + str(product_id)):
                                    temp.append(product_dict.get(str_time + "-" + str(product_id)))
                                else:
                                    temp.append(0)
                            data.append(temp)
                            for prov_id in list_province:
                                if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                    temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                                else:
                                    temp_prov.append(0)
                            dataProvince.append(temp_prov)

        except Exception as err:
            print(err)

    # Tinh theo product

    # count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
    #                     & (db.clsb_download_archieve.status.like('Completed'))
    #                     & (db.clsb_download_archieve.product_id.belongs(list_product))
    #                     & (db.clsb_download_archieve.download_time > start)
    #                     & (db.clsb_download_archieve.download_time < end)
    #                     & query_device).select(count,
    #                                            db.clsb_download_archieve.product_id,
    #                                            db.clsb_download_archieve.download_time,
    #                                            groupby=db.clsb_download_archieve.product_id)
    # # print(count_by_product)
    # for item_product in count_by_product:
    #     id = item_product[db.clsb_download_archieve.product_id]
    #     index_product = list_product.index(id)
    #     product = productsList[index_product]
    #     rows = dict()
    #     rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
    #     rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
    #     rows['product_id'] = product['clsb20_product_cp']['id']
    #     rows['product_code'] = product['clsb20_product_cp']['product_code']
    #     rows['download_time'] = item_product[db.clsb_download_archieve.download_time]
    #     rows['product_title'] = product['clsb20_product_cp']['product_title']
    #     rows['product_id'] = product['clsb20_product_cp']['id']
    #     rows['product_id'] = product['clsb20_product_cp']['id']
    #     rows['product_status'] = product['clsb20_product_cp']['product_status']
    #     rows['total_download'] = item_product[count]
    #     listDownload.append(rows)

    return dict(data=data, listDownloadTotal=listDownloadTotal, total_download=total_download,
                listDownload=listDownload,
                productsList=productsList, totalData=totalData, products=products,
                province=province,
                province_select=province_select,
                listProvince=listProvince,
                dataProvince=dataProvince)


# @auth.requires_authorize()
def payment():
    query = db(db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (((db.auth_user.created_by == auth.user.id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))
    query_location = None
    district = None
    discount_value = usercp.get_discount_value(auth.user.id,db)
    province = db(db.clsb_province).select()
    province_select = province
    if request.vars.province:
        if (int(request.vars.province) != 0) & (int(request.vars.province) != -1):
            # if not request.vars.district or int(request.vars.district) == 0:
            query_location = (db.clsb_province.id == int(request.vars.province))
            # else:
            #     query_location = (db.clsb_user.district == int(request.vars.district))
        elif int(request.vars.province) == -1:
            query_locationB = None
            if request.vars.select_province:
                if type(request.vars.select_province) == type(list()):
                    query_locationB = (db.clsb_province.id.belongs(request.vars.select_province))
                    # for i in range(1, len(request.vars.select_province)):
                    #     query_locationB = query_locationB | (db.clsb_province.id == request.vars.select_province[i])
                else:
                    query_locationB = (db.clsb_province.id == request.vars.select_province)
                print query_locationB
            query_location = query_locationB
        province_select = db(query_location).select(groupby=db.clsb_province.id)
        print db(query_location)
    if query_location != None:
        query_location = query_location & (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    else:
        query_location = (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)

    query_device = (db.clsb_download_archieve.rom_version.like("%%"))
    if request.vars.device:
        if int(request.vars.device) == 1:
            query_device = (db.clsb_download_archieve.rom_version.like("CB.%"))
        if int(request.vars.device) == 2:
            query_device = (db.clsb_download_archieve.rom_version.like("CBT.%"))

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

    products = query.select(groupby=db.clsb20_product_cp.product_code)
    queryB = None
    if request.vars.select:
        if request.vars.select != "select" and request.vars.select != "all":
            query = query(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product_type.id == db.clsb_category.category_type)\
                (db.clsb_product_type.type_name.like(request.vars.select))
        if request.vars.select == "select":
            if type(request.vars.selectProduct) == type(list()):
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct[0])
                for i in range(1,len(request.vars.selectProduct)):
                    queryB = queryB | (db.clsb20_product_cp.id == request.vars.selectProduct[i])
            else:
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct)

            # productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)

    import calendar
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
            end = datetime.strptime(request.vars.end + "-12-31", "%Y-%m-%d")
        elif by_month:
            end1 = datetime.strptime(request.vars.end, "%m-%Y")
            end = datetime.strptime(str(calendar.monthrange(end1.year, end1.month)[1]) + "-" + request.vars.end + " 23:59:59", "%d-%m-%Y %H:%M:%S")
            #end = end + timedelta(days=1)
        elif by_day:
            end1 = datetime.strptime(request.vars.end, "%d-%m-%Y")
            month = int(end1.month)
            day = int(end1.day)
            if end1.day < calendar.monthrange(end1.year, end1.month):
                day += 1
            else:
                day = 1
                month += 1
            end = datetime.strptime(str(day) + "-" + str(month) + "-" + str(end1.year), "%d-%m-%Y")

    # print start, end
    maxMonth = datetime.now().month
    maxYear = datetime.now().year

    if end.year < maxYear:
        maxYear = end.year
        maxMonth = 12
    if end.month != maxMonth:
        maxMonth = end.month

    tableList = list()
    totalData = list()
    data = list()
    dataAll = list()
    datacp = list()
    list_product = list()
    listProvince = list()
    dataProvince = list()
    for item in productsList:
        list_product.append(item['clsb_product']['id'])

    list_province = list()
    try:
        for prov in province_select:
            list_province.append(prov['id'])
    except Exception as err:
        print(err)

    total_price = 0
    print(start)
    print(end)
    sum = db.clsb_download_archieve.price.sum()
    sum_p = db.clsb_download_archieve.pay_provider.sum()
    sum_c = db.clsb_download_archieve.pay_cp.sum()
    count = db.clsb_download_archieve.id.count()
    if by_year:
        try:
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user != 1)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(sum, sum_p, sum_c,
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.year()))
            # print(len(count_by_time))
            # print(count_by_time)



            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve.status.like('Completed'))
                                    & (db.clsb_user.test_user != 1)
                                    & (db.clsb_download_archieve.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve.download_time > start)
                                    & (db.clsb_download_archieve.download_time <= end)
                                    & query_device).select(sum, count, sum_p, sum_c,
                                                           db.clsb_download_archieve.product_id,
                                                           groupby=(db.clsb_download_archieve.product_id))
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = ""
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = ""
                rows['count'] = item_product[count]
                price = int(item_product[sum])
                price_p = int(item_product[sum_p])
                price_c = int(item_product[sum_c])
                rows['total_price'] = price
                rows['total_discount'] = price_c
                rows['total_payment'] = price_p
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum, sum_p, sum_c,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_province[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                price_p = int(item_province[sum_p])
                price_c = int(item_province[sum_c])
                rows['total_price'] = price
                rows['total_discount'] = price_c
                rows['total_payment'] = price_p
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                temp.append(str_time)
                temp_prov = list()
                temp_prov.append(str_time)
                if str_time in time_data:
                    index = time_data.index(str_time)
                    total_data=[]
                    cp_data = []
                    total_data.append(str(count_by_time[index][db.clsb_download_archieve.download_time.year()]))
                    total_data.append(int(count_by_time[index][sum]))
                    cp_data.append(int(count_by_time[index][sum_p])*85/100)
                    cp_data.append(int(count_by_time[index][sum_c])*85/100)
                    total_price += int(count_by_time[index][sum])
                    price = int(count_by_time[index][sum])
                    price_c = int(count_by_time[index][sum_c])
                    price_p = int(count_by_time[index][sum_p])
                    total_payment += price_p*85/100
                    total_discount += price_c*85/100
                    total_phi += price*15/100
                    dataAll.append(total_data)
                    datacp.append(cp_data)
                else:
                    total_data=[]
                    cp_data = []
                    total_data.append(str_time)
                    total_data.append(0)
                    cp_data.append(0)
                    cp_data.append(0)
                    dataAll.append(total_data)
                    datacp.append(cp_data)
                for product_id in list_product:
                    if product_dict.has_key(str_time + "-" + str(product_id)):
                        temp.append(product_dict.get(str_time + "-" + str(product_id)))
                    else:
                        temp.append(0)
                data.append(temp)
                for prov_id in list_province:
                    if prov_dict.has_key(str_time + "-" + str(prov_id)):
                        temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                    else:
                        temp_prov.append(0)
                dataProvince.append(temp_prov)

        except Exception as err:
            print(err)
    elif by_month:
        try:
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(sum, sum_p, sum_c,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
            # print(len(test))
            # print(test)

            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve.status.like('Completed'))
                                    & (db.clsb_user.test_user == 0)
                                    & (db.clsb_download_archieve.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve.download_time > start)
                                    & (db.clsb_download_archieve.download_time <= end)
                                    & (db.clsb_download_archieve.price > 0)
                                    & query_device).select(sum, count, sum_p, sum_c,
                                                           db.clsb_download_archieve.product_id,
                                                           db.clsb_download_archieve.download_time.month(),
                                                           db.clsb_download_archieve.download_time.year(),
                                                           groupby=(db.clsb_download_archieve.product_id))
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = ""
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = ""
                rows['count'] = item_product[count]
                price = int(item_product[sum])
                price_p = int(item_product[sum_p])
                price_c = int(item_product[sum_c])

                rows['total_price'] = price
                rows['total_discount'] = price_p
                rows['total_payment'] = price_c
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum, sum_p, sum_c,
                                                        db.clsb_district.province_id,
                                                        db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.month(),
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                price_p = int(item_province[sum_p])
                price_c = int(item_province[sum_c])
                rows['total_price'] = price
                rows['total_discount'] = price_p
                rows['total_payment'] = price_c
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.month()])
                                  + "/"
                                    + str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    time = datetime.strptime(str(y)+"-"+str(m), "%Y-%m")
                    if time <= end and time >= start:
                        str_time = str(m) + "/" + str(y)
                        temp = list()
                        temp.append(str_time)
                        temp_prov = list()
                        temp_prov.append(str_time)
                        if str_time in time_data:
                            index = time_data.index(str_time)
                            total_data=[]
                            cp_data = []
                            total_data.append(str(count_by_time[index][db.clsb_download_archieve.download_time.month()])
                                              + "/"
                                                + str(count_by_time[index][db.clsb_download_archieve.download_time.year()]))
                            total_data.append(int(count_by_time[index][sum]))
                            cp_data.append(int(count_by_time[index][sum_p])*85/100)
                            cp_data.append(int(count_by_time[index][sum_c])*85/100)
                            total_price += int(count_by_time[index][sum])
                            price = int(count_by_time[index][sum])
                            total_payment += price_p*85/100
                            total_discount += price_c*85/100
                            total_phi += price*15/100
                            dataAll.append(total_data)
                            datacp.append(cp_data)
                        else:
                            total_data=[]
                            cp_data = []
                            total_data.append(str_time)
                            total_data.append(0)
                            cp_data.append(0)
                            cp_data.append(0)
                            dataAll.append(total_data)
                            datacp.append(cp_data)

                        for product_id in list_product:
                            if product_dict.has_key(str_time + "-" + str(product_id)):
                                temp.append(product_dict.get(str_time + "-" + str(product_id)))
                            else:
                                temp.append(0)
                        data.append(temp)
                        for prov_id in list_province:
                            if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                            else:
                                temp_prov.append(0)
                        dataProvince.append(temp_prov)
        except Exception as err:
            print(err)
    elif by_day:
        try:
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(sum, sum_p, sum_c,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               db.clsb_download_archieve.download_time.day(),
                                               groupby=(db.clsb_download_archieve.download_time.month(),
                                                        db.clsb_download_archieve.download_time.year(),
                                                        db.clsb_download_archieve.download_time.day()))


            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve.status.like('Completed'))
                                    & (db.clsb_user.test_user == 0)
                                    & (db.clsb_download_archieve.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve.download_time > start)
                                    & (db.clsb_download_archieve.download_time <= end)
                                    & query_device).select(sum, count, sum_p, sum_c,
                                                           db.clsb_download_archieve.product_id,
                                                           groupby=db.clsb_download_archieve.product_id)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = ""
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = ""
                rows['count'] = item_product[count]
                price = int(item_product[sum])
                price_p = int(item_product[sum_p])
                price_c = int(item_product[sum_c])

                rows['total_price'] = price
                rows['total_discount'] = price_p
                rows['total_payment'] = price_c
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed') & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum, sum_p, sum_c,
                                                        db.clsb_district.province_id,
                                                        db.clsb_download_archieve.download_time.day(),
                                                        db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.day(),
                                                                db.clsb_download_archieve.download_time.month(),
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                price_p = int(item_province[sum_p])
                price_c = int(item_province[sum_c])
                rows['total_price'] = price
                rows['total_discount'] = price_p
                rows['total_payment'] = price_c
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.day()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve.download_time.month()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    max_day = calendar.monthrange(y, m)[1]
                    for d in range(1, max_day + 1):
                        time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                        if time < end and time >= start:
                            str_time = str(d) + "/" + str(m) + "/" + str(y)
                            temp = list()
                            temp.append(str_time)
                            temp_prov = list()
                            temp_prov.append(str_time)
                            if str_time in time_data:
                                index = time_data.index(str_time)
                                total_data=[]
                                cp_data = []
                                total_data.append(str_time)
                                total_data.append(int(count_by_time[index][sum]))
                                cp_data.append(int(count_by_time[index][sum_p])*85/100)
                                cp_data.append(int(count_by_time[index][sum_c])*85/100)
                                total_price += int(count_by_time[index][sum])
                                price = int(count_by_time[index][sum])
                                total_payment += price_p*85/100
                                total_discount += price_c*85/100
                                total_phi += price*15/100
                                dataAll.append(total_data)
                            else:
                                total_data=[]
                                cp_data = []
                                total_data.append(str_time)
                                total_data.append(0)
                                cp_data.append(0)
                                cp_data.append(0)
                                dataAll.append(total_data)
                                datacp.append(cp_data)
                            for product_id in list_product:
                                if product_dict.has_key(str_time + "-" + str(product_id)):
                                    temp.append(product_dict.get(str_time + "-" + str(product_id)))
                                else:
                                    temp.append(0)
                            data.append(temp)
                            for prov_id in list_province:
                                if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                    temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                                else:
                                    temp_prov.append(0)
                            dataProvince.append(temp_prov)
        except Exception as err:
            print(err)

    province = db(db.clsb_province).select()
    return dict(
        tableList=tableList, totalData=totalData, data=data, dataAll=dataAll, products=products, productsList=productsList,
        total_price=total_price,
        total_payment=total_payment,
        total_discount=total_discount,
        total_phi=total_phi,
        province=province,
        listProvince=listProvince,
        dataProvince=dataProvince,
        province_select=province_select,
        datacp=datacp
    )


def payment2014():
    query = db(db.clsb20_product_cp)\
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (((db.auth_user.created_by == auth.user.id) & (db.clsb20_product_cp.created_by == db.auth_user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))\
            (db.clsb20_product_purchase_item.product_code.like(db.clsb20_product_cp.product_code))\
            (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
            (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type)

    query_location = None
    district = None
    discount_value = usercp.get_discount_value(auth.user.id,db)
    province = db(db.clsb_province).select()
    province_select = province
    if request.vars.province:
        if (int(request.vars.province) != 0) & (int(request.vars.province) != -1):
            # if not request.vars.district or int(request.vars.district) == 0:
            query_location = (db.clsb_province.id == int(request.vars.province))
            # else:
            #     query_location = (db.clsb_user.district == int(request.vars.district))
        elif int(request.vars.province) == -1:
            query_locationB = None
            if request.vars.select_province:
                if type(request.vars.select_province) == type(list()):
                    query_locationB = (db.clsb_province.id.belongs(request.vars.select_province))
                    # for i in range(1, len(request.vars.select_province)):
                    #     query_locationB = query_locationB | (db.clsb_province.id == request.vars.select_province[i])
                else:
                    query_locationB = (db.clsb_province.id == request.vars.select_province)
                print query_locationB
            query_location = query_locationB
        province_select = db(query_location).select(groupby=db.clsb_province.id)
        print db(query_location)
    if query_location != None:
        query_location = query_location & (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    else:
        query_location = (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)

    query_device = (db.clsb_download_archieve_2014.rom_version.like("%%"))
    if request.vars.device:
        if int(request.vars.device) == 1:
            query_device = (db.clsb_download_archieve_2014.rom_version.like("CB.%"))
        if int(request.vars.device) == 2:
            query_device = (db.clsb_download_archieve_2014.rom_version.like("CBT.%"))

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

    products = query.select(groupby=db.clsb20_product_cp.product_code)
    queryB = None
    if request.vars.select:
        if request.vars.select != "select" and request.vars.select != "all":
            query = query(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product_type.id == db.clsb_category.category_type)\
                (db.clsb_product_type.type_name.like(request.vars.select))
        if request.vars.select == "select":
            if type(request.vars.selectProduct) == type(list()):
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct[0])
                for i in range(1,len(request.vars.selectProduct)):
                    queryB = queryB | (db.clsb20_product_cp.id == request.vars.selectProduct[i])
            else:
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct)

            # productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)

    import calendar
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
            end = datetime.strptime(request.vars.end + "-12-31", "%Y-%m-%d")
        elif by_month:
            end1 = datetime.strptime(request.vars.end, "%m-%Y")
            end = datetime.strptime(str(calendar.monthrange(end1.year, end1.month)[1]) + "-" + request.vars.end + " 23:59:59", "%d-%m-%Y %H:%M:%S")
            #end = end + timedelta(days=1)
        elif by_day:
            end1 = datetime.strptime(request.vars.end, "%d-%m-%Y")
            month = int(end1.month)
            day = int(end1.day)
            if end1.day < calendar.monthrange(end1.year, end1.month):
                day += 1
            else:
                day = 1
                month += 1
            end = datetime.strptime(str(day) + "-" + str(month) + "-" + str(end1.year), "%d-%m-%Y")

    # print start, end
    maxMonth = datetime.now().month
    maxYear = datetime.now().year

    if end.year < maxYear:
        maxYear = end.year
        maxMonth = 12
    if end.month != maxMonth:
        maxMonth = end.month

    tableList = list()
    totalData = list()
    data = list()
    dataAll = list()
    list_product = list()
    listProvince = list()
    dataProvince = list()
    for item in productsList:
        list_product.append(item['clsb_product']['id'])

    list_province = list()
    try:
        for prov in province_select:
            list_province.append(prov['id'])
    except Exception as err:
        print(err)

    total_price = 0
    print(start)
    print(end)

    if by_year:
        try:
            sum = db.clsb_download_archieve_2014.price.sum()
            count_by_time = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve_2014.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve_2014.product_id.belongs(list_product))
                        & (db.clsb_download_archieve_2014.download_time > start)
                        & (db.clsb_download_archieve_2014.download_time <= end)
                        & query_device & query_location).select(sum,
                                               db.clsb_download_archieve_2014.download_time.year(),
                                               groupby=(db.clsb_download_archieve_2014.download_time.year()))
            # print(len(count_by_time))
            # print(count_by_time)



            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve_2014.status.like('Completed'))
                                    & (db.clsb_user.test_user == 0)
                                    & (db.clsb_download_archieve_2014.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve_2014.download_time > start)
                                    & (db.clsb_download_archieve_2014.download_time <= end)
                                    & query_device).select(sum,
                                                           db.clsb_download_archieve_2014.product_id,
                                                           db.clsb_download_archieve_2014.download_time.year(),
                                                           groupby=(db.clsb_download_archieve_2014.product_id,
                                                                    db.clsb_download_archieve_2014.download_time.year()),
                                                           orderby=db.clsb_download_archieve_2014.download_time)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve_2014.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] =str(item_product[db.clsb_download_archieve_2014.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = product['clsb20_purchase_item']['description']

                price = int (item_product[sum])

                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id) & (db.clsb_download_archieve_2014.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve_2014.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve_2014.download_time > start) & (db.clsb_download_archieve_2014.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve_2014.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve_2014.download_time.year()),
                                                       orderby=db.clsb_download_archieve_2014.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_province[db.clsb_download_archieve_2014.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve_2014.download_time.year()]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                temp.append(str_time)
                temp_prov = list()
                temp_prov.append(str_time)
                if str_time in time_data:
                    index = time_data.index(str_time)
                    total_data=[]
                    total_data.append(str(count_by_time[index][db.clsb_download_archieve_2014.download_time.year()]))
                    total_data.append(int(count_by_time[index][sum]))
                    total_price += int(count_by_time[index][sum])
                    price = int(count_by_time[index][sum])
                    total_payment += price*85/100 - (price*85/100)*discount_value/100
                    total_discount += (price*85/100)*discount_value/100
                    total_phi += price*15/100
                    dataAll.append(total_data)
                else:
                    total_data=[]
                    total_data.append(str_time)
                    total_data.append(0)
                    dataAll.append(total_data)
                for product_id in list_product:
                    if product_dict.has_key(str_time + "-" + str(product_id)):
                        temp.append(product_dict.get(str_time + "-" + str(product_id)))
                    else:
                        temp.append(0)
                data.append(temp)
                for prov_id in list_province:
                    if prov_dict.has_key(str_time + "-" + str(prov_id)):
                        temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                    else:
                        temp_prov.append(0)
                dataProvince.append(temp_prov)

        except Exception as err:
            print(err)
    elif by_month:
        try:
            #Tinh theo thoi gian
            sum = db.clsb_download_archieve_2014.price.sum()
            count_by_time = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve_2014.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve_2014.product_id.belongs(list_product))
                        & (db.clsb_download_archieve_2014.download_time > start)
                        & (db.clsb_download_archieve_2014.download_time <= end)
                        & query_device & query_location).select(sum,
                                               db.clsb_download_archieve_2014.download_time.month(),
                                               db.clsb_download_archieve_2014.download_time.year(),
                                               groupby=(db.clsb_download_archieve_2014.download_time.month(), db.clsb_download_archieve_2014.download_time.year()))
            # print(len(test))
            # print(test)

            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve_2014.status.like('Completed'))
                                    & (db.clsb_user.test_user == 0)
                                    & (db.clsb_download_archieve_2014.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve_2014.download_time > start)
                                    & (db.clsb_download_archieve_2014.download_time <= end)
                                    & query_device).select(sum,
                                                           db.clsb_download_archieve_2014.product_id,
                                                           db.clsb_download_archieve_2014.download_time.month(),
                                                           db.clsb_download_archieve_2014.download_time.year(),
                                                           groupby=(db.clsb_download_archieve_2014.product_id,
                                                                    db.clsb_download_archieve_2014.download_time.month(),
                                                                    db.clsb_download_archieve_2014.download_time.year()),
                                                           orderby=db.clsb_download_archieve_2014.download_time)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve_2014.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] =  str(item_product[db.clsb_download_archieve_2014.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve_2014.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = product['clsb20_purchase_item']['description']

                price = int (item_product[sum])

                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            count_by_province = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id) & (db.clsb_download_archieve_2014.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve_2014.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve_2014.download_time > start) & (db.clsb_download_archieve_2014.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum,
                                                        db.clsb_district.province_id,
                                                        db.clsb_download_archieve_2014.download_time.month(),
                                                       db.clsb_download_archieve_2014.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve_2014.download_time.month(),
                                                                db.clsb_download_archieve_2014.download_time.year()),
                                                       orderby=db.clsb_download_archieve_2014.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_product[db.clsb_download_archieve_2014.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve_2014.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve_2014.download_time.month()])
                                  + "/"
                                    + str(test_item[db.clsb_download_archieve_2014.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    time = datetime.strptime(str(y)+"-"+str(m), "%Y-%m")
                    if time <= end and time >= start:
                        str_time = str(m) + "/" + str(y)
                        temp = list()
                        temp.append(str_time)
                        temp_prov = list()
                        temp_prov.append(str_time)
                        if str_time in time_data:
                            index = time_data.index(str_time)
                            total_data=[]
                            total_data.append(str(count_by_time[index][db.clsb_download_archieve_2014.download_time.month()])
                                              + "/"
                                                + str(count_by_time[index][db.clsb_download_archieve_2014.download_time.year()]))
                            total_data.append(int(count_by_time[index][sum]))
                            total_price += int(count_by_time[index][sum])
                            price = int(count_by_time[index][sum])
                            total_payment += price*85/100 - (price*85/100)*discount_value/100
                            total_discount += (price*85/100)*discount_value/100
                            total_phi += price*15/100
                            dataAll.append(total_data)
                        else:
                            total_data=[]
                            total_data.append(str_time)
                            total_data.append(0)
                            dataAll.append(total_data)

                        for product_id in list_product:
                            if product_dict.has_key(str_time + "-" + str(product_id)):
                                temp.append(product_dict.get(str_time + "-" + str(product_id)))
                            else:
                                temp.append(0)
                        data.append(temp)
                        for prov_id in list_province:
                            if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                            else:
                                temp_prov.append(0)
                        dataProvince.append(temp_prov)
        except Exception as err:
            print(err)
    elif by_day:
        try:
            sum = db.clsb_download_archieve_2014.price.sum()
            count_by_time = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve_2014.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve_2014.product_id.belongs(list_product))
                        & (db.clsb_download_archieve_2014.download_time > start)
                        & (db.clsb_download_archieve_2014.download_time <= end)
                        & query_device & query_location).select(sum,
                                               db.clsb_download_archieve_2014.download_time.month(),
                                               db.clsb_download_archieve_2014.download_time.year(),
                                               db.clsb_download_archieve_2014.download_time.day(),
                                               groupby=(db.clsb_download_archieve_2014.download_time.month(),
                                                        db.clsb_download_archieve_2014.download_time.year(),
                                                        db.clsb_download_archieve_2014.download_time.day()))


            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve_2014.status.like('Completed'))
                                    & (db.clsb_user.test_user == 0)
                                    & (db.clsb_download_archieve_2014.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve_2014.download_time > start)
                                    & (db.clsb_download_archieve_2014.download_time <= end)
                                    & query_device).select(sum,
                                                           db.clsb_download_archieve_2014.product_id,
                                                           db.clsb_download_archieve_2014.download_time.day(),
                                                           db.clsb_download_archieve_2014.download_time.month(),
                                                           db.clsb_download_archieve_2014.download_time.year(),
                                                           groupby=(db.clsb_download_archieve_2014.product_id,
                                                                    db.clsb_download_archieve_2014.download_time.day(),
                                                                    db.clsb_download_archieve_2014.download_time.month(),
                                                                    db.clsb_download_archieve_2014.download_time.year()),
                                                           orderby=db.clsb_download_archieve_2014.download_time)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve_2014.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] =  str(item_product[db.clsb_download_archieve_2014.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve_2014.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve_2014.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = product['clsb20_purchase_item']['description']

                price = int (item_product[sum])

                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve_2014.user_id == db.clsb_user.id) & (db.clsb_download_archieve_2014.status.like('Completed') & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve_2014.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve_2014.download_time > start) & (db.clsb_download_archieve_2014.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum,
                                                        db.clsb_district.province_id,
                                                        db.clsb_download_archieve_2014.download_time.day(),
                                                        db.clsb_download_archieve_2014.download_time.month(),
                                                       db.clsb_download_archieve_2014.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve_2014.download_time.day(),
                                                                db.clsb_download_archieve_2014.download_time.month(),
                                                                db.clsb_download_archieve_2014.download_time.year()),
                                                       orderby=db.clsb_download_archieve_2014.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_product[db.clsb_download_archieve_2014.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve_2014.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve_2014.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve_2014.download_time.day()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve_2014.download_time.month()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve_2014.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    max_day = calendar.monthrange(y, m)[1]
                    for d in range(1, max_day + 1):
                        time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                        if time < end and time >= start:
                            str_time = str(d) + "/" + str(m) + "/" + str(y)
                            temp = list()
                            temp.append(str_time)
                            temp_prov = list()
                            temp_prov.append(str_time)
                            if str_time in time_data:
                                index = time_data.index(str_time)
                                total_data=[]
                                total_data.append(str_time)
                                total_data.append(int(count_by_time[index][sum]))
                                total_price += int(count_by_time[index][sum])
                                price = int(count_by_time[index][sum])
                                total_payment += price*85/100 - (price*85/100)*discount_value/100
                                total_discount += (price*85/100)*discount_value/100
                                total_phi += price*15/100
                                dataAll.append(total_data)
                            else:
                                total_data=[]
                                total_data.append(str_time)
                                total_data.append(0)
                                dataAll.append(total_data)
                            for product_id in list_product:
                                if product_dict.has_key(str_time + "-" + str(product_id)):
                                    temp.append(product_dict.get(str_time + "-" + str(product_id)))
                                else:
                                    temp.append(0)
                            data.append(temp)
                            for prov_id in list_province:
                                if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                    temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                                else:
                                    temp_prov.append(0)
                            dataProvince.append(temp_prov)
        except Exception as err:
            print(err)

    province = db(db.clsb_province).select()
    return dict(
        tableList=tableList, totalData=totalData, data=data, dataAll=dataAll, products=products, productsList=productsList,
        total_price=total_price,
        total_payment=total_payment,
        total_discount=total_discount,
        total_phi=total_phi,
        province=province,
        listProvince=listProvince,
        dataProvince=dataProvince,
        province_select=province_select
    )


def download_overview():
    query = db(db.clsb20_product_cp)\
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (((db.clsb20_product_cp.created_by == db.auth_user.created_by) & (db.auth_user.id == auth.user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))
    # query = db(db.clsb20_product_cp)\
    #         ((db.clsb20_product_cp.created_by == db.auth_user.id) | (db.clsb20_product_cp.created_by == auth.user.id))\
    #         (db.auth_user.created_by == auth.user.id)
    # print(query)
    """
    # query_location tạo thêm diều kiện query với tuỳ chọn theo tỉnh thành nếu có request với province
    # district tạm thời chưa giải quyết với district
    # province
    # sử dụng dữ liệu địa chỉ của người dùng tải về
    """
    query_location = None
    district = None
    province = db(db.clsb_province).select()
    province_select = province
    if request.vars.province:
        if (int(request.vars.province) != 0) & (int(request.vars.province) != -1):
            # if not request.vars.district or int(request.vars.district) == 0:
            query_location = (db.clsb_province.id == int(request.vars.province))
            # else:
            #     query_location = (db.clsb_user.district == int(request.vars.district))
        elif int(request.vars.province) == -1:
            query_locationB = None
            if request.vars.select_province:
                if type(request.vars.select_province) == type(list()):
                    query_locationB = (db.clsb_province.id.belongs(request.vars.select_province))
                    # for i in range(1, len(request.vars.select_province)):
                    #     query_locationB = query_locationB | (db.clsb_province.id == request.vars.select_province[i])
                else:
                    query_locationB = (db.clsb_province.id == request.vars.select_province)
                # print query_locationB
            query_location = query_locationB
        province_select = db(query_location).select(groupby=db.clsb_province.id)
        # print db(query_location)
    if query_location != None:
        query_location = query_location & (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    else:
        query_location = (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    """
    # query_device lấy điều kiện query cho phiên bản ROM tải về. Mặc định accept tất.
        Khi có tuỳ chọn theo thiết bị thì thay đổi theo bản giáo viên or học sinh
    """
    query_device = (db.clsb_download_archieve.rom_version.like("%%"))
    if request.vars.device:
        if int(request.vars.device) == 1:
            query_device = (db.clsb_download_archieve.rom_version.like("CB.%"))
        if int(request.vars.device) == 2:
            query_device = (db.clsb_download_archieve.rom_version.like("CBT.%"))


    """
    # by_year, day, month check dữ liệu yêu cầu trả về là theo ngày, tháng hay năm
    """
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




    """
    # products query lấy tất cả danh sách products user có thể xem theo điều kiện biến query ở trên
    """

    products = query.select(groupby=db.clsb20_product_cp.product_code)
    """
    # queryB mặc định là none
    # khi có điều kiện select all hoặc từng product hay category product queryB sẽ được tạo điều kiện query
    """
    queryB = None
    if request.vars.select:
        if request.vars.select != "select" and request.vars.select != "all":
            query = query(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product_type.id == db.clsb_category.category_type)\
                (db.clsb_product_type.type_name.like(request.vars.select))
        if request.vars.select == "select":
            if type(request.vars.selectProduct) == type(list()):
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct[0])
                for i in range(1, len(request.vars.selectProduct)):
                    queryB = queryB | (db.clsb20_product_cp.id == request.vars.selectProduct[i])
            else:
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct)

            # productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    """
    lấy dữ liệu products cần thống kê với kết hợp giữa biến query và queryB
    """
    productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    """
    start, end là thời gian bắt đầu đến kết thúc của request yêu cầu thống kê
    mặc định là bắt đầu vào đầu năm, hiện tại và kết thúc tại thời điểm hiện tại (ngày yêu cầu thống kê)
    Khi có request về thời gian bắt đầu và kết thúc + điều kiện thống kê theo tháng, năm hay ngày thì bắt đầu gán giá trị cho start, end
    """
    import calendar
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
            end = datetime.strptime(request.vars.end + "-12-31", "%Y-%m-%d")
        elif by_month:
            end1 = datetime.strptime(request.vars.end, "%m-%Y")
            end = datetime.strptime(str(calendar.monthrange(end1.year, end1.month)[1]) + "-" + request.vars.end, "%d-%m-%Y")
        elif by_day:
            end1 = datetime.strptime(request.vars.end, "%d-%m-%Y")
            month = int(end1.month)
            day = int(end1.day)
            if end1.day < calendar.monthrange(end1.year, end1.month)[1]:
                day += 1
            else:
                day = 1
                month += 1
            end = datetime.strptime(str(day) + "-" + str(month) + "-" + str(end1.year), "%d-%m-%Y")

    print start, end


    """
    thời gian tối đa có thể xem với tháng và năm lấy theo thời điểm hiện tại
    """
    maxMonth = datetime.now().month
    maxYear = datetime.now().year

    if end.year < maxYear:
        maxYear = end.year
        maxMonth = 12
    if end.month != maxMonth:
        maxMonth = end.month


    """
    # data là dữ liệu tải về cho từng sản phẩm theo từng năm
    # totalData là dữ liệu tải về tổng các sản phẩm theo từng năm
    """
    data = list()
    totalData = list()

    # Dữ liệu tải về sau khi được query theo các điều kiện lập ở trên
    downloads = list()

    """
    listDownload, listDownloadTotal mang thông tin từng dòng dữ liệu vs tên sản phẩm + số lượt tải
    listProvince mang thông tin tỉnh thành khi có thống kê theo tỉnh thành
    """
    listDownload = list()
    listDownloadTotal = list()
    listProvince = list()
    list_product = list()
    dataProvince = list()

    """
    List products là thông tin chứa id các products được thống kê
    """
    for item in productsList:
        list_product.append(item['clsb_product']['id'])

    list_province = list()
    try:
        for prov in province_select:
            list_province.append(prov['id'])
    except Exception as err:
        print(err)

    total_download = 0

    print(start)
    print(end)

    if by_year:
        try:
            count = db.clsb_download_archieve.id.count()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(count,
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.year()))
            # print(len(count_by_time))
            # print(count_by_time)



            # Tinh theo product

            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                & (db.clsb_download_archieve.status.like('Completed'))
                                & (db.clsb_user.test_user == 0)
                                & (db.clsb_download_archieve.product_id.belongs(list_product))
                                & (db.clsb_download_archieve.download_time > start)
                                & (db.clsb_download_archieve.download_time < end)
                                & query_device).select(count,
                                                       db.clsb_download_archieve.product_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_download_archieve.product_id,
                                                       db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            product_dict = dict()
            # print(count_by_product)
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]

                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = item_product[db.clsb_download_archieve.download_time.year()]
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['total_download'] = item_product[count]
                listDownload.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = int(item_product[count])

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(count,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_province[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                rows['total_download'] = int(item_province[count])
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = int(item_province[count])

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                temp.append(str_time)
                temp_prov = list()
                temp_prov.append(str_time)
                if str_time in time_data:
                    index = time_data.index(str_time)
                    total_data=[]
                    total_data.append(str(count_by_time[index][db.clsb_download_archieve.download_time.year()]))
                    total_data.append(int(count_by_time[index][count]))
                    total_download += int(count_by_time[index][count])
                    totalData.append(total_data)
                else:
                    total_data=[]
                    total_data.append(str_time)
                    total_data.append(0)
                    totalData.append(total_data)

                for product_id in list_product:
                    if product_dict.has_key(str_time + "-" + str(product_id)):
                        temp.append(product_dict.get(str_time + "-" + str(product_id)))
                    else:
                        temp.append(0)
                data.append(temp)

                for prov_id in list_province:
                    if prov_dict.has_key(str_time + "-" + str(prov_id)):
                        temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                    else:
                        temp_prov.append(0)
                dataProvince.append(temp_prov)

        except Exception as err:
            print(err)
    elif by_month:
        try:
            #Tinh theo thoi gian
            count = db.clsb_download_archieve.id.count()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time < end)
                        & query_device & query_location).select(count,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
            # print(len(test))
            # print(test)

            # Tinh theo product

            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                & (db.clsb_download_archieve.status.like('Completed'))
                                & (db.clsb_user.test_user == 0)
                                & (db.clsb_download_archieve.product_id.belongs(list_product))
                                & (db.clsb_download_archieve.download_time > start)
                                & (db.clsb_download_archieve.download_time < end)
                                & query_device).select(count,
                                                       db.clsb_download_archieve.product_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       db.clsb_download_archieve.download_time.month(),
                                                       groupby=(db.clsb_download_archieve.product_id,
                                                                db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            # print(count_by_product)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" +str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['total_download'] = item_product[count]
                listDownload.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = int(item_product[count])

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(count,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       db.clsb_download_archieve.download_time.month(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.month(),
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_province[db.clsb_download_archieve.download_time.month()]) + "/" +str(item_province[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                rows['total_download'] = int(item_province[count])
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = int(item_province[count])

            #Tong hop du lieu

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.month()])
                                  + "/"
                                    + str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    time = datetime.strptime(str(y)+"-"+str(m), "%Y-%m")
                    if time <= end and time >= start:

                        str_time = str(m) + "/" + str(y)
                        temp = list()
                        temp.append(str_time)
                        temp_prov = list()
                        temp_prov.append(str_time)
                        if str_time in time_data:
                            index = time_data.index(str_time)
                            total_data=[]
                            total_data.append(str(count_by_time[index][db.clsb_download_archieve.download_time.month()])
                                              + "/"
                                                + str(count_by_time[index][db.clsb_download_archieve.download_time.year()]))
                            total_data.append(int(count_by_time[index][count]))
                            total_download += int(count_by_time[index][count])
                            totalData.append(total_data)
                        else:
                            total_data=[]
                            total_data.append(str_time)
                            total_data.append(0)
                            totalData.append(total_data)
                        for product_id in list_product:
                            if product_dict.has_key(str_time + "-" + str(product_id)):
                                temp.append(product_dict.get(str_time + "-" + str(product_id)))
                            else:
                                temp.append(0)
                        data.append(temp)
                        for prov_id in list_province:
                            if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                            else:
                                temp_prov.append(0)
                        dataProvince.append(temp_prov)
            print("province" + str(dataProvince))
        except Exception as err:
            print(err)
    elif by_day:
        try:
            count = db.clsb_download_archieve.id.count()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(count,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               db.clsb_download_archieve.download_time.day(),
                                               groupby=(db.clsb_download_archieve.download_time.month(),
                                                        db.clsb_download_archieve.download_time.year(),
                                                        db.clsb_download_archieve.download_time.day()))

            # Tinh theo product

            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                & (db.clsb_download_archieve.status.like('Completed'))
                                & (db.clsb_user.test_user == 0)
                                & (db.clsb_download_archieve.product_id.belongs(list_product))
                                & (db.clsb_download_archieve.download_time > start)
                                & (db.clsb_download_archieve.download_time <= end)
                                & query_device).select(count,
                                                       db.clsb_download_archieve.product_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.day(),
                                                       groupby=(db.clsb_download_archieve.product_id,
                                                                db.clsb_download_archieve.download_time.day(),
                                                                db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            product_dict = dict()
            # print(count_by_product)
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" +str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['total_download'] = item_product[count]
                listDownload.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = int(item_product[count])

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed') & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(count,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.day(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.day(),
                                                                db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" +str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                rows['total_download'] = int(item_province[count])
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = int(item_province[count])

            #Tong hop du lieu

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.day()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve.download_time.month()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    max_day = calendar.monthrange(y, m)[1]
                    for d in range(1, max_day + 1):
                        time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                        if time <= end and time >= start:
                            str_time = str(d) + "/" + str(m) + "/" + str(y)
                            temp = list()
                            temp.append(str_time)
                            temp_prov = list()
                            temp_prov.append(str_time)
                            if str_time in time_data:
                                index = time_data.index(str_time)
                                total_data=[]
                                total_data.append(str_time)
                                total_data.append(int(count_by_time[index][count]))
                                total_download += int(count_by_time[index][count])
                                totalData.append(total_data)
                            else:
                                total_data=[]
                                total_data.append(str_time)
                                total_data.append(0)
                                totalData.append(total_data)

                            for product_id in list_product:
                                if product_dict.has_key(str_time + "-" + str(product_id)):
                                    temp.append(product_dict.get(str_time + "-" + str(product_id)))
                                else:
                                    temp.append(0)
                            data.append(temp)
                            for prov_id in list_province:
                                if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                    temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                                else:
                                    temp_prov.append(0)
                            dataProvince.append(temp_prov)

        except Exception as err:
            print(err)


    return dict(data=data, listDownloadTotal=listDownloadTotal, total_download=total_download,
                listDownload=listDownload,
                productsList=productsList, totalData=totalData, products=products,
                province=province,
                province_select=province_select,
                listProvince=listProvince,
                dataProvince=dataProvince)


def payment_overview():
    query = db(db.clsb20_product_cp)\
            (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
            (((db.clsb20_product_cp.created_by == db.auth_user.created_by) & (db.auth_user.id == auth.user.id)) | (db.clsb20_product_cp.created_by == auth.user.id))\
            (db.clsb20_product_purchase_item.product_code.like(db.clsb20_product_cp.product_code))\
            (db.clsb20_purchase_item.id == db.clsb20_product_purchase_item.purchase_item)\
            (db.clsb20_purchase_type.id == db.clsb20_purchase_item.purchase_type)

    query_location = None
    district = None
    discount_value = usercp.get_discount_value(auth.user.id,db)
    province = db(db.clsb_province).select()
    province_select = province
    if request.vars.province:
        if (int(request.vars.province) != 0) & (int(request.vars.province) != -1):
            # if not request.vars.district or int(request.vars.district) == 0:
            query_location = (db.clsb_province.id == int(request.vars.province))
            # else:
            #     query_location = (db.clsb_user.district == int(request.vars.district))
        elif int(request.vars.province) == -1:
            query_locationB = None
            if request.vars.select_province:
                if type(request.vars.select_province) == type(list()):
                    query_locationB = (db.clsb_province.id.belongs(request.vars.select_province))
                    # for i in range(1, len(request.vars.select_province)):
                    #     query_locationB = query_locationB | (db.clsb_province.id == request.vars.select_province[i])
                else:
                    query_locationB = (db.clsb_province.id == request.vars.select_province)
                print query_locationB
            query_location = query_locationB
        province_select = db(query_location).select(groupby=db.clsb_province.id)
        print db(query_location)
    if query_location != None:
        query_location = query_location & (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)
    else:
        query_location = (db.clsb_user.district == db.clsb_district.id) & (db.clsb_district.province_id == db.clsb_province.id)

    query_device = (db.clsb_download_archieve.rom_version.like("%%"))
    if request.vars.device:
        if int(request.vars.device) == 1:
            query_device = (db.clsb_download_archieve.rom_version.like("CB.%"))
        if int(request.vars.device) == 2:
            query_device = (db.clsb_download_archieve.rom_version.like("CBT.%"))

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

    products = query.select(groupby=db.clsb20_product_cp.product_code)
    queryB = None
    if request.vars.select:
        if request.vars.select != "select" and request.vars.select != "all":
            query = query(db.clsb_product.product_category == db.clsb_category.id)\
                (db.clsb_product_type.id == db.clsb_category.category_type)\
                (db.clsb_product_type.type_name.like(request.vars.select))
        if request.vars.select == "select":
            if type(request.vars.selectProduct) == type(list()):
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct[0])
                for i in range(1,len(request.vars.selectProduct)):
                    queryB = queryB | (db.clsb20_product_cp.id == request.vars.selectProduct[i])
            else:
                queryB = (db.clsb20_product_cp.id == request.vars.selectProduct)

            # productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)


    productsList = query(queryB).select(groupby=db.clsb20_product_cp.product_code)

    import calendar
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
            end = datetime.strptime(request.vars.end + "-12-31", "%Y-%m-%d")
        elif by_month:
            end1 = datetime.strptime(request.vars.end, "%m-%Y")
            end = datetime.strptime(str(calendar.monthrange(end1.year, end1.month)[1]) + "-" + request.vars.end + " 23:59:59", "%d-%m-%Y %H:%M:%S")
            #end = end + timedelta(days=1)
        elif by_day:
            end1 = datetime.strptime(request.vars.end, "%d-%m-%Y")
            month = int(end1.month)
            day = int(end1.day)
            if end1.day < calendar.monthrange(end1.year, end1.month):
                day += 1
            else:
                day = 1
                month += 1
            end = datetime.strptime(str(day) + "-" + str(month) + "-" + str(end1.year), "%d-%m-%Y")

    # print start, end
    maxMonth = datetime.now().month
    maxYear = datetime.now().year

    if end.year < maxYear:
        maxYear = end.year
        maxMonth = 12
    if end.month != maxMonth:
        maxMonth = end.month

    tableList = list()
    totalData = list()
    data = list()
    dataAll = list()
    list_product = list()
    listProvince = list()
    dataProvince = list()
    for item in productsList:
        list_product.append(item['clsb_product']['id'])

    list_province = list()
    try:
        for prov in province_select:
            list_province.append(prov['id'])
    except Exception as err:
        print(err)

    total_price = 0
    print(start)
    print(end)

    if by_year:
        try:
            sum = db.clsb_download_archieve.price.sum()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(sum,
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.year()))
            # print(len(count_by_time))
            # print(count_by_time)



            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve.status.like('Completed'))
                                    & (db.clsb_user.test_user == 0)
                                    & (db.clsb_download_archieve.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve.download_time > start)
                                    & (db.clsb_download_archieve.download_time <= end)
                                    & query_device).select(sum,
                                                           db.clsb_download_archieve.product_id,
                                                           db.clsb_download_archieve.download_time.year(),
                                                           groupby=(db.clsb_download_archieve.product_id,
                                                                    db.clsb_download_archieve.download_time.year()),
                                                           orderby=db.clsb_download_archieve.download_time)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] =str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = product['clsb20_purchase_item']['description']

                price = int (item_product[sum])

                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum,
                                                        db.clsb_district.province_id,
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_province[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                temp.append(str_time)
                temp_prov = list()
                temp_prov.append(str_time)
                if str_time in time_data:
                    index = time_data.index(str_time)
                    total_data=[]
                    total_data.append(str(count_by_time[index][db.clsb_download_archieve.download_time.year()]))
                    total_data.append(int(count_by_time[index][sum]))
                    total_price += int(count_by_time[index][sum])
                    price = int(count_by_time[index][sum])
                    total_payment += price*85/100 - (price*85/100)*discount_value/100
                    total_discount += (price*85/100)*discount_value/100
                    total_phi += price*15/100
                    dataAll.append(total_data)
                else:
                    total_data=[]
                    total_data.append(str_time)
                    total_data.append(0)
                    dataAll.append(total_data)
                for product_id in list_product:
                    if product_dict.has_key(str_time + "-" + str(product_id)):
                        temp.append(product_dict.get(str_time + "-" + str(product_id)))
                    else:
                        temp.append(0)
                data.append(temp)
                for prov_id in list_province:
                    if prov_dict.has_key(str_time + "-" + str(prov_id)):
                        temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                    else:
                        temp_prov.append(0)
                dataProvince.append(temp_prov)

        except Exception as err:
            print(err)
    elif by_month:
        try:
            #Tinh theo thoi gian
            sum = db.clsb_download_archieve.price.sum()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(sum,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               groupby=(db.clsb_download_archieve.download_time.month(), db.clsb_download_archieve.download_time.year()))
            # print(len(test))
            # print(test)

            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve.status.like('Completed'))
                                    & (db.clsb_user.test_user == 0)
                                    & (db.clsb_download_archieve.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve.download_time > start)
                                    & (db.clsb_download_archieve.download_time <= end)
                                    & query_device).select(sum,
                                                           db.clsb_download_archieve.product_id,
                                                           db.clsb_download_archieve.download_time.month(),
                                                           db.clsb_download_archieve.download_time.year(),
                                                           groupby=(db.clsb_download_archieve.product_id,
                                                                    db.clsb_download_archieve.download_time.month(),
                                                                    db.clsb_download_archieve.download_time.year()),
                                                           orderby=db.clsb_download_archieve.download_time)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] =  str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = product['clsb20_purchase_item']['description']

                price = int (item_product[sum])

                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed')  & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum,
                                                        db.clsb_district.province_id,
                                                        db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.month(),
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.month()])
                                  + "/"
                                    + str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    time = datetime.strptime(str(y)+"-"+str(m), "%Y-%m")
                    if time <= end and time >= start:
                        str_time = str(m) + "/" + str(y)
                        temp = list()
                        temp.append(str_time)
                        temp_prov = list()
                        temp_prov.append(str_time)
                        if str_time in time_data:
                            index = time_data.index(str_time)
                            total_data=[]
                            total_data.append(str(count_by_time[index][db.clsb_download_archieve.download_time.month()])
                                              + "/"
                                                + str(count_by_time[index][db.clsb_download_archieve.download_time.year()]))
                            total_data.append(int(count_by_time[index][sum]))
                            total_price += int(count_by_time[index][sum])
                            price = int(count_by_time[index][sum])
                            total_payment += price*85/100 - (price*85/100)*discount_value/100
                            total_discount += (price*85/100)*discount_value/100
                            total_phi += price*15/100
                            dataAll.append(total_data)
                        else:
                            total_data=[]
                            total_data.append(str_time)
                            total_data.append(0)
                            dataAll.append(total_data)

                        for product_id in list_product:
                            if product_dict.has_key(str_time + "-" + str(product_id)):
                                temp.append(product_dict.get(str_time + "-" + str(product_id)))
                            else:
                                temp.append(0)
                        data.append(temp)
                        for prov_id in list_province:
                            if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                            else:
                                temp_prov.append(0)
                        dataProvince.append(temp_prov)
        except Exception as err:
            print(err)
    elif by_day:
        try:
            sum = db.clsb_download_archieve.price.sum()
            count_by_time = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                        & (db.clsb_download_archieve.status.like('Completed'))
                        & (db.clsb_user.test_user == 0)
                        & (db.clsb_download_archieve.product_id.belongs(list_product))
                        & (db.clsb_download_archieve.download_time > start)
                        & (db.clsb_download_archieve.download_time <= end)
                        & query_device & query_location).select(sum,
                                               db.clsb_download_archieve.download_time.month(),
                                               db.clsb_download_archieve.download_time.year(),
                                               db.clsb_download_archieve.download_time.day(),
                                               groupby=(db.clsb_download_archieve.download_time.month(),
                                                        db.clsb_download_archieve.download_time.year(),
                                                        db.clsb_download_archieve.download_time.day()))


            # Tinh theo product
            total_price = 0
            total_discount = 0
            total_payment = 0
            total_phi = 0
            count_by_product = db((db.clsb_download_archieve.user_id == db.clsb_user.id)
                                    & (db.clsb_download_archieve.status.like('Completed'))
                                    & (db.clsb_user.test_user == 0)
                                    & (db.clsb_download_archieve.product_id.belongs(list_product))
                                    & (db.clsb_download_archieve.download_time > start)
                                    & (db.clsb_download_archieve.download_time <= end)
                                    & query_device).select(sum,
                                                           db.clsb_download_archieve.product_id,
                                                           db.clsb_download_archieve.download_time.day(),
                                                           db.clsb_download_archieve.download_time.month(),
                                                           db.clsb_download_archieve.download_time.year(),
                                                           groupby=(db.clsb_download_archieve.product_id,
                                                                    db.clsb_download_archieve.download_time.day(),
                                                                    db.clsb_download_archieve.download_time.month(),
                                                                    db.clsb_download_archieve.download_time.year()),
                                                           orderby=db.clsb_download_archieve.download_time)
            product_dict = dict()
            for item_product in count_by_product:
                id = item_product[db.clsb_download_archieve.product_id]
                index_product = list_product.index(id)
                product = productsList[index_product]
                rows = dict()
                rows['start'] = str(start.day)+"-"+str(start.month)+"-"+str(start.year)
                rows['end'] = str(end.day)+"-"+str(end.month)+"-"+str(end.year)
                rows['product_id'] = product['clsb20_product_cp']['id']
                rows['product_code'] = product['clsb20_product_cp']['product_code']
                rows['download_time'] =  str(item_product[db.clsb_download_archieve.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['product_title'] = product['clsb20_product_cp']['product_title']
                rows['product_status'] = product['clsb20_product_cp']['product_status']
                rows['purchase_type'] = product['clsb20_purchase_item']['description']

                price = int (item_product[sum])

                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                #total_price += price
                totalData.append(rows)
                tableList.append(rows)
                product_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            #Tinh theo tinh thanh
            count_by_province = db((db.clsb_download_archieve.user_id == db.clsb_user.id) & (db.clsb_download_archieve.status.like('Completed') & (db.clsb_user.test_user == 0) & query_device))\
                    (db.clsb_download_archieve.product_id.belongs(list_product))\
                    ((db.clsb_download_archieve.download_time > start) & (db.clsb_download_archieve.download_time <= end))\
                    (db.clsb_user.district == db.clsb_district.id)(db.clsb_district.province_id.belongs(list_province))\
                                                .select(sum,
                                                        db.clsb_district.province_id,
                                                        db.clsb_download_archieve.download_time.day(),
                                                        db.clsb_download_archieve.download_time.month(),
                                                       db.clsb_download_archieve.download_time.year(),
                                                       groupby=(db.clsb_district.province_id,
                                                                db.clsb_download_archieve.download_time.day(),
                                                                db.clsb_download_archieve.download_time.month(),
                                                                db.clsb_download_archieve.download_time.year()),
                                                       orderby=db.clsb_download_archieve.download_time)
            prov_dict = dict()
            for item_province in count_by_province:
                id = item_province[db.clsb_district.province_id]
                index_prov = list_province.index(id)
                prov = province_select[index_prov]
                rows = dict()
                rows['download_time'] = str(item_product[db.clsb_download_archieve.download_time.day()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.month()]) + "/" + str(item_product[db.clsb_download_archieve.download_time.year()])
                rows['province'] = prov['province_name']
                price = int(item_province[sum])
                rows['total_price'] = price
                rows['total_discount'] = price*discount_value/100
                rows['total_payment'] = price - price*discount_value/100
                listProvince.append(rows)
                prov_dict[rows['download_time'] + "-" + str(id)] = rows['total_payment']

            time_data = []
            for test_item in count_by_time:
                time_data.append(str(test_item[db.clsb_download_archieve.download_time.day()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve.download_time.month()])
                                + "/"
                                + str(test_item[db.clsb_download_archieve.download_time.year()]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    max_day = calendar.monthrange(y, m)[1]
                    for d in range(1, max_day + 1):
                        time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                        if time < end and time >= start:
                            str_time = str(d) + "/" + str(m) + "/" + str(y)
                            temp = list()
                            temp.append(str_time)
                            temp_prov = list()
                            temp_prov.append(str_time)
                            if str_time in time_data:
                                index = time_data.index(str_time)
                                total_data=[]
                                total_data.append(str_time)
                                total_data.append(int(count_by_time[index][sum]))
                                total_price += int(count_by_time[index][sum])
                                price = int(count_by_time[index][sum])
                                total_payment += price*85/100 - (price*85/100)*discount_value/100
                                total_discount += (price*85/100)*discount_value/100
                                total_phi += price*15/100
                                dataAll.append(total_data)
                            else:
                                total_data=[]
                                total_data.append(str_time)
                                total_data.append(0)
                                dataAll.append(total_data)
                            for product_id in list_product:
                                if product_dict.has_key(str_time + "-" + str(product_id)):
                                    temp.append(product_dict.get(str_time + "-" + str(product_id)))
                                else:
                                    temp.append(0)
                            data.append(temp)
                            for prov_id in list_province:
                                if prov_dict.has_key(str_time + "-" + str(prov_id)):
                                    temp_prov.append(prov_dict.get(str_time + "-" + str(prov_id)))
                                else:
                                    temp_prov.append(0)
                            dataProvince.append(temp_prov)
        except Exception as err:
            print(err)

    province = db(db.clsb_province).select()
    return dict(
        tableList=tableList, totalData=totalData, data=data, dataAll=dataAll, products=products, productsList=productsList,
        total_price=total_price,
        total_payment=total_payment,
        total_discount=total_discount,
        total_phi=total_phi,
        province=province,
        listProvince=listProvince,
        dataProvince=dataProvince,
        province_select=province_select
    )