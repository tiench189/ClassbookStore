__author__ = 'Tien'

def send():
    try:
        print request.vars
        metadata_version_name = 'version'
        product_id = request.args[0]
        info = db(db.clsb_product.id == product_id).select().first()
        # get metadata named: version
        metadata_version = db(db.clsb_dic_metadata.metadata_name == metadata_version_name).select(
            db.clsb_dic_metadata.id).first()

        metadata_version_value = db((db.clsb_product_metadata.metadata_id == metadata_version['id']) & (
                    db.clsb_product_metadata.product_id == product_id)).select(
                    db.clsb_product_metadata.metadata_value).first()
        if metadata_version_value is None:
            metadata_version_value = dict()
            metadata_version_value['metadata_value'] = 0
        product = dict()
        product['id'] = info['id']
        product['code'] = info['product_code']
        product['version'] = metadata_version_value['metadata_value']

        product_list = list()
        product_list.append(product)
        custom = dict()
        custom['list_product']=product_list

        token_hex = db(db.clsb_download_archieve.product_id == product_id) \
            (db.clsb_download_archieve.user_id == db.clsb_user.id) \
            (db.clsb_user.email == db.clsb30_apns.user_email).select(db.clsb30_apns.apns_token, groupby=db.clsb30_apns.apns_token).as_list()
        print(token_hex)
        # tem_token1 = dict()
        # tem_token1['apns_token'] = '53f5a4ffaeccfb53d71ef3946ce2a0fb61c988863de58030654ecc5b4900725e'
        # token_hex.append(tem_token1)
        # tem_token = dict()
        # tem_token['apns_token'] = '606817bcc8b4880aae7309220c7f1de11c41ec944f3f3bccadc96d69d994e3c8'
        # token_hex.append(tem_token)
        try:
            mess = request.vars.mess
            if None != mess:
                print(mess)
                if len(token_hex) == 0:
                    return dict(mess="Chưa có thiết bị IOS nào tải sản phẩm này")
                else:
                    for token in token_hex:
                        send_apns(mess, token['apns_token'], custom)
                    return dict(mess="Thành công" + str(token_hex))
            else:
                return dict(mess="")
        except Exception as err:
            print(err)
            return dict(mess=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))
    except Exception as err:
        print(err)
        return dict(error=str(err) + " on line: "+str(sys.exc_traceback.tb_lineno))

def send_apns(mess, token, custom):
    from apns import APNs, Payload
    pem_file = settings.home_dir + "apns_dev.pem"
    apns = APNs(use_sandbox=True, cert_file=pem_file, key_file=pem_file)
    payload = Payload(alert=mess, badge=1, sound='default', custom=custom)
    print(payload)
    apns.gateway_server.send_notification(token, payload)
