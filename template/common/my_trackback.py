# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2020/12/8 9:08

# desc:

import inspect
import logging
import sys
import traceback
import os
import sys
import time
import inspect
import linecache
import pydoc
import tokenize
import keyword
import weakref
import cgitb

InstanceType = None


def Init():
    sys.excepthook = lambda tp, val, tb: _OnTraceback(tp, val, tb, True)


def OnException():
    TypeClass, ValueObj, TracebackObj = sys.exc_info()
    _OnTraceback(TypeClass, ValueObj, TracebackObj)


def _OnTraceback(TypeClass, ValueObj, TracebackObj, bSysExcepthook=False):
    sys.last_type = TypeClass
    sys.last_value = ValueObj
    sys.last_traceback = TracebackObj

    szStack = _Stack(TracebackObj, bSysExcepthook)
    szCode = _Code(TracebackObj)
    szLocalVar = _LocalVar(TracebackObj)
    szError = "\n".join(["Traceback (most recent call last):", szStack, szCode, "\n  Local var:", szLocalVar])

    logging.error("\n" + szError)

    try:
        g_AppObj.GetDingDingMgr().Send(szError)
    except BaseException:
        logging.getLogger("myLog").error("\n\n{0}\n".format(traceback.format_exc()))


def _Stack(eTb, bSysExcepthook):
    listFinalRecords = []

    listRecordsInner = inspect.getinnerframes(eTb, 1)
    if bSysExcepthook is False:
        listRecordsOut = inspect.stack()
        nLenRecordsOut = len(listRecordsOut)
        nLenRecordsOut = nLenRecordsOut - 1
        if nLenRecordsOut > 0:
            for nIndex in range(nLenRecordsOut, 2, -1):
                listFinalRecords.append(listRecordsOut[nIndex])

    for Record in listRecordsInner:
        listFinalRecords.append(Record)

    listMsg = []

    szFormat = '  File "{0}", line {1}, in {2}\n    {3}\n'
    for Record in listFinalRecords:
        _, szSourceFullPath, nLine, szFunName, listLine, nIndex = Record
        szLine = listLine[nIndex].strip()

        listMsg.append(szFormat.format(szSourceFullPath, nLine, szFunName, szLine))

    return "".join(listMsg)


def _Code(TracebackObj):
    listCode = []

    listRecords = inspect.getinnerframes(TracebackObj, 10)
    FrameObj, szSourceFullPath, nNum, szFunName, listLine, nIndex = listRecords[-1]

    if nIndex is not None:
        i = nNum - nIndex
        for szLine in listLine:
            if i == nNum:
                szNum = '>%6d ' % i
            else:
                szNum = ' %6d ' % i
            listCode.append(szNum + szLine.rstrip())
            i += 1

    return "\n".join(listCode)


def _LocalVar(TracebackObj):
    # ref cgitb.text https://svn.python.org/projects/python/trunk/Lib/cgitb.py
    listRecords = inspect.getinnerframes(TracebackObj, 10)
    FrameObj, szSourceFullPath, nNum, szFunName, szLines, nIndex = listRecords[-1]
    _, _, _, listLocals = inspect.getargvalues(FrameObj)

    dictHighlight = {}

    def ReaderFun(listNum=None):
        if listNum is None:
            listNum = [nNum]
        dictHighlight[listNum[0]] = 1
        try:
            return linecache.getline(szSourceFullPath, listNum[0])
        finally:
            listNum[0] += 1

    listVars = cgitb.scanvars(ReaderFun, FrameObj, listLocals)

    dictDone, listLocalValue = {}, []
    for szKey, szWhere, ValueObj in listVars:
        if szKey in dictDone:
            continue
        dictDone[szKey] = 1
        if ValueObj is not cgitb.__UNDEF__:
            if szWhere == 'global':
                szKey = 'global ' + szKey
            elif szWhere != 'local':
                szKey = szWhere + szKey.split('.')[-1]
            listLocalValue.append('    %s = %s' % (szKey, pydoc.text.repr(ValueObj)))
        else:
            listLocalValue.append('    undefined: ' + szKey)

    return "\n".join(listLocalValue)

