__author__ = 'User'


def insert(): #param : exam_page_id/exam_id/page_index
    if len(request.args) < 3:
        return dict(mess=CB_0002)

    exam_page_id = request.args[0]
    exam_id = request.args[1]
    page_index = request.args[2]

    try:
        db.clsb_exam_page.insert(exam_page_id=exam_page_id, exam_id=exam_id, page_index=page_index)
    except Exception as e:
        print str(e)
        return dict(mess=CB_0003)
    return dict(mess=CB_0000)
