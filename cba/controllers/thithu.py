# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys
from datetime import *


def get_exam():
    try:
        exam_index = request.vars.exam
        select_exam = db(db.clsb30_ki_thi_thu.exam_index == int(exam_index)).select()
        if len(select_exam) == 0:
            return dict(result=False, mess="Not found")
        exam = select_exam.first()
        data = dict()
        data['result'] = True
        data['exam_name'] = str(exam['exam_name'])
        data['exam_index'] = int(exam['exam_index'])
        data['start_date'] = exam['start_date'].strftime('%Y/%m/%d %H:%M:%S')
        data['end_date'] = exam['end_date'].strftime('%Y/%m/%d %H:%M:%S')
        data['exam_time'] = int(exam['exam_time'])
        return data
    except Exception as err:
        return dict(result=False, mess=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def get_active_axam():
    try:
        exams = list()
        select_exam = db(db.clsb30_ki_thi_thu.start_date <= datetime.now()).select()
        for ex in select_exam:
            temp = dict()
            temp['id'] = ex['id']
            temp['name'] = ex['exam_name']
            temp['index'] = ex['exam_index']
            exams.append(temp)
        return dict(exams=exams)
    except Exception as err:
        return dict(result=False, mess=err.message + " on line: " + str(sys.exc_traceback.tb_lineno))