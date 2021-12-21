__all__ = ["EConnectionType"]


class EConnectionType:
    eServer = 1
    eClient = 2

    eReg = 3
    eExeInReg = 4
    eExe2Reg = 5

    eExe = 6
    eExeInExe = 7
    eExe2Exe = 8

    eFileExe = 9
    eFileExeInExe = 10
    eFileExe2Exe = 11

    dictMsg = {
        eServer: "Server",
        eClient: "Client",

        eReg: "Reg",
        eExeInReg: "ExeinReg",
        eExe2Reg: "Exe2Reg",

        eExe: "Exe",
        eExeInExe: "ExeInExe",
        eExe2Exe: "Exe2Exe",

        eFileExe: "FileExe",
        eFileExeInExe: "FileExeInExe",
        eFileExe2Exe: "FileExe2Exe",
    }

    @staticmethod
    def ToStr(eState):
        assert eState in EConnectionType.dictMsg
        return EConnectionType.dictMsg[eState]


class EConnectionState:
    eConnected = 1
    eConnecting = 2
    eDisconnecting = 3
    eDisconnected = 4
    eClose = 5
    eListening = 6
    eUnListen = 7

    dictMsg = {
        eConnected: "Connected",
        eConnecting: "Connecting",
        eDisconnecting: "Disconnecting",
        eDisconnected: "Disconnected",
        eClose: "Close",
        eListening: "Listening",
        eUnListen: "UnListen"
    }

    @staticmethod
    def ToStr(eState):
        assert eState in EConnectionState.dictMsg
        return EConnectionState.dictMsg[eState]


class EAsyncName:
    eRetAsyncID = "RetAsyncID"
    eAsyncID = "AsyncID"
