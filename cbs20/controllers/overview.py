__author__ = 'Tien'


import sys
import re
import os

rxcountpages = re.compile(r"/Type\s*/Page([^s]|$)", re.MULTILINE|re.DOTALL)


def count_pages(filename):
    data = file(filename, "rb").read()
    return len(rxcountpages.findall(data))


def conver_pdf():
    try:
        pdf = "/temp/view_book/amin_amino_axit_protein_bai_tap.pdf"
        from pyPdf import PdfFileReader
        from PythonMagick import Image
        myfile = PdfFileReader(open(pdf, 'rb'))
        pages = count_pages(pdf)
        print(pages)
        for i in range(0, pages):
            im = Image(myfile.getPage(i))
            im.write('/home/view_book/file_image{}.png'.format(i))
    except Exception as ex:
        print(str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))
