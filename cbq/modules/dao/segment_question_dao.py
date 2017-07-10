__author__ = 'User'

from applications.cbq.modules.entities.question_entities.segment_question import SegmentQuestion
tag = 'segment_question_dao'


def insert(segment_question, db):
    """
    @todo : insert into table segment_question
    @param segment_question:
    @param db:
    @return: id of record
    """
    try:
        result = db.clsb_segment_question.insert(segment_id=segment_question.segment_id,
                                                 question_id=segment_question.question_id,
                                                 segment_question_order=segment_question.question_order)
    except Exception as e:
        print tag + ' insert ' + str(e)
        result = -1
    return result


def get_last_order_segment_question(segment_id, db):
    """
    @todo : get lastest order of segment
    @param segment_id:
    @return:
    """
    result = 0
    try:
        rows = db(db.clsb_segment_question.segment_id == segment_id).select()

        if rows:
            row = rows.last()
            segment_question_order = row[SegmentQuestion.question_order_field]
            result = segment_question_order

    except Exception as e:
        print tag + " get_last_order_segment_question " + str(e)
    return result


def get_list_by_segment_id(segment_id, db):
    segment_question_list = list()
    try:
        rows = db(db.clsb_segment_question.segment_id == segment_id).select()

        for row in rows:
            segment_question = SegmentQuestion()
            segment_question.item_id = row[SegmentQuestion.item_id_field]
            segment_question.segment_id = row[SegmentQuestion.segment_id_field]
            segment_question.question_id = row[SegmentQuestion.question_id_field]
            segment_question.question_order = row[SegmentQuestion.question_order_field]
            segment_question_list.append(segment_question)
    except Exception as e:
        print tag + "get_list_by_segment_id : " + str(e)
    return segment_question_list