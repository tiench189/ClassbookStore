__author__ = 'User'


from applications.cbq.modules.dao import quiz_category_dao
from applications.cbq.modules.dao import question_dao


def index():

    return dict()


def report_question_by_parent():

    parent_id = request.vars['parent_id']
    if parent_id == '':
        parent_id = None
    i = 0
    result = list()
    # get all category
    category_list = quiz_category_dao.get_list_quiz_category_by_parent_id(parent_id, db)

    for category_item in category_list:
        item = dict()
        number_question = question_dao.get_total_question_by_category(category_item.item_id, db)

        item['name'] = category_item.category_name
        item['value'] = number_question
        item['id'] = category_item.item_id
        item['level'] = category_item.category_level

        result.append(item)

    return dict(result=result)
#def report_question_by_class():
#
#    result = list()
#    # get all class
#    class_list = quiz_category_dao.get_class_list(db)
#    for class_item in class_list:
#        item = dict()
#
#        number_question = question_dao.get_total_question_by_class(class_item.item_id, db)
#
#        item['name'] = class_item.category_name
#        item['value'] = number_question
#
#        result.append(item)
#
#    return dict(result=result)
#
#
#def report_question_by_subject():
#
#    result = list()
#    # get all class
#    subject_list = quiz_category_dao.get_subject_list(db)
#    for subject_item in subject_list:
#        item = dict()
#
#        number_question = question_dao.get_total_question_by_subject(subject_item.item_id, db)
#
#        item['name'] = subject_item.category_name
#        item['value'] = number_question
#
#        result.append(item)
#
#    return dict(result=result)
#
#
def report_question_by_category():

    child_id = request.vars['child_id']

    result = list()
    # get all category
    #category_list = quiz_category_dao.get_quiz_category_has_parent_map(db)
    category_list = quiz_category_dao.get_list_quiz_category_by_parent_id(child_id, db)

    for category_item in category_list:
        item = dict()

        number_question = question_dao.get_total_question_by_category(category_item.item_id, db)

        item['name'] = category_item.category_name
        item['value'] = number_question

        result.append(item)

    return dict(result=result)





