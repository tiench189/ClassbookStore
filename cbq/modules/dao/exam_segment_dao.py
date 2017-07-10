__author__ = 'User'
from applications.cbq.modules.entities.question_entities.exam_segment import ExamSegment
from applications.cbq.modules import cbMsb

tag = "exam_segment_dao"


def insert(exam_segment, db):
    """
    @todo insert data into table clsb_exam_segment
    @param exam_segment:
    @param db:
    @return: -1 if fail else return id of record has just inserted
    """
    result = -1
    if exam_segment is None:
        return result
    try:
        result = db.clsb_exam_segment.insert(segment_id=exam_segment.segment_id, exam_id=exam_segment.exam_id,
                                             segment_name=exam_segment.segment_name, des=exam_segment.des,
                                             duration=exam_segment.duration, segment_mark=exam_segment.segment_mark,
                                             exam_segment_order=exam_segment.exam_segment_order)
    except Exception as e:
        print tag + " insert " + str(e)
        result = -1

    return result


def get_exam_segment_by_id(item_id, db):
    try:
        rows = db(db.clsb_exam_segment.id == item_id).select()
        row = rows.first()
        exam_segment = ExamSegment()
        exam_segment.item_id = row[ExamSegment.item_id_field]
        exam_segment.exam_id = row[ExamSegment.exam_id_field]
        exam_segment.segment_id = row[ExamSegment.segment_id_field]
        exam_segment.segment_name = row[ExamSegment.segment_name_field]
        exam_segment.segment_mark = row[ExamSegment.segment_mark_field]
        exam_segment.des = row[ExamSegment.description_field]
        exam_segment.duration = row[ExamSegment.duration_field]
        exam_segment.exam_segment_order = row[ExamSegment.exam_segment_order_field]

    except Exception as e:
        print tag + " get_exam_segment_by_id " + str(e)
    return exam_segment


def get_list_exam_segment_by_exam_id(exam_id, db):
    list_exam_segment = list()
    try:

        rows = db(db.clsb_exam_segment.exam_id == exam_id).select()
        for row in rows:

            exam_segment = ExamSegment()
            exam_segment.item_id = row[ExamSegment.item_id_field]

            exam_segment.exam_id = row[ExamSegment.exam_id_field]
            exam_segment.segment_id = row[ExamSegment.segment_id_field]
            exam_segment.segment_name = row[ExamSegment.segment_name_field]
            exam_segment.segment_mark = row[ExamSegment.segment_mark_field]
            exam_segment.des = row[ExamSegment.description_field]
            exam_segment.duration = row[ExamSegment.duration_field]
            exam_segment.exam_segment_order = row[ExamSegment.exam_segment_order_field]
            list_exam_segment.append(exam_segment)
    except Exception as e:
        print tag + " get_list_exam_segment_by_exam_id " + str(e)
    return list_exam_segment