#@author: hant
#table1 = 'clsb_device'
#table1 = 'clsb_user_log'
#table2 = 'clsb_contact'
#table2 = 'clsb_download_archieve'
#table1 = 'clsb_product_type'
@auth.requires_login()
def index():
    list_tables = list()
    tables = db.executesql("select TABLE_NAME from information_schema.tables where table_schema='tvb20';")
    for table in tables:
        list_tables.append(table[0])
    if not request.args(0):
        return dict(args=False, tables=list_tables)

    table = request.args(0)
    if not table in db.tables(): return 'Table is not exist'

    #grid1 = SQLFORM.smartgrid(db[table1], showbuttontext = False)
    #grid = SQLFORM.smartgrid(db[table], showbuttontext = False)
    form = SQLFORM.smartgrid(db[table], args=request.args[:1],
                             showbuttontext=False,
    )
    return dict(args=True, grid=form, tables=list_tables)


def classbook_device():
    opened = (db.clsb_device.device_type == None)
    opened_rows = db(opened).select()
    opened_set = set()
    for r in opened_rows:
        opened_set.add(r.id)
    db.clsb_device._common_filter = lambda query: db.clsb_device.id.belongs(opened_set)

    records = SQLFORM.smartgrid(db.clsb_device)
    return dict(grid=records)
