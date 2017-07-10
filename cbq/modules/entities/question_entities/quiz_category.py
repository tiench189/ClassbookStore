__author__ = 'User'


class QuizCategory(object):
    item_id_field = "id"
    category_code_field = "category_code"
    category_name_field = "category_name"
    description_field = "description"
    parent_id_field = "parent_id"
    parent_map_file = "parent_map"
    category_level_field = "category_level"

    def __init__(self):
        self.item_id = None
        self.category_code = None
        self.category_name = None
        self.description = None
        self.parent_id = None
        self.parent_map = None
        self.category_level = None

    def print_info(self):
        info = " Quiz category item : "
        info += " id : " + str(self.item_id)
        info += " category_code : " + str(self.category_code)
        info += " category_name : " + str(self.category_name)
        info += " description : " + str(self.description)
        info += " parent_id : " + str(self.parent_id)
        info += " category_level: " + str(self.category_level)
        print info
