# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/1/13 22:09

# desc:

import os
import logging


def MyLog(szName):
    if os.path.exists(szName):
        szName = _ConvertFile2ModuleName(szName)

    return logging.getLogger("myLog." + szName)


def _ConvertFile2ModuleName(szFullPath):
    assert os.path.exists(szFullPath), "文件路径不存在" + szFullPath

    szRelPath = os.path.relpath(szFullPath, os.getcwd())
    szRelPathNoExt = os.path.splitext(szRelPath)[0]
    szModuleName = szRelPathNoExt.replace("\\", ".").replace("/", ".")

    return szModuleName
