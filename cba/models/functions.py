import logging
logger = logging.getLogger("web2py.app.cba")
logger.setLevel(logging.DEBUG)


def list_to_excel(table, filename):
    response.view = 'generic.csv'
    return dict(filename=filename+'.xls', table=table)