# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################


def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simple replace the two lines below with:
    return auth.wiki()
    """
    # response.flash = T("Welcome to web2py!")
    return dict(message=T('Hello World'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in 
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())


def error():
    """
    handle error pages
    """
    response.generic_patterns = ['*']
    response.view = "generic.json"
    response.title = "Thông báo lỗi"
    if "code" in request.vars and request.vars.request_url != request.url:
        code = request.vars.code
        response.status = int(code)

        # show custom error message and view
        if not session.error is None:
            if "view" in session.error:
                response.view = session.error['view']
            message = session.error['message']
            del session.error
            if not message is None:
                return dict(request.vars, message=message)

        # default error handle
        if code == "500":
            if 'ticket' in request.vars:
                if str.startswith(request.client, '192.168.'):
                    url_ticket = URL(a="admin", c="default", f="ticket", args=request.vars["ticket"])
                    message = "Server error! Check more info <a href='%s' target='_blank'>here</a>." % url_ticket
                    return dict(request.vars, message=message)
        elif code == "401":
            return dict(request.vars, message="You don't have permission to access!")
        elif code == "404" or code == "400":
            return dict(request.vars, message="The path doesn't exist(%s)!" % code)
        return dict(request.vars, message="Function is maintaining(%s)!" % code)
    redirect(URL('index'))
