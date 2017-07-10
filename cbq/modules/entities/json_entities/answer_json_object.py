__author__ = 'User'


class AnswerJsonObject(object):

    prefix_json = "={"
    suffix_json = "}="

    answer_tf_type = "TRUEFALSE"
    answer_textbox_type = "FILLIN"
    # MC_1 : mutilchoice import form Moodle
    answer_radio_type= "MC"
    #MC : multichoice import from excel
    answer_cb_type = "MC_1"
    answer_checkbox_type = "PC"
    answer_matching_type = "MATCHING"
    answer_sequences_type = "SEQUENCES"

    item_type_field = "type"
    item_id_field = "id"
    size_field = "size"
    content_field = "content"

    def __init__(self):

        self.type = None
        self.item_id = None
        self.size = None
        self.content = None

    def print_info(self):
        info = " Text box json object: "
        info += " type: " + str(self.type)
        info += " item_id: " + str(self.item_id)
        info += "size: " + str(self.size)
        info += "content: " + str(self.content)

        print info


