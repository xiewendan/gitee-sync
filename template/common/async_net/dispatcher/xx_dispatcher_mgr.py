# -*- coding: utf-8 -*-

# __author__ = xiaobao
# __date__ = 2021/3/11 20:28

# desc: dispatcher管理器，管理所有的dispatcher。其中，selectors等的event注册和响应，可以放到这里

__all__ = ["CreateDispatcher"]


class XxDispatcherMgr:
    """"""

    def __init__(self):
        import common.my_log as my_log
        import common.async_net.dispatcher.xx_dispatcher_factory as xx_dispatcher_factory

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictDispathcer = {}

        self.m_DispatcherFactory = xx_dispatcher_factory.XxDispatcherFactory()
        self.m_DispatcherFactory.RegisterAll()

    def CreateDispatcher(self, nType, dictData):
        self.m_LoggerObj.debug("type:%d, dictData:%s", nType, str(dictData))

        DispatcherObj = self.m_DispatcherFactory.CreateDispatcher(nType, dictData)

        self._AddDispatcher(DispatcherObj)

        return DispatcherObj.ID

    def GetDispatcher(self, nID):
        assert nID in self.m_dictDispathcer

        return self.m_dictDispathcer[nID]

    # ********************************************************************************
    # dictDispatcher
    # ********************************************************************************
    def _AddDispatcher(self, DispatcherObj):
        self.m_LoggerObj.debug("dispatcher id:%d", DispatcherObj.ID)

        nID = DispatcherObj.ID
        assert nID not in self.m_dictDispathcer

        self.m_dictDispathcer[nID] = DispatcherObj

    def _RemoveDispatcher(self, nID):
        self.m_LoggerObj.debug("dispatcher id:%d", nID)

        assert nID in self.m_dictDispathcer
        del self.m_dictDispathcer[nID]


g_DispatcherMgr = XxDispatcherMgr()
CreateDispatcher = g_DispatcherMgr.CreateDispatcher
GetDispatcher = g_DispatcherMgr.GetDispatcher
