__author__ = 'User'

from applications.cbq.modules.dao import question_content_dao
from applications.cbq.modules.entities.question_entities.question_content import QuestionContent

question_content_request = ('item_id', 'content_id', 'content', 'type', 'des')


def index():
    form = SQLFORM.smartgrid(db.clsb_question_content)
    return dict(form=form)


def insert():
    """ return
        param : content_id&content&type&des
    """
    if len(request.vars) < 3:
        return dict(mess=CB_0002)

    question_content_item = QuestionContent()

    for re in request.vars:
        if re == QuestionContent.content_id_field:
            question_content_item.content_id = request.vars[QuestionContent.content_id_field]
        elif re == QuestionContent.question_content_field:
            question_content_item.question_content = request.vars[QuestionContent.question_content_field]
        elif re == QuestionContent.question_type_field:
            question_content_item.question_type = request.vars[QuestionContent.question_type_field]
        elif re == QuestionContent.description_field:
            question_content_item.description = request.vars[QuestionContent.description_field]
    #print question_content_item.question_content
    try:
        result = question_content_dao.insert_data(question_content_item, db)
    except Exception as e:
        print str(e)
        return dict(error=CB_0003)
    return dict(result=result)


def get_by_id():
    """ return question_content item as dict
        get question content item by id
    """
    if len(request.vars) < 1 and QuestionContent.item_id_field not in request.vars:
        return dict(error=CB_0002)
    question_content = dict()
    question_content_id = request.vars[QuestionContent.item_id]
    try:
        question_content_item = question_content_dao.get_question_content_by_id(question_content_id, db)

        question_content[QuestionContent.item_id_field] = question_content_item.item_id
        question_content[QuestionContent.content_id_field] = question_content_item.content_id
        question_content[QuestionContent.description_field] = question_content_item.description
        question_content[QuestionContent.question_content_field] = question_content_item.question_content
        question_content[QuestionContent.question_type_field] = question_content_item.question_type
    except:
        return dict(error=CB_0003)
    return dict(question_content=question_content)