# coding=utf-8


@request.restful()
def index():
    response.view = 'generic.json'

    def GET(*args):
        # get product rating info
        # args: product_id
        # return: rating_score, rating_count
        if len(args) == 1:
            try:
                rating = db(db.clsb_product.id == args[0]).select(db.clsb_product.rating_count,
                                                                  db.clsb_product.product_rating)
                if len(rating) > 0:
                    rating_score = rating[0].product_rating if rating[0].product_rating is not None else 0
                    rating_count = rating[0].rating_count if rating[0].rating_count is not None else 0
                    score = 0 if rating_score == 0 else rating_score / rating_count
                    return dict(rating_score=score, rating_count=rating_count)
                else:
                    raise HTTP(400, str(dict(error="Product ID is not exist!")))
            except ValueError:
                raise HTTP(400, str(dict(error="Product ID is invalid!")))
        elif len(args) == 2:
            try:
                user_name = args[0]
                product_id = int(args[1])
            except ValueError:
                raise HTTP(400, str(dict(error="Parameters is invalid!")))

            user = db(db.clsb_user.username == user_name).select(db.clsb_user.id)

            if len(user) == 0:
                raise HTTP(400, str(dict(error="Invalid user!")))
            user_id = user[0].id
            rated = db((db.clsb_rating.user_id == user_id) & (db.clsb_rating.product_id == product_id)).count()
            return rated

        raise HTTP(400, str(dict(error='Parameters is invalid!')))

    def POST(**vags):
        if len(vags) == 4 and "user_token" in vags and "user_name" in vags and "product_id" in vags and "score" in vags:
            user_token = vags["user_token"]
            user_name = vags["user_name"]

            try:
                product_id = int(vags["product_id"])
                score = int(vags["score"])
                score = 5 if score > 5 else score
            except ValueError:
                raise HTTP(400, str(dict(error="Parameters is invalid!")))

            user = db((db.clsb_user.username == user_name) &
                      (db.clsb_user.user_token == user_token)).select(db.clsb_user.lastLoginTime, db.clsb_user.id)

            if len(user) == 0 or user[0].lastLoginTime + TIME_OUT < datetime.now():
                raise HTTP(401)

            user_id = user[0].id
            try:
                rating = db(db.clsb_product.id == product_id).select(db.clsb_product.rating_count,
                                                                     db.clsb_product.product_rating)
                if len(rating) == 0:
                    raise HTTP(400, str(dict(error="Product ID is not exist!")))
                rating_score = (rating[0].product_rating if rating[0].product_rating is not None else 0) + score
                rating_count = (rating[0].rating_count if rating[0].rating_count is not None else 0) + 1
                db(db.clsb_product.id == product_id).update(rating_count=rating_count, product_rating=rating_score)
                db.clsb_rating.insert(user_id=user_id, product_id=product_id, star=score)
                return dict(rating_score=(rating_score / rating_count), rating_count=rating_count)
            except Exception as ex:
                raise HTTP(500, str(dict(error="Your rating is invalid! " + str(ex))))
        raise HTTP(400, str(dict(error="Parameters is invalid!")))

    return locals()