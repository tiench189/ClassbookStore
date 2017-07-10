__author__ = 'User'


class QuestionAnswer(object):
    item_id_field = "id"
    question_id_field = "question_id"
    question_answer_field = "question_answer"
    mark_percent_field = "mark_percent"
    sign_mark_field = "sign_mark"
    is_correct_field = "is_correct"
    explanation_field = "explanation"

    def __init__(self):
        self.item_id = None
        self.question_id = None
        self.question_answer = None
        self.mark_percent = None
        self.sign_mark = None
        self.is_correct = None
        self.explanation = None

    def print_info(self):
        info = "Question answer : "
        info += 'id : ' + str(self.item_id)
        info += ', question_id: ' + str(self.question_id)
        info += ', question_answer: ' + str(self.question_answer)
        info += ', mark_percent: ' + str(self.mark_percent)
        info += ', sign_mark: ' + str(self.sign_mark)
        info += ', is_correct: ' + str(self.is_correct)
        info += ', explanation: ' + str(self.explanation)

        print info