# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2018/11/23 14:22:12

# desc: 异常


class MyException(Exception):
    def __init__(self, *args):
        self.args = args

    @property
    def message(self):
        return self.args
