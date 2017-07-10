__author__ = 'manhtd'


def get_yahoo_icon():
    try:
        http = urllib3.PoolManager()
        fetch_data = http.request('GET', 'http://opi.yahoo.com/online?u=%s&m=t&t=1' % request.args[0])
        if fetch_data.status == 200:
            from fs.osfs import OSFS

            file_server = OSFS('/home/www-data/web2py/applications/cbw/static/images')

            if len(request.args) != 1:
                raise HTTP(400)
            if fetch_data.data == "01":
                path = "icon-YMonline.png"
            else:
                path = "icon-YMoffline.png"
            if file_server.exists(path):
                response.headers['Content-Length'] = file_server.getinfo(path)['size']
                response.headers['Content-Type'] = 'image/png'
                response.headers['Content-Disposition'] = "attachment; filename=yahoo.png"
                return response.stream(file_server.open(path=path, mode='rb'))
            else:
                raise HTTP(404)
        else:
            raise Exception(fetch_data.status)
    except:
        return None


def get_skype_icon():
    return response.download()
