__author__ = 'User'
import fs
import os


def uploadfile():

    if len(request.vars) < 2:
        return dict(mess=CB_0002)

    if 'data' in request.vars:
        try:
            filename = request.vars.data.filename
            user = request.vars['user']
            path = fs.path.join("quiz", user)

            index_ = filename.rfind("\\") + 1
            filename = filename[index_:]
            filename = filename.replace(" ", "_")

            if str(filename).endswith("mp3"):

                index_dot = filename.rfind(".")
                file_name = filename[:index_dot]
                file_name += ".clsbs10"
                #static_path = static_path.join(static_path, file_name)
                #osStaticFolder.setcontents(static_path, request.vars.data.file)

                #osStaticFolder.setcontents(path)
            if str(filename).endswith("jpg"):
                index_dot = filename.rfind(".")
                file_name = filename[:index_dot]
                file_name += ".clsbi21"

            path = fs.path.join(path, "media")
            path = fs.path.join(path, file_name)
            osFileServer.setcontents(path, request.vars.data.file)

            print 'uploaded ' + str(filename)
        except Exception as e:
            print str(e)
            return dict(mess=CB_0003)
    return dict(mess=CB_0000)


def ckeditor_upload():
    upload = request.vars.upload
    if upload is not None:
        if hasattr(upload, 'file'):
            filename = upload.filename
            data = upload.file

            user = 'admin'
            path = fs.path.join("quiz", user)

            index_ = filename.rfind("\\") + 1
            filename = filename[index_:]
            filename = filename.replace(" ", "_")

            if str(filename).endswith("mp3"):

                index_dot = filename.rfind(".")
                file_name = filename[:index_dot]
                file_name += ".clsbs10"

            if str(filename).endswith("jpg"):
                index_dot = filename.rfind(".")
                file_name = filename[:index_dot]
                file_name += ".clsbi21"

            path = fs.path.join(path, "media")
            path = fs.path.join(path, file_name)
            osFileServer.setcontents(path, data)

    return dict(mess='Success')

            #result = db.files.insert(filename = old_filename,
            #                         uploaded_data = new_filename,
            #                         created_on = datetime.today())
            #if not result:
            #    message = T('An error has occured during upload.')
            #    url = ''
            #else:
            #    message = T('File uploaded succesfully.')
            #    url = URL(r = request, f = 'download', args = new_filename)
        #    return dict(form = None, cknum = request.vars.CKEditorFuncNum, url = url, message = message)
        #else:
        #    raise HTTP(401, T('Upload is not proper type.'))