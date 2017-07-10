__author__ = 'User'


def insert(): #param segment_id/exam_id/segment_name/segment_order
    if len(request.args) < 4:
        return dict(mess=CB_0002)

    segment_id = request.args[0]
    exam_id = request.args[1]
    segment_name = request.args[2]
    segment_order = request.args[3]

    try:
        db.clsb_exam_segment.insert(segment_id=segment_id, exam_id=exam_id,
                                    segment_name=segment_name, exam_segment_order=segment_order)
    except Exception as e:
        print str(e)
        return dict(mess=CB_0003)

    return dict(mess=CB_0000)


