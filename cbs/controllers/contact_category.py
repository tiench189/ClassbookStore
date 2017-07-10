########################################
#hant 04-03-2013 

SUCCESS = CB_0000
LACK_ARGS = CB_0002
DB_RQ_FAILD = CB_0003
NOT_EXIST = CB_0001

table = 'clsb_contact_category'

"""
    Get all contact_category (used in the page Phản hồi).
"""
def get():
    try:
        rows = db().select(db[table].ALL).as_list()
        return dict(items=rows)
    except Exception as e:
        return dict(error=DB_RQ_FAILD + str(e)) 
