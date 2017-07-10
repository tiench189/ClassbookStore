# -*- coding: utf-8 -*-
__author__ = 'PhuongNH'

import random
from applications.cbq.modules.dao import question_dao
from applications.cbq.modules.dao import exam_dao
from applications.cbq.modules.dao import exam_segment_dao
from applications.cbq.modules.dao import question_content_dao
from applications.cbq.modules.dao import quiz_category_dao
from applications.cbq.modules.dao import question_answer_dao
from applications.cbq.modules.entities import app_constant
from applications.cbq.modules.entities.json_entities.json_content import ContentAttr
from applications.cbq.modules.entities.question_entities.question import Question
from applications.cbq.modules.entities.question_entities.question_content import QuestionContent
from applications.cbq.modules.entities.question_entities.question_answer import QuestionAnswer
from applications.cbq.modules.entities.question_entities.exam_segment import ExamSegment
from applications.cbq.modules.util import content_util


question_request = ('item_id', 'content_id', 'mark', 'type', 'difficult_level', 'question_guide', 'description',
                    'question_title', 'explanation', 'page_index')


def index():
    if request.vars is not None and len(request.vars) >= 1:
        exam_id = request.vars['exam_id']
        segment_id = request.vars['segment_id']
        class_id = request.vars['class_id']
        subject_id = request.vars['subject_id']
        category_id = request.vars['cate_id']

        print request.vars
        if segment_id is None:
            segment_id_list = exam_segment_dao.get_list_exam_segment_by_exam_id(exam_id, db)
            print 'passs'
            if segment_id_list is None or len(segment_id_list) < 1:
                segment = ExamSegment()
                segment.exam_id = exam_id
                segment.segment_name = "Segment mặc định"
                segment.exam_segment_order = 1
                segment_id = exam_segment_dao.insert(segment, db)
            else:
                segment_id = segment_id_list[0].item_id
    else:
        exam_id = None
        segment_id = None
        class_id = None
        subject_id = None
        category_id = None
    return dict(exam_id=exam_id, segment_id=segment_id, class_id=class_id, subject_id=subject_id, cate_id=category_id)


def get_list_question_preview():
    question_dict_list = list()
    if request.vars['page'] is None:
        page = 1
    else:
        page = int(request.vars['page'])

    exam_id = request.vars['exam_id']

    question_list = question_dao.get_all_record(db, page)
    total_record = question_dao.count_all(db)
    total_page = int(total_record) / 20

    question_list_in_exam = question_dao.get_question_id_list_by_exam_id(exam_id, db)

    question_list_ok = [question for question in question_list if question.item_id not in question_list_in_exam]

    for question in question_list_ok:
        question_dict = question_dao.preview_question(question.item_id, db)
        if question_dict is not None:
            question_dict_list.append(question_dict)

    return dict(question_list=question_dict_list, total_page=total_page, total_record=total_record)


def list_question():
    return dict()


def insert():
    """
        insert new question to table clsb_question
        param :content_id/mark/type/difficult_level/question_guide/description
                                /question_title/page_index/explanation
    """
    if len(request.vars) < 5:
        return dict(mess=CB_0002)
    print request.vars
    if 'category_id' in request.vars:
        cate_id = int(request.vars['category_id'])
    question_item = Question()
    for re in request.vars:
        print str(re)
        if re == Question.content_id_field:
            question_item.content_id = request.vars[Question.content_id_field]
        elif re == Question.description_field:
            question_item.description = request.vars[Question.description_field]
        elif re == Question.difficult_level_field:
            question_item.difficult_level = request.vars[Question.difficult_level_field]
        elif re == Question.explanation_field:
            question_item.explanation = request.vars[Question.explanation_field]
            print 'question explanation ' + str(request.vars[Question.explanation_field])
        elif re == Question.mark_field:
            question_item.mark = request.vars[Question.mark_field]
        elif re == Question.page_index_field:
            question_item.page_index = request.vars[Question.page_index_field]
        elif re == Question.question_guide_field:
            question_item.question_guide = request.vars[Question.question_guide_field]
        elif re == Question.question_title_field:
            question_item.question_title = request.vars[Question.question_title_field]
        elif re == Question.type_field:
            question_item.question_type = request.vars[Question.type_field]
    try:
        result = question_dao.insert_data(question_item, cate_id, db)
    except Exception as e:
        print str(e)
        return dict(mess=CB_0003)

    return dict(result=result)


def get_question_by_id():
    """ return question
        get question by question_id
    """
    question_item = dict()
    try:
        if len(request.vars) < 1 or Question.item_id_field not in request.vars:
            return dict(mess=CB_0002)

        question_id = request.vars['id']

        question_result = question_dao.get_question_by_id(question_id, db)
        #question_result = Question(question_result)
        question_item['item_id'] = question_result.item_id
        question_item['content_id'] = question_result.content_id

        question_item['mark'] = question_result.mark
        question_item['question_type'] = question_result.question_type
        question_item['question_guide'] = question_result.question_guide
        question_item['description'] = question_result.description
        question_item['difficult_level'] = question_result.difficult_level
        question_item['question_title'] = question_result.question_title
        question_item['page_index'] = question_result.page_index
        question_item['explanation'] = question_result.explanation
    except:
        print "get_question_by_id error"
        return dict(error=CB_0003)
    return dict(question=question_item)


def preview():
    question_id = request.vars['id']
    question_info = question_dao.preview_question(question_id, db)
    print str(question_info)
    return dict(question=question_info)


def gen_random_list_question():
    random_array = list()
    print request.vars
    question_random_list = list()
    number_question = request.vars['count']
    cate_name = request.vars['cate_id']
    question_type = request.vars['question_type']
    has_img = request.vars['hasImg']
    has_audio = request.vars['hasAudio']
    has_video = request.vars['hasVideo']
    key_word = request.vars['keyWord']
    exam_id = request.vars['exam_id']
    page = int(request.vars['page'])
    difficult_level = int(request.vars['difficult_level'])
    start_date = request.vars['start_date']
    end_date = request.vars['end_date']

    try_random = 1
    max_record = page * int(app_constant.item_per_page)
    min_record = (page - 1) * int(app_constant.item_per_page)
    cate_id = None

    if cate_name is not None and cate_name != '':
        category_item = quiz_category_dao.get_category_by_name(cate_name, db)
        cate_id = category_item.item_id

    question_list = question_dao.search(db, cate_id, question_type, key_word, has_img, has_audio, has_video, start_date,
                                        end_date)

    if exam_id is not None:
        question_list_in_exam = question_dao.get_question_id_list_by_exam_id(exam_id, db)
    else:
        question_list_in_exam = list()

    try:
        question_list_ok = [question for question in question_list if question.item_id not in question_list_in_exam]

        question_list_ok = [question for question in question_list_ok if question.difficult_level == difficult_level]
        print 'ket qua: '  + str(len(question_list_ok))
        if int(number_question) >= len(question_list_ok):
            for question in question_list_ok:
                question_dict = question_dao.preview_question(question.item_id, db)
                question_random_list.append(question_dict)
        else:
            if max_record >= len(question_list):
                max_record = len(question_list)
                number_question = max_record - int(number_question)
            for i in range(0, int(number_question)):

                ran_index = random.randint(min_record, max_record - 1)
                while ran_index in random_array:
                    if try_random == 10:
                        break
                    try_random += 1
                    ran_index = random.randint(min_record, max_record - 1)
                if try_random < 10:
                    random_array.append(ran_index)
                    question = question_list[ran_index]
                    question_dict = question_dao.preview_question(question.item_id, db)
                    question_random_list.append(question_dict)
                    try_random = 1
    except Exception as e:
        print 'gen_random_list_question ' + str(e)

    return dict(question_list=question_random_list)


def generate_quiz():
    id_list = request.vars['id_list']
    exam_id = request.vars['exam_id']
    segment_id = request.vars['segment_id']
    segment_id_continue = None
    flag = 0
    try:
        id_question_list = id_list.split(',')
        question_dao.gen_quiz(id_question_list, exam_id, segment_id, db)
        ##insert into table segment_question
        #question_dao.add_segment_question(id_list, exam_id, segment_id, db)
        #
        ##update value : number_question of exam
        #id_question_list = id_list.split(',')
        #exam_dao.update_exam_number_question(exam_id, len(id_question_list) - 1, db)
        segment_list = exam_segment_dao.get_list_exam_segment_by_exam_id(exam_id, db)

        for seg in segment_list:
            if flag == 1:
                segment_id_continue = seg.item_id
            if seg.item_id == int(segment_id):
                flag = 1

        if segment_id_continue is None:
            segment_id_continue = -1
    except Exception as e:
        print "generate_quiz" + str(e)
        return dict(result=-1)
    return dict(result=segment_id_continue)


def delete_question_pending():
    try:
        result = question_dao.delete_question_pending(db)
        if result == -1:
            return dict(result=CB_0003)
    except Exception as e:
        print str(e)
        return dict(result=CB_0003)
    return dict(result=CB_0000)


def delete_question():

    id_list = request.vars['question_id_arr']
    id_question_list = id_list.split(',')
    try:
        for question_id in id_question_list:
            if question_id is None or question_id == '':
                continue
            question_dao.delete_question_by_id(question_id, db)
    except Exception as e:
        print str(e)
    return dict(result=len(id_question_list))



def approved_question():
    try:
        result = question_dao.approved_question(db)
    except Exception as e:
        print str(e)
        return dict(result=CB_0003)
    return dict(result=result)


def edit():
    if len(request.vars) < 1:
        return dict(result=CB_0002)
    question_id = request.vars['id']

    question_info = question_dao.preview_question(question_id, db)

    return dict(question=question_info)


def create1():
    if len(request.vars) < 3:
        return dict(result=CB_0002)

    print request.vars

    answer_list_tmp = list()
    answer_list = list()
    question_guide = request.vars['question_guide']
    question_content = request.vars['question_content']
    question_info = request.vars['question_info']
    number_answer = request.vars['count']

    if number_answer is None:
        number_answer = 0

    try:
        for i in range(0, int(number_answer)):
            ans_content = 'txt_ans' + str(i + 1)
            rdb_ans = 'rdb_ans' + str(i + 1)
            if rdb_ans in request.vars:
                is_correct = True
            else:
                is_correct = False
            if request.vars[ans_content] is None or request.vars[ans_content] == '':
                continue
            answer = ContentAttr()
            answer.value = request.vars[ans_content]
            answer.is_correct = is_correct
            if is_correct:
                answer.mark = 1
            else:
                answer.mark = 0
            answer_list_tmp.append(answer)

        # init object question_content
        if str(question_content).strip() != '':
            qContent = QuestionContent()
            print 'qContent: ' + question_content
            qContent.question_content = content_util.parse_question_content(question_content)
            qContent.question_type = 'MC'

        #init object question
        question = Question()
        question.question_guide = question_guide
        question.explanation = question_info
        question.question_type = 'MC'
        question.mark = 1

        # init object question_answer
        for ans_tmp in answer_list_tmp:
            ans = QuestionAnswer()
            ans.is_correct = ans_tmp.is_correct
            ans.mark_percent = ans_tmp.mark
            ans.question_answer = ans_tmp.value
            answer_list.append(ans)
            ######################################
        #insert into database
        ######################################

        if str(question_content).strip() != '':
            content_id = question_content_dao.insert_data(qContent, db)
        else:
            content_id = None
            #insert question
        question.content_id = content_id
        question_id = question_dao.insert_data(question, 23, db)

        #insert question_answer
        if int(question_id) > -1:
            for ques_ans in answer_list:
                ques_ans.question_id = question_id
                question_answer_dao.insert_data(ques_ans, db)
    except Exception as e:
        print str(e)
    return dict(result='success')


def create():
    def image_upload_or_choose():

        try:
            form = SQLFORM(db.plugin_elrte_widget_image, upload=URL('download'))
            info = ''
            if form.accepts(request.vars, session):
                img_file = request.vars['image']
                #download_img_from_url()
            records = db(db.plugin_elrte_widget_image.id > 0).select(orderby=~db.plugin_elrte_widget_image.id)
            _get_src = lambda r: URL(request.controller, 'download', args=r.image)
            records = DIV([IMG(_src=_get_src(r),
                               _onclick="""
    jQuery.data(document.body, 'elrte_callback')('%s');jQuery('.dialog').hide(); return false;
    """ % _get_src(r), _style='max-width:100px;max-height:100px;margin:5px;cursor:pointer;')
                           for r in records])
            return BEAUTIFY(dict(form=form, records=records))
        except Exception as e:
            print str(e)


def file_upload_or_choose():
    form = SQLFORM(db.plugin_elrte_widget_file, upload=URL('download'))
    info = ''
    if form.accepts(request.vars, session):
        info = 'submitted %s' % form.vars

    def _get_icon(v):
        ext = v.split('.')[-1]
        if ext in ('pdf',):
            filename = 'icon_pdf.gif'
        elif ext in ('doc', 'docx', 'rst'):
            filename = 'icon_doc.gif'
        elif ext in ('xls', 'xlsx'):
            filename = 'icon_xls.gif'
        elif ext in ('ppt', 'pptx', 'pps'):
            filename = 'icon_pps.gif'
        elif ext in ('jpg', 'gif', 'png', 'bmp', 'svg', 'eps'):
            filename = 'icon_pic.gif'
        elif ext in ('swf', 'fla'):
            filename = 'icon_flash.gif'
        elif ext in ('mp3', 'wav', 'ogg', 'wma', 'm4a'):
            filename = 'icon_music.gif'
        elif ext in ('mov', 'wmv', 'mp4', 'api', 'mpg', 'flv'):
            filename = 'icon_film.gif'
        elif ext in ('zip', 'rar', 'gzip', 'bzip', 'ace', 'gz'):
            filename = 'icon_archive.gif'
        else:
            filename = 'icon_txt.gif'
        return IMG(_src=URL('static', 'plugin_elrte_widget/custom/icons/%s' % filename),
                   _style='cursor:pointer;margin-right:5px;')

    records = db(db.plugin_elrte_widget_file.id > 0).select(orderby=~db.plugin_elrte_widget_file.id)
    records = DIV([DIV(A(_get_icon(r.file), r.name, _href='#', _onclick="""
jQuery.data(document.body, 'elrte_callback')('%s');jQuery('.dialog').hide(); return false;
""" % A(_get_icon(r.file), r.name, _href=URL(request.controller, 'download', args=r.file)).xml()),
                       _style='margin-bottom:5px;') for r in records])

    return BEAUTIFY(dict(form=form, records=records))


def download():
    return response.download(request, db)


def get_total_question_by_class():
    if len(request.vars) < 1:
        return dict(result=CB_0002)

    class_id = request.vars['class_id']
    try:
        number_question = question_dao.get_total_question_by_class(class_id, db)
    except Exception as e:
        number_question = 0
        print str(e)
    return dict(total_question=number_question)


def get_total_question_by_subject():
    if len(request.vars) < 1:
        return dict(totalquestion=0)

    subject_id = request.vars['subject_id']
    try:
        number_question = question_dao.get_total_question_by_subject(subject_id, db)
    except Exception as e:
        number_question = 0
        print str(e)

    return dict(total_question=number_question)


def get_total_question_by_category():
    if len(request.vars) < 1:
        return dict(total_question=0)

    category_id = request.vars['category_id']
    try:
        total_question = question_dao.get_total_question_by_category(category_id, db)
    except Exception as e:
        total_question = 0
        print str(e)

    return dict(total_question=total_question)



