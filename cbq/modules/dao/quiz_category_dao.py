from applications.cbq.modules.util.answer_to_html_element import parse_list_answer_to_html

__author__ = 'User'

from applications.cbq.modules.entities.question_entities.quiz_category import QuizCategory
#from applications.cbq.modules.dao import category_relation_dao

tag = "quiz_category_dao"
class_category_code = 'LOP'
subject_category_code = 'MON_HOC'


def parse_category_record_to_object(record):
    """
    @todo : parse category record select from db to QuizCategory object
    @param record:
    @return:
    """
    quiz_category = QuizCategory()
    try:
        quiz_category = QuizCategory()
        quiz_category.item_id = record[QuizCategory.item_id_field]

        quiz_category.category_code = record[QuizCategory.category_code_field]
        quiz_category.category_name = record[QuizCategory.category_name_field]
        quiz_category.description = record[QuizCategory.description_field]
        quiz_category.parent_id = record[QuizCategory.parent_id_field]
        quiz_category.parent_map = record[QuizCategory.parent_map_file]
        quiz_category.category_level = record[QuizCategory.category_level_field]
    except Exception as e:
        print tag + 'parse_category_record_to_object ' + str(e)
        #quiz_category = QuizCategory()
    return quiz_category


def get_all_tree_category_by_id(category_id, db):
    cate_list = list()
    category_list = get_list_quiz_category_by_parent_id(category_id, db)
    cate_list += category_list
    while len(category_list) > 0:
        cate_tmpp = category_list
        category_list = list()
        for cate in cate_tmpp:
            print cate.category_name
            cate_tempp = get_list_quiz_category_by_parent_id(cate.item_id, db)
            cate_list += cate_tempp
            category_list += cate_tempp
    return cate_list


def get_all_category_by_level(category_level, db):
    category_list = list()
    try:
        rows = db(db.clsb_quiz_category.category_level == category_level).select()
        for row in rows:
            category = parse_category_record_to_object(row)
            category_list.append(category)
    except Exception as e:
        print tag + str(e)
    return category_list


def get_category_by_id(category_id, db):
    try:
        rows = db(db.clsb_quiz_category.id == category_id).select()
        row = rows.first()
        category = parse_category_record_to_object(row)
    except Exception as e:
        print str(e)
        return None
    return category


def get_category_by_name(category_name, db):
    try:
        rows = db(db.clsb_quiz_category.category_name == category_name).select()
        row = rows.first()
        category = parse_category_record_to_object(row)
    except Exception as e:
        print str(e)
        return None
    return category

#def get_all_category(db, class_id, subject_id):
#    """
#    @todo : get all category object in table tbl_quiz_category
#    @return: list category object
#    """
#    category_list = list()
#    category_relation = category_relation_dao.get_category_relation_by_cate_id(class_id, subject_id, db)
#
#    if category_relation is None:
#        return category_list
#    item_id = int(category_relation.item_id)
#    rows = db(db.clsb_quiz_category.parent_map == item_id).select()
#
#    if rows is None:
#        return None
#
#    for row in rows:
#        try:
#            quiz_category = parse_category_record_to_object(row)
#
#            category_list.append(quiz_category)
#
#        except Exception as e:
#            print tag + str(e)
#    return category_list


#def get_total_category_by_parent_id(category_id, db):
#    """
#    @todo : get all quiz_category by parent_id = category_id (recursive)
#    @param category_id:
#    @param db:
#    @return:
#    """
#
#    category_list = list()
#
#
#    return category_list


def get_list_quiz_category_by_parent_id(category_id, db):
    """
    @todo : get quiz_category list has parent_id = category_id (not recursive)
    @param category_id:
    @return:
    """
    category_list = list()
    try:
        rows = db(db.clsb_quiz_category.parent_id == category_id).select()

        for row in rows:
            quiz_category = parse_category_record_to_object(row)
            category_list.append(quiz_category)

    except Exception as e:
        print tag + 'get_list_quiz_category_by_parent_id' + str(e)

    return category_list


#def get_quiz_category_parent_list(db):
#    """
#    @todo : get all quiz_category parent (has parent_id = None)
#    @param db:
#    @return:
#    """
#    category_list = list()
#    try:
#        rows = db(db.clsb_quiz_category.parent_id is None).select()
#
#        for row in rows:
#            quiz_category = parse_category_record_to_object(row)
#            category_list.append(quiz_category)
#
#    except Exception as e:
#        print tag + ' get_list_quiz_category_by_parent_id ' + str(e)
#    return category_list


def get_quiz_category_by_code(category_code, db):
    """
    @todo : get quiz_category by category_code
    @param category_code:
    @param db:
    @return:
    """
    try:

        rows = db(db.clsb_quiz_category.category_code == category_code).select()

        if rows is None or len(rows) < 1:
            return None

        row = rows.first()
        quiz_category = parse_category_record_to_object(row)
    except Exception as e:
        print tag + ' get_quiz_category_by_code ' + str(e)
        quiz_category = None
    return quiz_category


def get_quiz_category_by_id(category_id, db):
    """
    @todo : get quiz_category by id
    @param category_code:
    @param db:
    @return:
    """
    try:

        rows = db(db.clsb_quiz_category.id == category_id).select()

        if rows is None or len(rows) < 1:
            return None

        row = rows.first()
        quiz_category = parse_category_record_to_object(row)
    except Exception as e:
        print tag + ' get_quiz_category_by_id ' + str(e)
        quiz_category = None
    return quiz_category


def get_quiz_category_has_parent_map(db):
    """
    @todo : get list category has parent_map is None
    @param db:
    @return:
    """
    quiz_category_list = list()
    quiz_cate_list = list()

    try:
        #rows = db(db.clsb_quiz_category.category_level == '3').select()
        rows = db(db.clsb_quiz_category.parent_id != None).select()

        if rows is None:
            return quiz_category_list

        for row in rows:
            quiz_category = parse_category_record_to_object(row)
            quiz_category_list.append(quiz_category)

        for quiz in quiz_category:

            rows = db(db.clsb_quiz_category.parent_id == quiz.parent_id)
            if len(rows) > 0:
                continue
            else:
                quiz_cate_list.append(quiz)

        #for row in rows:
        #    quiz_category = parse_category_record_to_object(row)
        #    quiz_category_list.append(quiz_category)

    except Exception as e:
        print tag + ' get_quiz_category_has_parent_map ' + str(e)

    return quiz_category_list


def get_category_by_parent_id_and_level(parent_id, db):
    category_list = list()
    if parent_id is None:
        rows = db((db.clsb_quiz_category.parent_id == None)).select()
    else:
        rows = db(db.clsb_quiz_category.parent_id == parent_id).select()

    for row in rows:
        category = parse_category_record_to_object(row)
        category_list.append(category)

    return category_list


def get_class_list(db):
    try:
        class_category_item = get_quiz_category_by_code(class_category_code, db)

        cate_class_list = get_list_quiz_category_by_parent_id(class_category_item.item_id, db)

    except Exception as e:
        cate_class_list = list()
        print tag + str(e)

    return cate_class_list


def get_list_category_has_null_parent(db):
    category_list = list()
    try:
        rows = db(db.clsb_quiz_category.parent_id == None).select()

        for row in rows:
            category = parse_category_record_to_object(row)
            category_list.append(category)
    except Exception as e:
        category_list = list()
        print tag + ' get_list_category_has_null_parent ' + str(e)

    return category_list


def get_subject_list(db):
    try:
        subject_category_item = get_quiz_category_by_code(subject_category_code, db)

        cate_subject_list = get_list_quiz_category_by_parent_id(subject_category_item.item_id, db)

    except Exception as e:
        cate_subject_list = list()
        print tag + str(e)

    return cate_subject_list


def insert(quiz_category, db):
    result = 0
    print quiz_category.print_info()
    try:
        result = db.clsb_quiz_category.insert(category_code=quiz_category.category_code,
                                              category_name=quiz_category.category_name,
                                              description=quiz_category.description,
                                              parent_id=quiz_category.parent_id, parent_map=quiz_category.parent_map,
                                              category_level=quiz_category.category_level)
    except Exception as e:
        print str(e)
    return result


def get_all_category(db):
    cate_list = list()
    rows = db(db.clsb_quiz_category).select()

    for row in rows:
        #total_question = question_dao.get_total_question_by_category(row.item_id, db)

        cate = parse_category_record_to_object(row)
        #cate['total_question'] = total_question
        cate_list.append(cate)

    return cate_list


def get_list_category_name(db):

    category_list = get_all_category(db)
    category_name_list = list()
    for i in range(0, len(category_list)):
        category_name_list.append(category_name_list[i].category_name)

    return category_name_list


def get_all_category_by_parent_id(parent_id, db):

    parent_id_level = 0
    category_max_level = int(get_max_level_in_quiz_category(db))

    category_list = list()
    category_tmp = list()
    category_tmp.append(parent_id)
    for i in range(parent_id_level + 1, category_max_level):
        category_tmp = get_list_category_by_parent_id(category_tmp, db)
        if len(category_tmp) > 0:
            for j in range(0, len(category_tmp)):
                category_list.append(category_tmp[j])
    category_list.append(parent_id)
    return category_list


def get_list_category_by_parent_id(category_id_list, db):
    category_list = list()
    rows = db(db.clsb_quiz_category.parent_id.belongs(category_id_list)).select()

    for row in rows:
        category_list.append(row[QuizCategory.item_id_field])

    return category_list


def get_max_level_in_quiz_category(db):
    max_level = db.clsb_quiz_category.category_level.max()
    max_level = db().select(max_level).first()[max_level]

    return max_level


