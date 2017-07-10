__author__ = 'Tien'
import sys

def get_version():
    try:
        app_name = request.args[0]
        data = db(db.clsb_version)
    except Exception as err:
        return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))