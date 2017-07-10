# -*- coding: utf-8 -*-
__author__ = 'PhuongNH'

from applications.cbq.modules.entities.question_entities.question_content import QuestionContent
from applications.cbq.modules import cbMsb

file_tag = "question_content_dao"


def insert_data(question_content_item, db):
    """ return id of record just inserted
    insert a new record into table clsb_question_content
    """
    if question_content_item is None:
        return dict(error=cbMsb.CB_0002)

    if question_content_item.question_content is not None:
        question_content_item.question_content = question_content_item.question_content.replace('</span>', '')

    rows = db(db.clsb_question_content.question_content == question_content_item.question_content).select()

    if len(rows) > 0:
        row = rows.first()
        result = row['id']
        return result
    try:

        result = db.clsb_question_content.insert(content_id=question_content_item.content_id,
                                                 question_content=question_content_item.question_content,
                                                 description=question_content_item.description,
                                                 question_type=question_content_item.question_type)
    except Exception as e:
        print file_tag + " insert_data " + str(e)
        result = -1
    return result


def delete_question_content_by_id(question_content_id, db):
    try:
        result = db(db.clsb_question_content.id == question_content_id).delete()
    except Exception as e:
        result = 0
        print str(e)
    return result


def get_question_content_by_id(question_content_id, db):
    """ return a record question content as dict
    get question content by question content id
    """
    #question_content = dict()
    if question_content_id is None:
        return dict(error=cbMsb.CB_0002)

    try:
        question_content_row = db(db.clsb_question_content.id == question_content_id).select().first()
        question_content_item = QuestionContent()

        question_content_item.item_id = question_content_row[QuestionContent.item_id_field]
        question_content_item.content_id = question_content_row[QuestionContent.content_id_field]
        question_content_item.question_content = question_content_row[QuestionContent.question_content_field]
        question_content_item.description = question_content_row[QuestionContent.description_field]

    except Exception as e:
        print file_tag + " get_question_content_by_id " + str(e)
        raise e

    return question_content_item


def search_key_word(question_content_id, key_word, db):
    result = False
    try:
        if question_content_id is None:
            return result
        question_content = get_question_content_by_id(question_content_id, db)
        if question_content.question_content is not None and question_content.question_content != "":
            if key_word in question_content.question_content:
                result = True
    except Exception as e:
        print 'loi' + str(e)
    return result
