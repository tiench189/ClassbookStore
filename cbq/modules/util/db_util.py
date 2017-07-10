# -*- coding: utf-8 -*-
__author__ = 'User'

import sqlite3 as lite
import sys

tag = 'db_util'
con = None


def open_connection(sqlite_file):
    """
    @todo open connection to sqlite_file
    @param sqlite_file:
    @return:
    """
    global con
    try:
        con = lite.connect(str(sqlite_file))
        con.text_factory = str
    except:
        con = None
    return con


def close_connection(connection):
    if connection:
        con.close()


def create_tbl_exam(conn):
    """
    @todo : create table exam named tbl_exam
    @return:
    """

    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE exam (exam_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE ,"
                    " name TEXT, des TEXT, type TEXT, duration INTEGER, number_question INTEGER,"
                    " cover TEXT, total_mark REAL, mode TEXT)")
        conn.commit()
    except lite.Error, e:
        print "err : " + str(e)
        if conn:
            conn.rollback()

        print tag + "Error %s:" % e.args[0]
        sys.exit(1)
    return None


def create_tbl_exam_page(conn):
    """
    @todo : create table named tbl_exam_page
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute("CREATE TABLE exam_page (id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,"
                    " exam_id INTEGER NOT NULL , page_index INTEGER NOT NULL )")
        conn.commit()
    except lite.Error, e:
        if conn:
            conn.rollback()

        print tag + "Error %s:" % e.args[0]
        sys.exit(1)
    return None


def create_tbl_exam_segment(conn):
    """
    @todo : create table named : exam_segment
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE exam_segment (segment_id INTEGER PRIMARY KEY AUTOINCREMENT  NOT NULL ,"
            "exam_id  INTEGER,segment_name TEXT,des TEXT,segment_mark REAL,"
            "segment_duration INTEGER,segment_order INTEGER DEFAULT (1) )")
        conn.commit()
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + "Error %s:" % e.args[0]
        sys.exit(1)
    return None


def create_tbl_segment_question(conn):
    """
    @todo : create table named : segment_question
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE segment_question (id INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL ,"
            "segment_id INTEGER NOT NULL , question_id INTEGER NOT NULL , "
            "question_order INTEGER DEFAULT (0) )")
        conn.commit()

    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + "Error %s:" % e.args[0]
        sys.exit(1)
    return None


def create_tbl_score_history(conn):
    """
    @todo : create table named : score_history
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            'CREATE TABLE "score_history" ("examid" INTEGER, "date_time" TEXT, "score_history" TEXT)'
        )
        conn.commit()

    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + "Error %s:" % e.args[0]
        sys.exit(1)
    return None


def create_tbl_question(conn):
    """
    @todo : create table named : question
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE question (question_id INTEGER  PRIMARY KEY  AUTOINCREMENT  NOT NULL  UNIQUE ,"
            "content_id TEXT,mark REAL,type TEXT,difficult_level INTEGER,question_guide TEXT DEFAULT (null) ,"
            "des TEXT, explaination TEXT,question_title VARCHAR,page_index INTEGER)")
        conn.commit()

    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + "Error %s:" % e.args[0]
        sys.exit(1)
    return None


def create_tbl_question_answer(conn):
    """
    @todo : create table named : question_answer
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE question_answer (answer_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL ,"
            "question_id INTEGER, question_answer TEXT, mark_percent INTEGER, "
            "sign_mark TEXT, is_correct BOOL, explaination TEXT)")
        con.commit()

    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + "Error %s:" % e.args[0]
        sys.exit(1)
    return None


def create_tbl_question_content(conn):
    """
    @todo : create table named : question_answer
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE question_content (content_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, "
            "content TEXT, des TEXT, type TEXT)")
        conn.commit()

    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + "Error %s:" % e.args[0]
        sys.exit(1)
    return None


def create_tbl_user_answer(conn):
    """
    @todo : create table named : question_answer
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "CREATE TABLE user_answer (exam_id INTEGER ,  question_id INTEGER ,"
            "answer_id INTEGER ,fill_value TEXT , sign_mark TEXT )")
        conn.commit()
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + " create_tbl_user_answer : Error %s:" % e.args[0]
        #sys.exit(1)
    return None


def insert_exam(exam, conn):
    """
    @todo : insert data into table exam
    @param exam:
    @return:
    """
    exam.print_info()
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO exam (name, des, type, duration, number_question, cover, total_mark, mode)"
            " values (?,?,?,?,?,?,?,?)", (
                exam.name, exam.des, exam.exam_type, exam.duration, exam.number_question, exam.cover,
                exam.total_mark, exam.exam_mode))
        conn.commit()
        result = cur.lastrowid
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + " insert_exam: Error %s:" % e.args[0]
        #sys.exit(1)
        result = -1
    return result


def insert_exam_page(exam_page, conn):
    """
    @todo : insert data into table exam_page
    @param exam_page:
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO exam_page ( exam_id, page_index) values (?, ?)", (exam_page.exam_id, exam_page.page_index))
        conn.commit()
        result = cur.lastrowid
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + " insert_exam_page: Error %s:" % e.args[0]
        #sys.exit(1)
        result = -1
    return result


def insert_exam_segment(exam_segment, conn):
    """
    @todo : insert data into table exam_segment
    @param exam_segment:
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO exam_segment (exam_id, segment_name, des, segment_duration,  segment_mark, segment_order)'
            ' values ( ?, ?, ?, ?, ?, ?)',
            (exam_segment.exam_id, exam_segment.segment_name, exam_segment.des,
             exam_segment.duration, exam_segment.segment_mark, exam_segment.exam_segment_order))
        conn.commit()
        result = cur.lastrowid
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + " insert_exam_segment: Error %s:" % e.args[0]
        #sys.exit(1)
        result = -1
    return result


def insert_segment_question(segment_question, conn):
    """
    @todo : insert data into table segment_question
    @param segment_question:
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO segment_question (segment_id, question_id, question_order)'
            ' values (?, ?, ?)',
            (segment_question.segment_id, segment_question.question_id, segment_question.question_order))
        conn.commit()
        result = cur.lastrowid
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + " insert_segment_question: Error %s:" % e.args[0]
        #sys.exit(1)
        result = -1
    return result


def insert_question_content(question_content, conn):
    """
    @todo : insert data into table question_content
    @param question_content:
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO question_content '
            '( content, des, type) values (?, ?, ?)',
            (question_content.question_content, question_content.description, question_content.question_type))
        conn.commit()
        result = cur.lastrowid
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + "insert_question_content: Error %s:" % e.args[0]
        #sys.exit(1)
        result = -1
    return result


def insert_question(question, conn):
    """
    @todo : insert data into table question
    @param question:
    @return:
    """
    question.print_info()
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO question '
            '( content_id, mark, type, difficult_level, question_guide, des, explaination, question_title, page_index)'
            ' values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (question.content_id, question.mark, question.question_type, question.difficult_level
             , question.question_guide, question.description, question.explanation, question.question_title,
             question.page_index))

        conn.commit()
        result = cur.lastrowid
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + "insert_question : Error %s:" % e.args[0]
        #sys.exit(1)
        result = -1
    return result


def insert_question_answer(question_answer, conn):
    """
    @todo : insert data into table question_answer
    @param question_answer:
    @return:
    """
    try:
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO question_answer '
            '(question_id, question_answer, mark_percent, sign_mark, is_correct, explaination)'
            ' values (?, ?, ?, ?, ?, ?)',
            (question_answer.question_id, question_answer.question_answer, question_answer.mark_percent,
             question_answer.sign_mark, question_answer.is_correct, question_answer.explanation))
        conn.commit()
        result = cur.lastrowid
    except lite.Error, e:
        if conn:
            conn.rollback()
        print tag + " insert_question_answer : Error %s:" % e.args[0]
        #sys.exit(1)
        result = -1
    return result
