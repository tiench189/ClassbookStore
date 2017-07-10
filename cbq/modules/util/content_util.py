# -*- coding: utf-8 -*-
__author__ = 'User'

from applications.cbq.modules.entities.json_entities.img_entity import ImageEntity
from applications.cbq.modules.util import file_util
from applications.cbq.modules.entities import app_constant
import time


def parse_question_content(content):
    index = 0
    list_json = list()

    list_image_object = get_list_image_object(content)
    for img_object in list_image_object:
        file_util.download_img_from_url(img_object.src, app_constant.home_dir + '/admin/media')
    list_img_url = get_list_image_url(content)

    for img_object in list_image_object:
        json_string = parse_img_to_json_string(img_object)
        content = content.replace(list_img_url[index], json_string)
        index += 1
    return content


def get_list_image_object(content):
    list_img = list()
    prefix_img = '<img'
    prefix_end_img = '/>'
    while content.find(prefix_img) > 0:
        index = content.find(prefix_img)
        end_index = content.find(prefix_end_img)
        end_index += len(prefix_end_img)
        img_url = content[index:end_index]
        img_object = parse_img_url_to_object(img_url)
        list_img.append(img_object)

        content = content[end_index:]

    return list_img


def get_list_image_url(content):
    list_img_url = list()
    prefix_img = '<img'
    prefix_end_img = '/>'
    while content.find(prefix_img) > 0:
        index = content.find(prefix_img)
        end_index = content.find(prefix_end_img)
        end_index += len(prefix_end_img)
        img_url = content[index:end_index]
        list_img_url.append(img_url)
        content = content[end_index:]

    return list_img_url


def parse_img_url_to_object(img_url):
    #<img alt="" src="http://hatgionghoa.net/images/stories/baiviet/hoa_hong_8-3-20130506152206.jpg"
    # style="height:768px; width:1024px" />

    img_object = ImageEntity()
    index_alt = img_url.find(ImageEntity.alt_prop) + len(ImageEntity.alt_prop)

    img_url = img_url[index_alt:]
    alt_value = img_url[index_alt:img_url.find('"')]
    img_object.alt = alt_value

    index_src = img_url.find(ImageEntity.src_prop)
    img_url = img_url[index_src:]

    img_url = img_url[len(ImageEntity.src_prop):]
    src_value = img_url[:img_url.find('"')]
    img_object.src = src_value

    index_height = img_url.find(ImageEntity.height_prop)
    img_url = img_url[index_height + len(ImageEntity.height_prop):]
    height_value = img_url[:img_url.find(';')]
    height_value = height_value.replace('px', '')
    img_object.height = height_value

    index_width = img_url.find(ImageEntity.width_prop)
    img_url = img_url[index_width + len(ImageEntity.width_prop):]
    width_value = img_url[:img_url.find('"')]
    width_value = width_value.replace('px', '')
    img_object.width = width_value

    return img_object


def parse_img_to_json_string(img_object):
    #={"type":"img", "id":"635231442185883062_img" , "src":"vl6_b1_q3.clsbi21" , "width":327, "height":327}=

    file_name = img_object.src.split('/')[-1]
    file_name = file_util.rename_extension(file_name)

    random_id = str(int(round(time.time() * 1000)))
    json_string = '={"type":"img", "id":"'
    json_string += random_id + '_img",'
    json_string += '"src":"' + file_name + '",'
    json_string += ' "width":' + img_object.width + ','
    json_string += ' "height":' + img_object.height + '}='
    #json_string += '"src":"' + file_name + '"'

    return json_string

#content1 = '<p><img alt="" src="http://hatgionghoa.net/images/stories/baiviet/hoa_hong_8-3-20130506152206.jpg" style="height:768px; width:1024px" /></p>'
#list_object = get_list_image_object(content1)
#for img_object in list_object:
#    json_string = parse_img_to_json_string(img_object)
#    print json_string


#
#content11 = '<p><img alt="" src="http://hatgionghoa.net/images/stories/baiviet/hoa_hong_8-3-20130506152206.jpg" ' \
#            'style="height:150px; width:200px" /></p><p>Cho biết </p>'
#print parse_question_content(content11)
