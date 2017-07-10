__author__ = 'Tien'
myTable = db.clsb_free_product
table = 'clsb_free_product'

def add_product():
    if request.vars:
        token = request.vars.token
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")
        user = user.first()
        try:
            product = db(db.clsb_product.product_code == request.vars.product_code)(
                db.clsb_category.id == db.clsb_product.product_category).select().first()
            quiz = db(db.clsb_product.product_code == ("Exer" + request.vars.product_code))(
                db.clsb_category.id == db.clsb_product.product_category).select()
        except:
            return dict(error="Mã sách không đúng")
        try:
            db.clsb30_product_history.insert(
                product_title=product['clsb_product']['product_title'],
                product_id=product['clsb_product']['id'],
                user_id=user['id'],
                category_id=product['clsb_category']['id'],
                product_price=product['clsb_product']['product_price']
            )
            db.clsb30_media_history.insert(
                product_title=product['clsb_product']['product_title'],
                product_id=product['clsb_product']['id'],
                user_id=user['id'],
                category_id=product['clsb_category']['id'],
                product_price=product['clsb_product']['product_price']
            )
            if len(quiz) > 0:
                quiz = quiz.first()
                db.clsb30_product_history.insert(
                    product_title=quiz['clsb_product']['product_title'],
                    product_id=quiz['clsb_product']['id'],
                    user_id=user['id'],
                    category_id=quiz['clsb_category']['id'],
                    product_price=0
                )
        except Exception as err:
            print(err)
            return  dict(error="Không thể insert")

        #insert vao bang khuyen mai
        try:
            myTable.insert(username=user['username'], product_code=request.vars.product_code, is_download=0)
            return dict(status="success")
        except Exception as err:
            print(err)
            return dict(status="error")

def get_free_product():
    list_free = []
    token = request.vars.token
    user = db(db.clsb_user.user_token.like(token)).select()
    if len(user) <= 0:
        return dict(error="Sai token")
    user = user.first()
    try:
        for row in db(db.clsb_product.product_code == myTable.product_code)\
                        (myTable.username == user['username']).select(myTable.username,
                               myTable.product_code,
                               myTable.is_download,
                               db.clsb_product.product_title,
                               db.clsb_product.id):
            list_free.append(dict(username=row.clsb_free_product.username, product_code=row.clsb_free_product.product_code,
                                  is_download=row.clsb_free_product.is_download, product_title=row.clsb_product.product_title,
                                  product_id=row.clsb_product.id))
    except Exception as err:
        print(err)
    return dict(list_free= list_free)

def check_user_product():
    if request.vars:
        print(request.vars)
        try:
            user_info = db(db.clsb_user.user_token == request.vars.token).select(db.clsb_user.username, db.clsb_user.id).as_list()

            if len(user_info) == 0:
                return dict(result=False, mess='Hết thời gian thao tác, vui lòng đăng nhập lại.', code = 'TOKEN_ERROR')
            user_info = user_info[0]

            product_info = db(db.clsb_product.product_code == request.vars.product_code).select(db.clsb_product.id, db.clsb_product.product_title).as_list()

            if len(product_info) == 0:
                return dict(result=False, mess='Sản phẩm không tồn tại', code="PRODUCT_NOT_EXITS")

            product_info = product_info[0]

            #check user buy product?

            download_archive = db(db.clsb_download_archieve.user_id == user_info['id'])(db.clsb_download_archieve.product_id == product_info['id']).select(db.clsb_download_archieve.id).as_list()

            if len(download_archive) > 0:
                return dict(result=False, mess='Đã mua', code='BOUGHT')

            download_history = db(db.clsb30_product_history.user_id == user_info['id'])(db.clsb30_product_history.product_id == product_info['id']).select(db.clsb30_product_history.id).as_list()

            if len(download_history) > 0:
                return dict(result=False, mess='Đã mua.', code='BOUGHT')

            return dict(result=True, mess='Sản phẩm ' + product_info['product_title']  +'chưa được mua cho tài khoản' + user_info['username'], code='NOT_YET_BUY')
        except Exception as err:
            print(err)
            return dict(result=False, mess='Có lỗi xảy ra', code='ERROR')

def add_product_free_to_db():
    if  request.vars:
        token = request.vars.token
        user = db(db.clsb_user.user_token.like(token)).select()
        if len(user) <= 0:
            return dict(error="Sai token")

        try:
            product = db(db.clsb_product.product_code.like(request.args[0]))(
                db.clsb_category.id == db.clsb_product.product_category).select().first()
        except:
            return dict(error="Mã sách không đúng")

        try:
            db.clsb30_product_history.insert(
                product_title=product['clsb_product']['product_title'],
                product_id=product['clsb_product']['id'],
                user_id=user['id'],
                category_id=product['clsb_category']['id'],
                product_price=product['clsb_product']['product_price']
            )
            return  dict()
        except Exception as err:
            print(err)
            return  dict(error="Không thể insert")
    return dict()
