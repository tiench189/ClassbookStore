#Class su dung cho service gen SMS Code ung dung A0Tec
import md5
import time

current_time_in_milli_second = lambda: int(round(time.time() * 1000))


class SMSCode:

    def __init__(self, message_id, send_number):
        #Do nothing
        self.messageid = message_id
        self.sendnumber = send_number

    def gen_sms_pay_code(self):
        m = md5.new()
        stmp = str(self.messageid) + str(self.sendnumber) + str(current_time_in_milli_second())
        m.update(stmp)
        return m.hexdigest()[:5]
