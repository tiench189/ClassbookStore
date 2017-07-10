# -*- coding: utf-8 -*-
__author__ = 'Tiench'

import sys
import requests
from Crypto.Cipher import AES
import base64
import os

AES_KEY = "clsb1234clsb1234"


def test_soap():
    try:
        data = '<soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:web="http://webservice.bccsgw.viettel.com/"><soapenv:Header/><soapenv:Body><web:gwOperation><Input><wscode>getsubinfo</wscode><username>2427adb509b93ed4</username><password>e7a34fb48b5f12af4687ccba21e07165</password><rawData>?</rawData><param name="isdn" value="789456123"/></Input></web:gwOperation></soapenv:Body></soapenv:Envelope>'
        res = requests.post(url='http://183.182.100.169:8999/BCCSGateway?wsdl',
                            data=data,
                            headers={'Content-Type': 'text/xml; charset=utf-8'})
        print(res.text)
    except Exception as ex:
        print(ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))


def aes_action(action, text):
    try:
        # the block size for the cipher object; must be 16 per FIPS-197
        BLOCK_SIZE = 16
        # the character used for padding--with a block cipher such as AES, the value
        # you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
        # used to ensure that your value is always a multiple of BLOCK_SIZE
        PADDING = '{'

        # one-liner to sufficiently pad the text to be encrypted
        pad = lambda s: s + (BLOCK_SIZE - len(s) % BLOCK_SIZE) * PADDING

        # one-liners to encrypt/encode and decrypt/decode a string
        # encrypt with AES, encode with base64
        EncodeAES = lambda c, s: base64.b64encode(c.encrypt(pad(s)))
        DecodeAES = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(PADDING)

        # generate a random secret key
        secret = os.urandom(BLOCK_SIZE)

        # create a cipher object using the random secret
        cipher = AES.new(AES_KEY)

        # encode a string
        if action == "encrypt":
            return EncodeAES(cipher, text)
        else:
            return DecodeAES(cipher, text)
    except Exception as ex:
        return str(ex) + " on line: " + str(sys.exc_traceback.tb_lineno)


def test():
    try:
        return dict(result=aes_action(request.args[0], request.args[1]))
    except Exception as ex:
        return dict(error=ex.message + " on line: " + str(sys.exc_traceback.tb_lineno))

