# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:24

# desc: 维护连接状态、重连、并统计发送包数据，连接断开的逻辑处理，重连的逻辑处理


import common.async_net.connection.xx_connection as xx_connection


class XxConnectionBase:
    """"""

    def __init__(self, dictConnectionData):
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_nID = dictConnectionData["id"]

        nDispatcherID = self._CreateDispatch(dictConnectionData)
        assert self.m_nID == nDispatcherID

        self.m_eConnectState = xx_connection.EConnectionState.eDisconnected

        self.m_bConnectionAccpeted = dictConnectionData["connection_accepted"]

    def Destroy(self):
        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.DestroyDispatcher(self.m_nID)

    def Close(self):
        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.CloseDispatcher(self.ID)

    @staticmethod
    def GetType():
        # noinspection PyStatementEffect
        NotImplementedError

    @staticmethod
    def GetDispathcerType():
        # noinspection PyStatementEffect
        NotImplementedError

    @property
    def ID(self):
        return self.m_nID

    @property
    def DispatcherID(self):
        return self.m_nID

    @property
    def Ip(self):
        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        return xx_dispatcher_mgr.GetIp(self.DispatcherID)

    @property
    def Port(self):
        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        return xx_dispatcher_mgr.GetPort(self.DispatcherID)

    def Send(self, dictData):
        self.m_LoggerObj.debug("data:%s", Str(dictData))

        if self.m_eConnectState not in (xx_connection.EConnectionState.eConnected,):
            self.m_LoggerObj.error("failed, not connected, ID:%d, ConnectState:%d", self.m_nID, self.m_eConnectState)
            return False

        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.Send(self.DispatcherID, dictData)

    def SendFile(self, dictData):
        self.m_LoggerObj.debug("data:%s", Str(dictData))

        if self.m_eConnectState not in (xx_connection.EConnectionState.eConnected,):
            self.m_LoggerObj.error("failed, not connected, ID:%d, ConnectState:%d", self.m_nID, self.m_eConnectState)
            return False

        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr
        xx_dispatcher_mgr.SendFile(self.DispatcherID, dictData)

    # ********************************************************************************
    # private
    # ********************************************************************************

    def _CreateDispatch(self, dictConnectionData):
        import common.async_net.dispatcher.xx_dispatcher_mgr as xx_dispatcher_mgr

        nDispatcherType = self.GetDispathcerType()
        return xx_dispatcher_mgr.CreateDispatcher(nDispatcherType, dictConnectionData)

    def _SetConnectState(self, nState):
        self.m_LoggerObj.debug("change state from %s to %s",
                               xx_connection.EConnectionState.ToStr(self.m_eConnectState),
                               xx_connection.EConnectionState.ToStr(nState))

        dictState = {
            xx_connection.EConnectionState.eConnected:
                (xx_connection.EConnectionState.eConnecting,
                 xx_connection.EConnectionState.eDisconnected),

            xx_connection.EConnectionState.eConnecting:
                (xx_connection.EConnectionState.eConnected,
                 xx_connection.EConnectionState.eConnecting,
                 xx_connection.EConnectionState.eDisconnected,
                 None),

            xx_connection.EConnectionState.eDisconnected:
                (xx_connection.EConnectionState.eConnecting,
                 xx_connection.EConnectionState.eConnected,
                 ),

            xx_connection.EConnectionState.eUnListen:
                (xx_connection.EConnectionState.eDisconnected,),

            xx_connection.EConnectionState.eListening:
                (xx_connection.EConnectionState.eUnListen,),
        }

        assert self.m_eConnectState in dictState[nState]

        self.m_eConnectState = nState

    def F_IsConnectionAccpeted(self):
        return self.m_bConnectionAccpeted

    def F_GetDataStr(self):
        import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher

        szConnectState = xx_connection.EConnectionState.ToStr(self.m_eConnectState)
        szConnectType = xx_connection.EConnectionType.ToStr(self.GetType())
        szDispatcherType = xx_dispatcher.EDispatcherType.ToStr(self.GetDispathcerType())

        return "%8s %16s %10s %16s %12s %12s %15s" % (
            self.m_nID, szConnectState, self.m_bConnectionAccpeted, self.Ip, self.Port, szConnectType, szDispatcherType)

    def F_GetDataColName(self):
        return "%8s %16s %10s %16s %12s %12s %15s" % ("ConnID", "ConnectState", "Accepted", "ip", "port", "ConnectType", "DispatcherType")

    # ********************************************************************************
    # callback
    # ********************************************************************************
    def F_OnConnect(self):
        self._OnConnect()

    def _OnConnect(self):
        self.m_LoggerObj.debug("id:%d, connectstate:%d", self.m_nID, self.m_eConnectState)
        self._SetConnectState(xx_connection.EConnectionState.eConnected)

    def F_OnDisconnect(self):
        self._OnDisconnect()

    def _OnDisconnect(self):
        self.m_LoggerObj.debug("id:%d, connectstate:%d", self.m_nID, self.m_eConnectState)
        self._SetConnectState(xx_connection.EConnectionState.eDisconnected)

        if self.m_bConnectionAccpeted:
            import common.async_net.xx_connection_mgr as xx_connection_mgr
            xx_connection_mgr.F_SetConnectionToDestroy(self.m_nID)

    def F_Accept(self, szIp, nPort):
        return self._Accept(szIp, nPort)

    def _Accept(self, szIp, nPort):
        # noinspection PyStatementEffect
        NotImplementedError

    def F_OnRead(self, dictData):
        return self._OnRead(dictData)

    def _OnRead(self, dictData):
        self.m_LoggerObj.info("dictData:%s", Str(dictData))
        import logic.connection.message_dispatcher as message_dispatcher

        return message_dispatcher.OnRecv(self.m_nID, dictData)

    def F_OnClose(self):
        self._OnClose()

    def _OnClose(self):
        self.m_LoggerObj.debug("id:%d, connectstate:%d", self.m_nID, self.m_eConnectState)
        self._SetConnectState(xx_connection.EConnectionState.eClose)
