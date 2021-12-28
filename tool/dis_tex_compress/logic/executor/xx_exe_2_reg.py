# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:05

# desc:

import common.async_net.connection.xx_connection_client as xx_connection_client


class XxExe2Reg(xx_connection_client.XxConnectionClient):
    """"""

    def __init__(self, dictData):
        super().__init__(dictData)
        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_ExecutorObj = dictData["executor"]

        self.m_szTickID = None
        self.m_nAutoReconnectCount = 0
        self.m_nAutoReconnectMaxCount = dictData["auto_reconnect_max_count"]
        self.m_nAutoReconnectInterval = dictData["auto_reconnect_interval"]

    @staticmethod
    def GetType():
        import common.async_net.connection.xx_connection as xx_connection
        return xx_connection.EConnectionType.eExe2Reg

    def _OnConnect(self):
        super()._OnConnect()

        import logic.connection.message_dispatcher as message_dispatcher

        dictData = {
            "listen_ip": self.m_ExecutorObj.ListenIp,
            "listen_port": self.m_ExecutorObj.ListenPort
        }

        self.m_LoggerObj.info("Update exe listen ip and port to register server, listen ip:%s, port:%d", self.m_ExecutorObj.ListenIp, self.m_ExecutorObj.ListenPort)
        message_dispatcher.CallRpc(self.ID, "logic.register.executor_mgr", "UpdateExecutorData", [dictData])

        self.m_nAutoReconnectCount = 0
        self._UnRegisterAutoReconnect()

    def _OnDisconnect(self):
        self.m_LoggerObj.debug("")

        super()._OnDisconnect()

        self.m_nAutoReconnectCount = 0
        self._RegisterAutoReconnect()

    def _RegisterAutoReconnect(self):
        self._UnRegisterAutoReconnect()

        self.m_szTickID = g_AppObj.GetService("scheduler").GetSchedulerMgr().RegisterTick("executor_auto_connect",
                                                                                          self.m_nAutoReconnectInterval,
                                                                                          self._AutoConnectCB,
                                                                                          tupleArgs=None)

    def _UnRegisterAutoReconnect(self):
        if self.m_szTickID is not None:
            g_AppObj.GetService("scheduler").GetSchedulerMgr().UnregisterTick(self.m_szTickID)
            self.m_szTickID = None

    def _AutoConnectCB(self):
        self.m_LoggerObj.debug("")

        if self.m_nAutoReconnectCount < self.m_nAutoReconnectMaxCount:
            self.m_nAutoReconnectCount += 1
            self.Connect(self.Ip, self.Port)

        else:
            self._UnRegisterAutoReconnect()
            self.m_LoggerObj.error("reconnect failed!")

    def F_GetDataStr(self):
        szDataStr = super().F_GetDataStr()

        return szDataStr + " %22s %22s %22s" % (
            self.m_nAutoReconnectCount, self.m_nAutoReconnectMaxCount, self.m_nAutoReconnectInterval)

    def F_GetDataColName(self):
        szDataColName = super().F_GetDataColName()
        return szDataColName + " %22s %22s %22s" % (
            "AutoReconnectCount", "AutoReconnectMaxCount", "AutoReconnectInterval")
