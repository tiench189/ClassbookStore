__author__ = 'User'


def index():
    if len(request.args) > 0:
        table_name = request.args[0]
        if not table_name in db.tables():
            return 'Table is not exist'
        form = SQLFORM.smartgrid(db[table_name])
        return dict(form=form)
    else:
        return dict(mess=str('invalid agument'))
