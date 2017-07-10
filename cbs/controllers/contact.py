# #######################################
#hant 04-03-2013 

SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_contact'

"""
    Insert contact in to database. (form Phản hồi)
"""
# usage: /CBS/contact/send?username
def send():
    if request.vars and request.vars.email \
            and request.vars.contact_category_id and request.vars.contact_content \
            and request.vars.contact_subject:
        try:
            if request.vars.status:
                request.vars.pop('status')
            else:
                request.vars.update(status='PROCESSING')
            id = db[table].insert(**request.vars)
            message = "<html>From: " + request.vars.email + "<br>Xem chi tiết tại <a href='http://classbook.vn/cba/contactlist/index/view/clsb_contact/" + str(
                id) + "'>đây</a><br>" + request.vars.contact_content + "</html>"

            list_report = db(db.auth_user.id == db.clsb20_user_report_list.user_id)
            list_report = list_report(db.clsb20_user_report_list.report_type == db.clsb20_user_report_type.id)
            list_report = list_report(db["clsb20_user_report_type"]["code"].like("Support"))
            list_report = list_report.select(db.auth_user.email, groupby=db.auth_user.id).as_list()
            for user in list_report:
                mail.send(to=[user['email']], subject=request.vars.contact_subject, message=message)
            # mail.send(to=["chamsockhachhang@edcom.vn"], subject=request.vars.contact_subject, message=message)
            return dict(item=SUCCESS)
        except Exception as e:
            return dict(error=DB_RQ_FAILD + str(e))
    else:
        return dict(error=LACK_ARGS)
