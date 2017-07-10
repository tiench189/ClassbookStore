# -*- coding: utf-8 -*-
__author__ = 'tanbm'
import os

def index():
    raise HTTP(404)

# @auth.requires_authorize
def file():
    file_name = ""
    num = 0
    for path in request.args:
        if num > 0:
            file_name += "/"
        file_name += path
        num += 1
    file_path = os.path.join(settings.cp_dir, file_name)
    try:
        # f = open(file_path)
        response.headers['Content-Type'] = 'text/plain'
        attachment = 'attachment;filename='+request.args[len(request.args)-1]
        response.headers['Content-Disposition'] = attachment
        # raise HTTP(200, f, **{'Content-Type': 'text/csv', 'Content-Disposition': attachment + ';'})
        return response.stream(osFileServer.open(path=file_path, mode='rb'))
    except Exception as e:
        raise HTTP(404)
def cover():
    file_name = ""
    num = 0
    print(request.args)
    for path in request.args:
        if num > 0:
            file_name += "/"
        file_name += path
        num += 1

    file_path = os.path.join(settings.cp_dir, file_name)

    try:
        # f = open(file_path)
        response.headers['Content-Type'] = 'text/plain'
        attachment = 'attachment;filename='+request.args[len(request.args)-1]
        response.headers['Content-Disposition'] = attachment
        # raise HTTP(200, f, **{'Content-Type': 'text/csv', 'Content-Disposition': attachment + ';'})
        return response.stream(osFileServer.open(path=file_path, mode='rb'))
    except Exception as e:
        # f = open(settings.home_dir+settings.cp_dir+"cover.png")
        file_path = settings.cp_dir+"cover.png"
        response.headers['Content-Type'] = 'text/plain'
        attachment = 'attachment;filename=no_image.png'
        response.headers['Content-Disposition'] = attachment
        # raise HTTP(200, f, **{'Content-Type': 'text/csv', 'Content-Disposition': attachment + ';'})
        return response.stream(osFileServer.open(path=file_path, mode='rb'))

def image():
    file_name = ""
    num = 0
    for path in request.args:
        if num > 0: file_name += "/"
        file_name += path
        num += 1
    file_path = os.path.join(settings.cp_dir, file_name)
    img = db(db.clsb20_product_image.image == request.args[len(request.args)-1]).select()
    try:
        # f = open(file_path)
        response.headers['Content-Type'] = 'text/plain'
        attachment = 'attachment;filename='+str(img[0].description)
        response.headers['Content-Disposition'] = attachment
        # raise HTTP(200, f, **{'Content-Type': 'text/csv', 'Content-Disposition': attachment + ';'})
        return response.stream(osFileServer.open(path=file_path, mode='rb'))
    except Exception as e:
        # f = open(settings.home_dir+settings.cp_dir+"cover.png")
        file_path = settings.cp_dir+"cover.png"
        response.headers['Content-Type'] = 'text/plain'
        attachment = 'attachment;filename=no_image.png'
        response.headers['Content-Disposition'] = attachment
        return response.stream(osFileServer.open(path=file_path, mode='rb'))
        # raise HTTP(200, f, **{'Content-Type': 'text/csv', 'Content-Disposition': attachment + ';'})