# -*- coding: utf-8 -*-
"""
#-----------------------------------------------------------------------------
# Name:        cpuser
#
# Purpose:     manage cp users
#
# Version:     1.1
#
# Author:      manhtd
#
# Created:     1/17/14
# Updated:     1/17/14
#
# Copyright:   (c) Tinh Vân Books
#
# Todo: 
#-----------------------------------------------------------------------------
"""
import usercp

@auth.requires_login()
@auth.requires_authorize()
def pending():
    def get_role(user):
        user_id = user.id
        roles = db(db.auth_membership.user_id == user_id)
        roles = roles(db.auth_group.id == db.auth_membership.group_id)
        roles = roles.select(db.auth_group.role)
        return ', '.join([r.role for r in roles])

    def confirm_approve(user, url):
        return SCRIPT("""
        jQuery("#approve_%d").click(function(){
            if(confirm("Are you sure you want to approve this user?")){
                $.ajax({
                  url: "%s",
                });
                jQuery(this).closest('tr').remove();
            };
            var e = arguments[0] || window.event;
            e.cancelBubble=true;
            if (e.stopPropagation) {
                e.stopPropagation();
                e.stopImmediatePropagation();
                e.preventDefault();
            }
        });
        """ % (user.id, url))

    if len(request.args) == 1:
        if request.args[0] == 'approve':
            uid = request.vars.cp_id
            u = db(db.auth_user.id == uid).select().first()
            u.update_record(registration_key='')
            message = """
            <html>
                Tài khoản %s đã được kích hoạt thành công!<br>
                Chúc mừng bạn đã trở thành CP tại hệ thống Classbook.
            </html>
            """ % u.username
            mail.send(u.email, 'Kích hoạt thành công!', message)
            return "alert('Approved succesfully!')"
        if request.args[0] == 'delete':
            uid = request.vars.cp_id
            u = db(db.auth_user.id == uid).select().first()
            u.delete_record()
            message = """
            <html>
                Tài khoản CP %s mà bạn đăng ký đã bị ban quản trị từ chối!
            </html>
            """ % u.username
            mail.send(u.email, 'Kích hoạt thất bại!', message)
            return "alert('Deleted succesfully!')"

    constraints = {str(db.auth_user): (db.auth_user.registration_key != '')}
    links = [{'header': A('Membership', _href=URL(c='membership', f='index')),
              'body': lambda user: SPAN(get_role(user))},
             {'header': DIV(),
              'body': lambda user: DIV(A(SPAN('', _class='icon ok icon-ok'),
                                         SPAN("Approve", _class='buttontext button'),
                                         _class='w2p_trap button btn', _href=URL(args=['approve'], vars=dict(cp_id=user.id)),
                                         target=':eval', _title='Approve', _id='approve_%d' % user.id),
                                       confirm_approve(user, URL(args=['approve'], vars=dict(cp_id=user.id))),
                                       A(SPAN('', _class='icon trash icon-trash'),
                                         SPAN("Delete", _class='buttontext button'),
                                         _class='w2p_trap button btn', callback=URL(args=['delete'], vars=dict(cp_id=user.id)),
                                         _href=URL(args=['delete'], vars=dict(cp_id=user.id)), delete='tr',
                                         target=':eval', _title='Delete'),
                                       _class="row_buttons", _nowrap="nowrap")}]
    grid = SQLFORM.smartgrid(db.auth_user, constraints=constraints, linked_tables=[], links=links,
                             editable=False, details=False, deletable=False, create=False)
    return dict(grid=grid)


@auth.requires_login()
@auth.requires_authorize()
def index():
    def get_role(user):
        user_id = user.id
        roles = db(db.auth_membership.user_id == user_id)
        roles = roles(db.auth_group.id == db.auth_membership.group_id)
        roles = roles.select(db.auth_group.role)
        return ', '.join([r.role for r in roles])
    query = db(db.auth_group.role.startswith('CP'))
    query = query(db.auth_membership.group_id == db.auth_group.id)
    query = query(db.auth_user.id == db.auth_membership.user_id)
    query = query(db.auth_user.registration_key == '')
    filter_users = query.select(db.auth_user.id, groupby=db.auth_user.id)
    filter_users = [x.id for x in filter_users]

    constraints = {str(db.auth_user): (db.auth_user.id.belongs(filter_users))}

    links = [{'header': A('Membership', _href=URL(c='membership', f='index')),
              'body': lambda row_data: SPAN(get_role(row_data))},
            {'header': 'Doanh thu',
              'body': lambda row_data: A(SPAN("Xem chi tiết", _class="btn"), _href=URL(c='reports', f='index', vars=dict(select=usercp.user_get_id_cp(row_data['id'],db))))}
            ]
    grid = SQLFORM.smartgrid(db.auth_user, constraints=constraints,
                             showbuttontext=False, linked_tables=[], links=links)
    return dict(grid=grid)
