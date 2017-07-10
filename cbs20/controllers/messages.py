
import os.path
from applications.cba.modules import clsbUltils
from gluon.contrib.aes import ECBMode
import usercp
"""
    Get all message.
"""
def get_version():
	 book1 = dict()
	 book1['267'] = "20150514"
	 book1['268'] = "20150514"
	 ids = request.vars['id']
	 return dict(ids=ids, typeof=type(ids))

def get():
    try:
        msgs = list()
        msg1 = dict()
        msg1['code'] = 'SS01'
        msg1['type'] = 'NOTIFY'
        msg1['order'] = 1
        msg1['title'] = 'Tặng app classbook + Tài khoản 200.000 VNĐ khi mua SAMSUNG TAB 3V'
        msg1['short_description'] = 'Chương trình được tài trợ bởi SS. Khi mua 1 thiết bị tab 3V, bạn sẽ được tặng app + 02 sách miễn phí từ kho classbook.vn'
        msg1['msg'] = "Chương trình được tài trợ bởi SS. Khi mua 1 thiết bị tab 3V, bạn sẽ được tặng app + 02 sách miễn phí từ kho classbook.vn, bản quyền NXBGD VN"
        msg1['link'] = "http://classbook.vn"
        msg1['permanent'] = 'true'

        msg2 = dict()
        msg2['code'] = 'SS02'
        msg2['type'] = 'NOTIFY'
        msg2['order']= 3
        msg2['title'] = 'Tặng 02 sách miễn phí khi tải và cài đặt classbookApp'
        msg2['short_description'] = '"Chương trình được tài trợ bởi SS. Khi mua 1 thiết bị tab 3V, bạn sẽ được tặng app + 02 sách miễn phí từ kho classbook.vn'
        msg2['msg'] = "Chương trình được tài trợ bởi SS. Khi mua 1 thiết bị tab 3V, bạn sẽ được tặng app + 02 sách miễn phí từ kho classbook.vn, bản quyền NXBGD VN"
        msg2['link'] = ""
        msg2['permanent'] = 'false'

        msg3 = dict()
        msg3['code'] = 'NEW_VERSION'
        msg3['type'] = 'FILE'
        msg3['order']= 1
        msg3['title'] = 'Đã có phiên bản cập nhật classbookApp'
        msg3['short_description'] = 'Hỗ trợ ePub, html. Nâng cao hiệu năng hoạt động. Sửa một số lỗi crash'
        msg3['msg'] = "Tải và cài đặt lại để có thể xem được các định dạng sách mới"
        msg3['link'] = "http://app.classbook.vn/static/ClassbookAppSS.apk"
        msg3['permanent'] = 'true'
        msgs.append(msg1)
        msgs.append(msg2)
        msgs.append(msg3)
        return dict(messages=msgs)
    except Exception as ex:
        raise HTTP(500, "Bad request")