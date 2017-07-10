__author__ = 'Tien'

######################SYNC#######################
import urllib

P_2_D_KEY = 'c-p3d*b'
def test_sync():
    str_test = "Chuỗi tiếng việt"
    return dict(result=str_test.encode("utf8","ignore"))
def sign_buy_media():
    try:
        username = request.args[2];
        user = db(db.clsb_user.username == username).select()
        if len(user) == 0:
            return dict(error="Tài khoản không tồn tại")
        else:
            user = user.first()
            db.clsb30_media_history.insert(
                product_title=request.args[0],
                product_id=request.args[1],
                user_id=user['id'],
                category_id=request.args[3],
                product_price=request.args[4]
            )
        return dict(result="SUCCESS")
    except Exception as err:
        return dict(error=str(err))

def sign_buy_product():
    print("sign_buy_product")
    try:
        username = request.args[2];
        user = db(db.clsb_user.username == username).select()
        if len(user) == 0:
            return dict(error="Tài khoản không tồn tại")
        else:
            user = user.first()
            db.clsb30_product_history.insert(
                product_title=request.args[0],
                product_id=request.args[1],
                user_id=user['id'],
                category_id=request.args[3],
                product_price=request.args[4]
            )
        return dict(result="SUCCESS")
    except Exception as err:
        print(err)
        return dict(error=str(err))

def register_user():
    if request.vars and not request.args:
        try:
            db.clsb_user.insert(**request.vars)
            return dict(result="SUCCESS")
        except Exception as err:
            return dict(error=str(err))
    elif request.args and not request.vars:
        try:
            lname = request.args(3)
            fname = request.args(2)
            if lname == "" and fname == "":
                lname = "User"
                fname = "Guest"
            db.clsb_user.update_or_insert(
                username=request.args(0), password=pbkdf2_hex(P_2_D_KEY, request.args(1)),
                lastLoginTime=request.now, firstName=lname,
                lastName=fname, email=request.args(4),
                phoneNumber=request.args(5), address=(request.args(6) or "ND"), district=request.args(7))
            return dict(result="SUCCESS")
        except Exception as err:
            return dict(error=str(err))

def update_user_fund():
    try:
        if request.vars:
            fund = request.vars.fund
            data_sum = request.vars.data_sum
            username = request.vars.username
            db(db.clsb_user.username == username).update(fund=fund, data_sum=data_sum)
            return dict(result="SUCCESS", fund=fund, data_sum=data_sum, username=username)
    except Exception as err:
        return dict(error=str(err))

