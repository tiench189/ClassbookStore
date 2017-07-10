__author__ = 'Tien'

import sys


def caculate_real():
    try:
        select_transaction = db(db.clsb_transaction.status == 'COMPLETE').select()
        for trans in select_transaction:
            print(trans)
            amount = int(trans['amount'])
            payment_type = trans['payment_type']
            if payment_type == "VISA":
                face_value = amount
                real_value = amount * 0.97 - 5000
                db(db.clsb_transaction.id == trans['id']).update(face_value=face_value, real_value=real_value)
            elif payment_type == "NL":
                face_value = amount
                real_value = amount
                db(db.clsb_transaction.id == trans['id']).update(face_value=face_value, real_value=real_value)
            elif payment_type == "VIETTEL" or payment_type == "VMS" or payment_type == "VNP":
                face_value = int(trans['card_amount'])
                real_value = amount
                db(db.clsb_transaction.id == trans['id']).update(face_value=face_value, real_value=real_value)
            elif payment_type == "ATM_ONLINE":
                face_value = amount
                real_value = amount * 0.985 - 500
                db(db.clsb_transaction.id == trans['id']).update(face_value=face_value, real_value=real_value)
            else:
                db(db.clsb_transaction.id == trans['id']).update(face_value=amount, real_value=amount)
        return "SUCCESS" + str(len(select_transaction))
    except Exception as err:
        return dict(err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
