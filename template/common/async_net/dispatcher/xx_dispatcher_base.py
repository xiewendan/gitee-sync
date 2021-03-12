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

        nSocketFamily = dictData["socket_family"]
        nSocketType = dictData["socket_type"]

        self.m_szIpPort = ""

        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eCreated

        self.m_SocketObj = self._CreateSocket(nSocketFamily, nSocketType, self.m_nID)

    @staticmethod
    def GetType():
        NotImplemented

    @property
    def ID(self):
        return self.m_nID

    @property
    def SocketObj(self):
        return self.m_SocketObj

    def _CreateSocket(self, nFamily, nType, nFileNo):
        self.m_LoggerObj.debug("family:%d, type:%d, fileno:%d", nFamily, nType, nFileNo)

        SocketObj = socket.socket(nFamily, nType, fileno=nFileNo)
        SocketObj.setblocking(False)

        return SocketObj

    def Bind(self, szIp, nPort):
        self.m_LoggerObj.debug("ip:%s, port:%d", szIp, nPort)
        # TODO 重复绑定相关端口，如何处理
        self.m_SocketObj.bind((szIp, nPort))

    def Listen(self, nCount):
        self.m_LoggerObj.debug("count:%d", nCount)
        self.m_SocketObj.listen(nCount)

    def SetReuseAddress(self):
        self.m_SocketObj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def Connect(self, szIp, nPort):
        assert self.m_eDispatcherState in (xx_dispatcher.EDispatcherState.eCreated,
                                           xx_dispatcher.EDispatcherState.eDisconnected)

        self.m_szIpPort = "%s:%d" % (szIp, nPort)
        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eConnecting

        self.m_LoggerObj.info("try connect ip_port:%s", self.m_szIpPort)

        nError = self.m_SocketObj.connect_ex((szIp, nPort))
        if nError in (EINPROGRESS, EALREADY, EWOULDBLOCK):
            return

        if nError in (0, EISCONN):
            self._HandleConnectEvent()

        else:
            raise OSError(nError, errorcode[nError])

    def Send(self, dictData):
        pass

    # ********************************************************************************
    # handle event
    # ********************************************************************************
    def _HandleConnectEvent(self):
        nError = self.m_SocketObj.getsockopt(socket.SOL_SOCKET, socket.SO_ERROR)
        if nError != 0:
            szError = nError in errorcode and errorcode["nError"] or "unknown error %s" % nError
            raise OSError(nError, szError)

        self.m_eDispatcherState = xx_dispatcher.EDispatcherState.eConnected
        self._HandleConnect()

    def _HandleDisconnectEvent(self):
        pass

    def _HandleReadEvent(self):
        pass

    def _HandleWriteEvent(self):
        pass

    # ********************************************************************************
    # callback
    # ********************************************************************************
    def _HandleConnect(self):
        self.m_LoggerObj.info("connect [ip:port]:%s", self.m_szIpPort)

        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnConnect(self.m_nID)

    def _HandleDisconnect(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnDisconnect(self.m_nID)

    def _HandleAccpet(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnAccept(self.m_nID)

    def _HandleRead(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnRead(self.m_nID)

    def _HandleWrite(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnWrite(self.m_nID)

    def _HandleClose(self):
        import common.async_net.xx_connection_mgr as xx_connection_mgr
        xx_connection_mgr.F_OnClose(self.m_nID)
