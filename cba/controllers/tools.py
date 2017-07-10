# -*- coding: utf-8 -*-
__author__ = 'manhtd'
from datetime import datetime


def call():
    session.forget()
    return service()


@auth.requires_login()
def delete_pdf_in_zip():
    response.view = 'generic.json'
    dirs = sorted(osFileServer.listdir(dirs_only=True))

    for cur_dir in dirs:
        files = sorted(osFileServer.listdir(path="./" + cur_dir, wildcard=cur_dir + ".[Zz][Ii][Pp]",
                                            files_only=True, absolute=True))
        if len(files) > 0:
            osFileServer.copy(files[0], files[0] + ".bk", True)
            import zipfile
            with zipfile.ZipFile(osFileServer.open(files[0] + ".bk", 'rb')) as zin:
                with zipfile.ZipFile(osFileServer.open(files[0], 'wb+'), mode="w") as zout:
                    try:
                        for name in zin.namelist():
                            if name[-4:] != ".pdf":
                                buffer_data = zin.read(name)
                                zout.writestr(name, buffer_data)
                    except Exception as ex:
                        print "Error on /" + cur_dir + ":" + str(ex.message)

    return dict(data="Complete!")


@service.jsonrpc
def encrypt_pdf(input_file, output_folder):
    import sys
    sys.path.append('/home/pylibs/pdflib_new')

    try:
        import pdfcryptor
        pdfcryptor.encrypt(input_file, output_folder)
        # sinh ra sample.W.pdf và sample.E.pdf trong thư mục hiện tại
    except:
        import traceback
        traceback.print_exc()
        import traceback
        import StringIO
        str_err = StringIO.StringIO()
        traceback.print_exc(file=str_err)
        return dict(result=False, error=str_err.getvalue())
    else:
        return dict(result=True)


@service.jsonrpc
def encrypt_device(serial, input_file, output_file):
    import sys
    sys.path.append('/home/pylibs/pdflib_new')

    try:
        import pdf2dev
        pdf2dev.encrypt(serial, input_file, output_file)
        # sinh ra sample.D.pdf cho thiết bị với serial '0132CE-121200123'
    except:
        import traceback
        import StringIO
        str_err = StringIO.StringIO()
        traceback.print_exc(file=str_err)
        return dict(result=False, error=str_err.getvalue())
    else:
        return dict(result=True)


def test():
    # from gluon.contrib.simplejsonrpc import ServerProxy
    # url = "http://127.0.0.1:8001/cba/tools/call/jsonrpc"
    # service = ServerProxy(url)
    # return service.encrypt_device('0132CE-121200123',
    #                               '/home/pylibs/output/sample.E.pdf', '/home/pylibs/output/sample.D.pdf')

    #test list to excel
    form = FORM('Date 1:', INPUT(_name='date1',_class='date',_size=10,requires=IS_DATE(format='%Y-%m-%d',error_message='must be YYYY-MM-DD')),'Date 2:',
              INPUT(_name='date2',_class='date',requires=IS_DATE(format='%Y-%m-%d',error_message='must be YYYY-MM-DD')),
              INPUT(_type='submit'),keepvalues=True)
    accpac_orders = {}

    if form.accepts(request, session):
        field_names = ('Order Nbr', 'Invoice Nbr', 'Location', 'Reference', 'Order Date', 'Invoice Date', 'Amount Paid', 'Amount Invoiced')

        response.view = 'generic.csv'
        return dict(filename='accpac_payment_details.csv', csvdata=accpac_orders, field_names=field_names)

    return dict(form=form)
