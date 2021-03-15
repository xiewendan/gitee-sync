# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:23

# desc: Socket，除了对Socket的接口进行一次异步封装之外，会新增OnConnected，OnDisconnect等接口，简化上层使用

import socket
from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, EISCONN, errorcode

import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher


class XxDispatcherBase:
    """"""

    def __init__(self, dictData):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_nID = dictData["id"]

        self.m_szIp = ""
        self.m_nPort = 0

        self.m_SocketObj = None

        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eCreated

    def Destroy(self):
        if self.m_SocketObj is not None:
            self.m_SocketObj.close()
            self.m_SocketObj = None

    @staticmethod
    def GetType():
        NotImplemented

    @property
    def ID(self):
        return self.m_nID

    @property
    def SocketObj(self):
        return self.m_SocketObj

    def CreateSocket(self, nFamily, nType):
        self.m_LoggerObj.debug("family:%d, type:%d, fileno:%d", nFamily, nType)

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

        # TODO 重复绑定相关端口，如何处理
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
            return

        if nError in (0, EISCONN):
            import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
            xx_dispatcher_mgr.HandleConnectEvent(self.m_nID)

        else:
            raise OSError(nError, errorcode[nError])

    def Send(self, dictData):
        NotImplementedError

    # ********************************************************************************
    # handle event
    # ********************************************************************************
    def HandleConnectEvent(self):
        nError = self.m_SocketObj.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if nError != 0:
            szError = nError in errorcode and errorcode["nError"] or "unknown error %s" % nError
            raise OSError(nError, szError)

        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eConnected
        self._HandleConnect()

    def HandleDisconnectEvent(self):
        self._HandleDisconnect()

    def HandleReadEvent(self, byteData):
        self._HandleRead(byteData)

    def HandleWriteEvent(self):
        self._HandleWrite()

    def _HandleWriteEvent(self):
        self._HandleWrite()

    def HanleAcceptEvent(self, SocketObj, szIp, nPort):
        return self._HandleAccept(SocketObj, szIp, nPort)

    # ********************************************************************************
    # callback
    # ********************************************************************************
    def _HandleConnect(self):
        self.m_LoggerObj.info("connect ip:%s, port:%d", self.m_szIp, self.m_nPort)

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnConnect(self.m_nID)

    def _HandleDisconnect(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnDisconnect(self.m_nID)

    def _HandleAccpet(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_Accept(self.m_nID)

    def _HandleRead(self, byteData):
        NotImplementedError

    def _HandleWrite(self):
        NotImplementedError

    def _HandleClose(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnClose(self.m_nID)

    def _HandleAccept(self, SocketObj, szIp, nPort):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        return xx_connection_mgr.F_Accept(self.m_nID, SocketObj, szIp, nPort)
