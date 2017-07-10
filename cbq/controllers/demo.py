__author__ = 'User'


from applications.cbq.controllers.plugin_notemptymarker import mark_not_empty, unmark_not_empty


def index():
    form = SQLFORM(db.plugin_uploadify_widget, upload=URL('download'))
    if form.accepts(request.vars, session):
        session.flash = 'submitted %s' % form.vars
        redirect(URL('index'))

    unmark_not_empty(db.plugin_uploadify_widget)
    records = db(db.plugin_uploadify_widget.id > 0).select(orderby=~db.plugin_uploadify_widget.id)
    records = SQLTABLE(records, headers="labels",
                       upload=URL('download'), linkto=lambda f, t, r: URL('edit', args=f))
    return dict(form=form, records=records, tests=[A('test_load', _href=URL('test'))])


def edit():
    record = db(db.plugin_uploadify_widget.id == request.args(0)).select().first() or redirect('index')
    form = SQLFORM(db.plugin_uploadify_widget, record, upload=URL('download'))
    if form.accepts(request.vars, session):
        session.flash = 'edit %s' % form.vars
        redirect(URL('edit', args=request.args))

    return dict(back=A('back', _href=URL('index')), form=form)


def download():
    return response.download(request, db)


def test():
    if request.args(0) == 'ajax':
        form = SQLFORM(db.plugin_uploadify_widget)
        if form.accepts(request.vars, session):
            response.flash = DIV('submitted %s' % form.vars).xml()
            db.commit()
        return form

    form = LOAD('demo', 'test', args='ajax', ajax=True)
    return dict(back=A('back', _href=URL('index')), form=form)
