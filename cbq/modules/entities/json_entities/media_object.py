__author__ = 'User'


class MediaObject(object):

    prefix_media = '={'
    suffix_media = '}='

    item_type_field = 'type'
    item_id_field = 'id'
    item_src_field = 'src'
    item_width_field = 'width'
    item_height_field = 'height'

    image_type = 'img'
    audio_type = 'audio'
    video_type = 'video'

    def __init__(self):
        self.item_type = None
        self.item_id = None
        self.source = None
        self.width = None
        self.height = None

    def print_info(self):
        info = "Media object : "
        info += "type: " + str(self.item_type)
        info += " id: " + str(self.item_id)
        info += " source: " + str(self.source)
        info += " width: " + str(self.width)
        info += " height: " + str(self.height)

        print info