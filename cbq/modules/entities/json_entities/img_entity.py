__author__ = 'User'


class ImageEntity(object):

    alt_prop = 'alt='
    src_prop = 'src="'
    width_prop = 'width:'
    height_prop = 'height:'
    style_prop = 'style="'

    def __init__(self):
        self.alt = None
        self.src = None
        self.width = None
        self.height = None
