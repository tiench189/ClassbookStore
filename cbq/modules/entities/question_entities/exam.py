__author__ = 'User'


class Exam(object):

    item_id_field = "id"
    exam_id_field = "exam_id"
    name_field = "name"
    type_field = "exam_type"
    description_field = "des"
    duration_field = "duration"
    number_question_field = "number_question"
    cover_field = "cover"
    total_mark_field = "total_mark"
    exam_mode_filed = "exam_mode"

    def __init__(self):
        self.item_id = None
        self.exam_id = None
        self.name = None
        self.exam_type = None
        self.des = None
        self.duration = None
        self.number_question = None
        self.cover = None
        self.total_mark = None
        self.exam_mode = None

    def print_info(self):
        info = "Exam item : "
        info += ", id : " + str(self.item_id)
        info += ", exam_id : " + str(self.exam_id)
        info += ", name : " + str(self.name)
        info += ", exam_type: " + str(self.exam_type)
        info += ", des: " + str(self.des)
        info += ", duration: " + str(self.duration)
        info += ", number_question: " + str(self.number_question)
        info += ", cover: " + str(self.cover)
        info += ", total_mark: " + str(self.total_mark)
        info += ", exam_mode : " + str(self.exam_mode)

        print info