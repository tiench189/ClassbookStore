# -*- coding: utf-8 -*-

"""
This file is part of the Classbook Service Copyrighted by Trần Đức Mạnh <ducmanh86@gmail.com>
License: LGPLv3 (http://www.gnu.org/licenses/lgpl.html)
"""

PATH_TO_DATA = "/Violet/"
SYSTEM_PASS = "Violet@2013"

def __listdir(path):
    result = sorted(osFileServer.listdir(path = path, absolute = True, files_only = True))
    for i in range(0, len(result)):
        result[i] = result[i].replace(PATH_TO_DATA, '').replace('+', '-plus-')
    dirs = sorted(osFileServer.listdir(path = path, absolute = True, dirs_only = True))
    for dir in dirs:
        result.extend(__listdir(dir))
    return result

def index():
    response.view = 'generic.xml'
    # response.generic_patterns = ['*.xml']
    files = __listdir(PATH_TO_DATA)
    return dict(files = files)
    
@request.restful()
def download():
    response.view = 'generic.json'
    def GET(*args, **vars):
        files = __listdir(PATH_TO_DATA)
        return dict(files = files)
    def POST(*args, **vars):
        if request.env.http_authorization is None or request.env.http_authorization != SYSTEM_PASS:
            raise HTTP(401, "{'error': 'Not Authorization!'}")
        elif not "filename" in vars:
            raise HTTP(400, "{'error': 'Not valid parameters!'}")
        try:
            filename = vars["filename"].replace('-plus-', '+')
            response.headers['Content-Length'] = osFileServer.getinfo(PATH_TO_DATA + filename)['size']
            response.headers['Content-Type'] = 'application/octet-stream'
            response.headers['Content-Disposition'] = "attachment; filename=" + filename.split("/")[-1]
            return response.stream(osFileServer.open(path = PATH_TO_DATA + filename, mode = 'rb'))
        except Exception as ex:
            raise HTTP(404, "{'error': 'File Not Found!'}")
            # raise HTTP(404, "{'error': 'File Not Found" + PATH_TO_DATA + vars["filename"] + "!" + str(ex) + "'}")
    def PUT(*args, **vars):
        return "PUT SERVICE"
    def DELETE(*args, **vars):
        return "DELETE SERVICE"
    return locals()    