from gluon import URL
def get_error_link(a, c, f, error, is_local = False):
    if is_local:
        return URL(a = a, c = c, f = f, vars = dict(error = str(error).encode('base64')))
    else:
        return URL(a = a, c = c, f = f)