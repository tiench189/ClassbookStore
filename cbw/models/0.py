# coding=utf-8
from applications.cbq import controllers
from gluon.storage import Storage

settings = Storage()

settings.title = 'Class Book Service'
settings.subtitle = 'powered by TVB'
settings.author = 'TVB'
settings.author_email = 'admin@classbook.vn'
settings.keywords = ''
settings.description = ''
response.generic_patterns = ['*']
#================================================================================================
# STRINGS
#================================================================================================

settings.string_register_user_success = 'Đăng ký thành công!'
settings.string_ok = 'OK'

#=================================================================================================
# WEB SERVICES
#=================================================================================================

settings.service_scheme = 'http'
settings.service_host = "localhost"
settings.service_port = 80
settings.service_extension = 'json'

#tiench test
settings.service_get_product_details = dict(app='cbw', controller='tien_test', function='tiench_get_details_product')
#end tiench
settings.service_user_info = dict(app='cbs', controller='users', function='select')
settings.service_user_download = dict(app='cbs', controller='users', function='getDownloadInfo')
settings.service_user_auth = dict(app='cbs', controller='users', function='authentication')
settings.service_user_update = dict(app='cbs', controller='users', function='update')
settings.service_user_register = dict(app='cbs', controller='users', function='register')
settings.service_user_deposit = dict(app='cbs', controller='users', function='deposit')
settings.service_user_device = dict(app='cbs', controller='users', function='get_list_device')
settings.service_change_device_name = dict(app='cbs', controller='devices', function='change_device_name')
settings.service_confirm_password = dict(app='cbs', controller='users', function='confirmpwd')
settings.service_check_buy_product = dict(app='cbs', controller='users', function='is_user_buy_a_book')
settings.service_get_cb_price = dict(app='cbs', controller='order', function='cb_price')

settings.service_country_get = dict(app='cbs', controller='country', function='get')
settings.service_province_get = dict(app='cbs', controller='province', function='get')
settings.service_province_get_district = dict(app='cbs', controller='province', function='district')
settings.service_district_get = dict(app='cbs', controller='district', function='get')

settings.service_classes_get = dict(app='cbs', controller='classes', function='get')
settings.service_subject_getbcatid = dict(app='cbs', controller='subjects', function='getbcatid')
settings.service_subject_get = dict(app='cbs', controller='subjects', function='get')
settings.service_subject_get_classes = dict(app='cbs', controller='subjects', function='classes')
settings.service_product_getquiz = dict(app='cbs', controller='products', function='getquiz')
settings.service_verify_request_rspwd = dict(app='cbs', controller='users', function='verify_email')
settings.service_renew_pwd = dict(app='cbs', controller='users', function='renewpwd')

settings.service_user_add_device = dict(app='cbs', controller='warrantydevice', function='register')
settings.service_user_get_warranty_history = dict(app='cbs', controller='users', function='get_warranty_history')
settings.service_get_warranty_history = dict(app='cbs', controller='warranty_history', function='api')

settings.service_device = dict(app='cbs', controller='devices', function='device')
settings.service_delete_device = dict(app='cbs', controller='users', function='delete_device')
settings.service_device_registed = dict(app='cbs', controller='warrantydevice', function='registed')
settings.service_get_device_detail = dict(app='cbs', controller='devices', function='get_device_detail')

settings.service_user_send_message = dict(app='cbs', controller='contact', function='send')
settings.service_order_send = dict(app='cbs', controller='order', function='send')

settings.service_comment_send = dict(app='cbs', controller='comments', function='send')
settings.service_comment_info = dict(app='cbs', controller='comments', function='getinfo')

settings.service_category_get = dict(app='cbs', controller='categories', function='get_tree')
settings.service_category_getall = dict(app='cbs', controller='categories', function='getall')
# settings.service_category_getall = dict(app='cbs', controller='categories', function='get')

settings.service_product_get = dict(app='cbs', controller='products', function='get')
settings.service_product_search_by_creator = dict(app='cbs', controller='products', function='creator')
settings.service_product_search_advance = dict(app='cbs', controller='products', function='search_advance')
settings.service_product_search = dict(app='cbs', controller='products', function='search')
settings.service_product_info = dict(app='cbs', controller='products', function='getinfo')
settings.service_product_all = dict(app='cbs20', controller='product', function='getinfo')
settings.service_product_getquizinfo = dict(app='cbs', controller='products', function='getquizinfo')
settings.service_product_relation = dict(app='cbs', controller='products', function='relation')
settings.service_product_metadata = dict(app='cbs', controller='products', function='metadatainfo')
settings.service_product_top_download = dict(app='cbs', controller='products', function='topdownload')
settings.service_product_top_pay = dict(app='cbs', controller='products', function='toppay')
settings.service_product_top_new = dict(app='cbs', controller='products', function='topnew')
settings.service_check_free_classbook = dict(app='cbs', controller='products', function='check_free_classbook')

settings.service_check_media = dict(app='cbs', controller='download', function='check_media')

settings.service_rating = dict(app='cbs', controller='rating', function='index')

settings.service_home_topic_item_get = dict(app='cbs', controller='home_topic_item', function='get')
settings.service_home_topic_get = dict(app='cbs', controller='home_topic', function='get')
settings.service_get_published_topic = dict(app='cbs', controller='home_topic', function='get_published_topic')

settings.service_paygate = dict(app='cbs', controller='paygate', function='api')
settings.service_transaction = dict(app='cbs', controller='transaction', function='index')
settings.service_user_auth_by_token = dict(app='cbs', controller='users', function='authentication_by_token')

##########TienCH######################################
settings.service_add_free_product = dict(app='cbs', controller='free_product', function='add_product')
settings.service_get_free_product = dict(app='cbs', controller='free_product', function='get_free_product')
settings.service_check_user_product = dict(app='cbs', controller='free_product', function='check_user_product')
settings.service_get_info_by_code = dict(app='cbs', controller='products', function='get_info_by_code')
settings.service_check_payment = dict(app='cbs', controller='download', function='check_payment')
settings.service_check_classbook = dict(app='cbs', controller='devices', function='is_device_classbook')
settings.service_get_detail_list = dict(app='cbs', controller='products', function='get_list_product_by_id')
settings.service_check_elearning = dict(app='cbs', controller='users', function='check_elearning')

settings.service_buy_history = dict(app='cbs20', controller='product', function='get_all_history')
settings.service_check_free_cp = dict(app='cbs20', controller='download', function='check_free_cp')
settings.check_buy_product_20 = dict(app='cbs20', controller='product', function='check_buy_product')
settings.check_buy_quiz = dict(app='cbs20', controller='product', function='check_buy_quiz')
settings.check_buy_media = dict(app='cbs20', controller='product', function='check_buy_media')
settings.service_get_data_price = dict(app='cbs20', controller='product', function='get_data_price')
settings.get_list_media = dict(app='cbs20', controller='product', function='get_list_media')
settings.service_buy_product = dict(app='cbs20', controller='product', function='buy_product')
settings.service_buy_product_divide = dict(app='cbs20', controller='product', function='buy_product_divide')
settings.service_check_available_payment = dict(app='cbs20', controller='users', function='check_available_payment')
settings.service_feature_image = dict(app='cbs20', controller='product', function='feature_image')
settings.service_login_fb = dict(app='cbs20', controller='users', function='authentication_fb')
settings.service_login_gg = dict(app='cbs20', controller='users', function='authentication_gg')
settings.service_category_top_item = dict(app='cbs20', controller='product', function='category_top_product')
settings.service_solr_search = dict(app='cbs20', controller='solr', function='search_from_app')
settings.service_product_by_creator = dict(app='cbs20', controller='product', function='get_product_by_creator')
settings.service_product_by_cp = dict(app='cbs20', controller='product', function='get_product_by_cp')
settings.service_product_by_publisher = dict(app='cbs20', controller='product', function='get_product_by_publisher')
settings.service_auto_get_relation = dict(app='cbs20', controller='product', function='auto_get_relation')
settings.service_set_info = dict(app='cbs20', controller='set_product', function='info')
settings.service_check_preview = dict(app='cbs20', controller='download_preview', function='check_available')
settings.service_gcv_thiquocgia = dict(app='cbs20', controller='gcv', function='thiquocgia')
settings.service_gcv_pay_tqg = dict(app='cbs20', controller='gcv', function='pay_tqg')
settings.service_payment_code = dict(app='cbs20', controller='gcv', function='payment_code')
settings.service_tranfer_thiquocgia = dict(app='cbs20', controller='users', function='thiquocgia_tranfer_fund')
settings.service_tqg_tranfer_pay = dict(app='cbs20', controller='users', function='tqg_tranfer_pay')
settings.service_tranfer_to_tqg = dict(app='cbs', controller='users', function='tranfer_to_tqg')
settings.service_tranfer_to_third = dict(app='cbs', controller='users', function='tranfer_to_third')
settings.service_chuyen_de = dict(app='cbs20', controller='chuyen_de', function='get_all')
settings.service_bai_tap_chuyen_de = dict(app='cbs20', controller='chuyen_de', function='baitap_info')
settings.service_auto_login = dict(app='cbs20', controller='thiquocgia', function='auto_login')
settings.service_auto_login_third = dict(app='cbs20', controller='thiquocgia', function='auto_login_third')
settings.service_sum_pay_tqg = dict(app='cbs20', controller='thiquocgia', function='sum_pay_tqg')
settings.service_check_tvt_code = dict(app='cba', controller='promotion', function='check_tvt_code')
settings.service_get_exam = dict(app='cba', controller='thithu', function='get_exam')
settings.service_get_active_exam = dict(app='cba', controller='thithu', function='get_active_axam')
settings.service_changepass = dict(app='cbs', controller='users', function='changepwd')

settings.captchas_client = 'classbook_vn'
settings.captchas_secret = 'xUU0mDyhO6W0nJtYlLCUhlXOReo9FxndlncVRnfa'
settings.captchas_alphabet = 'abcdefghkmnopqrstuvwxyz'
settings.captchas_letters = 3
settings.captchas_width = 100
settings.captchas_height = 80

settings.tvid_login_url = "http://testid.mcgame.vn:2013/au/login.htm"
settings.tvid_logout_url = "http://testid.mcgame.vn:2013/au/logout.htm"
settings.tvid_register_url = "http://testid.mcgame.vn:2013/au/register.htm"

settings.nl_version = "3.1"
settings.nl_function = "SetExpressCheckout"

settings.nl_card_function = "CardCharge"
settings.nl_card_version = "2.0"
