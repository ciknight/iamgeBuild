# -*- coding: utf-8 -*-

import os


RUNNING_PATH = os.path.abspath('.')


class PathError(Exception):
    def __init__(self, message):
        super(PathError, self).__init__()
        self.message = message


def join_path(file_path):
    path = '{}/{}'.format(RUNNING_PATH, file_path)
    if not os.path.isfile(path): raise PathError(u'路径无效')
    return path
