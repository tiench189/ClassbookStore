__author__ = 'User'

from applications.cbq.controllers.plugin_elrte_widget import ElrteWidget
from applications.cbq.controllers.plugin_dialog import DIALOG


def index():
    # set language
    try:
        lang = 'vi'
    except:
        lang = 'en'

    image_chooser = DIALOG(title=T('Select an image'), close=T('close'), renderstyle=True,
                           content=LOAD('demoelrt', 'image_upload_or_choose', ajax=True))
    file_chooser = DIALOG(title=T('Select a file'), close=T('close'), renderstyle=True,
                          content=LOAD('demoelrt', 'file_upload_or_choose', ajax=True))
    fm_open = """function(callback, kind){
if (kind == 'elfinder') {%s;} else {%s;}
jQuery.data(document.body, 'elrte_callback', callback)
}""" % (file_chooser.show(), image_chooser.show())

    cssfiles = [URL('cbq', 'static', 'css/base.css')]

    ################################ The core ######################################
    # Inject the elrte widget
    # You can specify the language for the editor, and include your image chooser.
    # In this demo, the image chooser uses the uploadify plugin.
    # If you want to edit contents with css applied, pass the css file urls for an argument.
    db.clsb_question_content.question_content.widget = ElrteWidget()
    db.clsb_question_content.question_content.widget.settings.lang = lang
    db.clsb_question_content.question_content.widget.settings.fm_open = fm_open
    db.clsb_question_content.question_content.widget.settings.cssfiles = cssfiles
    ################################################################################

    form = SQLFORM(db.clsb_question_content)
    if form.accepts(request.vars, session):
        print request.vars
        #session.flash = 'submitted %s' % form.vars
        redirect(URL('index'))

    return dict(form=form)


def image_upload_or_choose():
    try:
        form = SQLFORM(db.plugin_elrte_widget_image, upload=URL('download'))
        info = ''
        if form.accepts(request.vars, session):
            img_file = request.vars['image']
            #download_img_from_url()
        records = db(db.plugin_elrte_widget_image.id > 0).select(orderby=~db.plugin_elrte_widget_image.id)
        _get_src = lambda r: URL(request.controller, 'download', args=r.image)
        records = DIV([IMG(_src=_get_src(r),
                           _onclick="""
    jQuery.data(document.body, 'elrte_callback')('%s');jQuery('.dialog').hide(); return false;
    """ % _get_src(r), _style='max-width:100px;max-height:100px;margin:5px;cursor:pointer;')
                       for r in records])
        return BEAUTIFY(dict(form=form, records=records))
    except Exception as e:
        print str(e)


def file_upload_or_choose():
    form = SQLFORM(db.plugin_elrte_widget_file, upload=URL('download'))
    info = ''
    if form.accepts(request.vars, session):
        info = 'submitted %s' % form.vars

    def _get_icon(v):
        ext = v.split('.')[-1]
        if ext in ('pdf',):
            filename = 'icon_pdf.gif'
        elif ext in ('doc', 'docx', 'rst'):
            filename = 'icon_doc.gif'
        elif ext in ('xls', 'xlsx'):
            filename = 'icon_xls.gif'
        elif ext in ('ppt', 'pptx', 'pps'):
            filename = 'icon_pps.gif'
        elif ext in ('jpg', 'gif', 'png', 'bmp', 'svg', 'eps'):
            filename = 'icon_pic.gif'
        elif ext in ('swf', 'fla'):
            filename = 'icon_flash.gif'
        elif ext in ('mp3', 'wav', 'ogg', 'wma', 'm4a'):
            filename = 'icon_music.gif'
        elif ext in ('mov', 'wmv', 'mp4', 'api', 'mpg', 'flv'):
            filename = 'icon_film.gif'
        elif ext in ('zip', 'rar', 'gzip', 'bzip', 'ace', 'gz'):
            filename = 'icon_archive.gif'
        else:
            filename = 'icon_txt.gif'
        return IMG(_src=URL('static', 'plugin_elrte_widget/custom/icons/%s' % filename),
                   _style='cursor:pointer;margin-right:5px;')

    records = db(db.plugin_elrte_widget_file.id > 0).select(orderby=~db.plugin_elrte_widget_file.id)
    records = DIV([DIV(A(_get_icon(r.file), r.name, _href='#', _onclick="""
jQuery.data(document.body, 'elrte_callback')('%s');jQuery('.dialog').hide(); return false;
""" % A(_get_icon(r.file), r.name, _href=URL(request.controller, 'download', args=r.file)).xml()),
                       _style='margin-bottom:5px;') for r in records])

    return BEAUTIFY(dict(form=form, records=records))


def download():
    return response.download(request, db)