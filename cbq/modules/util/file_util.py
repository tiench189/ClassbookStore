__author__ = 'User'

from applications.cbq.modules.entities import app_constant
import os
import shutil
import zipfile
import hashlib
import urllib

tag = "file_util"


def get_file_upload_by_user(list_file, user_name):
    file_full_path_list = list()
    user_dir = os.path.join(app_constant.home_dir, user_name)
    media_dir = os.path.join(user_dir, app_constant.media_dir_name)
    for media_item in list_file:
        file_path = os.path.join(media_dir, media_item)
        file_full_path_list.append(file_path)
    return file_full_path_list


def copy_file(src, dst):
    """
    @todo : copy file to dest
    @param src:
    @param dst:
    @return:
    """
    result = 1
    try:
        shutil.copy2(src, dst)
    except Exception as e:
        print tag + " copy_file " + str(e)
        raise e
    return result


def copy_list_file(list_file_path, dst_dir):
    count = 0
    try:
        for file_item in list_file_path:
            copy_file(file_item, dst_dir)
            count += 1
    except Exception as e:
        print tag + " copy_list_file " + str(e)
    return count


def init_folder_quiz_package(parent_dir, user_name, exam_package):
    """
    @todo :
    @param parent_dir: /home/developers/phuongnh/CBSData/quiz
    @param user_name: author quiz
    @param exam_package: package app
    @return: folder name by package_name
    """
    #folder quiz/username
    user_dir = os.path.join(parent_dir, user_name)
    create_folder_if_not_exits(user_dir)
    #folder quiz/username/exam (folder exam: use store exam)
    folder_exam = os.path.join(user_dir, app_constant.folder_exam)
    create_folder_if_not_exits(folder_exam)
    #folder package name:
    folder_quiz = os.path.join(folder_exam, exam_package)
    create_folder_if_not_exits(folder_quiz)
    return folder_quiz


def create_folder_if_not_exits(folder_path):
    """
    @todo : make directory by folder_path if not exits
    @param folder_path:
    @return:
    """
    if not os.path.exists(folder_path):
        os.mkdir(folder_path)


def zip_dir(path_to_zip, zip_path):
    zip = zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(path_to_zip) + 1
    for base, dirs, files in os.walk(path_to_zip):
        for file in files:
            fn = os.path.join(base, file)
            zip.write(fn, fn[rootlen:])
    return zip_path


def hash_file(afile):
    blocksize = 65536
    md5 = hashlib.md5()
    buf = afile.read(blocksize)
    while len(buf) > 0:
        md5.update(buf)
        buf = afile.read(blocksize)
    return md5.hexdigest()


def download_img_from_url(img_url, des):
    file_name = img_url.split('/')[-1]
    file_name = rename_extension(file_name)
    des_path = os.path.join(des, file_name)
    urllib.urlretrieve(img_url, des_path)


def rename_extension(file_name):
    mp3_ext = 'mp3'
    jpg_ext = 'jpg'

    if file_name.endswith(jpg_ext):
        name_without_ext = file_name[:file_name.rfind('.')]
        ext = file_name[file_name.rfind('.') + 1:]

        if ext == jpg_ext:
            new_file_name = name_without_ext + '.clsbi21'
        elif ext == mp3_ext:
            new_file_name = name_without_ext + '.clsbs10'

    return new_file_name

#print rename_extension('hoa_hong_8-3-20130506152206.jpg')
