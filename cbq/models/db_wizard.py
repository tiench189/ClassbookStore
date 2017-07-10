'''
Created on Oct 30, 2013

@author: PhuongNH
'''
# table clsb_category
db.define_table('clsb_quiz_category',
                Field('category_code', type='string', notnull=True,
                      label=T('Category code')),
                Field('category_name', type='string', notnull=True,
                      label=T('Category name')),
                Field('description', type='string', label=T('Description')),
                Field('parent_id', type='reference clsb_quiz_category',
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb_quiz_category.id', '%(category_name)s')),
                      label=T('Parent id')),
                Field('parent_map', type='reference clsb_category_relation.id', label=T('Parent mapping')),
                Field('category_level', type='string', label=T('Category level')),
                format='%(category_name)s')
db.clsb_quiz_category._singular = 'Category'
db.clsb_quiz_category._plural = 'Categories'

db.define_table('clsb_category_relation',
                Field('category_first', type='reference clsb_quiz_category', notnull=True, label=T('Category first')),
                Field('category_second', type='reference clsb_quiz_category', notnull=True, label=T('Category second')),
                Field('parent_id', type='reference clsb_category_relation',
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb_category_relation.id', '%(id)s')),
                      label=T('Parent id')))

# table clsb_question_content
db.define_table('clsb_question_content',
                Field('content_id', type='string', notnull=False, unique=False, label=T('Content id')),
                Field('question_content', type='text', notnull=False, label=T('Question content')),
                Field('description', type='string', label=T('Description')),
                Field('question_type', type='string', label=T('Question type')))
db.clsb_question_content._singular = 'Question content'
db.clsb_question_content._plural = 'Question contents'

from datetime import datetime
#table question
db.define_table('clsb_question',
                Field('content_id', type='reference clsb_question_content', notnull=False,
                      label=T('Content id')),
                Field('mark', type='double', notnull=True, label=T('Mark')),
                Field('question_type', type='string', label=T('Type')),
                Field('difficult_level', type='integer', label=T('Difficult level')),
                Field('question_guide', type='text', label=T('Question guide')),
                Field('description', type='string', label=T('Description')),
                Field('question_title', type='string', label=T('Question title')),
                Field('page_index', type='integer', label=T('Page index')),
                Field('explanation', type='string', label=T('explanation')),
                Field('status', type='string', default='PENDING', label=T('Status')),
                Field('created_on', type='datetime', writable=False, default=datetime.now(),
                      label=T('Created On')),
                format='%(id)s')
db.clsb_question._singular = 'Question'
db.clsb_question._plural = 'Questions'

#table question_answer
db.define_table('clsb_question_answer',
                Field('question_id', type='reference clsb_question', notnull=True,
                      label=T('Question id')),
                Field('question_answer', type='text', notnull=True, label=T('Question answer')),
                Field('mark_percent', type='integer', label=T('Mark percent')),
                Field('sign_mark', type='string', label=T('Sign mark')),
                Field('is_correct', type='boolean', label=T('Is correct')),
                Field('explanation', type='text', label=T('explanation')),
                format='%(question_answer)s')
db.clsb_question_answer._singular = 'Question answer'
db.clsb_question_answer._plural = 'Question answers'

# table category_question
db.define_table('clsb_category_question',
                Field('category_id', type='reference clsb_quiz_category', notnull=True, label='Category id'),
                Field('question_id', type='reference clsb_question', notnull=True, label='Question id'))
db.clsb_category_question._singular = 'Category question'
db.clsb_category_question._plural = 'Category questions'

## table exam
db.define_table('clsb_exam',
                Field('exam_id', type='integer', notnull=True, label=T('Exam id')),
                Field('name', type='string', label=T('Name')),
                Field('exam_type', type='string', label=T('Exam type')),
                Field('des', type='string', label=T('Description')),
                Field('duration', type='integer', label=T('Duration')),
                Field('number_question', type='integer', label=T('Number question')),
                Field('cover', type='string', label=T('Cover image')),
                Field('total_mark', type='integer', label=T('Total mark')),
                Field('exam_mode', type='string', label=T('Mode')),
                format='%(name)s')
db.clsb_exam._singular = 'Exam'
db.clsb_exam._plural = 'Exams'
#
##table exam page
db.define_table('clsb_exam_page',
                Field('exam_page_id', type='integer', notnull=True, label=T('Exam page id')),
                Field('exam_id', type='reference clsb_exam', notnull=True, label=T('Exam id'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb_exam.id', '%(exam_name)s'))),
                Field('page_index', type='integer', notnull=True, label=T('Page index')))
db.clsb_exam_page._singular = 'Exam page'
db.clsb_exam_page._plural = 'Exams page'
#
##table exam_segment
db.define_table('clsb_exam_segment',
                Field('segment_id', type='integer', label=T('Segment id')),
                Field('exam_id', type='reference clsb_exam', notnull=True, label=T('Exam id'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb_exam.id', '%(name)s'))),
                Field('segment_name', type='string', label=T('Segment name')),
                Field('des', type='string', label=T('Description')),
                Field('duration', type='integer', label=T('Duration')),
                Field('segment_mark', type='integer', label=T('Segment mark')),
                Field('exam_segment_order', type='integer', label=T('Order')))
db.clsb_exam_segment._singular = 'Exam segment'
db.clsb_exam_segment._plural = 'Exams segment'
#
##table segment_question
db.define_table('clsb_segment_question',
                Field('segment_id', type='reference clsb_exam_segment', notnull=True, label=T('Segment id'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb_exam_segment.segment_id', '%(segment_name)s'))),
                Field('question_id', type='reference clsb_question', notnull=True, label=T('Question id'),
                      requires=IS_EMPTY_OR(IS_IN_DB(db, 'clsb_question.id', '%(id)s'))),
                Field('segment_question_order', type='integer', notnull=True, label=T('Order')))
db.clsb_segment_question._singular = 'Segment question'
db.clsb_segment_question._plural = 'Segments question'

from applications.cbq.controllers.plugin_uploadify_widget import (
    uploadify_widget, IS_UPLOADIFY_IMAGE, IS_UPLOADIFY_FILENAME, IS_UPLOADIFY_LENGTH
    )
#from applications.cbq.controllers.plugin_notemptymarker import mark_not_empty, unmark_not_empty
import uuid

table = db.define_table('plugin_uploadify_widget',
                        Field('name', default=str(uuid.uuid4())),
                        Field('image', 'upload', autodelete=True, comment='<- upload an image file(max file size=10k)'),
                        Field('des', 'upload', autodelete=True, comment='<- upload a txt file (max file size=1k)'),
)
################################ The core ######################################
# Inject the uploadify widget
# The "requires" needs custom validators.
#table.image.widget = uploadify_widget
#table.image.requires = [IS_UPLOADIFY_LENGTH(10240, 1), IS_UPLOADIFY_IMAGE()]
## Inject the another uploadify widget with different requires
#table.des.widget = uploadify_widget
#table.des.requires = IS_EMPTY_OR([IS_UPLOADIFY_FILENAME(extension='txt'),
#                                          IS_UPLOADIFY_LENGTH(1024)])

db.define_table('product_demo', Field('description', 'text'))

# define an image table using disk db
image_table = db.define_table('plugin_elrte_widget_image',
                              Field('image', 'upload', autodelete=True,
                                    comment='<- upload an image (max file size=10k)')
)
image_table.image.widget = uploadify_widget
image_table.image.requires = [IS_UPLOADIFY_LENGTH(10240, 1), IS_UPLOADIFY_IMAGE()]

file_table = db.define_table('plugin_elrte_widget_file',
                             Field('name'),
                             Field('file_widget', 'upload', autodelete=True,
                                   comment='<- upload a file(max file size=100k)')
)
file_table.file_widget.widget = uploadify_widget
file_table.file_widget.requires = IS_UPLOADIFY_LENGTH(102400, 1)