# -*- coding: utf-8 -*-

__author__ = 'User'

import ast
from applications.cbq.modules.entities.json_entities.answer_json_object import AnswerJsonObject
from applications.cbq.modules.entities.json_entities.json_content import ContentAttr
import time

#file_tag = "answer_to_html_element :"
"""
    @note : need a function to standardized question_answer string
"""


def parse_list_answer_to_html(list_answer, question_type):
    """
    parse list of object question_content to html string
    @param list_answer:
    @param question_type:
    @return:
    """
    html_content_result = ""
    for ans in list_answer:
        # check if ans is null or empty
        #if not ans.question_answer:
        #    continue
        try:

            html_content_result += str(parse_answer_json_to_html(ans, question_type))
        except Exception as e:
            print "parse_list_answer_to_html" + str(e)
            #html_content_result = "<select>" + html_content_result + "</select>"

    return html_content_result


def parse_answer_json_to_html(question_answer_obj, question_type):
    list_object_json = get_list_object_answer(question_answer_obj, question_type)
    content = question_answer_obj.question_answer
    for ans in list_object_json:
        content = content.replace(str(ans['json']), str(ans['html']))

    return content


def get_list_content_object(content_data):
    """ return list content object
        get list content object in attribute "content" of answer object
    """

    list_content = list()

    for content in content_data:

        content_item = ContentAttr()
        for k, v in content.iteritems():

            if str(k) == ContentAttr.item_is_true_field:
                content_item.is_correct = str(v)
            elif str(k) == ContentAttr.item_mark_field:
                content_item.mark = str(v)
            elif str(k) == ContentAttr.item_value_field:
                content_item.value = str(v)
        list_content.append(content_item)

    return list_content


def get_list_json_answer(content):
    """ return list json answer

    """
    list_answer = list()
    content_tmp = content

    while AnswerJsonObject.prefix_json in content_tmp:
        start_index = content_tmp.index(AnswerJsonObject.prefix_json)
        end_index = content_tmp.index(AnswerJsonObject.suffix_json)

        str_json = content_tmp[start_index:end_index + 1]
        content_tmp = content_tmp[end_index + 2:]

        str_json = str_json.replace(AnswerJsonObject.prefix_json, "{")
        list_answer.append(str_json)
    return list_answer


def get_list_object_answer(question_answer_obj, question_type):
    """ return list answer object from answer content
        get list answer object
    @param question_answer_obj:
    @param question_type
    """

    content_tmp = question_answer_obj.question_answer
    list_answer = list()

    # TH type MC trong moodle
    if question_type == AnswerJsonObject.answer_radio_type:
        answer_dict = dict()
        answer_obj = AnswerJsonObject()
        answer_obj.type = "radio"
        answer_obj.content = content_tmp

        html_element = parse_json_object_to_html_element(answer_obj, question_answer_obj, question_type)
        answer_dict['json'] = content_tmp
        answer_dict['html'] = html_element
        list_answer.append(answer_dict)

        return list_answer

    # type PC
    if question_type == AnswerJsonObject.answer_checkbox_type or question_type == AnswerJsonObject.answer_radio_type:
        answer_dict = dict()
        answer_obj = AnswerJsonObject()
        answer_obj.content = content_tmp

        html_element = parse_json_object_to_html_element(answer_obj, question_answer_obj, question_type)

        answer_dict['json'] = content_tmp
        answer_dict['html'] = html_element
        list_answer.append(answer_dict)

        return list_answer
        #if question_type == AnswerJsonObject.answer_radio_type:
    #    answer_dict = dict()
    #    answer_obj = AnswerJsonObject()
    #    answer_obj.content = content_tmp

    while AnswerJsonObject.prefix_json in content_tmp:

        answer_dict = dict()
        start_index = content_tmp.index(AnswerJsonObject.prefix_json)
        end_index = content_tmp.index(AnswerJsonObject.suffix_json)

        str_json = content_tmp[start_index:end_index + 1]

        content_tmp = content_tmp[end_index + 2:]

        str_json = str_json.replace(AnswerJsonObject.prefix_json, "{")

        str_pre_json = str_json
        if 'true' in str_json:
            str_json = str_json.replace('true', 'True')
        if 'false' in str_json:
            str_json = str_json.replace('false', 'False')

        answer_obj = AnswerJsonObject()
        for key, value in ast.literal_eval(str_json).iteritems():

            if str(key) == AnswerJsonObject.item_id_field:
                answer_obj.item_id = str(value)
            elif str(key) == AnswerJsonObject.size_field:
                answer_obj.size = str(value)
            elif str(key) == AnswerJsonObject.item_type_field:
                answer_obj.type = str(value)
            elif str(key) == AnswerJsonObject.content_field:
                answer_obj.content = get_list_content_object(value)

        html_element = parse_json_object_to_html_element(answer_obj, question_answer_obj, question_type)
        answer_dict['json'] = "=" + str(str_pre_json) + "="
        answer_dict['html'] = html_element
        list_answer.append(answer_dict)
    if len(list_answer) < 1:
        answer_dict = dict()
        answer_dict['json'] = content_tmp
        answer_dict['html'] = content_tmp
        list_answer.append(answer_dict)
    return list_answer


def parse_json_object_to_html_element(json_object, question_answer_obj, question_type):
    """
        @return html string
    """
    html_element = ""
    if question_type == AnswerJsonObject.answer_textbox_type or question_type == AnswerJsonObject.answer_sequences_type:

        html_element = parse_text_box(json_object, question_answer_obj) + "<br/>"

    elif question_type == AnswerJsonObject.answer_cb_type:#answer_mc_combobox_type:
        html_element = parse_mc_combobox_html(json_object)
        html_element = "<select class='basic_combobox'>" + html_element + "</select><br/>"

    elif question_type == AnswerJsonObject.answer_radio_type:
        html_element = parse_radio_html(json_object, question_answer_obj)

    elif question_type == AnswerJsonObject.answer_tf_type:
        html_element = parse_mc_combobox_html(json_object)
        html_element = "<select class='basic_combobox'>" + html_element + "</select><br/>"

    elif question_type == AnswerJsonObject.answer_matching_type:
        html_element = parse_mc_combobox_html(json_object)
        html_element = "<select class='basic_combobox'>" + html_element + "</select><br/>"

    elif question_type == AnswerJsonObject.answer_checkbox_type:
        html_element = parse_pc_checkbox_html(json_object, question_answer_obj)

    return html_element


def parse_pc_checkbox_html(json_object, question_answer_obj):
    """
    parse json answer object to checkbox html
    @param json_object:
    @return:
    """
    html_element = '<input type = "checkbox" value = "OBJECT_VALUE" CHECKED readonly>OBJECT_VALUE<br>'
    html_element = html_element.replace("OBJECT_VALUE", json_object.content)
    if question_answer_obj.is_correct is True:
        html_element = html_element.replace("CHECKED", 'checked="checked"')
    else:
        html_element = html_element.replace("CHECKED", "")

    return html_element


def parse_mc_combobox_html(json_object):
    """
    parse json answer object to combobox html
    @param json_object:
    @return:
    """
    html_element = ""

    for attr_content in json_object.content:
        html_element_tmp = '<option value="OBJECT_VALUE" selected readonly>OBJECT_VALUE</option>'
        html_element_tmp = html_element_tmp.replace("OBJECT_VALUE", str(attr_content.value))

        if attr_content.is_correct is False or attr_content.is_correct == 'False':
            html_element_tmp = html_element_tmp.replace("selected", '')
        else:
            html_element_tmp = html_element_tmp.replace("selected", 'selected="selected"')
        html_element += html_element_tmp
    return html_element


def parse_radio_html(json_object, question_answer_obj):
    """
    use for type MC_1, import form moodle
    @param json_object:
    @return: string html of radio
    """
    try:

        if "</span>" in json_object.content:
            json_object.content = json_object.content.replace("</span>", "")
        random_name = str(int(round(time.time() * 1000)))
        html_element = '<input type="radio" IS_CHECKED name=\"' + random_name + '\" value="OBJECT_VALUE" >OBJECT_VALUE<br>'
        ans_content = json_object.content.replace('</span>', '')
        html_element = html_element.replace("OBJECT_VALUE", ans_content)
        html_element = html_element.replace("OBJECT_TYPE", json_object.type)

        if question_answer_obj.is_correct is not None:

            if question_answer_obj.is_correct is True:
                html_element = html_element.replace('IS_CHECKED', 'checked="checked"')
            else:
                html_element = html_element.replace("IS_CHECKED", "")
        return html_element
    except Exception as e:
        print "parse_radio_html error "


def parse_combobox_html(json_object, question_answer_obj):
    """

    @param json_object:
    @return: string html of combobox
    """

    html_element = '<option value="OBJECT_VALUE" readonly>OBJECT_VALUE</option>'
    html_element = html_element.replace("OBJECT_VALUE", json_object.content)
    return html_element


def parse_text_box(json_object, question_answer_obj):
    """ return string html of text box
        parse json object to text box html
    """

    answer_content = ""
    html_element = '<input type="text" value = "OBJECT_VALUE" id = "OBJECT_ID" style="width:OBJECT_SIZEpx;" readonly/>'

    html_element = html_element.replace("OBJECT_ID", json_object.item_id)
    if json_object.size is not None:
        html_element = html_element.replace("OBJECT_SIZE", json_object.size)
    else:
        html_element = html_element.replace("OBJECT_SIZE", "50")
    for attr_content in json_object.content:
        answer_content += attr_content.value
        answer_content += "/"
    if answer_content.endswith("/"):
        answer_content = answer_content[0:(len(answer_content) - 1)]
    html_element = html_element.replace("OBJECT_VALUE", answer_content)
    return html_element


    #data = 'Mọi cơ thể sống đều được cấu tạo từ tế bào và các tế bào đều tham gia vào chức năng ' \
    #       'hoạt động của các cơ quan</span>'
    #
    #data = parse_answer_json_to_html(data, "MC")
    #print data