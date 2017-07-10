__author__ = 'User'

from applications.cbq.modules.entities.question_entities.quiz_category import QuizCategory
from applications.cbq.modules.entities.question_entities.category_relation import CategoryRelation
from applications.cbq.modules.dao import quiz_category_dao
from applications.cbq.modules.dao import question_dao

tag = 'quiz_category.py '
class_category_code = 'LOP'
subject_category_code = 'MON_HOC'


def get_list_quiz_category():

    class_id = request.vars['class_id']
    subject_id = request.vars['subject_id']

    category_list = list()

    category_object_list = quiz_category_dao.get_all_category(db, class_id, subject_id)

    for category in category_object_list:
        item = dict()
        item[QuizCategory.item_id_field] = category.item_id
        item[QuizCategory.category_code_field] = category.category_code
        item[QuizCategory.category_name_field] = category.category_name
        category_list.append(item)

    return dict(category_list=category_list)


def get_list_quiz_category_by_parent_id():
    category_list = list()
    try:
        category_id = int(request.vars['parent_id'])
        rows = quiz_category_dao.get_list_quiz_category_by_parent_id(category_id, db)

        for row in rows:
            item = dict()
            item['id'] = row.item_id
            item['category_code'] = row.category_code
            item['category_name'] = row.category_name
            item['description'] = row.description
            item['parent_id'] = row.parent_id
            item['category_level'] = row.category_level
            category_list.append(item)
    except Exception as e:
        print tag + 'get_list_quiz_category_by_parent_id' + str(e)
    return dict(category_list=category_list)


def get_list_class_category():
    category_list = list()
    try:
        #class_category_item = quiz_category_dao.get_quiz_category_by_code(class_category_code, db)
        cate_class_list = quiz_category_dao.get_category_by_parent_id_and_level(None, db)

        print 'len class_category_item ' + str(len(cate_class_list))
        #cate_class_list = quiz_category_dao.get_list_quiz_category_by_parent_id(class_category_item.item_id, db)

        if cate_class_list is None:
            return dict(class_list=category_list)

        for row in cate_class_list:
            item = dict()
            item['id'] = row.item_id
            item['category_code'] = row.category_code
            item['category_name'] = row.category_name
            item['description'] = row.description
            item['parent_id'] = row.parent_id
            category_list.append(item)
    except Exception as e:
        print tag + ' get_list_class_category ' + str(e)
    return dict(class_list=category_list)


def get_list_subject_category():
    category_list = list()
    try:

        print request.vars
        class_id = request.vars['class_id']
        #class_category_item = quiz_category_dao.get_quiz_category_by_code(class_category_code, db)
        cate_subject_list = quiz_category_dao.get_category_by_parent_id_and_level(class_id, db)

        print 'len class_category_item ' + str(len(cate_subject_list))
        #cate_class_list = quiz_category_dao.get_list_quiz_category_by_parent_id(class_category_item.item_id, db)

        if cate_subject_list is None:
            return dict(class_list=category_list)

        for row in cate_subject_list:
            item = dict()
            item['id'] = row.item_id
            item['category_code'] = row.category_code
            item['category_name'] = row.category_name
            item['description'] = row.description
            item['parent_id'] = row.parent_id
            category_list.append(item)
    except Exception as e:
        print tag + ' get_list_subject_category ' + str(e)
    return dict(subject_list=category_list)


def get_category_has_parent_map():

    category_list = list()

    quiz_category_list = quiz_category_dao.get_quiz_category_has_parent_map(db)

    for row in quiz_category_list:
        item = dict()
        item['id'] = row.item_id
        item['category_code'] = row.category_code
        item['category_name'] = row.category_name
        item['description'] = row.description
        item['parent_id'] = row.parent_id
        category_list.append(item)

    return dict(category_list=category_list)


#def insert_class():
#    result = 0
#    if len(request.vars) < 3:
#        return dict(result=result)
#    print request.vars
#    try:
#        category_class = quiz_category_dao.get_quiz_category_by_code('LOP', db)
#
#        if category_class is None:
#                return dict(result=result)
#        quiz_category = QuizCategory()
#        quiz_category.category_code = request.vars['category_code']
#        quiz_category.category_name = request.vars['category_name']
#        quiz_category.description = request.vars['description']
#        quiz_category.parent_id = category_class.item_id
#
#        result = quiz_category_dao.insert(quiz_category, db)
#        print 'pass' + str(result)
#    except Exception as e:
#        print str(e)
#
#    return dict(result=result)
#
#
#def insert_subject():
#    if len(request.vars) < 3:
#        return dict(result=0)
#    result = 0
#    try:
#        category_subject = quiz_category_dao.get_quiz_category_by_code('MON_HOC', db)
#
#        print category_subject.item_id
#        if category_subject is None:
#            return dict(result=result)
#
#        quiz_category = QuizCategory()
#        quiz_category.category_code = request.vars['category_code']
#        quiz_category.category_name = request.vars['category_name']
#        quiz_category.description = request.vars['description']
#        quiz_category.parent_id = category_subject.item_id
#
#        result = quiz_category_dao.insert(quiz_category, db)
#    except Exception as e:
#        print str(e)
#
#    return dict(result=result)


def insert_category():
    result = 0
    print request.vars
    if len(request.vars) < 5:
        return dict(result=result)
    try:
        category_level = int(request.vars['category_level'])
        print str(category_level)
        prefix_cate_level = 'sclParent'
        parent_id = None
        for i in range(0, (category_level+1)):
            if prefix_cate_level + str(i) in request.vars:
                if int(request.vars[prefix_cate_level + str(i)]) != -1:
                    parent_id = request.vars[prefix_cate_level + str(i)]
                else:
                    break
        print 'parent_id ' + str(parent_id)
        # get info of parent_category
        if parent_id is not None:
            print parent_id
            category_parent = quiz_category_dao.get_category_by_id(parent_id, db)
            category_parent.print_info()

        #parent_id = request.vars['sclParent']
        #if parent_id == '-1':
        #    parent_id = None
        #child_id = request.vars['sclChild']
        #if child_id == '-1':
        #    child_id = None

        category_code = request.vars['category_code']
        category_name = request.vars['category_name']
        des = request.vars['des']

        quiz_category = QuizCategory()
        quiz_category.category_code = category_code
        quiz_category.category_name = category_name
        quiz_category.description = des
        if parent_id is not None:
            quiz_category.parent_id = parent_id
            quiz_category.category_level = int(category_parent.category_level) + 1
        else:
            quiz_category.category_level = '1'

        result = quiz_category_dao.insert(quiz_category, db)

    except Exception as e:
        print str(e)

    return dict(result=result)


def get_list_category_name():
    category_name_dict = list()
    try:
        category_name_list = quiz_category_dao.get_all_category(db)
        for row in category_name_list:
            item = dict()
            item['category_name'] = row.category_name
            category_name_dict.append(item)
    except Exception as e:
        print str(e)
    return dict(category_name_list=category_name_dict)


def get_list_category_has_null_parent():
    category_dict_list = list()
    try:
        category_list = quiz_category_dao.get_list_category_has_null_parent(db)

        if category_list is None:
            return dict(class_list=category_list)

        for row in category_list:
            item = dict()
            item['id'] = row.item_id
            item['category_code'] = row.category_code
            item['category_name'] = row.category_name
            item['description'] = row.description
            item['parent_id'] = row.parent_id
            category_dict_list.append(item)
    except Exception as e:
        print tag + ' get_list_class_category ' + str(e)
    return dict(class_list=category_dict_list)


def get_all_cate():
    category_dict_list = list()
    category_list = quiz_category_dao.get_all_category(db)
    for row in category_list:
            total_question = question_dao.get_total_question_by_category(row.item_id, db)
            item = dict()
            item['id'] = row.item_id
            item['category_code'] = row.category_code
            item['category_name'] = row.category_name
            item['description'] = row.description
            item['parent_id'] = row.parent_id
            item['total_question'] = total_question
            category_dict_list.append(item)
    return dict(category_list=category_dict_list)


def get_list_tree_category():
    cate_list = list()
    parent_id = int(request.vars['parent_id'])
    category_list = quiz_category_dao.get_all_tree_category_by_id(parent_id, db)
    for row in category_list:
            total_question = question_dao.get_total_question_by_category(row.item_id, db)
            item = dict()
            item['id'] = row.item_id
            item['category_code'] = row.category_code
            item['category_name'] = row.category_name
            item['description'] = row.description
            item['parent_id'] = row.parent_id
            item['total_question'] = total_question
            cate_list.append(item)
    return dict(result=cate_list)


def test():
    max_value = quiz_category_dao.get_max_level_in_quiz_category(db)

    return dict(category_dict_list=str(max_value))