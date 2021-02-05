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

            # 注册 listen socket
            self.m_XxSocketMgrObj.Register(self.m_SelectorObj)

            #


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
        self.m_dictIp2Port2Data = {}

    def Init(self):
        self.m_LoggerObj.debug("Init")

        self.m_SelectThreadObj = SelectorThread(self, self.m_nTimeout)
        self.m_SelectThreadObj.start()

    def Destroy(self):
        self.m_LoggerObj.debug("Destroy")

        self.m_SelectThreadObj.stop()
        self.m_SelectThreadObj.join()

    def Listen(self, szIp, nPort, nBacklog=1):
        """监听指定端口"""
        # TODO 边界：相同ip相同端口； 不同ip相同端口； 相同ip不同端口

        self.m_LoggerObj.info("ip:%s, port:%d", szIp, nPort)
        assert nBacklog >= 0, "back log %s" % nBacklog

        import socket
        import selectors
        import common.net.xx_socket as xx_socket

        self.m_RegisterLockObj.acquire()
        bHasListenSocket = self._HasListenSocket(szIp, nPort)
        self.m_RegisterLockObj.release()

        if bHasListenSocket:
            return

        SocketObj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        SocketObj.bind((szIp, nPort))   # TODO 监听相同端口会报错，需要处理
        SocketObj.listen(nBacklog)
        XxSocketObj = xx_socket.XxSocket(SocketObj)

        self.m_RegisterLockObj.acquire()
        if self._HasListenSocket(szIp, nPort):
            SocketObj.close()
        else:
            self._AddListenSocket(szIp, nPort, XxSocketObj)
            self.m_dictSocket2Register[XxSocketObj] = (selectors.EVENT_READ, self._Accept)
        self.m_RegisterLockObj.release()

    def Send(self, szIp, nPort, dictData):
        """发送数据到指定ip和端口"""
        # TODO 尚未有连接；以后连接；已有通过listen上来的连接
        # TODO 相同ip相同端口，在连接的间隔内，正在尝试连接，可以能会重复发起连接，会存在多个连接
        self.m_LoggerObj.debug("ip:%s, port:%d, data:%s", szIp, nPort, dictData)

        byteData = SerializeData(dictData)

        import socket

        self.m_RegisterLockObj.acquire()
        bHasEstablishSocket = self._HasEstablishSocket(szIp, nPort)
        self._AddSendData(szIp, nPort, byteData)
        self.m_RegisterLockObj.release()

        if bHasEstablishSocket:
            pass
        else:
            # TODO 需要异步创建socket，并发送数据
            SocketObj = socket.socket()
            SocketObj.connect((szIp, nPort))

            self.m_RegisterLockObj.acquire()

            if self._HasEstablishSocket(szIp, nPort):
                SocketObj.close()
            else:
                import common.net.xx_socket as xx_socket
                XxSocketObj = xx_socket.XxSocket(SocketObj)
                self._AddEstablishSocket(szIp, nPort, XxSocketObj)

            self.m_RegisterLockObj.release()

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

        # TODO AddrObj获得IP和端口
        szIp, nPort = AddrObj.IP, AddrObj.Port

        # 添加到管理器中
        self.m_RegisterLockObj.acquire()

        if self._HasEstablishSocket(szIp, nPort):
            ConnObj.close()
        else:
            SelectorObj.register(ConnObj, selectors.EVENT_READ, self._Read)
            XxSocketObj = xx_socket.XxSocket(ConnObj)
            XxSocketObj.SetState(xx_socket.ESocketState.eRegister)

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
            # SelectorObj.modify(ConnObj, selectors.EVENT_WRITE, self._Write)

        else:
            self.m_LoggerObj.info("closing:%s", str(ConnObj))
            SelectorObj.unregister(ConnObj)

            self.m_RegisterLockObj.acquire()
            self._RemoveEstablishSocketByObj(ConnObj)
            self.m_RegisterLockObj.release()

    def _Write(self, SelectorObj, ConnObj, nMask):
        self.m_LoggerObj.info("socket can write: %s", str(ConnObj))

        # import selectors
        # SelectorObj.modify(ConnObj, selectors.EVENT_READ, self._Read)

    def _ReadWrite(self, SelectorObj, ConnObj, nMask):
        self.m_LoggerObj.debug("socket can read or write, ConnObj:%s, Mask:%d", str(ConnObj), nMask)

        import selectors
        if nMask & selectors.EVENT_READ:
            self._Read(SelectorObj, ConnObj, nMask)
        elif nMask & selectors.EVENT_WRITE:
            self._Write(SelectorObj, ConnObj, nMask)

    # ********************************************************************************
    # listen socket
    # ********************************************************************************
    def _HasListenSocket(self, szIp, nPort):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""
        self.m_LoggerObj.debug("ip:%s, port:%d", szIp, nPort)

        if szIp not in self.m_dictIp2Port2ListenXxSocket:
            return False

        return nPort in self.m_dictIp2Port2ListenXxSocket[szIp]

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
    def _HasEstablishSocket(self, szIp, nPort):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""
        self.m_LoggerObj.debug("ip:%s, port:%d", szIp, nPort)

        if szIp not in self.m_dictIp2Port2EstablishXxSocket:
            return False

        return nPort in self.m_dictIp2Port2EstablishXxSocket[szIp]

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

    def _AddSendData(self, szIp, nPort, byteData):
        """外部调用，需要获得锁 self.m_RegisterLockObj.acquire()"""
        self.m_LoggerObj.debug("ip:%s, port:%d, data:%s", szIp, nPort, repr(byteData))

        if szIp not in self.m_dictIp2Port2Data:
            self.m_dictIp2Port2Data[szIp] = {}

        if nPort not in self.m_dictIp2Port2Data[szIp]:
            self.m_dictIp2Port2Data[szIp][nPort] = []

        self.m_dictIp2Port2Data[szIp][nPort].append(byteData)
