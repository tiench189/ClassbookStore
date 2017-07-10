__author__ = 'PhuongNH'


def index():
    current_table = "clsb20_device_exception"
    if request.url.find('cba/device_exception/index/clsb20_device_exception/new/clsb20_device_exception') >= 0:
        redirect(URL('cba', 'device_exception', 'add'))
    form = SQLFORM.smartgrid(db[current_table])
    return dict(form=form)


def add():
    try:
        if len(request.vars) > 0:
            device_serial = request.vars['txtSerial']

            if len(request.vars) > 1:
                email = request.vars['txtUserMoveTo']
                if email is None or email == "":
                    user_move_to_id = None
                else:
                    user_move_to = db(db.clsb_user.email == email).select()
                    if len(user_move_to) <= 0:
                        response.flash = "Không tồn tại địa chỉ email"
                        return dict()
                    else:
                        user_move_to_id = user_move_to.first()['id']

            user_move = db(db.clsb_device.device_serial == device_serial).select()
            if len(user_move) > 0:
                user_move_id = user_move.first()['user_id']
            else:
                user_move_id = None

            change_history_id = db.clsb20_device_change_history.insert(device_serial=device_serial,
                                                                       user_id_move=user_move_id,
                                                                       user_id_move_to=user_move_to_id)
            # insert record into table clsb20_device_exception:
            result = db.clsb20_device_exception.insert(device_serial=device_serial, history_change=change_history_id)

            if user_move is not None:
                # delete device owner
                if user_move_to_id is not None:
                    db(db.clsb_device.device_serial == device_serial).delete()
                    db.clsb_device.insert(user_id=user_move_to_id, device_serial=device_serial, in_use=False)

            session.flash = "Thành công"
            redirect(URL(a='cba', c='device_exception', f='index'))
    except Exception as e:
        print str(e)
    return dict()


def check_device_ownership():
    print request.vars
    try:
        if len(request.vars) < 1:
            return dict(result="Request invalid")
        device_serial = request.vars['device_serial']

        rows = db(db.clsb_device.device_serial == device_serial).select()
        if len(rows) > 0:
            user_owner = db(db.clsb_user.id == rows.first()['user_id']).select().first()
            return dict(result=str(user_owner['email']))
        else:
            return dict(result="")
    except Exception as e:
        print str(e)
    return dict(result="error")
