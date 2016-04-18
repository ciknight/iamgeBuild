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
    DEFAULT_FONT_SIZE = 18

    WHITE = 0xffffff
    BLACK = 0x000000

    RGB_WHITE = (255, 255, 255)
    RGB_BLACK = (0, 0, 0)
    RGBA_OPACITY = (0, 0, 0, 0)

    def __init__(self, width=None, **kwargs):
        super(Reader, self).__init__()
        if not width: self.width = self.DEFAULT_WIDTH
        self.footer_height = 60
        self.text_background_color = kwargs.get('text_background_color', self.RGB_WHITE)
        self.font_size = kwargs.get('font_size', self.RGB_WHITE)
        self.font = kwargs.get('font', self.DEFAULT_FONT)
        self.font_color = kwargs.get('font_color', self.RGB_BLACK)

    def __suggest_width(self, width):
        if width != self.DEFAULT_WIDTH:
            sys.stdout.write(u'suggest width use {}px\n'.format(self.DEFAULT_WIDTH))

    def __combine_imgs(self, *args):
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
        combine_img = Image.new(self.OPACITY_IMAGE_MODE, size, self.RGBA_OPACITY)

        paste_height = 0
        for _, image in enumerate(args):
            combine_img.paste(image, (0, paste_height))
            paste_height += image.size[1]
        # TODO <ci_knight@msn.cn>> height over the max height
        return combine_img

    @classmethod
    def combine_img(cls, *args):
        return cls.__combine_imgs(*args)

    def __text_to_png(self, text='', font_size=DEFAULT_FONT_SIZE,
                      font_path=DEFAULT_FONT, font_color=RGB_BLACK, background_color=RGB_WHITE):
        if not isinstance(text, unicode): text = unicode(text, 'UTF-8')

        font = ImageFont.truetype(font_path, font_size)
        width, height = font.getsize(text)
        if width > self.width: width = self.width

        sys.stdout.write('text_to_png establish width:{}px,height:{}px\n'.format(width, height))
        image = Image.new(self.DEFAULT_IMAGE_MODE, (width, height), background_color)
        draw = ImageDraw.Draw(image)
        draw.text((0, 0), text, font=font, fill=font_color)
        return image

    def __combine_text(self, text='', font_size=DEFAULT_FONT_SIZE,
                       font_path=DEFAULT_FONT, font_color=RGB_BLACK, background_color=RGB_WHITE):
        if not text: return None
        texts = text.split('\n')
        margin = 50
        word_count = (self.width - margin) / font_size
        images = []
        text_sections = [self.__chunks(t, word_count) for t in texts]
        for text_lines in text_sections:
            for t in text_lines:
                image = self.__text_to_png(text=t,
                                           font_size=font_size,
                                           font_path=font_path,
                                           font_color=font_color,
                                           background_color=background_color)
                images.append(image)
        return self.__combine_imgs(*images)

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text=''):
        self._text = self.__combine_text(text)
        return self

    @text.getter
    def text(self):
        return self._text

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
    def footer(self, text=''):
        size = (self.width, self.footer_height)
        self._footer = Image.new(self.DEFAULT_IMAGE_MODE, size, self.WHITE)
        return self

    @footer.getter
    def footer(self):
        return self._footer

    # TODO <ci_knight@msn.cn> title

    @staticmethod
    def __reg_img(path):
        path = join_path(path)
        return Image.open(path)

    @staticmethod
    def __chunks(text, setp):
        for i in xrange(0, len(text), setp):
            yield text[i:i+setp]


class Blog(Reader):

    def __init__(self, width=None):
        super(Blog, self).__init__(width)

    def build(self):
        pass


if __name__ == '__main__':
    # file = join_path('source_1.png')
    # im = Image.open(file)
    # print im.format, im.size, im.mode
    r = Reader()
    #r.header = 'source_1.png'
    #r.footer = ''
    #im = r.combined(r.header, r.footer)
    text = u"hello world"
    r.text = text
    r.text.save('test.png')

