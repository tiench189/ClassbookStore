# -*- coding: utf-8 -*-
__author__ = 'tanbm'


@auth.requires_authorize()
def index():
    form = SQLFORM.grid(db.clsb20_product_type)
    return dict(form=form)