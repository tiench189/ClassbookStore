# @auth.requires_login()
@auth.requires_authorize()
def index():
    # check_is_root()

    grid = smartgrid(db.auth_group, 
                             oncreate = group_on_create,
                             onupdate = group_on_update,
                             ondelete = group_on_delete,
                             showbuttontext = False)
    return dict(grid = grid)

def group_on_create(form):
    table = request.args[-1]
    record_id = form.vars.id
    auth.log_event(description='Create id ' + str(record_id) + ' in ' + str(table), origin='data')

def group_on_update(form):
    table = request.args[-2]
    record_id = request.args[-1]
    auth.log_event(description='Update id ' + str(record_id) + ' in ' + str(table), origin='data')

def group_on_delete(table, record_id):
    auth.log_event(description='Delete id ' + str(record_id) + ' in ' + str(table), origin='data')
