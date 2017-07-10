__author__ = 'User'

from applications.cbq.modules.dao import question_answer_dao
from applications.cbq.modules.entities.question_entities.question_answer import QuestionAnswer

question_answer_request = (
    'item_id', 'question_id', 'question_id', 'question_answer', 'mark_percent', 'sign_mark', 'is_correct')


def index():
    form = SQLFORM.smartgrid(db.clsb_question)
    return dict(form=form)


def insert():
    """ return result
        param  question_id&question_answer&mark_percent&is_correct
        insert new question_answer into table clsb_question_answer
    """
    if len(request.vars) < 3:
        return dict(mess=CB_0002)
    question_answer_item = QuestionAnswer()
    for re in request.vars:
        if re == QuestionAnswer.question_id_field:
            question_answer_item.question_id = request.vars[QuestionAnswer.question_id_field]
        elif re == QuestionAnswer.question_answer_field:
            question_answer_item.question_answer = request.vars[QuestionAnswer.question_answer_field]
        elif re == QuestionAnswer.mark_percent_field:
            question_answer_item.mark_percent = request.vars[QuestionAnswer.mark_percent_field]
        elif re == QuestionAnswer.is_correct_field:
            question_answer_item.is_correct = request.vars[QuestionAnswer.is_correct_field]
        elif re == QuestionAnswer.sign_mark_field:
            question_answer_item.sign_mark = request.vars[QuestionAnswer.sign_mark_field]
    try:
        result = question_answer_dao.insert_data(question_answer_item, db)
    except Exception as e:
        print str(e)
        return dict(mess=CB_0003)
    return dict(result=result)


def get_question_answer_by_id():
    """ return record question answer
        get question answer by question answer id
        param : answer_id
    """
    if len(request.vars) < 1 or QuestionAnswer.item_id_field not in request.vars:
        return dict(mess=CB_0002)

    answer_id = request.vars[QuestionAnswer.item_id_field]
    try:
        answer_item = question_answer_dao.get_question_answer_by_id(answer_id, db)
        answer_dict = dict()

        answer_dict[QuestionAnswer.item_id_field] = answer_item.item_id
        answer_dict[QuestionAnswer.question_id_field] = answer_item.question_id
        answer_dict[QuestionAnswer.question_answer_field] = answer_item.question_answer
        answer_dict[QuestionAnswer.mark_percent_field] = answer_item.mark_percent
        answer_dict[QuestionAnswer.sign_mark_field] = answer_item.sign_mark
        answer_dict[QuestionAnswer.is_correct_field] = answer_item.is_correct
        answer_dict[QuestionAnswer.explanation_field] = answer_item.explanation
    except:
        return dict(error=CB_0003)
    return dict(answer=answer_dict)


def get_list_answer_by_qid():
    """  return list answer of question
        get list answer by question_id
        param : question_id
    """
    if len(request.vars) < 1 or QuestionAnswer.question_id_field not in request.vars:
        return dict(mess=CB_0002)
    answer_list_item = list()
    question_id = request.vars[QuestionAnswer.question_id_field]
    try:
        answers = question_answer_dao.get_list_answer_by_question_id(question_id, db)
        for ans in answers:
            answer_item = dict()

            answer_item[QuestionAnswer.item_id_field] = ans.item_id
            answer_item[QuestionAnswer.question_id_field] = ans.question_id
            answer_item[QuestionAnswer.question_answer_field] = ans.question_answer
            answer_item[QuestionAnswer.mark_percent_field] = ans.mark_percent
            answer_item[QuestionAnswer.sign_mark_field] = ans.sign_mark
            answer_item[QuestionAnswer.is_correct_field] = ans.is_correct
            answer_item[QuestionAnswer.explanation_field] = ans.explanation

            answer_list_item.append(answer_item)
    except:
        return dict(error=CB_0003)
    return dict(answers=answer_list_item)