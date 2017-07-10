# -*- coding: utf-8 -*-


### required - do no delete
def user():
    return dict(form=auth())


def download():
    return response.download(request, db)


def call():
    session.forget()
    return service()
### end requires


def index():
    return dict(message='Homepage')


def error():
    """
    handle error pages
    """
    response.generic_patterns = ['*']
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
                    message = TAG("Server error! Check more info <a href='%s' target='_blank'>here</a>." % url_ticket)
                    return dict(message=message)
        elif code == "401":
            return dict(message=TAG("Bạn không có quyền truy cập! Quay trở về <a href='%s'>trang chủ</a>"
                                    % URL('index')))
        elif code == "404" or code == "400":
            return dict(message=TAG("Đường dẫn không tồn tại(%s)! Quay trở về <a href='%s'>trang chủ</a>"
                                    % (code, URL('index'))))

        return dict(message=TAG("Chức năng đang bảo trì(%s). Bạn có thể quay về <a href='%s'>trang chủ</a> hoặc "
                                "<a href='%s'>thông báo</a> với quản trị viên!"
                                % (code, URL('index'), URL('support_form'))))
    redirect(URL('index'))
