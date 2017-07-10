# -*- coding: utf-8 -*-
__author__ = 'tanbm'


def view():
    try:
        id = request.args[0]
        redirect(URL(a='cpa', c='creator', f='index', args=["clsb20_dic_creator_cp", "view", "clsb20_dic_creator_cp", id], user_signature=True))
    except Exception as e:
        return dict(error='Not found')


def index():
    form = SQLFORM.smartgrid(
        db.clsb20_dic_creator_cp,
        deletable=False,
        create=False
    )
    return dict(form=form)