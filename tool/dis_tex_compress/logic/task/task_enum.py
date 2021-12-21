# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/31 2:05

# desc:

class ETaskState:
    eTodo = "todo"
    eDoing = "doing"
    eAccept = "accept"
    ePrepare = "prepare"
    eCreate = "create"
    eConnecting = "connecting"
    ePreparing = "preparing"
    ePrepared = "prepared"
    eExecing = "execing"
    eReturning = "returning"
    eFailed = "failed"
    eNone = "none"
    eSucceed = "succeed"


class ETaskType:
    eDis = 1
    eAccept = 2


class EVarType:
    eFile = 1
    eDir = 2

    dictStr = {
        eFile: "file",
        eDir: "dir"
    }

    dictType = {
        "file": eFile,
        "dir": eDir,
    }

    @staticmethod
    def ToType(szType):
        if isinstance(szType, int):
            assert szType in EVarType.dictStr
            return szType

        assert szType in EVarType.dictType
        return EVarType.dictType[szType]

    @staticmethod
    def ToStr(nType):
        assert nType in EVarType.dictStr
        return EVarType.dictStr[nType]


class EIotType:
    eInput = 1
    eOutput = 2
    eTemp = 3

    dictStr = {
        eInput: "input",
        eOutput: "output",
        eTemp: "temp",
    }

    dictType = {
        "input": eInput,
        "output": eOutput,
        "temp": eTemp,
    }

    @staticmethod
    def ToType(szType):
        if isinstance(szType, int):
            assert szType in EIotType.dictStr
            return szType

        assert szType in EIotType.dictType
        return EIotType.dictType[szType]

    @staticmethod
    def ToStr(nType):
        assert nType in EIotType.dictStr
        return EIotType.dictStr[nType]


class ETaskConst:
    eDisDeltaTime = 90  # 发布任务时间间隔
    eExecDeltaTime = 300  # 请求文件执行间隔
    eReturnDeltaTime = 90  # 返回结果间隔
