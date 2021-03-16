class XxDispatcherFactory:
    """"""

    def __init__(self):
        import common.my_log as my_log

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictDispatcherCls = {}

    def RegisterAll(self):
        self.m_LoggerObj.info("register all dispatcher class")

        import common.async_net.dispatcher.xx_buffer_dispatcher as xx_buffer_dispatcher
        self._RegisterClass(xx_buffer_dispatcher.XxBufferDispatcher)

    def UnregisterAll(self):
        self.m_LoggerObj.info("unregister all dispatcher class")
        self.m_dictDispatcherCls = {}

    def CreateDispatcher(self, nType, dictDispatcherData):
        self.m_LoggerObj.debug("type:%d, dictData:%s", nType, str(dictDispatcherData))

        assert nType in self.m_dictDispatcherCls
        DispatcherCls = self.m_dictDispatcherCls[nType]

        assert "id" in dictDispatcherData

        return DispatcherCls(dictDispatcherData)

    def _RegisterClass(self, DispatcherClsObj):
        nType = DispatcherClsObj.GetType()
        assert nType not in self.m_dictDispatcherCls

        self.m_dictDispatcherCls[nType] = DispatcherClsObj
        self.m_LoggerObj.debug("register class type: %s", nType)

    def _UnregisterClass(self, DispatcherClsObj):
        nType = DispatcherClsObj.GetType()
        assert nType in self.m_dictDispatcherCls
        del self.m_dictDispatcherCls[nType]
        self.m_LoggerObj.debug("unregister class type: %s", nType)
