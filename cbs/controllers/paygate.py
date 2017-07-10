import urllib2
import json
import mc_paygate_sdk as mc

###BANK CARD NAME: TRAN DUC MANH
###BANK CARD NUMBER: 345345345
###BANK NAME: BIDV
###BANK CREATED: 04/13
###BANK PHONE VERIFY: 01656093458
CONSUMER_KEY = 'LsEpjnSGJm8nFU2BaLprdDtUBb'
CONSUMER_SECRET = 'p1uSoATIucROaph8UstL65lEdrL8spIapRi5H4Edro4SwIEH832OUR5e'
API_BASE_URL = "https://210.211.99.170:8090/api/"

def http_request(http_url, http_method = 'GET', parameters = None):
    consumer = mc.MCConsumer(CONSUMER_KEY, CONSUMER_SECRET)
    request = mc.MCRequest.from_consumer(consumer, http_method, http_url, parameters)
    request.sign_request(mc.MCSignatureMethod_HMAC_SHA1(), consumer)
    try:
        if http_method == 'GET':
            req = urllib2.Request(request.to_url())
            response = urllib2.urlopen(req)
        else:
            req = urllib2.Request(request.http_url, request.to_postdata())
            req.get_method = lambda: http_method
            response = urllib2.urlopen(req)

        return response.read()
    except urllib2.HTTPError as e:
        return e.read()
    except urllib2.URLError as e:
        return dict(hash = dict(code = 0, message = e.reason))

@request.restful()
def api():
    response.view = 'generic.json'
    def GET(*args, **vars):
        return json.loads(http_request("%s%s" % (API_BASE_URL, '/'.join(args)), 'GET', vars))
    def POST(*args, **vars):
        return json.loads(http_request("%s%s" % (API_BASE_URL, '/'.join(args)), 'POST', vars))
    def PUT(*args, **vars):
        return json.loads(http_request("%s%s" % (API_BASE_URL, '/'.join(args)), 'PUT', vars))
    def DELETE(*args, **vars):
        return json.loads(http_request("%s%s" % (API_BASE_URL, '/'.join(args)), 'DELETE', vars))
    return locals()        
