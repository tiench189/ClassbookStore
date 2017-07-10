__author__ = 'User'


class ExamPage(object):
    item_id_field = "id"
    exam_id_field = "exam_id"
    page_index_field = "page_index"

    def __init__(self):
        self.item_id = None
        self.exam_id = None
        self.page_index = None