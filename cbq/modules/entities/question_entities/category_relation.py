__author__ = 'User'


class CategoryRelation(object):

    def __init__(self):
        self.item_id = None
        self.category_first = None
        self.category_second = None
        self.parent_id = None

    def print_info(self):
        info = 'category relation : '
        info += 'id : ' + str(self.item_id)
        info += ', category first : ' + str(self.category_first)
        info += ', category second : ' + str(self.category_second)
        info += ', parent_id : ' + str(self.parent_id)

        print info