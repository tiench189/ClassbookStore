# -*- coding: utf-8 -*-
__author__ = 'Tien'
import calendar
from datetime import datetime
import sys

@auth.requires_authorize()
def report():
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
        total_type['tqg_card1face'] = 0
        total_type['tqg_card1real'] = 0
        total_type['tqg_card2face'] = 0
        total_type['tqg_card2real'] = 0
        total_type["tranferreal"] = 0
        total_type["tranferface"] = 0
        data = list()
        list_total = list()
        total_face = 0
        total_real = 0
        if by_year:
            time_type = 'by_year'
            sum_face = "SUM(clsb_transaction.face_value)"
            sum_real = "SUM(clsb_transaction.real_value)"
            sum_by_time = db(db.clsb_transaction.created_on > start)\
                    (db.clsb_transaction.site == "TQG")\
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
                #the tqg
                sum_card = db.clsb30_tqg_card_log.card_value.sum()
                card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                            (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                            (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                            (db.clsb30_tqg_card.card_gift == 0).select(sum_card).first()[sum_card]
                if card_value is None:
                    card_value = 0
                rows["tqg_card1real"] = card_value
                rows["tqg_card1face"] = card_value
                temp_face += card_value
                temp_real += card_value
                total_face += card_value
                total_real += card_value
                total_type["tqg_card1real"] += card_value
                total_type["tqg_card1face"] += card_value
                #the tqg
                sum_card = db.clsb30_tqg_card_log.card_value.sum()
                card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                            (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                            (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                            (db.clsb30_tqg_card.card_gift == 1).select(sum_card).first()[sum_card]
                if card_value is None:
                    card_value = 0
                rows["tqg_card2real"] = card_value
                rows["tqg_card2face"] = card_value
                temp_face += card_value
                temp_real += card_value
                total_face += card_value
                total_real += card_value
                total_type["tqg_card2real"] += card_value
                total_type["tqg_card2face"] += card_value
                #tranfer
                sum_tranfer = db.clsb30_tqg_log_tranfer.fund.sum()
                tranfer_value = db(db.clsb30_tqg_log_tranfer.created_on >= time)\
                                    (db.clsb30_tqg_log_tranfer.created_on <= tmp_end)\
                                    (db.clsb30_tqg_log_tranfer.status.like("SUCCESS"))\
                                    (~db.clsb30_tqg_log_tranfer.description.like("nap_tien"))\
                                    (db.clsb30_tqg_log_tranfer.user_id == db.clsb_user.id)\
                                    (db.clsb_user.test_user != 1).select(sum_tranfer).first()[sum_tranfer]
                if tranfer_value is None:
                    tranfer_value = 0
                rows["tranferreal"] = tranfer_value
                rows["tranferface"] = tranfer_value
                temp_face += tranfer_value
                temp_real += tranfer_value
                total_face += tranfer_value
                total_real += tranfer_value
                total_type["tranferreal"] += tranfer_value
                total_type["tranferface"] += tranfer_value
                #
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
                    (db.clsb_transaction.site == "TQG")\
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
                        #the tqg
                        sum_card = db.clsb30_tqg_card_log.card_value.sum()
                        card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                    (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                    (db.clsb30_tqg_card.card_gift == 0).select(sum_card).first()[sum_card]
                        if card_value is None:
                            card_value = 0
                        rows["tqg_card1real"] = card_value
                        rows["tqg_card1face"] = card_value
                        temp_face += card_value
                        temp_real += card_value
                        total_face += card_value
                        total_real += card_value
                        total_type["tqg_card1real"] += card_value
                        total_type["tqg_card1face"] += card_value
                        #the tqg
                        sum_card = db.clsb30_tqg_card_log.card_value.sum()
                        card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                    (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                    (db.clsb30_tqg_card.card_gift == 1).select(sum_card).first()[sum_card]
                        if card_value is None:
                            card_value = 0
                        rows["tqg_card2real"] = card_value
                        rows["tqg_card2face"] = card_value
                        temp_face += card_value
                        temp_real += card_value
                        total_face += card_value
                        total_real += card_value
                        total_type["tqg_card2real"] += card_value
                        total_type["tqg_card2face"] += card_value
                        #tranfer
                        sum_tranfer = db.clsb30_tqg_log_tranfer.fund.sum()
                        tranfer_value = db(db.clsb30_tqg_log_tranfer.created_on >= time)\
                                    (db.clsb30_tqg_log_tranfer.created_on <= tmp_end)\
                                    (db.clsb30_tqg_log_tranfer.status.like("SUCCESS"))\
                                    (~db.clsb30_tqg_log_tranfer.description.like("nap_tien"))\
                                    (db.clsb30_tqg_log_tranfer.user_id == db.clsb_user.id)\
                                    (db.clsb_user.test_user != 1).select(sum_tranfer).first()[sum_tranfer]
                        if tranfer_value is None:
                            tranfer_value = 0
                        rows["tranferreal"] = tranfer_value
                        rows["tranferface"] = tranfer_value
                        temp_face += tranfer_value
                        temp_real += tranfer_value
                        total_face += tranfer_value
                        total_real += tranfer_value
                        total_type["tranferreal"] += tranfer_value
                        total_type["tranferface"] += tranfer_value
                        #
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
                    (db.clsb_transaction.site == "TQG")\
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
                            #the tqg
                            sum_card = db.clsb30_tqg_card_log.card_value.sum()
                            card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                        (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                        (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                        (db.clsb30_tqg_card.card_gift == 0).select(sum_card).first()[sum_card]
                            if card_value is None:
                                card_value = 0
                            rows["tqg_card1real"] = card_value
                            rows["tqg_card1face"] = card_value
                            temp_face += card_value
                            temp_real += card_value
                            total_face += card_value
                            total_real += card_value
                            total_type["tqg_card1real"] += card_value
                            total_type["tqg_card1face"] += card_value
                            #the tqg
                            sum_card = db.clsb30_tqg_card_log.card_value.sum()
                            card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                        (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                        (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                        (db.clsb30_tqg_card.card_gift == 1).select(sum_card).first()[sum_card]
                            if card_value is None:
                                card_value = 0
                            rows["tqg_card2real"] = card_value
                            rows["tqg_card2face"] = card_value
                            temp_face += card_value
                            temp_real += card_value
                            total_face += card_value
                            total_real += card_value
                            total_type["tqg_card2real"] += card_value
                            total_type["tqg_card2face"] += card_value
                            #tranfer
                            sum_tranfer = db.clsb30_tqg_log_tranfer.fund.sum()
                            tranfer_value = db(db.clsb30_tqg_log_tranfer.created_on >= time)\
                                    (db.clsb30_tqg_log_tranfer.created_on <= tmp_end)\
                                    (db.clsb30_tqg_log_tranfer.status.like("SUCCESS"))\
                                    (~db.clsb30_tqg_log_tranfer.description.like("nap_tien"))\
                                    (db.clsb30_tqg_log_tranfer.user_id == db.clsb_user.id)\
                                    (db.clsb_user.test_user != 1).select(sum_tranfer).first()[sum_tranfer]
                            if tranfer_value is None:
                                tranfer_value = 0
                            rows["tranferreal"] = tranfer_value
                            rows["tranferface"] = tranfer_value
                            temp_face += tranfer_value
                            temp_real += tranfer_value
                            total_face += tranfer_value
                            total_real += tranfer_value
                            total_type["tranferreal"] += tranfer_value
                            total_type["tranferface"] += tranfer_value
                            #
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
                    (db.clsb_transaction.site == "TQG")\
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
                    (db.clsb_transaction.site == "TQG")\
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
                    (db.clsb_transaction.site == "TQG")\
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


def card_report():
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
        list_type = ["0", "1"]
        total_type = dict()
        for type in list_type:
            total_type[type] = 0
        data = list()
        list_total = list()
        total_value = 0
        if by_year:
            time_type = 'by_year'
            sum_value = "SUM(clsb30_tqg_card_log.card_value)"
            sum_by_time = db(db.clsb30_tqg_card_log.created_on > start)\
                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                    (db.clsb30_tqg_card_log.created_on <= end).select(sum_value,
                                                   db.clsb30_tqg_card_log.created_on.year(),
                                                   db.clsb30_tqg_card.card_gift,
                                                   groupby=(db.clsb30_tqg_card_log.created_on.year(),
                                                   db.clsb30_tqg_card.card_gift))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb30_tqg_card_log.created_on.year()]) + "-" +
                                        str(index_time[db.clsb30_tqg_card.card_gift]))
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                tempTotal = list()
                tempTotal.append(str_time)
                temp.append(str_time)
                rows = dict()
                temp_value = 0
                rows['time'] = str_time
                for type in list_type:
                    time_type = str_time + "-" + type
                    if time_type in time_data:
                        index = time_data.index(time_type)
                        value = sum_by_time[index][sum_value]
                        total_value += value
                        temp_value += value
                        rows[type] = value
                        total_type[type] = total_type[type] + value
                    else:
                        rows[type] = 0
                rows['value'] = temp_value
                list_total.append(rows)
                temp.append(temp_value)
                data.append(temp)
        if by_month:
            time_type = 'by_month'
            sum_value = "SUM(clsb30_tqg_card_log.card_value)"
            sum_by_time = db(db.clsb30_tqg_card_log.created_on > start)\
                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                    (db.clsb30_tqg_card_log.created_on <= end).select(sum_value,
                                                   db.clsb30_tqg_card_log.created_on.month(),
                                                   db.clsb30_tqg_card_log.created_on.year(),
                                                   db.clsb30_tqg_card.card_gift,
                                                   groupby=(db.clsb30_tqg_card_log.created_on.month(),
                                                            db.clsb30_tqg_card_log.created_on.year(),
                                                            db.clsb30_tqg_card.card_gift))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb30_tqg_card_log.created_on.month()])
                                      + "-"
                                        + str(index_time[db.clsb30_tqg_card_log.created_on.year()]) + "-" +
                                        str(index_time[db.clsb30_tqg_card.card_gift]))
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
                        temp = list()
                        tempTotal = list()
                        tempTotal.append(str_time)
                        temp.append(str_time)
                        rows = dict()
                        temp_value = 0
                        rows['time'] = str_time
                        for type in list_type:
                            time_type = str_time + "-" + type
                            if time_type in time_data:
                                index = time_data.index(time_type)
                                value = sum_by_time[index][sum_value]
                                total_value += value
                                temp_value += value
                                rows[type] = value
                                total_type[type] = total_type[type] + value
                            else:
                                rows[type] = 0
                        rows['value'] = temp_value
                        list_total.append(rows)
                        temp.append(temp_value)
                        data.append(temp)
        if by_day:
            time_type = 'by_day'
            sum_value = "SUM(clsb30_tqg_card_log.card_value)"
            sum_by_time = db(db.clsb30_tqg_card_log.created_on > start)\
                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                    (db.clsb30_tqg_card_log.created_on <= end).select(sum_value,
                                                    db.clsb30_tqg_card_log.created_on.day(),
                                                    db.clsb30_tqg_card_log.created_on.month(),
                                                    db.clsb30_tqg_card_log.created_on.year(),
                                                    db.clsb30_tqg_card.card_gift,
                                                    groupby=(db.clsb30_tqg_card_log.created_on.day(),
                                                            db.clsb30_tqg_card_log.created_on.month(),
                                                            db.clsb30_tqg_card_log.created_on.year(),
                                                            db.clsb30_tqg_card.card_gift))
            time_data = list()
            for index_time in sum_by_time:
                time_data.append(str(index_time[db.clsb30_tqg_card_log.created_on.day()])
                                    + "-" + str(index_time[db.clsb30_tqg_card_log.created_on.month()])
                                      + "-"
                                        + str(index_time[db.clsb30_tqg_card_log.created_on.year()])+ "-" +
                                        str(index_time[db.clsb30_tqg_card.card_gift]))
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    max_day = calendar.monthrange(y, m)[1]
                    for d in range(1, max_day + 1):
                        time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                        tmp_end = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d) + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                        if time <= end and time >= start:
                            str_time = str(d) + "-" +str(m) + "-" + str(y)
                            temp = list()
                            tempTotal = list()
                            tempTotal.append(str_time)
                            temp.append(str_time)
                            rows = dict()
                            temp_value = 0
                            rows['time'] = str_time
                            for type in list_type:
                                time_type = str_time + "-" + type
                                if time_type in time_data:
                                    index = time_data.index(time_type)
                                    value = sum_by_time[index][sum_value]
                                    total_value += value
                                    temp_value += value
                                    rows[type] = value
                                    total_type[type] = total_type[type] + value
                                else:
                                    rows[type] = 0
                            rows['value'] = temp_value
                            list_total.append(rows)
                            temp.append(temp_value)
                            data.append(temp)
        return dict(data=data, total_value=total_value, listTotal=list_total,
                    time=time_type, total_type=total_type, list_type=list_type)
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


# @auth.requires_authorize()
def card_log():
    form = SQLFORM.smartgrid(db.clsb30_tqg_card_log, args=request.args[:1],
                             showbuttontext=False)
    return dict(grid=form)


# @auth.requires_authorize()
def tranfer_log():
    form = SQLFORM.smartgrid(db.clsb30_tqg_log_tranfer, args=request.args[:1],
                             showbuttontext=False)
    return dict(grid=form)


@auth.requires_login()
def card_manager():
    form = SQLFORM.smartgrid(db.clsb30_tqg_card, args=request.args[:1],
                             showbuttontext=False,
                             deletable=False)
    return dict(grid=form)


@auth.requires_login()
def exam_manager():
    form = SQLFORM.smartgrid(db.clsb30_ki_thi_thu, args=request.args[:1],
                             showbuttontext=False)
    return dict(grid=form)


@auth.requires_authorize()
def card_active():
    try:
        if request.vars:
            type = request.vars.type
            serial_activate = int(request.vars.action)
            time_valid = request.vars.time_valid.strip()
            if time_valid != "":
                time_valid = datetime.strptime(time_valid + " 23:59:59", "%Y-%m-%d %H:%M:%S")
            else:
                time_valid = None
            gift = 0
            if "gift" in request.vars:
                gift = 1
            if type == "single":
                serial = request.vars.serial
                serial = serial.strip()
                query = db(db.clsb30_tqg_card.card_serial == serial)
                select_card = query.select()
                if len(select_card) == 0:
                    return dict(result=False, mess="Mã thẻ không tồn tại: " + serial)
                query.update(serial_activate=serial_activate, time_valid=time_valid,
                             actived_by=auth.user.id, actived_on=datetime.now(),
                             card_gift=gift)
                return dict(result=True, mess="SUCCESS")
            else:
                serial_start = request.vars.serial_start.strip()
                serial_end = request.vars.serial_end.strip()
                select_start = db(db.clsb30_tqg_card.card_serial == serial_start).select()
                if len(select_start) == 0:
                    return dict(result=False, mess="Mã thẻ không tồn tại: " + serial_start)
                select_end = db(db.clsb30_tqg_card.card_serial == serial_end).select()
                if len(select_end) == 0:
                    return dict(result=False, mess="Mã thẻ không tồn tại: " + serial_end)
                db(db.clsb30_tqg_card.card_serial >= serial_start)\
                    (db.clsb30_tqg_card.card_serial <= serial_end).update(serial_activate=serial_activate,
                                                                          time_valid=time_valid,
                                                                          actived_by=auth.user.id,
                                                                          actived_on=datetime.now(),
                                                                          card_gift=gift)
                return dict(result=True, mess="SUCCESS")
        return dict(result=True, mess="")
    except Exception as err:
        return dict(result=False, mess=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


@auth.requires_login()
def third_card_manager():
    form = SQLFORM.smartgrid(db.clsb30_tqg_card, args=request.args[:1],
                             showbuttontext=False,
                             deletable=False,
                             editable=False,
                             create=False)
    return dict(grid=form)


@auth.requires_authorize()
def third_card_active():
    try:
        if request.vars:
            type = request.vars.type
            if type == "single":
                serial = request.vars.serial
                serial = serial.strip()
                query = db(db.clsb30_tqg_card.card_serial == serial)
                select_card = query.select()
                if len(select_card) == 0:
                    return dict(result=False, mess="Mã thẻ không tồn tại: " + serial)
                query.update(serial_activate=1, actived_by=auth.user.id, actived_on=datetime.now())
                return dict(result=True, mess="SUCCESS")
            else:
                serial_start = request.vars.serial_start.strip()
                serial_end = request.vars.serial_end.strip()
                select_start = db(db.clsb30_tqg_card.card_serial == serial_start).select()
                if len(select_start) == 0:
                    return dict(result=False, mess="Mã thẻ không tồn tại: " + serial_start)
                select_end = db(db.clsb30_tqg_card.card_serial == serial_end).select()
                if len(select_end) == 0:
                    return dict(result=False, mess="Mã thẻ không tồn tại: " + serial_end)
                db(db.clsb30_tqg_card.card_serial >= serial_start)\
                    (db.clsb30_tqg_card.card_serial <= serial_end).update(serial_activate=1,
                                                                          actived_by=auth.user.id,
                                                                          actived_on=datetime.now())
                return dict(result=True, mess="SUCCESS")
        return dict(result=True, mess="")
    except Exception as err:
        return dict(result=False, mess=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def report_card():
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
        total_pay = 0
        if by_year:
            time_type = 'by_year'
            for y in range(start.year, maxYear+1):
                str_time = str(y)
                temp = list()
                temp.append(str_time)
                rows = dict()
                rows['time'] = str_time
                #the tqg
                sum_card = db.clsb30_tqg_card_log.card_value.sum()
                card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                    (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                    (db.clsb30_tqg_card.card_gift == 0).select(sum_card).first()[sum_card]
                if card_value is None:
                    card_value = 0
                total_pay += card_value
                rows['pay1'] = card_value
                #the tqg
                sum_card = db.clsb30_tqg_card_log.card_value.sum()
                card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                    (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                    (db.clsb30_tqg_card.card_gift == 1).select(sum_card).first()[sum_card]
                if card_value is None:
                    card_value = 0
                total_pay += card_value
                rows['pay2'] = card_value
                #
                list_total.append(rows)
                temp.append(rows['pay1'] + rows['pay2'])
                data.append(temp)
        if by_month:
            time_type = 'by_month'
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    time = datetime.strptime(str(y)+"-"+str(m), "%Y-%m")
                    if m < 12:
                        tmp_end = datetime.strptime(str(y)+"-"+str(m + 1), "%Y-%m")
                    else:
                        tmp_end = datetime.strptime(str(y + 1)+"-1", "%Y-%m")
                    if time <= end and time >= start:
                        str_time = str(m) + "-" + str(y)
                        temp = list()
                        temp.append(str_time)
                        rows = dict()
                        rows['time'] = str_time
                        #the tqg
                        sum_card = db.clsb30_tqg_card_log.card_value.sum()
                        card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                    (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                    (db.clsb30_tqg_card.card_gift == 0).select(sum_card).first()[sum_card]
                        if card_value is None:
                            card_value = 0
                        total_pay += card_value
                        rows['pay1'] = card_value
                        #the tqg
                        sum_card = db.clsb30_tqg_card_log.card_value.sum()
                        card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                    (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                    (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                    (db.clsb30_tqg_card.card_gift == 1).select(sum_card).first()[sum_card]
                        if card_value is None:
                            card_value = 0
                        total_pay += card_value
                        rows['pay2'] = card_value
                        #
                        list_total.append(rows)
                        temp.append(rows['pay1'] + rows['pay2'])
                        data.append(temp)
        if by_day:
            time_type = 'by_month'
            for y in range(start.year, maxYear+1):
                for m in range(1,13):
                    max_day = calendar.monthrange(y, m)[1]
                    for d in range(1, max_day + 1):
                        time = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d), "%Y-%m-%d")
                        tmp_end = datetime.strptime(str(y)+"-"+str(m)+"-"+str(d) + " 23:59:59", "%Y-%m-%d %H:%M:%S")
                        if time <= end and time >= start:
                            str_time = str(d) + "-" +str(m) + "-" + str(y)
                            temp = list()
                            temp.append(str_time)
                            rows = dict()
                            rows['time'] = str_time
                            #the tqg
                            sum_card = db.clsb30_tqg_card_log.card_value.sum()
                            card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                        (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                        (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                        (db.clsb30_tqg_card.card_gift == 0).select(sum_card).first()[sum_card]
                            if card_value is None:
                                card_value = 0
                            total_pay += card_value
                            rows['pay1'] = card_value
                            #the tqg
                            sum_card = db.clsb30_tqg_card_log.card_value.sum()
                            card_value = db(db.clsb30_tqg_card_log.created_on >= time)\
                                        (db.clsb30_tqg_card_log.created_on <= tmp_end)\
                                        (db.clsb30_tqg_card_log.card_serial == db.clsb30_tqg_card.card_serial)\
                                        (db.clsb30_tqg_card.card_gift == 1).select(sum_card).first()[sum_card]
                            if card_value is None:
                                card_value = 0
                            total_pay += card_value
                            rows['pay2'] = card_value
                            #
                            list_total.append(rows)
                            temp.append(rows['pay1'] + rows['pay2'])
                            data.append(temp)
        return dict(data=data, total_pay=total_pay, listTotal=list_total,
                    time=time_type)
    except Exception as err:
        return dict(error=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


@auth.requires_login()
def tvt_log():
    form = SQLFORM.smartgrid(db.clsb30_tvt_log, args=request.args[:1],
                             showbuttontext=False,
                             deletable=False,
                             editable=False,
                             create=False)
    return dict(grid=form)