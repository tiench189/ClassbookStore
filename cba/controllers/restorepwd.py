__author__ = 'User'

from applications.cba.modules import restore_cbfw_pass


def index():
    print request.vars
    if len(request.vars) > 0:
        serial = request.vars['serial']
        secret_key = request.vars['secretkey']

        result = restore_cbfw_pass.gen_restore_code(serial, secret_key)
        return dict(pwd = result)
    return dict(pwd=None)