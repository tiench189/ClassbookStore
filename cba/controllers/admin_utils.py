#@author: hant
#table1 = 'clsb_device'
#table1 = 'clsb_user_log'
#table2 = 'clsb_contact'
#table2 = 'clsb_download_archieve'
#table1 = 'clsb_product_type'


def index():

    return dict()


def add_product_relation():

    txtfilter = request.vars["txtfilter"]
    product_found = list()
    if txtfilter is not None and txtfilter.strip() != "":
        product_found = db(db.clsb_product.product_title.contains(txtfilter)).select(db.clsb_product.id, db.clsb_product.product_title).as_list()
    checked_vals = request.vars['checkedval']

    tmp_checked_vals = list()
    if type(checked_vals) is str:
        tmp_checked_vals.append(checked_vals)
    else:
        tmp_checked_vals = checked_vals

    prlist = ProductRelationList()
    if tmp_checked_vals is not None:
        for pid in tmp_checked_vals:
            for pid2 in tmp_checked_vals:
                if pid != pid2:

                    pr = ProductRelation()
                    pr.product_id = pid
                    pr.relation_id = pid2
                    prlist.add_new_relation(pr)

                    pr2 = ProductRelation()
                    pr2.product_id = pid2
                    pr2.relation_id = pid
                    prlist.add_new_relation(pr2)

        prlist.insert_if_not_exist()

    return dict(products=product_found, checkedvals=tmp_checked_vals, relations=prlist)


###########################################################################################
#  DEFINE CLASSS
##########################################################################################


class ProductRelationList:

    list_rel = list()

    def __init__(self):
        list_rel = list()

    def add_new_relation(self, prealtion):

        found = False
        for item in self.list_rel:
            if (item.product_id == prealtion.product_id) and (item.relation_id == prealtion.relation_id):
                found = True
                break

        if not found:
            self.list_rel.append(prealtion)

    def insert_if_not_exist(self):

        for pr in self.list_rel:
            if not pr.is_in_db():
                pr.insert_to_db()


class ProductRelation:

    def __init__(self):
        self.product_id = -1
        self.relation_id = -1

    def is_in_db(self):

        found = False
        rs = db((db.clsb_product_relation.product_id == self.product_id) &
                (db.clsb_product_relation.relation_id == self.relation_id)).select().as_list()

        if len(rs) > 0:
            found = True

        return found

    def insert_to_db(self):

        if (self.product_id > 0) and (self.relation_id > 0):
            db.clsb_product_relation.insert(product_id=self.product_id, relation_id=self.relation_id)

