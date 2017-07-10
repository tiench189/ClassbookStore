#@author: hant 08-03-2013

from gluon.tools import Auth
#import cbMsg
SUCCESS = CB_0000#cbMsg.CB_0000
LACK_ARGS = CB_0002#cbMsg.CB_0002
DB_RQ_FAILD = CB_0003#cbMsg.CB_0003

table = 'clsb_contact'


def delete(ids, table):
    try:
        to_delete=db(db[table]._id.belongs(ids))
        to_delete.delete()
    except Exception as e:
        print "cba/controllers/contactlist/delete(ids, table) " + str(e)


@auth.requires_authorize()
def index():
    current_table = "clsb_contact"
#     if request.url.find('/clsb_contact/clsb_product.') >= 0:
#         current_table = "clsb_product"
#     print current_table
    selectable = lambda ids: delete(ids, current_table)

    links = [{'header': A('Reply', _href='' ), 'body': lambda row: A(IMG(_src=URL('static/images', 'icon_reply.png')), _href=URL('reply/'+ str(row.id)))}]
    
    try:
        if not table in db.tables(): redirect(URL('error'))
        form = SQLFORM.grid(db[table], 
                            showbuttontext = False,
                            user_signature = False,
                            create=False, editable=False, details=True, 
                            links=links, maxtextlength=8,
                            selectable=selectable )
        if form.element('.web2py_table input[type=submit]'):
            form.element('.web2py_table input[type=submit]')['_value'] = T('Delete')   
            form.element('.web2py_table input[type=submit]')['_onclick'] = \
            "return confirm('"+ CONFIRM_DELETE +"');"
        return dict(form = form)
    except Exception as ex: 
        if request.is_local: 
            return ex 
        else: 
            raise HTTP(400)
        
@auth.requires_login()   
def reply():
    contactID = request.args(0)
    #row = db().select(db[table].ALL, orderby=db[table].user_id)
    row =  db(db[table]._id.like(contactID)).select().first()
    
    receiver = row['email']
    form=FORM(B('Reply To: '), I(receiver),
              INPUT(_type='hidden', _value=receiver, _name='receiver'),
              INPUT(_type='hidden', _value=contactID, _name='contactID'),
              BR(),
              INPUT( _value = 'Re:' + row['contact_subject'], _name='rsubject', requires=IS_NOT_EMPTY(), _placeholder="subject",),#, _style="width: 490px; height: 20px;"  ), 
              BR(),
              TEXTAREA(BR(), BR(), BR(), BR(), BR(), BR(), BR(), BR(),
                       DIV('--------------------------------------------------'),
                       DIV('On ' + str(row['create_date']) + ', ' + row('name') + "&lt;" + row('email') + '&gt; wrote:'), 
                       DIV(row['contact_content']), _name='rcontent', 
                       requires=IS_NOT_EMPTY(), _placeholder="message content",),
#                        _style="width: 500px; height: 300px;"),
              BR(),
              INPUT(_type='submit', _value='Reply'))
    form.add_button('Back', URL('index'))
    #form['_style']='border:1px solid black'

    if form.accepts(request, session, onvalidation=sendE, detect_record_change=True):
        response.flash = 'Email đã được gửi thành công.'
        #force to "refresh" the page to update new contact's info
        #redirect(URL('reply/' + contactID))
    elif form.errors:
        response.flash = 'form has errors'
    else:
        response.flash = 'please fill the form'
        
    return dict(ReplyTo=form)

# Send email to user who contacted.
# Update the contact: processed_by, reply_content, status, confirm_date
def sendE(form):
    if request.vars:
        receiver = request.vars.receiver
        rsubject = request.vars.rsubject
        rmessage = request.vars.rcontent
        contactID = request.vars.contactID
        
        result = mail.send(to=[receiver], subject=rsubject, message="<html>" + rmessage + "</html>")
        db(db[table]._id.like(contactID)).update(processed_by=auth.user.username, 
                                        reply_content=rmessage, 
                                        status='PROCESSING', 
                                        confirm_date=request.now)
        return True
    else:
        return False