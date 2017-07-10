__author__ = 'User'
import ast


class QuestionContent(object):

    item_id_field = "id"
    content_id_field = "content_id"
    question_content_field = "question_content"
    description_field = "description"
    question_type_field = "question_type"

    def __init__(self):
        self.item_id = None
        self.content_id = None
        self.question_content = None
        self.description = None
        self.question_type = None

    def print_info(self):
        info = 'id : ' + str(self.item_id)
        info += 'content_id: ' + str(self.content_id)
        info += 'question_content: ' + str(self.question_content)
        info += 'description: ' + str(self.description)
        info += 'question_type: ' + str(self.question_type)

        print info