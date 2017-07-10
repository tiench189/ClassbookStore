# -*- coding: utf-8 -*-
__author__ = 'tanbm'

import shutil
import errno
import os
import zipfile
import re
import sys


def get_store_status(code, db):
    product = db(db.clsb_product.product_code == code).select()
    if len(product) > 0:
        return product[0].product_status
    else:
        return "Không tồn tại"


def get_total_download(code, db):
    downloads = db((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.status.like('Completed')))\
                (db.clsb_product.product_code == code).select(groupby=db.clsb_download_archieve.id)
    if len(downloads) > 0:
        return len(downloads)
    else:
        return "Không tồn tại"


def fbuffer(f, chunk_size=10000):
    while True:
        chunk = f.read(chunk_size)
        if not chunk:
            break
        yield chunk


def copyanything(src, dst, ovewrite=False):
    try:
        if ovewrite & os.path.exists(dst):
            shutil.rmtree(dst)
        shutil.copytree(src, dst)
    except OSError as exc:
        # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise


def validate_zip(path, product_type):
    have_pdf = False
    have_cover = False

    have_apk = False

    have_qz = False
    have_quiz_zip = False
    try:
        z = zipfile.ZipFile(path, 'r')
        for name in z.namelist():
            if product_type == 'Book':
                if name.endswith('.pdf'):
                    have_pdf = True
                if name.find('cover.clsbi') >= 0 or bool(re.search('cover.[Pp][Nn][Gg]$', name)) or bool(re.search('cover.[Jj][Pp][Gg]$', name)):
                    have_cover = True
            elif product_type == 'Application':
                if name.find('cover.clsbi') >= 0 or bool(re.search('cover.[Pp][Nn][Gg]$', name)) or bool(re.search('cover.[Jj][Pp][Gg]$', name)):
                    have_cover = True
                if name.find('.apk') >= 0:
                    have_apk = True
            elif product_type == 'Exam' or product_type == 'Exercise':
                if name.endswith('.qz'):
                    have_qz = True
        z.close()
        if (product_type == 'Book') and (not have_cover or not have_pdf):
            errors = list()
            errors.append(" have_cover = " + str(have_cover) + " | ")
            errors.append(" have_pdf = " + str(have_pdf) + " | ")
            return errors
        elif (product_type == 'Application') and (not have_cover or not have_apk):
            errors = list()
            errors.append(" have_cover = " + str(have_cover) + " | ")
            errors.append(" have_apk = " + str(have_apk) + " | ")
            return errors
        elif (product_type == 'Exam' or product_type == 'Exercise') and (not have_qz ):
            errors = list()
            errors.append(" have_qz = " + str(have_qz) + " | ")
            return errors
        else:
            return "OK"
    except Exception as e:
        print e, " on line: "+str(sys.exc_traceback.tb_lineno)
        return "ZIP not found"