import sys
import fs.path
import hashlib
import usercp

DEVICE_NOT_EXIST = CB_0013
ID_NOT_EXIST = CB_0014
PRODUCT_CODE_NOT_EXIST = CB_0015
SUCCES = CB_0000
DB_RQ_FAILD = CB_0003
ERROR_DATA = CB_0007

def hash_file(afile):
    blocksize=65536
    md5 = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        md5.update(buf)
        buf = afile.read(blocksize)
    return md5.hexdigest()


def cover(): #params: product_code
    """
        Service download product's cover.
        (CB_Manager da tra ve device in_use)
    """
    try:
        product_data = db(db.clsb20_product_cp.product_code == request.args(0)).select()
        product_id = product_data[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không tồn tại.
        type_name = db(db.clsb_product_type.id == db.clsb_category.category_type)(db.clsb_category.id == product_data[0].product_category).select()[0]['clsb_product_type']['type_name']

        cp_path = ""
        check_cp = db(db.clsb20_product_cp.product_code.like(request.args(0))).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
            cp_path = fs.path.pathjoin(settings.cp_dir, "CP%s" % cpid, 'review', request.args(0), 'cover.clsbi')
        else:
            raise HTTP(400)


        path = cp_path
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'image/png'
        response.headers['Content-Disposition'] = "attachment; filename=cover.png"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    except Exception as ex:
        print str("Download cover error: " + str(ex))
        try:
            path = fs.path.pathjoin(settings.cp_dir+"cover.png")
            response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
            response.headers['Content-Type'] = 'image/png'
            response.headers['Content-Disposition'] = "attachment; filename=cover.png"
            return response.stream(osFileServer.open(path = path, mode = 'rb'))
        except Exception as ex:
            # redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
            return ex.message + "on line: "+str(sys.exc_traceback.tb_lineno) +"-"+path

from applications.cba.modules import clsbUltils


# @auth.requires_authorize
def data(): #params: product_code
    try:
        product_data = db(db.clsb20_product_cp.product_code == request.args(0)).select()
        product_id = product_data[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không tồn tại.
        type_name = db(db.clsb_product_type.id==db.clsb_category.category_type)(db.clsb_category.id==product_data[0].product_category).select()[0]['clsb_product_type']['type_name']

        cp_path = ""
        check_cp = db(db.clsb20_product_cp.product_code.like(request.args(0))).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
            cp_path = "CP%s" % cpid
        else:
            raise HTTP(400)
        product_files = osFileServer.listdir(path='./' + settings.cp_dir+cp_path+"/review/"+request.args(0), wildcard=request.args(0) + ".[Zz][Ii][Pp]", files_only=True)
        if len(product_files) == 0:
			raise Exception("File Not Found")
        path = fs.path.pathjoin(settings.cp_dir+cp_path+"/review/"+request.args(0), product_files[0])
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + hash_file(osFileServer.open(path = path, mode = 'rb')) + '.zip'
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    except Exception as ex: 
        # redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))

        return ex.message + "on line: "+str(sys.exc_traceback.tb_lineno)


# @auth.requires_authorize
def product(): #params: product_code
    try:
        product_data = db(db.clsb20_product_cp.product_code == request.args(0)).select()
        product_id = product_data[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không tồn tại.
        type_name = db(db.clsb_product_type.id==db.clsb_category.category_type)(db.clsb_category.id==product_data[0].product_category).select()[0]['clsb_product_type']['type_name']

        cp_path = ""
        check_cp = db(db.clsb20_product_cp.product_code.like(request.args(0))).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
            cp_path = "CP%s" % cpid
        else:
            raise HTTP(400)
        
        #product_files = osFileServer.listdir(path='./' + request.args(0)[:-17]+"/review/"+request.args(0), wildcard=request.args(0) + ".E.[Pp][Dd][Ff]", files_only=True)
        product_files = osFileServer.listdir(path='./' + settings.cp_dir+cp_path+"/review/"+request.args(0), wildcard=request.args(0) + ".[Pp][Dd][Ff]", files_only=True)
        if len(product_files) == 0:
			raise Exception("File Not Found")

        path = fs.path.pathjoin(settings.cp_dir+cp_path+"/review/"+request.args(0), product_files[0])
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = "attachment; filename=" + hash_file(osFileServer.open(path = path, mode = 'rb')) + '.pdf'
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    except Exception as ex: 
#         redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
        return ex.message + "on line: "+str(sys.exc_traceback.tb_lineno)


def thumb(): #product_code
    if len(request.args) != 1:
        return CB_0002
    
    try:
        product_data = db(db.clsb20_product_cp.product_code == request.args(0)).select()
        product_id = product_data[0]['id']
        if not product_id:
            raise HTTP(400, T(CB_0001))#Không tồn tại.
        type_name = db(db.clsb_product_type.id==db.clsb_category.category_type)(db.clsb_category.id==product_data[0].product_category).select()[0]['clsb_product_type']['type_name']

        cp_path = ""
        check_cp = db(db.clsb20_product_cp.product_code.like(request.args(0))).select()
        if len(check_cp) > 0:
            cpid = usercp.user_get_id_cp(check_cp.first()['created_by'], db)
            cp_path = "CP%s" % cpid
        else:
            raise HTTP(400)

        folder = request.args(0)
        path = fs.path.pathjoin(settings.cp_dir+cp_path+"/review/"+folder, 'thumb.png')

        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'image'
        response.headers['Content-Disposition'] = "attachment; filename=thumb.png"
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    except Exception as ex:
        print "Download Thumb Error:" + str(ex)
        try:
            path = fs.path.pathjoin(settings.cp_dir+"cover.png")
            response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
            response.headers['Content-Type'] = 'image'
            response.headers['Content-Disposition'] = "attachment; filename=thumb.png"
            return response.stream(osFileServer.open(path = path, mode = 'rb'))
        except Exception as ex:
            redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
#        return e