class XxDispatcherFactory:
    """"""

    def __init__(self):
        import common.my_log as my_log

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictDispatcherCls = {}

    def RegisterAll(self):
        self.m_LoggerObj.debug("register all dispatcher class")

        import os
        import common.util as util
        import common.async_net.dispatcher.xx_dispatcher_base as xx_dispatcher_base

        szCwd = os.getcwd()
        listDispatcherClassObj = []
        listDispatcherClassObj.extend(
            util.FilterClassObj(
                os.path.join(szCwd, "common/async_net/dispatcher"),
                r"^xx_[_a-zA-Z0-9]*.py$",
                xx_dispatcher_base.XxDispatcherBase))

        for DispatcherClassObj in listDispatcherClassObj:
            self._RegisterClass(DispatcherClassObj)

    def UnregisterAll(self):
        self.m_LoggerObj.debug("unregister all dispatcher class")
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
