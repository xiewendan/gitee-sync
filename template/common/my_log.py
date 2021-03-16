# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/1/13 22:09

# desc:

import inspect
import logging
import os
from functools import wraps

_g_nMaxSeperate = 40
_g_nMinSeperate = 5
_g_nCurSeperate = _g_nMaxSeperate
_g_nStep = 5
_g_szSeperate = "=" * _g_nMaxSeperate


def MyLog(szName):
    if os.path.exists(szName):
        szName = _ConvertFile2ModuleName(szName)

    return logging.getLogger("myLog." + szName)


def SeperateWrap():
    CallerFrameRecordObj = inspect.stack()[1]  # 0 represents this line
    FrameObj = CallerFrameRecordObj[0]
    InfoObj = inspect.getframeinfo(FrameObj)
    nLineNo = InfoObj.lineno
    szFileName = os.path.basename(InfoObj.filename)
    LoggerObj = logging.getLogger()

    def Seperate(FunObj):
        @wraps(FunObj)
        def A(*args, **kwargs):
            LoggerObj.debug("%s begin %s - %s:%d", _GetBeginSeperate(), szFileName, FunObj.__name__, nLineNo)

            ResultObj = FunObj(*args, **kwargs)

            LoggerObj.debug("%s end %s - %s:%d", _GetEndSeperate(), szFileName, FunObj.__name__, nLineNo)

            return ResultObj

        return A

    return Seperate


def _ConvertFile2ModuleName(szFullPath):
    assert os.path.exists(szFullPath), "文件路径不存在" + szFullPath

    szRelPath = os.path.relpath(szFullPath, os.getcwd())
    szRelPathNoExt = os.path.splitext(szRelPath)[0]
    szModuleName = szRelPathNoExt.replace("\\", ".").replace("/", ".")

    return szModuleName


def _AddCurSeperate(nStep):
    global _g_nCurSeperate
    _g_nCurSeperate += nStep

    return min(max(_g_nCurSeperate, _g_nMinSeperate), _g_nMaxSeperate)


def _GetBeginSeperate():
    szSeperate = _g_szSeperate[:_g_nCurSeperate]
    _AddCurSeperate(-_g_nStep)

    return szSeperate


def _GetEndSeperate():
    _AddCurSeperate(_g_nStep)
    return _g_szSeperate[:_g_nCurSeperate]
