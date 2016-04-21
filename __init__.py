# -*- coding: utf-8 -*-

import sys

from PIL import Image, ImageDraw, ImageFont

from util import FILE_TYPE_PNG, FILE_TYPE_TTC, join_path





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
    DEFAULT_FORMAT = FILE_TYPE_PNG
    DEFAULT_FONT = join_path('font.{}'.format(FILE_TYPE_TTC))
    DEFAULT_FONT_SIZE = 18

    MARGIN_LEFT = DEFAULT_FONT_SIZE * 1
    MARGIN_RIGHT = DEFAULT_FONT_SIZE * 2
    MARGIN_TOP = 8
    MARGIN_BOTTOM = 8

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

        assert len(set(widths)) == 1, u'图片宽度不同'

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
                      font_path=DEFAULT_FONT, font_color=RGB_BLACK,
                      background_color=RGB_WHITE, is_header_width=True):
        if not isinstance(text, unicode): text = unicode(text, 'UTF-8')

        font = ImageFont.truetype(font_path, font_size)
        width, height = font.getsize(text)
        if is_header_width: width = self.width
        height += self.MARGIN_TOP
        sys.stdout.write('text_to_png establish width:{}px,height:{}px\n'.format(width, height))
        image = Image.new(self.DEFAULT_IMAGE_MODE, (width, height), background_color)
        draw = ImageDraw.Draw(image)
        draw.text((self.MARGIN_LEFT, self.MARGIN_TOP), text, font=font, fill=font_color)
        return image

    def __combine_text(self, text='', font_size=DEFAULT_FONT_SIZE,
                       font_path=DEFAULT_FONT, font_color=RGB_BLACK, background_color=RGB_WHITE):
        if not text: return None

        texts = text.split('\n')
        word_count = (self.width - self.MARGIN_LEFT - self.MARGIN_RIGHT) / font_size
        print word_count,
        images = []
        text_sections = [self.__chunks(t.strip(), word_count) for t in texts]
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
        self._footer = Image.new(self.DEFAULT_IMAGE_MODE, size, self.RGB_WHITE)
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
    r = Reader()
    text = u"""
    Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
    """
    chinese_text = u"""
    盼望着，盼望着，东风来了，春天的脚步近了。一切都像刚睡醒的样子，欣欣然张开了眼。山朗润起来了，水涨起来了，太阳的脸红起来了。小草偷偷地从土地里钻出来，嫩嫩的，绿绿的。园子里，田野里，瞧去，一大片一大片满是的。坐着，躺着，打两个滚，踢几脚球，赛几趟跑，捉几回迷藏。风轻俏俏的，草软绵绵的。
    """
    r.text = text
    r.text.save('test.png')

