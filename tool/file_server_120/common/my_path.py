# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2019/5/15 17:11

# desc: 针对os.path提供功能的补充或做一层封装

import os


# "a/b/c.txt -> .txt"
def FileExt(szPath):
    return os.path.splitext(szPath)[1]


def ParseDir(szPath):
    return os.path.split(szPath)[0]


# "a/b/c.txt -> c"
# "a/b/c     -> c"
def FileName(szPath):
    szBaseName = os.path.basename(szPath)
    return os.path.splitext(szBaseName)[0]


# "a/b/c.txt -> c.txt"
def FileNameWithExt(szPath):
    return os.path.basename(szPath)


def CreateFileDir(szFilePath):
    szDir = ParseDir(szFilePath)
    if not os.path.exists(szDir):
        os.makedirs(szDir)
