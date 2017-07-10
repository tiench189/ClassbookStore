#@author: hant
import sys
import fs.path

SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_image'

def get():
    if not table in db.tables(): NOT_EXIST
    
    rows =  db().select(db.clsb_image.ALL)
    
    l = list()
    for row in rows:
#        row['item_path'] = URL('download',args=row['item_path'], host = True)
        temp = dict()
        temp['id'] = row['id']
        temp['title'] = row['image_title']
        temp['description'] = row['description']
#        temp['item_path'] = row['item_path']
        l.append(temp)
    return dict(items=l)

def getinfo(): #params: args(0) = table's field, args(1) = value
    if not table in db.tables(): NOT_EXIST
    
    field = request.args(0)
    if field == 'id':
        field = '_id'
        
    rows =  db(db.clsb_image[field] == request.args(1)).select(db.clsb_image.ALL)
    
    l = list()
    for row in rows:
#        row['item_path'] = URL('download',args=row['item_path'], host = True)
        temp = dict()
        temp['id'] = row['id']
        temp['title'] = row['image_title']
        temp['description'] = row['description']
#        temp['item_path'] = row['item_path']
        l.append(temp)
    return dict(items=l)

from applications.cba.modules import clsbUltils
def getImage(): #params: image_code
    FILE_EXTENTION = '.png'
    FOLDER = 'CB_STORE_IMAGES'

    file = request.args(0) + FILE_EXTENTION
    try:
        row =  db(db.clsb_image.image_code == request.args(0)).select(db.clsb_image.ALL).first()
    except Exception as e:
        return e
    
    try:
        path = fs.path.pathjoin(FOLDER, file)
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'image/png'
        response.headers['Content-Disposition'] = "attachment; filename="+ file
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    except Exception as ex:
#        return e 
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))

"""
    List all banner in folder CB_STORE_BANNER.
"""        
def listBanner(): # list all file in the directory BANNER on server.
    FOLDER = 'CB_STORE_BANNER'
    
    try:
        path = fs.path.pathjoin(FOLDER)
        ff = osFileServer.listdir(path)
        ff.remove('Thumbs.db')
        return dict(items = ff)
    except Exception as e:
        return dict(error=str(e))

"""
    Get a banner.
"""
def getBanner(): #params: fileName
    FOLDER = 'CB_STORE_BANNER'
    if len(request.args) != 1:
        return LACK_ARGS
    banner = request.args(0)

    try:
        rows = osFileServer.listdir(FOLDER)
        for row in rows:
            if row[0:] == banner:
                banner = row
                path = fs.path.pathjoin(FOLDER, banner)
        response.headers['Content-Length'] = osFileServer.getinfo(path)['size']
        response.headers['Content-Type'] = 'image'
        response.headers['Content-Disposition'] = "attachment; filename="+ banner
        return response.stream(osFileServer.open(path = path, mode = 'rb'))
    except Exception as ex:
        redirect(clsbUltils.get_error_link('cba', 'default', 'error', ex, request.is_local))
      
def download():
    return response.download(request, db)