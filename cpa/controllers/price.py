# -*- coding: utf-8 -*-
__author__ = 'tanbm'


def index():
    return dict()


# @auth.requires_signature()
def history():
    form = db(db.clsb20_product_price_history.product_id == request.vars.product_id)(db.auth_user.id == db.clsb20_product_price_history.created_by)(db.clsb20_purchase_item.id == db.clsb20_product_price_history.purchase_item).select(orderby=~db.clsb20_product_price_history.created_on)
    return dict(form=form)