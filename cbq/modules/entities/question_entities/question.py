__author__ = 'User'
import ast


class Question(object):

    item_id_field = "id"
    content_id_field = "content_id"
    mark_field = "mark"
    type_field = "question_type"
    difficult_level_field = "difficult_level"
    question_guide_field = "question_guide"
    description_field = "description"
    question_title_field = "question_title"
    explanation_field = "explanation"
    page_index_field = "page_index"
    status_field = "status"

    def __init__(self):
        self.item_id = None
        self.content_id = None
        self.mark = None
        self.question_type = None
        self.difficult_level = None
        self.question_guide = None
        self.description = None
        self.question_title = None
        self.page_index = None
        self.explanation = None
        self.status = None

    def print_info(self):
        info = 'id: ' + str(self.item_id)
        info += ', content_id: ' + str(self.content_id)
        info += ', mark: ' + str(self.mark)
        info += ', question_type: ' + str(self.question_type)
        info += ', difficult_level: ' + str(self.difficult_level)
        info += ', question_guide: ' + str(self.question_guide)
        info += ', description: ' + str(self.description)
        info += ', question_title: ' + str(self.question_title)
        info += ', page_index: ' + str(self.page_index)
        info += ', explanation: ' + str(self.explanation)
        info += ', status: ' + str(self.status)
        print info
