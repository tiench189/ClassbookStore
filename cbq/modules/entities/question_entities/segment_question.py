__author__ = 'User'


class SegmentQuestion(object):
    item_id_field = "id"
    segment_id_field = "segment_id"
    question_id_field = "question_id"
    question_order_field = "segment_question_order"


    def __init__(self):
        self.item_id = None
        self.segment_id = None
        self.question_id = None
        self.question_order = None

    #def print_info(selfs):
