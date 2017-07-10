# -*- coding: utf-8 -*-
__author__ = 'PhuongNH'

import os
import time

from applications.cbq.modules.entities.question_entities.question import Question
from applications.cbq.modules.util import file_util
from applications.cbq.modules.entities.json_entities.media_object import MediaObject
from applications.cbq.modules.entities.question_entities.exam_page import ExamPage
from applications.cbq.modules.entities.question_entities.segment_question import SegmentQuestion
from applications.cbq.modules.entities.question_entities.category_question import CategoryQuestion
from applications.cbq.modules.entities.question_entities.question_content import QuestionContent
from applications.cbq.modules.entities.question_entities.question_answer import QuestionAnswer
from applications.cbq.modules.dao import category_question_dao
from applications.cbq.modules.dao import question_content_dao
from applications.cbq.modules.dao import question_answer_dao
from applications.cbq.modules.dao import segment_question_dao
#from applications.cbq.modules.dao import category_relation_dao
from applications.cbq.modules.dao import quiz_category_dao
from applications.cbq.modules.dao import exam_dao
from applications.cbq.modules.dao import exam_segment_dao
from applications.cbq.modules.util import db_util
from applications.cbq.modules.util import answer_to_html_element
from applications.cbq.modules.util import media_to_html_element
from applications.cbq.modules.entities import app_constant
from applications.cbq.modules import cbMsb

tag = "question_dao : "


def insert_data(question_item, category_id, db):
    if question_item is None:
        return dict(error=cbMsb.CB_0007)

    if question_item.question_guide is not None:
        question_item.question_guide = question_item.question_guide.replace('</span>', '')
    if question_item.explanation is not None:
        question_item.explanation = question_item.explanation.replace('</span>', '')

    #rows = db((db.clsb_question.question_type == question_item.question_type) & (
    #    db.clsb_question.difficult_level == question_item.difficult_level)).select()
    #        #  & (
    #        #db.clsb_question.question_guide == question_item.question_guide)).select()
    #
    #if len(rows) > 0:
    #    row = rows.first()
    #    result = row['id']
    #    return result

    try:
        result = db.clsb_question.insert(content_id=question_item.content_id,
                                         mark=question_item.mark,
                                         question_type=question_item.question_type,
                                         difficult_level=question_item.difficult_level,
                                         question_guide=question_item.question_guide,
                                         explanation=question_item.explanation)

        category_question = CategoryQuestion()
        category_question.category_id = category_id
        category_question.question_id = result

        result_category = category_question_dao.insert(category_question, db)

    except Exception as e:
        print tag + "insert_data" + str(e)
        result = -1
    return result


def get_list_question_by_type(type_name, db):
    question_list = list()
    try:
        rows = db(db.clsb_question.question_type == type_name).select()

        for question_row in rows:
            question_item = Question()
            question_item.item_id = question_row[Question.item_id_field]
            question_item.content_id = question_row[Question.content_id_field]
            question_item.mark = question_row[Question.mark_field]
            question_item.description = question_row[Question.description_field]
            question_item.difficult_level = question_row[Question.difficult_level_field]
            question_item.page_index = question_row[Question.page_index_field]
            question_item.question_guide = question_row[Question.question_guide_field]
            question_item.question_type = question_row[Question.type_field]
            question_item.explanation = question_row[Question.explanation_field]
            question_list.append(question_item)
    except Exception as e:
        print str(e)

    return question_list


def get_question_by_id(question_id, db):
    # get question
    question_list = db(db.clsb_question.id == question_id).select()

    if len(question_list) < 1:
        return None
    question_row = question_list.first()

    try:
        question_item = Question()
        question_item.item_id = question_row[Question.item_id_field]
        question_item.content_id = question_row[Question.content_id_field]
        question_item.mark = question_row[Question.mark_field]
        question_item.description = question_row[Question.description_field]
        question_item.difficult_level = question_row[Question.difficult_level_field]
        question_item.page_index = question_row[Question.page_index_field]
        question_item.question_guide = question_row[Question.question_guide_field]
        question_item.question_type = question_row[Question.type_field]
        question_item.explanation = question_row[Question.explanation_field]

    except Exception as e:
        print tag + "get_question_by_id" + str(e)
        raise e

    return question_item


def get_all_record(db, page):
    """

    @param db:
    @param page: number of page
    @return: list question
    """
    page_size = 20
    max_record = page * page_size
    min_record = (page - 1) * page_size
    question_list = list()

    rows = db(db.clsb_question).select(limitby=(min_record, max_record))

    if rows is None:
        return question_list

    for row in rows:
        try:
            item = Question()
            item.item_id = row[Question.item_id_field]
            item.content_id = row[Question.content_id_field]
            item.description = row[Question.description_field]
            item.difficult_level = row[Question.difficult_level_field]
            item.explanation = row[Question.explanation_field]
            item.page_index = row[Question.page_index_field]
            item.mark = row[Question.mark_field]
            item.explanation = row[Question.explanation_field]
            item.question_guide = row[Question.question_guide_field]
            item.question_title = row[Question.question_title_field]
            item.question_type = row[Question.type_field]
            question_list.append(item)
        except Exception as e:
            print tag + " get_all_record : " + str(e)
    return question_list


def count_all(db):
    """
    @todo : count total record in table clsb_question
    @param db:
    @return:
    """
    try:
        total_record = db(db.clsb_question).count()
    except Exception as e:
        total_record = 0
        print tag + " count all " + str(e)
    return total_record


def add_segment_question(id_question_list, exam_id, segment_id, db):
    #id_question_list = id_list.split(',')
    lastest_order = segment_question_dao.get_last_order_segment_question(segment_id, db)
    for question_id in id_question_list:
        if str(question_id).strip() == '':
            continue
        lastest_order += 1
        segment_question = SegmentQuestion()
        segment_question.segment_id = segment_id
        segment_question.question_id = question_id
        segment_question.question_order = lastest_order
        kq = segment_question_dao.insert(segment_question, db)
        if kq == -1:
            print tag + "question_dao" + "add_segment_question err"
            lastest_order -= 1
    return None


def generate_quiz(id_list, exam_id, segment_id, db):
    print "generate_quiz,  exam_id : " + exam_id + "segment_id : " + segment_id
    exam_package = 'com.tvb.qexam2'
    exam_media_list = list()
    question_list = list()
    id_question_list = id_list.split(',')

    for id in id_question_list:
        if str(id).strip() == '':
            continue
        print "id : " + str(id)
        question_item = get_question_by_id(id, db)
        question_list.append(question_item)
        # create folder named by package name
    folder_quiz_package = file_util.init_folder_quiz_package(app_constant.home_dir, app_constant.user_name,
                                                             exam_package)
    ###
    # create folder named by exam (store qz file) and media (store media file)
    ###
    #create folder named by exam
    folder_exam = os.path.join(folder_quiz_package, app_constant.folder_exam)
    file_util.create_folder_if_not_exits(folder_exam)
    #create folder name by package_name :
    folder_package = os.path.join(folder_exam, exam_package)
    file_util.create_folder_if_not_exits(folder_package)
    #create folder named by "media"
    folder_media = os.path.join(folder_quiz_package, app_constant.media_dir_name)
    file_util.create_folder_if_not_exits(folder_media)
    #file quizapp.qz to store quiz data
    # create file:

    # create file qz to store quiz:
    random_name = str(int(round(time.time() * 1000))) + ".sqlite"
    file_quiz_db = os.path.join(folder_package, random_name)

    target = open(file_quiz_db, 'a')

    conn = db_util.open_connection(file_quiz_db)

    db_util.create_tbl_exam(conn)

    db_util.create_tbl_exam_page(conn)
    db_util.create_tbl_exam_segment(conn)
    db_util.create_tbl_question(conn)
    db_util.create_tbl_question_content(conn)
    db_util.create_tbl_question_answer(conn)
    db_util.create_tbl_segment_question(conn)
    db_util.create_tbl_user_answer(conn)

    #insert into table exam :
    exam = exam_dao.get_exam_by_id(exam_id, db)
    exam.number_question = len(question_list)

    #exam = Exam()
    #exam.name = "DEMO EXAM"
    #exam.duration = 500
    #exam.number_question = len(question_list)
    exam_id = db_util.insert_exam(exam, conn)

    #insert into table exam_page
    exam_page = ExamPage()
    exam_page.exam_id = exam_id
    exam_page.page_index = 10
    db_util.insert_exam_page(exam_page, conn)

    #insert into table exam_segment
    exam_segment = exam_segment_dao.get_exam_segment_by_id(segment_id, db)
    #exam_segment.segment_name = "Segment 1"
    exam_segment.exam_id = exam_id
    exam_segment.duration = 500
    exam_segment_id = db_util.insert_exam_segment(exam_segment, conn)
    question_order = 1
    for question in question_list:
        #insert into table question_content
        if question.content_id is not None and question.content_id != 'None':
            question_content = question_content_dao.get_question_content_by_id(question.content_id, db)
            content_id = db_util.insert_question_content(question_content, conn)
            # get media list:
            media_list = media_to_html_element.get_list_source_media_object(question_content.question_content)
            exam_media_list += media_list
        else:
            content_id = None

        #insert into table question:
        question.content_id = content_id
        question.question_type = 'CL'
        question_id = db_util.insert_question(question, conn)

        #insert into table question_answer:
        question_answer_list = question_answer_dao.get_list_answer_by_question_id(question.item_id, db)
        for answer in question_answer_list:
            answer.question_id = question_id
            db_util.insert_question_answer(answer, conn)

        # insert into table segment_question
        segment_question = SegmentQuestion()
        segment_question.question_id = question_id
        segment_question.segment_id = exam_segment_id
        segment_question.question_order = question_order
        question_order += 1
        db_util.insert_segment_question(segment_question, conn)

    media_full_path = file_util.get_file_upload_by_user(exam_media_list, app_constant.user_name)

    file_util.copy_list_file(media_full_path, folder_media)


def search(db, cate_id, question_type, keyWord, has_img, has_audio, has_video, start_date, end_date):
    """
    @todo : search question by clause
    @param db:
    @param cate_id:
    @param question_type:
    @param keyWord:
    @param has_img:
    @param has_audio:
    @param has_video:
    @return:
    """
    try:
        if cate_id is not None:
            question_cate_list = category_question_dao.get_list_by_cate_id(cate_id, db)
            print 'len ' + str(len(question_cate_list))
            question_list = list()
            for question_cate in question_cate_list:
                question = get_question_by_id(question_cate.question_id, db)
                question_list.append(question)
            print 'pass'

        if question_type is not None and question_type != '':
            if 'question_list' in locals():
                question_list = [s for s in question_list if s.question_type == question_type]
            else:
                question_list = get_list_question_by_type(question_type, db)
        if 'question_list' in locals():
            if has_img is True or has_img == 'true':
                question_list = get_question_content_media(question_list, MediaObject.image_type, db)
            if has_audio is True or has_audio == 'true':
                question_list = get_question_content_media(question_list, MediaObject.audio_type, db)
            if has_video is True or has_video == 'true':
                question_list = get_question_content_media(question_list, MediaObject.video_type, db)
        else:
            question_list = get_all_question(db)
            if has_img is True or has_img == 'true':
                question_list = get_question_content_media(question_list, MediaObject.image_type, db)
            if has_audio is True or has_audio == 'true':
                question_list = get_question_content_media(question_list, MediaObject.audio_type, db)
            if has_video is True or has_video == 'true':
                question_list = get_question_content_media(question_list, MediaObject.video_type, db)

        if keyWord is not None and keyWord != '':
            if 'question_list' in locals():
                question_list = [q for q in question_list if
                                 question_content_dao.search_key_word(q.content_id, keyWord, db)]
            else:
                question_list = get_all_question(db)
                question_list = [q for q in question_list if
                                 question_content_dao.search_key_word(q.content_id, keyWord, db)]
        if start_date is not None and start_date != '':
            if 'question_list' not in locals():
                question_list = get_all_question(db)
            list_search_by_date = get_question_list_by_date(start_date, end_date, db)
            ques_ok = list()
            for ques in question_list:
                for q in list_search_by_date:
                    if ques.item_id == q.item_id:
                        ques_ok.append(ques)
            question_list = ques_ok
    except Exception as e:
        print 'search' + str(e)

    return question_list


def get_question_list_by_date(start_date, end_date, db):

    question_list = list()
    try:
        rows = db((db.clsb_question.created_on >= start_date) & (db.clsb_question.created_on <= end_date)).select()

        for question_row in rows:
            question_item = Question()
            question_item.item_id = question_row[Question.item_id_field]
            question_item.content_id = question_row[Question.content_id_field]
            question_item.mark = question_row[Question.mark_field]
            question_item.description = question_row[Question.description_field]
            question_item.difficult_level = question_row[Question.difficult_level_field]
            question_item.page_index = question_row[Question.page_index_field]
            question_item.question_guide = question_row[Question.question_guide_field]
            question_item.question_type = question_row[Question.type_field]
            question_item.explanation = question_row[Question.explanation_field]
            question_list.append(question_item)
    except Exception as e:
        print tag + ' get_question_list_by_date ' + str(e)
    return question_list


def get_all_question(db):
    question_list = list()
    rows = db(db.clsb_question).select()

    for question_row in rows:
        try:
            question_item = Question()
            question_item.item_id = question_row[Question.item_id_field]
            question_item.content_id = question_row[Question.content_id_field]
            question_item.mark = question_row[Question.mark_field]
            question_item.description = question_row[Question.description_field]
            question_item.difficult_level = question_row[Question.difficult_level_field]
            question_item.page_index = question_row[Question.page_index_field]
            question_item.question_guide = question_row[Question.question_guide_field]
            question_item.question_type = question_row[Question.type_field]
            question_item.explanation = question_row[Question.explanation_field]
            question_list.append(question_item)
        except Exception as e:
            print tag + ' get_all_question ' + str(e)
    return question_list


def get_question_content_media(question_list, media_type, db):
    """
    @todo : get question has content contain image
    @param question_list:
    @return: list question has content contain image
    """
    question_result_list = list()
    for question in question_list:
        if question.content_id is None or question.content_id == 'None':
            continue
        question_content = question_content_dao.get_question_content_by_id(question.content_id, db)
        media_list = media_to_html_element.get_media_object_list(question_content.question_content)

        if media_list is not None and len(media_list) > 0:
            for media in media_list:
                if media.item_type == media_type:
                    question_result_list.append(question)
                    break

    return question_result_list


def preview_question(question_id, db):
    """
    @return:
    """

    #if len(request.vars) < 1 or Question.item_id_field not in request.vars:
    #    return dict(error=CB_0002)
    question_info = dict()

    #question_id = request.vars[Question.item_id_field]
    try:
        question_item = get_question_by_id(question_id, db)

        # get question_content has id = question_item.content_id

        if question_item.content_id is not None:
            question_content_item = question_content_dao.get_question_content_by_id(question_item.content_id, db)
        else:
            question_content_item = None

        # get list question answer has question_id = question_item.item_id
        question_answer_list = question_answer_dao.get_list_answer_by_question_id(question_item.item_id, db)
        answer_list = answer_to_html_element.parse_list_answer_to_html(question_answer_list,
                                                                       question_item.question_type)

    except Exception as e:
        print tag + str(e)
        #return dict(error=CB_0003)
    try:
        question_info[Question.item_id_field] = question_item.item_id

        question_info[Question.type_field] = question_item.question_type
        question_info[Question.question_guide_field] = question_item.question_guide
        question_info[Question.type_field] = question_item.question_type
        question_info[Question.mark_field] = question_item.mark

        if question_content_item is not None:

            question_info[QuestionContent.question_content_field] = \
                media_to_html_element.convert_question_content_to_html(question_content_item.question_content)
        else:
            question_info[QuestionContent.question_content_field] = ""

        question_info[QuestionAnswer.question_answer_field] = answer_list

    except Exception as e:
        print "preview_question : " + str(e)
        question_info = None
    return question_info


def delete_question_pending(db):
    """
    @todo : delete all question has status = 'PENDING'
    @return:
    """
    try:
        rows = db(db.clsb_question.status == 'PENDING').select()
        for row in rows:
            db(db.clsb_question.id == row['id']).delete()
            if row['content_id'] is not None or row['content_id'] == 'None':
                db(db.clsb_question_content.id == row['content_id']).delete()
    except Exception as e:
        result = -1
        print tag + 'delete question' + str(e)
    return None


def approved_question_by_id(question_id, db):
    """
    @todo : change status from PENDING to APPROVED where id = question_id
    @param question_id:
    @return:
    """
    try:
        result = db(db.clsb_question.id == question_id).update(status="APPROVED")
    except Exception as e:
        print tag + "approved_question_by_id : " + str(e)
        result = -1
    return result


def approved_question(db):
    """
    @todo : change status from PENDING to APPROVED
    @return:
    """
    try:
        result = db(db.clsb_question).update(status="APPROVED")
    except Exception as e:
        print tag + "approved_question : " + str(e)
        result = -1
    return result


def get_question_id_list_by_exam_id(exam_id, db):
    """
    @todo : get all question in exam as list
    @param exam_id:
    @param db:
    @return:
    """
    question_list = list()
    segment_question_list = list()
    try:
        exam_segment_list = exam_segment_dao.get_list_exam_segment_by_exam_id(exam_id, db)

        for exam_segment in exam_segment_list:
            #get list segment_question

            segment_question_list_tmp = segment_question_dao.get_list_by_segment_id(exam_segment.item_id, db)

            segment_question_list += segment_question_list_tmp

        for segment_question in segment_question_list:
            question = get_question_by_id(segment_question.question_id, db)
            question_list.append(question.item_id)
    except Exception as e:
        print tag + 'get_question_list_by_exam_id' + str(e)
    return question_list


#def get_total_question_by_class(class_id, db):
#    total_question = 0
#    category_list = list()
#    question_list = list()
#    try:
#
#        cate_relation_list = category_relation_dao.get_category_relation_by_cate1(class_id, db)
#
#        if cate_relation_list is None or len(cate_relation_list) <= 0:
#            return total_question
#
#        for cate_relation in cate_relation_list:
#            cate_list_tmp = quiz_category_dao.get_list_category_by_parent_map(cate_relation.item_id, db)
#            category_list += cate_list_tmp
#
#        for category in category_list:
#            question_list_tmp = category_question_dao.get_list_by_cate_id(category.item_id, db)
#            question_list += question_list_tmp
#
#        total_question = len(question_list)
#    except Exception as e:
#        print tag + ' get_total_question_by_class ' + str(e)
#
#    return total_question


#def get_total_question_by_subject(subject_id, db):
#    total_question = 0
#    category_list = list()
#    question_list = list()
#
#    try:
#
#        cate_relation_list = category_relation_dao.get_category_relation_by_cate2(subject_id, db)
#
#        if cate_relation_list is None or len(cate_relation_list) <= 0:
#            return total_question
#
#        for cate_relation in cate_relation_list:
#            cate_list_tmp = quiz_category_dao.get_list_category_by_parent_map(cate_relation.item_id, db)
#            category_list += cate_list_tmp
#
#        for category in category_list:
#            question_list_tmp = category_question_dao.get_list_by_cate_id(category.item_id, db)
#            question_list += question_list_tmp
#
#        total_question = len(question_list)
#    except Exception as e:
#        print tag + ' get_total_question_by_class ' + str(e)
#
#    return total_question


def get_total_question_by_category(category_id, db):
    total_question = 0
    try:
        category_list = quiz_category_dao.get_all_tree_category_by_id(category_id, db)
        if len(category_list) < 1:
            question_list = category_question_dao.get_list_by_cate_id(category_id, db)
            total_question = len(question_list)
        else:
            for category in category_list:
                question_list = category_question_dao.get_list_by_cate_id(int(category.item_id), db)
                total_question += len(question_list)
    except Exception as e:
        print str(e)
    return total_question


def delete_question_by_id(item_id, db):
    try:
        question_item = get_question_by_id(item_id, db)

        result = db(db.clsb_question.id == item_id).delete()

        if question_item.content_id is not None:
            if get_list_question_by_question_content(question_item.content_id, db) == 0:
                question_content_dao.delete_question_content_by_id(question_item.content_id, db)
        #question_answer_dao.
    except Exception as e:
        print tag + str(e)
    return result


def get_list_question_by_question_content(question_content_id, db):
    try:
        rows = db(db.clsb_question.content_id == question_content_id).select()

        result = len(rows)
    except Exception as e:
        result = -1
        print tag + str(e)
    return result


def gen_quiz(id_question_list, exam_id, segment_id, db):
    #insert into table segment_question
    add_segment_question(id_question_list, exam_id, segment_id, db)

    #update value : number_question of exam
    exam_dao.update_exam_number_question(exam_id, len(id_question_list) - 1, db)
    return dict()


def get_total_point_of_list_question(question_id_list, db):

    total_point = 0
    for i in range(0, len(question_id_list)):
        question_item = get_question_by_id(question_id_list[i], db)
        total_point += question_item.mark

    return total_point
