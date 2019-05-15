# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/5/15 17:11

# desc: 针对os.path提供功能的补充或做一层封装

import os


def FileExt(szPath):
    return os.path.splitext(szPath)[1]

def ParseDir(szPath):
    return os.path.split(szPath)[0]
