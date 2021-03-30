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
        assert szType in EIotType.dictType
        return EIotType.dictType[szType]

    @staticmethod
    def ToStr(nType):
        assert nType in EIotType.dictStr
        return EIotType.dictStr[nType]


class ETaskConst:
    eDisDeltaTime = 60
