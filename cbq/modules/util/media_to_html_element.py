__author__ = 'User'
import gluon.html
from applications.cbq.modules.entities.json_entities.media_object import MediaObject
from applications.cbq.modules.util import common_util

import ast


tag = 'media_to_html_element'


def get_json_media_list(content):
    media_json_list = list()

    content_tmp = content
    try:
        while MediaObject.prefix_media in content_tmp:
            start_index = content_tmp.index(MediaObject.prefix_media)
            end_index = content_tmp.index(MediaObject.suffix_media)

            str_json = content_tmp[start_index:end_index + 1]

            content_tmp = content_tmp[end_index + 2:]

            str_json = str_json.replace(MediaObject.prefix_media, "{")
            media_json_list.append(str_json)
    except Exception as e:
        print str(e)
        return None
    return media_json_list


def get_list_source_media_object(content):
    """
    @todo : get list content object (modules/entities/json_entities/json_content
    @param content:
    @return:
    """
    media_list_obj = list()
    content_tmp = content
    try:
        while MediaObject.prefix_media in content_tmp:
            start_index = content_tmp.index(MediaObject.prefix_media)
            end_index = content_tmp.index(MediaObject.suffix_media)

            str_json = content_tmp[start_index:end_index + 1]

            content_tmp = content_tmp[end_index + 2:]

            # analyse str_json:
            str_json = str_json.replace(MediaObject.prefix_media, "{")
            #media_obj = MediaObject()

            for key, value in ast.literal_eval(str_json).iteritems():
                if str(key) == str(MediaObject.item_src_field):
                    media_list_obj.append(str(value))
            if content_tmp is None or content_tmp.strip() == "":
                break
    except Exception as e:
        print str(e)
        return None
    return media_list_obj


def get_media_object_list(content):
    """
    @todo :
    @param content: question content
    @return:
    """
    media_object_list = list()
    content_tmp = content
    try:
        while MediaObject.prefix_media in content_tmp:
            start_index = content_tmp.index(MediaObject.prefix_media)
            end_index = content_tmp.index(MediaObject.suffix_media)

            str_json = content_tmp[start_index:end_index + 1]

            content_tmp = content_tmp[end_index + 2:]

            # analyse str_json:
            str_json = str_json.replace(MediaObject.prefix_media, "{")
            media_obj = MediaObject()

            for key, value in ast.literal_eval(str_json).iteritems():
                if str(key) == str(MediaObject.item_id_field):
                    media_obj.item_id = str(value)
                elif str(key) == str(MediaObject.item_src_field):
                    media_obj.source = str(value)
                elif str(key) == str(MediaObject.item_type_field):
                    media_obj.item_type = str(value)
                elif str(key) == str(MediaObject.item_width_field):
                    media_obj.width = str(value)
                elif str(key) == str(MediaObject.item_height_field):
                    media_obj.height = str(value)
            media_object_list.append(media_obj)
    except Exception as e:
        print tag + 'get_media_object_list' + str(e)
    return media_object_list


def get_media_list(content):
    """ return media list  : img, audio, video
        get media list in content
    """
    media_list_obj = list()
    content_tmp = content
    try:
        while MediaObject.prefix_media in content_tmp:
            start_index = content_tmp.index(MediaObject.prefix_media)
            end_index = content_tmp.index(MediaObject.suffix_media)

            str_json = content_tmp[start_index:end_index + 1]

            content_tmp = content_tmp[end_index + 2:]

            # analyse str_json:
            str_json = str_json.replace(MediaObject.prefix_media, "{")
            media_obj = MediaObject()
            media_dict = dict()
            for key, value in ast.literal_eval(str_json).iteritems():
                if str(key) == str(MediaObject.item_id_field):
                    media_obj.item_id = str(value)
                elif str(key) == str(MediaObject.item_src_field):
                    media_obj.source = str(value)
                elif str(key) == str(MediaObject.item_type_field):
                    media_obj.item_type = str(value)
                elif str(key) == str(MediaObject.item_width_field):
                    media_obj.width = str(value)
                elif str(key) == str(MediaObject.item_height_field):
                    media_obj.height = str(value)
            media_dict['json'] = str_json
            media_dict['html'] = convert_media_obj_to_html(media_obj)
            media_list_obj.append(media_dict)
            if content_tmp is None or content_tmp.strip() == "":
                break
    except Exception as e:
        print tag + str(e)
        return None
    return media_list_obj


def convert_media_obj_to_html(media_obj):
    """ return html string
        convert media object ( audio, image, video ) to html element
    """
    html_element_obj = None

    if media_obj.item_type == MediaObject.image_type:
        html_element_obj = convert_image_object(media_obj)
    elif media_obj.item_type == MediaObject.audio_type:
        html_element_obj = convert_audio_object(media_obj)
    elif media_obj.item_type == MediaObject.video_type:
        html_element_obj = convert_video_object()
    return html_element_obj


def convert_image_object(img_obj):
    """ return html img element
        convert media object to html element
    """
    img_element = '<img src = "OBJECT_SOURCE" id = "OBJECT_ID" width = "OBJECT_WIDTH" height = "OBJECT_HEIGHT" />'
    file_name = common_util.get_file_name(img_obj.source)
    ext = common_util.get_ext_file(img_obj.source)
    url1 = "/cbq/download/cover/" + file_name + "/" + ext

    img_element = img_element.replace("OBJECT_SOURCE", str(url1)) #+ str(img_obj.source)))
    img_element = img_element.replace("OBJECT_ID", str(img_obj.item_id))
    img_element = img_element.replace("OBJECT_WIDTH", str(img_obj.width))
    img_element = img_element.replace("OBJECT_HEIGHT", str(img_obj.height))

    return img_element


def convert_video_object(video_obj):
    """ return html img element
        convert media object to html element
    """
    video_element = '<video width="OBJECT_WIDTH" height="OBJECT_HEIGHT" controls><source src="OBJECT_SOURCE"' \
                    ' type="video/mp4"><param name="autoplay" value="false"><source src="movie.ogg" type="video/ogg">' \
                    'Your browser does' \
                    ' not support the video tag.</video>'

    video_element = video_element.replace("OBJECT_SOURCE", video_obj.source)
    video_element = video_element.replace("OBJECT_WIDTH", video_obj.width)
    video_element = video_element.replace("OBJECT_HEIGHT", video_obj.height)
    #audio_element = audio_element.replace("OBJECT_ID", audio_obj.item_id)

    return video_element


def convert_audio_object(audio_obj):
    """

    @param audio_obj:
    @return: html audio tag
    """
    #audio_element = '<audio controls="controls">' \
    #                '<source src="OBJECT_SOURCE" type="audio/clsbs10">' \
    #                '</audio >'

    audio_element = '<object type="application/x-shockwave-flash" data="http://192.168.50.75:8003/cbq/static/player_mp3_maxi.swf" width="200" height="20">' \
                    '<param name="movie" value="http://192.168.50.75:8003/cbq/static/player_mp3_maxi.swf">' \
                    '<param name="FlashVars" value="mp3=OBJECT_SOURCE&amp;showinfo=1&amp;textcolor=666666&amp;buttoncolor=666666&amp;buttonovercolor=000000&amp;bgcolor1=f5f5f5&amp;bgcolor2=cccccc&amp;sliderovercolor=333333">' \
                    '</object>'

    #audio_element = '<object type="application/x-shockwave-flash" data="http://192.168.50.75:8003/cbq/static/player.swf?url=OBJECT_SOURCE&amp;' \
    #                'volume=100&amp;autoPlay=false" width="640px" height="480px" wmode="opaque" id="video_overlay">' \
    #                '<param name="allowScriptAccess" value="always"><param name="allowFullScreen" value="true">' \
    #                '<param name="FlashVars" value=""></object>'

    file_name = common_util.get_file_name(audio_obj.source)
    ext = common_util.get_ext_file(audio_obj.source)

    #url1 = "http://192.168.50.75:8003/cbq/static/media/" + file_name + "." + ext
    url1 = "/cbq/download/cover/" + file_name + "/" + ext

    #print str(url1)
    audio_element = audio_element.replace("OBJECT_SOURCE", str(url1))

    return audio_element


def convert_question_content_to_html(content):
    media_list = get_media_list(content)

    for media in media_list:
        content = content.replace("=" + media['json'] + "=", media['html'])

    return content

#
#str1 = 'Example: 1. Ann is slimmer than Laura. '\
#       '(slim)<br><br> ={"type":"img",' \
#       ' "id":"635117337583809310_img_1" , "src":"41_U4_1.jpg" , "width":200, "height":300}= abc djhajjjhjhhhj' \
#       ' ={"type":"audio", "id":"635117337232553164_sound_1" , "src":"U1_-_ACL1_-_6_-_tit.mp3" ' \
#       ',"width": 300, "height": 200,"media_type":"audio/mpeg"}='
##
#content1 = get_list_content_object(str1)
#for c in content1:
#    print str(c.source)
#media_list = get_media_list(str1)
#print 'Size  : ' + str(len(media_list))
#for media in media_list:
#    #print "Media source : " + str(media.source)
#    #print "Media type = " + str(media.item_type)
#    #print media.item_type
#    #print media.width
#    html_element = convert_media_obj_to_html(media)
#    print html_element
