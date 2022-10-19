# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:23

# desc: Socket，除了对Socket的接口进行一次异步封装之外，会新增OnConnected，OnDisconnect等接口，简化上层使用

import socket
from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, EISCONN, errorcode

import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher


class XxDispatcherBase:
    def __init__(self, dictData):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        # listen：为监听的地址
        # accept：为连接上来的地址
        # connect：希望连接的地址
        self.m_szIp = dictData.get("ip", "")
        self.m_nPort = dictData.get("port", 0)

        self.m_SocketObj = None

        self.m_nID = dictData["id"]

        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eCreated

    def Destroy(self):
        if self.m_SocketObj is not None:
            self.m_SocketObj.close()
            self.m_SocketObj = None

    @staticmethod
    def GetType():
        # noinspection PyStatementEffect
        NotImplementedError

    @property
    def ID(self):
        return self.m_nID

    @property
    def Ip(self):
        return self.m_szIp

    @property
    def Port(self):
        return self.m_nPort

    @property
    def SocketObj(self):
        return self.m_SocketObj

    def CreateSocket(self, nFamily, nType):
        self.m_LoggerObj.debug("family:%d, type:%d", nFamily, nType)

        SocketObj = socket.socket(nFamily, nType)
        SocketObj.setblocking(False)

        self.SetSocket(SocketObj)

    def SetSocket(self, SocketObj):
        if SocketObj is None:
            assert self.m_SocketObj is not None
        if SocketObj is not None:
            assert self.m_SocketObj is None

        self.m_SocketObj = SocketObj

    def Listen(self, nCount):
        self.m_LoggerObj.debug("count:%d", nCount)
        self.m_SocketObj.listen(nCount)

    def Bind(self, szIp, nPort):
        self.m_LoggerObj.debug("ip:%s, port:%d", szIp, nPort)
        # 未设置SO_REUSEADDR，所以绑定相同地址直接报错。避免绑定到相同地址，不好查问题
        self.m_szIp = szIp
        self.m_nPort = nPort
        self.m_SocketObj.bind((szIp, nPort))

    def SetReuseAddress(self):
        self.m_SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def Connect(self, szIp, nPort):
        assert self.m_eDispatcherState in (xx_dispatcher.EDispatcherState.eCreated,
                                           xx_dispatcher.EDispatcherState.eDisconnected)

        self.m_szIp = szIp
        self.m_nPort = nPort

        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eConnecting

        self.m_LoggerObj.info("try connect ip:%s, port:%d", szIp, nPort)

        nError = self.m_SocketObj.connect_ex((szIp, nPort))

        if nError in (EINPROGRESS, EALREADY, EWOULDBLOCK):
            self.m_LoggerObj.debug("try:connecting....:%d", nError)
            return

        if nError in (0, EISCONN):
            pass

        else:
            raise OSError(nError, errorcode[nError])

    def Send(self, dictData):
        # noinspection PyStatementEffect
        NotImplementedError

    def SendFile(self, dictData):
        # noinspection PyStatementEffect
        NotImplementedError

    def Close(self):
        if self.m_eDispatcherState in (
                xx_dispatcher.EDispatcherState.eConnecting, xx_dispatcher.EDispatcherState.eConnected):
            import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
            xx_dispatcher_mgr.HandleDisconnectEvent(self.m_nID)
        elif self.m_eDispatcherState == xx_dispatcher.EDispatcherState.eDisconnected:
            pass
        else:
            assert False

    def GetDataColName(self):
        return "%8s %16s %16s %12s" % ("ID", "DispatcherState", "Ip", "Port")

    def GetDataStr(self):
        szDispatcherState = xx_dispatcher.EDispatcherState.ToStr(self.m_eDispatcherState)

        return "%8s %16s %16s %12s" % (self.m_nID, szDispatcherState, self.Ip, self.Port)

    # ********************************************************************************
    # handle event
    # ********************************************************************************
    def HandleConnectEvent(self):
        nError = self.m_SocketObj.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if nError != 0:
            szError = nError in errorcode and errorcode[nError] or "unknown error %s" % nError
            szData = "ip:%s, port:%d" % (self.Ip, self.Port)
            raise OSError(nError, szError + szData)

        self._OnConnect()

        self._HandleConnect()

    def HandleDisconnectEvent(self):
        self._OnDisconnect()

        self._HandleDisconnect()

    def HandleReadEvent(self):
        self._HandleRead()

    def HandleWriteEvent(self):
        self._HandleWrite()

    def HanleAcceptEvent(self):
        return self._HandleAccept()

    # ********************************************************************************
    # callback
    # ********************************************************************************
    def _OnConnect(self):
        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eConnected

    def _HandleConnect(self):
        self.m_LoggerObj.info("connect, ip:%s, port:%d", self.m_szIp, self.m_nPort)

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnConnect(self.m_nID)

    def _OnDisconnect(self):
        self.m_SocketObj.close()
        self.SetSocket(None)

        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eDisconnected

    def _HandleDisconnect(self):
        self.m_LoggerObj.info("disconnected, ip:%s, port:%d", self.m_szIp, self.m_nPort)

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnDisconnect(self.m_nID)

    def _HandleRead(self):
        # noinspection PyStatementEffect
        NotImplementedError

    def _HandleWrite(self):
        # noinspection PyStatementEffect
        NotImplementedError

    def _HandleClose(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnClose(self.m_nID)

    def _HandleAccept(self):
        try:
            SocketObj, AddrObj = self.m_SocketObj.accept()
        except OSError:
            raise

        szIp, nPort = AddrObj
        self.m_LoggerObj.info("new client come, ip:%s, port:%d", szIp, nPort)

        assert szIp is not None
        assert nPort is not None

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        nClientID = xx_connection_mgr.F_Accept(self.m_nID, szIp, nPort)
        nDispatcherID = nClientID

        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.SetSocket(nDispatcherID, SocketObj)
        xx_dispatcher_mgr.HandleConnectEvent(nDispatcherID)
