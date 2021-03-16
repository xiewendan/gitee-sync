class XxConnectionFactory:
    """"""

    def __init__(self):
        import common.my_log as my_log

        self.m_LoggerObj = my_log.MyLog(__file__)

        self.m_dictConnectionCls = {}

        self.m_nConnectionID = 0

    def RegisterAll(self):
        self.m_LoggerObj.info("register all connection class")

        import common.async_net.connection.xx_connection_client as xx_connection_client
        self._RegisterClass(xx_connection_client.XxConnectionClient)

        import common.async_net.connection.xx_connection_server as xx_connection_server
        self._RegisterClass(xx_connection_server.XxConnectionServer)

    def UnregisterAll(self):
        self.m_LoggerObj.info("unregister all connection class")
        self.m_dictConnectionCls = {}

    def CreateConnection(self, nType, dictConnectionData):
        assert nType in self.m_dictConnectionCls
        assert dictConnectionData is not None

        ConnectionCls = self.m_dictConnectionCls[nType]

        assert "id" not in dictConnectionData
        dictConnectionData["id"] = self._GenConnectionID()

        return ConnectionCls(dictConnectionData)

    def _GenConnectionID(self):
        self.m_nConnectionID += 1
        return self.m_nConnectionID

    def _RegisterClass(self, ConnectionClsObj):
        nType = ConnectionClsObj.GetType()
        assert nType not in self.m_dictConnectionCls

        self.m_dictConnectionCls[nType] = ConnectionClsObj
        self.m_LoggerObj.debug("register class type: %s", nType)

    def _UnregisterClass(self, ConnectionClsObj):
        nType = ConnectionClsObj.GetType()
        assert nType in self.m_dictConnectionCls
        del self.m_dictConnectionCls[nType]
        self.m_LoggerObj.debug("unregister class type: %s", nType)
