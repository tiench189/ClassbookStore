# coding=utf-8


from Crypto.Cipher import AES
import base64

__aes_key = b"#+Renajeva=URe6eV94EWu66asW-T?uB"

# the block size for the cipher object; must be 16, 24, or 32 for AES
__aes_blocksize = 32

# the character used for padding--with a block cipher such as AES, the value
# you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
# used to ensure that your value is always a multiple of BLOCK_SIZE
__aes_padding = '{'


def __aes_encrypt(value):
    # the block size for the cipher object; must be 16, 24, or 32 for AES
    block_size = __aes_blocksize

    # the character used for padding--with a block cipher such as AES, the value
    # you encrypt must be a multiple of block_size in length.  This character is
    # used to ensure that your value is always a multiple of block_size
    padding = __aes_padding

    # one-liner to sufficiently pad the text to be encrypted
    pad = lambda s: s + (block_size - len(s) % block_size) * padding

    # one-liners to encrypt/encode and decrypt/decode a string
    # encrypt with AES, encode with base64
    encode_aes = lambda c, s: base64.b64encode(c.encrypt(pad(s)))

    # create a cipher object using the random secret
    cipher = AES.new(__aes_key)

    # encode a string
    temp = encode_aes(cipher, value)
    return temp


def __aes_decrypt(value):
    # the character used for padding--with a block cipher such as AES, the value
    # you encrypt must be a multiple of BLOCK_SIZE in length.  This character is
    # used to ensure that your value is always a multiple of BLOCK_SIZE
    padding = __aes_padding

    # one-liners to encrypt/encode and decrypt/decode a string
    # encrypt with AES, encode with base64
    decode_aes = lambda c, e: c.decrypt(base64.b64decode(e)).rstrip(padding)

    # create a cipher object using the random secret
    cipher = AES.new(__aes_key)

    # decode the encoded string
    return decode_aes(cipher, value)


def encrypt(fund, username):
    return __aes_encrypt(username + "@" + str(fund))


def decrypt(db, username):
    user = db(db.clsb_user.username == username).select(db.clsb_user.fund, db.clsb_user.data_sum).as_list()
    if len(user) == 0:
        #print "FUCKING"
        return False
    else:
        #print "FUCKING1"
        str_decrypt = __aes_decrypt(user[0]['data_sum'])
        #print "FUCKING2: " + str_decrypt
        if str_decrypt.find("@") == -1:
            return False
        else:
            decrypt_datas = str_decrypt.split("@")
            if decrypt_datas[0] != username:
                return False
            else:
                return True


def money(value, split_char=',', str_zero='0', unit=''):
    value = str(value)
    i = 0
    price = ''
    for index in range(len(value) - 1, -1, -1):
        i += 1
        price = value[index] + price
        if i == 3:
            price = split_char + price
            i = 0
    if price[0] == split_char:
        price = price[1:]
    return str_zero if price == '0' else price + unit
