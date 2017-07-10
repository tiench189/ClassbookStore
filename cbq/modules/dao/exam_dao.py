__author__ = 'User'
from applications.cbq.modules.entities.question_entities.exam import Exam
#from applications.cbq.modules.dao import question_dao
#from applications.cbq.modules.dao import exam_dao
from applications.cbq.modules import cbMsb
from random import randint

tag = "exam_dao: "


def delete_exam(exam_id, db):
    try:
        result = db(db.clsb_exam.id == exam_id).delete()
        redirect(URL("cbq", "exam", "index", host=True))
    except Exception as e:
        result = 0
        print tag + ' delete_exam ' + str(e)
    return result


def get_exam_by_id(exam_id, db):

    rows = db(db.clsb_exam.id == exam_id).select()

    if rows is None:
        return None
    row = rows.first()

    try:
        exam_item = Exam()
        exam_item.item_id = row[Exam.item_id_field]
        exam_item.exam_id = row[Exam.exam_id_field]
        exam_item.name = row[Exam.name_field]
        exam_item.duration = row[Exam.duration_field]
        exam_item.exam_type = row[Exam.type_field]
        exam_item.des = row[Exam.description_field]
        exam_item.total_mark = row[Exam.total_mark_field]
        exam_item.number_question = row[Exam.number_question_field]
        exam_item.cover = row[Exam.cover_field]
        exam_item.exam_mode = row[Exam.exam_mode_filed]

    except Exception as e:
        print tag + "get_exam_by_id : " + str(e)
        raise e
    return exam_item


def insert(exam_item, db):
    """
    @todo insert new record into table clsb_exam
    @param exam_item:
    @param db:
    @return: id of record has just inserted
    """
    result = -1
    if exam_item is None:
        return result
    try:
        result = db.clsb_exam.insert(exam_id=exam_item.exam_id, name=exam_item.name, exam_type=exam_item.exam_type,
                                     des=exam_item.des, duration=exam_item.duration,
                                     number_question=exam_item.number_question, cover=exam_item.cover,
                                     total_mark=exam_item.total_mark, exam_mode=exam_item.exam_mode)
        print 'id exam sau khi tao ' + str(result)
        print db.clsb_exam(id=result)
    except Exception as e:
        print tag + "insert " + str(e)
    return result


def edit_exam(exam_item):
    """
    @todo edit exam item
    @param exam_item:
    @return:
    """
    if exam_item is None:
        return dict(error=cbMsb.CB_0007)

    try:
        result = db(db.clsb_exam.id == exam_item.item_id).update(name=exam_item.name, exam_type=exam_item.exam_type,
                                                                 des=exam_item.des, duration=exam_item.duration,
                                                                 number_question=exam_item.number_question,
                                                                 cover=exam_item.cover,
                                                                 total_mark=exam_item.total_mark,
                                                                 exam_mode=exam_item.exam_mode)
    except Exception as e:
        print tag + " edit " + str(e)
        raise e

    return result


def get_all_exam(db, page, exam_name):
    """

    @todo : get all exam record in table clsb_exam
    @param db:
    @return: list exam item
    """
    page_size = 10
    max_record = page * page_size
    min_record = (page - 1) * page_size
    exam_list = list()

    rows = db(db.clsb_exam.name.like('%' + exam_name + '%')).select(limitby=(min_record, max_record))

    if rows is None:
        return None

    for row in rows:
        try:
            exam_item = Exam()
            exam_item.item_id = row[Exam.item_id_field]
            exam_item.exam_id = row[Exam.exam_id_field]
            exam_item.name = row[Exam.name_field]
            exam_item.duration = row[Exam.duration_field]
            exam_item.exam_type = row[Exam.type_field]
            exam_item.des = row[Exam.description_field]
            exam_item.total_mark = row[Exam.total_mark_field]
            exam_item.number_question = row[Exam.number_question_field]
            exam_item.cover = row[Exam.cover_field]
            exam_item.exam_mode = row[Exam.exam_mode_filed]

            exam_list.append(exam_item)
        except Exception as e:
            print tag + "get_all_exam : " + str(e)
            raise e

    return exam_list


def count_all(db):
    try:
        total_record = db(db.clsb_exam).count()
    except Exception as e:
        total_record = 0
        print tag + " count all " + str(e)
    return total_record


def update_exam_number_question(exam_id, question_count, db):
    """
    @todo : update column "number_question" in table clsb_question where id = exam_id
    @param exam_id:
    @param question_count:
    @param db:
    @return:
    """
    try:
        exam = get_exam_by_id(exam_id, db)
        if exam.number_question is None or exam.number_question == 'None':
            current_question = 0
        else:
            current_question = int(exam.number_question)
        number_question = current_question + int(question_count)

        result = db(db.clsb_exam.id == exam_id).update(number_question=number_question)
    except Exception as e:
        print tag + 'update_exam_number_question' + str(e)
        result = -1
    return result


def update_exam_total_mark(exam_id, total_mark, db):
    """
    @todo : update total_mark field of record
    @param exam_id:
    @param total_mark:
    @param db:
    @return:
    """
    try:
        result = db(db.clsb_exam.id == exam_id).update(total_mark=total_mark)
    except Exception as e:
        print tag + 'update_exam_total_mark' + str(e)
        result = -1
    return result


def check_question_invalid(question_used_list, question_id, max_occurrence, question_used_in_segment, segment_question_list, segment_order):
    """
    @todo : check question invalid
    @param question_used_list:
    @param question_id:
    @param max_occurrence:
    @return:
    """
    try:
        segment_question = str(segment_order) + "_" + str(question_id)
        if segment_question in segment_question_list:
            return False
        if question_id in question_used_in_segment:
            return False
        #if question_used_list.get(question_id) is None:
        #    question_used_list[question_id] = 1
        #    return True
        #else:
        #    number_of_occurrences = question_used_list.get(question_id)
        #    if number_of_occurrences >= max_occurrence:
        #        return False
        #    else:
        #        question_used_list[question_id] = (max_occurrence+1)
        #        return True
    except Exception as e:
        print 'exam dao : check_question_invalid ' + str(e)
    return True

def check_to_delete_question(question_used_list, question_id, max_occurrence, question_used_in_exam):
    try:
        if question_id in question_used_in_exam:
            return True
        if question_used_list.get(question_id) is None:
            return False
        elif question_used_list.get(question_id) == max_occurrence:
            return True
        return dict()
    except Exception as e:
        print 'exam dao : check_to_delete_question ' + str(e)


def get_invalid_question(question_used_in_exam, question_list, max_occurrence, question_used_list, segment_question_list, segment_order):
    """
    @param question_used_in_exam:
    @param question_list: list of question object (
    @param max_occurrence:
    @param question_used_list:
    @return: -1 if can not get a question, else return question_id
    """

    retry_counter = 0
    total_question = len(question_list)
    try:
        print 'bat dau chay vong lap'
        #while True:

        selected_index = randint(0, (total_question-1))

        #if selected_index in question_used_in_exam:
        #    print 'hiuhiu'
        #
        #result = check_question_invalid(question_used_list, question_list[selected_index].item_id, max_occurrence, question_used_in_exam, segment_question_list, segment_order)

        #if result:
        #    return question_list[selected_index].item_id
        #else:
        #    retry_counter += 1
        #    if retry_counter == 10:
        #        return None
        #print 'chay xong khoi vong lap'
        return question_list[selected_index]
    except Exception as e:
        print 'exam_dao' + ' get_invalid_question ' + str(e)
        return None
    return -1


def check_to_delete_question_invalid(question_used_dict, question_list, max_occurrence, question_used_in_exam, j, segment_question_list):
    question_list_result = list()
    list_question_invalid = list()

    # filter cau hoi xuat hien trong exam:
    for i in range(0, len(question_list)):
        for j in range(0,  len(question_used_in_exam)):
            if question_used_in_exam[j] == question_list[i].item_id:
                list_question_invalid.append(question_list[i].item_id)
    #filter cau hoi xuat hien theo segment_question:
    for i in range(0,  len(question_list)):
        item_tmp = str(j) + '_' + str(question_list[i].item_id)
        if item_tmp in segment_question_list:
            if question_list[i].item_id not in list_question_invalid:
                list_question_invalid.append(question_list[i].item_id)
    for k, v in question_used_dict.iteritems():
        if k in question_used_dict:
            if v >= max_occurrence:
                print str(k) + 'da xuat hien ' + str(v) + 'lan'
                if k not in list_question_invalid:
                    list_question_invalid.append(k)
    for i in range(len(question_list)):
        if question_list[i].item_id in list_question_invalid:
            continue
        else:
            question_list_result.append(question_list[i])

    return question_list_result


#def get_all_exam(db):
#    """
#
#    @todo : get all exam record in table clsb_exam
#    @param db:
#    @return: list exam item
#    """
#
#    exam_list = list()
#
#    rows = db(db.clsb_exam).select()
#
#    if rows is None:
#        return None
#
#    for row in rows:
#        try:
#            exam_item = Exam()
#            exam_item.item_id = row[Exam.item_id_field]
#            exam_item.exam_id = row[Exam.exam_id_field]
#            exam_item.name = row[Exam.name_field]
#            exam_item.duration = row[Exam.duration_field]
#            exam_item.exam_type = row[Exam.type_field]
#            exam_item.des = row[Exam.description_field]
#            exam_item.total_mark = row[Exam.total_mark_field]
#            exam_item.number_question = row[Exam.number_question_field]
#            exam_item.cover = row[Exam.cover_field]
#            exam_item.exam_mode = row[Exam.exam_mode_filed]
#
#            exam_list.append(exam_item)
#        except Exception as e:
#            print tag + "get_all_exam : " + str(e)
#            raise e
#
#    return exam_list