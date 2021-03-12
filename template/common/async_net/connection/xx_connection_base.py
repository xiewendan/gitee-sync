# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:24

# desc: 维护连接状态、重连、并统计发送包数据，连接断开的逻辑处理，重连的逻辑处理


import common.async_net.connection.xx_connection as xx_connection
import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr


class XxConnectionBase:
    """"""

    def __init__(self, dictConnectionData):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_nID = dictConnectionData["id"]

        self.m_nDispatcherID = self._CreateDispatch(dictConnectionData)

        self.m_eConnectState = xx_connection.EConnectionState.eDisconnected

    @staticmethod
    def GetType():
        NotImplemented

    @staticmethod
    def GetDispathcerType():
        NotImplemented

    @property
    def ID(self):
        return self.m_nID

    def _CreateDispatch(self, dictConnectionData):
        nDispatcherType = self.GetDispathcerType()
        return xx_dispatcher_mgr.CreateDispatcher(nDispatcherType, dictConnectionData)

    def _GetDispatcher(self):
        return xx_dispatcher_mgr.GetDispatcher(self.m_nDispatcherID)

    def Send(self, dictData):
        self.m_LoggerObj.debug("data:%s", str(dictData))

        assert self.m_eConnectState in (xx_connection.EConnectionState.eConnecting,)

        DispatcherObj = self._GetDispatcher()
        DispatcherObj.Send(dictData)

    # ********************************************************************************
    # callback
    # ********************************************************************************
    def F_OnConnect(self):
        self._OnConnect()

    def _OnConnect(self):
        pass

    def F_OnDisconnect(self):
        self._OnDisconnect()

    def _OnDisconnect(self):
        pass

    def F_OnAccept(self):
        self._OnAccept()

    def _OnAccept(self):
        pass

    def F_OnRead(self):
        self._OnRead()

    def _OnRead(self):
        pass

    def F_OnWrite(self):
        self._OnWrite()

    def _OnWrite(self):
        pass

    def F_OnClose(self):
        self._OnClose()

    def _OnClose(self):
        pass
