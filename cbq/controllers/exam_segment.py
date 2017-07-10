__author__ = 'User'

from applications.cbq.modules.dao import exam_dao
from applications.cbq.modules.dao import exam_segment_dao
from applications.cbq.modules.entities.question_entities.exam_segment import ExamSegment

tag = 'exam_segment'


def insert():

    if len(request.vars) < 1:
        return dict(CB_0002)
    exam_id = request.vars['exam_id']
    result = None
    print request.vars
    try:
        if len(request.vars) > 1:
            segment_name = request.vars['segment_name']
            segment_des = request.vars['segment_des']
            segment_duration = request.vars['segment_duration']

            exam_segment = ExamSegment()
            exam_segment.exam_id = exam_id
            exam_segment.segment_name = segment_name
            exam_segment.des = segment_des
            exam_segment.duration = segment_duration

            result = exam_segment_dao.insert(exam_segment, db)
            return dict(result=result)
        exam = exam_dao.get_exam_by_id(exam_id, db)
    except Exception as e:
        print tag + ' insert ' + str(e)
        result = -1

    return dict(exam=exam, result=result)

#def insert_exam_segment():
#

