__author__ = 'Tien'


@auth.requires_authorize()
def index():
    form = SQLFORM.smartgrid(db.clsb30_set_of_product, showbuttontext=False)
    return dict(form=form)


@auth.requires_authorize()
def product():
    form = SQLFORM.smartgrid(db.clsb30_product_in_set, showbuttontext=False)
    return dict(form=form)