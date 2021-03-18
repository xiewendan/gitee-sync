# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/18 21:06

# desc:

import common.async_net.connection.xx_connection_base as xx_connection_base


class ExecutorConnectionInRegister(xx_connection_base.XxConnectionBase):
    def __init__(self, dictData):
        super().__init__(dictData)

        import common.my_log as my_log
        self.m_LoggerObj = my_log.MyLog(__file__)

    @staticmethod
    def GetType():
        import common.async_net.connection.xx_connection as xx_connection
        return xx_connection.EConnectionType.eExecutorInRegister

    @staticmethod
    def GetDispathcerType():
        import common.async_net.dispatcher.xx_dispatcher as xx_dispatcher
        return xx_dispatcher.EDispatcherType.eBuffer

    def _OnConnect(self):
        self.m_LoggerObj.debug("nConnID:%d", self.ID)

        super()._OnConnect()

        dictData = {
            "ip": self.Ip,
            "port": self.Port
        }

        import logic.server.executor_mgr as executor_mgr
        executor_mgr.AddExecutorData(self.ID, dictData)

    def _OnDisconnect(self):
        self.m_LoggerObj.debug("nConnID:%d", self.ID)

        super()._OnDisconnect()

        import logic.server.executor_mgr as executor_mgr
        executor_mgr.RemoveExecutorData(self.ID)
