__author__ = 'User'

import os
import subprocess
from applications.cbq.modules.entities import app_constant
#from bs4 import BeautifulSoup


def get_file_name(file_name):
    """

    @param file_name:
    @return: file name without extension
    """
    str_file_name = file_name[:file_name.rfind(".")]
    return str_file_name


def get_ext_file(file_name):
    """

    @param file_name:
    @return:  extension of file
    """
    ext = file_name[file_name.rfind(".") + 1:]
    return ext


def encryption_quiz(file_src):
    """
    @todo : call lib to encryt quiz file
    @param file_src:
    @return:
    """
    lib_path = os.path.join(app_constant.home_dir, 'encryption')
    lib_path = os.path.join(lib_path, 'EncryptionQuiz.jar')

    ret = subprocess.call(['java', '-jar', lib_path, file_src])
    print str(ret)
