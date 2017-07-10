# -*- coding: utf-8 -*-

__author__ = 'Tien'

from PIL import Image
import glob, os
import sys


def divide_piece(size, split):
    return (size / split) + (1 if size % split != 0 else 0)


def cut_position(i, size, split):
    result = i * divide_piece(size, split)
    return result if result < size else size


def split_file(path_in, path_out):
    try:
        print(path_in)
        resize_thumb(path_in)
        path_in = path_in.replace(".jpg", ".png")
        split_x = 4
        split_y = 4
        root_img = Image.open(path_in)
        root_w = root_img.size[0]
        root_h = root_img.size[1]
        mindex = 0
        for i in range(0, split_y):
            for j in range(0, split_x):
                dict_out = path_out
                try:
                    if not os.path.exists(dict_out):
                        os.makedirs(dict_out)
                except Exception as err:
                    print err
                box = (cut_position(j, root_w, split_x), cut_position(i, root_h, split_y),
                       cut_position(j + 1, root_w, split_x), cut_position(i + 1, root_h, split_y))
                a = root_img.crop(box)
                new_img = Image.new("RGBA", (divide_piece(root_w, split_x), divide_piece(root_h, split_y)), (0, 0, 0, 0))
                new_img.paste(a, (0, 0))
                new_img.save(dict_out + "/" + str(mindex) + ".png", "PNG")
                mindex += 1
        os.remove(path_in)
        return "SUCCESS"
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def split_book(dict_in):
    try:
        page = 1
        for file in sorted(os.listdir(dict_in)):
            if file.endswith(".jpg") or file.endswith(".png"):
                split_file(dict_in + "/" + str(file), dict_in + "/page" + str(page))
                page += 1
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


def resize_thumb(path):
    try:
        import os
        import PIL
        from PIL import Image
        basewidth = 1600
        # print(path)
        thumb = Image.open(path)
        wper = (basewidth / float(thumb.size[0]))
        hsize = int(float(thumb.size[1]) * float(wper))
        new_thumb = thumb.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
        new_thumb.save(path.replace(".jpg", ".png"))
    except Exception as err:
        print str(err) + path
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))


def prepare_view_pdf():
    try:
        dict_in = "/home/vuongtm/thithu"
        for file in os.listdir(dict_in):
            if os.path.isdir(dict_in + "/" + str(file)):
                # print(dict_in + "/" + str(file))
                split_book(dict_in + "/" + str(file))
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))


prepare_view_pdf()
