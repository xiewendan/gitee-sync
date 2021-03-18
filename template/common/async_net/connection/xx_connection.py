__all__ = ["EConnectionType"]


class EConnectionType:
    eServer = 1
    eClient = 2
    eExecutor = 3
    eRegisterServer = 4
    eExecutorInRegister = 5


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
