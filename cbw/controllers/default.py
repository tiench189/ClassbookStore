# -*- coding: utf-8 -*-
import os
import sys
import json
import requests

max_free = 12
is_khuyen_mai = True

if session.authorized and session.expired is False and request.function != "nganluong_mobile":
    _profile = service_user_info(session.username)
    if _profile is None or 'error' in _profile:
        if _profile is not None and 'error' in _profile:
            session.expired = True
            redirect(URL(f="signup", vars={'show_login': True, 'location': URL()}))


def signin():
    response.title = u"Đăng nhập - Sách giáo khoa điện tử Classbook"
    categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    location = "/"
    if "location" in request.vars:
        location = request.vars['location']
    return dict(location=location)


def category():
    try:
        create_session_cart()
        # menu = service_category_get()
        # if menu is not None and not 'error' in menu:
        #     session.categories = menu['categories']

        if 't' in request.vars and 'u' in request.vars:
            token = request.vars['t']
            username = request.vars['u']
            login_result = service_user_auth_by_token(username, token)
            if login_result is None or 'error' in login_result:
                session.login_fail = True
            else:
                # print 'login success'
                session.authorized = True
                session.expired = False
                session.token = login_result['token']
                session.username = request.vars['u']
                profile_result = service_user_info(session.username)
                session.display_name = profile_result['items']['email']
                session.userfund = price2str(str(profile_result['items']['fund']))

        m_args = list()
        category_id = request.args[1]
        page = 0
        item_per_page = 15
        if len(request.args) > 2:
            page = request.args[2]
        m_args.append(category_id)
        m_args.append(page)
        m_args.append(item_per_page)
        #print(m_args)
        products = service_product_get(m_args)
        #print(products)
        for index in range(0, len(products['products'])):
            # products['products'][index]['product_cover'] = URL(a='cbs', c='download', f='thumb',
            #      scheme=True, host=False, args=products['products'][index]['product_code'])
            products['products'][index]['product_cover'] = "/static/covers/" + \
                                                           products['products'][index]['product_code'] + "/thumb.png"
        cate_parent = dict()
        cate_child = dict()
        for parent in get_menu():
            for child in parent['children']:
                if child['category_id'] == int(category_id):
                    cate_parent = parent
                    cate_child = child
                else:
                    for c in child['children']:
                        if c['category_id'] == int(category_id):
                            cate_parent = child
                            cate_child = c
        response.title = cate_child['category_name'] + u" - Sách giáo khoa điện tử Classbook"
        return dict(products=products, cate_child=cate_child, cate_parent=cate_parent)
    except Exception as err:
        print "ERROR: " + str(err) + " on line: " + str(sys.exc_traceback.tb_lineno)
        return dict(err=err)


@request.restful()
def country():
    response.view = 'generic.json'

    def GET(*args, **vars):
        try:
            country = service_country_get()

            if country:
                country = country['items']
                res = dict(countrys=country)
                return res if res is not None else dict()
            else:
                return dict()
        except Exception as e:
            return e

    return locals()


@request.restful()
def province():
    response.view = 'generic.json'

    def GET(*args, **vars):
        try:
            province = service_province_get()

            if province:
                province = province['items']
                res = dict(provinces=province)
                return res if res is not None else dict()
            else:
                return dict()
        except Exception as e:
            return e

    return locals()


@request.restful()
def district():
    response.view = 'generic.json'

    def GET(*args, **vars):
        try:
            if args:
                province_id = args[0]
                district = service_province_get_district(province_id)
            else:
                district = service_district_get()

            district = district['items']
            res = dict(districts=district)
            return res if res is not None else dict()
        except Exception as e:
            return e

    return locals()


@request.restful()
def subjects():
    response.view = 'generic.json'

    def GET(*args, **vars):
        try:
            subjects = service_subject_get()

            if subjects:
                subjects = subjects['items']
                res = dict(subjects=subjects)
                return res if res is not None else dict()
            else:
                return dict()
        except Exception as e:
            return e

    return locals()


@request.restful()
def classes():
    response.view = 'generic.json'

    def GET(*args, **vars):
        try:
            if args:
                subject_id = args[0]
                classes = service_subject_get_classes(subject_id)
            else:
                classes = service_classes_get()

            classes = classes['items']

            res = dict(classes=classes)
            return res if res is not None else dict()
        except Exception as e:
            return e

    return locals()


@request.restful()
def quiz():
    response.view = 'generic.json'

    def GET(*args, **vars):
        try:
            quizs = service_product_getquiz(args)

            quizs = quizs['products']
            quizs = dict(quizs=quizs)
            return quizs if quizs is not None else dict()
        except Exception as e:
            return e

    return locals()


def search():
    response.title = u"Tìm kiếm - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    item_per_page = 18
    products = list()
    is_search = False
    category_id = 0
    subject_id = 0
    class_id = 0
    keyword = ""
    page = 0
    total_item = 0
    total_page = 0

    # get category
    category = list()
    categories_search = service_category_getall()
    if categories_search is not None and not 'error' in categories_search:
        category = categories_search['categories']
        temp = dict()
        temp['category_id'] = 0
        temp['category_name'] = "- Tất cả -"
        category.insert(0, temp)

    # get subjects
    subjects = list()
    subjects_search = service_subject_get()
    if subjects_search is not None and not 'error' in subjects_search:
        subjects = subjects_search['items']
        temp = dict()
        temp['id'] = 0
        temp['subject_name'] = "- Tất cả -"
        subjects.insert(0, temp)

    # get class
    classes = list()
    classes_search = service_classes_get()
    if classes_search is not None and not 'error' in classes_search:
        classes = classes_search['items']
        temp = dict()
        temp['id'] = 0
        temp['class_name'] = "- Tất cả -"
        classes.insert(0, temp)
    if request.vars:
        vars = dict()
        if "keyword" in request.vars and request.vars.keyword.strip() != "":
            keyword = request.vars.keyword
            vars['key'] = keyword
        if "category_id" in request.vars and request.vars.category_id != "0":
            category_id = request.vars.category_id
            vars['category_id'] = category_id
        if "subject_id" in request.vars and request.vars.subject_id != "0":
            subject_id = request.vars.subject_id
            vars['subject_id'] = subject_id
        if "class_id" in request.vars and request.vars.class_id != "0":
            class_id = request.vars.class_id
            vars['class_id'] = class_id
        if "page" in request.vars:
            page = int(request.vars.page)
        if len(vars) > 0:
            is_search = True
        vars['start'] = page * item_per_page
        vars['row'] = item_per_page
        if is_search:
            solr_products = service_solr_search(vars)
            products = solr_products['docs']
            total_item = solr_products['numFound']
            total_page = int(solr_products['numFound'] / item_per_page) + 1
            for index in range(0, len(products)):
                # products[index]['product_cover'] = URL(a='cbs', c='download', f='thumb',
                #         scheme=True, host=False, args=products[index]['product_code'])
                products[index]['product_cover'] = "/static/covers/" + products[index]['product_code'] + "/thumb.png"
                products[index]['creator_name'] = products[index]['product_creator']

    return dict(products=products, is_search=is_search, category_id=category_id, subject_id=subject_id,
                class_id=class_id, keyword=keyword,
                category=category, subjects=subjects, classes=classes, total_item=total_item, total_page=total_page,
                page=page)


@request.restful()
def product():
    response.view = 'generic.json'

    def GET(*args, **vars):
        if args[0] == settings.service_product_search["function"]:  # and 'store_search' in vars:
            products = service_product_search_advance(args[1:], vars)

            # print 'cbw: search done'

            if products:
                for index in range(0, len(products["products"])):
                    products["products"][index]['product_cover'] = URL('cbs', 'download', 'thumb',
                                                                       args=products["products"][index]['product_code'])
                    try:
                        products["products"][index]["free"] = dict(result=products["products"][index]["free"])
                    except Exception as err:
                        products["products"][index]["free"] = dict(result=False)
                    # products["products"][index]["free"] = products["products"][index]["free"]["result"]
                    products["products"][index]['product_price'] = str2price(
                        str(products["products"][index]['product_price']))
                    #                     print "-----------------------------"
                    #                     print products["products"][index]
                    #                     print "-----------------------------"
                    if products["products"][index] and 'cover_price' in products["products"][index] and \
                                    products["products"][index]['cover_price'] != 0 and products["products"][index][
                        'cover_price'] != '':
                        products["products"][index]['cover_price'] = str2price(
                            str(products["products"][index]['cover_price']))
            return products if products is not None else dict()

        products = service_product_get(args)
        if products is None:
            return dict()

        for index in range(0, len(products["products"])):
            products["products"][index]['product_cover'] = URL('cbs', 'download', 'thumb',
                                                               args=products["products"][index]['product_code'])
            products["products"][index]["free"] = dict(result=products["products"][index]["free"])
            # products["products"][index]["free"] = products["products"][index]["free"]["result"]
            products["products"][index]['product_price'] = str2price(str(products["products"][index]['product_price']))
            if 'cover_price' in products["products"][index]:
                if products["products"][index]['cover_price'] != 0 and products["products"][index]['cover_price'] != '':
                    products["products"][index]['cover_price'] = str2price(
                        str(products["products"][index]['cover_price']))

        return products if products is not None else dict()

    return locals()


###CONTROLLERS###


def bao_tri():
    return dict()


def error():
    """
    handle error pages
    """
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    response.generic_patterns = ['*']
    response.title = "Thông báo lỗi"
    create_session_cart()
    if "code" in request.vars and request.vars.request_url != request.url:
        code = request.vars.code
        response.status = int(code)

        # show custom error message and view
        if not session.error is None:
            if "view" in session.error:
                response.view = session.error['view']
            message = session.error['message']
            del session.error
            if not message is None:
                return dict(request.vars, message=message)

        # default error handle
        if code == "500":
            if 'ticket' in request.vars:
                if str.startswith(request.client, '192.168.'):
                    url_ticket = URL(a="admin", c="default", f="ticket", args=request.vars["ticket"])
                    message = TAG("Server error! Check more info <a href='%s' target='_blank'>here</a>." % url_ticket)
                    return dict(message=message)
        elif code == "401":
            return dict(message=TAG("Bạn không có quyền truy cập! Quay trở về <a href='%s'>trang chủ</a>"
                                    % URL('index')))
        elif code == "404" or code == "400":
            return dict(message=TAG("Đường dẫn không tồn tại(%s)! Quay trở về <a href='%s'>trang chủ</a>"
                                    % (code, URL('index'))))

        return dict(message=TAG("Chức năng đang bảo trì(%s). Bạn có thể quay về <a href='%s'>trang chủ</a> hoặc "
                                "<a href='%s'>thông báo</a> với quản trị viên!"
                                % (code, URL('index'), URL('support_form'))))
    redirect(URL('index'))


def index():
    response.title = u"Sách giáo khoa điện tử Classbook"

    result_dict = dict()
    create_session_cart()
    # menu = service_category_get()
    # if menu is not None and not 'error' in menu:
    #     session.categories = menu['categories']
    # else:
    #     session.categories = dict()

    result_dict['cat_id'] = None
    home_topic = list()
    topic1 = dict()
    topic1['topic_name'] = 'Sách đáng chú ý'
    topic1['topic_id'] = 0
    topic1['topic_code'] = 'book_feature'
    topic1['type'] = 'book'
    topic1['items'] = list()
    home_topic.append(topic1)
    #
    select_topic = service_get_published_topic()['topics']
    for i in range(0, 2):
        topic = select_topic[i]
        temp = dict()
        temp['topic_name'] = topic['topic_name']
        temp['topic_id'] = topic['id']
        temp['topic_code'] = 'home_topic_item'
        temp['type'] = 'book'
        temp['items'] = list()
        home_topic.append(temp)
    #
    topic2 = dict()
    topic2['topic_name'] = 'Sách mới'
    topic2['topic_id'] = 0
    topic2['topic_code'] = 'book_new'
    topic2['type'] = 'book'
    topic2['items'] = list()
    home_topic.append(topic2)
    result_dict['home_topic'] = home_topic
    #
    topic3 = dict()
    topic3['topic_name'] = 'Sách bán chạy nhất'
    topic3['topic_id'] = 0
    topic3['topic_code'] = 'book_top_pay'
    topic3['type'] = 'book'
    topic3['items'] = list()
    home_topic.append(topic3)
    #
    for i in range(2, len(select_topic)):
        topic = select_topic[i]
        temp = dict()
        temp['topic_name'] = topic['topic_name']
        temp['topic_id'] = topic['id']
        temp['topic_code'] = 'home_topic_item'
        temp['type'] = 'book'
        temp['items'] = list()
        home_topic.append(temp)
    #
    topic4 = dict()
    topic4['topic_name'] = 'Ứng dụng nổi bật'
    topic4['topic_id'] = 0
    topic4['topic_code'] = 'app_feature'
    topic4['type'] = 'app'
    topic4['items'] = list()
    home_topic.append(topic4)
    #
    topic5 = dict()
    topic5['topic_name'] = 'Ứng dụng mới'
    topic5['topic_id'] = 0
    topic5['topic_code'] = 'app_new'
    topic5['type'] = 'app'
    topic5['items'] = list()
    home_topic.append(topic5)
    result_dict['home_topic'] = home_topic
    return result_dict


@request.restful()
def home_topic():
    response.view = 'generic.json'

    def GET(*args, **vars):
        products = list()
        topic_code = args[0]
        if topic_code == "book_feature":
            products = service_home_topic_item_get(1)
        elif topic_code == "book_new":
            products = service_product_top_new("Book")
        elif topic_code == "book_top_pay":
            products = service_product_top_pay("Book")
        elif topic_code == "app_feature":
            products = service_product_top_download("Application")
        elif topic_code == "app_new":
            products = service_product_top_new("Application")
        elif topic_code == "home_topic_item":
            topic_id = args[1]
            products = service_home_topic_item_get(topic_id)
        for i in range(0, len(products['items'])):
            products['items'][i]['product_price'] = str2price(
                str(products['items'][i]['product_price']))
            products['items'][i]['cover_price'] = str2price(
                str(products['items'][i]['cover_price']))
            products['items'][i]['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                        scheme=True, host=False,
                                                        args=products['items'][i]['product_code'])
            products['items'][i]['in_cart'] = True if str(
                products['items'][i]['product_id']) in session.shopping_cart else False
        return products

    return locals()


def home_product():
    create_session_cart()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    try:
        products = list()
        topic_code = request.args[0]
        topic_name = request.vars.topic
        response.title = u"Sách giáo khoa điện tử Classbook"
        if topic_code == "book_feature":
            products = service_home_topic_item_get(1)
        elif topic_code == "book_new":
            products = service_product_top_new("Book")
        elif topic_code == "book_top_pay":
            products = service_product_top_pay("Book")
        elif topic_code == "app_feature":
            products = service_product_top_download("Application")
        elif topic_code == "app_new":
            products = service_product_top_new("Application")
        elif topic_code == "home_topic_item":
            topic_id = request.args[1]
            products = service_home_topic_item_get(topic_id)
        # print(products)
        for i in range(0, len(products['items'])):
            products['items'][i]['product_price'] = str2price(
                str(products['items'][i]['product_price']))
            products['items'][i]['cover_price'] = str2price(
                str(products['items'][i]['cover_price']))
            # products['items'][i]['product_cover'] = URL(a='cbs', c='download', f='thumb',
            #         scheme=True, host=False, args=products['items'][i]['product_code'])
            products['items'][i]['product_cover'] = "/static/covers/" + \
                                                    products['items'][i]['product_code'] + "/thumb.png"
            products['items'][i]['in_cart'] = True if str(
                products['items'][i]['product_id']) in session.shopping_cart else False
    except Exception as err:
        print(err)
    return dict(products=products['items'], topic_name=topic_name)


def about():
    response.title = u"Giới thiệu - Sách giáo khoa điện tử Classbook"
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()
    return dict()


def manager():
    response.title = u"Phòng học tương tác - Sách giáo khoa điện tử Classbook"
    result_dict = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()
    return result_dict


def new():
    response.title = u"Tin tức - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    result_dict = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     # print('service_category_get')
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()
    link = "http://tintuc.classbook.vn/"
    if request.vars and "link" in request.vars:
        link = request.vars.link
    result_dict['link'] = link
    return result_dict


def support_manager():
    response.title = u"Phần mềm quản lý - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    result_dict = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     # print('service_category_get')
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()
    return result_dict


def support():
    response.title = u"Hỗ trợ - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    result_dict = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()
    return result_dict


def device():
    response.title = u"Thiết bị Classbook - Sách giáo khoa điện tử Classbook"
    redirect(URL(f="index"))
    result_dict = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     # print('service_category_get')
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()
    return result_dict


def cbapp_guide():
    response.title = u"Sách giáo khoa điện tử Classbook - Hướng dẫn sử dụng ứng dụng Classbook(Tablet, smartphone)"
    create_session_cart()
    return dict()


def store():
    redirect(URL(f="index"))


@request.restful()
def relation():
    response.view = 'generic.json'

    def GET(*args, **vars):
        products = list()
        product_id = args[0]
        products = service_product_relation(product_id)
        for i in range(0, len(products['products'])):
            products['products'][i]['product_price'] = str2price(
                str(products['products'][i]['product_price']))
            products['products'][i]['cover_price'] = str2price(
                str(products['products'][i]['cover_price']))
            products['products'][i]['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                           scheme=True, host=False,
                                                           args=products['products'][i]['product_code'])
            products['products'][i]['in_cart'] = True if str(
                products['products'][i]['id']) in session.shopping_cart else False
        return products

    return locals()


@request.restful()
def relation_auto():
    response.view = 'generic.json'

    def GET(*args, **vars):
        products = list()
        product_id = args[0]
        products = service_auto_get_relation(product_id)
        for i in range(0, len(products['products'])):
            products['products'][i]['product_price'] = str2price(
                str(products['products'][i]['product_price']))
            products['products'][i]['cover_price'] = str2price(
                str(products['products'][i]['cover_price']))
            products['products'][i]['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                           scheme=True, host=False,
                                                           args=products['products'][i]['product_code'])
            products['products'][i]['in_cart'] = True if str(
                products['products'][i]['id']) in session.shopping_cart else False
        return products

    return locals()


def store_detail():
    have_flash_preview = False
    ### Quiz
    create_session_cart()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()

    if request.args and len(request.args) < 3:
        if len(request.args) == 1:
            product_id = request.args[0]
        else:
            product_id = request.args[1]
        # print(product_id)
        rating = service_rating_get(product_id)
        if rating["status"] != 200:
            rating = dict(rating_score=0, rating_count=0)
        else:
            rating = json.loads(rating["data"])

        is_rated = service_rating_check(session.username, product_id)
        if not session.authorized or is_rated["status"] != 200:
            is_rated = True
        else:
            is_rated = False if is_rated["data"] == "0" else True

        info = service_product_all(product_id)
        if info is None or 'error' in info or not info['product']:
            if info is not None and 'error' in info:
                add_alert(title='Lỗi', content=info['error'])
            redirect(URL('index'))

        # info['product']['product_cover'] = URL('cbs', 'download', 'cover', args=info['product']['product_code'])
        info['product']['product_cover'] = '/static/covers/' + info['product']['product_code'] + "/cover.clsbi"
        response.title = info['product']['product_title'] + u" - " + info['product']['creator_name'][0] + \
                         u" - " + info['product']['publisher_name'] + u" - Sách giáo khoa điện tử Classbook Store"
        metadata = service_product_metadata(info['product']['id'])
        if metadata is None or 'error' in metadata:
            metadata = dict()

        has_preview = service_check_preview(info['product']['product_code'])['result']
        if os.path.isdir(os.path.join('applications', 'cbw', 'static', 'flash', info['product']['product_code'])):
            have_flash_preview = True
        check_buy = False
        check_media = False
        check_quiz = False
        if session.authorized:
            check_buy = check_buy_product(info['product']['id'])
            # print check_buy
            if check_buy and 'result' in check_buy:
                check_buy = check_buy['result']
            check_media = check_buy_media(info['product']['id'])
            if check_media and 'result' in check_media:
                check_media = check_media['result']
            check_quiz = check_buy_quiz(info['product']['id'])
            if check_quiz and 'result' in check_quiz:
                check_quiz = check_quiz['result']
        # data_price = service_get_data_price(product_id)
        # print(data_price)
        price_media = info['product']['media_price']
        price_quiz = info['product']['quiz_price']
        # if info['product']['has_quiz']:
        #     if 'quiz' in data_price:
        #         price_quiz = data_price['quiz']
        # if info['product']['has_media']:
        #     if 'media' in data_price:
        #         price_media = data_price['media']
        payment = dict(price_media=price_media, price_quiz=price_quiz)
        media_list = get_list_media(info['product']['product_code'])['media']
        # media_list = list()
        if info['product']['has_media'] and len(media_list) == 0:
            media = dict()
            media['type'] = "click"
            media['title'] = "Dữ liệu tương tác"
            media['page'] = ""
            media_list.append(media)
        return dict(info=info['product'],
                    metadata=metadata, is_rated=is_rated,
                    rating_score=rating['rating_score'], rating_count=rating['rating_count'],
                    have_flash_preview=have_flash_preview, payment=payment,
                    media_list=media_list, check_buy=check_buy, check_media=check_media,
                    check_quiz=check_quiz, has_preview=has_preview)
    else:
        redirect(URL('index'))
    return dict()


def support_form():
    response.title = u"Phản hồi - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    hoten = request.vars['ho_ten']
    dienthoai = request.vars['dien_thoai']
    tieu_de = request.vars['tieu_de']
    noi_dung = request.vars['noi_dung']
    email = request.vars['email']

    captchas = get_captchas_object()
    captchas_random = request.vars['captchas_random']
    captchas_value = request.vars['captchas_value']
    captchas_result = 0

    question_types = request.vars['question_types']

    result_dict = dict(captchas_random=captchas.random(),
                       captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654')
    # questionTypes = db(db.contact_category.id > 0).select(db.contact_category.ALL)
    if (email is not None) and (noi_dung is not None) and (email != "") and (noi_dung != ""):
        captchas_result = validate_captchas(captchas, captchas_random, captchas_value)
        if captchas_result == 0:
            mes = service_user_send_message(email, hoten, dienthoai, question_types, tieu_de, noi_dung)
            if mes is None or 'error' in mes:
                if mes is not None and 'error' in mes:
                    add_alert(title="Lỗi", content=mes['error'])
                else:
                    add_alert(title="Lỗi", content="Có lỗi xảy ra trong quá trình gửi dữ liệu!")
            else:
                add_alert(title='Thông báo', content="Gửi thành công!")
        else:
            add_alert(title='Lỗi', content="Mã không hợp lệ!")
    result_dict['captchas_result'] = captchas_result
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    return result_dict


def download():
    response.title = u"Sách giáo khoa điện tử Classbook"
    result_dict = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    return result_dict


def signup():
    # register.json?username=&password=&firstName=&lastName=&email=&phoneNumber=&address=
    response.title = u"Đăng kí tài khoản - Sách giáo khoa điện tử Classbook"
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']

    fname = ""
    lname = ""
    dienthoai = ""
    diachi = ""
    email = request.vars['email']
    matkhau = request.vars['password']
    district = 5
    # print(request.vars)

    captchas = get_captchas_object()
    captchas_random = request.vars['captchas_random']
    captchas_value = request.vars['captchas_value']
    captchas_result = 0

    result = ""
    if email is not None:
        # print request.vars
        captchas_result = validate_captchas(captchas, captchas_random, captchas_value)
        if captchas_result == 0:
            if lname == "":
                lname = "User"
            if fname == "":
                fname = "Guest"
            register = service_user_register(email, matkhau, email, fname, lname, dienthoai, diachi, district)
            if register is None or 'error' in register:
                result = 'Email %s đã được sử dụng. Xin dùng email khác!' % email
            else:
                result = 'Chúc mừng bạn đã đăng kí tài khoản %s thành công' % email
    location = URL(f='index')
    if "location" in request.vars:
        location = request.vars['location']

    return dict(result=result, captchas_result=captchas_result, captchas_random=captchas.random(),
                captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654', location=location)


from datetime import datetime


def warranty_adddevice():
    response.title = u"Đăng kí bảo hành - Sách giáo khoa điện tử Classbook"
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    model = request.vars['model']
    serial = request.vars['serial']
    retype_serial = request.vars['retype_serial']
    fullname = request.vars['fullname']
    dienthoai = request.vars['dien_thoai']
    diachi = request.vars['address']
    email = request.vars['email']
    ngay_mua = request.vars['purchase_date']
    if ngay_mua:
        ngay_mua = datetime.strptime(ngay_mua, "%d/%m/%Y")

    captchas = get_captchas_object()
    captchas_random = request.vars['captchas_random']
    captchas_value = request.vars['captchas_value']
    captchas_result = 0

    result = ""

    if serial is None:
        return dict(result=result, cb_model=CB_MODEL, captchas_result=captchas_result,
                    captchas_random=captchas.random(),
                    captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654')

    captchas_result = validate_captchas(captchas, captchas_random, captchas_value)
    if captchas_result == 0:
        if serial != retype_serial:
            result = 'Serial không giống nhau. Đề nghị kiểm tra lại!'
        else:
            device_serial = service_device(serial)
            registed_serial = service_device_registed(serial)['item']

            if not device_serial:
                result = 'Error: ' + serial
                return dict(result=result, cb_model=CB_MODEL, captchas_result=captchas_result,
                            captchas_random=captchas.random(),
                            captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654')

            if device_serial and 'error' in device_serial:
                result = u'Error ' + device_serial['error']
                return dict(result=result, cb_model=CB_MODEL, captchas_result=captchas_result,
                            captchas_random=captchas.random(),
                            captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654')

            if not registed_serial and device_serial and 'error' not in device_serial:

                register = service_user_add_device(model + "-" + serial, fullname, dienthoai, email, diachi, ngay_mua)
                if register is None:
                    result = 'Error: ' + serial
                elif register and 'error' in register:
                    result = u'Error ' + register['error']
                else:
                    result = u'Đăng kí bảo hành thành công!'
            elif registed_serial:
                result = u'Thiết bị đã đăng kí bảo hành!'

    return dict(result=result, cb_model=CB_MODEL, captchas_result=captchas_result, captchas_random=captchas.random(),
                captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654')


def logout():
    session.authorized = False
    session.token = ""


def user_info():
    response.generic_patterns = ['*']
    if session.authorized:
        profile_result = service_user_info(session.username)
        session.email = profile_result['items']['email']
        session.userfund = price2str(str(profile_result['items']['fund']))
        session.userid = str(profile_result['items']['id'])
        return dict(email=session.email, fund=session.userfund)
    else:
        return dict()

def trashses():
    from gluon import current
    sessions = []
    table = current.response.session_db_table
    if table:
        for row in table._db(table.id > 0).select():
            sessions.append(row)
    return dict(a=sessions)

def login():


    response.generic_patterns = ['*']
    try:
        if "type" in request.vars:
            if request.vars['type'] == "fb":
                login_result = service_login_fb(request.vars['access_token'])
            elif request.vars['type'] == "gg":
                login_result = service_login_gg(request.vars['access_token'])
        else:
            login_result = service_user_auth(request.vars['username'], request.vars['password'])
        back_location = "/"
        if login_result is None or 'error' in login_result:
            session.login_fail = True
            return dict(result=False, mess=login_result['error'])
        else:
            session.authorized = True
            session.expired = False
            session.token = login_result['token']
            session.username = request.vars.username
            if "type" in request.vars:
                session.username = login_result['username']

            profile_result = service_user_info(session.username)
            # print("profile: " + str(profile_result))
            session.display_name = profile_result['items']['email']
            if "type" in request.vars:
                session.display_name = profile_result['items']['firstName'] + " " + profile_result['items']['lastName']
            session.email = profile_result['items']['email']
            session.userfund = price2str(str(profile_result['items']['fund']))
            session.password = request.vars['password']
            session.userid = str(profile_result['items']['id'])
        if "location" in request.vars:
            back_location = request.vars["location"]
        if "type" in request.vars:
            redirect(back_location)
        else:
            return dict(result=True, location=back_location)
    except Exception as err:
        return dict(err=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno), profile_result=profile_result)


def change_device_name():
    change_result = service_change_device_name(request.vars['deviceSerial'], request.vars['new_device_name'])

    back_location = URL("profile")
    redirect(back_location)


# @request.restful()
def get_list_user_device():
    try:
        user_device_list = service_get_list_user_device(session.username, session.token)
        # print "Fukciong " + str(user_device_list)
        return dict(user_device_list=user_device_list['items'])
        return None
    except Exception as e:
        print e


def check_login():
    if session.authorized:
        return 1
    return 0


def profile_bk():
    response.title = u"Thông tin cá nhân - Sách giáo khoa điện tử  Classbook"
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    if not session.authorized:
        redirect(URL(f="signin", vars={'show_login': True}))

    if request.vars:
        service_user_update(session.username, request.vars['first_name'],
                            request.vars['last_name'], request.vars['phone'],
                            request.vars['address'])

    profile_result = service_user_info(session.username)
    if profile_result is None or 'error' in profile_result:
        if profile_result is not None and profile_result['error']:
            session.authorized = False
        return dict()
    else:
        download_result = service_user_download(session.username)
        if download_result is None or 'error' in download_result:
            download_result = None

        war_history = service_get_warranty_history(session.username, session.token)

        if war_history is None or not "result" in war_history:
            war_history = list()
        else:
            war_history = war_history["result"]

        user_device_list = service_get_list_user_device(session.username, session.token)
        # print 'ac'
        # print user_device_list

        user_fund = price2str(str(profile_result['items']['fund']))
        session.userfund = user_fund
        return dict(user=profile_result['items'], download=download_result['items'],
                    user_fund=user_fund, history=war_history, user_device_list=user_device_list['items'])


def profile():
    response.title = u"Thông tin cá nhân - Sách giáo khoa điện tử  Classbook"
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    if not session.authorized:
        redirect(URL(f="signin", vars={'location': "profile():"}))

    if request.vars:
        service_user_update(session.username, "",
                            request.vars['fullName'], request.vars['phoneNumber'],
                            request.vars['address'])

    profile_result = service_user_info(session.username)
    if profile_result is None or 'error' in profile_result:
        if profile_result is not None and profile_result['error']:
            session.authorized = False
        redirect(URL(f="signin", vars={'location': "profile():"}))
    user_fund = price2str(str(profile_result['items']['fund']))
    session.userfund = user_fund
    return dict(user=profile_result['items'],
                user_fund=user_fund)


def all_user_device():
    response.title = u"Danh sách thiết bị - Sách giáo khoa điện tử  Classbook"
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    if not session.authorized:
        redirect(URL(f="signin", vars={'location': "all_user_device"}))

    profile_result = service_user_info(session.username)
    if profile_result is None or 'error' in profile_result:
        if profile_result is not None and profile_result['error']:
            session.authorized = False
        redirect(URL(f="signin", vars={'location': "all_user_device"}))
    else:
        user_device_list = service_get_list_user_device(session.username, session.token)

        user_fund = price2str(str(profile_result['items']['fund']))
        session.userfund = user_fund
        return dict(user=profile_result['items'],
                    user_fund=user_fund, user_device_list=user_device_list['items'])


def download_history():
    response.title = u"Lịch sử tải - Sách giáo khoa điện tử  Classbook"
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    if not session.authorized:
        redirect(URL(f="signin", vars={'location': "download_history"}))

    if request.vars:
        service_user_update(session.username, request.vars['first_name'],
                            request.vars['last_name'], request.vars['phone'],
                            request.vars['address'])

    profile_result = service_user_info(session.username)
    if profile_result is None or 'error' in profile_result:
        if profile_result is not None and profile_result['error']:
            session.authorized = False
        redirect(URL(f="signin", vars={'location': "download_history"}))
        return dict()
    else:
        download_result = service_user_download(session.username)
        if download_result is None or 'error' in download_result:
            download_result = None

        user_fund = price2str(str(profile_result['items']['fund']))
        session.userfund = user_fund
        return dict(user=profile_result['items'], download=download_result['items'],
                    user_fund=user_fund)


@request.restful()
def get_user_profile():
    profile_result = service_user_info(session.username)
    if profile_result is None or 'error' in profile_result:
        if profile_result is not None and profile_result['error']:
            session.authorized = False
        return dict()

    return dict(user=profile_result['items'])


def is_classbook_device():
    device_serial = request.vars.device_serial

    profile_result = service_get_device_detail(device_serial)

    return dict(profile_result=profile_result['device_detail'])


def warranty():
    field = request.vars.field
    value = request.vars.field_value

    warranty_history = service_user_get_warranty_history(session.username, field, value)
    #     print warranty_history
    if warranty_history is None or 'error' in warranty_history:
        if warranty_history is not None and warranty_history['error'] == 'CB_0012:ERR_TOKEN':
            session.authorized = False
        redirect(URL(f="index"))
    return dict(warranty=warranty_history['items'])


def order():
    redirect("http://dathang.classbook.vn/")
    response.title = u"Sách giáo khoa điện tử Classbook - Đặt hàng"
    hoten = request.vars['ho_ten']
    dienthoai = request.vars['dien_thoai']
    dia_chi = request.vars['dia_chi']
    noi_dung = request.vars['noi_dung']
    if not request.vars['email']:
        email = ''
    else:
        email = request.vars['email']
    province = request.vars['province']
    district = request.vars['district']
    if not request.vars['number_devices']:
        number_devices = 0
    else:
        number_devices = request.vars['number_devices']

    captchas = get_captchas_object()
    captchas_random = request.vars['captchas_random']
    captchas_value = request.vars['captchas_value']
    captchas_error = 0

    cb_price = service_get_cb_price()
    cb_price = cb_price['cb_price']
    provices = service_province_get()
    districts = service_district_get()
    if ((dienthoai is not None) and (dienthoai != "") and (hoten is not None) and (hoten != "") and (
                noi_dung is not None) and (noi_dung != "") and (province is not None) and (province != "")):
        captchas_error = validate_captchas(captchas, captchas_random, captchas_value)
        if captchas_error == 0:
            mes = service_order_send(email, hoten, dienthoai, number_devices, dia_chi, noi_dung, province, district)
            if mes is None or 'error' in mes:
                if mes is not None and 'error' in mes:
                    add_alert(title='Lỗi', content=mes['error'])
                add_alert(title='Lỗi', content="Có lỗi xảy ra trong quá trình gửi dữ liệu! ")
            else:
                add_alert(title='Thông báo', content="Cảm ơn quý khách, yêu cầu của quý khách đã được gửi thành công! ")
    return dict(items="", cb_price=cb_price, provinces=provices, districts=districts, captchas_error=captchas_error,
                captchas_random=captchas.random(),
                captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654')


def comment():
    #     print 'r1'
    #     print request.vars
    response.title = u"Bình luận - Sách giáo khoa điện tử Classbook"
    #     print HTML('<b>Test</b>')
    if not request.vars['binh_luan']:
        binh_luan = None
    else:
        binh_luan = request.vars['binh_luan']
    status = 'NEW'
    product_code = request.vars['product_code']
    product_title = request.vars['product_title']

    if not request.vars['email']:
        email = None
    else:
        email = request.vars['email']

    captchas = get_captchas_object()
    captchas_random = request.vars['captchas_random']
    captchas_value = request.vars['captchas_value']
    captchas_error = 0

    if (binh_luan is not None) and (binh_luan != "") and (email is not None) and (email != ""):
        captchas_error = validate_captchas(captchas, captchas_random, captchas_value)
        if captchas_error == 0:
            mes = service_comment_send(email, binh_luan, product_code, status)
            if mes is None or 'error' in mes:
                if mes is not None and 'error' in mes:
                    add_alert(title='Lỗi', content=mes['error'])
                add_alert(title='Lỗi', content="Có lỗi xảy ra trong quá trình gửi dữ liệu!")
            else:
                add_alert(title='Thông báo', content="Cảm ơn quý khách đã gửi lời bình luận!")
                #                 request.vars['captcha'] = None
                #                 print 'r2'
                #                 print request.vars
                #                 print '-------------------------'
                d = dict(product_code=product_code, product_title=product_title, email=None, binh_luan=None,
                         captchas_error=captchas_error, captchas_random=captchas.random(),
                         captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654')
                return d

    d = dict(product_code=product_code, product_title=product_title, email=email, binh_luan=binh_luan,
             captchas_error=captchas_error, captchas_random=captchas.random(),
             captchas_image=captchas.image_url().replace('&amp;', '&') + '&color=123654')
    return d


@request.restful()
def get_comments():
    response.view = 'generic.json'

    def GET(*args):
        comments = service_comment_info(args[0: len(args)])
        return comments if comments is not None else dict()

    return locals()


@request.restful()
def rating():
    response.view = 'generic.json'

    def GET(**vags):
        if len(vags) == 2 and "product_id" in vags and "score" in vags:
            try:
                product_id = int(vags["product_id"])
                score = int(vags["score"])
                score = 5 if score > 5 else score
            except ValueError:
                return dict(error="Parameters is invalid!")
            result = service_rating_rate(session.username, session.token, product_id, score)
            if result["status"] != 200:
                return dict(error="Error!")
            else:
                return result["data"]
        return dict(error="Parameters is invalid!")

    return locals()


def nganluong_mobile():
    response.title = u"Sách giáo khoa điện tử Classbook - Nạp tiền"
    purchase_type = ""
    email = ""
    package = ""
    pack_type = ""
    if len(request.args) == 1 and request.args[0] == "canceled":
        pass
    elif len(request.vars) > 0:
        if "nlpayment" in request.vars:
            bank_code = ""
            if "bankcode" in request.vars:
                bank_code = request.vars.bankcode

            rs = service_transaction_checkout(session.username, session.token, request.vars.option_payment,
                                              bank_code, request.vars.buyer_amount, "test",
                                              URL(f="nganluong_mobile", host=True, scheme=True),
                                              URL(f="nganluong_mobile", args="canceled", host=True, scheme=True),
                                              purchase_type, package, email, pack_type)
            if rs is not None:
                if rs["status"] != 200:
                    add_alert(title='Lỗi', content=rs["data"])
                    # redirect(URL(f="index"))
                else:
                    redirect(rs["data"])
        elif "NLNapThe" in request.vars:
            pin_card = request.vars.txtSoPin
            card_serial = request.vars.txtSoSeri
            type_card = request.vars.select_method

            rs = service_transaction_cardpay(session.username, session.token, pin_card, card_serial, type_card)
            if rs is not None:
                if rs["status"] != 200:
                    add_alert(title='Lỗi', content=rs["data"])
                    # redirect(URL(f="index"))
                else:
                    # print(rs["data"])
                    add_alert(title='Thông báo', content="Nạp tiền thành công!")
                    redirect(URL(f="profile"))
        elif "token" in request.vars:
            rs = service_transaction_confirm(session.username, session.token, request.vars.token)
            if rs is not None:
                if rs["status"] != 200:
                    add_alert(title='Lỗi', content=rs["data"])
                    # redirect(URL(f="index"))
                else:
                    add_alert(title='Thông báo', content="Nạp tiền thành công!")
                    redirect(URL(f="profile"))
    elif len(request.args) == 2:
        session.username = request.args[0]
        session.token = request.args[1]
    else:
        raise HTTP(404, "Trang không tồn tại")

    return dict()


def confirm_password():
    result = service_confirm_password(request.vars['password'], session.username, session.token)

    if 'error' in result:
        return dict(result='error')

    return dict(result='ok')


def buy_book():
    product_id = request.vars.product_id
    result = service_confirm_password(request.vars['password'], session.username, session.token)

    if 'error' in result:
        session.err_message = result['error']
    else:
        session.err_message = ''

    redirect(URL(f="store_detail", args=product_id))


def delete_device():
    password = request.vars['password']
    device_serial = request.vars['device_serial']

    #print request.vars

    # check password valid
    confirm_password_result = service_confirm_password(password, session.username, session.token)
    if 'error' in confirm_password_result:
        session.delete_devices_message = confirm_password_result['error']

    # delete_device
    delete_device_result = service_delete_device(session.username, device_serial, session.token)
    # print delete_device_result
    if 'error' in delete_device_result:
        session.delete_devices_message = delete_device_result['error']
    redirect(URL(f='profile'))


def forgotpwd():
    response.title = u"Lấy lại mật khẩu - Sách giáo khoa điện tử Classbook"
    # print request.args
    try:
        err = None
        token_rs_pwd = None
        if len(request.args) < 1:
            dict(isOk=False)

        if len(request.args) == 1:
            err = ''
            token_rs_pwd = request.args[0]
            is_ok = service_verify_token_rspwd(token_rs_pwd)

        if request.vars:
            new_pass = request.vars['newPwd']
            token = request.vars['token_rs_pwd']
            is_ok = service_renew_pwd(token, new_pass)
            # redirect(URL(f='store'))
    except Exception as e:
        print str(e)
        err = 'Đã có lỗi xảy ra, vui lòng thử lại sau.'
    return dict(isOk=is_ok['result'], token_rs=token_rs_pwd, err=err)


##########################Tiench##########################################
def service():
    try:
        response.generic_patterns = ['*']
        action = request.args[0]
        result = dict()
        # print(action)
        if action == "buy_product":
            args = [request.args[1], 'WEB.MOBILE', session.token]
            if len(request.args) > 2:
                args.append(request.args[2])
            result = service_buy_product(args)
        if action == "buy_product_divide":
            args = [request.args[1], 'WEB.MOBILE', session.token, request.args[2], int(request.args[3])]
            # print(args)
            result = service_buy_product_divide(args)
        if action == "check_payment":
            args = [request.args[1], session.token, 'beta']
            if len(request.args) > 2:
                args.append(request.args[2])
            result = service_check_payment(args)
        if action == "check_classbook":
            result = service_check_classbook_device(request.vars['device_serial'])
        return result
    except Exception as e:
        return dict(error="Service error:" + e.message)


##########Shopping cart##############
def add_to_cart():  # product_id
    try:
        response.generic_patterns = ['*']
        if request.args:
            product_id = request.args[0]
            # print(product_id)
            if session.shopping_cart:
                if product_id in session.shopping_cart:
                    return dict(err='Ấn phẩm đã trong giỏ hàng rồi')
                else:
                    session.shopping_cart.append(product_id)
            else:
                session.shopping_cart = list()
                session.shopping_cart.append(product_id)
            return dict(result='success')
    except Exception as err:
        print "ERROR: " + str(err)
        return dict(err=err)


def remove_from_cart():  # product_id
    try:
        response.generic_patterns = ['*']
        product_id = request.args[0]
        if product_id in session.shopping_cart:
            session.shopping_cart.remove(product_id)
            return dict(result='success')
        else:
            return dict(err="not in")
    except Exception as err:
        print "ERROR: " + str(err)
        return dict(err=err)


def shoppingcart():
    try:
        login = False;
        if request.args and 'login' in request.args:
            login = True
        response.title = u"Sách giáo khoa điện tử Classbook Store - Giỏ hàng"
        list_products = list()
        relations = list()
        list_id_relation = list()
        # print(session.shopping_cart)
        list_products = get_detail_list(session.shopping_cart, dict(token=session.token))['product']
        for cart_id in session.shopping_cart:
            # get ralation
            relation = service_product_relation(cart_id)
            # remake cover link else the link will have localhost and it make an error
            relation_item = relation['products']
            for index in range(0, len(relation_item)):
                relation_item[index]['product_cover'] = URL('cbs', 'download', 'thumb',
                                                            args=relation_item[index]['product_code'])

                relation_item[index]['product_price'] = str2price(str(relation_item[index]['product_price']))
                relation_item[index]['cover_price'] = str2price(str(relation_item[index]['cover_price']))
                if relation_item[index]['id'] not in list_id_relation \
                        and relation_item[index]['id'] not in session.shopping_cart:
                    relations.append(relation_item[index])
                    list_id_relation.append(relation_item[index]['id'])

        top_download = service_product_top_download("Book")
        if top_download is not None and not 'error' in top_download:
            for index in range(0, len(top_download['items'])):
                top_download['items'][index]['product_cover'] = URL('cbs', 'download', 'thumb',
                                                                    args=top_download['items'][index]['product_code'])
                top_download['items'][index]['product_price'] = str2price(
                    str(top_download['items'][index]['product_price']))
                top_download['items'][index]['cover_price'] = str2price(
                    str(top_download['items'][index]['cover_price']))
        # get relation
        # print "login:" + str(login)
        return dict(list_products=list_products, top_download=top_download['items'], relations=relations,
                    is_login=login)
    except Exception as err:
        print "ERROR: " + str(err) + " on line: " + str(sys.exc_traceback.tb_lineno)
        return dict(err=err)


def cart():
    try:
        create_session_cart()
        # categories = dict()
        # if not session.categories:
        #     menu = service_category_get()
        #     if menu is not None and not 'error' in menu:
        #         session.categories = menu['categories']
        response.title = u"Giỏ hàng - Sách giáo khoa điện tử Classbook Store"
        list_products = get_detail_list(session.shopping_cart, dict(token=session.token))['product']
        return dict(list_products=list_products)
    except Exception as err:
        print "ERROR: " + str(err) + " on line: " + str(sys.exc_traceback.tb_lineno)
        return dict(err=err)


def clear_cart():
    try:
        response.generic_patterns = ['*']
        session.shopping_cart = []
        if session.authorized:
            profile_result = service_user_info(session.username)
            session.email = profile_result['items']['email']
            session.userfund = price2str(str(profile_result['items']['fund']))
            session.userid = str(profile_result['items']['id'])
            return dict(email=session.email, fund=session.userfund)
        else:
            return dict()
    except Exception as err:
        print "ERROR: " + str(err)
        return dict(err=err)


def classroom_technical_specs():
    response.title = u"Sách giáo khoa điện tử Classbook - Thông số kĩ thuật"
    return dict()


def classroom_interactive():
    response.title = u"Sách giáo khoa điện tử Classbook - Nội dung tương tác"
    return dict()


def classroom_support():
    response.title = u"Sách giáo khoa điện tử Classbook - Hỗ trợ"
    return dict()


def forgot_password():
    response.title = u"Lấy lại mật khẩu - Sách giáo khoa điện tử Classbook"
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    return dict()


def nganluong():
    create_session_cart()
    categories = dict()
    fail_mess = "- Đề nghị liên lạc CSKH để được hỗ trợ. " + \
                "Số điện thoại: 047-302-0888"
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    purchase_type = ""
    email = ""
    package = ""
    pack_type = ""
    if "purchase_type" in request.vars:
        purchase_type = request.vars.purchase_type
        package = request.vars.package
        if purchase_type == "gift":
            email = request.vars.email
            pack_type = request.vars.type
    #print(purchase_type + "/" + email + "/" + package + "/" + pack_type)
    if 'autologin' in request.vars:
        token = request.vars['usertoken']
        username = request.vars['username']
        login_result = service_user_auth_by_token(username, token)
        if "site" in request.vars:
            site = request.vars.site
        back_location = URL("nganluong")  # request.env['http_referer']
        if login_result is None or 'error' in login_result:
            # print 'login fail'
            session.login_fail = True
        else:
            # print 'login success'
            session.authorized = True
            session.expired = False
            session.token = login_result['token']
            session.username = request.vars['username']
            profile_result = service_user_info(session.username)
            session.display_name = profile_result['items']['email']
            session.userfund = price2str(str(profile_result['items']['fund']))

    if not session.authorized:
        redirect(URL(f="signin", vars={'location': 'nganluong'}))

    response.title = u"Sách giáo khoa điện tử Classbook - Nạp tiền"

    if len(request.args) > 0 and request.args[0] == "canceled":
        pass
    elif len(request.vars) > 0:
        # print(request.vars)
        if "nlpayment" in request.vars:
            min_nl = 2000
            if request.vars.option_payment == "VISA":
                min_nl = 50000
            elif request.vars.option_payment == "ATM_ONLINE":
                min_nl = 10000
            if int(request.vars.buyer_amount.replace(".", "")) >= min_nl:
                bank_code = ""
                if "bankcode" in request.vars:
                    bank_code = request.vars.bankcode
                if request.vars.option_payment == "VISA":
                    bank_code = request.vars.bank_code
                rs = service_transaction_checkout(session.username, session.token, request.vars.option_payment,
                                                  bank_code, request.vars.buyer_amount, "test",
                                                  URL(f="nganluong", host=True, scheme=True),
                                                  URL(f="nganluong", args="canceled", host=True, scheme=True),
                                                  purchase_type, package, email, pack_type)
                if rs is not None:
                    if rs["status"] == 200:
                        redirect(rs["data"])
                    else:
                        add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)
            else:
                add_alert(title='Lỗi', content="Số tiền bạn muốn thanh toán nhỏ hơn số tiền tối thiểu là " + str(min_nl) + " VND nên giao dịch không thể thực hiện. " + fail_mess)
        elif "NLNapThe" in request.vars:
            pin_card = request.vars.txtSoPin
            card_serial = request.vars.txtSoSeri
            type_card = request.vars.select_method

            rs = service_transaction_cardpay(session.username, session.token, pin_card, card_serial, type_card,
                                             purchase_type, package, email, pack_type)
            #print(rs)
            session.report = ""
            if rs is not None:
                if rs["status"] == 200:
                    if "purchase_type" in request.vars:
                        check = service_check_elearning(username)
                        if check['check']:
                            if check['message'] == 'success':
                                redirect("http://thiquocgia.vn")
                            else:
                                add_alert(title='Thông báo', content=check['message'])
                    else:
                        add_alert(title='Thông báo', content="Nạp tiền thành công!")
                        redirect(URL(f="profile"))
                else:
                    add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)
        elif "token" in request.vars:
            rs = service_transaction_confirm(session.username, session.token, request.vars.token)
            if rs is not None:
                if rs["status"] == 200:
                    if "purchase_type" in request.vars:
                        check = service_check_elearning(username)
                        if check['check']:
                            if check['message'] == 'success':
                                redirect("http://thiquocgia.vn")
                            else:
                                add_alert(title='Thông báo', content=check['message'])
                    else:
                        add_alert(title='Thông báo', content="Nạp tiền thành công!")
                        redirect(URL(f="profile"))
                else:
                    add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)
    return dict(err="")


def naptien_thiquocgia():
    success = False
    message = ""
    if not session.site_back:
        session.site_back = "http://thiquocgia.vn"
    create_session_cart()
    categories = dict()
    fail_mess = "- Đề nghị liên lạc CSKH để được hỗ trợ. " + \
                "Số điện thoại: 047-302-0888"
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    purchase_type = ""
    email = ""
    package = ""
    pack_type = ""
    if "purchase_type" in request.vars:
        purchase_type = request.vars.purchase_type
        package = request.vars.package
        if purchase_type == "gift":
            email = request.vars.email
            pack_type = request.vars.type
    #print(purchase_type + "/" + email + "/" + package + "/" + pack_type)
    if 'secret' in request.vars:
        username = request.vars['username']
        secret = request.vars['secret']
        password = request.vars['password']
        firstName = request.vars['firstName']
        lastName = request.vars['lastName']
        email = request.vars['email']
        phoneNumber = request.vars['phoneNumber']
        address = request.vars['address']
        type_user = request.vars['type_user']
        session.site_back = request.vars['site_back']
        auto_login = service_auto_login(username, secret, password, firstName, lastName, email, phoneNumber,
                                        address, type_user, session.site_back)
        if 'error' in auto_login:
            add_alert(title='Lỗi', content=auto_login['error'])
        else:
            token = auto_login['token']
            login_result = service_user_auth_by_token(username, token)
            if login_result is None or 'error' in login_result:
                session.login_fail = True
            else:
                session.authorized = True
                session.expired = False
                session.token = login_result['token']
                session.username = request.vars['username']
                profile_result = service_user_info(session.username)
                if profile_result['items']['type_user'] == "google" or profile_result['items']['type_user'] == "facebook":
                    session.display_name = profile_result['items']['firstName'] + " " + profile_result['items']['lastName']
                else:
                    session.display_name = profile_result['items']['email']
                session.userfund = price2str(str(profile_result['items']['fund']))

    if not session.authorized:
        redirect(URL(f="signin", vars={'location': 'naptien_thiquocgia'}))

    response.title = u"Thi quốc gia - Nạp tiền"

    if len(request.args) > 0 and request.args[0] == "canceled":
        pass
    elif len(request.vars) > 0:
        # print(request.vars)
        # add_alert(title='Thông báo', content=str(request.vars))
        if "nlpayment" in request.vars:
            min_nl = 2000
            if request.vars.option_payment == "VISA":
                min_nl = 50000
            elif request.vars.option_payment == "ATM_ONLINE":
                min_nl = 10000
            if int(request.vars['discount-value'].replace(".", "")) >= min_nl:
                bank_code = ""
                if "bankcode" in request.vars:
                    bank_code = request.vars.bankcode
                if request.vars.option_payment == "VISA":
                    bank_code = request.vars.bank_code
                discount_code = request.vars['discount-code'].strip()
                rs = service_tqg_checkout(session.username, session.token, request.vars.option_payment,
                                          bank_code, request.vars['discount-value'].replace(".", ""), "test",
                                          URL(f="naptien_thiquocgia", host=True, scheme=True),
                                          URL(f="naptien_thiquocgia", args="canceled", host=True, scheme=True),
                                          purchase_type, package, email, pack_type, "TQG", discount_code)
                if rs is not None:
                    if rs["status"] == 200:
                        redirect(rs["data"])
                    else:
                        add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)
            else:
                add_alert(title='Lỗi', content="Số tiền bạn muốn thanh toán nhỏ hơn số tiền tối thiểu là " + str(min_nl) + " VND nên giao dịch không thể thực hiện. " + fail_mess)
        elif 'tqgpayment' in request.vars:
            tqg_card = request.vars.tqg_card
            discount_code = request.vars['discount-code'].strip()
            if purchase_type == "":
                rs = service_gcv_thiquocgia(tqg_card, discount_code=discount_code)
            if 'error' in rs:
                add_alert(title='Thông báo', content=rs['mess'])
            else:
                if rs['tranfer']:
                    success = True
                    message = "Chúc mừng bạn đã sử dụng thẻ thành công, tài khoản của bạn được cộng thêm " + \
                              str(rs['fund']) + "đ"
                else:
                    add_alert(title='Thông báo', content="Có lỗi xảy ra! Tiền được cộng vào tài khoản Classbook")
        elif 'tqgtranfer' in request.vars:
            tranfer_fund = request.vars.tranfer_fund.replace(".", "")
            discount_code = request.vars['discount-code'].strip()
            discount_value = request.vars['discount-value'].replace(".", "")
            rs = service_tranfer_thiquocgia(tranfer_fund, discount_value, discount_code)
            if 'error' in rs:
                add_alert(title='Thông báo', content=rs['error'])
            else:
                success = True
                message = "Chúc mừng bạn đã chuyển thành công " + str(rs['fund']) + "đ từ tài khoản Classbook thành " + \
                    str(rs['base_fund']) + "đ tài khoản Thi Quốc Gia"
                profile_result = service_user_info(session.username)
                session.userfund = price2str(str(profile_result['items']['fund']))
        elif "NLNapThe" in request.vars:
            pin_card = request.vars.txtSoPin
            card_serial = request.vars.txtSoSeri
            type_card = request.vars.select_method
            discount_code = request.vars['discount-code'].strip()
            rs = service_tqg_cardpay(session.username, session.token, pin_card, card_serial, type_card,
                                     purchase_type, package, email, pack_type, 'TQG', discount_code)
            #print(rs)
            session.report = ""
            if rs is not None:
                if rs["status"] == 200:
                    if "purchase_type" in request.vars:
                        check = service_check_elearning(username)
                        if check['check']:
                            if check['message'] == 'success':
                                success = True
                            else:
                                add_alert(title='Thông báo', content=check['message'])
                    else:
                        rs_tranfer = service_tranfer_to_tqg(session.username)
                        success = True
                        message = "Chúc mừng bạn đã nạp thành công " + \
                              str(rs_tranfer['fund']) + "đ vào tài khoản."
                else:
                    add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)
        elif "token" in request.vars:
            rs = service_transaction_confirm(session.username, session.token, request.vars.token)
            if rs is not None:
                if rs["status"] == 200:
                    if "purchase_type" in request.vars:
                        check = service_check_elearning(username)
                        if check['check']:
                            if check['message'] == 'success':
                                success = True
                            else:
                                add_alert(title='Thông báo', content=check['message'])
                    else:
                        rs_tranfer = service_tranfer_to_tqg(session.username)
                        success = True
                        message = "Chúc mừng bạn đã nạp thành công " + \
                              str(rs_tranfer['fund']) + "đ vào tài khoản."
                else:
                    add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)

    tqg_fund = get_fund_tqg()
    get_pay_history = service_sum_pay_tqg(session.username)
    total_pay = 0
    if 'total' in get_pay_history:
        total_pay = int(get_pay_history['total'])
    return dict(err="", tqg_fund=tqg_fund, success=success, message=message, total_pay=total_pay)



def naptien():
    success = False
    message = ""
    if not session.site_back:
        session.site_back = "http://classbook.vn"
    create_session_cart()
    categories = dict()
    fail_mess = "- Đề nghị liên lạc CSKH để được hỗ trợ. " + \
                "Số điện thoại: 047-302-0888"
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    purchase_type = ""
    email = ""
    package = ""
    pack_type = ""
    party_code = ""
    service_tranfer = ""
    if "purchase_type" in request.vars:
        purchase_type = request.vars.purchase_type
        package = request.vars.package
        if purchase_type == "gift":
            email = request.vars.email
            pack_type = request.vars.type
    #print(purchase_type + "/" + email + "/" + package + "/" + pack_type)
    if 'secret' in request.vars:
        username = request.vars['username']
        secret = request.vars['secret']
        password = request.vars['password']
        firstName = request.vars['firstName']
        lastName = request.vars['lastName']
        email = request.vars['email']
        phoneNumber = request.vars['phoneNumber']
        address = request.vars['address']
        type_user = request.vars['type_user']
        session.site_back = request.vars['site_back']
        party_code = request.vars['party_code']
        service_tranfer = request.vars['service_tranfer']
        auto_login = service_auto_login_third(username, secret, password, firstName, lastName, email, phoneNumber,
                                        address, type_user, session.site_back)
        if 'error' in auto_login:
            add_alert(title='Lỗi', content=auto_login['error'])
        else:
            token = auto_login['token']
            login_result = service_user_auth_by_token(username, token)
            if login_result is None or 'error' in login_result:
                session.login_fail = True
            else:
                session.authorized = True
                session.expired = False
                session.token = login_result['token']
                session.username = request.vars['username']
                profile_result = service_user_info(session.username)
                if profile_result['items']['type_user'] == "google" or profile_result['items']['type_user'] == "facebook":
                    session.display_name = profile_result['items']['firstName'] + " " + profile_result['items']['lastName']
                else:
                    session.display_name = profile_result['items']['email']
                session.userfund = price2str(str(profile_result['items']['fund']))

    if not session.authorized:
        redirect(URL(f="signin", vars={'location': 'naptien'}))

    response.title = u"Nạp tiền"

    if len(request.args) > 0 and request.args[0] == "canceled":
        pass
    elif len(request.vars) > 0:
        # print(request.vars)
        # add_alert(title='Thông báo', content=str(request.vars))
        if "nlpayment" in request.vars:
            min_nl = 2000
            if request.vars.option_payment == "VISA":
                min_nl = 50000
            elif request.vars.option_payment == "ATM_ONLINE":
                min_nl = 10000
            if int(request.vars['buyer_amount'].replace(".", "")) >= min_nl:
                bank_code = ""
                if "bankcode" in request.vars:
                    bank_code = request.vars.bankcode
                if request.vars.option_payment == "VISA":
                    bank_code = request.vars.bank_code
                # discount_code = request.vars['discount-code'].strip()
                rs = service_tqg_checkout(session.username, session.token, request.vars.option_payment,
                                          bank_code, request.vars['buyer_amount'].replace(".", ""), "test",
                                          URL(f="naptien", host=True, scheme=True),
                                          URL(f="naptien", args="canceled", host=True, scheme=True),
                                          purchase_type, package, email, pack_type, party_code, "")
                if rs is not None:
                    if rs["status"] == 200:
                        redirect(rs["data"])
                    else:
                        add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)
            else:
                add_alert(title='Lỗi', content="Số tiền bạn muốn thanh toán nhỏ hơn số tiền tối thiểu là " + str(min_nl) + " VND nên giao dịch không thể thực hiện. " + fail_mess)
        elif "NLNapThe" in request.vars:
            pin_card = request.vars.txtSoPin
            card_serial = request.vars.txtSoSeri
            type_card = request.vars.select_method
            # discount_code = request.vars['discount-code'].strip()
            rs = service_tqg_cardpay(session.username, session.token, pin_card, card_serial, type_card,
                                     purchase_type, package, email, pack_type, party_code, "")
            #print(rs)
            session.report = ""
            if rs is not None:
                if rs["status"] == 200:
                    if "purchase_type" in request.vars:
                        check = service_check_elearning(username)
                        if check['check']:
                            if check['message'] == 'success':
                                success = True
                            else:
                                add_alert(title='Thông báo', content=check['message'])
                    else:
                        rs_tranfer = service_tranfer_to_third(session.username, service_tranfer)
                        if 'result' in rs_tranfer and rs_tranfer['result']:
                            success = True
                            message = "Chúc mừng bạn đã nạp thành công " + \
                                  str(rs_tranfer['fund']) + "đ vào tài khoản."
                        else:
                            add_alert(title='Lỗi',
                                      content="Xảy ra lỗi kết nối, tiền bạn nạp chưa được chuyển về tài khoản vstep" + fail_mess)
                else:
                    add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)
        elif "token" in request.vars:
            rs = service_transaction_confirm(session.username, session.token, request.vars.token)
            if rs is not None:
                if rs["status"] == 200:
                    if "purchase_type" in request.vars:
                        check = service_check_elearning(username)
                        if check['check']:
                            if check['message'] == 'success':
                                success = True
                            else:
                                add_alert(title='Thông báo', content=check['message'])
                    else:
                        rs_tranfer = service_tranfer_to_third(session.username, service_tranfer)
                        if 'result' in rs_tranfer and rs_tranfer['result']:
                            success = True
                            message = "Chúc mừng bạn đã nạp thành công " + \
                                  str(rs_tranfer['fund']) + "đ vào tài khoản."
                        else:
                            add_alert(title='Lỗi',
                                      content="Xảy ra lỗi kết nối, tiền bạn nạp chưa được chuyển về tài khoản vstep" + fail_mess)
                else:
                    add_alert(title='Lỗi', content=str(rs["data"]) + fail_mess)

    return dict(err="", success=success, message=message)


def get_fund_tqg():
    url = 'http://thiquocgia.vn/userpanel/service_ajax.php'
    data = dict(type='get_fund', u=session.username)
    r = requests.post(url, data=data, allow_redirects=True)
    result = json.loads(r.content)
    tqg_fund = "0"
    if result['type'] == 'success':
        tqg_fund = result['value']
    tqg_fund = price2str(str(tqg_fund))
    return tqg_fund


def check_service_tqg():
    import requests
    my_url = 'http://capi.thiquocgia.vn/userpanel/service_ajax.php'
    data = dict(type='get_fund', u="tien3@test.vn")
    r = requests.post(my_url, data=data, allow_redirects=True)
    return dict(data=r.content)


def check_service_cb():
    import requests
    my_url = 'http://mp3.zing.vn/'
    data = dict(name='tiench', id="1")
    r = requests.post(my_url, data=data, allow_redirects=True)
    return dict(data=r.content)


def test_api():
    name = request.vars.name
    id = request.vars.id
    return dict(name=name, id=id)


def check_in_cart():  # product_id
    product_id = request.args[0]
    if not session.shopping_cart:
        session.shopping_cart = list()
    if product_id in session.shopping_cart:
        return dict(result=True)
    else:
        return dict(result=False)


def pcategory():
    create_session_cart()
    parent_id = 1
    if len(request.args) > 1:
        parent_id = request.args[1]
    # menu = service_category_get()
    # if menu is not None and not 'error' in menu:
    #     session.categories = menu['categories']

    if 't' in request.vars and 'u' in request.vars:
        token = request.vars['t']
        username = request.vars['u']
        login_result = service_user_auth_by_token(username, token)
        if login_result is None or 'error' in login_result:
            session.login_fail = True
        else:
            # print 'login success'
            session.authorized = True
            session.expired = False
            session.token = login_result['token']
            session.username = request.vars['username']
            profile_result = service_user_info(session.username)
            session.display_name = profile_result['items']['email']
            session.userfund = price2str(str(profile_result['items']['fund']))
    home_topic = list()
    # top_item = dict()
    # top_item['title'] = "Nội dung nổi bật"
    # top_item['code'] = "top"
    # top_item['id'] = 0
    # top_item['items'] = service_category_top_item([parent_id])['products']
    # for index in range(0, len(top_item['items'])):
    #    top_item['items'][index]['product_cover'] = URL(a='cbs', c='download', f='thumb',
    #             scheme=True, host=False, args=top_item['items'][index]['product_code'])
    # home_topic.append(top_item)
    cate_parent = dict()
    for parent in get_menu():
        if parent['category_id'] == int(parent_id):
            cate_parent = parent
        else:
            for child in parent['children']:
                if child['category_id'] == int(parent_id):
                    cate_parent = child
    response.title = cate_parent['category_name'] + u" - Sách giáo khoa điện tử Classbook"
    count_topic = 0
    for child in cate_parent['children']:
        if count_topic < 4:
            count_topic += 1
            child_item = dict()
            child_item['title'] = child['category_name']
            child_item['code'] = child['category_code']
            child_item['id'] = child['category_id']
            child_item['count_child'] = len(child['children'])
            marg = list()
            marg.append(child['category_id'])
            marg.append(0)
            marg.append(5)
            child_item['items'] = service_product_get(marg)['products']
            for index in range(0, len(child_item['items'])):
                # child_item['items'][index]['product_cover'] = URL(a='cbs', c='download', f='thumb',
                #      scheme=True, host=False, args=child_item['items'][index]['product_code'])
                child_item['items'][index]['product_cover'] = "/static/covers/" + \
                                                              child_item['items'][index]['product_code'] + "/thumb.png"
            home_topic.append(child_item)
    return dict(home_topic=home_topic, cate_parent=cate_parent)


def create_session_cart():
    if not session.shopping_cart:
        session.shopping_cart = list()


def samsung_gift_tutorial():
    response.title = u"Hướng dẫn lấy Mã quà tặng Samsung - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    return dict()


def by_creator():
    create_session_cart()
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    products = list()
    if not request.vars or len(request.vars) == 0:
        return dict(products=products, total_item=0, total_page=0)
    creator_name = request.vars.creator
    response.title = u"Tác giả - Sách giáo khoa điện tử Classbook"
    page = 0
    item_per_page = 18
    if "page" in request.vars:
        page = int(request.vars.page)
    vars = dict()
    vars['creator'] = creator_name
    vars['page'] = page
    vars['item_per_page'] = item_per_page
    products = service_product_by_creator(vars)
    for index in range(0, len(products['products'])):
        products['products'][index]['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                           scheme=True, host=False,
                                                           args=products['products'][index]['product_code'])
    products['categories'] = service_category_get()['categories']
    return products


def by_cp():
    create_session_cart()
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    products = list()
    if not request.vars or len(request.vars) == 0:
        return dict(products=products, total_item=0, total_page=0)
    product_id = request.vars.product_id
    cp_name = request.vars.cp_name
    response.title = u"Sách giáo khoa điện tử Classbook"
    page = 0
    item_per_page = 18
    if "page" in request.vars:
        page = int(request.vars.page)
    vars = dict()
    vars['product_id'] = product_id
    vars['page'] = page
    vars['item_per_page'] = item_per_page
    products = service_product_by_cp(vars)
    for index in range(0, len(products['products'])):
        products['products'][index]['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                           scheme=True, host=False,
                                                           args=products['products'][index]['product_code'])
    products['categories'] = service_category_get()['categories']
    return products


def by_publisher():
    create_session_cart()
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    products = list()
    if not request.vars or len(request.vars) == 0:
        return dict(products=products, total_item=0, total_page=0)
    product_id = request.vars.product_id
    response.title = u"Sách giáo khoa điện tử Classbook"
    page = 0
    item_per_page = 18
    if "page" in request.vars:
        page = int(request.vars.page)
    vars = dict()
    vars['product_id'] = product_id
    vars['page'] = page
    vars['item_per_page'] = item_per_page
    products = service_product_by_publisher(vars)
    for index in range(0, len(products['products'])):
        products['products'][index]['product_cover'] = URL(a='cbs', c='download', f='thumb',
                                                           scheme=True, host=False,
                                                           args=products['products'][index]['product_code'])
    products['categories'] = service_category_get()['categories']
    return products


def guid_buy():
    response.title = u"Hướng dẫn mua - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    # categories = dict()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    return dict()


def guid_check_out():
    response.title = u"Hướng dẫn nạp tiền - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    # if not session.categories:
    #     session.categories = dict()
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    return dict()


def set_product():
    try:
        response.title = u"Bộ sách - Sách giáo khoa điện tử Classbook"
        create_session_cart()
        # categories = dict()
        # if not session.categories:
        #     menu = service_category_get()
        #     if menu is not None and not 'error' in menu:
        #         session.categories = menu['categories']
        set_id = request.args[0]
        set_info = service_set_info(dict(set_id=set_id))
        set_info['categories'] = categories
        return set_info
    except Exception as err:
        return dict(err=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def set_to_cart():
    try:
        set_id = request.args[0]
        set_info = service_set_info(dict(set_id=set_id))
        for product in set_info['products']:
            if str(product['id']) not in session.shopping_cart:
                session.shopping_cart.append(str(product['id']))
        redirect(URL("cart"))
    except Exception as err:
        return dict(err=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def teacher():
    response.title = u"Giáo viên - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()
    return dict()


def author():
    response.title = u"Tác giả - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    #     else:
    #         session.categories = dict()
    return dict()


def preview():
    product_id = request.args[1]
    info = service_product_info(product_id)['product']
    return dict(info=info)


def view_pdf():
    try:
        exer_code = request.args[0]
        root_dic = "/home/www-data/web2py/applications/cbw/static/view_pdf/document/"
        page_count = 0
        if os.path.isdir(root_dic + exer_code):
            page_count = count_dir(root_dic + exer_code)
        return dict(exer_code=exer_code, page_count=page_count,
                    info=service_bai_tap_chuyen_de(exer_code))
    except Exception as err:
        print "ERROR: " + str(err) + " on line: " + str(sys.exc_traceback.tb_lineno)
        return dict(err=err)


def count_dir(path):
    count = 0
    for f in os.listdir(path):
        child = os.path.join(path, f)
        if os.path.isdir(child):
            count += 1
    return count


def third_party_fb():
    create_session_cart()
    if not session.categories:
        menu = service_category_get()
        if menu is not None and not 'error' in menu:
            session.categories = menu['categories']
        else:
            session.categories = dict()
    return dict()


def test_third_party():
    return dict()


def chuyen_de():
    all_cd = service_chuyen_de()
    select_cd = "Tổng hợp"
    if len(request.args) > 0:
        for cd in all_cd['chuyen_de']:
            if str(cd['id']) == str(request.args):
                select_cd = cd['title']
    all_cd['select'] = select_cd
    return all_cd


def chuyen_de_mobile():
    all_cd = service_chuyen_de()
    select_cd = "Tổng hợp"
    if len(request.args) > 0:
        for cd in all_cd['chuyen_de']:
            if str(cd['id']) == str(request.args):
                select_cd = cd['title']
    all_cd['select'] = select_cd
    return all_cd


def chuyen_de_mobile_test():
    all_cd = service_chuyen_de()
    select_cd = "Tổng hợp"
    if len(request.args) > 0:
        for cd in all_cd['chuyen_de']:
            if str(cd['id']) == str(request.args):
                select_cd = cd['title']
    all_cd['select'] = select_cd
    return all_cd


def thithu():
    try:
        from datetime import datetime, timedelta
        subject = str(request.args[0]).upper()
        exam_round = request.args[1]
        select_exam = service_get_exam(exam_round)
        if not select_exam['result']:
            return dict(exer_code=subject, page_count=0, mess="Not found exam")
        start = datetime.strptime(select_exam['start_date'], "%Y/%m/%d %H:%M:%S")
        end = datetime.strptime(select_exam['end_date'], "%Y/%m/%d %H:%M:%S") + timedelta(minutes=int(select_exam['exam_time']))
        if start > datetime.now():
            return dict(exer_code=subject, page_count=0, mess="Invalid time", start=str(start), end=str(end), now=str(datetime.now()))
        exer_code = ""
        if len(request.args) >= 3 and end <= datetime.now():
            exer_code = "DA_DETHITHU_" + subject + exam_round
        else:
            exer_code = "DETHITHU_" + subject + exam_round
        root_dic = "/home/www-data/web2py/applications/cbw/static/view_pdf/document/"
        page_count = 0
        if os.path.isdir(root_dic + exer_code):
            page_count = count_dir(root_dic + exer_code)
        exams = service_get_active_exam()['exams']
        return dict(exer_code=exer_code, page_count=page_count, end=end.strftime('%Y/%m/%d %H:%M:%S'),
                    exams=list(), da=(end <= datetime.now()))
    except Exception as err:
        print "ERROR: " + str(err) + " on line: " + str(sys.exc_traceback.tb_lineno)
        return dict(err=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))


def thithu_test():
    try:
        from datetime import datetime, timedelta
        subject = str(request.args[0]).upper()
        exam_round = request.args[1]
        select_exam = service_get_exam(exam_round)
        if not select_exam['result']:
            return dict(exer_code=subject, page_count=0)
        start = datetime.strptime(select_exam['start_date'], "%Y/%m/%d %H:%M:%S")
        end = datetime.strptime(select_exam['end_date'], "%Y/%m/%d %H:%M:%S") + timedelta(minutes=int(select_exam['exam_time']))
        if start > datetime.now():
            return dict(exer_code=subject, page_count=0)
        exer_code = ""
        if len(request.args) >= 3 and end <= datetime.now():
            exer_code = "DA_DETHITHU_" + subject + exam_round
        else:
            exer_code = "DETHITHU_" + subject + exam_round
        root_dic = "/home/www-data/web2py/applications/cbw/static/view_pdf/document/"
        page_count = 0
        if os.path.isdir(root_dic + exer_code):
            page_count = count_dir(root_dic + exer_code)
        exams = service_get_active_exam()['exams']
        return dict(exer_code=exer_code, page_count=page_count, end=end.strftime('%Y/%m/%d %H:%M:%S'), exams=exams)
    except Exception as err:
        print "ERROR: " + str(err) + " on line: " + str(sys.exc_traceback.tb_lineno)
        return dict(err=str(err) + " on line: " + str(sys.exc_traceback.tb_lineno))

def changepass():
    response.title = u"Đổi mật khẩu - Sách giáo khoa điện tử Classbook"
    if not session.authorized:
        redirect(URL(f="signin", vars={'location': "changepass"}))
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    result = "default"
    if request.vars and len(request.vars) > 0:
        oldpass = request.vars.oldpassword
        newpass = request.vars.newpassword
        change = service_changepass(oldpass, newpass)
        if "error" in change:
            result = "Lỗi: " + change['error']
        else:
            result = ""
            session.token = change['token']
    return dict(result=result)


def install(): #param: product_code
    import os
    try:
        if len(request.args) == 0:
            return 'Không thấy file'
        file_type = request.args[0]
        if file_type == 'android':
            path = "/home/file/ClassbookWS.apk"
            filename = "Classbook.apk"
        else:
            return 'Không thấy file'
        response.headers['Content-Length'] = os.path.getsize(path)
        response.headers['Content-Type'] = 'application/zip'
        response.headers['Content-Disposition'] = "attachment; filename=" + \
                                                  filename
        response.headers['X-Sendfile'] = path

    except Exception as ex:
        return ex.message


def paycode():
    response.title = u"Mã thanh toán - Sách giáo khoa điện tử Classbook"
    if not session.authorized:
        redirect(URL(f="signin", vars={'location': "paycode"}))
    # if not session.categories:
    #     menu = service_category_get()
    #     if menu is not None and not 'error' in menu:
    #         session.categories = menu['categories']
    result = "default"
    check = True
    if request.vars and len(request.vars) > 0:
        code = request.vars.code
        checkpay = service_payment_code(code)
        result = checkpay['mess']
        if 'error' in checkpay:
            check = False
    return dict(result=result, check=check)


def giftcard_guid():
    response.title = u"Gift card - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    return dict()


def buy_history():
    response.title = u"Lịch sử mua - Sách giáo khoa điện tử Classbook"
    create_session_cart()
    if not session.authorized:
        redirect(URL(f="signin", vars={'location': "buy_history"}))

    profile_result = service_user_info(session.username)
    if profile_result is None or 'error' in profile_result:
        if profile_result is not None and profile_result['error']:
            session.authorized = False
        redirect(URL(f="signin", vars={'location': "download_history"}))
        return dict()
    else:
        buy_his = service_buy_history()

        buy_his['user_fund'] = price2str(str(profile_result['items']['fund']))
        buy_his['user'] = profile_result['items']
        session.userfund = price2str(str(profile_result['items']['fund']))
        return buy_his


def res():
    site = request.args[0]
    if site == "hoclien":
        link = request.args[1]
        if link == "ios":
            redirect("https://i.diawi.com/ygE1B8")
        else:
            redirect("http://classbook.vn/cbw/static/hoclien/HoclienAR-20161209_04.apk")


def apps():
    return dict()
