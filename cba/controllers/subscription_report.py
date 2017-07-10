__author__ = 'Tien'

import scripts
import usercp
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import calendar
import sys

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
        data_sms = list()
        pay87 = 6400
        pay86 = 4050
        pay85 = 2000
        total_sms = 0;

        subscript_levels = db(db.cbless_subscription_level.id > 0).select()
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
                for level in subscript_levels:
                    count_subscript = db(db.cbless_purcharsing_log.subscription_level_id == level['id'])\
                            (db.cbless_purcharsing_log.user_id == db.clsb_user.id)\
                            (db.clsb_user.test_user == 0)\
                            (db.cbless_purcharsing_log.time_active > timeStart)\
                            (db.cbless_purcharsing_log.time_active < timeEnd)\
                            (db.cbless_purcharsing_log.package_id != 1).select(db.cbless_purcharsing_log.id)
                    temp.append(len(count_subscript))
                count_package_parent = db(db.cbless_purcharsing_log.time_active > timeStart)\
                            (db.cbless_purcharsing_log.time_active < timeEnd)\
                            (db.cbless_purcharsing_log.user_id == db.clsb_user.id)\
                            (db.clsb_user.test_user == 0)\
                            (db.cbless_purcharsing_log.package_id == 1).select(db.cbless_purcharsing_log.id)
                temp.append(len(count_package_parent))
                data.append(temp)

                temp_sms = list()
                temp_sms.append(str(y))
                count_87 = db(db.a0tech_sms_pay_code.service_number == "8775")\
                        (db.a0tech_sms_pay_code.created_on > timeStart)\
                        (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                temp_sms.append(len(count_87))
                count_86 = db(db.a0tech_sms_pay_code.service_number == "8675")\
                        (db.a0tech_sms_pay_code.created_on > timeStart)\
                        (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                temp_sms.append(len(count_86))
                count_85 = db(db.a0tech_sms_pay_code.service_number == "8575")\
                        (db.a0tech_sms_pay_code.created_on > timeStart)\
                        (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                temp_sms.append(len(count_85))
                pay = len(count_87)*pay87 + len(count_86)*pay86 + len(count_85)*pay85
                temp_sms.append(pay)
                total_sms += pay
                data_sms.append(temp_sms)


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
                    for level in subscript_levels:
                        count_subscript = db(db.cbless_purcharsing_log.subscription_level_id == level['id'])\
                                (db.cbless_purcharsing_log.user_id == db.clsb_user.id)\
                                (db.clsb_user.test_user == 0)\
                                (db.cbless_purcharsing_log.time_active > timeStart)\
                                (db.cbless_purcharsing_log.time_active < timeEnd)\
                                (db.cbless_purcharsing_log.package_id != 1).select(db.cbless_purcharsing_log.id)
                        temp.append(len(count_subscript))
                    count_package_parent = db(db.cbless_purcharsing_log.time_active > timeStart)\
                                (db.cbless_purcharsing_log.user_id == db.clsb_user.id)\
                                (db.clsb_user.test_user == 0)\
                                (db.cbless_purcharsing_log.time_active < timeEnd)\
                                (db.cbless_purcharsing_log.package_id == 1).select(db.cbless_purcharsing_log.id)
                    temp.append(len(count_package_parent))
                    data.append(temp)

                    temp_sms = list()
                    temp_sms.append(str(i)+"/"+str(y))
                    count_87 = db(db.a0tech_sms_pay_code.service_number == "8775")\
                            (db.a0tech_sms_pay_code.created_on > timeStart)\
                            (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                    temp_sms.append(len(count_87))
                    count_86 = db(db.a0tech_sms_pay_code.service_number == "8675")\
                            (db.a0tech_sms_pay_code.created_on > timeStart)\
                            (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                    temp_sms.append(len(count_86))
                    count_85 = db(db.a0tech_sms_pay_code.service_number == "8575")\
                            (db.a0tech_sms_pay_code.created_on > timeStart)\
                            (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                    temp_sms.append(len(count_85))
                    pay = len(count_87)*pay87 + len(count_86)*pay86 + len(count_85)*pay85
                    temp_sms.append(pay)
                    total_sms += pay
                    data_sms.append(temp_sms)
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
                        temp.append(str(d)+"/"+str(i))
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
                        for level in subscript_levels:
                            count_subscript = db(db.cbless_purcharsing_log.subscription_level_id == level['id'])\
                                    (db.cbless_purcharsing_log.user_id == db.clsb_user.id)\
                                    (db.clsb_user.test_user == 0)\
                                    (db.cbless_purcharsing_log.time_active > timeStart)\
                                    (db.cbless_purcharsing_log.time_active < timeEnd)\
                                    (db.cbless_purcharsing_log.package_id != 1).select(db.cbless_purcharsing_log.id)
                            temp.append(len(count_subscript))
                        count_package_parent = db(db.cbless_purcharsing_log.time_active > timeStart)\
                                    (db.cbless_purcharsing_log.time_active < timeEnd)\
                                    (db.cbless_purcharsing_log.user_id == db.clsb_user.id)\
                                    (db.clsb_user.test_user == 0)\
                                    (db.cbless_purcharsing_log.package_id == 1).select(db.cbless_purcharsing_log.id)
                        temp.append(len(count_package_parent))
                        data.append(temp)

                        temp_sms = list()
                        temp_sms.append(str(d)+"/"+str(i))
                        count_87 = db(db.a0tech_sms_pay_code.service_number == "8775")\
                                (db.a0tech_sms_pay_code.created_on > timeStart)\
                                (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                        temp_sms.append(len(count_87))
                        count_86 = db(db.a0tech_sms_pay_code.service_number == "8675")\
                                (db.a0tech_sms_pay_code.created_on > timeStart)\
                                (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                        temp_sms.append(len(count_86))
                        count_85 = db(db.a0tech_sms_pay_code.service_number == "8575")\
                                (db.a0tech_sms_pay_code.created_on > timeStart)\
                                (db.a0tech_sms_pay_code.created_on < timeEnd).select(db.a0tech_sms_pay_code.id)
                        temp_sms.append(len(count_85))
                        pay = len(count_87)*pay87 + len(count_86)*pay86 + len(count_85)*pay85
                        temp_sms.append(pay)
                        total_sms += pay
                        data_sms.append(temp_sms)
        print(data)
        package_subscriptions = list()
        packages = list()
        total_payment = 0
        select_package = db(db.cbless_package.parent_id == 1).select()
        for package in select_package:
            temp = dict()
            temp['id'] = package['id']
            temp['name'] = package['package_name']
            packages.append(temp)
        root_package = dict()
        root_package['id'] = 1
        root_package['name'] = "Toàn bộ"
        packages.append(root_package)
        for package in packages:
            temp = dict()
            temp['package'] = package['name']
            payment = 0
            for level in subscript_levels:
                count = list()
                package_price = db(db.cbless_package_price.package_id == package['id'])\
                        (db.cbless_package_price.level_id == level['id']).select()
                if len(package_price) == 0:
                    count.append(0)
                    count.append(0)
                else:
                    count.append(package_price.first()['price'])
                    count_by_level = db(db.cbless_purcharsing_log.package_id == package['id'])\
                            (db.cbless_purcharsing_log.subscription_level_id == level['id'])\
                            (db.cbless_purcharsing_log.user_id == db.clsb_user.id)\
                            (db.clsb_user.test_user == 0)\
                            (db.cbless_purcharsing_log.time_active > start)\
                            (db.cbless_purcharsing_log.time_active < end).select(db.cbless_purcharsing_log.id)
                    count.append(len(count_by_level))
                    payment += len(count_by_level) * int(package_price.first()['price'])
                temp["level" + str(level['id'])] = count
            temp['payment'] = payment
            total_payment += payment
            package_subscriptions.append(temp)
        return dict(data=data, data_sms=data_sms, packages=package_subscriptions, total_payment=total_payment,
                    total_sms=total_sms, start=str(start), end=str(end))
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))