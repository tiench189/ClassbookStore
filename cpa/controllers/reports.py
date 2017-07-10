# -*- coding: utf-8 -*-
""" Reports
    Theo dõi thống kê dữ liệu, doanh thu, lượt tải...
"""

__author__ = 'manhtd'
import scripts


@auth.requires_authorize()
def index():
    left = [db.auth_group.on(db.auth_group.role.like("CP Admin")), db.auth_membership.on(db.auth_membership.group_id == db.auth_group.id)]
    fields = (
        db.auth_user.id,
        db.auth_user.username,
        db.auth_user.email
    )
    payment_list = dict()
    users = db(db.auth_user.id == db.auth_membership.user_id)\
        (db.auth_group.role.like("CP Admin"))\
        (db.auth_membership.group_id == db.auth_group.id).select(groupby=db.auth_user.id)

    for user in users:
        payment_list[user.auth_user.id] = get_payment_cp_admin(user.auth_user.id)

    form = SQLFORM.grid(db.auth_user.id == db.auth_membership.user_id,
                        fields=fields,
                        deletable=False,
                        editable=False,
                        details=False,
                        create=False,
                        searchable=False,
                        links=[
                            {
                                'header': 'Doanh thu',
                                'body': lambda row: [
                                    scripts.style_money(payment_list[row['id']])
                                ]
                            },
                            {
                                'header': 'Phí phải trả',
                                'body': lambda row: [
                                    scripts.style_money(payment_list[row['id']]*5/100)
                                ]
                            },
                            {
                                'header': 'Thực lĩnh',
                                'body': lambda row: [
                                    scripts.style_money(payment_list[row['id']] - payment_list[row['id']]*5/100)
                                ]
                            }
                        ],
                        left=left)
    return dict(form=form)


@auth.requires_login()
def get_payment_cp_admin(cp_admin_id):
    query = db(db.clsb_download_archieve)\
        ((db.clsb_download_archieve.product_id == db.clsb_product.id) & (db.clsb_download_archieve.status.like('Completed')))\
        (db.clsb_product.product_code == db.clsb20_product_cp.product_code)\
        (db.auth_user.created_by == cp_admin_id)\
        ((db.clsb20_product_cp.created_by == cp_admin_id) | (db.clsb20_product_cp.created_by == cp_admin_id))

    total_payment = 0
    downloads = query.select(groupby=db.clsb_download_archieve.id)
    for download in downloads:
        total_payment += download['clsb_download_archieve']['price']
    return total_payment