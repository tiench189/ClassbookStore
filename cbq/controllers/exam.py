from applications.cbq.modules import cbMsb

__author__ = 'User'

from applications.cbq.modules.entities.question_entities.exam import Exam
from applications.cbq.modules.entities.question_entities.exam_segment import ExamSegment
from applications.cbq.modules.entities.question_entities.exam_page import ExamPage
from applications.cbq.modules.dao import exam_dao
from applications.cbq.modules.dao import question_content_dao
from applications.cbq.modules.dao import quiz_category_dao
from applications.cbq.modules.dao import segment_question_dao
from applications.cbq.modules.dao import question_answer_dao
from applications.cbq.modules.dao import question_dao
from applications.cbq.modules.util import file_util
from applications.cbq.modules.entities import app_constant
from applications.cbq.modules.util import db_util
from applications.cbq.modules.util import common_util
from applications.cbq.modules.util import media_to_html_element
from applications.cbq.modules.dao import exam_segment_dao
import os
import time
import shutil


def index():
    #page = request.vars['page']
    #total_record = exam_dao.count_all(db)
    #total_page = int(total_record)/20
    #if total_page == 0:
    #    total_page = 1
    #if page is None:
    #    page = 1

    if len(request.vars) > 0:
        action = request.vars['action']
        print "action: " + action

        if action is not None:
            if action == 'add':
                redirect(URL("cbq", "exam", "insert"))
                return
                #        if action == 'edit':
                #            pass
                #
        #list_exam_item = get_data_json()

    return dict()


def delete():
    if len(request.vars) < 1:
        return dict(result=cbMsb.CB_0002)

    exam_id = request.vars['exam_id']
    result = exam_dao.delete_exam(exam_id, db)
    redirect(URL("cbq", "exam", "index", host=True))
    return dict()


def get_data_json():
    exam_list = list()

    if request.vars['page'] is None:
        page = 1
    else:
        page = int(request.vars['page'])

    if request.vars['exam_name'] is not None:
        exam_name = request.vars['exam_name']
    else:
        exam_name = ""

    list_exam_item = exam_dao.get_all_exam(db, page, exam_name)
    total_record = exam_dao.count_all(db)
    total_page = int(total_record) / 10

    for exam in list_exam_item:
        item = dict()
        item[Exam.item_id_field] = exam.item_id
        item[Exam.name_field] = exam.name
        item[Exam.total_mark_field] = exam.total_mark
        item[Exam.duration_field] = exam.duration
        item[Exam.description_field] = exam.des
        item[Exam.number_question_field] = exam.number_question
        exam.print_info()
        exam_list.append(item)
    return dict(exam_list=exam_list, total_record=total_record, total_page=total_page)


def insert(): #param exam_id/exam_name/exam_type

    name = request.vars['examName']
    duration = request.vars['duration']
    des = request.vars['des']
    total_mark = request.vars['total_mark']
    total_segment = request.vars['count']
    segment_id_list = list()
    item_id = None

    if len(request.vars) > 3:

        exam = Exam()
        exam.exam_id = 12
        exam.name = name
        exam.duration = duration
        exam.des = des
        exam.total_mark = total_mark

        item_id = exam_dao.insert(exam, db)

        if item_id == -1:
            return dict(error="Lỗi insert exam")

        for i in range(0, int(total_segment)):
            segment_name_order = 'segment_name' + str(i)
            segment_des_order = 'segment_des' + str(i)
            segment_duration_order = 'segment_duration' + str(i)

            segment_name = request.vars[segment_name_order]
            print 'segment_name : ' + str(segment_name)
            segment_des = request.vars[segment_des_order]
            segment_duration = request.vars[segment_duration_order]

            #create and assign value for exam_segment object
            exam_segment = ExamSegment()
            exam_segment.segment_name = segment_name
            exam_segment.des = segment_des
            exam_segment.duration = segment_duration
            exam_segment.exam_id = item_id

            #insert
            segment_id_result = exam_segment_dao.insert(exam_segment, db)
            segment_id_list.append(segment_id_result)
    return dict(exam_id=item_id, segment_id_list=segment_id_list)


def exam_manager():
    if len(request.vars) < 1:
        return dict(error=cbMsb.CB_0002)

    exam_id = request.vars['exam_id']

    exam = exam_dao.get_exam_by_id(exam_id, db)
    exam_segment_list = exam_segment_dao.get_list_exam_segment_by_exam_id(exam_id, db)

    return dict(exam=exam, exam_segment_list=exam_segment_list)


def export_quiz():
    if len(request.vars) < 2:
        return dict(error=CB_0002)
    try:
        exam_id = request.vars['exam_id']
        exam_package = request.vars['exam_package']

        exam_media_list = list()

        exam = exam_dao.get_exam_by_id(exam_id, db)
        exam_segment_list = exam_segment_dao.get_list_exam_segment_by_exam_id(exam_id, db)

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
        if os.path.exists(folder_package):
            shutil.rmtree(folder_package)
        file_util.create_folder_if_not_exits(folder_package)
        #create folder named by "media"
        folder_media = os.path.join(folder_quiz_package, app_constant.media_dir_name)
        file_util.create_folder_if_not_exits(folder_media)
        #file quizapp.qz to store quiz data
        # create file:

        # create file qz to store quiz:
        random_name = str(int(round(time.time() * 1000))) + ".qz"
        file_quiz_db = os.path.join(folder_package, random_name)

        #open connection and create table
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
        db_util.create_tbl_score_history(conn)

        exam_id = db_util.insert_exam(exam, conn)

        exam_page = ExamPage()
        exam_page.exam_id = exam_id
        exam_page.page_index = 10
        db_util.insert_exam_page(exam_page, conn)

        for exam_segment in exam_segment_list:
            exam_segment.exam_id = exam_id
            #exam_segment.duration = 500
            exam_segment_id = db_util.insert_exam_segment(exam_segment, conn)

            segment_question_list = segment_question_dao.get_list_by_segment_id(exam_segment.item_id, db)

            for segment_question in segment_question_list:
                question = question_dao.get_question_by_id(segment_question.question_id, db)
                if question.question_type != 'PC':
                    question.question_type = 'CL'
                if question.content_id is not None and question.content_id != 'None':
                    question_content = question_content_dao.get_question_content_by_id(question.content_id, db)
                    question_content_id = db_util.insert_question_content(question_content, conn)
                    question.content_id = question_content_id

                    # get media list:
                    media_list = media_to_html_element.get_list_source_media_object(question_content.question_content)
                    exam_media_list += media_list
                else:
                    question.content_id = None
                question_id = db_util.insert_question(question, conn)
                #get answer list
                answer_list = question_answer_dao.get_list_answer_by_question_id(question.item_id, db)
                for answer in answer_list:
                    answer.question_id = question_id
                    db_util.insert_question_answer(answer, conn)

                segment_question.question_id = question_id
                segment_question.segment_id = exam_segment_id
                db_util.insert_segment_question(segment_question, conn)

        #encryption quiz
        common_util.encryption_quiz(file_quiz_db)
        if os.path.exists(file_quiz_db + "bfen"):
            os.remove(file_quiz_db + "bfen")
        media_full_path = file_util.get_file_upload_by_user(exam_media_list, app_constant.user_name)
        file_util.copy_list_file(media_full_path, folder_media)
        if os.path.exists(folder_quiz_package + ".zip"):
            os.remove(folder_quiz_package + ".zip")
        result_data = file_util.zip_dir(folder_quiz_package, folder_quiz_package + ".zip")
        url1 = URL("cbq", "download", "download_quiz", vars=dict(path=exam_package, user="admin"), host=True)

    except Exception as e:
        print 'exam.py: export_quiz' + str(e)
        return dict(result="Đã có lỗi xảy ra " + str(e))
    print str(url1)
    return dict(result=url1)


def preview_question_by_segment():
    print request.vars
    if len(request.vars) < 1:
        return dict(error=CB_0002)
    segment_id = request.vars['segment_id']
    question_preview_list = list()
    segment_question_list = segment_question_dao.get_list_by_segment_id(segment_id, db)
    for segment_question in segment_question_list:
        question_dict = question_dao.preview_question(segment_question.question_id, db)
        question_preview_list.append(question_dict)
    return dict(question_list=question_preview_list, segment_id=segment_id)


def create_exam():
    print request.vars
    return dict()


def gen_exam():
    print request.vars
    if len(request.vars) < 1:
        return dict()

    total_question = 0
    number_exam = int(request.vars['txtNumberOfExam'])
    number_segment = int(request.vars['txtNumberOfSegment'])
    duplicate = int(request.vars['duplicate'])

    segment_list = list()
    if len(request.vars) > 4:
        segment_duration_list = list()
        question_used = dict()
        list_category = list()
        list_segment_name = list()
        segment_question_list = list()
        total_exam_duration = 0
        list_exam = list()
        segment_id = None
        #get all question
        #question_list = question_dao.search(db, None, None, None, None, None, None, None, None)
        total_question_list = question_dao.search(db, None, None, None, None, None, None, None, None)

        # get number of question for each segment
        segment_vars = 'seg'
        segment_duration_vars = 'time_seg'
        segment_name_vars = 'seg_name'
        category_vars = 'category'
        for i in range(0, number_segment):
            segment_list.append(int(request.vars[segment_vars + str(i)]))
            total_question += int(request.vars[segment_vars + str(i)])
            segment_duration_list.append(int(request.vars[segment_duration_vars + str(i)]))
            total_exam_duration += int(request.vars[segment_duration_vars + str(i)])
            list_segment_name.append(request.vars[segment_name_vars + str(i)])
        for i in range(0, number_segment):
            cate_name = request.vars[category_vars + str(i)]
            category_item = quiz_category_dao.get_category_by_name(cate_name, db)
            list_category.append(category_item.item_id)
        # calculator recent duplicate
        max_occurrence = int((duplicate / total_question) * 100)
        #max_occurrence = int(duplicate/10)
        if max_occurrence == 0:
            max_occurrence = 1
        #build content for each exam
        for i in range(0, number_exam):
            exam_total_mark = 0
            exam_question_reality = 1
            #if len(total_question_list) < total_question:
            #    response.flash("So luong cau hoi khong du de tao de")
            #    return dict()

            question_used_in_exam = list()
            # create exam
            exam_item = Exam()
            exam_item.duration = total_exam_duration
            exam_item.name = 'Exam test'
            exam_item.number_question = 0
            exam_item.exam_id = 1
            exam_id = exam_dao.insert(exam_item, db)

            for j in range(0, number_segment):

                question_list = question_dao.search(db, list_category[j], None, None, None, None, None, None, None)
                # lay danh sach cau hoi hop le (xuat hien qua so lan va da xuat hien trong exam?:
                question_list_can_use = exam_dao.check_to_delete_question_invalid(question_used, question_list, max_occurrence, question_used_in_exam, j ,segment_question_list)
                if len(question_list_can_use) < segment_list[j]:
                    exam_data = dict()
                    exam_data['NumberOfExam'] = number_exam
                    exam_data['NumberOfSegment'] = number_segment
                    exam_data['duplicate'] = duplicate
                    exam_data['result'] = 'Không đủ dữ liệu để tạo đề, đã tạo xong ' + str(i) + 'đề.'
                    return dict(exam_data=exam_data)

                segment_list_question = list()
                for t in range(0, segment_list[j]):
                    question_selected = exam_dao.get_invalid_question(question_used_in_exam, question_list_can_use,
                                                                      max_occurrence, question_used,
                                                                      segment_question_list, j)
                    if question_selected is not None:
                        question_used_in_exam.append(question_selected.item_id)
                        segment_list_question.append(question_selected.item_id)
                        segment_question_list.append(str(j) + "_" + str(question_selected.item_id))
                        if question_used.get(question_selected.item_id) is not None:
                            question_used[question_selected.item_id] += 1
                        else:
                            question_used[question_selected.item_id] = 1

                        # check question appears max times
                        #if exam_dao.check_to_delete_question(question_used, question_selected, max_occurrence,
                        #
                        if question_selected in question_list_can_use: question_list_can_use.remove(question_selected)
                        #question_list_can_use = question_list_can_use.remove(question_selected)
                            #if question_selected in question_list_can_use: question_list_can_use = question_list_can_use.remove(
                            #    question_selected)
                    elif question_selected == -1:
                        response.flash('Ngân hàng câu hỏi đã hết, vui lòng thử lại sau')
                        return dict(error='Ngân hàng câu hỏi đã hết, vui lòng thử lại sau')
                #calculate total mark in segment
                total_mark = question_dao.get_total_point_of_list_question(segment_list_question, db)
                exam_total_mark += total_mark
                exam_question_reality += len(segment_list_question)
                #create segment
                segment = ExamSegment()
                segment.duration = segment_duration_list[j]
                segment.exam_id = exam_id
                segment.exam_segment_order = (j+1)
                segment.segment_name = list_segment_name[j]
                segment.segment_mark = total_mark
                segment_id = exam_segment_dao.insert(segment, db)
                question_dao.gen_quiz(segment_list_question, exam_id, segment_id, db)
            exam_dao.update_exam_total_mark(exam_id, exam_total_mark, db)
            exam_dao.update_exam_number_question(exam_id, exam_question_reality, db)
    exam_data = dict()
    exam_data['NumberOfExam'] = number_exam
    exam_data['NumberOfSegment'] = number_segment
    exam_data['duplicate'] = duplicate
    exam_data['result'] = ''

    return dict(exam_data=exam_data)


#def export_all_exam():
#    exam_list = exam_dao.get_all_exam(db)
#
#    for i in range(0, len(exam_list)):
#        exam_id = exam_list[i].item_id
#        package_name = 'com.tvb.qexam' + str(i)
#        export_all_quiz(exam_id, package_name)
#
#    return dict()


def export_all_quiz(exam_id, exam_package):

    try:
        #exam_id = request.vars['exam_id']
        #exam_package = request.vars['exam_package']

        exam_media_list = list()

        exam = exam_dao.get_exam_by_id(exam_id, db)
        exam_segment_list = exam_segment_dao.get_list_exam_segment_by_exam_id(exam_id, db)

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
        if os.path.exists(folder_package):
            shutil.rmtree(folder_package)
        file_util.create_folder_if_not_exits(folder_package)
        #create folder named by "media"
        folder_media = os.path.join(folder_quiz_package, app_constant.media_dir_name)
        file_util.create_folder_if_not_exits(folder_media)
        #file quizapp.qz to store quiz data
        # create file:

        # create file qz to store quiz:
        random_name = str(int(round(time.time() * 1000))) + ".qz"
        file_quiz_db = os.path.join(folder_package, random_name)

        #open connection and create table
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

        exam_id = db_util.insert_exam(exam, conn)

        exam_page = ExamPage()
        exam_page.exam_id = exam_id
        exam_page.page_index = 10
        db_util.insert_exam_page(exam_page, conn)

        for exam_segment in exam_segment_list:
            exam_segment.exam_id = exam_id
            #exam_segment.duration = 500
            exam_segment_id = db_util.insert_exam_segment(exam_segment, conn)

            segment_question_list = segment_question_dao.get_list_by_segment_id(exam_segment.item_id, db)

            for segment_question in segment_question_list:
                question = question_dao.get_question_by_id(segment_question.question_id, db)
                if question.question_type != 'PC':
                    question.question_type = 'CL'
                if question.content_id is not None and question.content_id != 'None':
                    question_content = question_content_dao.get_question_content_by_id(question.content_id, db)
                    question_content_id = db_util.insert_question_content(question_content, conn)
                    question.content_id = question_content_id

                    # get media list:
                    media_list = media_to_html_element.get_list_source_media_object(question_content.question_content)
                    exam_media_list += media_list
                else:
                    question.content_id = None
                question_id = db_util.insert_question(question, conn)
                #get answer list
                answer_list = question_answer_dao.get_list_answer_by_question_id(question.item_id, db)
                for answer in answer_list:
                    answer.question_id = question_id
                    db_util.insert_question_answer(answer, conn)

                segment_question.question_id = question_id
                segment_question.segment_id = exam_segment_id
                db_util.insert_segment_question(segment_question, conn)

        #encryption quiz
        common_util.encryption_quiz(file_quiz_db)
        if os.path.exists(file_quiz_db + "bfen"):
            os.remove(file_quiz_db + "bfen")
        media_full_path = file_util.get_file_upload_by_user(exam_media_list, app_constant.user_name)
        file_util.copy_list_file(media_full_path, folder_media)
        if os.path.exists(folder_quiz_package + ".zip"):
            os.remove(folder_quiz_package + ".zip")
        result_data = file_util.zip_dir(folder_quiz_package, folder_quiz_package + ".zip")
        url1 = URL("cbq", "download", "download_quiz", vars=dict(path=exam_package, user="admin"), host=True)

    except Exception as e:
        print 'exam.py: export_quiz' + str(e)
        return dict(result="Đã có lỗi xảy ra " + str(e))
    #print str(url1)
    return dict(result=url1)


def build_apk_file():
    package_name = 'com.tvb.qexam10'
    app_name = 'ung_dung_test'


