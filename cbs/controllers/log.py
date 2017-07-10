import logs


def index():
    return dict()


def get_log():
    return "[" + logs.cls_read_log(",") + "]"


def cmd():
    response.view = "generic.json"
    return {
        'clear': logs.cls_clear_log(),
        'session': session,
    }.get(request.vars.cmd, "") 