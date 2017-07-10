__author__ = 'PhuongNH'
"""
    use to store content attribute in answer json
    ex : {"type":"text", "id":"text_635117337234193115", "size":52 ,
   =>>>> "content":[ {"value":"some", "mark":1, "isTrue":true }] <<<==}
"""


class ContentAttr(object):
    item_value_field = "value"
    item_mark_field = "mark"
    item_is_true_field = "isTrue"

    def __init__(self):
        self.value = None
        self.mark = None
        self.is_correct = None

    def print_info(self):
        info = "Content attribute : "
        info += ", value: " + str(self.value)
        info += ", mark: " + str(self.mark)
        info += ", is_ correct: " + str(self.is_correct)

        print info