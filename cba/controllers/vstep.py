import sys
from datetime import datetime, timedelta
from dateutil import relativedelta
import calendar
import time


SITE_CODE = "ulis"


@auth.requires_authorize()
def recharge():
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

        end = datetime.now()
        start = end - relativedelta.relativedelta(months=6)
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
                    (db.clsb_transaction.site == SITE_CODE)\
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
                time = datetime.strptime(str(y), "%Y")
                tmp_end = datetime.strptime(str(y + 1), "%Y")
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
                    (db.clsb_transaction.site == SITE_CODE)\
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
                    if m < 12:
                        tmp_end = datetime.strptime(str(y)+"-"+str(m + 1), "%Y-%m")
                    else:
                        tmp_end = datetime.strptime(str(y + 1)+"-1", "%Y-%m")
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
                    (db.clsb_transaction.site == SITE_CODE)\
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
                        tmp_end = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d) + " 23:59:59", "%Y-%m-%d %H:%M:%S")
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
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


@auth.requires_authorize()
def paid():
    try:
        by_year = False
        by_day = False
        by_month = False
        tdelta = relativedelta.relativedelta(months=1)
        date_format = "%m-%Y"
        if request.vars.getbyyear:
            if request.vars.getbyyear == "1":
                tdelta = relativedelta.relativedelta(years=1)
                date_format = "%Y"
                by_year = True
            elif request.vars.getbyyear == "2":
                tdelta = relativedelta.relativedelta(months=1)
                date_format = "%m-%Y"
                by_month = True
            elif request.vars.getbyyear == "3":
                date_format = "%d-%m-%Y"
                tdelta = relativedelta.relativedelta(days=1)
                by_day = True
            else:
                by_month = True
        else:
            by_month = True
        format = ""
        if "format" in request.vars:
            format = request.vars.format

        end = datetime.now()
        start = end - relativedelta.relativedelta(months=6)
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
        total_type = dict()
        list_type = ["READING", "LISTENING", "WRITING", "SPEAKING"]
        prices = dict()
        prices['READING'] = 25000
        prices['LISTENING'] = 25000
        prices['WRITING'] = 35000
        prices['SPEAKING'] = 35000
        prices['ALL'] = 100000
        data = list()
        list_total = list()
        data_total = dict()
        data_total['total'] = 0
        for tp in list_type:
            data_total[tp + "_count"] = 0
            data_total[tp + "_sum"] = 0

        current_time = start
        while current_time < end:
            next_time = current_time + tdelta
            stamp_start = int(time.mktime(current_time.timetuple()))
            stamp_end = int(time.mktime(next_time.timetuple()))
            count = "COUNT(*)"
            select_count = db(db.vstep_attempts.timestart >= stamp_start)\
                (db.vstep_attempts.timestart < stamp_end)\
                (db.vstep_attempts.vstep_format.like("%" + format + "%"))\
                (db.vstep_attempts.user_id == db.clsb_user.id)\
                (db.clsb_user.test_user == 0).select(count, db.vstep_attempts.subject,
                                                     groupby=db.vstep_attempts.subject)
            temp = list()
            row = dict()
            temp.append(current_time.strftime(date_format))
            row['time'] = current_time.strftime(date_format)
            sum_pay = 0
            for sc in select_count:
                for tp in list_type:
                    if str(sc[db.vstep_attempts.subject]) == tp:
                        current_count = int(sc[count])
                        sum = current_count * prices[tp]
                        sum_pay += sum
                        row[tp + "_count"] = current_count
                        row[tp + "_sum"] = sum
                        data_total[tp + "_sum"] += sum
                        data_total[tp + "_count"] += current_count
            row['sum'] = sum_pay
            data_total['total'] += sum_pay
            temp.append(sum_pay)
            data.append(temp)
            list_total.append(row)
            current_time = next_time
        return dict(data=data, list_total=list_total, list_type=list_type, prices=prices, data_total=data_total,
                    timestart=start.strftime(date_format), timeend=end.strftime(date_format))
    except Exception as err:
        return dict(error=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))