# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:57

# desc: 测试类


import common.async_net.connection.xx_connection as xx_connection
import common.async_net.connection.xx_connection_base as xx_connection_base
import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher


class XxConnectionClient(xx_connection_base.XxConnectionBase):
    """"""

    def __init__(self, dictConnectionData):
        super().__init__(dictConnectionData)

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)


    @staticmethod
    def GetType():
        return xx_connection.EConnectionType.eClient

    @staticmethod
    def GetDispathcerType():
        return xx_dispatcher.EDispatcherType.eBuffer

    def Connect(self, szIp, nPort):
        self.m_LoggerObj.debug("id:%d, connectstate:%d, ip:%s, port:%d", self.m_nID, self.m_eConnectState, szIp, nPort)

        assert self.m_eConnectState in (xx_connection.EConnectionState.eDisconnected,)

        DispatcherObj = self._GetDispatcher()
        DispatcherObj.Connect(szIp, nPort)

        self.m_eConnectState = xx_connection.EConnectionState.eConnecting

    def _OnConnect(self):
        self.m_LoggerObj.debug("id:%d, connectstate:%d", self.m_nID, self.m_eConnectState)
        self.m_eConnectState = xx_connection.EConnectionState.eConnected
