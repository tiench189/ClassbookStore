# -*- coding: utf-8 -*-
__author__ = 'Tien'

import sys
import json
import myredis


def get():
    try:
        site = "classbook"
        if 'site' in request.vars:
            site = request.vars.site
        check_cache = myredis.get_cache(BANNER + site)
        if check_cache['result'] and check_cache['data'] is not None:
            data = json.loads(check_cache['data'])
            data['cache'] = True
            return data
        select_banner = db(db.clsb30_banner.active_status == 1)\
                (db.clsb30_banner.banner_site.like(site)).select(orderby=db.clsb30_banner.banner_order)
        banners = list()
        for b in select_banner:
            temp = dict()
            temp['id'] = b['id']
            temp['title'] = b['banner_title']
            temp['url'] = b['banner_url']
            temp['type'] = b['action_type']
            temp['data'] = b['action_data']
            banners.append(temp)
        data = dict(banners=banners)
        myredis.write_cache(BANNER + site, str(json.dumps(data)), DEFAULT_TIME)
        data['cache'] = False
        return data
    except Exception as ex:
        return dict(error=str(ex) + " on line: "+str(sys.exc_traceback.tb_lineno))