# -*- coding: utf-8 -*-
### required - do no delete

def index():
    return dict()


def error():
    """
    handle error pages
    """
    response.generic_patterns = ['*']
    response.view = "generic.json"
    response.title = "Thông báo lỗi"
    if "code" in request.vars and request.vars.request_url != request.url:
        code = request.vars.code
        response.status = int(code)

        # show custom error message and view
        if not session.error is None:
            if "view" in session.error:
                response.view = session.error['view']
            message = session.error['message']
            del session.error
            if not message is None:
                return dict(request.vars, message=message)

        # default error handle
        if code == "500":
            if 'ticket' in request.vars:
                if str.startswith(request.client, '192.168.') or str.startswith(request.client, '10.0.'):
                    url_ticket = URL(a="admin", c="default", f="ticket", args=request.vars["ticket"])
                    message = "Server error! Check more info <a href='%s' target='_blank'>here</a>." % url_ticket
                    return dict(message=message)
        elif code == "401":
            return dict(message="Bạn không có quyền truy cập!")
        elif code == "404" or code == "400":
            return dict(message="Đường dẫn không tồn tại(%s)!" % code)
        return dict(message="Chức năng đang bảo trì(%s)" % code)
    redirect(URL('index'))

def home():
    return dict(message="Create New")
