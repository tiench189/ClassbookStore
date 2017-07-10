
import os.path
from applications.cba.modules import clsbUltils
from gluon.contrib.aes import ECBMode
import usercp
"""
    Kiem tra he thong co san sang khong (ket noi internet available?)
"""
def system_available():
    infos = list()
    info1 = dict()
    info1['system_available'] = 'OK'

    infos.append(info1)
    return dict(infos=infos)

'''
def get():
    try:
	 msgs = list()
	 msg1 = dict()
	 
	 msg1['code'] = 'SS01'
	 msg1['title'] = 'Tặng app classbook + Tài khoản 200.000 VNĐ khi mua SAMSUNG TAB 3V'
	 msg1['short_description'] = 'Chương trình được tài trợ bởi SS. Khi mua 1 thiết bị tab 3V, bạn sẽ được tặng app + 02 sách miễn phí từ kho classbook.vn'
	 msg1['msg'] = "Chương trình được tài trợ bởi SS. Khi mua 1 thiết bị tab 3V, bạn sẽ được tặng app + 02 sách miễn phí từ kho classbook.vn, bản quyền NXBGD VN"
	 msg1['link'] = "http://classbook.vn"
	 msg1['permanent'] = 'true'

	 msg2 = dict()
	 msg2['code'] = 'SS02'
	 msg2['title'] = 'Tặng 02 sách miễn phí khi tải và cài đặt classbookApp'
	 msg2['short_description'] = '"Chương trình được tài trợ bởi SS. Khi mua 1 thiết bị tab 3V, bạn sẽ được tặng app + 02 sách miễn phí từ kho classbook.vn'
	 msg2['msg'] = "Chương trình được tài trợ bởi SS. Khi mua 1 thiết bị tab 3V, bạn sẽ được tặng app + 02 sách miễn phí từ kho classbook.vn, bản quyền NXBGD VN"
	 msg2['link'] = ""
	 msg2['permanent'] = 'false'
	 msgs.append(msg1)
	 msgs.append(msg2)
	 return dict(messages=msgs)
    except Exception as ex:
        raise HTTP(500, "Bad request")
'''