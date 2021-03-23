class EDispatcherType:
    eBuffer = 1

    dictMsg = {
        eBuffer: "Buffer",
    }

    @staticmethod
    def ToStr(eState):
        assert eState in EDispatcherType.dictMsg
        return EDispatcherType.dictMsg[eState]


class EDispatcherState:
    eCreated = 1
    eConnected = 2
    eConnecting = 3
    eClosing = 4
    eDisconnected = 5

    dictMsg = {
        eCreated: "Created",
        eConnected: "Connected",
        eConnecting: "Connecting",
        eClosing: "Closing",
        eDisconnected: "Disconnected",
    }

    @staticmethod
    def ToStr(eState):
        assert eState in EDispatcherState.dictMsg
        return EDispatcherState.dictMsg[eState]
