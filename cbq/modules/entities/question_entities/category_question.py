__author__ = 'User'


class CategoryQuestion(object):

    item_id_field = "id"
    category_id_field = "category_id"
    question_id_field = "question_id"

    def __init__(self):
        self.item_id = None
        self.category_id = None
        self.question_id = None

    def print_info(self):
        info = " Category question info : "
        info += " id : " + str(self.item_id)
        info += ", category_id : " + str(self.category_id)
        info += ", question_id : " + str(self.question_id)

        print info
