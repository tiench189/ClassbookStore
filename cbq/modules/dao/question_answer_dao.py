# -*- coding: utf-8 -*-
__author__ = 'PhuongNH'

from applications.cbq.modules.entities.question_entities.question_answer import QuestionAnswer
from applications.cbq.modules import cbMsb

file_tag = "question_answer_dao: "


def get_question_answer_by_id(answer_id, db):
    answer = QuestionAnswer()
    answer_list = db(db.clsb_question_answer.id == answer_id).select()

    if len(answer_list) < 1:
        return dict(error=cbMsb.CB_0001)
    answer_row = answer_list.first()

    try:
        answer.item_id = answer_row[QuestionAnswer.item_id_field]
        answer.question_id = answer_row[QuestionAnswer.question_id_field]
        answer.question_answer = answer_row[QuestionAnswer.question_answer_field]
        answer.mark_percent = answer_row[QuestionAnswer.mark_percent_field]
        answer.sign_mark = answer_row[QuestionAnswer.sign_mark_field]
        answer.is_correct = answer_row[QuestionAnswer.is_correct_field]
        answer.explanation = answer_row[QuestionAnswer.explanation_field]

    except Exception as e:
        print file_tag + ' get_question_answer_by_id ' + str(e)
        raise e
    return answer


def get_list_answer_by_question_id(question_id, db):
    answers = list()
    try:
        answer_list = db(db.clsb_question_answer.question_id == question_id).select()
        for answer_row in answer_list:
            answer = QuestionAnswer()
            answer.item_id = answer_row[QuestionAnswer.item_id_field]
            answer.question_id = answer_row[QuestionAnswer.question_id_field]
            answer.question_answer = answer_row[QuestionAnswer.question_answer_field]
            answer.mark_percent = answer_row[QuestionAnswer.mark_percent_field]
            answer.sign_mark = answer_row[QuestionAnswer.sign_mark_field]
            answer.is_correct = answer_row[QuestionAnswer.is_correct_field]
            answer.explanation = answer_row[QuestionAnswer.explanation_field]
            answers.append(answer)

    except Exception as e:
        print file_tag + ' get_list_answer_by_question_id ' + str(e)
        raise e
    return answers


def insert_data(question_answer_item, db):
    try:
        rows = db((db.clsb_question_answer.question_id == question_answer_item.question_id) & (
            db.clsb_question_answer.question_answer == question_answer_item.question_answer) & (
                db.clsb_question_answer.mark_percent == question_answer_item.mark_percent)).select()

        if len(rows) > 0:
            row = rows.first()
            result = row['id']

        else:
            result = db.clsb_question_answer.insert(question_id=question_answer_item.question_id,
                                                    question_answer=question_answer_item.question_answer,
                                                    mark_percent=question_answer_item.mark_percent,
                                                    is_correct=question_answer_item.is_correct)
    except Exception as e:
        print file_tag + ' insert_data ' + str(e)
        raise e
    return result