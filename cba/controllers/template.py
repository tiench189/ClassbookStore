__author__ = 'Tien'

import json
import sys
import os
import datetime
import shutil, errno

HOME_DIC = "/home/developers/manhtd/web2py/applications/cba/static/"
DATA_DIC = "/home/developers/manhtd/CBSData/template/"

def index():
    try:
        if request.args and len(request.args) > 0:
            interactive_code = request.args[0]
            interactive = db(db.clsb30_interactive.interactive_code == interactive_code).select()
            if len(interactive) > 0:
                interactive = interactive.first()
                str_data = str(interactive['interactive_data']).replace("\'[", "[").replace("]\'", "]").replace("\'", "\"")
                data = json.loads(str_data)
                recursive_overwrite("/home/developers/manhtd/CBSData/template/" + interactive_code + "/",  HOME_DIC + "temp/" + interactive_code + "/")
                return dict(path=interactive_code, data=data, edit=True)
        if len(request.vars) > 0:
            #print(request.vars)
            str_json = request.vars['final_json']
            background = request.vars['background']
            time_out = (int(request.vars['timeOut'])) * 50
            after_drop = int(request.vars['afterDrop'])
            check_true = int(request.vars['checkTrue'])
            orientation = request.vars['orientation']
            code = request.vars['path']
            name = request.vars['name']
            path = HOME_DIC + "temp/" + code + "/"
            edit = int(request.vars['edit'])
            #print(str_json)
            data = json.loads(str_json)

            html = ""
            html += "<!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'> \n"
            html += "<html xmlns='http://www.w3.org/1999/xhtml'>\n"
            html += "<head>\n"
            html += "<meta http-equiv='Content-Type' content='text/html; charset=utf-8' />\n" +\
                "<script src='js/jquery-1.7.2.min.js'></script>\n" +\
                "<link rel='stylesheet' type='text/css' href='css/style.css'>\n" +\
                "<link rel='stylesheet' type='text/css' href='css/animate.min.css' />\n" +\
                "<meta name='viewport' content='width=device-width, initial-scale=1, maximum-scale=1'>\n" +\
                "<title>Untitled Document</title>\n" +\
                "</head>\n"
            html += "<body>\n"
            html += "<div id='play'>\n" +\
                        "<div id='playStart'><img src='images/play-icon.png'></div>\n" +\
                    "</div>\n"
            html += "<div id='container'>\n"
            html += "<div id='time' style='float:right; font-size:25px; font-weight:normal; '>" +\
                    "<div id='progress-bar'></div>" +\
                "</div>"
            for element in data:
                html += "<div class='element " + element['key'] + " " + element['type'] + "' true='0'></div>\n"
            html += "</div>\n"
            html += "<div id='popup-backdrop'></div>\n" +\
                "<div id='popup_box'>\n" +\
                    "<div id='cry' class='shake animated'><img src='images/mat-khoc.png'></div>\n" +\
                    "<div style='display: inline-block;'><img src='images/reload-page.png' width='80px' height='80px' onclick='reloadPage()' style='margin-bottom: -10px;' /></div>\n" +\
                "</div>\n" +\
                "<div id='popup_victory'>\n" +\
                    "<div id='smile' class='flash animated'><img src='images/mat-cuoi.png'></div>\n" +\
                    "<div style='display: inline-block;'><img src='images/reload-page.png' width='80px' height='80px' onclick='reloadPage()' style='margin-bottom: -10px;' /></div>\n" +\
                "</div>\n"
            html += "</body>\n"

            html += "<script type='text/javascript'>\n"
            #khai bao bien trong js
            html += "var drag_list;\n"
            html += "var drop_list;\n"
            html += "var element_list;\n"
            html += "var current_drag = null;\n"
            html += "var container;\n"
            html += "var trueAns = 0;\n"
            html += "var interval;\n"
            html += "var oldX, oldY;\n"
            html += "var onTime = true;\n"
            html += "var popup_backdrop;\n"
            html += "var popup_box;\n"
            html += "var popup_victory;\n"
            html += "var timeLimit = " + str(time_out) + ";\n"
            html += "var fullTime = " + str(time_out) + ";\n"
            html += "var timeInterval;\n"
            html += "var reload;\n"
            #ready function
            html += "$(document).ready(function(e) {\n"
            html += "drag_list = document.getElementsByClassName('drag');\n" +\
                "drop_list = document.getElementsByClassName('drop');\n" +\
                "element_list = document.getElementsByClassName('element');\n" +\
                "container = document.getElementById('container');\n"
            html += "popup_backdrop = document.getElementById('popup-backdrop');\n" +\
                "popup_box = document.getElementById('popup_box');\n" +\
                "popup_victory = document.getElementById('popup_victory');\n"
            #cal function set view
            html += "setView();\n"
            # check first
            html += "if (window.AndroidFunction && !AndroidFunction.isFirst()){\n" +\
                    "$('#play').addClass('zoomIn animated done');\n" +\
                    "$('#play').css('display', 'none');\n" +\
                    "timeInterval = setInterval(updateTime, 600);\n" +\
                "}\n"
            html += "document.getElementById('playStart').addEventListener('touchstart', function (event){\n" +\
                    "setTimeout(function () {\n" +\
                        "$('#play').addClass('zoomIn animated done');\n" +\
                        "$('#play').css('display', 'none');\n" +\
                        "timeInterval = setInterval(updateTime, 600);\n" +\
                    "}, 500);\n" +\
                "});\n"

            html += "document.getElementById('playStart').addEventListener('mousedown', function (event){\n" +\
                    "setTimeout(function () {\n" +\
                        "$('#play').addClass('zoomIn animated done');\n" +\
                        "$('#play').css('display', 'none');\n" +\
                        "timeInterval = setInterval(updateTime, 600);\n" +\
                    "}, 500);\n" +\
                "});\n"

            #set dragable
            html += "for(var i = 0; i < drag_list.length; i++){\n" +\
                        "var drag = drag_list[i];\n" +\
                        "setDragable(drag);\n" +\
                    "}\n"
            # add event touch move
            html += "container.addEventListener('touchmove', function (event){\n" +\
                    "if (current_drag != null){\n" +\
                        "if (onTime){\n" +\
                            "var element = current_drag;\n" +\
                            "var touch = event.targetTouches[0];\n" +\
                            "element.style.setProperty('top', touch.pageY - element.parentNode.offsetTop - element.offsetHeight/2 + 'px')\n" +\
                            "element.style.setProperty('left', touch.pageX - element.parentNode.offsetLeft  - element.offsetWidth/2 + 'px')\n" +\
                        "}\n" +\
                    "}\n" +\
                    "event.preventDefault();\n" +\
                "}, false);\n"
            html += "container.addEventListener('mousemove', function (event){\n" +\
                    "if (current_drag != null){\n" +\
                        "if (onTime){\n" +\
                            "var element = current_drag;\n" +\
                            "element.style.setProperty('top', event.clientY - element.parentNode.offsetTop - element.offsetHeight/2 + 'px')\n" +\
                            "element.style.setProperty('left', event.clientX - element.parentNode.offsetLeft  - element.offsetWidth/2 + 'px')\n" +\
                        "}\n" +\
                    "}\n" +\
                    "event.preventDefault();\n" +\
                "}, false);\n"
            # add event touch end
            html += "container.addEventListener('touchend', function (event){\n" +\
                "if (current_drag != null){\n" +\
                    "var key_drag = current_drag.className.split(/\s+/)[1]\n" +\
                    "var drop_true = false;\n" +\
                    "for (var i = 0; i < drop_list.length; i++){\n" +\
                        "var drop = drop_list[i];\n"
            if check_true == 0:
                html += "if (drop.className.indexOf(key_drag) != -1 && checkDropped(current_drag, drop)){\n"
                if after_drop == 0:
                    html += "current_drag.style.display = 'none';\n"
                else:
                    html += "console.log('Drop: ' +  drop.offsetLeft + '/' + drop.offsetTop);\n"
                    html += "current_drag.style.setProperty('left', drop.offsetLeft + 'px');\n"
                    html += "current_drag.style.setProperty('top', drop.offsetTop + 'px');\n"
                html += "trueAns ++;\n" +\
                                        "if (trueAns < drag_list.length){\n" +\
                                            "//playAudio(audio_true);\n" +\
                                        "}else{\n" +\
                                            "//playAudio(audio_final);\n" +\
                                            "popup_victory.style.display = 'initial';\n" +\
                                            "popup_backdrop.style.display = 'block';\n"+\
                                            "popup_backdrop.style.opacity = 0.75;\n" +\
                                            "clearInterval(timeInterval);\n" +\
                                        "}\n" +\
                                    "}else{\n" +\
                                        "//playAudio(audio_false);\n" +\
                                    "}\n"
            else:
                html += "if (checkDropped(current_drag, drop)){\n" +\
                    "if (drop.className.indexOf(key_drag) != -1){\n"
                html += "current_drag.setAttribute('true', 1);\n"
                html += "drop_true = true;\n"
                html += "}\n"
                html += "console.log('Drop: ' +  drop.offsetLeft + '/' + drop.offsetTop);\n"
                html += "current_drag.style.setProperty('left', drop.offsetLeft + 'px');\n"
                html += "current_drag.style.setProperty('top', drop.offsetTop + 'px');\n"
                html += "if (checkFinal()){\n"
                html += "//playAudio(audio_final);\n" +\
                                            "popup_victory.style.display = 'initial';\n" +\
                                            "popup_backdrop.style.display = 'block';\n"+\
                                            "popup_backdrop.style.opacity = 0.75;\n" +\
                                            "clearInterval(timeInterval);\n"

                html += "}\n"
                html += "}\n"
            html += "}\n"
            if check_true == 0:
                html += "resetElement(current_drag);\n"
            html += "}\n" +\
                    "current_drag = null;\n" +\
                "});\n"
            # mouse up
            html += "container.addEventListener('mouseup', function (event){\n" +\
                "if (current_drag != null){\n" +\
                    "var key_drag = current_drag.className.split(/\s+/)[1]\n" +\
                    "var drop_true = false;\n" +\
                    "for (var i = 0; i < drop_list.length; i++){\n" +\
                        "var drop = drop_list[i];\n"
            if check_true == 0:
                html += "if (drop.className.indexOf(key_drag) != -1 && checkDropped(current_drag, drop)){\n"
                if after_drop == 0:
                    html += "current_drag.style.display = 'none';\n"
                else:
                    html += "console.log('Drop: ' +  drop.offsetLeft + '/' + drop.offsetTop);\n"
                    html += "current_drag.style.setProperty('left', drop.offsetLeft + 'px');\n"
                    html += "current_drag.style.setProperty('top', drop.offsetTop + 'px');\n"
                html += "trueAns ++;\n" +\
                                        "if (trueAns < drag_list.length){\n" +\
                                            "//playAudio(audio_true);\n" +\
                                        "}else{\n" +\
                                            "//playAudio(audio_final);\n" +\
                                            "popup_victory.style.display = 'initial';\n" +\
                                            "popup_backdrop.style.display = 'block';\n"+\
                                            "popup_backdrop.style.opacity = 0.75;\n" +\
                                            "clearInterval(timeInterval);\n" +\
                                        "}\n" +\
                                    "}else{\n" +\
                                        "//playAudio(audio_false);\n" +\
                                    "}\n"
            else:
                html += "if (checkDropped(current_drag, drop)){\n" +\
                    "if (drop.className.indexOf(key_drag) != -1){\n"
                html += "current_drag.setAttribute('true', 1);\n"
                html += "drop_true = true;\n"
                html += "}\n"
                html += "console.log('Drop: ' +  drop.offsetLeft + '/' + drop.offsetTop);\n"
                html += "current_drag.style.setProperty('left', drop.offsetLeft + 'px');\n"
                html += "current_drag.style.setProperty('top', drop.offsetTop + 'px');\n"
                html += "if (checkFinal()){\n"
                html += "//playAudio(audio_final);\n" +\
                                            "popup_victory.style.display = 'initial';\n" +\
                                            "popup_backdrop.style.display = 'block';\n"+\
                                            "popup_backdrop.style.opacity = 0.75;\n" +\
                                            "clearInterval(timeInterval);\n"

                html += "}\n"
                html += "}\n"
            html += "}\n"
            if check_true == 0:
                html += "resetElement(current_drag);\n"
            html += "}\n" +\
                    "current_drag = null;\n" +\
                "});\n"
            html += "});\n"
            #function setview
            html += "function setView(){\n"
            html += "container.style.setProperty('width', parseInt(window.innerWidth) + 'px');\n"
            html += "container.style.setProperty('height', parseInt(window.innerHeight) + 'px');\n"
            html += "container.style.setProperty('background-image', 'url(img/" + str(background) +")');\n"
            for i in range(0, len(data)):
                element = data[i]
                str_element = "element_list[" + str(i) + "]"
                if element["width_o"] == "0":
                    html += str_element + ".style.setProperty('width', parseInt(" + element['width_p'] + " * window.innerWidth / 100) + 'px');\n"
                else:
                    html += str_element + ".style.setProperty('width', parseInt(" + element['width_p'] + " * window.innerHeight / 100) + 'px');\n"

                if element["height_o"] == "0":
                    html += str_element + ".style.setProperty('height', parseInt(" + element['height_p'] + " * window.innerWidth / 100) + 'px');\n"
                else:
                    html += str_element + ".style.setProperty('height', parseInt(" + element['height_p'] + " * window.innerHeight / 100) + 'px');\n"

                if element["left_o"] == "0":
                    html += str_element + ".style.setProperty('left', parseInt(" + element['left_p'] + " * window.innerWidth / 100) + 'px');\n"
                else:
                    html += str_element + ".style.setProperty('left', parseInt(" + element['left_p'] + " * window.innerHeight / 100) + 'px');\n"

                if element["top_o"] == "0":
                    html += str_element + ".style.setProperty('top', parseInt(" + element['top_p'] + " * window.innerWidth / 100) + 'px');\n"
                else:
                    html += str_element + ".style.setProperty('top', parseInt(" + element['top_p'] + " * window.innerHeight / 100) + 'px');\n"

                html += str_element + ".style.setProperty('background-image', 'url(img/" + element['img_url'] +")');\n"
            html += "}\n"
            # function check drop
            html += "function checkDropped(drag, drop){\n" +\
                    "centerX = drag.offsetLeft + drag.offsetWidth/2;\n" +\
                    "centerY = drag.offsetTop + drag.offsetHeight/2;\n" +\
                    "if (centerX > drop.offsetLeft && centerX < (drop.offsetLeft + drop.offsetWidth) && centerY > drop.offsetTop && centerY < (drop.offsetTop + drop.offsetHeight)){\n" +\
                        "return true;\n" +\
                    "}else{\n" +\
                        "return false;\n" +\
                    "}\n" +\
                "}\n"
            # function reset element
            html += "function resetElement(current_drag){\n" +\
                    "current_drag.style.setProperty('top', oldY + 'px')\n" +\
                    "current_drag.style.setProperty('left', oldX + 'px')\n" +\
                    "current_drag.style.setProperty('z-index', '0');\n" +\
                    "current_drag.style.setProperty('transform', 'scale(1, 1)')\n" +\
                "}\n"
            # function set drag
            html += "function setDragable(element){\n"
            html += "element.addEventListener('touchstart', function (event){\n" +\
                        "if (onTime){\n" +\
                            "oldX = element.offsetLeft;\n" +\
                            "oldY = element.offsetTop;\n" +\
                            "current_drag = element;\n" +\
                            "element.style.setProperty('z-index', '100');\n" +\
                            "current_drag.setAttribute('true', 0);\n" +\
                            "//playAudio(audio_touch);\n" +\
                        "}\n" +\
                    "});\n"
            html += "element.addEventListener('mousedown', function (event){\n" +\
                        "if (onTime){\n" +\
                            "oldX = element.offsetLeft;\n" +\
                            "oldY = element.offsetTop;\n" +\
                            "current_drag = element;\n" +\
                            "element.style.setProperty('z-index', '100');\n" +\
                            "current_drag.setAttribute('true', 0);\n" +\
                            "//playAudio(audio_touch);\n" +\
                        "}\n" +\
                    "});\n"
            html += "}\n"
            # function check final
            html += "function checkFinal(){\n" +\
                    "result = true;\n" +\
                    "console.log('drag list: ' + drag_list.length)\n" +\
                    "for (var i = 0; i < drag_list.length; i ++){\n" +\
                        "if (drag_list[i].getAttribute('true') == '0'){\n" +\
                            "result = false;\n" +\
                        "}\n" +\
                    "}\n" +\
                    "console.log('final: ' + result)\n" +\
                    "return result;\n" +\
                "}\n"
            # reload
            html += "function reloadPage(){window.location.reload();}"
            html += "function updateTime(){" +\
                    "if (timeLimit > 0){" +\
                        "timeLimit --;" +\
                        "if (timeLimit == 0){" +\
                            "onTime = false;" +\
                            "popup_box.style.display = 'initial';" +\
                            "popup_backdrop.style.display = 'block';" +\
                            "popup_backdrop.style.opacity = 0.75;" +\
                            "$('.numberFlash').removeClass('false');" +\
                        "}else{" +\
                            "var progress_bar = document.getElementById('progress-bar');" +\
                            "progress_bar.style.setProperty('margin-top', (fullTime - timeLimit) / (fullTime / 50) + 'px');" +\
                            "progress_bar.style.setProperty('background-position-y', (timeLimit - fullTime) / (fullTime / 50) + 'px');" +\
                        "}" +\
                    "}else{" +\
                        "clearInterval(timeInterval);" +\
                    "}" +\
                "}"
            html += "</script>\n"
            html += "</html>"
            #print(html)

            html_file = open(path + "index.html", "w")
            html_file.write(html)
            html_file.close()

            cnf_file = open(path + "cnf.txt", "w")
            cnf_file.write(str(orientation))
            cnf_file.close()
            request.vars.pop("name")
            request.vars.pop("edit")
            #print(request.vars)
            if edit == 0:
                db.clsb30_interactive.insert(interactive_title=name, interactive_code=khongdau(name),
                                             interactive_data=str(request.vars)[9:-1])
                code = khongdau(name)
                recursive_overwrite(path, DATA_DIC + khongdau(name) + "/")
                recursive_overwrite(path, HOME_DIC + "temp/" + khongdau(name) + "/")
                make_zip(khongdau(name))
                shutil.rmtree(path)
            else:
                db(db.clsb30_interactive.interactive_code == code).update(interactive_data=str(request.vars)[9:-1])
                recursive_overwrite(path, DATA_DIC + code + "/")
                make_zip(code)

            return dict(result=True, path=code, edit=False)
        else:
            current_time = str(datetime.datetime.now()).replace("-", "").replace(":", "").replace(" ", "").replace(".", "")
            path = HOME_DIC + "temp/" + current_time + "/"
            copyanything(HOME_DIC + "template/", path)
            return dict(path=current_time, edit=False)
    except Exception as err:
        print(str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
    return dict(path="", edit=False)

def upload_image():
    try:
        osFileServer = OSFS("/home/developers/manhtd/web2py/applications/cba/static/template/img/")
        filename = request.vars.filename
        path = request.vars.path
        osFileServer = OSFS("/home/developers/manhtd/web2py/applications/cba/static/temp/" + path + "/img/")
        osFileServer.setcontents(filename, request.vars.image.file)
        return "<img width='100' height='100' src='" + URL('static','temp/' + path + '/img/' + filename) +"' class='show_drop_image'>"
    except Exception as err:
        print(str(err) + " on line " + str(sys.exc_traceback.tb_lineno))
    return dict()

def manager():
    try:
        fields = (db.clsb30_interactive.id,
            db.clsb30_interactive.interactive_title,
            db.clsb30_interactive.interactive_code)
        links = [{'header': 'Delete', 'body': lambda row: A('Delete', _href='javascript:delete_interactive(' + str(row.id) + ')')},
                 {'header': 'Edit', 'body': lambda row: A('Edit', _href=URL(f='index', args=[row.interactive_code]))},
                 {'header': 'Download', 'body': lambda row: A('Download', _href=URL(f='download', args=[row.interactive_code]))}]
        form = SQLFORM.smartgrid(db.clsb30_interactive, fields=fields,
                                 showbuttontext=False,
                                 linked_tables=[''],
                                 links=links)
        return dict(form=form)
    except Exception as err:
        return dict(error=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def copyanything(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc:
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise

def check_name_exist():
    try:
        name = request.vars.name
        check = db(db.clsb30_interactive.interactive_title == name).select()
        if len(check) == 0:
            return dict(exist=False)
        else:
            return dict(exist=True)
    except Exception as err:
        return dict(exist=True, err=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def recursive_overwrite(src, dest, ignore=None):
    import shutil
    import os
    if os.path.isdir(src):
        if not os.path.isdir(dest):
            os.makedirs(dest)
        files = os.listdir(src)
        if ignore is not None:
            ignored = ignore(src, files)
        else:
            ignored = set()
        for f in files:
            if f not in ignored:
                recursive_overwrite(os.path.join(src, f),
                                    os.path.join(dest, f),
                                    ignore)
    else:
        shutil.copyfile(src, dest)

def khongdau(utf8_str):
    import re
    utf8_str = utf8_str.replace(" ", "_").lower()
    INTAB = "ạảãàáâậầấẩẫăắằặẳẵóòọõỏôộổỗồốơờớợởỡéèẻẹẽêếềệểễúùụủũưựữửừứíìịỉĩýỳỷỵỹđ"
    INTAB = [ch.encode('utf8') for ch in unicode(INTAB, 'utf8')]

    OUTTAB = "a"*17 + "o"*17 + "e"*11 + "u"*11 + "i"*5 + "y"*5 + "d"

    r = re.compile("|".join(INTAB))
    replaces_dict = dict(zip(INTAB, OUTTAB))
    return r.sub(lambda m: replaces_dict[m.group(0)], utf8_str)

def make_zip(code):
    try:
        print("make zip: " + DATA_DIC + code)
        shutil.make_archive(DATA_DIC + code, "zip", DATA_DIC + code)
    except Exception as err:
        print(str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def download():
    try:
        code = request.args[0]
        file_path = DATA_DIC + code + ".zip"
        return response.stream(open(file_path, 'rb'), chunk_size=10**6)
    except Exception as err:
        raise HTTP(400, str(err) + " on line " + str(sys.exc_traceback.tb_lineno))

def delete():
    try:
        interactive_id = request.args[0]
        code = db(db.clsb30_interactive.id == interactive_id).select().first()['interactive_code']
        db(db.clsb30_interactive.interactive_code == code).delete()
        if os.path.isdir(HOME_DIC + "temp/" + code):
            shutil.rmtree(HOME_DIC + "temp/" + code)
        if os.path.isdir(DATA_DIC + code):
            shutil.rmtree(DATA_DIC + code)
        if os.path.isfile(DATA_DIC + code + ".zip"):
            os.remove(DATA_DIC + code + ".zip")
        return dict(result=True, mess="Thành công")
    except Exception as err:
        return dict(result=False, mess=str(err) + " on line " + str(sys.exc_traceback.tb_lineno))