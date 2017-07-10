from applications.cbq.modules.dao import quiz_category_dao

__author__ = 'User'

from applications.cbq.modules.entities.question_entities.category_question import CategoryQuestion

tag = "category_question_dao"


def insert(category_question, db):
    try:

        result = db.clsb_category_question.insert(category_id=category_question.category_id,
                                                  question_id=category_question.question_id)
    except Exception as e:
        print tag + "insert_data" + str(e)
        result = -1

    return result


def get_list_by_cate_id(cate_id, db):

    category_list = quiz_category_dao.get_all_category_by_parent_id(cate_id, db)
    print category_list
    cate_question_list = list()

    try:

        rows = db(db.clsb_category_question.category_id.belongs(category_list)).select()

        for row in rows:
            cate_question = CategoryQuestion()
            cate_question.item_id = row[CategoryQuestion.item_id_field]
            cate_question.category_id = row[CategoryQuestion.category_id_field]
            cate_question.question_id = row[CategoryQuestion.question_id_field]
            cate_question_list.append(cate_question)

    except Exception as e:
        print tag + " get_list_by_cate_id " + str(e)

    return cate_question_list


