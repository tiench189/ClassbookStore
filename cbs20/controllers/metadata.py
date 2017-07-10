# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys

def read_metadata():
    try:
        from pyPdf import PdfFileReader
        pdf_toread = PdfFileReader(open("/home/CBSData/upload/KHAC/TESTUPLOAD1.pdf", "rb"))
        pdf_info = pdf_toread.getDocumentInfo()
        ustr = str(pdf_info).encode("utf-8")
        print (ustr)
        return dict(metadata=pdf_info)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))

def read_xmp():
    try:
        with open( "/home/pylibs/black_edit.pdf", "rb") as fin:
            img = fin.read()
        imgAsString=str(img)
        xmp_start = imgAsString.find('<x:xmpmeta')
        xmp_end = imgAsString.find('</x:xmpmeta')
        if xmp_start != xmp_end:
            xmpString = imgAsString[xmp_start:xmp_end+12]
        print(xmpString)
    except Exception as ex:
        return dict(error=ex.message + " on line: "+str(sys.exc_traceback.tb_lineno))
