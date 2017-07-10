__author__ = 'User'

import fs.path
import os
from applications.cbq.modules.entities import app_constant
from applications.cbq.modules.util import file_util

tag = "download.py"

def cover():
    """
    @return:
    """
    if len(request.args) < 2:
        return dict(error=CB_0003)
    file_name = request.args[0]
    ext = request.args[1]

    full_path = file_name + "." + ext
    user_name = "admin"
    try:

        path = fs.path.pathjoin("quiz", user_name)
        path = fs.path.pathjoin(path, "media")

        path = fs.path.pathjoin(path, full_path)

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        if ext == 'cbsbs10':
            response.headers['Content-Type'] = 'audio/mpeg'
        else:
            response.headers['Content-Type'] = 'image/png'
        response.headers['Content-Disposition'] = "attachment; filename=" + full_path
        return response.stream(osFileServer.open(path=path, mode='rb'))
    except Exception as ex:
        print str("Download cover error: " + str(ex))
        return dict(error=CB_0007)


def download_quiz():
    package = request.vars['path']
    user_name = request.vars['user']

    try:
        path = fs.path.pathjoin("quiz", user_name)
        path = fs.path.pathjoin(path, "exam")

        path = fs.path.pathjoin(path, package + ".zip")
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  file_util.hash_file(osFileServer.open(path=path, mode='rb')) + '.zip'
        return response.stream(osFileServer.open(path=path, mode='rb'))
    except Exception as e:
        print tag + "download_quiz : " + str(e)
        return dict(error='Không tìm thấy tập tin cần tải')

def return_url():
    user_name = "admin"

    img_list = list()
    path = os.path.join(app_constant.home_dir, user_name)
    path = fs.path.pathjoin(path, 'media')

    file_list = os.listdir(path)

    for img in file_list:
        temp = dict()
        #temp['image'] =