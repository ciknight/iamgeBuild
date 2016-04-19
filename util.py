# -*- coding: utf-8 -*-

import os


RUNNING_PATH = os.getcwd()
ALL_SUPPORT_FILE = (
    'jpg',
    'jpeg',
    'png',
    'ttc',
    'ttf'
)
(
    FILE_TYPE_JPG,
    FILE_TYPE_JPEG,
    FILE_TYPE_PNG,
    FILE_TYPE_TTC,
    FULE_TYPE_TTF
) = ALL_SUPPORT_FILE


class PathError(Exception):
    def __init__(self, message):
        super(PathError, self).__init__()
        self.message = message


def join_path(file_path):
    type = file_path.split('.')[-1]
    assert type in ALL_SUPPORT_FILE, u'文件类型不支持'
    path = '{}/{}'.format(RUNNING_PATH, file_path)
    if not os.path.isfile(path): raise PathError(u'必须是个文件')
    return path
