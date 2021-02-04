# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/2/4 12:00

# desc: 管理所有的XxSocket对象
# 名词注释：
#   1 Listen：表示监听，用于监听连接
#   2 Establish: 表示建立连接，用于传输数据

import threading


class SelectorThread(threading.Thread):
    """Selector监控所有创建的socket，读和写都会从这里触发回调给上层"""

    def __init__(self, XxSocketMgrObj, nTimeout):
        import selectors
        import common.my_log as my_log

        super().__init__()

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_bRunning = True
        self.m_nTimeout = nTimeout
        self.m_XxSocketMgrObj = XxSocketMgrObj
        self.m_SelectorObj = selectors.DefaultSelector()

    def stop(self):
        self.m_bRunning = False

    def run(self):
        self.m_LoggerObj.info("run")

        while self.m_bRunning:
            # 监听处理回调
            listEvent = self.m_SelectorObj.select(self.m_nTimeout)
            for KeyObj, nMask in listEvent:
                CallbackObj = KeyObj.data
                CallbackObj(self.m_SelectorObj, KeyObj.fileobj, nMask)

            # 新增注册socket
            self.m_XxSocketMgrObj.Register(self.m_SelectorObj)


def SerializeData(dictData):
    import json
    return json.dumps(dictData).encode("utf-8")


def UnserializeData(szData):
    import json
    return json.loads(szData).decode("utf-8")


class XxSocketMgr:
    def __init__(self, nTimeout):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_SelectThreadObj = None

        assert nTimeout >= 0, "超时不能小于0"
        self.m_nTimeout = nTimeout

        # ip-port -> socket
        self.m_listListenList = []

        # send msg -> pack data
        self.m_listSendData = []

        # send data -> create socket

        # socket sending data

        # socket

        # establish socket
        self.m_dictIp2Port2EstablishXxSocket = {}  # self.m_dictIp2Port2EstablishSocket[IP][nPort] = SocketObj
        self.m_dictEstablishSocket2IpPort = {}  # self.m_dictEstablishSocket2IpPort = (ip, port)

        # listen socket
        self.m_dictIp2Port2ListenXxSocket = {}  # self.m_dictIp2Port2ListenXxSocket[IP][nPort] = XxSocketObj
        self.m_dictListenSocket2IpPort = {}  # self.m_dictListenSocket2IpPort = (ip, port)

        # socket wait register
        self.m_RegisterLockObj = threading.Lock()
        self.m_dictSocket2Register = {}

        # data wait to send

    def Init(self):
        self.m_LoggerObj.debug("Init")

        self.m_SelectThreadObj = SelectorThread(self, self.m_nTimeout)
        self.m_SelectThreadObj.start()

    def Destroy(self):
        self.m_LoggerObj.debug("Destroy")

        self.m_SelectThreadObj.stop()
        self.m_SelectThreadObj.join()

    def Listen(self, szIp, nPort, nBacklog=1):
        self.m_LoggerObj.info("ip:%s, port:%d", szIp, nPort)
        assert nBacklog >= 0, "back log %s" % nBacklog

        import socket
        import selectors
        import common.net.xx_socket as xx_socket

        SocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SocketObj.bind((szIp, nPort))
        SocketObj.listen(nBacklog)
        XxSocketObj = xx_socket.XxSocket(SocketObj)

        self.m_RegisterLockObj.acquire()

        self._AddListenSocket(szIp, nPort, XxSocketObj)
        self.m_dictSocket2Register[XxSocketObj] = (selectors.EVENT_READ, self._Accept)

        self.m_RegisterLockObj.release()

    def Send(self, szIp, nPort, dictData):
        self.m_LoggerObj.debug("ip:%s, port:%d, data:%s", szIp, nPort, dictData)

        byteData = SerializeData(dictData)

        pass

    # ********************************************************************************
    # selector 注册和相应的回调函数
    # ********************************************************************************
    def Register(self, SelectorObj):
        import common.net.xx_socket as xx_socket

        self.m_RegisterLockObj.acquire()

        for XxSocketObj, tupleRegisterValue in self.m_dictSocket2Register.items():
            eEvent, CallbackFunc = tupleRegisterValue
            SelectorObj.register(XxSocketObj.GetSocketObj(), eEvent, CallbackFunc)
            XxSocketObj.SetState(xx_socket.ESocketState.eRegister)

        self.m_dictSocket2Register = {}

        self.m_RegisterLockObj.release()

    def _Accept(self, SelectorObj, ListenSocketObj, nMask):
        import selectors
        import common.net.xx_socket as xx_socket

        ConnObj, AddrObj = ListenSocketObj.accept()
        self.m_LoggerObj.info("new client com:%s", str(AddrObj))
        SelectorObj.register(ConnObj, selectors.EVENT_READ, self._Read)

        XxSocketObj = xx_socket.XxSocket(ConnObj)
        XxSocketObj.SetState(xx_socket.ESocketState.eRegister)

        # TODO AddrObj获得IP和端口
        szIp, nPort = AddrObj.IP, AddrObj.Port

        # 添加到管理器中
        self.m_RegisterLockObj.acquire()

        self._AddEstablishSocket(szIp, nPort, XxSocketObj)

        self.m_RegisterLockObj.release()

    def _Read(self, SelectorObj, ConnObj, nMask):
        self.m_LoggerObj.info("socket can read: %s", str(ConnObj))

        import selectors

        try:
            byteData = ConnObj.recv(1024)
        except BaseException as e:
            SelectorObj.unregister(ConnObj)
            self.m_RegisterLockObj.acquire()
            self._RemoveEstablishSocketByObj(ConnObj)
            self.m_RegisterLockObj.release()

            self.m_LoggerObj.error("socket recv data failed:", e)
            return

        if byteData:
            self.m_LoggerObj.info("echoing:%s to %s", repr(byteData), str(ConnObj))
            SelectorObj.modify(ConnObj, selectors.EVENT_WRITE, self._Write)

        else:
            self.m_LoggerObj.info("closing:%s", str(ConnObj))
            SelectorObj.unregister(ConnObj)

            self.m_RegisterLockObj.acquire()
            self._RemoveEstablishSocketByObj(ConnObj)
            self.m_RegisterLockObj.release()

    def _Write(self, SelectorObj, ConnObj, nMask):
        self.m_LoggerObj.info("socket can write: %s", str(ConnObj))

        import selectors
        SelectorObj.modify(ConnObj, selectors.EVENT_READ, self._Read)

    # ********************************************************************************
    # listen socket
    # ********************************************************************************
    def _AddListenSocket(self, szIp, nPort, ListenXxSocketObj):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""

        self.m_LoggerObj.debug("ip:%s, port:%d, obj:%s", szIp, nPort, str(ListenXxSocketObj))

        if szIp not in self.m_dictIp2Port2ListenXxSocket:
            self.m_dictIp2Port2ListenXxSocket[szIp] = {}

        assert nPort not in self.m_dictIp2Port2ListenXxSocket
        self.m_dictIp2Port2ListenXxSocket[szIp][nPort] = ListenXxSocketObj

        SocketObj = ListenXxSocketObj.GetSocketObj()
        assert SocketObj not in self.m_dictListenSocket2IpPort
        self.m_dictListenSocket2IpPort[ListenXxSocketObj.GetSocketObj()] = (szIp, nPort)

    def _RemoveListenSocket(self, szIp, nPort):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""

        self.m_LoggerObj.debug("ip:%s, port:%d", szIp, nPort)

        ListenXxSocketObj = self.m_dictIp2Port2ListenXxSocket[szIp][nPort]
        del self.m_dictListenSocket2IpPort[ListenXxSocketObj.GetSocketObj()]
        del self.m_dictIp2Port2ListenXxSocket[szIp][nPort]

    def _RemoveListenSocketByObj(self, SocketObj):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""

        self.m_LoggerObj.debug("%s", str(SocketObj))

        szIp, nPort = self.m_dictListenSocket2IpPort[SocketObj]
        del self.m_dictListenSocket2IpPort[SocketObj]
        del self.m_dictIp2Port2ListenXxSocket[szIp][nPort]

    # ********************************************************************************
    # establish socket
    # ********************************************************************************
    def _AddEstablishSocket(self, szIp, nPort, EstablishXxSocketObj):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""

        self.m_LoggerObj.debug("ip:%s, port:%d, obj:%s", szIp, nPort, str(EstablishXxSocketObj))

        if szIp not in self.m_dictIp2Port2EstablishXxSocket:
            self.m_dictIp2Port2EstablishXxSocket[szIp] = {}

        assert nPort not in self.m_dictIp2Port2EstablishXxSocket[szIp]
        self.m_dictIp2Port2EstablishXxSocket[szIp][nPort] = EstablishXxSocketObj

        EstablishSocketObj = EstablishXxSocketObj.GetSocketObj()
        assert EstablishSocketObj not in self.m_dictEstablishSocket2IpPort
        self.m_dictEstablishSocket2IpPort[EstablishSocketObj] = (szIp, nPort)

    def _RemoveEstablishSocket(self, szIp, nPort):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""

        self.m_LoggerObj.debug("ip:%s, port:%d", szIp, nPort)

        EstablishXxSocketObj = self.m_dictIp2Port2EstablishXxSocket[szIp][nPort]
        del self.m_dictEstablishSocket2IpPort[EstablishXxSocketObj.GetSocketObj()]
        del self.m_dictIp2Port2EstablishXxSocket[szIp][nPort]

    def _RemoveEstablishSocketByObj(self, SocketObj):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""

        self.m_LoggerObj.debug("%s", str(SocketObj))

        szIp, nPort = self.m_dictEstablishSocket2IpPort[SocketObj]
        del self.m_dictEstablishSocket2IpPort[SocketObj]
        del self.m_dictIp2Port2EstablishXxSocket[szIp][nPort]
