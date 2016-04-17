# -*- coding: utf-8 -*-

import sys

from PIL import Image, ImageDraw, ImageFont

from util import join_path


class Reader(object):
    """Usage
    >>> r = Reader()
    >>> r.header = 'relative_path'
    >>> r.footer = 'message'

    Image.size = (width, height)
    """

    DEFAULT_IMAGE_MODE = 'RGB'
    OPACITY_IMAGE_MODE = 'RGBA'
    DEFAULT_WIDTH = 750  # default ios width
    DEFAULT_FORMAT = 'PNG'
    DEFAULT_FONT = join_path('font.ttc')

    WHITE = 0xffffff
    BLACK = 0x000000

    RGB_WHITE = (255, 255, 255)
    RGB_BLACK = (0, 0, 0)


    def __init__(self):
        super(Reader, self).__init__()
        self.width = self.DEFAULT_WIDTH

    def __suggest_width(self, width):
        if width != self.DEFAULT_WIDTH:
            sys.stdout.write(u'suggest width use {}px\n'.format(self.DEFAULT_WIDTH))

    def text_to_png(self, text='', font_size=16, font_path=None):
        if not font_path: font_path = self.DEFAULT_FONT
        if not isinstance(text, unicode): text = unicode(text, 'UTF-8')
        font = ImageFont.truetype(font_path, font_size)
        width, height = font.getsize(text)
        if width > self.width: width = self.width
        sys.stdout.write('text_to_png establish width:{}px,height:{}px\n'.format(width, height))
        image = Image.new(self.DEFAULT_IMAGE_MODE, (width, height), self.WHITE)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=self.RGB_BLACK)
        return image

    def combined(self, *args):
        if not args: raise ValueError(u'图片不能为空')

        widths, new_height = [], 0
        for image in args:
            if not image:continue
            new_height += image.size[1]
            widths.append(image.size[0])

        if len(set(widths)) != 1: raise ValueError(u'图片宽度不同')

        width = widths[0]
        self.__suggest_width(width)
        size = (width, new_height)
        combine_img = Image.new(self.DEFAULT_IMAGE_MODE, size, self.WHITE)

        paste_height = 0
        for _, image in enumerate(args):
            combine_img.paste(image, (0, paste_height))
            paste_height += image.size[1]
        # TODO <ci_knight@msn.cn>> height over the max height

        return combine_img

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
        self.width = self.header.size[0]
        return self

    @header.getter
    def header(self):
        self.__suggest_width(self.header.size[0])
        return self._header

    @property
    def footer(self):
        return self._footer

    @footer.setter
    def footer(self, footer_text='', width=None, color=None):
        if not width: width= self.width
        size = (width, 100)
        if not color: color=self.BLACK
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
    #r.header = 'source_1.png'
    #r.footer = ''
    #im = r.combined(r.header, r.footer)
    text = u"   你好~我是第一封可生成的字符库，你是我的我是你的。哈哈哈哈哈哈"
    im = r.text_to_png(text, font_size=24)
    im.save('test.png')

