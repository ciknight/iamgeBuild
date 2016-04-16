# -*- coding: utf-8 -*-

import sys

from PIL import Image

from util import join_path


class Reader(object):

    DEFAULT_IMAGE_MODE = 'RGB'
    DEFAULT_WIDTH = 750

    def __init__(self):
        super(Reader, self).__init__()

    def combined(self, *args):
        if not args: raise ValueError(u'图片不能为空')
        widths = []
        new_height = 0
        for image in args:
            if not image:
                continue
            new_height += image.size[1]
            widths.append(image.size[0])
        if len(set(widths)) != 1: raise ValueError(u'图片宽度不同')
        width = widths[0]
        if width != self.DEFAULT_WIDTH:
            sys.stdout.write(u'suggest width use {}px\n'.format(self.DEFAULT_WIDTH))
        size = (width, new_height)
        im = Image.new(self.DEFAULT_IMAGE_MODE, size)
        return im

    @staticmethod
    def __reg_img(path):
        path = join_path(path)
        return Image.open(path)

    @property
    def header(self):
        return self._header

    @header.setter
    def header(self, header_path):
        self._header = self.__reg_img(header_path)

    @header.getter
    def header(self):
        if self._header.size[0] != self.DEFAULT_WIDTH:
            sys.stdout.write(u'suggest width use {}px\n'.format(self.DEFAULT_WIDTH))
        return self._header

    @property
    def footer(self):
        return self._footer

    @footer.setter
    def footer(self, footer_text='', width=None, color=None):
        if not width: width= self.DEFAULT_WIDTH
        size = (width, 100)
        if not color: color=(255,255,255)
        self._footer = Image.new(self.DEFAULT_IMAGE_MODE, size, color)
        return self

    @footer.getter
    def footer(self):
        return self._footer

if __name__ == '__main__':
    # file = join_path('source_1.png')
    # im = Image.open(file)
    # print im.format, im.size, im.mode
    r = Reader()
    r.header = 'source_1.png'
    r.footer = ''
    im = r.combined(r.header, r.footer)
    im.save('test.png')
