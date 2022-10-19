# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:05

# desc:

class TaskCommand:
    """"""

    def __init__(self, szCommandFormat: str):
        self.m_szComandFormat = szCommandFormat

    def ToStr(self):
        return self.m_szComandFormat
