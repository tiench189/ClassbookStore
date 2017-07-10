#@author: hant 

from datetime import datetime

"""
    Get all comments in the comment table.
"""
def get():# software
    try:
        rows = db().select(db.clsb_comment.ALL, orderby = db.clsb_comment.comment_date).as_list()
        d = list()
        for row in rows:
            temp = dict()
            temp['email'] = row['email'] #notnull
            temp['comment_content'] = row['comment_content'] 
            temp['comment_date'] = row['comment_date'] 
            temp['product_code'] = row['product_code'] #notnull
            temp['status'] = row['status'] #notnull
            
            d.append(temp)
        return dict(items=d)
    except Exception as e:
        return dict(error =  CB_0003 + str(e)) #DB_RQ_FAILD
    
"""
    Get comment by product_code with pagination.
"""
def getinfo():# product_code, page
    page = 0
    items_per_page = 4
    if len(request.args) > 1: page = int(request.args[1])
    if len(request.args) > 2: items_per_page = int(request.args[2])

    limitby = (page * items_per_page, (page + 1) * items_per_page)
        
    try:
        total_items = db(db.clsb_comment.product_code == request.args(0))\
                (db.clsb_comment.status == 'APPROVED').count()
                
        total_pages = total_items / items_per_page + 1 
    #         if total_items % items_per_page > 0 else 0 

        rows = db(db.clsb_comment.product_code == request.args(0))\
                (db.clsb_comment.status == 'APPROVED').select(db.clsb_comment.ALL, orderby = ~db.clsb_comment.comment_date, limitby = limitby).as_list()
        d = list()
        for row in rows:
            temp = dict()
            temp['email'] = row['email'] #notnull
            temp['comment_content'] = row['comment_content'] 
            temp['comment_date'] = row['comment_date'] 
            temp['product_code'] = row['product_code'] #notnull
            temp['status'] = row['status'] #notnull

            d.append(temp)
        d = dict(items=d, page = page, total_items = str(total_items), total_pages = str(total_pages), items_per_page = items_per_page)
        return d
    except Exception as e:
        return dict(error =  CB_0003 + str(e)) #DB_RQ_FAILD
"""
    Submit comment, insert it in database.
"""
def send(): #vars: product_code, email, comment_content
    try:
        db.clsb_comment.insert(**request.vars)
        return dict(item=CB_0000)#SUCCESS
    except Exception as e:
        return dict(error =  CB_0003 + str(e)) #DB_RQ_FAILD