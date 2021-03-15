__all__ = ["EConnectionType"]


class EConnectionType:
    eServer = 1
    eClient = 2


class EConnectionState:
    eConnected = 1
    eConnecting = 2
    eDisconnecting = 3
    eDisconnected = 4
    eClose = 5
    eListening = 6
    eUnListen = 7
