__author__ = 'User'


class ExamSegment(object):

    item_id_field = "id"
    segment_id_field = "segment_id"
    exam_id_field = "exam_id"
    segment_name_field = "segment_name"
    description_field = "des"
    duration_field = "duration"
    segment_mark_field = "segment_mark"
    exam_segment_order_field = "exam_segment_order"

    def __init__(self):
        self.item_id = None
        self.segment_id = None
        self.exam_id = None
        self.segment_name = None
        self.des = None
        self.duration = None
        self.segment_mark = None
        self.exam_segment_order = None

